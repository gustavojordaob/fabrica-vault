"""
indexar_obsidian_chroma.py
Sobe o servidor HTTP RAG (ChromaDB + híbrido BM25/RRF/rerank) — NÃO indexa.

Indexação: use somente indexar_rapido.py

Instalar dependências:
    pip install chromadb sentence-transformers rank-bm25

Uso:
    python indexar_rapido.py                              # indexa o vault
    python indexar_obsidian_chroma.py --server            # sobe HTTP na porta 7332
    python indexar_obsidian_chroma.py --buscar "firebase" # testa busca (servidor não precisa estar up)
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Windows: evita UnicodeEncodeError nos prints (box drawing / emojis)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import os

from chroma_lock import limpar_pid_servidor, registrar_servidor

CHROMA_PATH = Path(
    os.environ.get("RAG_CHROMA_PATH", "C:/Users/gusta/obsidian/.chroma_db")
)
COLLECTION_NAME = "fabrica-knowledge"
MODEL_NAME = os.environ.get(
    "RAG_MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2"
)
MAX_RESULTS = int(os.environ.get("RAG_MAX_RESULTS", "5"))
# 127.0.0.1 local; 0.0.0.0 no Docker/App Runner
RAG_BIND = os.environ.get("RAG_BIND", "127.0.0.1")
RAG_API_KEY = os.environ.get("RAG_API_KEY", "").strip()
# Local: aws-rag/static; Docker: /app/static
_STATIC_CANDIDATES = [
    Path(os.environ.get("RAG_STATIC_PATH", "")),
    Path(__file__).resolve().parent / "aws-rag" / "static",
    Path(__file__).resolve().parent / "static",
    Path("/app/static"),
]


def _static_dir():
    for p in _STATIC_CANDIDATES:
        if p and (p / "index.html").is_file():
            return p
    return None


def buscar(collection, model, query, n=MAX_RESULTS, projeto=None):
    from rag_retrieval import buscar_hibrido

    return buscar_hibrido(collection, model, query, n, projeto=projeto)


def _sync_chroma_from_s3():
    """Baixa índice pré-indexado do S3 (App Runner). No-op se RAG_S3_BUCKET vazio."""
    bucket = os.environ.get("RAG_S3_BUCKET", "").strip()
    if not bucket:
        return
    import boto3

    prefix = os.environ.get("RAG_S3_CHROMA_PREFIX", "chroma").rstrip("/") + "/"
    dest = CHROMA_PATH
    dest.mkdir(parents=True, exist_ok=True)
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    print(f"📥  Sync Chroma s3://{bucket}/{prefix} → {dest}")
    sys.stdout.flush()
    s3 = boto3.client("s3", region_name=region)
    token = None
    n = 0
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix}
        if token:
            kw["ContinuationToken"] = token
        resp = s3.list_objects_v2(**kw)
        for obj in resp.get("Contents") or []:
            key = obj["Key"]
            if key.endswith("/"):
                continue
            rel = key[len(prefix) :]
            if not rel:
                continue
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(bucket, key, str(out))
            n += 1
        if not resp.get("IsTruncated"):
            break
        token = resp.get("NextContinuationToken")
    print(f"✅  {n} arquivos baixados do S3")
    sys.stdout.flush()


def iniciar_servidor(porta=7332, device="cpu"):
    """Sobe HTTP imediatamente (/health) e carrega modelo+Chroma em background.

    Necessário no App Runner: health check falha se a porta só abre após o warmup.
    """
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    state = {
        "ready": False,
        "error": None,
        "collection": None,
        "model": None,
        "chunks": None,
        "pools": None,
    }
    static_root = _static_dir()

    class RAGHandler(BaseHTTPRequestHandler):
        def _unauthorized(self):
            self.send_response(401)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"error":"unauthorized"}')

        def _check_auth(self) -> bool:
            if not RAG_API_KEY:
                return True
            got = self.headers.get("X-RAG-Key") or self.headers.get("x-rag-key") or ""
            return got == RAG_API_KEY

        def _send_json(self, code: int, body: dict):
            raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)

        def _send_file(self, path: Path, content_type: str):
            data = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _health_body(self) -> dict:
            rerank = os.environ.get("RAG_RERANK", "1").strip().lower() not in (
                "0",
                "false",
                "no",
                "off",
            )
            # Não importar rag_retrieval aqui — no boot do App Runner isso
            # compete com o warmup e pode matar a instância (OOM / health fail).
            chunks = state["chunks"]
            if chunks is None and state["collection"] is not None:
                try:
                    chunks = state["collection"].count()
                    state["chunks"] = chunks
                except Exception:
                    chunks = None
            pools = state.get("pools") or {
                "dense": 48,
                "bm25": 48,
                "meta": 32,
                "rerank": int(os.environ.get("RAG_RERANK_POOL", "24")) if rerank else None,
            }
            pipeline = (
                "denso+BM25+meta+RRF+rerank" if rerank else "denso+BM25+meta+RRF"
            )
            rerank_model = os.environ.get(
                "RAG_RERANK_MODEL", "BAAI/bge-reranker-v2-m3"
            ).strip()
            body = {
                "ok": True,
                "service": "fabrica-rag",
                "bind": RAG_BIND,
                "ready": state["ready"],
                "chunks": chunks,
                "rerank": bool(rerank),
                "model": MODEL_NAME,
                "rerank_model": rerank_model if rerank else None,
                "pipeline": pipeline,
                "pools": pools,
                "auth_required": bool(RAG_API_KEY),
                "ui": bool(static_root),
            }
            if state["error"]:
                body["error"] = state["error"]
            return body

        def do_GET(self):
            parsed = urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"

            if path == "/health":
                self._send_json(200, self._health_body())
                return

            if path in ("/", "/ui") and static_root:
                self._send_file(static_root / "index.html", "text/html; charset=utf-8")
                return

            if path == "/" and not static_root:
                self._send_json(200, self._health_body())
                return

            if path != "/buscar":
                self.send_response(404)
                self.end_headers()
                return

            if not state["ready"]:
                self.send_response(503)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    json.dumps(
                        {"error": "warming_up", "detail": state["error"]},
                        ensure_ascii=False,
                    ).encode("utf-8")
                )
                return

            if not self._check_auth():
                self._unauthorized()
                return

            params = parse_qs(parsed.query)
            query = params.get("q", [""])[0]
            n = int(params.get("n", [str(MAX_RESULTS)])[0])
            projeto = (params.get("projeto", [""])[0] or "").strip() or None
            if not query:
                self.send_response(400)
                self.end_headers()
                return
            t0 = datetime.now()
            resultados = buscar(
                state["collection"], state["model"], query, n, projeto=projeto
            )
            elapsed_ms = (datetime.now() - t0).total_seconds() * 1000
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("X-RAG-MS", f"{elapsed_ms:.1f}")
            self.end_headers()
            self.wfile.write(json.dumps(resultados, ensure_ascii=False).encode("utf-8"))

        def log_message(self, format, *args):
            print(f"  🌐  {datetime.now().strftime('%H:%M:%S')} {format % args}")

    def _warmup():
        try:
            from rag_retrieval import warmup_indices

            _sync_chroma_from_s3()
            if not CHROMA_PATH.exists() or not any(CHROMA_PATH.iterdir()):
                state["error"] = "chroma_vazio"
                print(f"❌  Chroma vazio em {CHROMA_PATH}")
                return

            model, collection = _carregar_chroma(device=device)
            n_chunks = collection.count()
            print(f"✅  Modelo carregado | {n_chunks} chunks no banco\n")
            sys.stdout.flush()
            if n_chunks == 0:
                state["error"] = "chroma_vazio"
                print("❌  Chroma vazio após sync")
                return
            print("⏳  Pré-carregando corpus + BM25...")
            sys.stdout.flush()
            warmup_indices(collection, model)
            state["collection"] = collection
            state["model"] = model
            state["chunks"] = n_chunks
            try:
                from rag_retrieval import (
                    POOL_BM25,
                    POOL_DENSE,
                    POOL_META,
                    RERANK_ENABLED,
                    RERANK_POOL,
                )

                state["pools"] = {
                    "dense": POOL_DENSE,
                    "bm25": POOL_BM25,
                    "meta": POOL_META,
                    "rerank": RERANK_POOL if RERANK_ENABLED else None,
                }
            except Exception:
                pass
            state["ready"] = True
            from rag_retrieval import RERANK_ENABLED

            modo = "denso+BM25+meta+RRF+rerank" if RERANK_ENABLED else "denso+BM25+meta+RRF"
            print(f"✅  Índices prontos — /buscar liberado ({modo})\n")
            sys.stdout.flush()
        except BaseException as e:
            # pyo3 PanicException do Chroma nao herda de Exception
            state["error"] = f"{type(e).__name__}: {e}"
            print(f"❌  Warmup falhou: {state['error']}")
            sys.stdout.flush()

    bind = RAG_BIND or "127.0.0.1"
    servidor = HTTPServer((bind, porta), RAGHandler)
    print(f"🚀  Servidor RAG (health) em http://{bind}:{porta}")
    print(f"    Health: http://{bind}:{porta}/health  (ready sobe após warmup)")
    if static_root:
        print(f"    UI:     http://{bind}:{porta}/  ({static_root})")
    print(f"    Teste:  http://{bind}:{porta}/buscar?q=como+fazer+auth")
    print(f"    Ctrl+C para parar\n")
    sys.stdout.flush()

    threading.Thread(target=_warmup, name="rag-warmup", daemon=True).start()
    registrar_servidor()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n⛔  Servidor encerrado")
    finally:
        limpar_pid_servidor()


def _resolver_device(s: str) -> str:
    s = (s or "auto").lower().strip()
    if s in ("cpu",):
        return "cpu"
    if s in ("cuda", "gpu"):
        return "cuda"
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def _abrir_collection_chroma():
    """Abre o banco antes do modelo pesado — falha mais cedo se .chroma_db estiver corrompido."""
    import chromadb

    if not CHROMA_PATH.exists():
        print(f"❌  Pasta não existe: {CHROMA_PATH}")
        print("    Rode: python C:/Users/gusta/obsidian/indexar_rapido.py\n")
        sys.exit(1)

    print(f"⏳  Abrindo Chroma em `{CHROMA_PATH}`...")
    sys.stdout.flush()
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )
    return collection


def _carregar_chroma(device="auto"):
    from sentence_transformers import SentenceTransformer

    collection = _abrir_collection_chroma()
    device = _resolver_device(device)
    print(f"⏳  Carregando modelo `{MODEL_NAME}` em `{device}`...")
    sys.stdout.flush()
    model = SentenceTransformer(MODEL_NAME, device=device)
    return model, collection


def main():
    parser = argparse.ArgumentParser(
        description="Servidor HTTP RAG (Chroma). Indexação: indexar_rapido.py"
    )
    parser.add_argument("--server", action="store_true", help="Sobe HTTP na porta 7332")
    parser.add_argument(
        "--porta",
        type=int,
        default=int(os.environ.get("RAG_PORT", os.environ.get("PORT", "7332"))),
    )
    parser.add_argument("--buscar", type=str, help="Testa busca sem subir servidor")
    parser.add_argument("--n", type=int, default=MAX_RESULTS)
    parser.add_argument("--device", type=str, default="auto", help="auto | cpu | cuda")
    parser.add_argument(
        "--doctor",
        action="store_true",
        help="Testa se .chroma_db abre (sem subir servidor)",
    )
    args = parser.parse_args()

    if not args.server and not args.buscar:
        print(
            "\nUso:\n"
            "  python indexar_rapido.py                    # indexar vault\n"
            "  python indexar_obsidian_chroma.py --server   # subir servidor RAG\n"
            "  python indexar_obsidian_chroma.py --buscar \"query\"\n"
        )
        return

    print("\n╔══════════════════════════════════════╗")
    print("║  RAG Local — Híbrido + meta/rerank   ║")
    print("╚══════════════════════════════════════╝\n")

    if args.doctor:
        col = _abrir_collection_chroma()
        print(f"✅  Chroma OK | {col.count()} chunks\n")
        return

    if args.server:
        # Health responde na hora; modelo/Chroma aquecem em background (App Runner).
        # Rerank ON por padrão (RAG_RERANK=0 para desligar).
        if "RAG_RERANK" not in os.environ:
            os.environ["RAG_RERANK"] = "1"
        iniciar_servidor(porta=args.porta, device=args.device)
        return

    model, collection = _carregar_chroma(device=args.device)
    n_chunks = collection.count()
    print(f"✅  Modelo carregado | {n_chunks} chunks no banco\n")

    if n_chunks == 0:
        print("❌  Chroma vazio. Rode primeiro:\n")
        print("    python C:/Users/gusta/obsidian/indexar_rapido.py\n")
        sys.exit(1)

    if args.buscar:
        if "RAG_RERANK" not in os.environ:
            os.environ["RAG_RERANK"] = "1"
        print(f"🔍  Buscando: '{args.buscar}'\n")
        for i, r in enumerate(buscar(collection, model, args.buscar, args.n), 1):
            cit = r.get("citacao", r["arquivo"])
            proj = r.get("projeto", "?")
            print(f"  [{i}] {cit}  projeto={proj}  sim={r['similaridade']}")
            print(f"      {r.get('trecho') or r['conteudo'][:200]}...\n")
        return


if __name__ == "__main__":
    main()

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


def buscar(collection, model, query, n=MAX_RESULTS):
    from rag_retrieval import buscar_hibrido

    return buscar_hibrido(collection, model, query, n)


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

    state = {"ready": False, "error": None, "collection": None, "model": None}

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

        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path in ("/health", "/"):
                body = {
                    "ok": True,
                    "service": "fabrica-rag",
                    "bind": RAG_BIND,
                    "ready": state["ready"],
                }
                if state["error"]:
                    body["error"] = state["error"]
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(body, ensure_ascii=False).encode("utf-8"))
                return

            if parsed.path != "/buscar":
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
            if not query:
                self.send_response(400)
                self.end_headers()
                return
            t0 = datetime.now()
            resultados = buscar(state["collection"], state["model"], query, n)
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
            state["ready"] = True
            print("✅  Índices BM25 prontos — /buscar liberado\n")
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
    print(f"    Teste:  http://{bind}:{porta}/buscar?q=como+fazer+auth")
    print(f"    Ctrl+C para parar\n")
    sys.stdout.flush()

    threading.Thread(target=_warmup, name="rag-warmup", daemon=True).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n⛔  Servidor encerrado")


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
    print("║  RAG Local — Híbrido (Chroma+BM25)   ║")
    print("╚══════════════════════════════════════╝\n")

    if args.doctor:
        col = _abrir_collection_chroma()
        print(f"✅  Chroma OK | {col.count()} chunks\n")
        return

    if args.server:
        # Health responde na hora; modelo/Chroma aquecem em background (App Runner).
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
        print(f"🔍  Buscando: '{args.buscar}'\n")
        for i, r in enumerate(buscar(collection, model, args.buscar, args.n), 1):
            print(f"  [{i}] {r['arquivo']} (similaridade: {r['similaridade']})")
            print(f"      {r['conteudo'][:200]}...\n")
        return


if __name__ == "__main__":
    main()

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

CHROMA_PATH = Path("C:/Users/gusta/obsidian/.chroma_db")
COLLECTION_NAME = "fabrica-knowledge"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
MAX_RESULTS = 5


def buscar(collection, model, query, n=MAX_RESULTS):
    from rag_retrieval import buscar_hibrido

    return buscar_hibrido(collection, model, query, n)


def iniciar_servidor(collection, model, porta=7332):
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    class RAGHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path != "/buscar":
                self.send_response(404)
                self.end_headers()
                return
            params = parse_qs(parsed.query)
            query = params.get("q", [""])[0]
            n = int(params.get("n", [str(MAX_RESULTS)])[0])
            if not query:
                self.send_response(400)
                self.end_headers()
                return
            resultados = buscar(collection, model, query, n)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resultados, ensure_ascii=False).encode("utf-8"))

        def log_message(self, format, *args):
            print(f"  🌐  {datetime.now().strftime('%H:%M:%S')} {format % args}")

    servidor = HTTPServer(("localhost", porta), RAGHandler)
    print(f"🚀  Servidor RAG rodando em http://localhost:{porta}")
    print(f"    Teste: http://localhost:{porta}/buscar?q=como+fazer+auth")
    print(f"    Ctrl+C para parar\n")
    sys.stdout.flush()
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
    parser.add_argument("--porta", type=int, default=7332)
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

    if args.server:
        iniciar_servidor(collection, model, args.porta)


if __name__ == "__main__":
    main()

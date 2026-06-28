import sys
import argparse
import chromadb
import hashlib
import shutil
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VAULT_PATH    = Path("C:/Users/gusta/obsidian/fabrica")
PROJETOS_PATH = Path("C:/Users/gusta/obsidian/projetos")
CHROMA_PATH   = Path("C:/Users/gusta/obsidian/.chroma_db")
COLLECTION    = "fabrica-knowledge"
MODEL_NAME    = "paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE    = 500
OVERLAP       = 100

def chunks(texto, arquivo):
    partes, inicio, idx = [], 0, 0
    while inicio < len(texto):
        fim = min(inicio + CHUNK_SIZE, len(texto))
        chunk = texto[inicio:fim].strip()
        if chunk:
            cid = hashlib.md5(f"{arquivo}_{idx}".encode()).hexdigest()
            partes.append((cid, chunk, idx))
            idx += 1
        if fim >= len(texto): break
        inicio = fim - OVERLAP
    return partes

def abrir_chroma():
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    print(f"Abrindo Chroma em {CHROMA_PATH}...")
    sys.stdout.flush()
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    col = client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    return client, col


def recriar_banco():
    if CHROMA_PATH.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = CHROMA_PATH.with_name(f".chroma_db.bak-{stamp}")
        print(f"Banco antigo movido para {dest}")
        shutil.move(str(CHROMA_PATH), str(dest))


def indexar_arquivo(col, model, md: Path) -> int:
    texto = md.read_text(encoding="utf-8")
    chks = chunks(texto, md.name)
    try:
        col.delete(where={"arquivo": md.name})
    except Exception:
        pass
    for cid, txt, idx in chks:
        emb = model.encode([txt], normalize_embeddings=True)[0].tolist()
        col.upsert(
            documents=[txt],
            embeddings=[emb],
            ids=[cid],
            metadatas=[{"arquivo": md.name, "chunk": idx}],
        )
    return len(chks)


def resolver_arquivos(nomes: list[str]) -> list[Path]:
    resolvidos: list[Path] = []
    for raw in nomes:
        p = Path(raw)
        if p.is_file():
            resolvidos.append(p.resolve())
            continue
        nome = p.name if p.suffix else f"{raw}.md"
        achou = False
        for base in (VAULT_PATH, PROJETOS_PATH):
            direto = base / nome
            if direto.is_file():
                resolvidos.append(direto.resolve())
                achou = True
                break
        if not achou:
            print(f"⚠️  Não encontrado: {raw}", file=sys.stderr)
    vistos: set[Path] = set()
    return [md for md in resolvidos if md not in vistos and not vistos.add(md)]


def main():
    parser = argparse.ArgumentParser(description="Indexa vault Obsidian no ChromaDB")
    parser.add_argument(
        "--recriar-banco",
        action="store_true",
        help="Move .chroma_db antigo e cria banco novo (use se o script crashar ao abrir)",
    )
    parser.add_argument(
        "--somente",
        nargs="+",
        metavar="ARQUIVO",
        help="Indexa só estes .md (rápido). Ex: --somente cortejo-modulos-jun2026-padrao.md erros-e-solucoes.md",
    )
    args = parser.parse_args()

    if args.recriar_banco:
        recriar_banco()

    _, col = abrir_chroma()

    from sentence_transformers import SentenceTransformer

    print("Carregando modelo...")
    sys.stdout.flush()
    model = SentenceTransformer(MODEL_NAME)

    if args.somente:
        arquivos = resolver_arquivos(args.somente)
        if not arquivos:
            print("Nenhum arquivo para indexar.")
            sys.exit(1)
        print(f"Indexação parcial: {len(arquivos)} arquivo(s)\n")
        for i, md in enumerate(arquivos, 1):
            n = indexar_arquivo(col, model, md)
            print(f"[{i}/{len(arquivos)}] {md.name} — {n} chunks ✅")
    else:
        col.delete(where={"arquivo": {"$ne": ""}}) if col.count() > 0 else None
        arquivos = list(VAULT_PATH.rglob("*.md")) + list(PROJETOS_PATH.rglob("*.md"))
        print(f"{len(arquivos)} arquivos encontrados (indexação completa — demora)\n")
        for i, md in enumerate(arquivos, 1):
            n = indexar_arquivo(col, model, md)
            print(f"[{i}/{len(arquivos)}] {md.name} — {n} chunks ✅")

    print(f"\nPronto! {col.count()} chunks no banco.")
    print("Servidor RAG (só consulta): python indexar_obsidian_chroma.py --server")


if __name__ == "__main__":
    main()
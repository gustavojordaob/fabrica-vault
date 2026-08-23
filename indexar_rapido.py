import os
import sys
import argparse
import chromadb
import hashlib
import shutil
import re
from datetime import datetime
from pathlib import Path

from chroma_lock import (
    CHROMA_PATH as LOCK_CHROMA_PATH,
    acquire_index_lock,
    fechar_cliente_chroma,
    parar_servidor_local,
    porta_em_uso,
    release_index_lock,
)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VAULT_PATH = Path(
    os.environ.get("RAG_VAULT_PATH", "C:/Users/gusta/obsidian/fabrica")
)
PROJETOS_PATH = Path(
    os.environ.get("RAG_PROJETOS_PATH", "C:/Users/gusta/obsidian/projetos")
)
CHROMA_PATH = Path(os.environ.get("RAG_CHROMA_PATH", str(LOCK_CHROMA_PATH)))
COLLECTION = "fabrica-knowledge"
MODEL_NAME = os.environ.get(
    "RAG_MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2"
)
CHUNK_SIZE    = 500
OVERLAP       = 100

_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL
)


def parse_frontmatter(texto: str) -> tuple[dict, str]:
    """Extrai YAML frontmatter simples (tags/projeto) sem depender de PyYAML."""
    m = _FRONTMATTER_RE.match(texto)
    if not m:
        return {}, texto
    meta: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.strip().startswith("-"):
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower()
        val = val.strip().strip("\"'")
        if not key:
            continue
        if key == "tags":
            # tags: [a, b] ou tags:\n  - a
            continue
        meta[key] = val
    # tags em lista YAML
    tags: list[str] = []
    in_tags = False
    for line in m.group(1).splitlines():
        s = line.strip()
        if s.startswith("tags:"):
            rest = s[5:].strip()
            if rest.startswith("[") and rest.endswith("]"):
                tags = [t.strip().strip("\"'") for t in rest[1:-1].split(",") if t.strip()]
            else:
                in_tags = True
            continue
        if in_tags:
            if s.startswith("-"):
                tags.append(s[1:].strip().strip("\"'"))
            elif s and not s.startswith("#"):
                in_tags = False
    if tags:
        meta["tags"] = ",".join(tags)
    body = texto[m.end():]
    return meta, body


def infer_projeto(md: Path, fm: dict | None = None) -> str:
    if fm and fm.get("projeto"):
        return str(fm["projeto"]).strip().lower()
    nome = md.name.lower()
    try:
        rel = md.relative_to(VAULT_PATH)
        if len(rel.parts) >= 2:
            # fabrica/sinaflor/foo.md → sinaflor
            return rel.parts[0].lower()
    except ValueError:
        pass
    for p in (
        "sinaflor", "lashmatch", "cortejo", "erp", "setmatch", "zenpro",
        "whatsapp", "firebase", "mercadopago", "trajeto", "health-quadra-tech",
    ):
        if nome.startswith(p) or f"-{p}" in nome or f"{p}-" in nome:
            return p
    if "health-quadra" in nome or "trajeto" in nome:
        return "trajeto"
    if md.parent.name == "projetos":
        stem = md.stem.lower().replace("-prd", "").replace("_prd", "")
        return stem.split("-")[0] if stem else "projetos"
    return "fabrica"


def infer_tipo_doc(md: Path) -> str:
    nome = md.name.lower()
    rel = md.relative_to(VAULT_PATH) if md.is_relative_to(VAULT_PATH) else md
    if "eval" in rel.parts:
        return "eval"
    if nome.endswith("-prd.md") or nome.endswith("prd.md"):
        return "spec"
    if md.parent.name == "projetos":
        return "spec"
    if nome == "erros-e-solucoes.md":
        return "solucao"
    return "padrao"

def should_index(md: Path) -> bool:
    try:
        rel = md.relative_to(VAULT_PATH)
    except ValueError:
        return True
    if "eval" in rel.parts:
        return False
    if md.name == "outros.md":
        return False
    return True

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

def abrir_chroma(path: Path | None = None):
    destino = path or CHROMA_PATH
    destino.mkdir(parents=True, exist_ok=True)
    print(f"Abrindo Chroma em {destino}...")
    sys.stdout.flush()
    client = chromadb.PersistentClient(path=str(destino))
    col = client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    return client, col


def publicar_banco_novo(build_path: Path):
    if CHROMA_PATH.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = CHROMA_PATH.with_name(f".chroma_db.bak-{stamp}")
        print(f"Banco antigo movido para {dest}")
        shutil.move(str(CHROMA_PATH), str(dest))
    shutil.move(str(build_path), str(CHROMA_PATH))
    print(f"Banco novo publicado em {CHROMA_PATH}")


def indexar_arquivo(col, model, md: Path) -> int:
    texto = md.read_text(encoding="utf-8")
    fm, _body = parse_frontmatter(texto)
    projeto = infer_projeto(md, fm)
    tags = str(fm.get("tags", ""))
    try:
        rel_path = str(md.relative_to(VAULT_PATH.parent)).replace("\\", "/")
    except ValueError:
        rel_path = md.name

    chks = chunks(texto, rel_path)
    try:
        col.delete(where={"path": rel_path})
    except Exception:
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
            metadatas=[{
                "arquivo": md.name,
                "chunk": idx,
                "tipo_doc": infer_tipo_doc(md),
                "projeto": projeto,
                "tags": tags,
                "path": rel_path,
            }],
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
                for cand in base.rglob(nome):
                    if cand.is_file():
                        resolvidos.append(cand.resolve())
                        achou = True
                        break
            if achou:
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
        help="Para o servidor local, indexa em .chroma_db.build e só então substitui o banco (evita HNSW 0xC0000005)",
    )
    parser.add_argument(
        "--somente",
        nargs="+",
        metavar="ARQUIVO",
        help="Indexa só estes .md (rápido). Ex: --somente cortejo-modulos-jun2026-padrao.md erros-e-solucoes.md",
    )
    args = parser.parse_args()
    acquire_index_lock()

    if not args.recriar_banco and porta_em_uso():
        print(
            "Servidor RAG local (porta 7332) está aberto no mesmo .chroma_db.\n"
            "Indexação incremental pulada para não corromper o HNSW.\n"
            "Para reindexar de verdade: python indexar_rapido.py --recriar-banco\n"
            "Depois: .\\aws-rag\\scripts\\sync-push.ps1 -SkipIndex -Region us-east-1"
        )
        release_index_lock()
        return

    build_path = None
    chroma_path = CHROMA_PATH
    if args.recriar_banco:
        parar_servidor_local()
        build_path = CHROMA_PATH.with_name(".chroma_db.build")
        if build_path.exists():
            shutil.rmtree(build_path)
        chroma_path = build_path
        print(f"Indexando em staging {build_path} (só troca o banco se terminar ok).")

    client, col = abrir_chroma(chroma_path)

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
        arquivos = [
            md for md in VAULT_PATH.rglob("*.md") if should_index(md)
        ] + list(PROJETOS_PATH.rglob("*.md"))
        print(f"{len(arquivos)} arquivos encontrados (indexação completa — demora)\n")
        for i, md in enumerate(arquivos, 1):
            n = indexar_arquivo(col, model, md)
            print(f"[{i}/{len(arquivos)}] {md.name} — {n} chunks ✅")

    total = col.count()
    print(f"\nPronto! {total} chunks no banco.")
    fechar_cliente_chroma(client, col)
    if build_path:
        publicar_banco_novo(build_path)
        print(f"Publicado. {total} chunks em {CHROMA_PATH}")
    print("Servidor RAG (só consulta): python indexar_obsidian_chroma.py --server")
    print("AWS: .\\aws-rag\\scripts\\sync-push.ps1 -SkipIndex -Region us-east-1")
    release_index_lock()


if __name__ == "__main__":
    main()
"""
indexar_obsidian.py
-------------------
Indexa as notas do Obsidian no ChromaDB para uso como RAG.
Chame este script sempre que atualizar notas no vault.

Instalar dependências:
    pip install chromadb sentence-transformers

Uso:
    python indexar_obsidian.py
"""

import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

VAULT_PATH = Path(__file__).parent  # mesma pasta do vault
CHROMA_PATH = Path(__file__).parent / ".chroma_db"
COLLECTION_NAME = "fabrica-knowledge"
CHUNK_SIZE = 600    # caracteres por chunk
CHUNK_OVERLAP = 100 # sobreposição entre chunks

def chunkar(texto: str, tamanho: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = min(inicio + tamanho, len(texto))
        chunks.append(texto[inicio:fim])
        inicio += tamanho - overlap
    return chunks

def main():
    print("🔍 Iniciando indexação do vault Obsidian...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")  # suporta PT-BR
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    arquivos_md = list(VAULT_PATH.glob("*.md"))
    arquivos_md = [f for f in arquivos_md if f.name != "INDEX.md"]

    total_chunks = 0
    for md_file in arquivos_md:
        texto = md_file.read_text(encoding="utf-8")
        chunks = chunkar(texto)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{md_file.stem}_{i}"
            embedding = model.encode(chunk).tolist()
            collection.upsert(
                documents=[chunk],
                embeddings=[embedding],
                ids=[chunk_id],
                metadatas=[{"arquivo": md_file.name, "chunk": i}]
            )

        total_chunks += len(chunks)
        print(f"  ✅  {md_file.name} → {len(chunks)} chunks")

    print(f"\n🎉 Indexação concluída! {len(arquivos_md)} arquivos, {total_chunks} chunks.")
    print(f"   Base salva em: {CHROMA_PATH}")

if __name__ == "__main__":
    main()

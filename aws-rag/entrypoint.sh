#!/bin/sh
set -eu

PORT="${PORT:-${RAG_PORT:-8080}}"
export RAG_PORT="$PORT"
export RAG_BIND="${RAG_BIND:-0.0.0.0}"
export RAG_CHROMA_PATH="${RAG_CHROMA_PATH:-/data/chroma}"
export RAG_VAULT_PATH="${RAG_VAULT_PATH:-/data/vault/fabrica}"
export RAG_PROJETOS_PATH="${RAG_PROJETOS_PATH:-/data/vault/projetos}"

mkdir -p "$RAG_CHROMA_PATH" "$RAG_VAULT_PATH" "$RAG_PROJETOS_PATH"

# S3 sync + modelo ficam no warmup do Python (depois do /health escutar).
echo "🚀  Subindo servidor RAG em 0.0.0.0:${PORT}"
exec python /app/indexar_obsidian_chroma.py --server --porta "$PORT" --device cpu

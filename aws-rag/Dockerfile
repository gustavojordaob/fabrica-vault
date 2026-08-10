# Fábrica RAG — runtime App Runner / Docker
# Build (na pasta obsidian):
#   docker build -f aws-rag/Dockerfile -t fabrica-rag:latest .

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    RAG_BIND=0.0.0.0 \
    RAG_PORT=8080 \
    PORT=8080 \
    RAG_CHROMA_PATH=/data/chroma \
    RAG_VAULT_PATH=/data/vault/fabrica \
    RAG_PROJETOS_PATH=/data/vault/projetos \
    RAG_MODEL_NAME=paraphrase-multilingual-MiniLM-L12-v2 \
    RAG_RERANK=1 \
    RAG_RERANK_MODEL=BAAI/bge-reranker-base \
    RAG_RERANK_POOL=12 \
    HF_HOME=/opt/hf-cache \
    TRANSFORMERS_CACHE=/opt/hf-cache \
    SENTENCE_TRANSFORMERS_HOME=/opt/hf-cache

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY aws-rag/requirements.txt /app/requirements.txt
# Torch CPU-only (App Runner nao tem GPU; imagem ~1-2GB em vez de ~10GB)
# Bake MiniLM + reranker-base (lazy load em runtime; evita download HF no boot)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && python -c "from sentence_transformers import SentenceTransformer, CrossEncoder; SentenceTransformer('${RAG_MODEL_NAME}'); CrossEncoder('${RAG_RERANK_MODEL}', max_length=512)"

COPY rag_retrieval.py /app/rag_retrieval.py
COPY indexar_obsidian_chroma.py /app/indexar_obsidian_chroma.py
COPY indexar_rapido.py /app/indexar_rapido.py
COPY aws-rag/static /app/static
COPY aws-rag/entrypoint.sh /app/entrypoint.sh

ENV RAG_STATIC_PATH=/app/static

# Windows checkout costuma salvar .sh com CRLF — quebra o shebang no Linux
RUN sed -i 's/\r$//' /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh \
    && mkdir -p /data/chroma /data/vault/fabrica /data/vault/projetos

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=3 \
  CMD curl -fsS "http://127.0.0.1:${PORT}/health" || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]

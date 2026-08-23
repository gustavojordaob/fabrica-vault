---
tags:
  - rag
  - retrieval
  - fabrica
  - rerank
  - chroma
projeto: fabrica
fonte: melhoria hot-path 2026-08-07
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. `rag_buscar("fabrica rag retrieval rerank")` + `buscar_historico("rag retrieval")`
> 2. Código: `C:/Users/gusta/obsidian/rag_retrieval.py` + `indexar_obsidian_chroma.py` + `indexar_rapido.py`

# RAG fábrica — retrieval (híbrido + meta + rerank)

## Pipeline (hot path `:7332`)

1. **Denso** (Chroma / MiniLM) — pool 48  
2. **BM25** — pool 48  
3. **Meta** (projeto/tags/nome) — pool 32 — 3ª recall  
4. **RRF** (pesos denso 1.5 / BM25 1.0 / meta 1.25)  
5. Affinity por query (sinaflor, schemas, etc.)  
6. **Rerank** `bge-reranker-v2-m3` — **ligado por padrão**

Desligar rerank: `RAG_RERANK=0` no ambiente do servidor.

## Resposta `/buscar` (citações)

Cada hit inclui:

| Campo | Uso |
|-------|-----|
| `arquivo` / `path` / `chunk` | Localização |
| `projeto` / `tags` / `tipo_doc` | Filtro e contexto |
| `trecho` | Citação curta com termos da query |
| `citacao` | `arquivo#chunk` |
| `similaridade` / `rank` | Score |

Filtro opcional: `GET /buscar?q=...&projeto=sinaflor&n=5`

## Indexação (`indexar_rapido.py`)

Metadados por chunk: `arquivo`, `chunk`, `tipo_doc`, **`projeto`**, **`tags`**, **`path`**.

- `projeto` vem do frontmatter, pasta (`fabrica/sinaflor/…`) ou prefixo do nome  
- Após mudar metadata: `python indexar_rapido.py` (completo) ou `--somente arquivo.md`

## Subir servidor

```powershell
python C:/Users/gusta/obsidian/indexar_obsidian_chroma.py --server
# opcional: $env:RAG_RERANK="0"
```

Warmup carrega corpus + BM25 + reranker (se ligado). Primeira subida pode demorar mais.

## Checklist

- [x] Rerank ON (default) — latência ↑ (~14–17s/query CPU), precisão ↑  
- [x] Query com `sinaflor` / `lashmatch` ativa 3ª recall de projeto  
- [x] `/buscar` devolve `citacao` + `trecho` + `projeto` + `path`  
- [x] Chroma recriado (2075 chunks) após HNSW corrompido — 2026-08-07  
- [x] Chroma recriado após HNSW corrompido no Windows — `indexar_rapido.py --recriar-banco` (staging `.chroma_db.build` + lock) + `reparar-chroma.ps1` → S3 **us-east-1**. Incremental não escreve com o servidor 7332 aberto.  
- [x] `INDEX.md` (catálogo/rank das notas) + Trajeto (`health-quadra-tech-*`) + `setmatch-rankings-*` no índice  
- [ ] Agente no Cursor: preferir citar `citacao` + `trecho` nas respostas  

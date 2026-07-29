---
tags:
  - fabrica
  - rag
  - aws
  - docker
  - terraform
  - app-runner
atualizado_em: 2026-07-29
autor: Gustavo
status: ativo
---

# Fábrica RAG na AWS — App Runner

> **Agente Cursor — use MCP antes de codar**
>
> ```
> rag_buscar("aws rag app runner docker terraform")
> buscar_historico("aws rag chroma deploy")
> ```
>
> Código: `C:/Users/gusta/obsidian/aws-rag/`  
> README: `aws-rag/README.md`

## Decisão

Hospedar o servidor HTTP da fábrica (`indexar_obsidian_chroma.py --server`) em **AWS App Runner**, com:

- **ECR** — imagem Docker (MiniLM baked-in, **torch CPU**)
- **S3** — dump do `.chroma_db` gerado no PC via `indexar_rapido.py`
- **Warmup assíncrono** — `/health` responde na hora; S3+modelo+BM25 em background
- **API key** — header `X-RAG-Key` em `/buscar`; `/health` aberto

**Não** usar Bedrock Knowledge Base, SageMaker nem Lambda+EFS neste momento.

## Região

**`us-east-1` obrigatório** — App Runner **não existe** em `sa-east-1`.

Bucket: `fabrica-rag-<account>-us-east-1`

## Produção (jul/2026)

| Item | Valor |
|------|--------|
| URL | `https://gmnxgbtjy9.us-east-1.awsapprunner.com` |
| Health | `/health` → `{ ok, ready }` |
| Buscar | `/buscar?q=` + header `X-RAG-Key` |
| Chroma no Docker | **1.5.x** (igual ao PC — major diferente quebra o dump) |

API key: `terraform output -raw rag_api_key` (não commitar).

MCP Cursor aponta para o remoto via:

- `~/.cursor/rag-remote.json` → `{ baseUrl, apiKey }`
- `~/.cursor/mcp.json` → env `RAG_BASE_URL` + `RAG_API_KEY` no servidor `fabrica-apps`
- Hooks (`rag-lib.js`) leem o mesmo `rag-remote.json`

Reinicie o MCP **fabrica-apps** no Cursor após mudar.

## Atualizar índice

```powershell
cd C:\Users\gusta\obsidian
.\aws-rag\scripts\sync-push.ps1
# App Runner reinicia sozinho (Lambda no upload de chroma/chroma.sqlite3)
```

## Observabilidade (CloudWatch + sync auto)

| Recurso | Função |
|---------|--------|
| SNS `fabrica-rag-alerts` | E-mail de alarmes — **confirmar** o link no inbox |
| Alarm `fabrica-rag-5xx` | Muitos 5xx |
| Alarm `fabrica-rag-latency-p50` | Latência média > 10s |
| Lambda `fabrica-rag-restart-on-chroma` | S3 `chroma/**/chroma.sqlite3` → `StartDeployment` |

## Checklist deploy

1. `bootstrap.ps1` → ECR + S3 + IAM
2. `sync-push.ps1` → indexa + sobe chroma (+ vault)
3. `build-push.ps1` → Docker CPU → ECR
4. `terraform apply` → App Runner + alarmes + Lambda
5. `test-remote.ps1` → health + buscar

## Lições

- Imagem com torch CUDA ~10GB — usar `--index-url .../cpu`
- Health check falha se a porta só abre após o modelo — health imediato + warmup thread
- Chroma 1.0.x no Docker + dump 1.5.x do Windows → panic SQLite; alinhar versão

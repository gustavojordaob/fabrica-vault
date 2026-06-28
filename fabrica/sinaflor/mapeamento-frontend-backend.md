---
tags:
  - sinaflor
  - mapeamento
  - api
fonte: sinaflor2/CLAUDE.md
atualizado_em: 2026-06-12
projeto: SINAFLOR2
links:
  - "[[../projetos/sinaflor-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor mapeamento frontend ↔ backend")` + `buscar_historico("sinaflor")`
> 2. Leia `obsidian/projetos/sinaflor-prd.md` para estrutura do monorepo
> 3. Projeto **legado** — não modernizar sem pedido explícito

# Mapeamento frontend ↔ backend

| Frontend (`src/app/service/`) | Backend (`web/rest/`) | URL |
|---|---|---|
| `AutorizacaoService` | `AutorizacaoResource` | `/sinaflor2autorizacao/api/autorizacao` |
| `CabecalhoService` | `CabecalhoResource` | `/sinaflor2autorizacao/api/cabecalho` |
| `ArvoreService` | `ArvoreResource` | `/sinaflor2autorizacao/api/arvore` |
| `SolicitacaoService` | `SolicitacaoResource` | `/sinaflor2autorizacao/api/solicitacao` |
| `LicenciamentoExploracao.service` / `licenciamento.ts` | `LicenciamentoResource` | `/sinaflor2autorizacao/api/licenciamento` |
| `licenciamento.ts` (PDF) | `ComprovanteEnvioLicenciamentoResource` | `/sinaflor2autorizacao/api/licenciamento/{id}/comprovante-envio-projeto` |
| `licenciamento.ts` (PDF) | `ComprovanteEnvioLicenciamentoResource` | `/sinaflor2autorizacao/api/licenciamento/{id}/formulario-envio-licenciamento` |

As **roles são idênticas** no frontend (`PermissaoUtil`) e no backend (`Roles`) — mesma string de valor.

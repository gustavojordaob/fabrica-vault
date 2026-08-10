---
tags:
  - fabrica
  - erp
  - cursor
  - agentes
  - rules
  - skills
  - gateway
atualizado_em: 2026-08-05
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

> **GATEWAY OBRIGATÓRIO — ERP**
>
> Qualquer consulta RAG / implementação sobre **ERP, Spring Boot, Flyway, multi-tenant, Hibernate SCHEMA, módulo ERP** deve **passar por esta nota primeiro**.
>
> Hooks (`detectMandatoryRagDocs` → id `erp-agente-modo`) forçam query RAG para esta nota e bloqueiam Write até MCP `rag_buscar` + `buscar_historico`.
>
> 1. `rag_buscar("erp agente modo cursor")` + `buscar_historico("erp")`
> 2. **Escopo MVP:** `rag_buscar("erp baseline prd mvp escopo")` → [[../projetos/erp-baseline-prd]] (v1 = auth + produto + estoque; PT-BR)
> 3. Rule `~/.cursor/rules/erp-fabrica.mdc` + skills `criar-modulo-erp` / `revisar-pr-erp`
> 4. Depois o tema: `erp-stack`, `erp-ui-telas`, `erp-modulo-produto`, `erp-modulo-estoque`, etc.
> 5. MCP **postgres** para schema real — nunca inventar tabela
>
> **Idioma:** telas e mensagens em português (Brasil). SAP só como modelo de processo.

# ERP — modo agente Cursor (nível 1)

**Palavras-chave de recuperação:** erp agente modo cursor, erp-fabrica.mdc, criar-modulo-erp, revisar-pr-erp, gateway ERP, Spring Boot Postgres multi-tenant, erp baseline prd mvp escopo, auth tenant produto estoque português.

Como especializar o Cursor para ERP **sem** orquestra de 6 agentes. Reutiliza o RAG App Runner e as notas `erp-*` já indexadas.

## O que foi criado (05/08/2026)

| Peça | Caminho |
|------|---------|
| Rule global | `~/.cursor/rules/erp-fabrica.mdc` (`alwaysApply: false` + globs Java/Flyway/backend/frontend) |
| Skill módulo | `~/.cursor/skills/criar-modulo-erp/SKILL.md` |
| Skill review | `~/.cursor/skills/revisar-pr-erp/SKILL.md` |
| Hook mandatory | `~/.cursor/hooks/rag-lib.js` → id `erp-agente-modo` (query RAG forçada + workflow `erp_modo_gateway`) |

## Como o RAG “sempre passa” por esta nota

Quando o prompt fala ERP / Spring Boot / Flyway / multi-tenant / Hibernate / skills ERP:

1. `detectMandatoryRagDocs` marca `erp-agente-modo`
2. `buildRagQuery` busca com query focada nesta nota (App Runner)
3. Gate de Write exige MCP `rag_buscar` + `buscar_historico`
4. Workflow injeta instruções do gateway

Não aplica em apps salão (Expo) sem essas palavras.

## Notas RAG já existentes (não duplicar)

- [[erp-stack]] · [[erp-multitenancy-spring]] · [[erp-spring-camadas]]
- [[erp-transacao-dominio]] · [[erp-postgres-schema]] · [[erp-migrations-flyway]]
- [[erp-angular-estrutura]] · [[erp-ui-telas]] · [[erp-modulo-produto]] · [[erp-modulo-estoque]] · [[erp-testes-backend]] · [[erp-aws-rds]] · [[erp-auth-login]]
- **PRD escopo MVP:** `projetos/erp-baseline-prd.md` — v1 auth+produto+estoque; vendas/financeiro fase 2; UI PT-BR

## No repo do ERP (obrigatório para always-on)

Criar `.cursor/rules/erp-projeto.mdc`:

```markdown
---
description: Workspace ERP — sempre modo Spring/Angular/Postgres
alwaysApply: true
---

# Projeto ERP

Seguir `erp-fabrica.mdc` (global) e notas `erp-*` via RAG.
Proibido default Expo/Firebase/Firestore.
Skills: criar-modulo-erp, revisar-pr-erp.
MCP postgres antes de inventar schema.
```

## Nível 2 (futuro — não bloqueia)

Orquestrador fora do Cursor (API + workers DB/Rules/Back/Front/Review) reutilizando o mesmo RAG/MCP. Ver decisão em `decisoes.md` / conversa Cursor ago/2026.

## Checklist novo PC / nuvem

- [ ] Clonar vault Obsidian + indexar / App Runner sync
- [ ] Copiar `~/.cursor/rules/erp-fabrica.mdc` e `~/.cursor/skills/criar-modulo-erp` + `revisar-pr-erp`
- [ ] `RAG_BASE_URL` = App Runner
- [ ] No repo ERP: `erp-projeto.mdc` com `alwaysApply: true`

# Plano de consolidação do vault — análise RAG (baseline v2)

**Data:** 2026-06-29  
**Fonte:** `fabrica/eval/report-baseline-v2.md` (31 pares, hit@1 58.1%, hit@3 90.3%)  
**Consulta RAG:** `rag_buscar("duplicacao notas consolidacao eval miss")` — servidor lento/offline no momento da análise; cruzamento manual com top-5 de cada par MISS/rank 2–3 + contagem de chunks (`indexar_rapido.chunks`).

> **Escopo deste documento:** recomendações apenas. **Nenhuma nota foi editada, fundida ou excluída.** Revisão humana obrigatória antes de executar.

---

## Resumo executivo

| Problema | Impacto no eval | Prioridade |
|----------|-----------------|------------|
| `outros.md` (127 chunks) — lixão do monólito CLAUDE | gs-011 rank 1 ruído; competição genérica em dezenas de temas | **P0** |
| `decisoes.md` (87 chunks) — log cronológico indexado como `padrao` | gs-003, gs-005, gs-018, gs-019, gs-020 — decisões competem com notas canônicas | **P0** |
| Schemas Firestore fragmentados (4+ notas) | gs-001 MISS; gs-002 `padroes-fabrica` > `lashmatch-schemas` | **P1** |
| Mercado Pago / assinatura (4+ notas) | gs-010 rank 3; gs-012 rank 3; gs-020 rank 3 | **P1** |
| Deploy / hosting (4 notas) | gs-015 MISS; gs-013 rank 2 | **P1** |
| RAG / arquitetura (3 notas novas) | gs-018 MISS; gs-022 competição guia vs arquitetura | **P2** |
| ERP vs SINAFLOR Spring/Angular/testes (stacks diferentes, vocabulário igual) | gs-004 `erp-auth-login` no top-5 de query Expo auth | **P2** |
| `*-prd.md` no índice | gs-003 top-5 com `cortejo-prd`, `setmatch-prd` | **P2** (já há filtro parcial no retrieval híbrido) |

---

## 1. Grupos de notas que competem no retrieval

### G1 — Schema / modelagem de dados (Firestore)

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `cortejo-schemas.md` | ~15 | Schema **Cortejo** (salons, members, appointments) |
| `lashmatch-schemas.md` | ~12 | Schema **LashMatch** (`artifacts/.../users/...`) |
| `firestore-schemas.md` | 18 | Genérico extraído do CLAUDE (users/posts/chats — **não** salão) |
| `padroes-fabrica.md` | 35 | Mix UI + setup + trechos de path Firestore |
| `cadastro-clientes-salao-expo.md` | ~10 | Regras `isMember` + overlap schema cliente |

**Evidência eval:** gs-001 MISS (esperado `cortejo-schemas`, top-5 sem nenhum schema); gs-002 rank 2 (`padroes-fabrica` #1).

---

### G2 — Mercado Pago / assinatura Android

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `mercadopago-integration.md` | ~25 | Guia **canônico** MP (preapproval, webhook §26–27) |
| `mercadopago-assinatura-ota-padroes.md` | ~30 | Padrão OTA Cortejo (cancel, sync, paywall) |
| `lashmatch-mercadopago-assinatura.md` | ~20 | Instância LashMatch |
| `lashmatch-modulos-assinatura-jun2026.md` | ~25 | Módulo dual RC+MP LashMatch |
| `cortejo-modulos-jun2026-padrao.md` | ~35 | Módulo dual RC+MP Cortejo |

**Evidência eval:** gs-010 rank 3; gs-012 rank 3 (`mercadopago-assinatura-ota` #1); gs-011 `outros.md` #1; gs-023 `mercadopago-assinatura-ota` no top-5 de query Firestore cliente.

---

### G3 — Assinatura iOS (RevenueCat / App Store)

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `lashmatch-revenuecat-assinatura.md` | ~20 | RC + App Store LashMatch |
| `cortejo-modulos-jun2026-padrao.md` | (overlap G2) | Seção RevenueCat Cortejo |
| `mcps-cursor-padrao.md` | ~15 | Tabela qual MCP usar |

**Evidência eval:** gs-020 rank 3 (`mercadopago-integration` e `lashmatch-revenuecat` antes de `mcps-cursor-padrao`).

---

### G4 — WhatsApp

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `whatsapp-business-api.md` | ~25 | Meta API single-tenant (LashMatch) |
| `whatsapp-salao-expo-padrao.md` | ~45 | Multi-tenant + Embedded Signup (Cortejo) |

**Evidência eval:** gs-007 hit@1 OK; gs-009 hit@1 OK mas `decisoes.md` #5 no top-5.

**Relação:** complementares por **modo de deploy** (single vs multi-tenant), não duplicatas literais.

---

### G5 — Firebase deploy / hosting / functions

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `firebase-deploy-checklist-padrao.md` | ~12 | Checklist **operacional** deploy |
| `firebase-setup-patterns.md` | ~40 | Setup + hosting + functions (amplo) |
| `cloud-functions-patterns.md` | ~25 | Functions isoladas |
| `checklists-deploy.md` | ~15 | Checklists genéricos (legado CLAUDE) |
| `arquitetura-fabrica-ia.md` | 56 | Menciona deploy + RAG + hooks |

**Evidência eval:** gs-013 rank 2 (`firebase-deploy-checklist` #1 vs `cloud-functions-patterns` esperado); gs-014 hit@1 OK; gs-015 MISS (`lashmatch-web-plataforma` + `expo-router` vs `firebase-setup-patterns`); gs-025 rank 1 OK mas `checklists-deploy` no top-5.

---

### G6 — Web Expo / Hosting

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `lashmatch-web-plataforma.md` | ~15 | Web LashMatch (sem checkout in-app) |
| `firebase-setup-patterns.md` | (overlap G5) | `expo export` + `firebase deploy hosting` |
| `expo-router-navegacao.md` | ~50 | Rotas Expo (não deploy) |
| `react-native-web-patterns.md` | ~20 | Padrões web RN |

**Evidência eval:** gs-015 MISS inteiro.

---

### G7 — Auth (Expo / Firebase)

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `auth-patterns.md` | ~25 | **Canônico** Expo Firebase auth |
| `erp-auth-login.md` | ~15 | JWT multi-tenant ERP (Spring) — **outro domínio** |
| `outros.md` | (overlap) | Trechos auth legados |
| `decisoes.md` | (overlap) | Decisões Google Sign-In etc. |

**Evidência eval:** gs-004 hit@1 mas top-5 com 3× `erp-auth-login`; gs-005 rank 2 (`decisoes` #1).

---

### G8 — RAG / fábrica / protocolo agente

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `arquitetura-fabrica-ia.md` | 56 | Doc **canônico** técnico |
| `guia-completo-usuario-fabrica.md` | 49 | Onboarding humano (overlap ~40% com arquitetura) |
| `rag-protocolo-antes-de-codar.md` | ~12 | Protocolo libs/UI |
| `mcps-cursor-padrao.md` | ~15 | MCPs por tema |

**Evidência eval:** gs-018 MISS (`decisoes` + `guia` no top-5, **sem** `arquitetura`); gs-017 rank 2 (`erros-e-solucoes` #1); gs-022 rank 1 OK com `guia` #3.

---

### G9 — Erros vs decisões (memória operacional)

| Nota | Chunks | Papel atual |
|------|--------|-------------|
| `erros-e-solucoes.md` | 61 | `tipo_doc: solucao` — incidentes resolvidos |
| `decisoes.md` | **87** | Log cronológico — indexado como `padrao` |
| `template-erro-aprendizado.md` | ~5 | Template vazio |

**Evidência eval:** gs-003, gs-006, gs-008, gs-012, gs-017, gs-019, gs-021 — `decisoes` aparece no top-5 em **11/31** pares.

---

### G10 — Backend Spring (ERP novo vs SINAFLOR legado)

| Nota | Stack | Chunks |
|------|-------|--------|
| `erp-stack.md` | Java 25, SB 4.1, Postgres | ~8 |
| `erp-spring-camadas.md` | Camadas ERP | ~12 |
| `erp-multitenancy-spring.md` | Multi-tenant schema | ~10 |
| `erp-auth-login.md` | JWT | ~15 |
| `erp-transacao-dominio.md` | `@Transactional` | ~8 |
| `sinaflor/spring-backend.md` | Java **11**, SB **2.2** legado | 16 |
| `sinaflor/regras-gerais.md` | Regras legado | 2 |

**Relação:** **complementares por projeto**, mas BM25/denso confunde “spring boot”, “jpa”, “service”.

---

### G11 — Frontend Angular (ERP novo vs SINAFLOR legado)

| Nota | Stack | Chunks |
|------|-------|--------|
| `erp-angular-estrutura.md` | Angular **21**, signals, standalone | ~12 |
| `sinaflor/angular-frontend.md` | Angular **7.2**, PrimeNG, NgModule | 19 |
| `sinaflor/mapeamento-frontend-backend.md` | Services ↔ Resources SINAFLOR | 4 |

---

### G12 — Testes backend

| Nota | Stack | Chunks |
|------|-------|--------|
| `erp-testes-backend.md` | JUnit 5, Testcontainers, Postgres | ~15 |
| `sinaflor/testes-backend.md` | JUnit 5, Mockito, **sem** Testcontainers | 21 |

---

### G13 — Testes frontend

| Nota | Stack | Chunks |
|------|-------|--------|
| `sinaflor/testes-frontend.md` | Jasmine + Karma Angular 7 | 45 |
| *(sem equivalente ERP)* | — | — |

---

### G14 — Monólito residual

| Nota | Chunks | Origem |
|------|--------|--------|
| `outros.md` | **127** | `fonte: CLAUDE.md` — catch-all 76 seções |
| `padroes-fabrica.md` | 35 | Subconjunto CLAUDE (setup, UI) |
| `firestore-schemas.md` | 18 | Subconjunto CLAUDE genérico |
| `mercadopago-integration.md` | ~25 | Subconjunto CLAUDE §26–27 |

---

### G15 — PRDs (`projetos/`)

| Nota | tipo_doc |
|------|----------|
| `cortejo-prd.md`, `lashmatch-prd.md`, `setmatch-prd.md`, `sinaflor-prd.md` | `spec` |

**Evidência eval:** gs-003 top-5 com PRDs; filtro PRD no retrieval híbrido ajuda mas baseline v2 ainda indexa.

---

## 2. Recomendações por grupo (canônica · consolidar · duplicado vs complementar)

### G1 — Schema Firestore

| | Recomendação |
|---|-------------|
| **Canônica por app** | `cortejo-schemas.md` (Cortejo) · `lashmatch-schemas.md` (LashMatch) |
| **Consolidar em canônicas** | Trechos de salão/members em `padroes-fabrica.md` → link para `cortejo-schemas` |
| **Deprecar / não indexar como padrao** | `firestore-schemas.md` — modelo genérico users/posts **não** reflete apps reais; manter como `tipo_doc: legado` ou mover para `docs/archive/` |
| **Complementar** | `cadastro-clientes-salao-expo.md` — regras de negócio + link para schema do app |

---

### G2 — Mercado Pago

| | Recomendação |
|---|-------------|
| **Canônica transversal** | `mercadopago-integration.md` — API, webhook, preapproval |
| **Canônica por app** | `mercadopago-assinatura-ota-padroes.md` (Cortejo fluxo completo) · `lashmatch-mercadopago-assinatura.md` (LashMatch) |
| **Consolidar** | Overlap entre `lashmatch-modulos-assinatura-jun2026` e `lashmatch-mercadopago` — módulo deve **linkar** MP, não repetir §26–27 |
| **Duplicado** | Trechos MP em `outros.md` — remover na fase de decomposição |
| **Complementar** | `cortejo-modulos-jun2026-padrao` — orquestração dual RC+MP, não substitui `mercadopago-integration` |

---

### G3 — RevenueCat / iOS

| | Recomendação |
|---|-------------|
| **Canônica** | `lashmatch-revenuecat-assinatura.md` (LashMatch) · seção RC em `cortejo-modulos-jun2026-padrao` (Cortejo) |
| **Canônica roteamento MCP** | `mcps-cursor-padrao.md` — tabela “qual MCP” |
| **Consolidar** | gs-020: reforçar no topo de `mcps-cursor-padrao` bloco “pergunta qual MCP → esta nota primeiro” |

---

### G4 — WhatsApp

| | Recomendação |
|---|-------------|
| **Canônicas** | Manter **duas**: `whatsapp-business-api.md` (single) + `whatsapp-salao-expo-padrao.md` (multi) |
| **Consolidar** | Nada — são complementares |
| **Reduzir ruído** | Cross-links explícitos no topo de cada uma (“se multi-tenant → outra nota”) |

---

### G5 — Firebase deploy

| | Recomendação |
|---|-------------|
| **Canônica checklist** | `firebase-deploy-checklist-padrao.md` |
| **Canônica setup** | `firebase-setup-patterns.md` (init, hosting, env) |
| **Canônica functions** | `cloud-functions-patterns.md` |
| **Consolidar** | `checklists-deploy.md` → fundir checklist útil em `firebase-deploy-checklist-padrao`; resto arquivar |
| **Duplicado** | Trechos deploy em `arquitetura-fabrica-ia` — manter 1 parágrafo + link |
| **Complementar** | `arquitetura-fabrica-ia` — contexto hooks/Firebase dinâmico, não passo a passo deploy |

---

### G6 — Web / Hosting

| | Recomendação |
|---|-------------|
| **Canônica fluxo export+hosting** | Seção em `firebase-setup-patterns.md` (gs-015 esperado) |
| **Canônica produto LashMatch** | `lashmatch-web-plataforma.md` — **o que** a web faz, não **como** deploy |
| **Consolidar** | Adicionar em `lashmatch-web-plataforma` link “deploy → firebase-setup §Hosting” |
| **Não confundir** | `expo-router-navegacao.md` — rotas, não deploy; considerar `tipo_doc` ou metadado `tema: navegacao` no índice |

---

### G7 — Auth Expo vs ERP

| | Recomendação |
|---|-------------|
| **Canônica Expo** | `auth-patterns.md` |
| **Canônica ERP** | `erp-auth-login.md` |
| **Consolidar** | Não fundir — domínios diferentes |
| **Reduzir competição** | Indexação: tag/metadado `dominio: expo` vs `dominio: erp`; ou prefixo de query no eval |
| **Retrieval** | Demote cruzado: query com “expo/firebase” não rankear `erp-*`; query com “erp/jwt/spring” não rankear `auth-patterns` |

---

### G8 — RAG / arquitetura

| | Recomendação |
|---|-------------|
| **Canônica técnica** | `arquitetura-fabrica-ia.md` |
| **Canônica humano** | `guia-completo-usuario-fabrica.md` — onboarding, sem duplicar tabelas de hooks |
| **Canônica protocolo libs** | `rag-protocolo-antes-de-codar.md` |
| **Consolidar** | Seção “Indexação / porta 7332” **só** em `arquitetura` — `guia` linka; corrige gs-018 |
| **Complementar** | `guia` — pitch, clone repos, adicionar especialidade |

---

### G9 — Erros vs decisões

| | Recomendação |
|---|-------------|
| **Canônica incidentes** | `erros-e-solucoes.md` |
| **Canônica decisões arquiteturais** | Extrair de `decisoes.md` → notas temáticas (`decisoes` vira índice curto ou `tipo_doc: log`) |
| **Consolidar** | Cada `salvar_decisao` futura: se repetível → `atualizar_padrao` na nota de tema; log em `decisoes` só referência |
| **Duplicado** | Mesmo incidente em `decisoes` **e** `erros-e-solucoes` — manter só em erros |

---

### G10–G13 — ERP vs SINAFLOR

| | Recomendação |
|---|-------------|
| **Canônicas ERP** | `erp-stack.md` (índice) → `erp-spring-camadas`, `erp-multitenancy-spring`, `erp-auth-login`, `erp-testes-backend`, `erp-angular-estrutura` |
| **Canônicas SINAFLOR** | `sinaflor/INDEX.md` → `spring-backend`, `angular-frontend`, `testes-*`, `mapeamento-frontend-backend`, `regras-gerais` |
| **Consolidar** | **Não fundir** — stacks incompatíveis (Java 11 vs 25) |
| **Reduzir competição** | Metadado `projeto: erp` vs `projeto: sinaflor` no índice; pasta `sinaflor/` já existe — reforçar tags no chunk |
| **Duplicado conceitual** | Ambos falam “JUnit 5 + Mockito” — ERP nota deve abrir com “**Não** confundir com SINAFLOR legado” |

---

### G14 — `outros.md`

| | Recomendação |
|---|-------------|
| **Canônica** | **Nenhuma** — nota lixão |
| **Ação recomendada (fase 2)** | Decompor 76 seções em notas existentes ou novas; **excluir do índice** até decomposição completa |
| **Atalho** | `tipo_doc: legado` + demote no retrieval (como PRD spec) |

---

## 3. Notas-lixão e redução de ruído

### 3.1 `decisoes.md` — 87 chunks, ~35 KB

**Aparece no top-5 (baseline v2):** gs-003 (#1), gs-005 (#1), gs-007 (#5), gs-008 (#4), gs-009 (#5), gs-018 (#1–2), gs-019 (#1,3), gs-020 (#2), gs-021 (#4), gs-023 (#3).

**Por que polui:** cada decisão é um chunk pequeno com vocabulário rico (firebase, whatsapp, rag, mercado pago); `infer_tipo_doc` classifica como `padrao`, mesmo peso que guias canônicos.

**Opções (combináveis):**

| Opção | Prós | Contras |
|-------|------|---------|
| **A. `tipo_doc: log`** + demote no retrieval | Rápido, sem perder histórico | `buscar_historico` ainda precisa achar decisões |
| **B. Indexar só últimos N meses** | Reduz volume | Perde decisões antigas na busca |
| **C. Chunk por decisão com metadata `projeto:`** | Busca filtrável | Exige mudança em `indexar_rapido.py` |
| **D. `decisoes.md` fora do índice; só MCP `listar_decisoes` + RAG nas notas temáticas** | Elimina competição | Histórico semântico some |
| **E. Duplicata → erros:** migrar incidentes que estão só em decisoes para `erros-e-solucoes` | Corrige gs-003/019 | Trabalho manual |

**Recomendação:** **A + E + C** — reclassificar como `log`, migrar incidentes duplicados para erros, metadata por projeto. Manter `salvar_decisao` gravando log, mas decisões reutilizáveis devem ir para nota de tema via `atualizar_padrao`.

---

### 3.2 `outros.md` — 127 chunks, ~51 KB

**Aparece no top-5:** gs-011 (#1, #5), gs-021 (#3).

**Por que polui:** monólito CLAUDE com auth, firebase, MP, whatsapp, UI, snippets — **duplica** quase todos os grupos G1–G7.

**Opções:**

| Opção | Ação |
|-------|------|
| **1. Excluir do índice imediatamente** | Maior ganho de precisão; conteúdo permanece no disco |
| **2. Decompor em lote** | Script mapeia seção → nota destino; apaga seção após migrar |
| **3. `tipo_doc: legado` + demote forte** | Meio-termo se ainda precisar busca esporádica |

**Recomendação:** **1 agora, 2 depois** — excluir da indexação na próxima fase; decompor seções ainda úteis para notas canônicas (muitas já existem).

---

### 3.3 Outros poluidores menores

| Nota | Problema | Sugestão |
|------|----------|----------|
| `padroes-fabrica.md` | Ganha gs-002 em Firestore path | Remover trechos schema; link para `lashmatch-schemas` |
| `firestore-schemas.md` | Genérico confunde gs-001 | Arquivar ou `legado` |
| `guia-completo-usuario-fabrica.md` | Compete com arquitetura em RAG ops | Marcar `tipo_doc: onboarding` ou excluir seções duplicadas |
| `*-prd.md` | Spec no top-5 | Manter filtro `tipo_doc: spec` no retrieval (já parcial) |
| `erp-auth-login.md` | Aparece em query Expo auth | Metadado `dominio: erp` |

---

## 4. Notas backend/front sem par no golden set — propostas

Notas em `fabrica/sinaflor/` (indexadas, **zero** pares no `golden-set.jsonl` hoje).  
Equivalentes ERP existem com pares `erp-auth-*` mas **sem** pares para stack/camadas/testes/angular.

### 4.1 `sinaflor/spring-backend.md`

```jsonl
{"id":"sinaflor-be-01","query":"sinaflor backend java 11 spring boot 2.2 regras legado","esperado_nota":"sinaflor/spring-backend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-be-02","query":"jhipster entity repository service sinaflor padrao","esperado_nota":"sinaflor/spring-backend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-be-03","query":"jasper reports backend sinaflor como gerar pdf","esperado_nota":"sinaflor/spring-backend.md","esperado_secao":null,"tipo":"padrao"}
```

### 4.2 `sinaflor/angular-frontend.md`

```jsonl
{"id":"sinaflor-ng-01","query":"sinaflor angular 7 primeng modulo legado","esperado_nota":"sinaflor/angular-frontend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-ng-02","query":"rxjs observable subscribe sinaflor frontend padrao","esperado_nota":"sinaflor/angular-frontend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-ng-03","query":"http interceptor angular 7 sinaflor autenticacao","esperado_nota":"sinaflor/angular-frontend.md","esperado_secao":null,"tipo":"padrao"}
```

### 4.3 `sinaflor/testes-backend.md` *(vs `erp-testes-backend.md`)*

```jsonl
{"id":"sinaflor-test-be-01","query":"teste unitario junit 5 mockito sinaflor sem spring context","esperado_nota":"sinaflor/testes-backend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-test-be-02","query":"mockito when thenreturn repository sinaflor legado","esperado_nota":"sinaflor/testes-backend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-test-be-03","query":"erp testcontainers postgres spring boot teste integracao","esperado_nota":"erp-testes-backend.md","esperado_secao":null,"tipo":"padrao","aceitaveis":["erp-testes-backend.md"]}
```

> O terceiro par **deliberadamente** separa ERP (Testcontainers) de SINAFLOR — valida que consolidação não mistura stacks.

### 4.4 `sinaflor/testes-frontend.md`

```jsonl
{"id":"sinaflor-test-fe-01","query":"jasmine karma teste componente angular 7 sinaflor","esperado_nota":"sinaflor/testes-frontend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-test-fe-02","query":"testbed configuretestingmodule sinaflor frontend","esperado_nota":"sinaflor/testes-frontend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-test-fe-03","query":"debug element nativeelement query sinaflor spec","esperado_nota":"sinaflor/testes-frontend.md","esperado_secao":null,"tipo":"padrao"}
```

### 4.5 `sinaflor/mapeamento-frontend-backend.md`

```jsonl
{"id":"sinaflor-map-01","query":"service angular chama qual endpoint resource sinaflor","esperado_nota":"sinaflor/mapeamento-frontend-backend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-map-02","query":"mapeamento frontend backend ibama sinaflor2 monorepo","esperado_nota":"sinaflor/mapeamento-frontend-backend.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-map-03","query":"dto request response entre angular e spring sinaflor","esperado_nota":"sinaflor/mapeamento-frontend-backend.md","esperado_secao":null,"tipo":"padrao"}
```

### 4.6 `sinaflor/regras-gerais.md`

```jsonl
{"id":"sinaflor-regras-01","query":"sinaflor legado o que nao fazer modernizar","esperado_nota":"sinaflor/regras-gerais.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-regras-02","query":"regra fabrica projeto sinaflor2 angular 7 java 11","esperado_nota":"sinaflor/regras-gerais.md","esperado_secao":null,"tipo":"padrao"}
{"id":"sinaflor-regras-03","query":"posso usar java 17 records no sinaflor","esperado_nota":"sinaflor/regras-gerais.md","esperado_secao":null,"tipo":"solucao"}
```

### 4.7 Notas ERP ainda sem par (além de `erp-auth-*`)

| Nota | Pares sugeridos |
|------|-----------------|
| `erp-spring-camadas.md` | `erp-cam-01` "controller service repository dto erp onde fica regra" · `erp-cam-02` "retornar entidade jpa na api erp" |
| `erp-multitenancy-spring.md` | já coberto indiretamente por `erp-auth-*`; adicionar `erp-mt-04` "hibernate troca schema tenant threadlocal" |
| `erp-angular-estrutura.md` | `erp-ng-01` "angular 21 standalone signals erp" · `erp-ng-02` "anexar jwt interceptor angular erp" |
| `erp-stack.md` | `erp-stack-01` "qual stack java spring postgres angular erp" · `erp-stack-02` "erp usa firestore ou postgres" |

---

## 5. Ordem de execução sugerida (após sua revisão)

| Fase | Ação | Risco | Ganho eval estimado |
|------|------|-------|---------------------|
| **0** | Aprovar este plano | — | — |
| **1** | Excluir `outros.md` do índice (`should_index` ou mover) | Baixo | gs-011, ruído geral |
| **2** | `decisoes.md` → `tipo_doc: log` + demote | Médio | gs-003,005,018,019,020 |
| **3** | Arquivar `firestore-schemas.md` do índice `padrao` | Baixo | gs-001, gs-002 |
| **4** | Links + dedup em MP (`outros` já fora) | Baixo | gs-010, gs-012 |
| **5** | `guia` vs `arquitetura` — uma seção RAG só em arquitetura | Baixo | gs-018 |
| **6** | Metadado `dominio: erp|expo|sinaflor` no índice | Médio | gs-004, cross-stack |
| **7** | Adicionar pares golden SINAFLOR + ERP stack | Nenhum (só mede) | Cobertura |
| **8** | Re-run `run_baseline.py --regua v2` | — | Validar |

---

## 6. Pares MISS / rank 2–3 — diagnóstico rápido

| ID | Rank | Causa provável |
|----|------|----------------|
| gs-001 | MISS | Schema Cortejo fraco vs MP/ERP/postgres genérico; `firestore-schemas` não ajuda |
| gs-002 | 2 | `padroes-fabrica` compete com `lashmatch-schemas` |
| gs-003 | 2 | `decisoes` #1 vs `erros-e-solucoes` |
| gs-005 | 2 | `decisoes` #1 vs `auth-patterns` |
| gs-010 | 3 | `mercadopago-assinatura-ota` + `lashmatch-mercadopago` antes da canônica |
| gs-011 | 2 | **`outros.md` #1** |
| gs-012 | 3 | `mercadopago-assinatura-ota` #1 vs erros |
| gs-013 | 2 | Checklist deploy vs cloud-functions (aceitável semanticamente) |
| gs-015 | MISS | `lashmatch-web-plataforma` + `expo-router` vs hosting em `firebase-setup` |
| gs-017 | 2 | `erros-e-solucoes` #1 vs `rag-protocolo` |
| gs-018 | MISS | `decisoes` + `guia` — **falta** `arquitetura` no top-5 |
| gs-019 | 2 | `decisoes` #1 vs erros |
| gs-020 | 3 | MP + RC antes de `mcps-cursor-padrao` |

---

## 7. O que NÃO fazer

- Fundir `erp-*` com `sinaflor/*` — stacks diferentes.
- Apagar `decisoes.md` — é audit trail; só mudar **peso no índice**.
- Deletar `outros.md` do disco antes de mapear seções ainda não migradas.
- Consolidar `whatsapp-business-api` + `whatsapp-salao-expo-padrao` — casos de uso distintos.

---

*Relatório gerado para revisão. Nenhuma alteração aplicada no vault além deste arquivo.*

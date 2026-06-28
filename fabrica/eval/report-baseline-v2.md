# RAG Eval — Baseline v2 (réguas justas)

Gerado em: 2026-06-28T19:11:01.460878+00:00
Servidor: `http://localhost:7332/buscar` · top-k=5
Régua: **v2** (hit se `esperado_nota` ou qualquer `aceitaveis` no top-k; MRR = melhor rank entre alvos)

## Auto-checagem do golden set

- Pares: **25**
- Com `aceitaveis`: **3**
- Com `revisar: true`: **5** — gs-002, gs-009, gs-011, gs-014, gs-019
- Cobertura por tipo: `{'padrao': 5, 'solucao': 6, 'integracao': 4, 'fluxo': 4, 'fabrica': 6}`

Validação: **OK** (todos os `esperado_nota` existem, sem queries duplicadas).

## Métricas agregadas

| Métrica | Valor |
|---------|-------|
| hit@1 | 48.0% |
| hit@3 | 72.0% |
| hit@5 | 76.0% |
| MRR | 0.5947 |

## Por tipo

| tipo | n | hit@1 | hit@3 | hit@5 | MRR |
|------|---|-------|-------|-------|-----|
| fabrica | 6 | 66.7% | 66.7% | 66.7% | 0.6667 |
| fluxo | 4 | 25.0% | 50.0% | 50.0% | 0.3750 |
| integracao | 4 | 25.0% | 75.0% | 100.0% | 0.5500 |
| padrao | 5 | 40.0% | 60.0% | 60.0% | 0.4667 |
| solucao | 6 | 66.7% | 100.0% | 100.0% | 0.8056 |

## Detalhe por query

### gs-001 — MISS

- **Query:** como modelar salão e members no firestore multi-tenant?
- **Esperado:** `cortejo-schemas.md` (padrao)
- **Top-5:** `cortejo-prd.md`, `erros-e-solucoes.md`, `cortejo-prd.md`, `cortejo-prd.md`, `cortejo-prd.md`

### gs-002 — rank 3 ⚠️ revisar

- **Query:** qual path artifacts appId users uid no firestore?
- **Esperado:** `lashmatch-schemas.md` (padrao)
- **Aceitáveis:** `lashmatch-schemas.md`, `firebase-setup-patterns.md`
- **Top-5:** `report-baseline.md`, `padroes-fabrica.md`, `firebase-setup-patterns.md`, `lashmatch-prd.md`, `whatsapp-salao-expo-padrao.md`

### gs-003 — rank 3

- **Query:** permission-denied ao criar conta do salão no onboarding
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `cortejo-prd.md`, `decisoes.md`, `erros-e-solucoes.md`, `cortejo-prd.md`, `mercadopago-integration.md`

### gs-004 — rank 1

- **Query:** login email e senha com firebase no expo
- **Esperado:** `auth-patterns.md` (padrao)
- **Top-5:** `auth-patterns.md`, `whatsapp-salao-expo-padrao.md`, `auth-patterns.md`, `whatsapp-salao-expo-padrao.md`, `auth-patterns.md`

### gs-005 — rank 1

- **Query:** google sign in no expo go qual pacote usar?
- **Esperado:** `auth-patterns.md` (padrao)
- **Top-5:** `auth-patterns.md`, `decisoes.md`, `auth-patterns.md`, `whatsapp-salao-expo-padrao.md`, `erros-e-solucoes.md`

### gs-006 — rank 1

- **Query:** androidClientId must be defined google auth expo
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `erros-e-solucoes.md`, `erros-e-solucoes.md`, `decisoes.md`, `auth-patterns.md`, `auth-patterns.md`

### gs-007 — rank 2

- **Query:** como enviar template whatsapp pela meta cloud api?
- **Esperado:** `whatsapp-business-api.md` (integracao)
- **Top-5:** `decisoes.md`, `whatsapp-business-api.md`, `modulo-ajuda-suporte-expo.md`, `lashmatch-prd.md`, `whatsapp-business-api.md`

### gs-008 — rank 1

- **Query:** whatsapp erro 132001 template não existe
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `erros-e-solucoes.md`, `erros-e-solucoes.md`, `decisoes.md`, `erros-e-solucoes.md`, `whatsapp-business-api.md`

### gs-009 — rank 1 ⚠️ revisar

- **Query:** webhook whatsapp multi-tenant phoneNumberId roteamento
- **Esperado:** `whatsapp-salao-expo-padrao.md` (integracao)
- **Aceitáveis:** `whatsapp-salao-expo-padrao.md`, `whatsapp-business-api.md`
- **Top-5:** `whatsapp-salao-expo-padrao.md`, `whatsapp-salao-expo-padrao.md`, `whatsapp-business-api.md`, `whatsapp-salao-expo-padrao.md`, `whatsapp-salao-expo-padrao.md`

### gs-010 — rank 2

- **Query:** assinatura recorrente mercado pago preapproval cartão tokenizado
- **Esperado:** `mercadopago-integration.md` (integracao)
- **Top-5:** `cortejo-prd.md`, `mercadopago-integration.md`, `mercadopago-assinatura-ota-padroes.md`, `lashmatch-modulos-assinatura-jun2026.md`, `lashmatch-prd.md`

### gs-011 — rank 5 ⚠️ revisar

- **Query:** webhook mercado pago confirma pagamento cloud function
- **Esperado:** `mercadopago-integration.md` (integracao)
- **Aceitáveis:** `mercadopago-integration.md`, `cloud-functions-patterns.md`
- **Top-5:** `outros.md`, `cortejo-prd.md`, `lashmatch-prd.md`, `report-baseline.md`, `mercadopago-integration.md`

### gs-012 — rank 2

- **Query:** cancelou assinatura no app mas mp continuou cobrando
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `mercadopago-assinatura-ota-padroes.md`, `erros-e-solucoes.md`, `mercadopago-integration.md`, `erros-e-solucoes.md`, `mercadopago-assinatura-ota-padroes.md`

### gs-013 — rank 2

- **Query:** deploy só cloud functions firebase build antes
- **Esperado:** `cloud-functions-patterns.md` (fluxo)
- **Top-5:** `checklists-deploy.md`, `cloud-functions-patterns.md`, `arquitetura-fabrica-ia.md`, `cloud-functions-patterns.md`, `arquitetura-fabrica-ia.md`

### gs-014 — MISS ⚠️ revisar

- **Query:** checklist antes de rodar firebase deploy
- **Esperado:** `checklists-deploy.md` (fluxo)
- **Top-5:** `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `report-baseline.md`, `mcps-cursor-padrao.md`, `arquitetura-fabrica-ia.md`

### gs-015 — MISS

- **Query:** expo export web e deploy firebase hosting
- **Esperado:** `firebase-setup-patterns.md` (fluxo)
- **Top-5:** `expo-router-navegacao.md`, `lashmatch-web-plataforma.md`, `report-baseline.md`, `cortejo-modulos-jun2026-padrao.md`, `lashmatch-web-plataforma.md`

### gs-016 — rank 1

- **Query:** gate bloqueia write até chamar rag_buscar
- **Esperado:** `arquitetura-fabrica-ia.md` (fabrica)
- **Top-5:** `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `erros-e-solucoes.md`, `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`

### gs-017 — MISS

- **Query:** dev pediu lib externa devo consultar rag antes?
- **Esperado:** `rag-protocolo-antes-de-codar.md` (fabrica)
- **Top-5:** `decisoes.md`, `decisoes.md`, `erros-e-solucoes.md`, `decisoes.md`, `decisoes.md`

### gs-018 — rank 1

- **Query:** como subir servidor chroma rag porta 7332?
- **Esperado:** `arquitetura-fabrica-ia.md` (fabrica)
- **Top-5:** `arquitetura-fabrica-ia.md`, `whatsapp-salao-expo-padrao.md`, `erros-e-solucoes.md`, `auth-patterns.md`, `auth-patterns.md`

### gs-019 — rank 1 ⚠️ revisar

- **Query:** servidor rag fecha depois de carregar modelo chroma
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `erros-e-solucoes.md`, `arquitetura-fabrica-ia.md`, `spring-backend.md`, `erros-e-solucoes.md`, `arquitetura-fabrica-ia.md`

### gs-020 — MISS

- **Query:** mercado pago ou revenuecat qual mcp usar?
- **Esperado:** `mcps-cursor-padrao.md` (fabrica)
- **Top-5:** `decisoes.md`, `decisoes.md`, `decisoes.md`, `decisoes.md`, `firestore-schemas.md`

### gs-021 — rank 1

- **Query:** agente codou calendário sem buscar no rag
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `erros-e-solucoes.md`, `cloud-functions-patterns.md`, `whatsapp-business-api.md`, `outros.md`, `outros.md`

### gs-022 — rank 1

- **Query:** fluxo criar feature branch e abrir pr na fabrica
- **Esperado:** `arquitetura-fabrica-ia.md` (fluxo)
- **Top-5:** `arquitetura-fabrica-ia.md`, `firestore-schemas.md`, `context-api-estado.md`, `sinaflor-prd.md`, `features-pendentes.md`

### gs-023 — MISS

- **Query:** cadastro de clientes do salão regra isMember firestore
- **Esperado:** `cadastro-clientes-salao-expo.md` (padrao)
- **Top-5:** `erros-e-solucoes.md`, `erros-e-solucoes.md`, `cortejo-prd.md`, `erros-e-solucoes.md`, `decisoes.md`

### gs-024 — rank 1

- **Query:** diferença rag_buscar buscar_historico buscar_solucao
- **Esperado:** `arquitetura-fabrica-ia.md` (fabrica)
- **Top-5:** `arquitetura-fabrica-ia.md`, `erros-e-solucoes.md`, `decisoes.md`, `arquitetura-fabrica-ia.md`, `report-baseline.md`

### gs-025 — rank 1

- **Query:** deploy firebase no projeto errado como evitar
- **Esperado:** `arquitetura-fabrica-ia.md` (fabrica)
- **Top-5:** `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `checklists-deploy.md`, `erros-e-solucoes.md`, `firebase-setup-patterns.md`

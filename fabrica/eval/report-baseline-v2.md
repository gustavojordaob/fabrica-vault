# RAG Eval — Baseline v2 (réguas justas)

Gerado em: 2026-06-29T13:24:11.750777+00:00
Servidor: `http://127.0.0.1:7332/buscar` · top-k=5
Régua: **v2** (hit se `esperado_nota` ou qualquer `aceitaveis` no top-k; MRR = melhor rank entre alvos)

## Auto-checagem do golden set

- Pares: **56**
- Com `aceitaveis`: **4**
- Com `revisar: true`: **3** — gs-002, gs-009, gs-011
- Cobertura por tipo: `{'padrao': 33, 'solucao': 9, 'integracao': 4, 'fluxo': 4, 'fabrica': 6}`

Validação: **OK** (todos os `esperado_nota` existem, sem queries duplicadas).

## Métricas agregadas

| Métrica | Valor |
|---------|-------|
| hit@1 | 66.1% |
| hit@3 | 87.5% |
| hit@5 | 91.1% |
| MRR | 0.7571 |

## Por tipo

| tipo | n | hit@1 | hit@3 | hit@5 | MRR |
|------|---|-------|-------|-------|-----|
| fabrica | 6 | 50.0% | 83.3% | 83.3% | 0.6389 |
| fluxo | 4 | 50.0% | 75.0% | 75.0% | 0.6250 |
| integracao | 4 | 75.0% | 100.0% | 100.0% | 0.8333 |
| padrao | 33 | 69.7% | 87.9% | 90.9% | 0.7788 |
| solucao | 9 | 66.7% | 88.9% | 100.0% | 0.7815 |

## Detalhe por query

### gs-001 — MISS

- **Query:** como modelar salão e members no firestore multi-tenant?
- **Esperado:** `cortejo-schemas.md` (padrao)
- **Top-5:** `erros-e-solucoes.md`, `lashmatch-mercadopago-assinatura.md`, `erp-postgres-schema.md`, `excluir-conta-app-expo-padrao.md`, `whatsapp-salao-expo-padrao.md`

### gs-002 — rank 2 ⚠️ revisar

- **Query:** qual path artifacts appId users uid no firestore?
- **Esperado:** `lashmatch-schemas.md` (padrao)
- **Aceitáveis:** `lashmatch-schemas.md`, `firebase-setup-patterns.md`
- **Top-5:** `padroes-fabrica.md`, `firebase-setup-patterns.md`, `whatsapp-salao-expo-padrao.md`, `cloud-functions-patterns.md`, `arquitetura-fabrica-ia.md`

### gs-003 — rank 1

- **Query:** permission-denied ao criar conta do salão no onboarding
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `erros-e-solucoes.md`, `decisoes.md`, `cortejo-prd.md`, `setmatch-prd.md`, `erros-e-solucoes.md`

### gs-004 — rank 1

- **Query:** login email e senha com firebase no expo
- **Esperado:** `auth-patterns.md` (padrao)
- **Top-5:** `auth-patterns.md`, `auth-patterns.md`, `erp-auth-login.md`, `erp-auth-login.md`, `erp-auth-login.md`

### gs-005 — rank 2

- **Query:** google sign in no expo go qual pacote usar?
- **Esperado:** `auth-patterns.md` (padrao)
- **Top-5:** `decisoes.md`, `auth-patterns.md`, `auth-patterns.md`, `erros-e-solucoes.md`, `expo-router-navegacao.md`

### gs-006 — rank 1

- **Query:** androidClientId must be defined google auth expo
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `erros-e-solucoes.md`, `erros-e-solucoes.md`, `decisoes.md`, `auth-patterns.md`, `auth-patterns.md`

### gs-007 — rank 1

- **Query:** como enviar template whatsapp pela meta cloud api?
- **Esperado:** `whatsapp-business-api.md` (integracao)
- **Top-5:** `whatsapp-business-api.md`, `whatsapp-business-api.md`, `whatsapp-business-api.md`, `decisoes.md`, `whatsapp-salao-expo-padrao.md`

### gs-008 — rank 1

- **Query:** whatsapp erro 132001 template não existe
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `erros-e-solucoes.md`, `erros-e-solucoes.md`, `erros-e-solucoes.md`, `decisoes.md`, `erros-e-solucoes.md`

### gs-009 — rank 1 ⚠️ revisar

- **Query:** webhook whatsapp multi-tenant phoneNumberId roteamento
- **Esperado:** `whatsapp-salao-expo-padrao.md` (integracao)
- **Aceitáveis:** `whatsapp-salao-expo-padrao.md`, `whatsapp-business-api.md`
- **Top-5:** `whatsapp-salao-expo-padrao.md`, `whatsapp-salao-expo-padrao.md`, `whatsapp-salao-expo-padrao.md`, `decisoes.md`, `whatsapp-salao-expo-padrao.md`

### gs-010 — rank 3

- **Query:** assinatura recorrente mercado pago preapproval cartão tokenizado
- **Esperado:** `mercadopago-integration.md` (integracao)
- **Top-5:** `mercadopago-assinatura-ota-padroes.md`, `lashmatch-mercadopago-assinatura.md`, `mercadopago-integration.md`, `mercadopago-integration.md`, `mercadopago-assinatura-ota-padroes.md`

### gs-011 — rank 1 ⚠️ revisar

- **Query:** webhook mercado pago confirma pagamento cloud function
- **Esperado:** `mercadopago-integration.md` (integracao)
- **Aceitáveis:** `mercadopago-integration.md`, `cloud-functions-patterns.md`
- **Top-5:** `mercadopago-integration.md`, `mercadopago-integration.md`, `cortejo-prd.md`, `mercadopago-integration.md`, `mercadopago-assinatura-ota-padroes.md`

### gs-012 — rank 3

- **Query:** cancelou assinatura no app mas mp continuou cobrando
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `mercadopago-assinatura-ota-padroes.md`, `mercadopago-integration.md`, `erros-e-solucoes.md`, `erros-e-solucoes.md`, `erros-e-solucoes.md`

### gs-013 — rank 2

- **Query:** deploy só cloud functions firebase build antes
- **Esperado:** `cloud-functions-patterns.md` (fluxo)
- **Top-5:** `firebase-deploy-checklist-padrao.md`, `cloud-functions-patterns.md`, `cloud-functions-patterns.md`, `whatsapp-salao-expo-padrao.md`, `cloud-functions-patterns.md`

### gs-014 — rank 1

- **Query:** checklist antes de rodar firebase deploy
- **Esperado:** `firebase-deploy-checklist-padrao.md` (fluxo)
- **Top-5:** `firebase-deploy-checklist-padrao.md`, `firebase-deploy-checklist-padrao.md`, `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`

### gs-015 — MISS

- **Query:** expo export web e deploy firebase hosting
- **Esperado:** `firebase-setup-patterns.md` (fluxo)
- **Top-5:** `lashmatch-web-plataforma.md`, `expo-router-navegacao.md`, `expo-router-navegacao.md`, `lashmatch-web-plataforma.md`, `expo-router-navegacao.md`

### gs-016 — rank 1

- **Query:** gate bloqueia write até chamar rag_buscar
- **Esperado:** `arquitetura-fabrica-ia.md` (fabrica)
- **Top-5:** `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `mcps-cursor-padrao.md`

### gs-017 — rank 2

- **Query:** dev pediu lib externa devo consultar rag antes?
- **Esperado:** `rag-protocolo-antes-de-codar.md` (fabrica)
- **Top-5:** `erros-e-solucoes.md`, `rag-protocolo-antes-de-codar.md`, `arquitetura-fabrica-ia.md`, `rag-protocolo-antes-de-codar.md`, `erros-e-solucoes.md`

### gs-018 — MISS

- **Query:** como subir servidor chroma rag porta 7332?
- **Esperado:** `arquitetura-fabrica-ia.md` (fabrica)
- **Top-5:** `decisoes.md`, `decisoes.md`, `guia-completo-usuario-fabrica.md`, `guia-completo-usuario-fabrica.md`, `guia-completo-usuario-fabrica.md`

### gs-019 — rank 2

- **Query:** servidor rag fecha depois de carregar modelo chroma
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `decisoes.md`, `erros-e-solucoes.md`, `decisoes.md`, `arquitetura-fabrica-ia.md`, `guia-completo-usuario-fabrica.md`

### gs-020 — rank 3

- **Query:** mercado pago ou revenuecat qual mcp usar?
- **Esperado:** `mcps-cursor-padrao.md` (fabrica)
- **Top-5:** `mercadopago-integration.md`, `decisoes.md`, `mcps-cursor-padrao.md`, `lashmatch-revenuecat-assinatura.md`, `lashmatch-modulos-assinatura-jun2026.md`

### gs-021 — rank 1

- **Query:** agente codou calendário sem buscar no rag
- **Esperado:** `erros-e-solucoes.md` (solucao)
- **Top-5:** `erros-e-solucoes.md`, `rag-protocolo-antes-de-codar.md`, `decisoes.md`, `rag-protocolo-antes-de-codar.md`, `agenda-salao-expo-padrao.md`

### gs-022 — rank 1

- **Query:** fluxo criar feature branch e abrir pr na fabrica
- **Esperado:** `arquitetura-fabrica-ia.md` (fluxo)
- **Top-5:** `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `guia-completo-usuario-fabrica.md`, `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`

### gs-023 — rank 1

- **Query:** cadastro de clientes do salão regra isMember firestore
- **Esperado:** `cadastro-clientes-salao-expo.md` (padrao)
- **Top-5:** `cadastro-clientes-salao-expo.md`, `erros-e-solucoes.md`, `decisoes.md`, `mercadopago-assinatura-ota-padroes.md`, `cortejo-schemas.md`

### gs-024 — rank 1

- **Query:** diferença rag_buscar buscar_historico buscar_solucao
- **Esperado:** `arquitetura-fabrica-ia.md` (fabrica)
- **Top-5:** `arquitetura-fabrica-ia.md`, `arquitetura-fabrica-ia.md`, `mcps-cursor-padrao.md`, `arquitetura-fabrica-ia.md`, `mcps-cursor-padrao.md`

### gs-025 — rank 1

- **Query:** deploy firebase no projeto errado como evitar
- **Esperado:** `arquitetura-fabrica-ia.md` (fabrica)
- **Top-5:** `arquitetura-fabrica-ia.md`, `firebase-deploy-checklist-padrao.md`, `expo-router-navegacao.md`, `firebase-setup-patterns.md`, `checklists-deploy.md`

### erp-auth-01 — rank 1

- **Query:** como faz login multi tenant jwt erp
- **Esperado:** `erp-auth-login.md` (padrao)
- **Top-5:** `erp-auth-login.md`, `erp-auth-login.md`, `erp-multitenancy-spring.md`, `erp-auth-login.md`, `erp-auth-login.md`

### erp-auth-02 — rank 1

- **Query:** onde fica a tabela de usuario tenant ou master
- **Esperado:** `erp-auth-login.md` (padrao)
- **Top-5:** `erp-auth-login.md`, `erp-postgres-schema.md`, `erp-auth-login.md`, `erp-postgres-schema.md`, `erp-multitenancy-spring.md`

### erp-auth-03 — rank 1

- **Query:** como o tenant entra no token jwt
- **Esperado:** `erp-auth-login.md` (padrao)
- **Top-5:** `erp-auth-login.md`, `erp-auth-login.md`, `erp-angular-estrutura.md`, `erp-auth-login.md`, `erp-auth-login.md`

### erp-auth-04 — rank 1

- **Query:** recuperar senha esqueci senha seguro
- **Esperado:** `erp-auth-login.md` (solucao)
- **Top-5:** `erp-auth-login.md`, `erp-auth-login.md`, `setmatch-prd.md`, `erp-auth-login.md`, `erp-auth-login.md`

### erp-auth-05 — rank 1

- **Query:** lembrar-me refresh token quanto tempo
- **Esperado:** `erp-auth-login.md` (padrao)
- **Top-5:** `erp-auth-login.md`, `erp-auth-login.md`, `erp-auth-login.md`, `erp-auth-login.md`, `erp-auth-login.md`

### erp-auth-06 — rank 1

- **Query:** ordem filtro jwt tenant spring security
- **Esperado:** `erp-auth-login.md` (solucao)
- **Top-5:** `erp-auth-login.md`, `erp-auth-login.md`, `erp-auth-login.md`, `erp-auth-login.md`, `erp-multitenancy-spring.md`

### sinaflor-be-01 — rank 1

- **Query:** sinaflor backend java 11 spring boot 2.2 regras legado
- **Esperado:** `spring-backend.md` (padrao)
- **Top-5:** `spring-backend.md`, `INDEX.md`, `spring-backend.md`, `erp-spring-camadas.md`, `testes-backend.md`

### sinaflor-be-02 — rank 1

- **Query:** jhipster entity repository service sinaflor padrao
- **Esperado:** `spring-backend.md` (padrao)
- **Top-5:** `spring-backend.md`, `erp-spring-camadas.md`, `mapeamento-frontend-backend.md`, `regras-gerais.md`, `testes-backend.md`

### sinaflor-be-03 — rank 2

- **Query:** jasper reports backend sinaflor como gerar pdf
- **Esperado:** `spring-backend.md` (padrao)
- **Top-5:** `mapeamento-frontend-backend.md`, `spring-backend.md`, `testes-backend.md`, `INDEX.md`, `spring-backend.md`

### sinaflor-ng-01 — rank 1

- **Query:** sinaflor angular 7 primeng modulo legado
- **Esperado:** `angular-frontend.md` (padrao)
- **Top-5:** `angular-frontend.md`, `sinaflor-prd.md`, `regras-gerais.md`, `INDEX.md`, `angular-frontend.md`

### sinaflor-ng-02 — rank 1

- **Query:** rxjs observable subscribe sinaflor frontend padrao
- **Esperado:** `angular-frontend.md` (padrao)
- **Top-5:** `angular-frontend.md`, `mapeamento-frontend-backend.md`, `spring-backend.md`, `testes-backend.md`, `testes-frontend.md`

### sinaflor-ng-03 — rank 1

- **Query:** http interceptor angular 7 sinaflor autenticacao
- **Esperado:** `angular-frontend.md` (padrao)
- **Top-5:** `angular-frontend.md`, `angular-frontend.md`, `sinaflor-prd.md`, `testes-frontend.md`, `spring-backend.md`

### sinaflor-test-be-01 — rank 1

- **Query:** teste unitario junit 5 mockito sinaflor sem spring context
- **Esperado:** `testes-backend.md` (padrao)
- **Top-5:** `testes-backend.md`, `testes-backend.md`, `INDEX.md`, `testes-frontend.md`, `spring-backend.md`

### sinaflor-test-be-02 — rank 1

- **Query:** mockito when thenreturn repository sinaflor legado
- **Esperado:** `testes-backend.md` (padrao)
- **Top-5:** `testes-backend.md`, `regras-gerais.md`, `spring-backend.md`, `mapeamento-frontend-backend.md`, `sinaflor-prd.md`

### sinaflor-test-be-03 — rank 1

- **Query:** erp testcontainers postgres spring boot teste integracao
- **Esperado:** `erp-testes-backend.md` (padrao)
- **Aceitáveis:** `erp-testes-backend.md`
- **Top-5:** `erp-testes-backend.md`, `erp-testes-backend.md`, `erp-testes-backend.md`, `erp-testes-backend.md`, `erp-testes-backend.md`

### sinaflor-test-fe-01 — rank 1

- **Query:** jasmine karma teste componente angular 7 sinaflor
- **Esperado:** `testes-frontend.md` (padrao)
- **Top-5:** `testes-frontend.md`, `testes-frontend.md`, `INDEX.md`, `angular-frontend.md`, `erp-angular-estrutura.md`

### sinaflor-test-fe-02 — rank 1

- **Query:** testbed configuretestingmodule sinaflor frontend
- **Esperado:** `testes-frontend.md` (padrao)
- **Top-5:** `testes-frontend.md`, `testes-backend.md`, `testes-frontend.md`, `testes-frontend.md`, `angular-frontend.md`

### sinaflor-test-fe-03 — rank 3

- **Query:** debug element nativeelement query sinaflor spec
- **Esperado:** `testes-frontend.md` (padrao)
- **Top-5:** `testes-backend.md`, `sinaflor-prd.md`, `testes-frontend.md`, `angular-frontend.md`, `INDEX.md`

### sinaflor-map-01 — MISS

- **Query:** service angular chama qual endpoint resource sinaflor
- **Esperado:** `mapeamento-frontend-backend.md` (padrao)
- **Top-5:** `sinaflor-prd.md`, `erp-angular-estrutura.md`, `sinaflor-prd.md`, `angular-frontend.md`, `erp-angular-estrutura.md`

### sinaflor-map-02 — rank 1

- **Query:** mapeamento frontend backend ibama sinaflor2 monorepo
- **Esperado:** `mapeamento-frontend-backend.md` (padrao)
- **Top-5:** `mapeamento-frontend-backend.md`, `sinaflor-prd.md`, `angular-frontend.md`, `INDEX.md`, `spring-backend.md`

### sinaflor-map-03 — MISS

- **Query:** dto request response entre angular e spring sinaflor
- **Esperado:** `mapeamento-frontend-backend.md` (padrao)
- **Top-5:** `sinaflor-prd.md`, `erp-stack.md`, `angular-frontend.md`, `erp-angular-estrutura.md`, `testes-frontend.md`

### sinaflor-regras-01 — rank 1

- **Query:** sinaflor legado o que nao fazer modernizar
- **Esperado:** `regras-gerais.md` (padrao)
- **Top-5:** `regras-gerais.md`, `testes-backend.md`, `INDEX.md`, `mapeamento-frontend-backend.md`, `angular-frontend.md`

### sinaflor-regras-02 — rank 5

- **Query:** regra fabrica projeto sinaflor2 angular 7 java 11
- **Esperado:** `regras-gerais.md` (padrao)
- **Top-5:** `angular-frontend.md`, `angular-frontend.md`, `INDEX.md`, `spring-backend.md`, `regras-gerais.md`

### sinaflor-regras-03 — rank 5

- **Query:** posso usar java 17 records no sinaflor
- **Esperado:** `regras-gerais.md` (solucao)
- **Top-5:** `spring-backend.md`, `testes-backend.md`, `testes-frontend.md`, `mapeamento-frontend-backend.md`, `regras-gerais.md`

### erp-cam-01 — rank 1

- **Query:** controller service repository dto erp onde fica regra
- **Esperado:** `erp-spring-camadas.md` (padrao)
- **Top-5:** `erp-spring-camadas.md`, `erp-spring-camadas.md`, `erp-spring-camadas.md`, `erp-spring-camadas.md`, `erp-transacao-dominio.md`

### erp-cam-02 — rank 1

- **Query:** retornar entidade jpa na api erp
- **Esperado:** `erp-spring-camadas.md` (padrao)
- **Top-5:** `erp-spring-camadas.md`, `erp-auth-login.md`, `erp-auth-login.md`, `decisoes.md`, `erp-spring-camadas.md`

### erp-mt-04 — rank 1

- **Query:** hibernate troca schema tenant threadlocal
- **Esperado:** `erp-multitenancy-spring.md` (padrao)
- **Top-5:** `erp-multitenancy-spring.md`, `erp-multitenancy-spring.md`, `erp-multitenancy-spring.md`, `erp-multitenancy-spring.md`, `erp-multitenancy-spring.md`

### erp-ng-01 — rank 1

- **Query:** angular 21 standalone signals erp
- **Esperado:** `erp-angular-estrutura.md` (padrao)
- **Top-5:** `erp-angular-estrutura.md`, `erp-angular-estrutura.md`, `erp-angular-estrutura.md`, `erp-angular-estrutura.md`, `angular-frontend.md`

### erp-ng-02 — rank 1

- **Query:** anexar jwt interceptor angular erp
- **Esperado:** `erp-angular-estrutura.md` (padrao)
- **Top-5:** `erp-angular-estrutura.md`, `erp-stack.md`, `erp-stack.md`, `erp-angular-estrutura.md`, `sinaflor-prd.md`

### erp-stack-01 — rank 3

- **Query:** qual stack java spring postgres angular erp
- **Esperado:** `erp-stack.md` (padrao)
- **Top-5:** `erp-angular-estrutura.md`, `sinaflor-prd.md`, `erp-stack.md`, `erp-stack.md`, `erp-angular-estrutura.md`

### erp-stack-02 — rank 3

- **Query:** erp usa firestore ou postgres
- **Esperado:** `erp-stack.md` (padrao)
- **Top-5:** `erp-aws-rds.md`, `erp-postgres-schema.md`, `erp-stack.md`, `erp-aws-rds.md`, `erp-multitenancy-spring.md`

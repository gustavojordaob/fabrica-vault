---
tags:
  - mcp
  - cursor
  - fabrica
  - appstore-connect
  - revenuecat
  - mercadopago
  - integracao
atualizado_em: 2026-06-22
---

> **Agente Cursor — MCP PRIMEIRO (obrigatório)**
>
> Antes de codar, deploy ou responder sobre integração externa:
>
> 1. MCP do **tema** (tabela abaixo) — consultar estado real (apps, planos, assinaturas)
> 2. MCP **fabrica-apps** — `rag_buscar` + `buscar_historico`
> 3. Ler nota `.md` linkada
> 4. Só então editar código ou Firestore
>
> **Nunca** assumir preço, status de assinatura ou lista de apps só pela memória do modelo.

# MCPs no Cursor — padrão fábrica (jun/2026)

Configuração global: `C:/Users/gusta/.cursor/mcp.json`  
Repo do MCP Apple: `C:/Users/gusta/projetos/mcp-apple-store`

---

## Regra de ouro: MCP antes de código

| Situação | MCP(s) |
|----------|--------|
| Assinatura MP, preapproval, cancelamento | **mercadopago** + **fabrica-apps** |
| Assinatura iOS, offerings, produtos StoreKit | **revenuecat** + **appstore-connect** |
| Listar apps, IAP, submissão App Store | **appstore-connect** |
| Deploy Firebase, rules, functions | **firebase** (plugin) + **fabrica-apps** |
| WhatsApp Meta | **whatsapp** + **fabrica-apps** |
| RAG, PR, erros, decisões | **fabrica-apps** |

Hooks em `~/.cursor/hooks/` **bloqueiam Write** até `rag_buscar` + `buscar_historico` (fabrica-apps).

---

## Servidores configurados

### 1. `fabrica-apps` (sempre)

| | |
|---|---|
| **Binário** | `C:/Users/gusta/fabrica-apps-mcp/server-v2.js` |
| **Uso** | RAG Obsidian, GitHub, PR, `salvar_decisao`, `registrar_erro_solucao`, features |

**Queries típicas:** `rag_buscar("tema")`, `buscar_historico("tema")`, `buscar_solucao("erro")`

---

### 2. `mercadopago`

| | |
|---|---|
| **Tipo** | Remote MCP (`mcp.mercadopago.com`) |
| **Auth** | `AUTH_HEADER` Bearer no `mcp.json` (**não commitar**) |
| **Doc** | [[mercadopago-integration]] · [[mercadopago-assinatura-ota-padroes]] |

**Quando usar:** criar/validar preapproval, entender status MP, dúvidas de API antes de alterar `functions/SRC/mercadoPagoAssinatura.ts`.

---

### 3. `revenuecat` (novo — jun/2026)

| | |
|---|---|
| **URL** | `https://mcp.revenuecat.ai/mcp` |
| **Auth** | Bearer secret API v2 no `mcp.json` |
| **Doc** | [[cortejo-modulos-jun2026-padrao]] § RevenueCat |

**Ferramentas úteis (consultar schema em `mcps/user-revenuecat/tools/`):**

| Tool | Uso |
|------|-----|
| `list-projects` | projetos RC |
| `list-apps` | apps vinculados (iOS/Android) |
| `list-offerings` | offerings e packages |
| `list-products` | product IDs (`plano1`, `planomensal2`, …) |
| `list-entitlements` | entitlement `pro` |
| `list-subscriptions` | assinantes (suporte) |
| `list-purchases` | compras recentes |

**Quando usar:** validar product IDs, offerings default, entitlement antes de mudar `IosAssinaturaView` ou webhook.

---

### 4. `appstore-connect` (novo — jun/2026)

| | |
|---|---|
| **Binário** | `C:/Users/gusta/projetos/mcp-apple-store/dist/index.js` |
| **Env** | `APP_STORE_ISSUER_ID`, `APP_STORE_KEY_ID`, `APP_STORE_PRIVATE_KEY_PATH` |
| **Chave** | `AuthKey_<KEY_ID>.p8` em `C:/Users/gusta/projetos/` (**API Key**, não Subscription Key) |
| **Repo** | `mcp-apple-store` — README `README.pt-BR.md` |

**Apps na conta (jun/2026):**

| App | Bundle ID | Apple ID |
|-----|-----------|----------|
| Cortejo | `com.fabricaapps.cortejo` | `6781006697` |
| LashMatch | `com.lashmatch` | `6782080036` |

**Ferramentas úteis:**

| Tool | Uso |
|------|-----|
| `connect_list_apps` | listar todos os apps |
| `connect_list_subscription_groups` | grupos de assinatura |
| `connect_list_iap` | IAPs / assinaturas |
| `connect_list_builds` | builds TestFlight |
| `connect_list_versions` | versões App Store |
| `connect_submit_for_review` | submeter review |
| `connect_list_reviews` | reviews clientes |

**Erros comuns:**

| Erro | Causa |
|------|--------|
| `Private key not found` | `.p8` no caminho errado ou nome errado |
| `Authentication credentials invalid` | Usou `SubscriptionKey_*.p8` em vez de `AuthKey_*.p8` |
| Key ID / Issuer ID divergentes | Regenerou chave e não atualizou `mcp.json` |

**Após trocar `.p8`:** reiniciar Cursor ou recarregar MCP.

---

### 5. `whatsapp`

| | |
|---|---|
| **Pacote** | `whatsapp-business-mcp-server` |
| **Doc** | [[whatsapp-business-api]] |

Tokens Meta em env (não commitar). Usar para templates, status número — não para lógica in-app.

---

### 6. `firebase` (plugin Cursor)

| | |
|---|---|
| **Uso** | deploy, rules, functions, Firestore read |
| **Regra** | `firebase_update_environment({ project_dir, active_project })` **antes** de qualquer operação |
| **Project ID** | Ler `.firebaserc` do repo aberto — **nunca** hardcodar |

---

## Checklist — adicionar MCP novo

1. Instalar / build do servidor (ex.: `npm run build` em `mcp-apple-store`)
2. Gerar credenciais no painel do provedor (Apple API Key, RC secret, etc.)
3. Entrada em `~/.cursor/mcp.json` — **só nomes de env**, secrets fora do Git
4. Criar/atualizar nota em `fabrica/*.md` (este arquivo + nota de domínio)
5. Entrada em [[INDEX]] → seção MCPs
6. `python C:/Users/gusta/obsidian/indexar_rapido.py`
7. `salvar_decisao` no fabrica-apps

---

## Pagamentos — qual MCP + qual doc

| Plataforma | MCP consulta | Doc código |
|------------|--------------|------------|
| Android MP | mercadopago | [[mercadopago-assinatura-ota-padroes]] |
| iOS IAP | revenuecat + appstore-connect | [[cortejo-modulos-jun2026-padrao]] |
| Preços na UI iOS | fabrica-apps (catálogo R$) | `constants/planos.ts` — **não** `localizedPrice` na listagem |
| Web Cortejo | — (sem checkout) | `WebPlanoView`, `showPlanCheckoutModule()` |

---

*Última atualização: 22/jun/2026*

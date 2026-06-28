---
tags:
  - whatsapp
  - meta
  - expo
  - salao
  - cloud-functions
  - multi-tenant
  - embedded-signup
  - coexistence
  - cortejo
fonte: implementação Cortejo (jun/2026)
referencia_repo: cortejo
firebase_project: cortejo-app
atualizado_em: 2026-06-23
links:
  - "[[whatsapp-business-api]]"
  - "[[cortejo-schemas]]"
  - "[[cloud-functions-patterns]]"
  - "[[firebase-setup-patterns]]"
  - "[[../projetos/cortejo-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **whatsapp** — Graph API, templates, credenciais Business
> 2. MCP **fabrica-apps** — `rag_buscar("whatsapp salao embedded signup coexistence")`
> 3. MCP **fabrica-apps** — `buscar_historico("whatsapp cortejo meta")`
> 4. Ler **[[whatsapp-business-api]]** (envio básico LashMatch) + **esta nota** (multi-tenant + Embedded Signup)
>
> **Referência de código:** repo `cortejo` — `functions/SRC/whatsapp*.ts`, `embeddedSignup.ts`, `services/embeddedSignup.ts`, `public/embedded-signup/`

---

# WhatsApp salão — padrão Expo multi-tenant (Cortejo)

Padrão reutilizável para apps de **salão/beleza** com:

| Canal | Remetente | Quando |
|-------|-----------|--------|
| **Compartilhado (padrão)** | Número da **plataforma** (`WHATSAPP_PHONE_ID`) | Todo salão; freemium e Pro sem conectar número próprio |
| **Próprio (opcional, Pro)** | Número do **tenant** via Embedded Signup Meta (Coexistence) | Dona conecta WhatsApp Business existente no celular |

> **Não confundir** com [[modulo-ajuda-suporte-expo]] — aquele módulo abre WhatsApp para **suporte ao app**, não para clientes do salão.

---

## Quando usar

| Cenário | Use este padrão |
|---------|-----------------|
| Confirmação + lembretes automáticos para clientes | ✅ |
| Tech Provider / multi-tenant com número compartilhado | ✅ |
| Plano Pro com “Conectar meu WhatsApp” (Coexistence) | ✅ |
| App single-tenant sem onboarding (só um número) | ⚠️ Use [[whatsapp-business-api]] (LashMatch) — mais simples |
| BSP (Gupshup, etc.) como caminho principal | ❌ Legado no Cortejo; preferir Meta direto |

---

## 1. Dois fluxos — não misturar credenciais

### Fluxo A — Envio compartilhado (já funciona sem Embedded Signup)

```
Agendamento criado / scheduler lembrete
  → Cloud Function (whatsapp.ts)
  → Graph API POST /{PHONE_ID}/messages
  → Token: secret WHATSAPP_TOKEN
  → Número: WHATSAPP_PHONE_ID (plataforma)
```

**Não depende de:** `META_APP_ID`, `META_CONFIG_ID`, Embedded Signup.

### Fluxo B — Onboarding número próprio (Embedded Signup, opcional)

```
App Pro + owner → Conectar meu WhatsApp
  → startEmbeddedSignup (status pending)
  → Web: /embedded-signup/ (FB JS SDK + config_id)
  → Meta Coexistence (número já no WhatsApp Business no celular)
  → Deep link cortejo://config/whatsapp?code&wabaId&phoneNumberId
  → completeEmbeddedSignup (status live, grava wabaId/phoneNumberId)
```

**Depende de:** `META_APP_ID`, `META_CONFIG_ID`, `META_APP_SECRET`, domínio OAuth na Meta.

> **Estado jun/2026:** onboarding grava `live` + IDs no Firestore; **envio automático ainda usa número da plataforma** (`resolveSenderPhoneId` retorna sempre `WHATSAPP_PHONE_ID`). Próximo passo: token/número do tenant quando `status==='live' && effectiveSender==='own'`.

---

## 2. Data model — `salons/{tenantId}.whatsapp`

Path Firestore: `artifacts/{appNamespace}/salons/{salonId}` (Cortejo: `cortejo`).

| Campo | Tipo | Uso |
|-------|------|-----|
| `mode` | `'own' \| 'shared'` | Intenção de conexão |
| `effectiveSender` | `'own' \| 'shared'` | Quem **envia** de fato (downgrade força `shared`) |
| `provider` | `'meta' \| 'gupshup' \| 'shared'` | Origem da integração |
| `status` | ver abaixo | Estado da conexão |
| `statusReason` | string? | Mensagem de erro / inelegível |
| `wabaId` | string? | WhatsApp Business Account ID |
| `phoneNumberId` | string? | Graph API Phone Number ID |
| `displayPhone` | string? | Número formatado para UI |
| `appId` | string? | Meta App ID usado no signup |
| `coexistence` | boolean? | Coexistence (app + API) |
| `onboardedAt` | Timestamp? | Go-live Embedded Signup |
| `liveAt` | Timestamp? | Última promoção para live |
| `disconnectedAt` | Timestamp? | Downgrade automático |
| `disconnectFailureCount` | number? | Debounce falhas de envio |

**Status:**

| Valor | UI / comportamento |
|-------|-------------------|
| `not_connected` | Padrão; envio compartilhado |
| `pending` | Fluxo Meta aberto; ainda envia compartilhado |
| `live` | Conectado; UI mostra número próprio |
| `error` | Falha técnica; reconectar |
| `ineligible` | Número não elegível Coexistence |
| `disconnected` | Meta caiu; downgrade para compartilhado |

**Rota auxiliar:** `artifacts/{ns}/whatsappPhoneRoutes/{phoneNumberId}` → `tenantId` (webhook multi-tenant).

Tipos: `types/whatsapp.ts` no repo Cortejo.

---

## 3. Arquivos do projeto (copiar/adaptar)

| Camada | Arquivo | Função |
|--------|---------|--------|
| Envio templates | `functions/SRC/whatsapp.ts` | E.164, templates 10 vars, `resolveSenderPhoneId`, `templateTextParam` |
| Triggers | `functions/SRC/index.ts` | `enviarConfirmacaoAgendamento`, `enviarLembretesAgendamento` |
| Embedded Signup | `functions/SRC/embeddedSignup.ts` | `startEmbeddedSignup`, `embeddedSignupPageConfig`, `completeEmbeddedSignup` |
| Status / downgrade | `functions/SRC/whatsappStatus.ts` | `downgradeWhatsAppConnection`, `promoteWhatsAppLive` |
| Webhook Meta | `functions/SRC/metaWhatsappWebhook.ts` | `webhookWhatsApp`, `account_update`, assinatura HMAC |
| Health check | `functions/SRC/whatsappHealthCheck.ts` | Scheduler 6h, tenants `own+live` |
| Web legado BSP | `functions/SRC/whatsappStatusWebhook.ts` | Gupshup (opcional) |
| Web pública | `public/embedded-signup/index.html` | FB SDK + `WA_EMBEDDED_SIGNUP` postMessage |
| App service | `services/embeddedSignup.ts` | `runEmbeddedSignupFlow`, deep link fixo |
| UI | `app/config/whatsapp.tsx`, `components/whatsapp/WhatsAppStatusCard.tsx` | Conectar / status |
| Guia pré-vínculo | `components/whatsapp/WhatsAppConnectGuide.tsx` | Instruções Coexistence antes do botão Meta |
| Feature flag | `services/platformConfig.ts`, `hooks/useWhatsappSalonFeature.ts` | Gate global `whatsappSalonEnabled` |
| Config URLs | `utils/config.ts` | URLs Cloud Functions + rewrite hosting |

**Path functions:** sempre `functions/SRC/` (maiúsculo) — build → `functions/lib/`.

---

## 4. Credenciais e variáveis

### Envio compartilhado (`functions/.env` + secrets)

```env
WHATSAPP_PHONE_ID=1115148658355291
WHATSAPP_BUSINESS_ID=4347413218803844
WHATSAPP_API_VERSION=v25.0
WHATSAPP_VERIFY_TOKEN=cortejo-webhook-2026
WHATSAPP_TEMPLATE_CONFIRMACAO=agendamento_confirmado_salao
WHATSAPP_TEMPLATE_LEMBRETE=lembrete_agendamento_salao_v3
WHATSAPP_TEMPLATE_LEMBRETE_7D=lembrete_agendamento_salao_7d
WHATSAPP_TEMPLATE_NOTIFICACAO_DONO=novo_agendamento_dono_v2
```

```bash
firebase functions:secrets:set WHATSAPP_TOKEN
```

| Variável | Onde pegar |
|----------|------------|
| `WHATSAPP_PHONE_ID` | Meta Business Suite → WhatsApp → API Setup → **Phone number ID** (não é WABA ID) |
| `WHATSAPP_TOKEN` | System User token ou token permanente com `whatsapp_business_messaging` |
| Templates | Meta Business Manager → WhatsApp → Message templates → **APPROVED** |

### Embedded Signup (opcional)

```env
META_APP_ID=990183433661795
META_CONFIG_ID=2803070780053459
META_GRAPH_VERSION=v23.0
COEXISTENCE_FEATURE_TYPE=whatsapp_business_app_onboarding
EMBEDDED_SIGNUP_PUBLIC_BASE_URL=https://cortejo-app.web.app
```

```bash
firebase functions:secrets:set META_APP_SECRET
# Opcional health check Graph:
firebase functions:secrets:set META_SYSTEM_USER_TOKEN
```

| Variável | Onde pegar |
|----------|------------|
| `META_APP_ID` | developers.facebook.com → App → **Configurações → Básico → Identificação do app** |
| `META_CONFIG_ID` | **Facebook Login for Business → Configurations** → Create → variation **WhatsApp Embedded Signup** |
| `META_APP_SECRET` | App → Configurações → Básico → **Chave secreta** |

> App Meta do Cortejo pode aparecer como **LashMatch** no painel — mesmo App ID.

---

## 5. Meta Developer Console — OAuth (obrigatório para Embedded Signup)

Caminho: **App → Login do Facebook para Empresas → Configurações** (não é a aba Configurations do signup).

### Toggles (todos **Sim**)

- Login no OAuth do cliente
- Login do OAuth na Web
- Forçar HTTPS
- Usar modo estrito para URIs de redirecionamento
- **Entrar com o SDK do JavaScript** ← crítico; sem isso a página `/embedded-signup/` não funciona
- Login OAuth no navegador incorporado (Embedded Browser OAuth Login)

### Campos

| Campo | Valor Cortejo |
|-------|---------------|
| **Domínios permitidos para o SDK do JavaScript** | `cortejo-app.web.app` (sem `https://`) |
| **URIs de redirecionamento OAuth válidos** | `https://cortejo-app.web.app/embedded-signup/` |

Salvar alterações no final da página.

### Configuration Embedded Signup (META_CONFIG_ID)

1. **Facebook Login for Business → Configurations**
2. **Create configuration** → Login variation: **WhatsApp Embedded Signup**
3. Permissões: `whatsapp_business_management`, `whatsapp_business_messaging`
4. Copiar **Configuration ID** → `META_CONFIG_ID`

---

## 6. Fluxo Embedded Signup (passo a passo — o que a cliente vê)

Pré-requisitos: plano **Pro**, usuária **owner**, WhatsApp Business **≥ 2.24.17**, número **já ativo** no app.

1. **Mais → WhatsApp do salão** (bloqueado se `whatsappSalonEnabled !== true` — ver §14)
2. Tela mostra **WhatsAppConnectGuide** (portfólio do salão, conta WABA existente, site)
3. **Conectar meu WhatsApp** (só `owner` + Pro + status ≠ live/pending)
4. Backend: `startEmbeddedSignup` → Firestore `status: pending`, `effectiveSender: shared`
5. Abre browser: `https://{host}/embedded-signup/?session=…&redirect=cortejo://config/whatsapp`
6. Página carrega `embeddedSignupPageConfig` → inicializa FB SDK
7. **Mobile:** redirect OAuth em **página inteira** (não popup `FB.login`) — ver §16
8. Cliente toca **Continuar com Meta** → login Facebook → escolhe portfólio **do salão** + WABA/número **existente** (Coexistence)
9. Celular pode pedir confirmação no WhatsApp Business
10. Web captura `code`, `waba_id`, `phone_number_id` via `postMessage` + OAuth return
11. **Mobile (fix jun/2026):** página chama `completeEmbeddedSignupWeb` na própria web → redirect `cortejo://config/whatsapp?connected=1`
12. **Fallback app:** deep link com `code` → app chama `completeEmbeddedSignup` (Bearer Firebase)
13. Backend troca code, inscreve webhooks, descobre WABA se ausente, grava `status: live`
14. Alert **Conectado** + card atualizado

**Deep link fixo (não usar `Linking.createURL` no mobile):**

```typescript
export const WHATSAPP_CONNECT_REDIRECT = 'cortejo://config/whatsapp';
```

Backend aceita também `exp+cortejo://` (Expo dev client) e `https://` (web).

---

## 7. Templates Meta (Cortejo — 10 variáveis pt_BR)

| Uso | Nome template |
|-----|---------------|
| Confirmação | `agendamento_confirmado_salao_v4` |
| Lembrete 24h | `lembrete_agendamento_salao_v4` |
| Lembrete 7d | `lembrete_agendamento_salao_7d_v4` |
| Novo agendamento (dono, link público) | `novo_agendamento_dono_v2` (7 vars) |

**Ordem {{1}}–{{9}}:** cliente, salão, endereço, data, hora, serviço, profissional, telefone salão, assinatura.

**{{10}}:** bloco único regras + observações (linha após `{{7}}`). **{{8}}:** `Em caso de dúvidas, entre em contato pelo [telefone da dona].` — só quando `envioViaNumeroCompartilhado` (número Cortejo); com WhatsApp próprio, {{8}} invisível (`parametroContatoDuvidas` em `whatsapp.ts`).

---

## 8. Downgrade automático (número próprio cai → compartilhado)

| Gatilho | Onde |
|---------|------|
| Webhook Meta `account_update`, quality, review | `metaWhatsappWebhook.ts` |
| 3 falhas de envio em 15 min (códigos Meta) | `whatsapp.ts` + `whatsappStatus.ts` |
| Health check Graph API a cada 6h | `whatsappHealthCheck.ts` |

Ação: `downgradeWhatsAppConnection` → `effectiveSender: shared`, `status: disconnected`, notificação push/inbox.

Reconexão: mesmo fluxo Embedded Signup ou botão **Tentar novamente** no `WhatsAppStatusCard`.

---

## 9. Cloud Functions — deploy

```powershell
Set-Location C:\Users\gusta\projetos\cortejo\functions
npm run build
Set-Location ..

# Envio + webhook
firebase deploy --only "functions:enviarConfirmacaoAgendamento,functions:enviarLembretesAgendamento,functions:webhookWhatsApp,functions:metaWhatsappWebhook,functions:whatsappHealthCheck" --project cortejo-app

# Embedded Signup (após META_* no .env)
firebase deploy --only "functions:startEmbeddedSignup,functions:embeddedSignupPageConfig,functions:completeEmbeddedSignup" --project cortejo-app

# Hosting (página embedded-signup)
npm run export:web
firebase deploy --only hosting --project cortejo-app
```

**URLs Cortejo:**

| Recurso | URL |
|---------|-----|
| Web app | https://cortejo-app.web.app |
| Embedded Signup | https://cortejo-app.web.app/embedded-signup/ |
| Webhook WhatsApp | https://us-central1-cortejo-app.cloudfunctions.net/webhookWhatsApp |

---

## 10. Erros conhecidos e fixes

| Erro | Causa | Solução |
|------|-------|---------|
| **URL de retorno inválida** | `Linking.createURL` → `exp://…` | Deep link fixo `cortejo://config/whatsapp`; backend valida schemes |
| Meta **#131008** | Parâmetro template vazio (`{{10}}`) | `parametroBloco10()` → `\u200B` quando vazio |
| Meta **#132018** | `\n\n` no **início** de `{{10}}` | Template v4: `{{10}}` em linha própria após `{{7}}`; uma `\n` entre regras e obs |
| **132001** template não existe | `WHATSAPP_PHONE_ID` errado | Usar Phone Number ID do número que tem os templates |
| Página Meta não abre / OAuth | SDK JS desligado ou domínio faltando | Login com SDK = Sim + domínio + redirect URI |
| Deploy falha `META_SYSTEM_USER_TOKEN` | `defineString` vazio obrigatório | Ler de `process.env` opcional ou secret |
| Mensagens “não chegam” com token OK | Params template, não credencial Embedded Signup | Testar `testarConfirmacaoAgendamento` |
| **Invalid App ID** | `META_APP_ID` truncado (ex.: falta último dígito) | Conferir ID completo em developers.facebook.com → Básico |
| **Permissions errors** (app teste) | App sem produto WhatsApp ou Configuration sem permissões | Adicionar WhatsApp; Configuration Embedded Signup com `whatsapp_business_management` + `whatsapp_business_messaging` |
| **Falha ao acessar essa conta** | App Meta em **Desenvolvimento**; conta FB sem role no app | Funções do app → Admin/Developer/Tester + convite aceito; admin no BM do WABA |
| **"Feche esta aba"** (mobile) | OAuth popup FB.login não devolve controle à página Cortejo | Redirect OAuth página inteira + `completeEmbeddedSignupWeb` na web (§16) |
| Volta para **Pronto para conectar** / pending eterno | Fluxo Meta incompleto (só login FB, sem WABA) ou sessão expirada | Escolher portfólio + WABA **existente**; cancelar pending e recomeçar |
| **`featureType: 'coexistence'`** | Valor incorreto no extras do Embedded Signup | Usar **`whatsapp_business_app_onboarding`** (`COEXISTENCE_FEATURE_TYPE`) |
| Flag `true` no Firestore mas app bloqueia | Build/OTA **antigo** com `alertWhatsAppOwnNumberInDevelopment()` hardcoded | Publicar OTA/build com código novo (§14, §19) |
| Flag `true` mas menu ainda bloqueia | Doc Firestore no **caminho errado** | Path canônico: `artifacts/{ns}/system/platformConfig` — **não** `artifacts/system` |
| Flag não atualiza ao mudar no Console | Hook só lia no `useFocusEffect` | `onSnapshot` em `subscribePlatformConfig` (§14) |
| `startEmbeddedSignup` 503 | `whatsappSalonEnabled !== true` no backend | Ativar flag no Firestore **e** redeploy functions se código antigo |

---

## 11. UI — o que mostrar para a dona

| Item | Regra |
|------|-------|
| **Conectar meu WhatsApp** | Só `owner` + plano Pro + status ≠ live/pending + **`whatsappSalonEnabled`** |
| **WhatsAppConnectGuide** | Antes do botão conectar / reconectar (Meta flow) |
| **Templates WhatsApp (admin Meta)** | Removido do menu Mais (jun/2026) — gerenciar pela plataforma/Meta |
| **WhatsAppStatusCard** | Textos por status; reconectar usa fluxo Meta se `provider !== 'gupshup'` |
| **Cancelar conexão** | Visível em `status === 'pending'` — chama `cancelEmbeddedSignup` |

---

## 12. Checklist — novo projeto salão

### Fase 1 — Envio compartilhado

- [ ] Criar app Meta + WABA + número plataforma verificado
- [ ] Templates APPROVED (confirmação + lembretes)
- [ ] `WHATSAPP_PHONE_ID` + secret `WHATSAPP_TOKEN` no Firebase
- [ ] Cloud Functions envio + webhook verify token
- [ ] Campos salão: `name`, `address`, `phone` para vars do template
- [ ] Agendamento: `clientPhone` desnormalizado
- [ ] Testar HTTP `testarConfirmacaoAgendamento`

### Fase 2 — Embedded Signup (Pro)

- [ ] `META_APP_ID`, `META_CONFIG_ID`, secret `META_APP_SECRET`
- [ ] Configuration Embedded Signup na Meta
- [ ] OAuth: domínio hosting + redirect `/embedded-signup/` + SDK JS = Sim
- [ ] `public/embedded-signup/index.html` + deploy hosting
- [ ] Deep link no `app.json` (Android intent filter + iOS scheme)
- [ ] `startEmbeddedSignup` / `completeEmbeddedSignup` com sessão TTL + owner auth
- [ ] Schema `salon.whatsapp` + `WhatsAppStatusCard`
- [ ] Webhook downgrade + health check
- [ ] **Implementar** `resolveSenderPhoneId` com token tenant quando live

### Fase 2b — Feature flag rollout (recomendado antes de Live)

- [ ] Doc `artifacts/{ns}/system/platformConfig` com `whatsappSalonEnabled: false` (padrão)
- [ ] Regras Firestore: read autenticado, write `false` (só Admin SDK / MCP)
- [ ] App: `useWhatsappSalonFeature` + gate em Mais e `/config/whatsapp`
- [ ] Backend: `isWhatsappSalonFeatureEnabled()` em `startEmbeddedSignup`
- [ ] Publicar **OTA/build** antes de ligar flag — build antigo ignora Firestore
- [ ] Ativar `whatsappSalonEnabled: true` quando pronto

### Fase 3 — operação

- [ ] App Live ou testers na Meta
- [ ] Rotacionar tokens se expostos em chat/log
- [ ] Documentar Phone ID e nomes de templates nesta nota + `.env.example`

---

## 13. Adaptar para outro app

1. Trocar namespace Firestore (`artifacts/{seuApp}/salons/…`)
2. Trocar deep link (`meuapp://config/whatsapp`) + intent filter
3. Trocar `EMBEDDED_SIGNUP_PUBLIC_BASE_URL` e domínios OAuth na Meta
4. Recriar templates Meta (nomes podem diferir) — atualizar `.env`
5. Copiar módulos listados na seção 3; não duplicar lógica de downgrade se já existir
6. Implementar feature flag §14 se quiser rollout gradual sem redeploy

---

## 14. Feature flag global — `platformConfig` (rollout gradual)

Padrão reutilizável para **liberar funcionalidade sensível** (Embedded Signup, beta, etc.) sem redeploy do app.

### Firestore

| Item | Valor |
|------|-------|
| **Path canônico** | `artifacts/{appNamespace}/system/platformConfig` |
| Cortejo | `artifacts/cortejo/system/platformConfig` |
| Campo | `whatsappSalonEnabled` (boolean) |
| Default ausente | `false` (bloqueado) |
| Write client | **Proibido** — só Admin SDK, Console, MCP Firebase |

### ❌ Caminho errado (incidente 23/06/2026)

```
artifacts → system (documento) → whatsappSalonEnabled
```

Isso **não funciona**. O app lê subcoleção **`system`** **dentro** do documento **`cortejo`**:

```
artifacts → cortejo → system → platformConfig
```

### Regras Firestore (Cortejo)

```javascript
match /artifacts/cortejo/system/platformConfig {
  allow read: if request.auth != null;
  allow write: if false;
}
```

Deploy: `firebase deploy --only firestore:rules`

### App (Expo)

| Arquivo | Função |
|---------|--------|
| `types/platformConfig.ts` | Tipo + constante de path |
| `services/platformConfig.ts` | `fetchPlatformConfig`, `subscribePlatformConfig` (onSnapshot), `isWhatsappSalonEnabled` |
| `hooks/useWhatsappSalonFeature.ts` | Estado `{ enabled, loading }` — **listener em tempo real** |
| `app/(tabs)/mais.tsx` | Alerta "Funcionalidade em desenvolvimento" se off |
| `app/config/whatsapp.tsx` | Bloqueia tela + alert se off |

**Leitura estrita:** `whatsappSalonEnabled === true` (string `"true"` no Console **não** libera).

**Criar doc via MCP Firebase:**

```json
{
  "document": {
    "name": "projects/{projectId}/databases/(default)/documents/artifacts/cortejo/system/platformConfig",
    "fields": { "whatsappSalonEnabled": { "booleanValue": true } }
  }
}
```

### Backend (Cloud Functions)

```typescript
async function isWhatsappSalonFeatureEnabled(): Promise<boolean> {
  const snap = await db().doc(`artifacts/${NS}/system/platformConfig`).get();
  return snap.exists && snap.data()?.whatsappSalonEnabled === true;
}
```

Gate em `startEmbeddedSignup` → HTTP **503** `"Funcionalidade em desenvolvimento."` se off.

### ⚠️ Armadilha crítica — OTA / build

| Versão do app | Comportamento ao clicar "Conectar" |
|---------------|-----------------------------------|
| **Antiga** (commit anterior) | `alertWhatsAppOwnNumberInDevelopment()` — **sempre bloqueia**, ignora Firestore |
| **Nova** (com hook + flag) | Respeita `whatsappSalonEnabled` |

**Sintoma:** usuário coloca `true` no Console e continua bloqueado → quase sempre **app desatualizado**.

**Fix:** `eas update` ou build nativo **depois** de merge do código da flag.

### Mensagem padrão

```typescript
export const WHATSAPP_SALON_DEV_MESSAGE = 'Funcionalidade em desenvolvimento';
```

---

## 15. Guia pré-vínculo — `WhatsAppConnectGuide`

Componente **obrigatório** antes do botão Meta — reduz abandono e erros de portfólio errado.

**Arquivo:** `components/whatsapp/WhatsAppConnectGuide.tsx`

**Onde renderizar:**
- `app/config/whatsapp.tsx` — acima de "Conectar meu WhatsApp"
- `WhatsAppStatusCard` — quando reconectar / pending / retry

**Conteúdo (copy canônica):**

1. Entrar com **sua** conta Facebook (conferir foto no canto superior direito)
2. **Portfólio empresarial:** escolher o **do salão** — não portfólio de teste nem conta de outra pessoa
3. **Conta WhatsApp Business:** escolher a **existente** (número já ativo no app) — **não criar número novo**
4. Campo **Site:** Instagram do salão ou `https://{project}.web.app/` ou link de agendamento `/agendar?salon={id}`

A página web `embeddedSignupPageConfig` também expõe `websiteFallbackUrl` e `bookingPageUrl` para a HTML.

**Erro típico sem guia:** usuária escolhe "Criar portfólio" / "Criar conta WABA" / "Novo número" → fluxo **não** é Coexistence → volta `not_connected` ou pending eterno.

---

## 16. Fluxo mobile — OAuth "Feche esta aba" (fix jun/2026)

### Problema

No celular, `FB.login` em popup/incorporado termina com tela Meta **"Feche esta aba"** — só vinculou login Facebook ao app, **sem** concluir Embedded Signup (WABA + número).

### Solução implementada

| Camada | Mudança |
|--------|---------|
| `public/embedded-signup/index.html` | Mobile: **redirect OAuth página inteira** (`window.location` para dialog OAuth Meta) em vez de popup |
| | `sessionStorage` persiste `code` / `wabaId` / `phoneNumberId` entre redirects |
| | Recupera `code` da query string ao voltar para `/embedded-signup/` |
| | Chama **`POST /api/completeEmbeddedSignupWeb`** na própria página (sem Bearer — autentica por `sessionId` TTL) |
| | Redirect app: `cortejo://config/whatsapp?connected=1` |
| `functions/SRC/embeddedSignup.ts` | `completeEmbeddedSignupWeb` — conclusão autenticada por sessão one-time |
| | `executeEmbeddedSignupCompletion` — descobre `wabaId`/`phoneNumberId` via Graph se ausentes |
| `services/embeddedSignup.ts` | Aceita `connected=1` no deep link como sucesso sem chamar `completeEmbeddedSignup` de novo |

### Functions a deployar

```powershell
firebase deploy --only "functions:startEmbeddedSignup,functions:embeddedSignupPageConfig,functions:completeEmbeddedSignup,functions:completeEmbeddedSignupWeb,functions:cancelEmbeddedSignup" --project cortejo-app
npm run export:web
firebase deploy --only hosting --project cortejo-app
```

### Deep link de sucesso

```
cortejo://config/whatsapp?connected=1
```

Fallback com params completos (app completa):

```
cortejo://config/whatsapp?sessionId=…&code=…&wabaId=…&phoneNumberId=…
```

---

## 17. App Meta — teste vs produção (Cortejo)

Credenciais **nunca** misturar: `META_APP_SECRET` deve ser da **mesma** app que `META_APP_ID`.

| Ambiente | `META_APP_ID` | `META_CONFIG_ID` | Notas |
|----------|---------------|------------------|-------|
| **Produção** (atual) | `990183433661795` (LashMatch no painel) | `2803070780053459` | App Live ou testadores cadastrados |
| **Teste** (jun/2026) | `26656571413984672` | `1003953905338591` | App "Lash match 2" — reverter após testes |

**Incidente:** ID teste salvo como `2665657141398467` (faltava **`2`** final) → Meta **Invalid App ID**.

**Trocar credenciais:**

1. `functions/.env` — `META_APP_ID`, `META_CONFIG_ID`
2. `firebase functions:secrets:set META_APP_SECRET` (secret da mesma app)
3. `npm run build` em `functions/` + redeploy embedded signup functions
4. `export:web` + hosting (página lê appId via `embeddedSignupPageConfig`)

---

## 18. Incidentes Embedded Signup — 23/06/2026 (playbook)

### Sintoma → diagnóstico → ação

| O que a usuária vê | Diagnóstico provável | Ação |
|--------------------|----------------------|------|
| Invalid App ID | ID truncado no `.env` | Corrigir dígitos; redeploy functions |
| Permissions errors | App teste sem WhatsApp product / Configuration | Meta Developer: produto WhatsApp + Configuration com permissões |
| Falha ao acessar conta | Facebook não é testador do app Dev | Funções do app → Admin/Testador + convite aceito |
| Feche esta aba | OAuth incompleto mobile | Deploy fix §16; tentar de novo |
| Pronto para conectar / pending | Parou no login ou criou recursos novos | Guia §15 — portfólio/WABA **existentes** |
| Funcionalidade em desenvolvimento (menu) | Flag off ou app antigo | Flag true no path correto + OTA |
| Funcionalidade em desenvolvimento (ao conectar) | Backend 503 ou app antigo hardcoded | Flag + deploy functions + OTA |
| Conectado mas status pending | `completeEmbeddedSignup` falhou silencioso | Logs Cloud Functions; secret Meta errado |

### Meta Console — checklist testador

- [ ] E-mail Facebook em **Funções do app** (Admin ou Testador) — convite aceito
- [ ] Mesma pessoa é **admin** do Business Manager do WABA/número
- [ ] App tem produto **WhatsApp** adicionado
- [ ] Configuration Embedded Signup com `whatsapp_business_management` + `whatsapp_business_messaging`
- [ ] OAuth: domínio hosting + redirect `/embedded-signup/` + **SDK JavaScript = Sim**

### Coexistence — o que a Meta pergunta vs o que escolher

| Tela Meta | Escolher |
|-----------|----------|
| Portfólio empresarial | **Existente** do salão |
| Conta WhatsApp Business | **Existente** (número no celular) |
| Número de telefone | **Não criar novo** |
| Site | Instagram ou URL plataforma / link agendamento |

---

## 19. Sessões Embedded Signup — Firestore auxiliar

| Path | Uso |
|------|-----|
| `artifacts/{ns}/embeddedSignupSessions/{sessionId}` | TTL 30 min; `tenantId`, `ownerUid`, `used` |
| `artifacts/{ns}/whatsappPhoneRoutes/{phoneNumberId}` | Map phone → tenant (webhook) |

**Cancelar pending:** `cancelEmbeddedSignup` — volta `whatsapp.status` para `not_connected`.

---

## 20. Cloud Functions — mapa completo Embedded Signup

| Function | Método | Auth | Descrição |
|----------|--------|------|-----------|
| `startEmbeddedSignup` | POST | Bearer Firebase + owner | Cria sessão; gate feature flag; URL signup |
| `embeddedSignupPageConfig` | GET | sessionId query | appId, configId, featureType, URLs site |
| `completeEmbeddedSignup` | POST | Bearer Firebase + owner | Finaliza com code + wabaId |
| `completeEmbeddedSignupWeb` | POST | sessionId TTL | Finaliza na página web (mobile) |
| `cancelEmbeddedSignup` | POST | Bearer Firebase + owner | Cancela pending |

Hosting rewrite: `/api/completeEmbeddedSignupWeb` → function.

---

## Histórico

- **Até mai/2026:** referência LashMatch single-tenant ([[whatsapp-business-api]])
- **Jun/2026:** Cortejo multi-tenant, templates 10 vars, downgrade Meta direto
- **20/06/2026:** Embedded Signup Coexistence sem BSP; fix OAuth deep link; fix template params #131008/#132018; META_CONFIG_ID configurado; domínio OAuth validado
- **23/06/2026:** Feature flag `platformConfig.whatsappSalonEnabled`; guia `WhatsAppConnectGuide`; fix mobile OAuth "Feche esta aba" + `completeEmbeddedSignupWeb`; app Meta teste vs prod documentado; listener onSnapshot; incidentes permissions/Invalid App ID/caminho Firestore errado documentados

**Espelho repo:** `cortejo/docs/whatsapp-business-api.md`

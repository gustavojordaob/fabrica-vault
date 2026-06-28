---
tags:
  - cortejo
  - assinatura
  - revenuecat
  - mercadopago
  - trial
  - msgUsage
  - whatsapp
  - suporte
  - expo
fonte: repo cortejo (jun/2026)
projeto: Cortejo
firebase_project: cortejo-app
links:
  - "[[mercadopago-assinatura-ota-padroes]]"
  - "[[mcps-cursor-padrao]]"
  - "[[cortejo-schemas]]"
  - "[[modulo-ajuda-suporte-expo]]"
  - "[[whatsapp-salao-expo-padrao]]"
  - "[[agenda-salao-expo-padrao]]"
atualizado_em: 2026-06-20
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. `rag_buscar("cortejo assinatura dual revenuecat mercadopago trial 14 firestore sync")`
> 2. `buscar_historico("assinatura agendamento publico cortejo")`
> 3. MCP **mercadopago** — preapproval, plan IDs (Android)
> 4. MCP **revenuecat** + **appstore-connect** — offerings, produtos, trial TWO_WEEKS (iOS)
> 5. MCP **firebase** — deploy functions + hosting
>
> **Regra no repo:** `cortejo/.cursor/rules/rag-assinatura-padrao.mdc`  
> Ver [[mcps-cursor-padrao]] — **MCP primeiro**, depois código.

# Cortejo — módulos jun/2026 (padrão reutilizável)

Documentação consolidada do que entrou no **Cortejo** após jun/2026: pagamentos dual-plataforma, trial **14 dias** (Android + iOS alinhados), limites de WhatsApp por plano, suporte App Store, auth e flags de tenant.

**Repo:** `C:/Users/gusta/projetos/cortejo` · **Firebase:** `cortejo-app`

---

## 1. Assinatura dual-plataforma (iOS × Android × Web)

| | **iOS** | **Android** | **Web** |
|---|---------|-------------|---------|
| Provedor | **RevenueCat** + StoreKit | **Mercado Pago** preapproval | Nenhum checkout |
| Paywall | `IosAssinaturaView` | `AndroidAssinaturaView` | `WebPlanoView` |
| Preço na UI | R$ catálogo (`androidPriceLabel`) | R$ catálogo | — |
| Checkout | IAP in-app (`usePurchase`) | `cartao.tsx` + `tokenizar.html` | Assinar pelo celular |
| Helper central | `usesRevenueCatIap()` | `canUseInAppCardCheckout()` | `isExpoWeb()` |
| Webhook | `revenuecatWebhook` | `mpWebhook` | — |
| Sync manual | `revenueCatSyncSubscription` | `mpSyncSubscription` | — |
| Cancelamento | Apple (Ajustes → Assinaturas) | `mpCancelarAssinatura` | `canCancelSubscription` |

**Regra App Store 3.1.1:** iOS **não** abre Mercado Pago in-app. Android **não** usa RevenueCat. Web **não** exibe cards MP/IAP.

### ⚠️ Firestore × RevenueCat — incidente jun/2026 (ler antes de codar)

O app iOS usa **RevenueCat no dispositivo** para liberar o paywall. O **agendamento público** (`/agendar`, `availableSlots`) usa **somente Firestore** + `salonHasActiveSubscription` — **não** chama o SDK RevenueCat.

| Sintoma | Causa típica | Correção |
|---------|--------------|----------|
| Pro no iPhone, `/agendar` diz "sem assinatura" | Firestore `plan: free` enquanto RC tem entitlement | Sync via `revenueCatSyncSubscription` |
| Sync CF falha 403 RevenueCat | Secret **V2** chamando API **V1** | Usar `https://api.revenuecat.com/v2/...` em `revenueCatSubscription.ts` |
| Cancelou MP mas ainda tem acesso até fim do mês | `CANCELLED` bloqueava antes de `planExpiresAt` | Checar `planExpiresAt` **antes** de `CANCELLED` |

**Onde sincronizar Firestore (iOS):**

| Gatilho | Arquivo |
|---------|---------|
| Boot / entitlement Pro | `components/RevenueCatBootstrap.tsx` |
| Compartilhar link agendamento | `utils/appLinks.ts` → `shareSalonBookingLink` |
| Compra / restore | `services/usePurchase.ts` |
| Webhook | `functions/SRC/revenuecatWebhook.ts` |
| Manual / API pública | CF `revenueCatSyncSubscription` |

**Validação rápida:** `GET .../api/availableSlots?meta=1&salonId=...` → conferir `subscriptionActive` e doc Firestore `plan` / `planExpiresAt`.

**Pendência conhecida:** `app/(tabs)/mais.tsx` ainda pode usar `Share.share` direto — preferir `shareSalonBookingLink` para sync prévio.

### Tiers (4 planos)

Fonte: `constants/planos.ts` + `functions/SRC/planosConfig.ts`

| Tier (`PlanTier`) | Nome | Preço ref. | Msgs/mês |
|-------------------|------|------------|----------|
| `plano1` | Starter | R$ 79,90 | 600 |
| `planomensal2` | Básico | R$ 99,90 | 1.100 |
| `planomensal3` | Avançado | R$ 129,90 | 1.800 |
| `planomensal4` | Profissional | R$ 199,90 | 3.000 |

Recomendado: `planomensal3`. UI: `components/planos/PlanTierCard.tsx`.  
Nomes curtos na UI: `PLANOS_SHORT_LABEL` (Starter, Básico, Avançado, Profissional) via `salonPlanDisplayName()`.

### Firestore (salão)

| Campo | Uso |
|-------|-----|
| `plan` | `free` \| `pro` |
| `planTier` | `PlanTier` |
| `planMsgLimit` | limite mensagens do tier |
| `planPlatform` | `ios` \| `android` |
| `planExpiresAt` | ISO fim período |
| `planRenewalDay` | dia do mês (1–28) |
| `hadAndroidTrial` | trial MP já usado |
| `hadIosTrial` | intro offer Apple já usado |
| `msgUsage` | ver §3 |
| `subscription` | status MP ou Apple |

---

## 2. Trial 14 dias (Android + iOS alinhados)

### Constante única (obrigatório espelhar)

```typescript
// constants/planos.ts  E  functions/SRC/planosConfig.ts
export const TRIAL_DAYS = 14;
```

| Regra | Detalhe |
|-------|---------|
| Textos UI | `TRIAL_DAYS` via `planoMarketing.ts` — **nunca** hardcodar `14` ou `16` solto |
| Apple máximo | Intro offer `TWO_WEEKS` (14d) — **não** configurar 16d no ASC |
| MP planos `withTrial` | Conferir painel MP: `free_trial.frequency` deve bater com `TRIAL_DAYS` |
| Deploy | Mudou `planosConfig.ts` → `firebase deploy` das functions MP |

### Android / Mercado Pago

- IDs MP: cada tier tem `production` e `withTrial` em `MP_PLAN_IDS`.
- Resolver ID: `getMpPlanId(tier, isEligibleForAndroidTrial(salon))`.
- Elegibilidade: `hadAndroidTrial !== true` **e** `subscription.trialUsed !== true`.
- Ao conceder trial: `hadAndroidTrial: true` + `trialUsed: true` no sync — **persistem após cancelar**.
- Reassinar após cancelar no trial → plano **sem** trial (`production`).

### iOS / Apple

- Intro offer: `TWO_WEEKS` nos 4 produtos (`plano1`, `planomensal2-4`) via RevenueCat MCP / ASC.
- Texto por pacote: `pkg.product.introPrice` → `utils/introPrice.ts`.
- Headline genérico: `planoMarketing.headlineTrialIos` usa `TRIAL_DAYS` (14).
- Elegibilidade app: `isEligibleForIosTrial(salon)` → `hadIosTrial !== true` + pacote com intro offer.
- Elegibilidade real: **Apple** — uma intro offer por grupo / Apple ID; cancelar no trial **não** devolve trial.
- Webhook: `revenueCatSubscription.ts` seta `hadIosTrial` em `INITIAL_PURCHASE` (TRIAL/INTRO) ou `RENEWAL` com `is_trial_conversion`.

### Paridade iOS × Android (elegibilidade)

| | Android | iOS |
|---|---------|-----|
| Flag principal | `hadAndroidTrial` | `hadIosTrial` |
| Flag extra | `subscription.trialUsed` | — (só MP) |
| Quem bloqueia cobrança trial | App + MP API | Apple StoreKit |
| Cancelou e reassinou | Sem trial | Sem trial |

### Marketing copy

`constants/planoMarketing.ts` — `headlineTrial` / `trialDetalhe` (Android); `headlineTrialIos` / `trialDetalheIos` (ambos com `TRIAL_DAYS`).

---

## 3. Limite de mensagens WhatsApp (`msgUsage`)

### Schema (`salons/{id}.msgUsage`)

| Campo | Tipo | Uso |
|-------|------|-----|
| `periodStart` | Timestamp | início ciclo renovação |
| `periodEnd` | Timestamp | fim ciclo |
| `sent` | number | mensagens enviadas no período |
| `limitReached` | boolean | bloqueio envio |
| `limitReachedAt` | Timestamp? | quando atingiu 100% |
| `notifiedAt80` / `notifiedAt100` | Timestamp? | push dona |

**Não usar** campo legado `month`.

### Backend

| Arquivo | Função |
|---------|--------|
| `functions/SRC/msgUsage.ts` | período, lazy reset, downgrade |
| `functions/SRC/whatsappSender.ts` | `resolveSender` → `blocked` se limite |
| `functions/SRC/notifyMsgLimit.ts` | push 80% e 100% |
| `functions/SRC/revenueCatSubscription.ts` | reset período em INITIAL_PURCHASE / RENEWAL / PRODUCT_CHANGE |

### Upgrade / downgrade

- **Upgrade:** novo `planMsgLimit` imediato; `sent` mantido.
- **Downgrade:** se `sent > novo limite` → `limitReached: true` + notificação.
- **Android troca plano:** CF `mpTrocarPlano` — cancela preapproval atual, cria nova **sem trial**, sync Firestore.

### UI

- `components/MsgLimitBanner.tsx`
- `components/whatsapp/WhatsAppStatusCard.tsx` — uso no card
- `components/planos/PlanTierCard.tsx` — uso no plano atual

---

## 4. Mercado Pago — funções e URLs

| CF | Uso |
|----|-----|
| `mpCriarAssinatura` | nova assinatura (trial se elegível) |
| `mpTrocarPlano` | troca tier (sem trial) |
| `mpSyncSubscription` | sync manual pós-pagamento |
| `mpCancelarAssinatura` | cancela todas ativas do e-mail |
| `mpWebhook` | notificações MP |

Hosting rewrite: `/api/mpTrocarPlano` → ver `firebase.json`.

App: `services/mercadoPago.ts` — `criarAssinaturaMp`, `trocarPlanoMp`.

`cartao.tsx`: param `changePlan=1` → `trocarPlanoMp`.

---

## 5. RevenueCat (iOS)

| Arquivo | Uso |
|---------|-----|
| `services/revenueCat.ts` | configure SDK |
| `services/usePurchase.ts` | offerings, purchase, restore |
| `components/RevenueCatBootstrap.tsx` | init no boot |
| `components/subscription/IosAssinaturaView.tsx` | paywall — **preço R$ catálogo**, compra via package RC |
| `utils/revenueCatPackages.ts` | map productId → tier |
| `functions/SRC/revenuecatWebhook.ts` | HTTP webhook |
| `functions/SRC/revenueCatSubscription.ts` | apply eventos → Firestore |

**MCP revenuecat:** `list-offerings`, `list-products`, `list-apps` antes de mudar produtos.  
**MCP appstore-connect:** `connect_list_apps`, `connect_list_subscription_groups`, `connect_list_iap`.

Secrets: `REVENUECAT_WEBHOOK_SECRET`, `REVENUECAT_SECRET_API_KEY` (**V2** — não usar endpoints `/v1/`).

**REST sync:** `fetchRevenueCatSubscriber` → `GET https://api.revenuecat.com/v2/projects/{REVENUECAT_PROJECT_ID}/customers/{appUserId}/subscriptions`  
Erro típico se V1: `403 — incompatible with RevenueCat API V1`.

EAS secret: `REVENUECAT_API_KEY_IOS` → `app.config.ts` espelha para bundle.

Produtos App Store Connect: `plano1`, `planomensal2`, `planomensal3`, `planomensal4` (mesmos IDs do tier).  
Trial ASC: `TWO_WEEKS` — configurar via MCP **revenuecat** (`trial_offer`) antes de release.

---

## 6. Suporte público (App Store / Play Store)

| URL | Arquivo |
|-----|---------|
| **Suporte** | `https://cortejo-app.web.app/suporte` → `public/suporte/index.html` |
| **Privacidade** | `https://cortejo-app.web.app/privacidade` → `public/privacidade/index.html` |

Constantes: `constants/support.ts` (`SUPPORT_PAGE_URL`, `PRIVACY_PAGE_URL`, `SUPPORT_EMAIL`).

App Store Connect → **URL de suporte:** `https://cortejo-app.web.app/suporte`

Deploy: `node scripts/copy-public-to-dist.mjs` + `firebase deploy --only hosting` (não depende de `expo export` para HTML estático em `public/`).

In-app: `app/config/ajuda.tsx` + `utils/supportContact.ts` (WhatsApp).

Ver também: [[modulo-ajuda-suporte-expo]].

---

## 7. Auth — confirmação de senha

| Fluxo | Arquivo |
|-------|---------|
| Cadastro | `app/(auth)/login.tsx` — senha + confirmar (devem ser iguais) |
| Alterar senha | `app/config/conta.tsx` — atual + nova + confirmar; `reauthenticateWithCredential` + `updatePassword` |

Só exibe troca de senha se `providerId === 'password'` (não Google).

---

## 8. WhatsApp número próprio (Embedded Signup)

Fluxo **ativo** na UI: `app/config/whatsapp.tsx` + `WhatsAppStatusCard` → `runEmbeddedSignupFlow` (Meta Coexistence).

Requisitos: plano **Pro**, role **owner**, secrets `META_APP_ID` / `META_CONFIG_ID` / `META_APP_SECRET` nas Functions. Ver [[whatsapp-salao-expo-padrao]].

---

## 9. OTA (EAS Update)

```bash
eas update --branch production --platform all --message "descrição"
```

- `runtimeVersion` em `app.config.ts` deve bater com o build instalado (`1.0.0`).
- Canal do build (`preview` / `production`) deve bater com o branch do OTA.
- Functions/hosting **não** vão no OTA — deploy Firebase separado.

---

## 10. Checklist — copiar para novo app salão

### Assinatura
- [ ] `constants/planos.ts` **e** `functions/SRC/planosConfig.ts` — `TRIAL_DAYS` **iguais**
- [ ] `types/tenant.ts` — elegibilidade trial (`hadAndroidTrial` / `hadIosTrial`)
- [ ] `utils/subscriptionPlatform.ts` — iOS IAP vs Android MP
- [ ] Telas `IosAssinaturaView` / `AndroidAssinaturaView`
- [ ] CFs MP + RevenueCat webhook + **API V2** no sync
- [ ] `RevenueCatBootstrap` + `shareSalonBookingLink` sincronizam Firestore
- [ ] `salonHasActiveSubscription`: `planExpiresAt` antes de `CANCELLED`
- [ ] Testar `/agendar?meta=1` com salão iOS Pro
- [ ] `msgUsage` + `whatsappSender` + notificações limite

### App Store
- [ ] `public/suporte/index.html` + `public/privacidade/index.html`
- [ ] URLs no App Store Connect
- [ ] EULA Apple em paywall iOS (`TERMS_OF_USE_URL`)
- [ ] Excluir conta ([[excluir-conta-app-expo-padrao]])

### Deploy
- [ ] `firebase deploy --only functions:mpCriarAssinatura,functions:mpTrocarPlano,functions:revenuecatWebhook,functions:mpWebhook`
- [ ] `firebase deploy --only hosting`
- [ ] `eas update` após mudanças JS

---

*Última atualização: 20/jun/2026 — Cortejo (trial 14d, sync Firestore iOS, RC API V2)*

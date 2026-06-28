---
tags:
  - mercadopago
  - assinatura
  - preapproval
  - paywall
  - cortejo
  - lashmatch
fonte: cortejo + lashmatch (jun/2026)
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **mercadopago** — API preapproval, cancel, search, webhooks
> 2. MCP **fabrica-apps** — `rag_buscar("mercadopago assinatura preapproval")`
> 3. Ler também: [[modulo-ajuda-suporte-expo]] (não confundir com suporte ao cliente final)

# Mercado Pago — Assinatura com cartão tokenizado (padrão Cortejo / LashMatch)

Casos de uso: plano Pro mensal, trial **14 dias** (Android, alinhado ao `TWO_WEEKS` iOS), paywall no app, cancelamento, OTA via EAS Update.

> **Atualização jun/2026:** iOS usa **RevenueCat IAP** (não mais site `/assinar` como checkout principal). Ver [[cortejo-modulos-jun2026-padrao]].

Referência de código: **Cortejo** (`functions/SRC/mercadoPagoAssinatura.ts`, `app/config/cartao.tsx`, `app/config/plano.tsx`).

---

## iOS vs Android vs Web (Cortejo — jun/2026)

| | **iOS** | **Android** | **Web (Expo)** |
|---|---------|-------------|----------------|
| Checkout | **RevenueCat IAP** (`IosAssinaturaView`) | `cartao.tsx` → `tokenizar.html` | **Sem checkout** — `WebPlanoView` |
| Preço na listagem | **R$ catálogo** (`androidPriceLabel` / `formatPlanoPreco`) | R$ catálogo | N/A (sem cards MP) |
| Preço no pagamento | Apple (StoreKit) — moeda da conta Apple | Mercado Pago BRL | — |
| Componente paywall | `IosAssinaturaView` | `AndroidAssinaturaView` | `WebPlanoView` |
| Helper | `usesRevenueCatIap()` | `canUseInAppCardCheckout()` | `isExpoWeb()`, `showPlanCheckoutModule()` |
| Trial | `introPrice` Apple + `TRIAL_DAYS` (14) em copy | `TRIAL_DAYS = 14` + `MP_PLAN_IDS.withTrial` | Trial segue Firestore |
| Troca plano | Apple (upgrade/downgrade) | `mpTrocarPlano` (sem trial) | Orientar app celular |

**MCP antes de alterar:** iOS → **revenuecat** + **appstore-connect** · Android → **mercadopago** · Ver [[mcps-cursor-padrao]].

**LashMatch legado:** ~~iOS site `public/assinar`~~ — **jun/2026:** iOS usa RevenueCat IAP. Ver [[lashmatch-revenuecat-assinatura]] e [[lashmatch-modulos-assinatura-jun2026]].

### Agendamento público depende do Firestore (não do SDK iOS)

`/agendar` e `availableSlots` usam `salonHasActiveSubscription` no documento do salão. Pro no RevenueCat **sem** sync → link público bloqueado.

Sync iOS: `RevenueCatBootstrap`, `shareSalonBookingLink`, `revenueCatSyncSubscription`, webhook. Ver [[cortejo-modulos-jun2026-padrao]] § Firestore × RevenueCat.

---

## Arquitetura (não usar checkout redirect genérico)

```
Android / web:
App (Expo)                    Firebase Hosting              Cloud Functions
─────────                     ─────────────────             ───────────────
plano.tsx → cartao.tsx   →    public/assinatura/tokenizar.html
       │                      (Mercado Pago SDK, só token)
       │  card_token_id
       └──────────────── POST mpCriarAssinatura ──────────► POST /preapproval (MP API)
                                                              syncSalonFromPreapproval → Firestore

iOS:
IosAssinaturaView → WebBrowser → public/assinar/index.html → tokenizar → mpCriarAssinatura
       (sem retorno automático ao app — sync manual ou listener Firestore)

mpWebhook ◄──────────────────────────────────────────────── notification_url
mpSyncSubscription (manual) ──────────────────────────────── GET preapproval + search by email
mpCancelarAssinatura ───────────────────────────────────── PUT cancelled (todas ativas do e-mail)
```

**Regra de segurança:** `MP_ACCESS_TOKEN` **somente** em secret Firebase (`MP_ACCESS_TOKEN`). App usa `EXPO_PUBLIC_MP_PUBLIC_KEY` na página de tokenização.

---

## Variáveis de ambiente (app)

| Variável | Uso |
|----------|-----|
| `EXPO_PUBLIC_MP_PUBLIC_KEY` | Página `tokenizar.html` |
| `EXPO_PUBLIC_MP_TOKENIZE_URL` | URL da página hospedada (ex.: `https://<projeto>.web.app/assinatura/tokenizar.html`) |
| `EXPO_PUBLIC_MP_CRIAR_ASSINATURA_URL` | Cloud Function `mpCriarAssinatura` |
| `EXPO_PUBLIC_MP_SYNC_SUBSCRIPTION_URL` | Cloud Function `mpSyncSubscription` |
| `EXPO_PUBLIC_MP_CANCELAR_ASSINATURA_URL` | Cloud Function `mpCancelarAssinatura` |

Copiar **todas** `EXPO_PUBLIC_MP_*` para `.env` e `.env.development` (mesma base de Functions em dev híbrido — ver [[mercadopago-integration]]).

---

## Firestore — schema assinatura (Cortejo: `artifacts/{ns}/salons/{salonId}`)

```typescript
subscription: {
  status: string;           // AUTHORIZED | PENDING | CANCELLED (uppercase no sync)
  mpPreapprovalId: string;
  mpPreapprovalPlanId: string;
  period: 'mensal' | 'anual';
  payerEmail: string;       // obrigatório para search/cancel no MP
  trialUsed: boolean;
  trialFimEm: string | null; // ISO
  canceladoEm: string | null;
  cancelMotivo: string | null;
}
plan: 'free' | 'pro';
```

**Sempre** gravar `subscription` como **objeto inteiro** no `update()` — evitar `set(merge)` com dot-notation (`subscription.status`) que pode falhar silenciosamente.

---

## Regras de negócio críticas (backend)

### 1. Acesso Pro (`isMpPreapprovalGrantedAccess`)

Liberar Pro para: `authorized`, `active`, `approved`, **`pending`** (pós-checkout, antes do MP confirmar).

Bloquear: `cancelled`, `paused`, `rejected`.

### 2. Criar assinatura (`mpCriarAssinatura`)

1. **Antes** do POST: `cancelAllActivePreapprovalsForEmail(payerEmail)` — evita duplicatas no painel MP.
2. Trial só se `!subscription.trialUsed` → plano `*_com_trial` vs `*_sem_trial`.
3. Após POST: `fetchPreapprovalFromMp(id)` + `syncSalonFromPreapproval` (não confiar só no body do POST).
4. **Deploy obrigatório** após alterar `functions/SRC/mercadoPagoAssinatura.ts`.

### 3. Cancelar (`mpCancelarAssinatura`)

**Nunca** marcar `CANCELLED` no Firestore só porque o doc local já diz cancelado.

Fluxo correto:

1. `cancelAllActivePreapprovalsForEmail(email)` via API MP (`PUT status: cancelled`).
2. Se falhar todas → HTTP 400, **não** atualizar Firestore.
3. Só então `plan: free` + `subscription.status: CANCELLED`.

Também tentar cancelar `subscription.mpPreapprovalId` salvo se não entrou na busca por e-mail.

### 4. Sincronizar (`mpSyncSubscription`)

1. GET `mpPreapprovalId` do Firestore.
2. Se inativo/cancelado → `searchActivePreapprovalsByEmail(payerEmail)` e pegar o **mais recente** ativo.
3. `syncSalonFromPreapproval` → atualiza `plan` e `subscription`.

### 5. Webhook (`mpWebhook`)

`onDocumentCreated` ou notificação MP → mesmo `syncSalonFromPreapproval`. `findSalonDocsForPreapproval` por id, e-mail ou `external_reference`.

---

## Regras de negócio críticas (app)

### Paywall (`utils/subscription.ts`)

```typescript
// Ativo se: trialFimEm no futuro OU status ACTIVE/AUTHORIZED/APPROVED
// PENDING + plan pro também libera (Android)
// Bloqueado se: CANCELLED | PAUSED | REJECTED
```

Helpers adicionais (jun/2026):

| Função | Uso |
|--------|-----|
| `isSubscriptionPaymentPendingReview(salon)` | Banner "Pagamento em análise" — **só** `PENDING` sem acesso ativo (não usar `AUTHORIZED`) |
| `isSubscriptionCancelled(salon)` | `status` CANCELLED ou `canceladoEm` |
| `canCancelSubscription(salon)` | Exibir botão cancelar |
| `salonPlanDisplayName(salon, { short })` | Starter/Básico/Avançado/Profissional — **nunca** "Pro" na UI |

Usar em: `salonStore.isPro()`, `SubscriptionAccessRedirect`, `plano.tsx`, `cancelamento.tsx`, `mais.tsx`.

### Após pagar (`app/config/cartao.tsx`)

1. POST `mpCriarAssinatura`
2. `syncMpSubscription(salonId)`
3. `loadSalonContextForEmail` / `loadSalonContextForUser`
4. `setSalonContext` no Zustand
5. `router.replace` só se `isSalonSubscriptionActive`

**Não remover** `const salonId = useSalonStore((s) => s.salonId)` se o JSX usar `salonId` — causa `ReferenceError: Property 'salonId' doesn't exist`.

### Paywall com botão recuperação

Em `app/config/plano.tsx`: botão **"Atualizar acesso"** sempre visível → chama `syncMpSubscription` e redireciona para `/(tabs)` se ativo.

### Cancelamento UI (`app/config/cancelamento.tsx`)

- **Não** exigir `mpPreapprovalId` local para habilitar cancelar (backend cancela por e-mail).
- Mensagem `alreadyCancelled` só quando MP não tinha nenhuma ativa.
- Se `isSubscriptionCancelled` → tela "Assinatura já cancelada" (sem botão de novo).
- Nome do plano: `salonPlanDisplayName` — tiers Starter/Básico/Avançado/Profissional.
- Trial cancelado: acesso até `trialFimEm`; botão cancelar **oculto** (`canCancelSubscription`).

### Web — sem módulo de plano (`utils/subscriptionPlatform.ts`)

- `isExpoWeb()` / `showPlanCheckoutModule()` → checkout só Android.
- `WebPlanoView`: mensagem "assine pelo app no celular".
- Sidebar web: sem item Plano; links painel + agendamento em `utils/appLinks.ts`.

### iOS — preço na tela vs checkout

- **Listagem:** `androidPriceLabel(tier)` = R$ de `constants/planos.ts`.
- **Checkout Apple:** preço real StoreKit (pode diferir da moeda da sandbox).
- **Não** usar `localizedPrice(pkg)` da RevenueCat nos cards.

---

## Hosting

- `public/assinatura/tokenizar.html` — copiar para `dist/` no export (`scripts/post-export-web.mjs`).
- `firebase.json` → `hosting.public: dist`, rewrite SPA.
- Deploy: `npx expo export --platform web` → `firebase deploy --only hosting`.

---

## Checklist antes de encerrar feature de assinatura

- [ ] Secrets `MP_ACCESS_TOKEN` no Firebase + redeploy functions
- [ ] `payerEmail` salvo em `subscription` em todo sync
- [ ] Cancelamento chama API MP (não só Firestore)
- [ ] Nova assinatura cancela prévias ativas no MP
- [ ] `mpSyncSubscription` busca por e-mail se id salvo estiver morto
- [ ] Paywall com "Atualizar acesso"
- [ ] `cartao.tsx` recarrega contexto após sucesso
- [ ] `isSalonSubscriptionActive` trata `PENDING`
- [ ] Tokenização: página hospedada, nunca ACCESS_TOKEN no app
- [ ] iOS: `IosAssinaturaView` — preço catálogo R$; compra via RevenueCat
- [ ] Android: `AndroidAssinaturaView` → `cartao.tsx`
- [ ] Web: `WebPlanoView` — sem MP/RevenueCat no navegador
- [ ] Decisão de plataforma em `utils/subscriptionPlatform.ts`
- [ ] Banner "Pagamento em análise" só com `isSubscriptionPaymentPendingReview`
- [ ] Cancelamento: `canCancelSubscription` + nomes de tier na UI
- [ ] `TRIAL_DAYS` igual em app e `functions/SRC/planosConfig.ts`
- [ ] iOS: sync Firestore quando RC Pro (`RevenueCatBootstrap`, link agendamento)
- [ ] Testar `availableSlots?meta=1` após assinar no iOS

---

## Erros conhecidos → ver [[erros-e-solucoes]]

| Sintoma | Doc |
|---------|-----|
| Cancelou no app mas MP ainda ativo | `mpCancelarAssinatura` confiava Firestore |
| Duas assinaturas trial no MP | Sem `cancelAllActivePreapprovalsForEmail` antes de criar |
| Pagou e ficou na paywall | Sync só no id antigo; store não atualizado |
| `Property 'salonId' doesn't exist` | Variável removida do `cartao.tsx` |
| `Property 'View' doesn't exist` | Import faltando em `cancelamento.tsx` |
| "Pagamento em análise" no trial | Banner usava `AUTHORIZED` — corrigido com `isSubscriptionPaymentPendingReview` |
| Preço em USD na lista iOS | Usar `androidPriceLabel`, não `localizedPrice` RevenueCat |
| Botão cancelar após cancelar | Usar `canCancelSubscription` / `isSubscriptionCancelled` |
| UI mostra "Pro" | Usar `salonPlanDisplayName` + `PLANOS_SHORT_LABEL` |
| Pro no iOS, `/agendar` indisponível | Firestore stale; sync RC → Firestore; ver `revenueCatSyncSubscription` |
| Sync RC 403 "incompatible with API V1" | Secret V2 + endpoint V1 — usar API **V2** em `revenueCatSubscription.ts` |
| Trial 16d no Android, 14d no iOS | `TRIAL_DAYS` deve ser **14** em `planos.ts` + `planosConfig.ts`; ASC `TWO_WEEKS` |
| Reassinar após cancelar no trial | `hadAndroidTrial` / `hadIosTrial` não resetam — sem trial de novo |

---

*Última atualização: 20/jun/2026 · Projetos: Cortejo, LashMatch*

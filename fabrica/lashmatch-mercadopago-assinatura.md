---
tags:
  - mercadopago
  - assinatura
  - preapproval
  - lashmatch
  - pagamentos
fonte: LashMatch (jun/2026)
projeto: LashMatch
atualizado_em: 2026-06-09
links:
  - "[[lashmatch-revenuecat-assinatura]]"
  - "[[lashmatch-modulos-assinatura-jun2026]]"
  - "[[mercadopago-assinatura-ota-padroes]]"
  - "[[lashmatch-schemas]]"
  - "[[../projetos/lashmatch-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **mercadopago** — preapproval, cancel, sync, webhooks (Android)
> 2. MCP **fabrica-apps** — `rag_buscar("lashmatch mercadopago assinatura")`
> 3. iOS **não** usa MP — ver [[lashmatch-revenuecat-assinatura]]
>
> **Espelho no repo:** `LashMatch/docs/mercadopago-assinatura.md` (ponteiro)

# Mercado Pago — Assinatura LashMatch (Android / web)

Espelha a arquitetura do Cortejo, com **planos e IDs próprios** do LashMatch. Dados em `usuarios/{uid}` (não `salons`).

## iOS vs Android (LashMatch — jun/2026)

| | **iOS** | **Android** |
|---|---------|-------------|
| Checkout | **RevenueCat IAP** — [[lashmatch-revenuecat-assinatura]] | `pagameto/cartao.tsx` → MP tokenizado |
| Cancelamento | App Store (Ajustes) | `mpCancelarAssinatura` |
| Trial | `introPrice` Apple | **5 dias** MP (`MP_PLAN_IDS.withTrial`) |
| Helper | `usesRevenueCatIap()` | `canUseInAppCardCheckout()` |

## Planos

| Plano | Valor | Recorrência | Trial (Android/MP) |
|-------|-------|-------------|-------------------|
| `mensal` | R$ 59,99 | Mensal | 5 dias |
| `anual` | R$ 599,99 | Anual (12 meses) | 5 dias |

## IDs Mercado Pago (`preapproval_plan`)

- **Código:** `LashMatch/constants/planos.ts` + `functions/SRC/planosConfig.ts` → `MP_PLAN_IDS`
- **Override produção:** Firestore `config/mercadopago_planos`

```json
{
  "mensal": {
    "mp_plan_id_trial": "SEU_ID_COM_TRIAL",
    "mp_plan_id_sem_trial": "SEU_ID_SEM_TRIAL"
  },
  "anual": {
    "mp_plan_id_trial": "...",
    "mp_plan_id_sem_trial": "..."
  }
}
```

Preferir override no Firestore para trocar IDs sem redeploy do app.

## Cloud Functions

| Função | Uso |
|--------|-----|
| `criarAssinatura` / `criarAssinaturaMercadoPago` | Nova assinatura com cartão tokenizado |
| `consultarStatusAssinaturaMercadoPago` | Status + último pagamento |
| `webhookAssinatura` | Webhook MP → sync `usuarios/{uid}` |
| `mpSyncSubscription` | Sync manual (botão “Atualizar status”) |
| `mpTrocarPlano` | Troca de plano (cancela anterior + nova preapproval) |
| `mpCancelarAssinatura` | Cancelamento com `motivo` opcional |
| `criarPlanoMP` | Admin: criar planos no MP → `config/mercadopago_planos` |

Módulos: `functions/SRC/mercadoPagoAssinatura.ts`, `functions/SRC/mpSubscriptionHandlers.ts`.

### Secrets

```bash
firebase functions:secrets:set MERCADOPAGO_ACCESS_TOKEN
# criarPlanoMP: MP_PLANO_SETUP_KEY em functions/.env
```

## App (React Native)

| Arquivo | Função |
|---------|--------|
| `services/mpSubscription.ts` | sync, trocar plano, cancelar |
| `utils/mercadoPagoEndpoints.ts` | URLs CF + hosting rewrites |
| `utils/subscriptionAccess.ts` | acesso premium + trial cadastro |
| `app/(tabs)/pagamento.tsx` | Android: gestão MP; iOS: `IosAssinaturaView` |
| `app/pagameto/cartao.tsx` | Tokenização + `criarAssinaturaMercadoPago` |
| `app/pagameto/cancelamento.tsx` | MP (Android) ou link Apple (iOS) |

### Env app

```bash
EXPO_PUBLIC_MP_SYNC_SUBSCRIPTION_URL=
EXPO_PUBLIC_MP_TROCAR_PLANO_URL=
EXPO_PUBLIC_MP_CANCELAR_URL=
EXPO_PUBLIC_MP_ASSINATURA_URL=
EXPO_PUBLIC_MP_STATUS_URL=
EXPO_PUBLIC_INTERNAL_API=https://us-central1-lashmatch-627fd.cloudfunctions.net
```

## Firebase Hosting (rewrites)

- `/api/mpSyncSubscription` → `mpSyncSubscription`
- `/api/mpTrocarPlano` → `mpTrocarPlano`
- `/api/mpCancelarAssinatura` → `mpCancelarAssinatura`

## Deploy

```powershell
Set-Location LashMatch/functions; npm run build
Set-Location ..
firebase deploy --only "functions:mpSyncSubscription,functions:mpTrocarPlano,functions:mpCancelarAssinatura,functions:webhookAssinatura"
```

## Diferença vs Cortejo

| | LashMatch | Cortejo |
|--|-----------|---------|
| Planos | 2 (`mensal` / `anual`) | 4 tiers |
| Trial MP | 5 dias | 14 dias |
| Firestore | `usuarios/{uid}` | `artifacts/.../salons/{id}` |
| IDs MP | **distintos** — nunca reutilizar | próprios |

Ver [[cortejo-modulos-jun2026-padrao]] para padrão salão multi-tenant.

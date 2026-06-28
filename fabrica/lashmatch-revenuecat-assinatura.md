---
tags:
  - revenuecat
  - assinatura
  - ios
  - iap
  - lashmatch
  - appstore
fonte: LashMatch (jun/2026)
projeto: LashMatch
atualizado_em: 2026-06-09
links:
  - "[[lashmatch-mercadopago-assinatura]]"
  - "[[lashmatch-modulos-assinatura-jun2026]]"
  - "[[cortejo-modulos-jun2026-padrao]]"
  - "[[mcps-cursor-padrao]]"
  - "[[lashmatch-schemas]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **revenuecat** — projeto `projf86ea1df`, app `app6962778a38`
> 2. MCP **appstore-connect** — app `6782080036`, bundle `com.lashmatch`
> 3. MCP **fabrica-apps** — `rag_buscar("lashmatch revenuecat ios")`
>
> **Espelho no repo:** `LashMatch/docs/revenuecat-assinatura.md` (ponteiro)

# RevenueCat + App Store — LashMatch (iOS)

Fluxo espelhado do Cortejo, adaptado para `usuarios/{uid}` e planos **mensal / anual**.

## Conta RevenueCat (jun/2026)

O app **Lash Match** está no **mesmo projeto RevenueCat** do Cortejo (nome do projeto no painel: *Cortejo*). Isso é normal — apps distintos, offerings separados.

| Recurso | ID / valor |
|---------|------------|
| **Project** | `projf86ea1df` |
| **App iOS** | `app6962778a38` — bundle `com.lashmatch` |
| **Entitlement** | `pro` (`entla166033dc2`) — compartilhado com Cortejo |
| **Offering LashMatch** | `lashmatch` (`ofrngac4964393a`) — **não** é o `default` (Cortejo) |
| **Packages** (offering `lashmatch`) | `$rc_monthly` Starter · `$rc_monthly_2` Básico · `$rc_monthly_3` Avançado · `$rc_monthly_4` Profissional |
| **Webhook** | `whintgre52e454fe6` — LashMatch Firebase (`app6962778a38`) |

### Produtos App Store (4 tiers mensais — sem plano anual)

| Tier Firestore | Store ID (App Store Connect) | Preço BR | Trial Apple |
|----------------|------------------------------|----------|-------------|
| `plano1` Starter | `lashmatch_mensal` | R$ 79,90/mês | **ONE_WEEK** (7 dias) |
| `planomensal2` Básico | `lashmatch_mensal2` | R$ 99,99/mês | **ONE_WEEK** |
| `planomensal3` Avançado | `lashmatch_mensal3` | R$ 129,99/mês | **ONE_WEEK** |
| `planomensal4` Profissional | `lashmatch_mensal4` | R$ 199,99/mês | **ONE_WEEK** |

**Estado ASC (grupo `22176006`, jun/2026 — IDs novos):**

| Store ID | ASC ID | Estado ASC |
|----------|--------|------------|
| `lashmatch_mensal` | `6783035503` | READY_TO_SUBMIT |
| `lashmatch_mensal2` | `6783361780` | READY_TO_SUBMIT |
| `lashmatch_mensal3` | `6783362865` | READY_TO_SUBMIT |
| `lashmatch_mensal4` | `6783364698` | READY_TO_SUBMIT |

- Atualizar **RevenueCat** offering `lashmatch`: packages devem apontar para os novos store identifiers acima.
- Paywall fora das tabs: rota `/assinatura` (sem bloqueio do `(tabs)/_layout`).

**RevenueCat products (jun/2026 — API v2 configurado):**

| Store ID | RC product id | Package |
|----------|---------------|---------|
| `lashmatch_mensal` | `prodcdd802eec5` | `$rc_monthly` (`pkge31725622c1`) |
| `lashmatch_mensal2` | `prod83f6e011f5` | `$rc_monthly_2` (`pkgecc35c8de39`) |
| `lashmatch_mensal3` | `prod752195a3ab` | `$rc_monthly_3` (`pkge03764bfe53`) |
| `lashmatch_mensal4` | `prodb762d40c49` | `$rc_monthly_4` (`pkgeb1bcbcd01c`) |

Entitlement `pro` (`entla166033dc2`): apenas os 4 produtos `lashmatch_mensal` … `mensal4` (LashMatch). Produtos legados LashMatch arquivados no RC.

- Grupo ASC: **LashMatch Pro** (`22176006`)
- App ASC: `6782080036`
- Política de privacidade no produto: `https://lashmatch-627fd.web.app/politica-privacidade`

> **Trial:** A Apple **não** oferece exatamente 5 dias. Opções próximas: `THREE_DAYS` ou `ONE_WEEK`. LashMatch usa **7 dias** (`ONE_WEEK`) no iOS e no código (`DIAS_TRIAL_GRATIS = 7`). Alinhar planos **com trial** no Mercado Pago aos mesmos 7 dias quando enviar os novos IDs.

## Arquitetura

```
iOS (StoreKit)     RevenueCat              Firebase
     │                  │                      │
     ├─ compra ────────►│                      │
     │                  ├─ webhook ───────────► usuarios/{uid}
     App logIn(uid) ────┤                      │
     revenueCatSyncSubscription ─────────────► Cloud Function
```

| Plataforma | Checkout | Cancelamento |
|------------|----------|--------------|
| **iOS** | `IosAssinaturaView` + offering `lashmatch` | Ajustes → Apple ID → Assinaturas |
| **Android** | Mercado Pago — [[lashmatch-mercadopago-assinatura]] | `mpCancelarAssinatura` |

**App:** `services/usePurchase.ts` prioriza `offerings.all.lashmatch` antes do `default` (Cortejo).

## Secrets / env

Secrets configurados em `lashmatch-627fd` (jun/2026). Deploy OK: `revenuecatWebhook` + `revenueCatSyncSubscription`.

```bash
# Webhook secret = mesmo valor do header no painel RC (whintgre52e454fe6)
firebase functions:secrets:set REVENUECAT_WEBHOOK_SECRET
firebase functions:secrets:set REVENUECAT_SECRET_API_KEY   # secret key projeto projf86ea1df
```

App (EAS) — public SDK key iOS (projeto `app6962778a38`, production):

```bash
eas secret:create --name REVENUECAT_API_KEY_IOS --value appl_uwzKNjjesAzYZeKHGSgmEasYuLJ
```

> Rotacionar/regenerar no painel RevenueCat se esta nota vazar. Nunca commitar a secret key.

**Não funciona no Expo Go** — exige EAS Build / dev client.

## Webhook

Criar integração **separada** do Cortejo (mesmo projeto RC, URL LashMatch):

- URL: `https://us-central1-lashmatch-627fd.cloudfunctions.net/revenuecatWebhook`
- Authorization: `Bearer <REVENUECAT_WEBHOOK_SECRET>`
- `app_id`: `app6962778a38` (só eventos LashMatch)
- Eventos: `initial_purchase`, `renewal`, `product_change`, `cancellation`, `billing_issue`, `uncancellation`, `expiration`

Webhook LashMatch criado (`whintgre52e454fe6`). **Authorization header RC:** `lashmatch-rc-webhook-secret` — definir o mesmo valor em `REVENUECAT_WEBHOOK_SECRET` no Firebase antes do deploy.

Webhook Cortejo (`whintgrdfc896fd4f`) permanece separado.

## Cloud Functions

| Função | Uso |
|--------|-----|
| `revenueCatSyncSubscription` | POST autenticado — sync após compra/restauração |
| `revenuecatWebhook` | Webhook → `usuarios/{uid}` |

Hosting: `/api/revenuecatWebhook`, `/api/revenueCatSyncSubscription`

**API REST:** V2 (`https://api.revenuecat.com/v2/...`).

## Pendências manuais (ASC)

1. **Equalizar preços** — rodar de novo quando ASC não estiver em rate limit:
   - MCP `equalize-subscription-prices` com `base_territory: BR` para `prodcdd802eec5` e `prod16e62b5b34`
2. Status pode ficar `MISSING_METADATA` até screenshot de review / metadados finais no ASC
3. **Primeira assinatura** do app: enviar com **nova versão** do app no App Store Connect (regra Apple)
4. Mercado Pago: novos `preapproval_plan` com trial **7 dias** — atualizar `MP_PLAN_IDS` / `config/mercadopago_planos`

## Deploy

```powershell
firebase deploy --only "functions:revenueCatSyncSubscription,functions:revenuecatWebhook"
```

## Checklist release iOS

- [x] Grupo + produtos ASC (`lashmatch_mensal`, `lashmatch_anual`)
- [x] Produtos + offering `lashmatch` no RevenueCat
- [x] Entitlement `pro` vinculado
- [x] Trial `ONE_WEEK` nos dois produtos
- [ ] Equalizar preços internacionais (retry após rate limit)
- [ ] Webhook LashMatch no RC + secrets Firebase
- [ ] `REVENUECAT_API_KEY_IOS` no EAS
- [ ] Planos MP com trial 7d (IDs do usuário)
- [ ] EAS build iOS + teste compra sandbox

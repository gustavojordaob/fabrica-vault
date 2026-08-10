---
tags:
  - fabrica
  - setmatch
  - pagamentos
  - stripe
atualizado_em: 2026-07-27
---

# Setmatch — Pagamentos Stripe (Checkout + Connect + Recorrência)

> **Agente Cursor — use MCP antes de codar**
> `rag_buscar("setmatch stripe checkout connect clube subscription")`
> `buscar_historico("setmatch stripe pagamentos recorrente desconto")`

Repo: `setmatch-app` · Firebase: `setmatch-app-fabrica`

## Fluxo

1. Jogador cria `pagamentos/{id}` → `pagarComEscolhaDeMeio` (escolhe PIX/cartão + vê % off) → `iniciarCheckoutStripe`
2. Cloud Function `criarCheckoutStripe`:
   - **ciclo mensal + cartão** → Checkout `mode: subscription` (renovação automática)
   - **PIX** (mesmo mensal) → `mode: payment` (só o mês atual)
   - **único** → `mode: payment` com o meio escolhido
3. Após browser: `confirmarCheckoutStripe` + webhook `webhookStripeSetmatch`
4. Renovações: evento `invoice.paid` estende `vigenteAte` (+1 mês)
5. Admin: **Financeiro → Recebimentos Stripe** → Connect Express

Se o clube tem `stripeChargesEnabled`, usa destination charge / `application_fee` (payment) ou `application_fee_percent` (subscription).

## Promo por meio (admin)

Campos em `rankings.pagamento`, `clubes.aulas`, `torneios.pagamento`:

| Campo | Uso |
|-------|-----|
| `descontoPixPercent` | % off no PIX (0–100) |
| `descontoCartaoPercent` | % off no cartão (0–100) |

UI admin: `ranking-novo`, `aulas-regras`, `torneio-novo`.  
UI jogador: badge `PIX −X%` / `Cartão −Y%` + Alert de escolha (`utils/checkoutComMeio.ts`, `utils/precoPagamento.ts`).

## Functions (southamerica-east1)

| Função | Uso |
|--------|-----|
| `criarCheckoutStripe` | Session Checkout (payment ou subscription) |
| `confirmarCheckoutStripe` | Sync pós-browser |
| `webhookStripeSetmatch` | Eventos Stripe |
| `stripeConnectOnboarding` | Link Express do clube |
| `stripeConnectStatus` | Atualiza flags no `clubes/{id}` |

## Env (`functions/.env` — não commitar)

```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PLATFORM_FEE_PERCENT=0
```

Webhook URL:
`https://southamerica-east1-setmatch-app-fabrica.cloudfunctions.net/webhookStripeSetmatch`

Eventos: `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`, `invoice.paid`, `customer.subscription.deleted`, `account.updated`

## PIX

Ativar em Stripe Dashboard → Payment methods. Se PIX falhar na sessão, backend cai para cartão.

**Limitação BR:** assinatura Stripe recorrente = cartão. PIX não entra em `subscription`.

## App

- `utils/stripeCheckout.ts` · `utils/checkoutComMeio.ts` · `utils/precoPagamento.ts`
- Páginas web: `/pagamento/sucesso`, `/pagamento/cancelado`, `/pagamento/stripe-connect`
- Admin: `app/clube/financeiro.tsx`

## Checklist

- [x] Secret em `functions/.env` + deploy
- [x] Checkout card + subscription mensal
- [x] Promo % por meio (admin + UI jogador)
- [ ] Ativar PIX no Dashboard (conta)
- [ ] Webhook com `invoice.paid` + `STRIPE_WEBHOOK_SECRET`
- [ ] Testar Connect Express com dono de clube

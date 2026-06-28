---
tags:
  - lashmatch
  - assinatura
  - revenuecat
  - mercadopago
  - paywall
fonte: LashMatch (jun/2026)
projeto: LashMatch
atualizado_em: 2026-06-09
links:
  - "[[lashmatch-mercadopago-assinatura]]"
  - "[[lashmatch-revenuecat-assinatura]]"
  - "[[cortejo-modulos-jun2026-padrao]]"
  - "[[mercadopago-assinatura-ota-padroes]]"
  - "[[lashmatch-schemas]]"
---

> **Agente Cursor — consultar ANTES de alterar pagamentos LashMatch**
>
> 1. `rag_buscar("lashmatch assinatura dual revenuecat mercadopago")`
> 2. MCP **revenuecat** + **appstore-connect** (iOS) · MCP **mercadopago** (Android)
> 3. Notas: [[lashmatch-mercadopago-assinatura]] · [[lashmatch-revenuecat-assinatura]]

# LashMatch — Módulo assinatura (jun/2026)

Visão consolidada: **dual provider** como Cortejo, com escopo e dados próprios.

## Resumo executivo

| | iOS | Android | Web (Expo) |
|---|-----|---------|------------|
| Provedor | **RevenueCat** + StoreKit | **Mercado Pago** preapproval | Sem checkout IAP/MP in-app |
| Planos | mensal + anual | mensal + anual | Ver `/planos` |
| Trial | Apple `introPrice` | **5 dias** MP | Trial cadastro Firestore |
| Dados | `usuarios/{uid}` | `usuarios/{uid}` | idem |
| Paywall | `IosAssinaturaView` | `pagameto/cartao.tsx` | `app/planos.tsx` |
| Gate de acesso | `usePlano` + RC entitlement | `usePlano` + MP status | `usePlano` |
| **Análises faciais** | App completo | App completo | **Bloqueado** (`canUseClientAnalysis`) |

**Regra App Store 3.1.1:** iOS **não** abre Mercado Pago in-app.

**Regra web (jun/2026):** análises (IA + manual) **somente** iOS/Android — ver [[lashmatch-web-plataforma]].

## Fluxo do usuário

1. Cadastro → trial de cadastro (dias em `planoMarketing` / Firestore)
2. Trial expira → `PlanoAccessRedirect` → `/planos`
3. Assinar:
   - iOS → `/(tabs)/pagamento` → `IosAssinaturaView`
   - Android → `/(tabs)/pagamento` → `pagameto/cartao`
4. Cancelar:
   - iOS → Apple Subscriptions (link em `cancelamento.tsx`)
   - Android → `mpCancelarAssinatura` + motivo

## Arquivos raiz (mapa)

```
app/
  _layout.tsx              RevenueCatBootstrap + PlanoAccessRedirect
  planos.tsx               paywall / status sem assinatura
  (tabs)/pagamento.tsx     iOS vs Android
  pagameto/cartao.tsx      Android MP
  pagameto/cancelamento.tsx
hooks/usePlano.ts          acesso efetivo
functions/SRC/
  mercadoPagoAssinatura.ts
  mpSubscriptionHandlers.ts
  revenueCatSubscription.ts
  revenuecatWebhook.ts
```

## Valores comerciais (referência)

- Mensal: **R$ 59,99/mês**
- Anual: **R$ 599,99/ano**
- Trial MP: **5 dias** (não confundir com Cortejo 14 dias)

## Sincronização documentação

| Ação | Onde |
|------|------|
| Fonte RAG | `obsidian/fabrica/lashmatch-*.md` (este arquivo + MP + RC) |
| Ponteiro repo | `LashMatch/docs/mercadopago-assinatura.md`, `revenuecat-assinatura.md` |
| Schema | [[lashmatch-schemas]] |
| Reindexar | `python C:/Users/gusta/obsidian/indexar_rapido.py --somente lashmatch-modulos-assinatura-jun2026.md lashmatch-mercadopago-assinatura.md lashmatch-revenuecat-assinatura.md lashmatch-schemas.md` |

## Checklist deploy assinatura

- [ ] Secrets MP + RevenueCat no Firebase
- [ ] `REVENUECAT_PROJECT_ID` em functions `.env`
- [ ] Produtos ASC + RevenueCat offering `default`
- [ ] IDs MP em `config/mercadopago_planos` ou `MP_PLAN_IDS`
- [ ] `firebase deploy` functions MP + RC
- [ ] EAS build iOS (não Expo Go)
- [ ] Reindexar Obsidian após editar docs

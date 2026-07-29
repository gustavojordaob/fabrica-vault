---
projeto: Cortejo
tipo: referencia-tecnica
stack: React Native (Expo) + Firebase
package: com.fabricaapps.cortejo
firebase: cortejo-app
repo: C:/Users/gusta/projetos/cortejo
atualizado_em: 2026-07-23
links:
  - "[[cortejo-prd]]"
  - "[[../fabrica/cortejo-schemas]]"
  - "[[../fabrica/cortejo-modulos-jun2026-padrao]]"
  - "[[../fabrica/agenda-salao-expo-padrao]]"
  - "[[../fabrica/whatsapp-salao-expo-padrao]]"
  - "[[../fabrica/arquitetura-fabrica-ia]]"
---

# Cortejo — PROJECT (referência técnica)

> **Fonte de verdade:** esta nota + PRD **[[cortejo-prd]]** + módulos **[[../fabrica/cortejo-modulos-jun2026-padrao]]**.  
> Padrões cross-projeto: `obsidian/fabrica/`.  
> O arquivo `PROJECT.md` / `CLAUDE.md` no repo Git é só **atalho** — KB = Obsidian.

---

## Visão rápida

App de gestão para salões: agenda, estoque, PDV, financeiro, WhatsApp, assinatura.

| Item | Valor |
|------|-------|
| Stack | Expo (SDK 54) · expo-router · Firebase JS SDK 12 · `theme/tokens.ts` |
| Firebase | `cortejo-app` |
| Multi-tenant | `artifacts/cortejo/salons/{salonId}/…` |
| Assinatura | **Dual:** RevenueCat iOS + Mercado Pago Android · trial **14 dias** · sync Firestore |
| WhatsApp | Número plataforma + próprio (Embedded Signup) · config Meta **só no web/PC** |
| Deploy | Cloud Functions · Hosting · EAS Update (OTA) · RC public key `appl_` no cliente |

---

## Design tokens

| Token | Hex |
|-------|-----|
| primary | `#6B4226` |
| bg | `#FAF6F1` |
| surface | `#FFFFFF` |

---

## Telas principais

| Rota | Função |
|------|--------|
| `/(tabs)/index` | Agenda |
| `/agendamento/[id]` | Detalhe / edição agendamento |
| `/config/horarios` | Horário por profissional |
| `/config/bloqueios` | Bloqueios agenda |
| `/config/clientes` | CRUD clientes |
| `/config/whatsapp` | Status + connect (web) + cartão Meta |
| `/config/plano` · `/config/cartao` | Assinatura / paywall |
| `/agendar` | Link público (web Hosting) |

---

## Documentação (Obsidian)

| Nota | Conteúdo |
|------|----------|
| **[[cortejo-prd]]** | Produto, design system, escopo |
| **[[../fabrica/cortejo-schemas]]** | Firestore Cortejo |
| **[[../fabrica/cortejo-modulos-jun2026-padrao]]** | Assinatura dual, trial, msgUsage, OTA |
| **[[../fabrica/agenda-salao-expo-padrao]]** | Agenda, slots, bloqueios |
| **[[../fabrica/whatsapp-salao-expo-padrao]]** | WhatsApp multi-tenant + Meta PC-only |
| **[[../fabrica/whatsapp-business-api]]** | Envio Meta / templates |
| **[[../fabrica/mercadopago-assinatura-ota-padroes]]** | Assinatura MP |
| **[[../fabrica/decisoes]]** · **[[../fabrica/erros-e-solucoes]]** | Memória |

---

## RAG

Queries úteis: `cortejo assinatura dual`, `whatsapp salao embedded signup`, `agenda calendario cortejo`.  
Antes de codar: `rag_buscar` + `buscar_historico`.

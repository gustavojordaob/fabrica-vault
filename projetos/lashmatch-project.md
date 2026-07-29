---
projeto: LashMatch
tipo: referencia-tecnica
stack: React Native (Expo) + Firebase
package: com.lashmatch
firebase: lashmatch-627fd
repo: C:/Users/gusta/LashMatch
atualizado_em: 2026-07-23
links:
  - "[[lashmatch-prd]]"
  - "[[../fabrica/lashmatch-schemas]]"
  - "[[../fabrica/lashmatch-modulos-assinatura-jun2026]]"
  - "[[../fabrica/lashmatch-web-plataforma]]"
  - "[[../fabrica/whatsapp-salao-expo-padrao]]"
  - "[[../fabrica/arquitetura-fabrica-ia]]"
---

# LashMatch — PROJECT (referência técnica)

> **Fonte de verdade:** esta nota + PRD **[[lashmatch-prd]]** + **[[../fabrica/lashmatch-modulos-assinatura-jun2026]]**.  
> Padrões cross-projeto: `obsidian/fabrica/`.  
> `CLAUDE.md` no repo = ponte — KB = Obsidian.

---

## Visão rápida

App de gestão para studios de cílios: agenda, clientes, estoque, financeiro, análise/visagismo (nativo), WhatsApp, assinatura.

| Item | Valor |
|------|-------|
| Stack | Expo · expo-router · Firebase JS · UI escura (`#D63384`) |
| Firebase | `lashmatch-627fd` (alias `prod`) |
| Tenant | `usuarios/{uid}` (single-owner por conta) |
| Assinatura | **Dual:** RevenueCat iOS + Mercado Pago Android |
| WhatsApp | Meta Business API · próprio via Embedded Signup · config Meta **só no web/PC** |
| Web | Hosting: **sem** análise facial / **sem** checkout IAP in-app — [[../fabrica/lashmatch-web-plataforma]] |
| Deploy | Functions · Hosting · EAS Update · RC public key `appl_` no cliente |

---

## Telas principais

| Rota | Função |
|------|--------|
| `/(tabs)/agendamentos` | Agenda |
| `/(tabs)/pagamento` | Paywall (iOS RC / Android MP) |
| `/config/whatsapp` | WhatsApp studio (connect web + cartão Meta) |
| `/agendar` | Link público |
| Assistente / análise | **Só nativo** (bloqueado na web) |

---

## Documentação (Obsidian)

| Nota | Conteúdo |
|------|----------|
| **[[lashmatch-prd]]** | Produto completo |
| **[[../fabrica/lashmatch-schemas]]** | Firestore |
| **[[../fabrica/lashmatch-modulos-assinatura-jun2026]]** | Dual RC+MP |
| **[[../fabrica/lashmatch-revenuecat-assinatura]]** | iOS RC |
| **[[../fabrica/lashmatch-mercadopago-assinatura]]** | Android MP |
| **[[../fabrica/whatsapp-business-api]]** | Envio Meta |
| **[[../fabrica/whatsapp-salao-expo-padrao]]** | Embedded Signup + PC-only (compartilhado com Cortejo) |

---

## RAG

Queries úteis: `lashmatch assinatura dual`, `lashmatch web plataforma`, `whatsapp meta computador`.  
Antes de codar: `rag_buscar` + `buscar_historico`. MCP WhatsApp: **whatsapp_lash_match**.

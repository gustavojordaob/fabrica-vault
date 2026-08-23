---
projeto: LashMatch
tipo: referencia-tecnica
stack: React Native (Expo) + Firebase
package: com.lashmatch
firebase: lashmatch-627fd
repo: C:/Users/gusta/LashMatch
atualizado_em: 2026-08-19
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

---

## Atualização recente (2026-08-19)

- Ajustado `PlanoAccessRedirect` para **não expulsar assinante** ao abrir `/plano-escolha`.
- Corrige o fluxo em `Pagamentos` quando a usuária toca em **"Escolher outro tipo de WhatsApp"** e **"Mudar tipo de lembrete (WhatsApp)"**.
- Resultado esperado: abrir a tela de escolha de estilo de WhatsApp/plano, sem voltar para início.
- Bump de versão para **1.0.7** (commitando build novo para store) e regeneração de ícones para release.
- Correção do build iOS: removidos `}` extras em `app/index.tsx` que causavam `SyntaxError ... Unexpected token (68:0)`.
- Bug (web/PWA): ao clicar “Escolher outro tipo de WhatsApp” em `app/assinatura.tsx`, agora alterna o `estilo` direto na rota `/assinatura` (sem usar `/plano-escolha` no web) para evitar o “volta pro início”.
- Bug (web/PWA): no primeiro load, o app estava caindo em `/plano-escolha` (“WhatsApp nos lembretes”) mesmo com acesso. Ajustado `PlanoAccessRedirect` para, no web, mandar de volta para `/(tabs)` (Home) quando `temAcessoEfetivo` estiver true.
- Bug (Expo Go / nativo): trial ativo vinha do Firestore como Timestamp/Date e `usePlano` só aceitava string. Normalizei `trialFimEm` em `hooks/usePlano.ts` pra detectar o trial corretamente e evitar telas brancas/redirect incorreto ao clicar “Meu plano”.
- Boot app (nativo + web): `app/index.tsx` não redireciona mais para `/plano-escolha`; com usuário logado, entra direto em `/(tabs)` (Home). `app/(tabs)/_layout.tsx` também deixou de forçar redirect para paywall no carregamento inicial.
- Bug (Expo Go / nativo): navegação via `openAppRoute` para `/planos` agora força `stay=1` (visualização explícita) pra evitar tela branca ao clicar “Meu plano”.
- Bug (Expo Go / nativo): ajuste no `app/(tabs)/index.tsx` — o botão de trial (“Ver planos — …”) agora navega para `/planos` com `params: { stay: '1' }` (antes era `router.push("/planos")` sem stay).
- Bug (Expo Go / nativo): `MoreMenu` (“Ver mais > Meu plano”) agora abre `href` explicitamente como `/planos?stay=1` (antes era `/planos` puro), evitando tela branca no Expo Go.
- Debug (Expo Go / nativo): adicionei logs `[PLANO_DEBUG]` em `components/MoreMenu.tsx` (ao selecionar “Meu plano”) e em `app/planos.tsx` (mount/forceShow) para investigar o branco ao abrir `/planos`.
- Debug Firebase (novo): criada Cloud Function `registrarPlanoDebug` e service `services/planoDebug.ts` para enviar eventos de “Ver mais > Meu plano” e `/planos` para `artifacts/{appId}/users/{uid}/debugPlanos`.
- UX plano expirado: botão **Sair da conta** (`PlanoSairContaButton`) em `PlanoWhatsAppEscolhaView`, `TelaBloqueadaPlano` e `app/assinatura.tsx` (web + nativo); web usa `confirmDestructive` (`window.confirm`).
- Versão store **1.0.8** (build EAS production iOS+Android, ago/2026).

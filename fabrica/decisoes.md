---
tags:
  - decisoes
  - historico
  - memoria
fonte: fabrica-knowledge
---

# 📋 Decisões Técnicas — Fábrica de Software

> Histórico de todas as decisões técnicas tomadas nos projetos.
> Atualizado automaticamente pelo agente após cada implementação.

---

## Como usar

O agente consulta esse arquivo antes de qualquer implementação.
Quando tomar uma nova decisão, salva aqui automaticamente via `salvar_decisao`.

---

## Formato de cada decisão

```
### [DATA] — [PROJETO] — [TÍTULO]
- **Decisão:** o que foi decidido
- **Motivo:** por que foi escolhido
- **Alternativa rejeitada:** o que foi descartado e por quê
- **Impacto:** quais arquivos/fluxos afeta
- **Quem decidiu:** Gustavo / Agente / Ambos
```

---

## 2026

### 12/06/2026 — SINAFLOR2 — Integração na fábrica + CLAUDE dividido

- **Decisão:** Entrar na fábrica com PRD `sinaflor-prd.md`, notas em `fabrica/sinaflor/` (6 arquivos + INDEX), `CLAUDE.md` no repo virou índice curto
- **Motivo:** RAG consulta chunks menores e diretos; agente não carrega 1100+ linhas por turno; alias `sinaflor2` → `sinaflor-prd.md` nos hooks
- **Alternativa rejeitada:** Manter monolito `CLAUDE.md` como única fonte — ruim para busca semântica e manutenção
- **Impacto:** `sinaflor2/CLAUDE.md`, `sinaflor2/.cursor/rules/`, `dividir_sinaflor_claude.py`, `rag-lib.js`, Chroma (+164 chunks)
- **Quem decidiu:** Gustavo / Agente

---

### 11/05/2026 — LashMatch + Setmatch — Google Sign-In

- **Decisão:** Usar `expo-auth-session` para login com Google
- **Motivo:** `@react-native-google-signin` requer código nativo e crasha no Expo Go com erro `RNGoogleSignin could not be found`
- **Alternativa rejeitada:** `@react-native-google-signin/google-signin` — incompatível com Expo Go
- **Impacto:** hooks/useAuth.ts, contexts/AuthContext.tsx
- **Quem decidiu:** Ambos

---

### 11/05/2026 — LashMatch + Setmatch — Firebase Auth Persistência

- **Decisão:** Usar `initializeAuth` com `getReactNativePersistence(AsyncStorage)`
- **Motivo:** `getAuth()` simples não persiste sessão entre sessões no React Native
- **Alternativa rejeitada:** `getAuth(app)` — perde login ao fechar o app
- **Impacto:** utils/firebaseConfig.ts
- **Quem decidiu:** Ambos

---

### 11/05/2026 — Fábrica — RAG Local

- **Decisão:** Usar Chroma + sentence-transformers (MiniLM multilingual) para RAG
- **Motivo:** Funciona offline, gratuito, suporta PT-BR nativamente, não depende do Obsidian estar aberto
- **Alternativa rejeitada:** Smart Connections plugin — não expõe API para o MCP
- **Impacto:** obsidian/indexar_obsidian_chroma.py, server-v2.js (rag_buscar)
- **Quem decidiu:** Ambos

---

### 17/05/2026 — LashMatch — Layout Web Desktop

- **Decisão:** Layout 3 colunas no desktop (sidebar 220px + conteúdo flex + painel 280px)
- **Motivo:** App mobile ficava pequeno e centralizado no desktop
- **Alternativa rejeitada:** Manter layout mobile no web — ruim para gestoras que usam no computador
- **Impacto:** components/layout/WebLayout.tsx, app/(tabs)/_layout.tsx
- **Quem decidiu:** Ambos

---

### 22/05/2026 — Setmatch — Cores reais do Figma

- **Decisão:** Usar cores reais extraídas do Figma (#255943, #C7D941, #1E1E1E)
- **Motivo:** PRD inicial tinha cores diferentes (#1B4332, #ADFF2F) que não batiam com o design
- **Alternativa rejeitada:** Cores do PRD v1 — divergiam do Figma real
- **Impacto:** constants/colors.ts de todos os projetos
- **Quem decidiu:** Ambos

---

### 24/05/2026 — LashMatch — WhatsApp Provider

- **Decisão:** Migrar Z-API para WhatsApp Business API oficial (Meta)
- **Motivo:** API oficial é mais confiável, sem custo por mensagem, suporte a templates aprovados
- **Alternativa rejeitada:** Z-API — terceiro não oficial, instável, custo adicional
- **Impacto:** functions/src/whatsapp.ts, functions/.env, todas as Cloud Functions de notificação
- **Quem decidiu:** Gustavo

---

### 24/05/2026 — LashMatch — Estoque sem tipo

- **Decisão:** Remover campo "tipo" do cadastro de produtos do estoque
- **Motivo:** Campo desnecessário para o fluxo da loja
- **Alternativa rejeitada:** Manter tipo — gerava complexidade sem valor
- **Impacto:** tela de estoque, schema Firestore produtos
- **Quem decidiu:** Gustavo

---

## Template para nova decisão

### DD/MM/AAAA — [PROJETO] — [TÍTULO]
- **Decisão:** 
- **Motivo:** 
- **Alternativa rejeitada:** 
- **Impacto:** 
- **Quem decidiu:** 

### 09/06/2026 — cortejo — undefined

- **Decisão:** App Cortejo scaffold completo via MCP staging com 53 arquivos: Expo Router, design tokens marrom café, multi-tenant artifacts/cortejo/salons, Zustand+React Query, paywall free/pro, Cloud Functions para booking público, WhatsApp, MP
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 10/06/2026 — cortejo — Firestore rules — bootstrap do primeiro owner

- **Decisão:** isSalonOwner(salonId) permite read do salão e create do doc members/{uid} com role owner na primeira configuração
- **Motivo:** Regra isMember sozinha impede o chicken-and-egg na criação do salão
- **Alternativa rejeitada:** Cloud Function admin para criar member — mais complexo para MVP
- **Impacto:** firestore.rules, onboarding, useSalonBootstrap
- **Quem decidiu:** Agente

---

### 10/06/2026 — cortejo — Google Sign-In condicional por plataforma

- **Decisão:** GoogleSignInButton só monta useAuthRequest quando EXPO_PUBLIC_GOOGLE_* da plataforma estiver definido; Android precisa androidClientId + webClientId
- **Motivo:** Evitar crash no login quando OAuth não está configurado; expo-auth-session exige client ID por OS
- **Alternativa rejeitada:** Passar só webClientId em todas as plataformas — quebra no Android
- **Impacto:** components/auth/GoogleSignInButton.tsx, utils/googleAuth.ts, app/(auth)/login.tsx
- **Quem decidiu:** Ambos

---

### 10/06/2026 — cortejo — Hidratação do salon context após onboarding

- **Decisão:** setSalonContext imediato após createSalon + navegação direta para /(tabs); isHydrated no store; index aguarda bootstrap antes de rotear
- **Motivo:** onAuthStateChanged não re-dispara após criar salão; evitar loop onboarding
- **Alternativa rejeitada:** router.replace('/') com setTimeout — race condition
- **Impacto:** stores/salonStore.ts, services/salonContext.ts, app/index.tsx, app/(auth)/onboarding.tsx
- **Quem decidiu:** Ambos

---

### 10/06/2026 — cortejo — Deploy Firebase cortejo-app (Blaze)

- **Decisão:** Projeto cortejo-app: Firestore, Hosting (dist), Functions v2, Storage rules, Auth email+Google; secrets WHATSAPP_TOKEN e MP_ACCESS_TOKEN no Secret Manager
- **Motivo:** Plano Blaze habilita Functions com fetch externo e schedulers
- **Alternativa rejeitada:** N/A
- **Impacto:** firebase.json, .firebaserc, functions/SRC/index.ts, hosting https://cortejo-app.web.app
- **Quem decidiu:** Ambos

---

### 10/06/2026 — fabrica — Reindex RAG automatico apos memoria

- **Decisão:** Ao gravar decisoes/erros/padroes via MCP, executar indexar_rapido.py e reiniciar indexar_obsidian_chroma.py --server (modulo rag-reindex.js)
- **Motivo:** Agente esquecia de registrar memoria e RAG ficava desatualizado; usuario pediu fluxo indexar_rapido + --server
- **Alternativa rejeitada:** So instruir no texto --force manual sem automacao no MCP
- **Impacto:** fabrica-apps-mcp/rag-reindex.js, learning-tools.js, server-v2.js, rag-memoria-fabrica.mdc
- **Quem decidiu:** Ambos

---

### 09/06/2026 — LashMatch — Sincronização obrigatória RAG + Obsidian

- **Decisão:** Agente consulta MCP fabrica-apps (`rag_buscar` + `buscar_historico`) antes de codar; ao encerrar, espelha estado em `obsidian/fabrica/*.md` + `lashmatch-prd.md` e reindexa Chroma
- **Motivo:** RAG desatualizado (PHONE_ID e templates antigos); agente pulava consulta MCP
- **Alternativa rejeitada:** Confiar só no CLAUDE.md embutido nas rules
- **Impacto:** `LashMatch/.cursor/rules/rag-memoria-fabrica.mdc` (alwaysApply), `whatsapp-business-api.md`, `lashmatch-schemas.md`, `lashmatch-prd.md`, `erros-e-solucoes.md`, regra global `~/.cursor/rules/rag-memoria-fabrica.mdc`
- **Quem decidiu:** Ambos

---

### 13/06/2026 — cortejo — Protocolo RAG obrigatório antes de libs UI externas

- **Decisão:** Qualquer implementação de calendário/agenda ou expo install + UI deve passar por rag_buscar + buscar_historico nos guias indexados antes de Write. Hooks detectam mandatory docs; gate bloqueia escrita.
- **Motivo:** Incidente 09/06/2026: calendário codado sem ler react-native-calendars.md — risco de componente errado e retrabalho.
- **Alternativa rejeitada:** Confiar só em injeção Chroma automática ou memória do modelo sem MCP
- **Impacto:** Todos os projetos da fábrica; Cortejo agenda como caso de referência
- **Quem decidiu:** usuário + agente

---

### 13/06/2026 — cortejo — Padrão agenda salão Expo — documentação fabrica

- **Decisão:** Padrões Cortejo (agenda card + slots 30min + SalonProfileForm + businessHours) documentados em obsidian/fabrica/agenda-salao-expo-padrao.md. Regra global documentacao-automatica-fabrica.mdc exige doc sem pedir do usuário.
- **Motivo:** Usuário pediu padrão reutilizável e documentação proativa
- **Alternativa rejeitada:** N/A
- **Impacto:** Projetos Expo salão/beleza futuros consultam RAG antes de reimplementar
- **Quem decidiu:** Ambos

---

### 15/06/2026 — fabrica — undefined

- **Decisão:** Módulo ajuda/suporte padrão: constants/support.ts + utils/supportContact.ts + tela ajuda + menu; só WhatsApp sem botão ligar; documentado em modulo-ajuda-suporte-expo.md
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 18/06/2026 — cortejo — Bloqueio de agenda por profissional e horário

- **Decisão:** blockedPeriods no documento do salão com professionalUid, startTime/endTime; lógica em utils/blockedPeriodsLogic.ts; slots filtrados por profissional; Cloud Functions availableSlots e publicBooking deployadas
- **Motivo:** Dono precisa bloquear salão inteiro ou só um profissional, dia inteiro ou intervalo
- **Alternativa rejeitada:** N/A
- **Impacto:** Agenda app, agendamento público e bloqueios por horário/folga
- **Quem decidiu:** Ambos

---

### 18/06/2026 — cortejo — Bloqueio agenda por profissional e horário

- **Decisão:** blockedPeriods no salão com professionalUid e startTime/endTime; utils/blockedPeriodsLogic.ts; deploy availableSlots e publicBooking
- **Motivo:** Bloqueio por profissional e horário
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 18/06/2026 — cortejo — Horário por funcionário

- **Decisão:** businessHours em members/{uid}; config/horarios por profissional; fallback salon.businessHours
- **Motivo:** Cada funcionário tem jornada diferente
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 18/06/2026 — cortejo — Busca cliente agendamento

- **Decisão:** Busca de cliente no topo em agendamento/[id].tsx com filterClientsByQuery; lista 8/20
- **Motivo:** Escalabilidade com muitas clientes
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 18/06/2026 — cortejo — undefined

- **Decisão:** Login automático no site /assinar via código ws de uso único (10 min): app chama assinarWebSessionCreate com Bearer, abre URL com ?ws=; site troca em assinarWebSessionExchange por customToken Firebase; persistência LOCAL mantém sessão no mesmo navegador
- **Motivo:** Usuário vindo do app iOS não deve digitar senha de novo; app e Safari não compartilham cookies nativamente
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 18/06/2026 — lashmatch — undefined

- **Decisão:** LashMatch: excluir conta implementado igual Cortejo — hook useDeleteAccount, services/account.ts, Cloud Function excluirConta (cancel MP + Firestore + Storage + Auth), botão em perfilUsuario.tsx. Doc: obsidian/fabrica/excluir-conta-app-expo-padrao.md
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 20/06/2026 — cortejo — Admin templates WhatsApp via Cloud Functions

- **Decisão:** Tela TemplatesAdminScreen (owner) + listWhatsAppTemplates/createWhatsAppTemplate HTTP com Auth Bearer, WABA de salon.whatsapp.wabaId ou WHATSAPP_BUSINESS_ID fallback, token só no backend
- **Motivo:** App Review Meta whatsapp_business_management e base Tech Provider multi-tenant
- **Alternativa rejeitada:** Graph API direto no app React Native
- **Impacto:** functions/SRC/whatsappTemplates.ts, services/whatsappTemplates.ts, app/config/whatsapp-templates.tsx, firebase.json rewrites
- **Quem decidiu:** Agente + usuário

---

### 20/06/2026 — cortejo — Downgrade automático WhatsApp Gupshup Cortejo

- **Decisão:** Downgrade WhatsApp own→shared via webhook Gupshup (IP allowlist) + health check 6h + push/inbox; promote no go-live ACCOUNT_VERIFIED; reconexão Embedded Signup link
- **Motivo:** Coexistence cai → lembretes continuam no número plataforma sem bloquear envio
- **Alternativa rejeitada:** N/A
- **Impacto:** functions/SRC/whatsappStatus*.ts, WhatsAppStatusCard, app/config/whatsapp, firestore indexes salons whatsapp
- **Quem decidiu:** Ambos

---

### 20/06/2026 — cortejo — Meta Embedded Signup Coexistence Cortejo

- **Decisão:** Embedded Signup Meta Coexistence direto (sem BSP): pagina public/embedded-signup, startEmbeddedSignup/completeEmbeddedSignup Cloud Functions, botao Pro na tela whatsapp
- **Motivo:** Tech Provider multi-tenant numero proprio via whatsapp_business_app_onboarding
- **Alternativa rejeitada:** N/A
- **Impacto:** functions/SRC/embeddedSignup.ts, services/embeddedSignup.ts, public/embedded-signup, WhatsAppStatusCard reconectar Meta
- **Quem decidiu:** Ambos

---

### 20/06/2026 — cortejo — undefined

- **Decisão:** Downgrade WhatsApp Meta direto (Cloud API): metaWhatsappWebhook.ts com X-Hub-Signature-256, mapa account_update/quality/review, debounce 3 falhas envio, health check Graph API 6h, integrado com downgradeWhatsAppConnection/promote existentes. Path functions/SRC/ (não src/).
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 21/06/2026 — cortejo — Documentação fábrica WhatsApp salão multi-tenant

- **Decisão:** Nota canônica whatsapp-salao-expo-padrao.md na Obsidian fabrica: dois fluxos (compartilhado vs Embedded Signup Coexistence), schema salon.whatsapp, setup Meta OAuth (domínio + SDK JS + CONFIG_ID), arquivos copiáveis, erros #131008/#132008, checklist novo projeto. Espelho em cortejo/docs/whatsapp-business-api.md
- **Motivo:** Consolidar conversas jun/2026 para reutilizar em outros apps salão sem repetir incidentes OAuth/template
- **Alternativa rejeitada:** Só atualizar whatsapp-business-api.md LashMatch (single-tenant)
- **Impacto:** obsidian/fabrica/whatsapp-salao-expo-padrao.md, INDEX.md, cortejo-schemas.md, docs/whatsapp-business-api.md
- **Quem decidiu:** Ambos

---

### 21/06/2026 — cortejo — Assinatura iOS via RevenueCat (StoreKit)

- **Decisão:** iOS usa react-native-purchases (RevenueCat) com entitlement pro, app_user_id=salonId, webhook revenuecatWebhook + sync revenueCatSyncSubscription. Android/web mantêm Mercado Pago.
- **Motivo:** Rejeição App Store 3.1.1 — checkout web/MP no iOS proibido; IAP nativo obrigatório.
- **Alternativa rejeitada:** Site /assinar + deep link cortejo://plano/confirmado + IosAssinaturaView WebBrowser
- **Impacto:** EAS Build iOS obrigatório; secrets REVENUECAT_API_KEY_IOS, REVENUECAT_SECRET_API_KEY, REVENUECAT_WEBHOOK_AUTHORIZATION; fonte de verdade Pro no iOS = RevenueCat (não só Firestore).
- **Quem decidiu:** Usuário + agente

---

### 21/06/2026 — cortejo — undefined

- **Decisão:** Planos tiered mensais (plano1/planomensal2-4) com limite WhatsApp msgUsage; RevenueCat 4 packages; planoAnual removido
- **Motivo:** Pacotes de mensagens por tier; anual descontinuado; iOS IAP + Android MP
- **Alternativa rejeitada:** N/A
- **Impacto:** Firestore salon.planTier/planMsgLimit/msgUsage; webhook RevenueCat; resolveSender WhatsApp
- **Quem decidiu:** Ambos

---

### 21/06/2026 — cortejo — undefined

- **Decisão:** Calendário AgendaCalendar: key={visibleMonthKey} no Calendar para remount ao navegar mês com data selecionada. Cliente: useFocusEffect + confirmed conta visita após start. Público /agendar: salonHasActiveSubscription respeita planExpiresAt/grace CANCELLED + sync RevenueCat API quando Firestore stale iOS.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/06/2026 — cortejo — undefined

- **Decisão:** msgUsage usa periodStart/periodEnd (não month). Lazy reset no resolveSender/prepareTenantForWhatsAppSend. blocked para Pro no limite (não envia shared). Apenas confirmação+D7+D24 contam. notify 80%/100% com notifiedAt80/100. RevenueCat INITIAL/RENEWAL reset período; PRODUCT_CHANGE mantém sent. UI PlanTierCard + badge lembrete pausado.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/06/2026 — cortejo — Documentação jun/2026 + página suporte App Store

- **Decisão:** Página pública /suporte no Firebase Hosting; doc consolidada cortejo-modulos-jun2026-padrao.md na fábrica; assinatura dual RevenueCat (iOS) + MP (Android); trial 16d; msgUsage por período.
- **Motivo:** Reutilizar em outros apps salão/beleza e atender App Store Connect (URL suporte + privacidade).
- **Alternativa rejeitada:** N/A
- **Impacto:** App Store URL suporte https://cortejo-app.web.app/suporte; INDEX Obsidian atualizado; schemas e MP doc revisados.
- **Quem decidiu:** Ambos

---

### 22/06/2026 — cortejo — Documentação MCPs revenuecat + appstore-connect e pagamentos jun/2026

- **Decisão:** Criada nota fabrica/mcps-cursor-padrao.md com regra MCP primeiro. Atualizados mercadopago-assinatura-ota-padroes, cortejo-modulos-jun2026, INDEX, arquitetura-fabrica-ia, mercadopago-integration. Pagamentos: web sem checkout, iOS preço R$ catálogo, helpers cancelamento/trial documentados.
- **Motivo:** Novos MCPs appstore-connect e revenuecat; mudanças de UI pagamento não estavam no Obsidian
- **Alternativa rejeitada:** Documentar só no repo docs/
- **Impacto:** Todos os projetos da fábrica; agente deve consultar MCP antes de codar integrações
- **Quem decidiu:** usuário + agente

---

### 22/06/2026 — cortejo — Doc MCPs e pagamentos jun/2026

- **Decisão:** Nota fabrica/mcps-cursor-padrao.md + atualização pagamentos jun/2026 no Obsidian
- **Motivo:** MCPs appstore-connect e revenuecat novos; UI pagamentos desatualizada
- **Alternativa rejeitada:** Documentar só no repo docs/
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/06/2026 — cortejo — Documentação MCPs (revenuecat, appstore-connect) e pagamentos jun/2026

- **Decisão:** Criada nota fabrica/mcps-cursor-padrao.md com regra MCP primeiro. Atualizados mercadopago-assinatura-ota-padroes, cortejo-modulos-jun2026, INDEX, arquitetura-fabrica-ia, mercadopago-integration e cortejo-projeto.mdc. Pagamentos documentados: web sem checkout (WebPlanoView), iOS preço R$ catálogo (androidPriceLabel), helpers isSubscriptionCancelled/canCancelSubscription/isSubscriptionPaymentPendingReview, nomes de tier Starter/Básico/Avançado/Profissional.
- **Motivo:** Novos MCPs appstore-connect e revenuecat; mudanças de UI pagamento jun/2026 não estavam refletidas no Obsidian/RAG
- **Alternativa rejeitada:** Documentar só no repo docs/ ou confiar na memória do agente sem Obsidian
- **Impacto:** Todos os projetos da fábrica; agente deve consultar MCP revenuecat + appstore-connect + mercadopago antes de codar integrações de pagamento
- **Quem decidiu:** usuário + agente

---

### 22/06/2026 — cortejo — Doc MCPs revenuecat + appstore-connect e pagamentos jun/2026

- **Decisão:** Criada fabrica/mcps-cursor-padrao.md (MCP primeiro). Atualizados mercadopago-assinatura-ota-padroes, cortejo-modulos-jun2026, INDEX, arquitetura-fabrica-ia, mercadopago-integration, cortejo-projeto.mdc. Pagamentos: web sem checkout, iOS preço R$ catálogo, helpers cancelamento/trial.
- **Motivo:** MCPs appstore-connect e revenuecat novos; UI pagamentos desatualizada no RAG
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/06/2026 — cortejo — undefined

- **Decisão:** salonHasActiveSubscription: checar planExpiresAt/currentPeriodEnd ANTES de bloquear CANCELLED do MP; RevenueCatBootstrap e shareSalonBookingLink sincronizam Firestore via revenueCatSyncSubscription quando iOS tem entitlement ativo
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/06/2026 — cortejo — Doc assinatura trial 14d + sync Firestore iOS + regra Cursor

- **Decisão:** Atualizada fabrica/cortejo-modulos-jun2026-padrao.md e mercadopago-assinatura-ota-padroes.md com seção Firestore×RevenueCat, trial TRIAL_DAYS=14 espelhado app/functions, RC API V2, elegibilidade trial. Criada regra cortejo/.cursor/rules/rag-assinatura-padrao.mdc. Erros registrados em erros-e-solucoes.md.
- **Motivo:** Incidente jun/2026: Pro no iOS mas /agendar bloqueado; trial 16 vs 14; sync RC 403 V1.
- **Alternativa rejeitada:** N/A
- **Impacto:** Agentes devem consultar RAG + regra antes de alterar paywall/trial/sync; checklist inclui availableSlots?meta=1
- **Quem decidiu:** usuário + agente

---

### 09/06/2026 — lashmatch — Docs assinatura MP + RevenueCat no Obsidian (RAG)

- **Decisão:** Notas `lashmatch-modulos-assinatura-jun2026.md`, `lashmatch-mercadopago-assinatura.md`, `lashmatch-revenuecat-assinatura.md` em `obsidian/fabrica/`. `LashMatch/docs/*.md` viraram ponteiros. Atualizados `lashmatch-schemas`, `INDEX.md`, `mercadopago-assinatura-ota-padroes`.
- **Motivo:** Padrão fábrica: docs indexáveis no Chroma; mesmo modelo do Cortejo.
- **Impacto:** `rag_buscar("lashmatch assinatura")` retorna guias completos; reindexar após editar notas.
- **Quem decidiu:** usuário + agente

---

### 22/06/2026 — LashMatch — Starter R$ 79,90 + iOS paywall alinhado

- **Decisão:** Plano Starter (plano1 / lashmatch_mensal) atualizado para R$ 79,90 no código e MP. IosAssinaturaView usa priceString da App Store e mapeia lashmatch_mensal → plano1. Deploy RC bloqueado até configurar REVENUECAT_WEBHOOK_SECRET e REVENUECAT_SECRET_API_KEY no Firebase.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/06/2026 — LashMatch — iOS 4 tiers — sem plano anual

- **Decisão:** iOS unificado com Android: 4 tiers mensais (plano1–planomensal4). Plano anual removido. Product IDs Apple: lashmatch_plano1 … lashmatch_planomensal4. Legado lashmatch_mensal→plano1, lashmatch_anual→planomensal4. IosAssinaturaView lista os 4 planos como pagamento Android.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/06/2026 — undefined — undefined

- **Decisão:** undefined
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/06/2026 — lashmatch — undefined

- **Decisão:** LashMatch paywall iOS: rota /assinatura fora das tabs (PlanoAccessRedirect) porque (tabs)/pagamento era bloqueado pelo TabsLayout quando !temAcessoEfetivo. ASC: 3/4 IAPs MISSING_METADATA.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/06/2026 — lashmatch — undefined

- **Decisão:** App Store Connect LashMatch: product IDs renomeados para lashmatch_mensal, lashmatch_mensal2, lashmatch_mensal3, lashmatch_mensal4. Código types/purchase.ts + revenueCatSubscription.ts atualizados; aliases legados planomensal* mantidos.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/06/2026 — lashmatch — undefined

- **Decisão:** RevenueCat lashmatch offering: packages $rc_monthly..$rc_monthly_4 apontam para lashmatch_mensal..mensal4. Deploy revenuecatWebhook + revenueCatSyncSubscription OK.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/06/2026 — lashmatch — undefined

- **Decisão:** Removidos aliases legados iOS (planomensal*, anual, lashmatch_plano1). RevenueCat: 4 produtos lashmatch_mensal..mensal4 apenas; legados arquivados no RC.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/06/2026 — cortejo — WhatsApp Embedded Signup reativado na UI

- **Decisão:** Reativado Embedded Signup Meta na UI: whatsapp.tsx e WhatsAppStatusCard usam runEmbeddedSignupFlow novamente; removido utils/whatsappOwnNumber.ts
- **Motivo:** Usuário pediu liberar número próprio após gate em desenvolvimento
- **Alternativa rejeitada:** N/A
- **Impacto:** Donas Pro podem Conectar meu WhatsApp; pending/reconectar no card
- **Quem decidiu:** Ambos

---

### 23/06/2026 — cortejo — Feature flag platformConfig para WhatsApp do salão

- **Decisão:** Gate global Firestore `artifacts/cortejo/system/platformConfig.whatsappSalonEnabled` (boolean); app (`useWhatsappSalonFeature` + onSnapshot), backend (`startEmbeddedSignup` 503 se off), rules read autenticado / write false
- **Motivo:** Rollout gradual sem redeploy; desligar rapidamente se incidente em produção
- **Alternativa rejeitada:** Hardcode `alertWhatsAppOwnNumberInDevelopment()` permanente no app
- **Impacto:** OTA/build obrigatório antes de flag true; doc em whatsapp-salao-expo-padrao.md §14 + cortejo-schemas.md
- **Quem decidiu:** Ambos

---

### 23/06/2026 — cortejo — completeEmbeddedSignupWeb para mobile OAuth

- **Decisão:** Conclusão Embedded Signup na página web via `completeEmbeddedSignupWeb` (auth por sessionId TTL); mobile usa redirect OAuth página inteira; app recebe `connected=1` no deep link
- **Motivo:** Popup FB.login no celular terminava em "Feche esta aba" sem WABA/número
- **Alternativa rejeitada:** Forçar usuária a completar fluxo só no deep link com Bearer (falhava no browser do app)
- **Impacto:** public/embedded-signup/index.html, embeddedSignup.ts, firebase.json rewrite /api/completeEmbeddedSignupWeb
- **Quem decidiu:** Ambos

---

### 23/06/2026 — cortejo — WhatsAppConnectGuide antes do vínculo Meta

- **Decisão:** Componente WhatsAppConnectGuide com instruções Coexistence (portfólio existente, WABA existente, site Instagram ou URL plataforma) renderizado antes de conectar/reconectar
- **Motivo:** Usuárias escolhiam "criar portfólio/conta/número" e fluxo falhava ou ficava pending
- **Alternativa rejeitada:** Apenas copy na página HTML (app não mostrava guia ao reconectar no card)
- **Impacto:** components/whatsapp/WhatsAppConnectGuide.tsx, whatsapp.tsx, WhatsAppStatusCard.tsx
- **Quem decidiu:** Ambos

---

### 25/06/2026 — cortejo — WhatsApp {{10}} regras e observações em linhas separadas

- **Decisão:** montarBlocoObservacoesRegras usa \n entre 📋 Regras e 📝 Observações (regras primeiro); sem \n\n no início do bloco; bloco10 não passa por templateTextParam para preservar quebra.
- **Motivo:** Usuário pediu observações abaixo das regras na mensagem WhatsApp; join com · ficava na mesma linha.
- **Alternativa rejeitada:** Duas variáveis {{10}}/{{11}} no template — exigiria novos templates Meta aprovados.
- **Impacto:** functions/SRC/whatsapp.ts — redeploy functions necessário.
- **Quem decidiu:** Ambos

---

### 25/06/2026 — LashMatch — WhatsApp Embedded Signup estilo Cortejo

- **Decisão:** Portar Embedded Signup Meta para LashMatch: tenantId=uid em usuarios/{uid}.whatsapp, flag artifacts/{appId}/system/platformConfig.whatsappSalonEnabled, resolveSender envia pelo phoneNumberId proprio quando live+assinatura ativa senao WHATSAPP_PHONE_ID LashMatch.
- **Motivo:** Permitir lash designers conectarem WhatsApp Business proprio com rollout controlado por flag global igual Cortejo.
- **Alternativa rejeitada:** N/A
- **Impacto:** Novas CFs startEmbeddedSignup/complete/cancel, tela app/config/whatsapp, rewrites hosting embedded-signup, rules bloqueiam client escrever whatsapp.
- **Quem decidiu:** Ambos

---

### 28/06/2026 — LashMatch — Análises bloqueadas na web (IA + manual)

- **Decisão:** Toda análise de clientes (IA, câmera, assistente manual, analysisResult) fica somente no app iOS/Android. Web: canUseClientAnalysis() + rotas *.web.tsx bloqueadas; Home sem card Iniciar Nova Análise; WebDesktopPanel sem atalho Nova análise. Histórico no perfil da cliente permanece leitura.
- **Motivo:** Reanimated, resolveAssetSource e câmera nativa quebram na web; gestão no browser, análise no mobile.
- **Alternativa rejeitada:** Manter assistente manual na web ou aviso com título Iniciar Nova Análise na Home.
- **Impacto:** utils/analysisPlatform.ts, index.tsx, WebDesktopPanel.tsx, camera.web.tsx, assistente/_layout.web.tsx, analysisResult.web.tsx, CLAUDE.md §19.3, fabrica/lashmatch-web-plataforma.md
- **Quem decidiu:** Gustavo

---

### 28/06/2026 — LashMatch — CLAUDE.md deixou de ser base de conhecimento

- **Decisão:** CLAUDE.md na raiz virou ponte curta; monólito em docs/archive/CLAUDE-monolito-historico.md. Regra alwaysApply fonte-verdade-fabrica.mdc: padrões só via rag_buscar + obsidian/fabrica, nunca Seção X do CLAUDE.
- **Motivo:** Duplicar KB no repo gasta contexto e desatualiza; fábrica Obsidian+RAG é fonte única.
- **Alternativa rejeitada:** Manter CLAUDE.md monolítico injetado no contexto do agente.
- **Impacto:** CLAUDE.md, .cursorrules, .cursor/rules/*, ~/.cursor/rules/rag-memoria-fabrica.mdc, arquitetura-fabrica-ia.md
- **Quem decidiu:** Gustavo

---

### 28/06/2026 — fabrica — Baseline RAG eval harness (PR1)

- **Decisão:** Criado golden set (25 pares em fabrica/eval/golden-set.jsonl) + harness run_baseline.py contra Chroma :7332. Baseline jun/2026: hit@1=40%, hit@3=60%, hit@5=72%, MRR=0.5233. PR1 não altera indexação/retrieval — só mede estado atual.
- **Motivo:** Medir qualidade do retrieval antes de otimizar chunking/ranking; evitar regressões em PRs futuros.
- **Alternativa rejeitada:** Avaliar só via MCP rag_buscar manual — não escala e mistura camada MCP com Chroma puro.
- **Impacto:** fabrica/eval/*, arquitetura-fabrica-ia.md, branch feature/rag-eval-harness
- **Quem decidiu:** Gustavo + agente

---

### 28/06/2026 — fabrica — Retrieval hibrido RAG + golden v2 + checklist deploy

- **Decisão:** Retrieval hibrido: denso+BM25+RRF+rerank bge-reranker-v2-m3; filtro tipo_doc spec/eval; golden v2 com aceitaveis; nova nota firebase-deploy-checklist-padrao.md. Delta vs v2: hit@1 +8pp (48→56%), integracao +25pp hit@1, padrao hit@1 flat (40%). Gate merge: integracao OK, padrao hit@1 nao subiu.
- **Motivo:** Melhorar recall em integracao/fluxo e reduzir PRD nos top-1 de queries de padrao; medir com harness v2.
- **Alternativa rejeitada:** Só denso Chroma — padrao empacava em 40% hit@1 por dominacao de PRD e BM25 puro sem rerank.
- **Impacto:** rag_retrieval.py, indexar_rapido.py, indexar_obsidian_chroma.py, fabrica/eval/*, firebase-deploy-checklist-padrao.md, arquitetura-fabrica-ia.md; MCP timeout 120s em server-v2.js
- **Quem decidiu:** Gustavo + agente

---

### 28/06/2026 — fabrica — Hot path RAG <200ms — BM25 pre-build + 127.0.0.1

- **Decisão:** Hot path otimizado: BM25Okapi x2 pre-build na subida (default + demote_spec); singleton fixo; MCP/eval usam 127.0.0.1. Latencia quente ~47ms (max 52ms). Eval hotpath identico ao baseline (hit@1 52%, hit@3 92%). gs-025 fabrica caiu hit@1 (1->2) mas permanece top-3. Recomendado merge PR #2.
- **Motivo:** Destravar merge: latencia real do hot path sem mascarar com timeout 120s.
- **Alternativa rejeitada:** Manter localhost no MCP — Windows IPv6 adicionava ~2s por query apesar de buscar interno ~25ms.
- **Impacto:** rag_retrieval.py, indexar_obsidian_chroma.py, run_baseline.py, fabrica-apps-mcp/server-v2.js (127.0.0.1, timeout 15s)
- **Quem decidiu:** Gustavo + agente

---

### 28/06/2026 — fabrica — MCP hotpath align — 127.0.0.1 e sem fallback CLAUDE.md

- **Decisão:** fabrica-apps-mcp branch feature/mcp-hotpath-align: buscarHistoricoRemoto e rag_buscar usam 127.0.0.1; rag_buscar offline retorna aviso (igual buscar_historico), sem TF-IDF legado; removidos carregarRAG/buscarRAG/RAG_INDEX. Smoke test: online ~92ms, offline mensagem correta.
- **Motivo:** Alinhar MCP ao hot path RAG (<200ms, Chroma hibrido) e impedir respostas silenciosas do monolito CLAUDE.md.
- **Alternativa rejeitada:** Manter fallback TF-IDF sobre CLAUDE.md/rag-index.json quando servidor 7332 offline — contradiz arquitetura (CLAUDE.md nao e KB).
- **Impacto:** fabrica-apps-mcp/server-v2.js — requer restart MCP no Cursor para aplicar.
- **Quem decidiu:** Gustavo + agente

---

### 28/06/2026 — fabrica — RAG hot path hibrido + fallback honesto

- **Decisão:** Retrieval do RAG passou a ser hibrido denso(Chroma)+BM25 com RRF, BM25 construido uma vez no boot/reindex. Reranker bge-reranker-v2-m3 e offline-only (flag de eval), nunca no hot path. rag_buscar e buscar_historico em 127.0.0.1:7332. Fallback do CLAUDE.md removido: servidor offline retorna aviso, nao busca degradada. Regua oficial de avaliacao: golden-set.jsonl v2 com campo aceitaveis, harness em fabrica/eval.
- **Motivo:** Hibrido subiu hit@3 de 72% para 92% sem custo de latencia. Reranker dava +qualidade mas 10s/query, inaceitavel no dia a dia. Fallback do CLAUDE.md mascarava servidor caido com busca pior numa fonte abandonada.
- **Alternativa rejeitada:** Reranker online (10s/query); manter fallback TF-IDF no CLAUDE.md
- **Impacto:** Busca da fabrica mais precisa e ~80ms; falha de servidor agora e visivel
- **Quem decidiu:** Ambos

---

### 28/06/2026 — ERP — Stack e multi-tenancy do ERP web

- **Decisão:** ERP web sério: Spring Boot + Angular + PostgreSQL. Multi-tenant por SCHEMA (um banco, um schema por cliente + schema master de catálogo). Troca de schema via Hibernate multi-tenancy (MultiTenantConnectionProvider + CurrentTenantIdentifierResolver). Migrations com Flyway orquestrado por schema. Provisionamento de tenant = CREATE SCHEMA + baseline de migrations + registro no master.
- **Motivo:** ERP transacional sério pede ACID e regra de negócio densa, onde Spring é mais adequado que serverless. Gustavo já domina Spring/Angular (acquirer SIPPE) e ERP por background SAP. Schema-por-tenant dá isolamento forte (modelo mandante/client do SAP) sem o custo operacional de banco-por-tenant (N pools, N backups, migration em N bancos).
- **Alternativa rejeitada:** Next.js+Supabase (serverless fraco pra transação ERP); banco-por-tenant (custo operacional alto); discriminador tenant_id (isolamento mais fraco)
- **Impacto:** Define schema, roteamento de conexão e processo de onboarding de cliente. Fábrica vira copiloto de conhecimento (RAG/memória/gate/PR) em vez de linha de montagem, já que scaffold é RN-specific.
- **Quem decidiu:** Ambos

---

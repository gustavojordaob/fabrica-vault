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

### 07/08/2026 — setmatch — Aula online pagar/liberar + feed social

- **Decisão:** Aula paga: aluno em `/aula/[id]` usa **Pagar** (MP, `tipo: aula_online` + `aulaPublicadaId`) ou **Pedir liberação** (pagamento `pendente` + chat). Professor libera em `/clube/financeiro` (query por `donoUid`). Feed: foto (`posts/{uid}`), comentários subcoleção, share in-app (chat) e fora (loja + deep link — precisa instalar o app). Perto de mim: banner na Home → `/(tabs)/proximos`.
- **Motivo:** Usuário pediu fluxo de liberar/pagar aula, achar pessoas/quadras e feed com comentário/foto/compartilhar.
- **Alternativa rejeitada:** Checkout iOS IAP nesta entrega (fica para depois); share externo sem app (conteúdo fica só autenticado).
- **Impacto:** `app/aula/[id].tsx`, `app/post/[id].tsx`, `app/(tabs)/home.tsx`, `services/feed.ts`, `services/aulasPublicadas.ts`, `firestore.rules`, `storage.rules`, financeiro por donoUid
- **Quem decidiu:** Ambos

### 06/08/2026 — SINAFLOR2 — HU133/HU134 Arquivar e Desarquivar na tramitação

- **Decisão:** Tipos 7 (Arquivar) e 8 (Desarquivar) na fila/rascunho/histórico existentes; `acoesDisponiveis` no contexto; Arquivar GO/GA com despacho+anexo → status Arquivado; Desarquivar GO/GA/Analista só se Arquivado → restaura `statusAnterior` do último Arquivar; bloquear 7+8 na mesma fila; front com `tramitacao-arquivamento`.
- **Motivo:** Atender HU133/HU134 sem fluxo paralelo.
- **Alternativa rejeitada:** Endpoints separados de arquivar/desarquivar fora da fila de tramitação.
- **Impacto:** `LicenciamentoTramitacaoService`, `gestao-tramitacao`, `tramitacao-arquivamento`, nota `tramitacao-arquivar-desarquivar.md`.
- **Quem decidiu:** Gustavo + Agente

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

### 09/06/2026 — cortejo

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

### 15/06/2026 — fabrica

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

### 18/06/2026 — cortejo

- **Decisão:** Login automático no site /assinar via código ws de uso único (10 min): app chama assinarWebSessionCreate com Bearer, abre URL com ?ws=; site troca em assinarWebSessionExchange por customToken Firebase; persistência LOCAL mantém sessão no mesmo navegador
- **Motivo:** Usuário vindo do app iOS não deve digitar senha de novo; app e Safari não compartilham cookies nativamente
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 18/06/2026 — lashmatch

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

### 20/06/2026 — cortejo

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

### 21/06/2026 — cortejo

- **Decisão:** Planos tiered mensais (plano1/planomensal2-4) com limite WhatsApp msgUsage; RevenueCat 4 packages; planoAnual removido
- **Motivo:** Pacotes de mensagens por tier; anual descontinuado; iOS IAP + Android MP
- **Alternativa rejeitada:** N/A
- **Impacto:** Firestore salon.planTier/planMsgLimit/msgUsage; webhook RevenueCat; resolveSender WhatsApp
- **Quem decidiu:** Ambos

---
### 21/06/2026 — cortejo

- **Decisão:** Calendário AgendaCalendar: key={visibleMonthKey} no Calendar para remount ao navegar mês com data selecionada. Cliente: useFocusEffect + confirmed conta visita após start. Público /agendar: salonHasActiveSubscription respeita planExpiresAt/grace CANCELLED + sync RevenueCat API quando Firestore stale iOS.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 22/06/2026 — cortejo

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

### 22/06/2026 — cortejo

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

### 23/06/2026 — lashmatch

- **Decisão:** LashMatch paywall iOS: rota /assinatura fora das tabs (PlanoAccessRedirect) porque (tabs)/pagamento era bloqueado pelo TabsLayout quando !temAcessoEfetivo. ASC: 3/4 IAPs MISSING_METADATA.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 23/06/2026 — lashmatch

- **Decisão:** App Store Connect LashMatch: product IDs renomeados para lashmatch_mensal, lashmatch_mensal2, lashmatch_mensal3, lashmatch_mensal4. Código types/purchase.ts + revenueCatSubscription.ts atualizados; aliases legados planomensal* mantidos.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 23/06/2026 — lashmatch

- **Decisão:** RevenueCat lashmatch offering: packages $rc_monthly..$rc_monthly_4 apontam para lashmatch_mensal..mensal4. Deploy revenuecatWebhook + revenueCatSyncSubscription OK.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 23/06/2026 — lashmatch

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

### 29/06/2026 — fabrica — Limpeza de indice RAG e cobertura ERP/SINAFLOR no eval

- **Decisão:** outros.md (monolito CLAUDE residual, 127 chunks) removido do indice via should_index em indexar_rapido.py (arquivo fica no disco). Golden set expandido de 31 para 56 pares cobrindo ERP e SINAFLOR. Indice usa basename como esperado_nota (nao path). Resultado regua v2: hit@1 66.1%, hit@3 87.5%.
- **Motivo:** outros.md poluia o top-5 em varios pares (mesmo problema do monolito). Pares novos dao medicao aos dominios ERP e SINAFLOR que estavam sem cobertura. Ganho de +6pp no hit@1 sem tocar nenhuma nota de conhecimento.
- **Alternativa rejeitada:** Mexer em decisoes.md, indexar_rapido.py (path relativo) e consolidar notas agora — adiado para Ondas 2/3 por risco a buscar_historico e ao conhecimento canonico
- **Impacto:** Dividas conhecidas e isoladas no plano-consolidacao.md: decisoes.md como log (Onda 2), metadado de dominio + consolidacao G1-G9 (Onda 3), gs-001 schema dominado por PRD.
- **Quem decidiu:** Ambos

---

### 29/06/2026 — fabrica — Limpeza de indice RAG e cobertura ERP/SINAFLOR no eval

- **Decisão:** outros.md (monolito CLAUDE residual, 127 chunks) removido do indice via should_index em indexar_rapido.py (arquivo fica no disco). Golden set expandido de 31 para 56 pares cobrindo ERP e SINAFLOR. Indice usa basename como esperado_nota (nao path). Resultado regua v2: hit@1 66.1%, hit@3 87.5%.
- **Motivo:** outros.md poluia o top-5 em varios pares (mesmo problema do monolito). Pares novos dao medicao aos dominios ERP e SINAFLOR que estavam sem cobertura. Ganho de +6pp no hit@1 sem tocar nenhuma nota de conhecimento.
- **Alternativa rejeitada:** Mexer em decisoes.md, indexar_rapido.py (path relativo) e consolidar notas agora — adiado para Ondas 2/3 por risco a buscar_historico e ao conhecimento canonico
- **Impacto:** Dividas conhecidas e isoladas no plano-consolidacao.md: decisoes.md como log (Onda 2), metadado de dominio + consolidacao G1-G9 (Onda 3), gs-001 schema dominado por PRD.
- **Quem decidiu:** Ambos

---

### 01/07/2026 — cortejo — Grace period após cancelamento MP — planExpiresAt global

- **Decisão:** Ao cancelar assinatura Mercado Pago, o salão mantém planTier e recebe planExpiresAt (MP next_payment_date → trial+1m → +1m). isSalonSubscriptionActive libera acesso até essa data mesmo com status CANCELLED. Após expirar, paywall mostra plano anterior com Assinar novamente. mpSyncSubscription faz backfill para cancelados sem planExpiresAt.
- **Motivo:** Usuários pagantes eram bloqueados imediatamente após cancelar; planTier permanecia mas gate negava acesso sem data de fim.
- **Alternativa rejeitada:** Manter planTier como proxy de acesso ativo (bloqueava cancelados sem planExpiresAt)
- **Impacto:** functions mpCancelarAssinatura/mpSyncSubscription/mpWebhook; utils/subscription.ts; AndroidAssinaturaView; cancelamento.tsx
- **Quem decidiu:** usuário + agente

---

### 01/07/2026 — zenpro — Editor capinha — realismo visual browser

- **Decisão:** Preview usa silhueta iphone-mask.png (sem frame preto), fundo #ececec, drop shadow Konva blur, bordas internas via canvas ring a partir da máscara, câmera como recorte escuro processado do overlay (não overlay branco opaco).
- **Motivo:** Mockup anterior parecia flat/schematic; overlay azul/branco cobria a foto.
- **Alternativa rejeitada:** Desenhar overlay PNG bruto por cima da foto
- **Impacto:** CaseEditor.tsx + caseEffectsUtils + overlayUtils + useCaseVisualAssets; transform/foto original inalterados
- **Quem decidiu:** Ambos

---

### 01/07/2026 — zenpro — Firestore personalizacoes e pedidos Zenpro

- **Decisão:** Zenpro persiste personalizacoes (Comprar) e pedidos (Pagar) no Firestore; foto continua no Storage; regras abertas dev com TODO auth; cliente mock no pedido.
- **Motivo:** Fatia loja+personalização precisa persistir antes de auth/MP
- **Alternativa rejeitada:** N/A
- **Impacto:** salvarPersonalizacao.ts, criarPedido.ts, firestore.rules, checkout/editor, docs/firebase-persistencia.md
- **Quem decidiu:** Ambos

---

### 01/07/2026 — zenpro

- **Decisão:** Zenpro fatia 1 multi-tenant: coleções lojas (slug, donoUid, config), usuarios com papel marca|revendedor, produtos e modelos_celular centrais, pedidos em lojas/{lojaId}/pedidos. Rules: marca tudo, revendedor só minhaLoja(), catálogo read público write marca. Seed tsx + testes emulator. Sem admin UI.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 01/07/2026 — capinhas — Fundacao multi-tenant validada com teste de isolamento

- **Decisão:** Multi-tenant de revendedores: produtos/modelos centrais (marca), pedidos por loja (lojas/{id}/pedidos), papeis marca|revendedor em usuarios/{uid}. Isolamento nas Security Rules do Firestore, testado no emulador (test:rules:multitenant): revendedor nao le pedido de outra loja, marca ve tudo. 3 cenarios PASS.
- **Motivo:** Isolamento entre revendedores nao pode depender do front. Rules testadas automatizadamente evitam vazamento de dados entre lojas.
- **Alternativa rejeitada:** N/A
- **Impacto:** Fundacao para as fatias 2-6 (auth, admin marca, admin revendedor, roteamento slug). Rules precisam de firebase deploy antes de producao.
- **Quem decidiu:** Ambos

---

### 01/07/2026 — zenpro — Checkout multitenant — pedido sempre em lojas/{lojaId}/pedidos

- **Decisão:** Checkout público grava pedidos apenas em lojas/{lojaId}/pedidos via criarPedidoLoja. Loja vinculada persiste no carrinho (sessionStorage). /checkout redireciona para /{slug}/checkout. criarPedido (raiz pedidos/) não é mais usado no fluxo de pagamento.
- **Motivo:** Admin revendedor/marca só consulta subcoleção por loja; pedidos na raiz ficam invisíveis ao revendedor.
- **Alternativa rejeitada:** Listar pedidos legados no admin — mantém dois modelos e confunde operação.
- **Impacto:** Compras pela home / sem slug exigem escolher loja revendedora antes do checkout.
- **Quem decidiu:** Agente + usuário

---

### 01/07/2026 — zenpro — Promover cliente existente a revendedor sem duplicar Auth

- **Decisão:** Ao aprovar solicitação ou criar revendedor manualmente, se signUp REST retorna EMAIL_EXISTS, buscar uid via indices_email ou scan usuarios, validar que não é marca/revendedor duplicado, e fazer merge em usuarios com papel revendedor + lojaId. Não criar segundo usuário Auth.
- **Motivo:** Clientes que já compram no site têm conta Auth; aprovação como revendedor deve reutilizar o mesmo uid.
- **Alternativa rejeitada:** Bloquear aprovação ou exigir e-mail diferente
- **Impacto:** revendedorAdminService, emailRevendedorUtils, UI admin solicitações e novo revendedor
- **Quem decidiu:** usuário + agente

---

### 01/07/2026 — zenpro — Produto personalizavel + email automatico revendedor

- **Decisão:** Produtos personalizáveis usam campo personalizavel no Firestore; seção do site lê produtos ativos com personalizavel=true e tipo capinha. E-mail de aprovação de revendedor via coleção emails_outbox + Cloud Function processarEmailOutbox (Resend ou SMTP).
- **Motivo:** Admin controla quais itens aparecem em Personalize com foto; aprovação de revendedor deve enviar e-mail automático com guia do sistema.
- **Alternativa rejeitada:** N/A
- **Impacto:** ProdutoFormPageClient, catalogoProdutos, PersonalizarSection, functions/, firestore.rules
- **Quem decidiu:** Ambos

---

### 02/07/2026 — zenpro — Catálogo dinâmico modelo × variante (material)

- **Decisão:** Separar aparelho (modelos/) de variante vendável (produtos/ com material, preço, modelosCompativeis). Visual resolvido por resolverVisualPersonalizacao: produto > modelo > SPECS código. Editor recebe ?modelo=&produto= e PersonalizacaoVisualProvider.
- **Motivo:** Permitir N capinhas (couro, silicone…) × N celulares com preços distintos sem hardcode no front.
- **Alternativa rejeitada:** Um produto por combinação hardcoded em produtosMock ou preço único por modeloId
- **Impacto:** Vitrine, editor, carrinho e admin passam a usar produtoId; seed com 3 variantes iPhone 17 Pro Max
- **Quem decidiu:** Cursor agente + usuário Gustavo

---

### 02/07/2026 — zenpro — Arte separada (foto/texto) + junta no pedido e tema preto+dourado

- **Decisão:** salvarPersonalizacao gera 3 artes (combinada, so-foto, so-texto transparente) via exportCaseArt com flags incluirFoto/incluirTexto; URLs salvas na personalizacao e propagadas ao item do pedido (criarPedidoLoja) para dono e revendedor baixarem em PedidoItemPreview. Tema preto+dourado com tokens gold em globals.css e classes btn-gold/btn-ink. Selecao de texto virou moldura tracejada dourada (Rect) sem alterar a cor/contorno do texto final. Clip da foto com inset = borderWidth para nao vazar do modelo.
- **Motivo:** Dono/franqueado precisa dos arquivos de producao separados e juntos; identidade da marca e preto+dourado; cliente se confundia achando que o texto sairia com contorno azul da selecao; foto vazava do contorno da capa.
- **Alternativa rejeitada:** Salvar so a arte combinada; aplicar stroke direto no texto para indicar selecao
- **Impacto:** exportCaseArt.ts, salvarPersonalizacao.ts, uploadArteProducao.ts, CaseTextNode.tsx, CaseEditor/CasePreview clip, firestoreTypes/multitenant types, criarPedido(Loja).ts, PedidoItemPreview.tsx, globals.css, AdminShell e CTAs da loja
- **Quem decidiu:** Cursor + Gustavo

---

### 02/07/2026 — zenpro

- **Decisão:** Multitenant sob Next output:export: rota dinamica /[slug] de revendedor resolvida com casca generica (slug 'loja' pre-renderizado em /loja, /loja/carrinho, /loja/checkout, /loja/personalizar) + rewrites no Firebase Hosting ('/*/personalizar','/*/carrinho','/*/checkout','/*') apontando para os HTMLs da casca. O client descobre o slug real via usePathname (LojaLayoutClient), nao pelo param pre-renderizado. Assim revendedores novos (ex.: /leozao) funcionam sem redeploy. /zenpro redireciona para '/' (marca nao e revendedor).
- **Motivo:** output:export exige params conhecidos em build-time; resolvia o erro 'Page /[slug]/page is missing param in generateStaticParams'
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 02/07/2026 — zenpro

- **Decisão:** Duas features multitenant reutilizaveis: (1) 'Meus pedidos' do cliente — indice pessoal em usuarios/{uid}/pedidos (ponteiro gravado no checkout via criarPedidoLoja) + leitura do status ao vivo em lojas/{lojaId}/pedidos (rules: cliente le o proprio pedido por clienteUid). Status ganhou 'entregue' e 'cancelado'. (2) Reposicao de estoque revendedor->dono: colecao pedidos_reposicao/{id} (lojaId, revendedorUid, itens, total, status solicitado|aprovado|enviado|recebido|cancelado). Rules: revendedor cria/le/cancela o proprio; marca le tudo e muda status. Pagina /admin/reposicao serve os dois papeis.
- **Motivo:** Cliente precisa acompanhar pedidos; revendedor precisa abastecer a loja pedindo ao dono
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 02/07/2026 — zenpro — Dimensões do modelo definem aspecto da capa + molde por modelo na arte de produção

- **Decisão:** A proporção (aspecto) da capa passa a derivar de larguraPx×alturaPx do modelo em toda a pipeline: CaseEditor, CasePreview, PreviewCapaModal e exportCaseArt usam a MESMA base (getCaseLayout(280, larguraPx, alturaPx)), então molduraW=280 fixo e molduraH proporcional. As dimensões e o molde (maskUrl) são resolvidos em resolverVisualPersonalizacao (a partir de modelos/{id}) e persistidos na Personalizacao/config para que carrinho, checkout e admin reconstruam a mesma proporção sem o provider. Na arte de produção, o recorte usa o maskUrl do próprio modelo (Storage) via loadImageForCanvasExport (evita canvas taint); fallback = máscara iPhone.
- **Motivo:** Usuário pediu que a dimensão cadastrada mude visivelmente a capa e que o molde do modelo reflita na arte. Antes tudo usava aspecto iPhone fixo e máscara iPhone hardcoded.
- **Alternativa rejeitada:** Manter máscara iPhone fixa e só variar câmera; ou criar sistema completo de máscaras SVG geradas por modelo (maior custo).
- **Impacto:** personalizacaoVisual.ts (ResolvedPersonalizacaoVisual ganha larguraPx/alturaPx/maskUrl), personalizacaoContext.ts, CaseEditor.tsx, CasePreview(+Lazy).tsx, exportCaseArt.ts (opts larguraPx/alturaPx/maskUrl + loadMaskImage via loadImageForCanvasExport), PreviewCapaModal.tsx, personalizacao/types.ts + catalogo/types.ts + personalizacaoConfig.ts (persistência), salvarPersonalizacao.ts, PersonalizarEditor.tsx, CartItemPreview/CheckoutPageContent/PedidoItemPreview.
- **Quem decidiu:** Ambos

---

### 02/07/2026 — zenpro — Dimensões do modelo definem aspecto da capa + molde por modelo na arte de produção

- **Decisão:** A proporção (aspecto) da capa deriva de larguraPx×alturaPx do modelo em toda a pipeline: CaseEditor, CasePreview, PreviewCapaModal e exportCaseArt usam a MESMA base getCaseLayout(280, larguraPx, alturaPx) — molduraW=280 fixo e molduraH proporcional. Dimensões e molde (maskUrl) resolvidos em resolverVisualPersonalizacao (modelos/{id}) e persistidos na Personalizacao/config para carrinho/checkout/admin reconstruírem sem provider. Arte de produção recorta com maskUrl do modelo (Storage) via loadImageForCanvasExport (evita canvas taint); fallback máscara iPhone.
- **Motivo:** Usuário pediu que a dimensão cadastrada mude visivelmente a capa e que o molde reflita na arte; antes usava aspecto e máscara iPhone fixos.
- **Alternativa rejeitada:** Manter máscara iPhone fixa; ou gerar máscaras SVG por modelo (maior custo).
- **Impacto:** personalizacaoVisual.ts, personalizacaoContext.ts, CaseEditor.tsx, CasePreview(+Lazy).tsx, exportCaseArt.ts, PreviewCapaModal.tsx, personalizacao/types.ts, catalogo/types.ts, personalizacaoConfig.ts, salvarPersonalizacao.ts, PersonalizarEditor.tsx, CartItemPreview/CheckoutPageContent/PedidoItemPreview.
- **Quem decidiu:** Ambos

---

### 03/07/2026 — zenpro — Assistente 'Nova capinha personalizável' (1 passo) sem upload de máscara/overlay

- **Decisão:** Criado /admin/capinha-nova: um wizard único que cria Marca (se nova) + Modelo + Produto personalizável de uma vez. Usa DISPOSITIVOS_PRESETS (Galaxy S23, iPhone Pro, Pixel, etc.) que preenchem larguraPx/alturaPx + cameraPresetId + cor. NÃO exige upload de PNG de máscara/overlay (maskUrl/overlayUrl vazios): o editor renderiza pela caseFrame (retângulo arredondado) + preset de câmera; produção cai no fallback de máscara proporcional. Fluxo antigo (Modelos + Produtos separados) foi mantido intacto.
- **Motivo:** Lojista queria forma fácil e sem falhas de publicar uma capinha personalizável nova (ex.: Galaxy S23). O fluxo antigo em 2 telas com upload de PNGs era confuso e propenso a erro.
- **Alternativa rejeitada:** Manter só os formulários Modelos+Produtos; exigir PNG de máscara por modelo.
- **Impacto:** Novos: src/app/admin/(painel)/capinha-nova/{page,CapinhaNovaPageClient}.tsx, src/features/admin/catalogo/dispositivosPresets.ts. Alterados: AdminShell (link '+ Nova capinha', marca), ModelosAdminPageClient (guia aponta pro wizard). Reusa criarMarcaAdmin/criarModeloAdmin/criarProdutoCentral/subirImagemProduto.
- **Quem decidiu:** Ambos

---

### 03/07/2026 — zenpro — Assistente 'Nova capinha personalizável' (1 passo) sem upload de máscara/overlay

- **Decisão:** Criado /admin/capinha-nova: wizard único que cria Marca (se nova) + Modelo + Produto personalizável de uma vez. Usa DISPOSITIVOS_PRESETS (Galaxy S23, iPhone Pro, Pixel...) que preenchem larguraPx/alturaPx + cameraPresetId + cor. Não exige PNG de máscara/overlay: editor renderiza pela caseFrame (retângulo arredondado) + preset de câmera; produção usa fallback de máscara proporcional. Fluxo antigo (Modelos+Produtos) mantido.
- **Motivo:** Lojista queria forma fácil e sem falhas de publicar capinha personalizável nova; fluxo antigo em 2 telas com upload de PNGs confundia.
- **Alternativa rejeitada:** Manter só Modelos+Produtos; exigir PNG de máscara por modelo.
- **Impacto:** Novos: capinha-nova/{page,CapinhaNovaPageClient}.tsx, dispositivosPresets.ts. Alterados: AdminShell (link '+ Nova capinha'), ModelosAdminPageClient (guia). Reusa criarMarcaAdmin/criarModeloAdmin/criarProdutoCentral/subirImagemProduto.
- **Quem decidiu:** Ambos

---

### 03/07/2026 — zenpro — Assistente 'Nova capinha personalizavel' (1 passo) sem upload de mascara/overlay

- **Decisão:** Criado /admin/capinha-nova: wizard unico que cria Marca (se nova) + Modelo + Produto personalizavel de uma vez. Usa DISPOSITIVOS_PRESETS (Galaxy S23, iPhone Pro, Pixel...) que preenchem larguraPx/alturaPx + cameraPresetId + cor. Nao exige PNG de mascara/overlay: editor renderiza pela caseFrame (retangulo arredondado) + preset de camera; producao usa fallback de mascara proporcional. Fluxo antigo (Modelos+Produtos) mantido.
- **Motivo:** Lojista queria forma facil e sem falhas de publicar capinha personalizavel nova; fluxo antigo em 2 telas com upload de PNGs confundia.
- **Alternativa rejeitada:** Manter so Modelos+Produtos; exigir PNG de mascara por modelo.
- **Impacto:** Novos: capinha-nova/{page,CapinhaNovaPageClient}.tsx, dispositivosPresets.ts. Alterados: AdminShell, ModelosAdminPageClient. Reusa criarMarcaAdmin/criarModeloAdmin/criarProdutoCentral/subirImagemProduto.
- **Quem decidiu:** Ambos

---

### 03/07/2026 — zenpro — Assistente 'Nova capinha personalizavel' (1 passo) sem upload de mascara/overlay

- **Decisão:** Criado /admin/capinha-nova: wizard unico que cria Marca (se nova) + Modelo + Produto personalizavel de uma vez. Usa DISPOSITIVOS_PRESETS (Galaxy S23, iPhone Pro, Pixel...) que preenchem larguraPx/alturaPx + cameraPresetId + cor. Nao exige PNG de mascara/overlay: editor renderiza pela caseFrame (retangulo arredondado) + preset de camera; producao usa fallback de mascara proporcional. Fluxo antigo (Modelos+Produtos) mantido.
- **Motivo:** Lojista queria forma facil e sem falhas de publicar capinha personalizavel nova; fluxo antigo em 2 telas com upload de PNGs confundia.
- **Alternativa rejeitada:** Manter so Modelos+Produtos; exigir PNG de mascara por modelo.
- **Impacto:** Novos: capinha-nova/{page,CapinhaNovaPageClient}.tsx, dispositivosPresets.ts. Alterados: AdminShell, ModelosAdminPageClient.
- **Quem decidiu:** Ambos

---

### 03/07/2026 — cortejo — Templates WhatsApp salon-local + durationMin por agendamento

- **Decisão:** Mensagens pré-definidas por salão em subcoleção messageTemplates com variáveis {{nome}}, {{servico}}, {{data}}, etc. Envio via abrirWhatsApp (wa.me) com SendClientMessageSheet — pré-definida ou manual. Duração por agendamento: campo durationMin opcional no appointment, UI no novo agendamento com chips 30–120 min.
- **Motivo:** Usuário pediu templates personalizáveis e duração específica por horário agendado.
- **Alternativa rejeitada:** N/A
- **Impacto:** app/config/mensagens.tsx, components/mensagens/, services/messageTemplates.ts, agendamento/[id].tsx, firestore.rules
- **Quem decidiu:** Ambos

---

### 03/07/2026 — lashmatch — Templates WhatsApp + duração custom agendamento LashMatch

- **Decisão:** Port Cortejo messageTemplates (Firestore artifacts/{appId}/users/{uid}/messageTemplates) + SendClientMessageSheet + duracaoMinutos override no modal agendamentos. Link {{link}} via getUrlAgendarPublico(uid).
- **Motivo:** Paridade Cortejo — mensagens pré-definidas WhatsApp e duração por agendamento.
- **Alternativa rejeitada:** N/A
- **Impacto:** LashMatch: types/messageTemplate, services/messageTemplates, utils/messageTemplateVars, components/mensagens, app/config/mensagens, aniversariantes, clientes, agendamentos
- **Quem decidiu:** Ambos

---

### 03/07/2026 — cortejo — Agenda: botão expandir/contrair lista de agendamentos do dia

- **Decisão:** Adicionado toggle dayExpanded na aba Agenda (Cortejo app/(tabs)/index.tsx e LashMatch app/(tabs)/agendamentos.tsx). Quando expandido, oculta o AgendaCalendar (condicional !dayExpanded) e o dayPanel (flex:1) cresce mostrando só a DayScheduleList do dia selecionado. Ícone Ionicons expand-outline/contract-outline no dayBar.
- **Motivo:** Usuário queria ver os horários agendados do dia em tela cheia, sem precisar manter o calendário ocupando espaço.
- **Alternativa rejeitada:** Rota separada só para lista do dia — desnecessário; toggle reaproveita layout e estado existentes.
- **Impacto:** Cortejo e LashMatch — aba Agenda; padrão de UX reutilizável para apps de salão
- **Quem decidiu:** usuário + agente

---

### 03/07/2026 — cortejo — Templates WhatsApp por WABA: provisionar na conexao + fallback compartilhado

- **Decisão:** Ao conectar numero proprio (Embedded Signup) provisionar os templates de agendamento na WABA do salao via provisionSalonWhatsAppTemplates(wabaId). No envio, se o template ainda nao existir/aprovado na WABA propria (132001), cair para o numero compartilhado da plataforma e disparar o provisionamento (auto-heal). Mensagens pre-definidas (defaultMessageTemplates) deixaram de sugerir link/'agende seu horario' por padrao.
- **Motivo:** Templates WhatsApp sao escopados por WABA. Enviar pelo numero proprio exige o template aprovado naquela WABA; sem isso a confirmacao/lembrete falhava (132001). Fallback garante entrega enquanto a Meta aprova; provisionamento automatico faz os proximos envios saírem do numero proprio.
- **Alternativa rejeitada:** Enviar texto livre pelo numero proprio (so funciona na janela 24h; confirmacao e business-initiated). Exigir criacao manual de templates por salao (fricção e recorrência do bug).
- **Impacto:** Cortejo e LashMatch: functions/SRC/whatsapp.ts (fallback + provisionSalonWhatsAppTemplates + retorno EnvioAgendamentoResult), whatsappTemplates.ts (Cortejo), embeddedSignup.ts (provisiona + secret WHATSAPP_TOKEN), index.ts (dispara provisionamento em confirmacao/lembretes). constants/defaultMessageTemplates.ts (remocao dos links).
- **Quem decidiu:** Ambos

---

### 03/07/2026 — cortejo — WhatsApp Embedded Signup: health check coexistence + retorno web ao app + guia de onboarding

- **Decisão:** 1) whatsappHealthCheck (assessMetaPhoneHealth): em coexistence NÃO desconectar por code_verification_status EXPIRED/NOT_VERIFIED nem por platform_type != CLOUD_API — só desconectar por quality RED ou is_on_biz_app === false. 2) Página web public/embedded-signup/index.html: após completeEmbeddedSignupWeb, mostrar tela de sucesso clara com botão 'Voltar para o app' + auto-retorno (deep link/URL) em vez de só redirecionar. 3) services/embeddedSignup.ts (app): em WebBrowser cancel/dismiss, reconferir status real no Firestore (waitSalonWhatsAppLive/waitUsuarioWhatsAppLive, 3 tentativas) antes de dizer 'Conexão cancelada' — corrige falso negativo. 4) WhatsAppConnectGuide: guia prático para quem já tem e quem não tem WhatsApp Business (baixar app Business, mesmo número, migração), passos Meta e dica do campo Site (Instagram/link/site). Espelhado no LashMatch (que não tem health check em functions).
- **Motivo:** Números coexistence eram desconectados por falso positivo do Graph; usuário reportava página web presa em 'conectando...' sem voltar ao app e falso 'conexão cancelada'; faltava orientação de onboarding para número próprio.
- **Alternativa rejeitada:** Confiar só no deep link automático (falhava em browser web); manter downgrade por code_verification_status em coexistence.
- **Impacto:** cortejo + LashMatch: functions/SRC/whatsappStatus.ts (só cortejo), services/embeddedSignup.ts, public/embedded-signup/index.html, components/whatsapp/WhatsAppConnectGuide.tsx. Deploy: cortejo functions:whatsappHealthCheck + hosting; lashmatch hosting.
- **Quem decidiu:** Gustavo

---

### 03/07/2026 — cortejo — WhatsApp Embedded Signup: health check coexistence + retorno web ao app + guia onboarding

- **Decisão:** 1) assessMetaPhoneHealth: em coexistence só desconecta por quality RED ou is_on_biz_app===false (ignora code_verification_status e platform_type). 2) public/embedded-signup/index.html: tela de sucesso com botão 'Voltar para o app' + auto-retorno. 3) services/embeddedSignup.ts: no cancel/dismiss reconfere status live no Firestore (3 tentativas) antes de erro 'Conexão cancelada'. 4) WhatsAppConnectGuide: onboarding prático (tem/não tem Business, baixar app, campo Site com Instagram). Espelhado LashMatch.
- **Motivo:** Falso positivo desconectava números coexistence; web presa em 'conectando'; falso 'conexão cancelada'; faltava onboarding.
- **Alternativa rejeitada:** N/A
- **Impacto:** Deploy cortejo functions:whatsappHealthCheck+hosting; lashmatch hosting.
- **Quem decidiu:** Gustavo

---

### 04/07/2026 — zenpro — Layout automático multi-foto capinha

- **Decisão:** Presets de layout por quantidade (1=página inteira, 2=empilhado vertical, 3=2+1, 4=grade 2x2) em fotoLayoutPresets.ts; auto-aplica ao mudar contagem; botão Reorganizar fotos; cada FotoLayer usa areaSlot própria para fit/clamp.
- **Motivo:** Cliente pediu arranjo automático ao adicionar várias fotos em vez de empilhar todas sobrepostas.
- **Alternativa rejeitada:** N/A
- **Impacto:** PersonalizarEditor + CaseEditor; export usa transforms absolutos já calculados por slot.
- **Quem decidiu:** Ambos

---

### 05/07/2026 — cortejo — Despesas recorrentes canal e categorias custom financeiro

- **Decisão:** Despesas com recorrencia (nenhuma/semanal/quinzenal/mensal/trimestral/anual), canal (presencial/online), categorias custom em financeCategories (Firestore), filtros no relatorio/lista. Cortejo: financeEntries + financeCategories em salons/{salonId}. LashMatch: despesas + financeCategories em users/{uid}. Tipo fixa/variavel mantido no LashMatch.
- **Motivo:** Donas precisam marcar gastos recorrentes, online vs fisico, criar categorias proprias e filtrar relatorio.
- **Alternativa rejeitada:** N/A
- **Impacto:** Cortejo e LashMatch — constants/financeExpense.ts, services/financeCategories.ts, telas financeiro/relatorio. Deploy rules+hosting+eas update preview.
- **Quem decidiu:** Ambos

---

### 06/07/2026 — cortejo — Coexistência WhatsApp: envio via número compartilhado até entrega própria verificada

- **Decisão:** resolveSender ignora own quando coexistence=true e ownDeliveryVerified!=true; effectiveSender inicia shared no embedded signup; webhook delivered promove own
- **Motivo:** API Meta aceita POST pelo número próprio mas mensagem não chega ao destinatário; número Cortejo entrega normalmente
- **Alternativa rejeitada:** Manter sender own e esperar só templates — templates já aprovados e entrega ainda falha
- **Impacto:** functions/SRC/whatsappSender.ts, embeddedSignup.ts, metaWhatsappWebhook.ts, whatsappHealthCheck.ts
- **Quem decidiu:** Agente + usuário (teste A/B)

---

### 06/07/2026 — cortejo — WhatsApp Meta 131042 billing currency — diagnóstico webhook + UI

- **Decisão:** Erro 131042 (moeda WABA não configurada) não desconecta o salão; webhook persiste billingCurrencyRequired + lastDeliveryError + effectiveSender shared; UI mostra botão Resolver na Meta; resolveSender força shared até billing corrigido e delivered limpa flags.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 06/07/2026 — cortejo — WhatsApp UI live+shared + modelo planos mensagens

- **Decisão:** UI WhatsApp: status live + effectiveSender shared mostra 'WhatsApp vinculado' + botão faturamento Meta; não esconde conexão como 'número plataforma'. Produto: Pro inclui msgs pelo número Cortejo; número próprio opt-in com billing Meta do salão.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 06/07/2026 — cortejo — Planos WhatsApp platform vs own desconto R$30

- **Decisão:** Dois modos de assinatura Android: whatsappBillingMode platform (preço cheio, envio número Cortejo) vs own (−R$30, salão paga Meta, pode conectar número). MP inline com valor descontado no modo own.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 06/07/2026 — cortejo — Plano planowpp WhatsApp Próprio R$49,90

- **Decisão:** Revertido toggle platform/own com desconto R$30. Novo tier planowpp (Plano WhatsApp Próprio R$49,90): 4 planos originais inalterados com número Cortejo; planowpp permite conectar número próprio (Meta cobra salão). Copy leiga em WhatsAppProprioPlanExplainer.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 06/07/2026 — cortejo

- **Decisão:** Paywall WhatsApp em duas telas: (1) /config/plano-escolha pergunta Cortejo vs próprio com prós/contras; (2) /config/plano?estilo=cortejo|proprio mostra só os planos compatíveis (4 tiers ou planowpp). Assinantes bloqueados redirecionam para escolha primeiro.
- **Motivo:** UX solicitada pelo usuário — não misturar todos os planos numa tela só.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 06/07/2026 — cortejo — planowpp sem fallback Cortejo e msgs ilimitadas

- **Decisão:** Plano planowpp (WhatsApp Próprio): resolveSender nunca retorna shared — bloqueia com own_billing_required/own_not_connected/own_not_ready. Sem limite planMsgLimit=0 (Meta cobra por msg). Sem fallback template 132001 nem retry 131042 via número Cortejo. UI/copy deixa claro custo Meta ~R$0,10/msg.
- **Motivo:** Usuário: custo Meta é do salão; lembretes não devem sair pelo número Cortejo no plano próprio.
- **Alternativa rejeitada:** Fallback shared enquanto billing/templates não prontos (coexistência)
- **Impacto:** functions whatsappSender, whatsapp, whatsappConfirmacaoFallback, msgUsage; app planos + WhatsAppStatusCard
- **Quem decidiu:** usuário + agente

---

### 06/07/2026 — cortejo — planowpp copy Business BRL/USD e contato ajuda

- **Decisão:** Copy planowpp: obrigatório WhatsApp Business no celular (não comum); pagamento Meta BRL preferencial ou USD se Real indisponível; dúvidas → SUPPORT_PHONE_DISPLAY + SUPPORT_EMAIL (Ajuda). Atualizado em planoMarketing, WhatsAppConnectGuide, WhatsAppProprioPlanExplainer, planoWhatsappEscolha, whatsapp.tsx.
- **Motivo:** Pedido usuário: deixar claro requisitos Business, moeda e contato suporte.
- **Alternativa rejeitada:** N/A
- **Impacto:** UI app + web após export; functions já deployadas
- **Quem decidiu:** Ambos

---

### 06/07/2026 — lashmatch — deploy web + copy WhatsApp próprio LashMatch

- **Decisão:** LashMatch: copy planowpp/mensalProprio espelhada do Cortejo (Business obrigatório, BRL ou USD, sem limite app, contato suporte). Web export + hosting lashmatch-627fd. Cortejo web re-export + hosting cortejo-app.
- **Motivo:** Usuário pediu publicar web nos dois apps com mesmas regras de copy WhatsApp próprio.
- **Alternativa rejeitada:** N/A
- **Impacto:** https://cortejo-app.web.app e https://lashmatch-627fd.web.app
- **Quem decidiu:** Ambos

---

### 06/07/2026 — lashmatch

- **Decisão:** LashMatch WhatsApp Próprio: espelhado Embedded Signup Meta do Cortejo — tenant usuarios/{uid}, plano mensalProprio, CF embeddedSignup + metaWhatsappWebhook, tela /whatsapp, hosting /embedded-signup/
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 07/07/2026 — lashmatch — LashMatch WhatsApp próprio — template v5 no envio

- **Decisão:** LashMatch WhatsApp próprio — template v5 no envio
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 08/07/2026 — zenpro

- **Decisão:** Zen Pro — Mercado Pago checkout (loja B2C + reposição B2B), webhook confirma pagamento antes de envio/estoque, rastreio e NF (Focus NFe opcional + manual admin). Parcelamento até 12x com 2x sem juros via Checkout Pro.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 08/07/2026 — zenpro

- **Decisão:** Zen Pro estoque: loja oficial zenpro (MARCA_LOJA_ID) incluída no dropdown Admin/Estoque — marca vende na raiz e precisa alocar estoque em lojas/zenpro/estoque, não só revendedores. Estoque central continua em produtos.estoqueCentral.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 09/07/2026 — zenpro — CEP origem envio por tipo de pedido e loja

- **Decisão:** Personalizada sempre expede da Zen Pro (lojas/zenpro.config.expedicao). Produto pronto expede da loja do pedido (zenpro ou revendedor). CEP não é env var única — resolverOrigemExpedicaoPedido() lê config.expedicao da loja. Pedido misto centraliza na Zen Pro.
- **Motivo:** Regra de negócio do usuário: capinha personalizada é produzida na marca; pronta pode sair do estoque do revendedor ou do galpão Zen Pro conforme onde foi vendida.
- **Alternativa rejeitada:** MELHOR_ENVIO_CEP_ORIGEM fixo global para todos os pedidos
- **Impacto:** Melhor Envio futuro; admin cadastra expedicao em Revendedores e Estoque (loja oficial); aprovação de revendedor copia endereço da solicitação
- **Quem decidiu:** Usuário + agente

---

### 09/07/2026 — zenpro

- **Decisão:** Zen Pro MP: webhook aceita GET IPN (?topic=&id=) e merchant_order; callable sincronizarPagamentoMercadoPago busca payment por id ou external_reference; retorno checkout e botão Meus pedidos sincronizam status quando webhook falha.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 10/07/2026 — cortejo

- **Decisão:** Cortejo: corrigido falso positivo de assinatura — MP status pending não libera Pro; mpSync só vincula preapproval com external_reference do salonId; removido auto-sync ao abrir paywall; isSalonSubscriptionActive não usa mais plan=pro sozinho.
- **Motivo:** Usuário ia para home sem assinar — sync puxava preapproval antigo/pending do mesmo e-mail
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 10/07/2026 — lashmatch

- **Decisão:** LashMatch análise: seletor de modelo (Gatinho/Boneca/Esquilo), tom dos fios via tintColor, fotoComCiliosUrl também na web, mapa 6 combinações corrigidas + dual Boneca/Esquilo, textos curvatura e colorimetria marrons
- **Motivo:** Pedido da dona do app — trocar modelo após IA, preview marrom, histórico com cílios aplicados
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 11/07/2026 — lashmatch

- **Decisão:** LashMatch paridade planos Cortejo: PlanTierCard com msgs/mês e barra de uso (msgUsage no Firestore usuarios/{uid}); backend msgUsage.ts + incremento em envios pelo número LashMatch; MetaBillingHelpPanel (copiar link, desktop, suporte) em LashMatch e Cortejo; telefone suporte 19989631786 nos dois apps.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 14/07/2026 — zenpro — Preço revendedor + blur editor + IA sem camera + filtros admin

- **Decisão:** Campo precoRevendedorCentavos no produto (B2B reposição); fallback no precoBaseCentavos. CaseEditor com blur cover no fundo. Prompt IA vazio com placeholder; INSTRUCOES proíbem módulo/bump de câmera na arte. Filtros de busca em produtos/modelos/marcas.
- **Motivo:** Revendedor precisa preço atacado distinto do B2C; UX editor sem espaço em branco; IA não deve pintar câmera (overlay do app); listas admin precisavam filtro.
- **Alternativa rejeitada:** N/A
- **Impacto:** Reposicao usa precoReposicaoCentavos(); cadastro produto e Nova case pedem preço revendedor.
- **Quem decidiu:** Usuário + agente

---

### 14/07/2026 — zenpro — Filtros marca/modelo na seção Personalizar da loja

- **Decisão:** Seção Personalize com sua foto (home/loja) ganhou filtros de busca, marca e modelo para o comprador final. Catálogo personalizável enriquece marca/modelo a partir de marcas+modelos ativos.
- **Motivo:** Usuário pediu filtros na vitrine de capinhas personalizadas, não só no admin.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 14/07/2026 — zenpro — PIX Checkout Pro + prévia CasePreview alinhada

- **Decisão:** Checkout PIX: preference deixa de excluir cartão (só boleto) — excluir credit/debit escondia PIX no Checkout Pro. Prévia da case no editor passa a usar CasePreview (mesmo do carrinho); borda cyan trocada por stroke discreto.
- **Motivo:** Usuário sem opção PIX no MP e prévia com borda/câmera desalinhadas.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 14/07/2026 — zenpro — borda dual CASE_BORDER + trocar foto substitui ativa

- **Decisão:** Borda do mockup em 2 strokes (outer claro + inner escuro) via CASE_BORDER em caseVisualConstants, usada em CaseEditor/CasePreview/caseFrame. Botão Trocar foto usa substituir:"ativa" (revoga blob da foto alvo); Adicionar foto empilha até MAX. Evitar substituir:false no Trocar (empilhava fotos).
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 14/07/2026 — zenpro — Preço revendedor obrigatório com faixas e pedido mínimo no admin

- **Decisão:** ProdutoFormPageClient e CapinhaNovaPageClient exigem precoRevendedorCentavos (number), pedidoMinimoRevendedorCentavos (0 se vazio) e faixasPrecoRevendedor validadas (faixasDraftParaDocs + validarFaixasPrecoRevendedor) no submit e na criação via upload de imagem.
- **Motivo:** B2B/reposição precisa de preço atacado e faixas por quantidade; fallback 'vazio = preço loja' não atende mais o contrato ProdutoFormInput.
- **Alternativa rejeitada:** Manter preço revendedor opcional com fallback ao preço B2C
- **Impacto:** Forms admin bloqueiam salvar/publicar sem preço e faixas válidas; payload alinhado a produtoCentralService
- **Quem decidiu:** Usuário + agente

---

### 14/07/2026 — zenpro — Portal B2B único /revendedor + faixas de preço + preview clip

- **Decisão:** Site atacado único em /revendedor (sem slug por loja), gated por papel revendedor. Pedidos via fluxo normal em lojas/zenpro/pedidos com canal=revendedor_b2b. Produto exige precoRevendedorCentavos + faixasPrecoRevendedor[] + pedidoMinimoRevendedorCentavos. CasePreview clipa foto na moldura (clipRoundRect).
- **Motivo:** Revendedores compram com preços/faixas no mesmo UX do cliente; clientes finais no site comum.
- **Alternativa rejeitada:** Slug B2B por loja ou só reposição admin
- **Impacto:** Novas rotas /revendedor/*; forms admin; carrinho com quantidade; rewrites hosting
- **Quem decidiu:** Usuario + agente

---

### 14/07/2026 — zenpro — Revendedor: sem Minha loja nem Pedir reposição no admin

- **Decisão:** Nav do revendedor remove Minha loja e Pedir reposição; compra no /revendedor com preços/faixas B2B. Admin marca mantém Reposição. Guard bloqueia /admin/reposicao e /admin/lojas/{id} para revendedor.
- **Motivo:** Pedido do usuário — fluxo único no site atacado
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 14/07/2026 — zenpro — Níveis revendedor Ouro/Prata/Bronze configuráveis

- **Decisão:** Níveis Ouro/Prata/Bronze dos revendedores: marca edita ouroMinCentavos e prataMinCentavos em lojas/zenpro.config.niveisRevendedor (UI em /admin/revendedores). Volume = compras faturadas na Zen Pro (pedidos lojas/zenpro do clienteUid + pedidos_reposicao). Bronze = abaixo de Prata.
- **Motivo:** Dono Zen Pro quer ranking/níveis configuráveis conforme volume
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 14/07/2026 — zenpro — Benefícios + métricas de níveis revendedor

- **Decisão:** Níveis revendedor: benefícios por nível (desconto%, freteGratis, chanceSorteio, texto); métricas mês/ano/total + ranking no admin; card nível/benefícios no dashboard admin e portal /revendedor; emailContatoZenPro no config da marca.
- **Motivo:** Pedido do usuário — métricas, benefícios e visibilidade para o revendedor
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 14/07/2026 — zenpro

- **Decisão:** StoreHeader: EntrarComoRevendedorLink no lugar do hard link /revendedor; Painel admin gated por podeAcessarPortalRevendedor (revendedor/marca) no site comum e no B2B; no portal isB2b mostra Site comum + Painel admin.
- **Motivo:** Link inteligente redireciona login/aviso conforme papel; painel admin so aparece para quem pode acessar o portal.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 14/07/2026 — zenpro — Fix acesso /revendedor + ranking mês/vendedor + benefícios no checkout B2B

- **Decisão:** Corrigir race de papel (papelResolvido + Guard sem bounce para aviso). EntrarComoRevendedorLink sempre vai a /revendedor se logado. Admin button via podeAcessarPortalRevendedor. Ranking admin com month picker e filtro vendedor. Checkout/carrinho B2B aplica desconto do nível (useBeneficiosCheckoutB2b) e grava beneficioNivel no pedido.
- **Motivo:** Usuário reportou loop em ?aviso=somente-revendedor; pediu filtros de ranking e aplicação de benefícios na compra.
- **Alternativa rejeitada:** N/A
- **Impacto:** Hosted em zenpro-capinhas.web.app. Contas sem papel revendedor ainda bloqueadas no Guard, sem redirect enganoso.
- **Quem decidiu:** Usuario + agente

---

### 14/07/2026 — zenpro — Fix acesso /revendedor + ranking mês/vendedor + beneficios checkout B2B

- **Decisão:** Corrigir race de papel (papelResolvido + Guard sem bounce para aviso). EntrarComoRevendedorLink sempre vai a /revendedor se logado. Admin button via podeAcessarPortalRevendedor. Ranking admin com month picker e filtro vendedor. Checkout/carrinho B2B aplica desconto do nível e grava beneficioNivel no pedido.
- **Motivo:** Loop em ?aviso=somente-revendedor; filtros ranking e beneficios na compra.
- **Alternativa rejeitada:** N/A
- **Impacto:** Deploy hosting zenpro-capinhas.web.app. Contas sem papel ainda bloqueadas no Guard.
- **Quem decidiu:** Usuario + agente

---

### 14/07/2026 — zenpro — MP secrets + Melhor Envio cotação + diagnóstico Chroma HNSW

- **Decisão:** MP_ACCESS_TOKEN atualizado (secret v2) + MELHOR_ENVIO_TOKEN. Function calcularFreteMelhorEnvio + campos peso/dimensões no produto + FreteCheckoutSection. Chroma HNSW corrompido (Error loading hnsw index) — causa do RAG offline/vazio; nao e so servidor parado.
- **Motivo:** Credenciais novas MP/ME + cotacao frete no checkout.
- **Alternativa rejeitada:** N/A
- **Impacto:** Deploy functions+hosting zenpro-capinhas. Frete exige CEP expedicao no admin. RAG precisa reset .chroma_db + reindex.
- **Quem decidiu:** Usuario + agente

---

### 15/07/2026 — zenpro — Checkout Pro MP — sem juros e botão Pagar

- **Decisão:** Parcelas sem juros vêm do painel Mercado Pago (Oferecer parcelamento sem juros), não só do código. Preference Zen Pro define installments/default_installments, alinha itens ao totalCentavos e statement_descriptor ZENPRO. Botão Pagar cinza: não testar pagamento com a mesma conta vendedor.
- **Motivo:** Usuário viu 2x com juros e Pagar desabilitado no Checkout Pro apesar do site anunciar 2x sem juros.
- **Alternativa rejeitada:** N/A
- **Impacto:** Configuração obrigatória no painel MP; testes de pagamento com segunda conta.
- **Quem decidiu:** agente+usuario

---

### 15/07/2026 — zenpro — Etiqueta Melhor Envio automática sem coleta

- **Decisão:** Após pagamento aprovado, enfileira envios_outbox → cart/checkout/generate no Melhor Envio. Modo postagem em agência (meAgencyName); nunca solicita coleta — dono leva o pacote. Admin pode reprocessar via reprocessarEnvioMelhorEnvio.
- **Motivo:** Usuário quer rastreio automático sem retirada ME.
- **Alternativa rejeitada:** N/A
- **Impacto:** Exige saldo ME, CNPJ remetente (FOCUS_NFE_CNPJ_EMITENTE), telefone remetente e expedição cadastrada.
- **Quem decidiu:** usuario+agente

---

### 15/07/2026 — zenpro — Copy prazo frete: após fabricado/postado

- **Decisão:** Checkout e Meus pedidos mostram que dias úteis do frete só contam após postagem; personalizada = após fabricado e postado.
- **Motivo:** Pedido explícito do usuário para alinhar expectativa de prazo.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** usuario

---

### 15/07/2026 — zenpro — Preference MP com items.description

- **Decisão:** Preferência Checkout Pro envia items.description + category_id em todos os itens (produto e frete) para melhorar score de aprovação do painel MP.
- **Motivo:** Painel Aprovação dos pagamentos pediu items.description.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** usuario+agente

---

### 15/07/2026 — zenpro — E-mails de status do pedido + erro ME stale

- **Decisão:** notificarClientePedidoAtualizado envia e-mail em pagamento aprovado, rastreio gerado, enviado e entregue via emails_outbox. Erro Melhor Envio de saldo insuficiente não sobrescreve pedido com etiqueta; UI esconde erro stale.
- **Motivo:** Usuário pediu avisos por e-mail e viu erro vermelho com rastreio já gerado.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** usuario+agente

---

### 15/07/2026 — sinaflor — Gestão — listagem exige órgão preenchido como no filtro personalizar

- **Decisão:** CG/AF e GO usam INNER JOIN dadosGerais + unidadeIbama e descricaoUnidadeIbama preenchidos (mesma base do personalizar por órgão). Listagem hidrata dadosGerais no resultado para o nome não vir N/A. Analista/GA continuam só por atribuição (RN10/RN14).
- **Motivo:** Usuário validou que filtrar um órgão no personalizar retorna só processos daquele órgão; esperava a mesma exclusão de N/A na listagem sem filtro.
- **Alternativa rejeitada:** Só filtrar unidadeIbama IS NOT NULL sem hidratar dadosGerais — continuava N/A na coluna.
- **Impacto:** LicenciamentoQueryService.findGestaoByCriteria — filtro e preencherOrgaoAmbientalNosResultados
- **Quem decidiu:** Usuário + agente

---

### 15/07/2026 — zenpro — Resend configurado usezenpro.com.br

- **Decisão:** E-mails via Resend: EMAIL_FROM=contato@usezenpro.com.br, EMAIL_REPLY_TO=contato.zenpro@icloud.com. Domínio usezenpro.com.br precisa estar Verified no Resend.
- **Motivo:** Usuário forneceu API key e domínio para disparar emails_outbox.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** usuario

---

### 15/07/2026 — zenpro — Email aguardando pagamento por forma

- **Decisão:** E-mail aguardando pagamento ao gravar checkoutUrl: copy PIX (minutos), boleto (1–3 dias úteis), cartão (na hora). Forma salva no pedido no create.
- **Motivo:** Usuário pediu aviso de aguardo sem confundir prazos PIX vs boleto.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** usuario

---

### 15/07/2026 — zenpro — Domínio customizado usezenpro.com.br no Hosting

- **Decisão:** Site oficial em https://usezenpro.com.br (Firebase Hosting + DNS A 199.36.158.100). SITE_URL / NEXT_PUBLIC_SITE_URL e defaults MP/e-mail/ME apontam para o domínio; zenpro-capinhas.web.app continua como alias do mesmo site. Auth authorized domains e Storage CORS devem incluir usezenpro.com.br.
- **Motivo:** Marca e retorno Mercado Pago / links de e-mail no domínio próprio verificado no Resend.
- **Alternativa rejeitada:** N/A
- **Impacto:** Deploy hosting + functions checkout/e-mail/envio; .env.local e functions/.env; storage.cors.json atualizado (aplicar com gsutil).
- **Quem decidiu:** Usuario + agente

---

### 16/07/2026 — zenpro — Quantidade no carrinho B2C (pronta e personalizada)

- **Decisão:** B2C pode escolher quantidade no catálogo (produto pronto), no editor de personalização e alterar no carrinho via QuantityStepper (+/−). Mesmo produto pronto no carrinho soma quantidade; personalizada aceita qty no add. Checkout mostra unitário × qtd.
- **Motivo:** Cliente pedia qty em personalizado e normal; antes só B2B tinha input.
- **Alternativa rejeitada:** N/A
- **Impacto:** CatalogProductCard, PersonalizarEditor, CarrinhoPageContent, CarrinhoProvider, CheckoutPageContent, QuantityStepper
- **Quem decidiu:** Usuario + agente

---

### 16/07/2026 — sinaflor — Gestão — combo todos órgãos SCA e filtro por unidade ou idOrgao

- **Decisão:** Gestão: combo CG/AF lista todos órgãos SCA; filtro por órgão casa unidadeIbama OU idOrgaoAmbiental; listagem exige apenas um dos IDs preenchidos.
- **Motivo:** Usuário: filtrar órgão que aparece na lista não retornava; combo deve trazer todos os órgãos
- **Alternativa rejeitada:** Combo só com órgãos que têm licenciamento + filtro só por unidadeIbama com exigência de descrição
- **Impacto:** PainelGestaoLicPersonalizacaoService.listarOrgaosAmbientaisDisponiveis e LicenciamentoQueryService filtros de órgão — só gestão
- **Quem decidiu:** Usuário + agente

---

### 16/07/2026 — zenpro — Melhor Envio — novas credenciais Zen Pro

- **Decisão:** Conta Melhor Envio Zen Pro: MELHOR_ENVIO_TOKEN atualizado (secret v2) + Client ID/Secret guardados no Secret Manager (não no Git). Functions de frete/etiqueta redeployadas. Runtime usa só o Bearer token; Client ID/Secret ficam para refresh OAuth futuro.
- **Motivo:** Usuário trocou app/credenciais ME (Client ID 27166).
- **Alternativa rejeitada:** N/A
- **Impacto:** calcularFreteMelhorEnvio, processarEnvioOutbox, reprocessarEnvioMelhorEnvio
- **Quem decidiu:** Usuario + agente

---

### 16/07/2026 — zenpro — Download real de arte no pedido admin

- **Decisão:** Admin pedido: botões de arte/foto usam baixarUrlComoArquivo (fetch+blob) em vez de <a download target=_blank>, que no Storage só abria nova aba. Fallback com response-content-disposition se CORS falhar.
- **Motivo:** Dono pedia download real da arte no detalhe do pedido.
- **Alternativa rejeitada:** N/A
- **Impacto:** PedidoItemPreview.tsx, src/lib/baixarArquivo.ts
- **Quem decidiu:** Usuario + agente

---

### 16/07/2026 — zenpro — Download arte via Cloud Function (sem abrir aba)

- **Decisão:** Download de arte no admin via callable baixarArquivoStorage (proxy base64→blob). Removido fallback que abria URL do Storage em nova aba — response-content-disposition não força download no Firebase Storage.
- **Motivo:** Usuário clicava Baixar e a foto só abria na aba.
- **Alternativa rejeitada:** N/A
- **Impacto:** functions/baixarArquivoStorage.ts, src/lib/baixarArquivo.ts, PedidoItemPreview
- **Quem decidiu:** Usuario + agente

---

### 16/07/2026 — zenpro — Form revendedor sem loja/slug + excluir produto admin

- **Decisão:** Seja revendedor: removidos campos nome da loja e slug URL; slug gerado na aprovação a partir de razão social/CNPJ. Admin produtos: botão Excluir com confirmação (deleteDoc produtos).
- **Motivo:** Portal B2B único em /revendedor; usuário não escolhe mais URL da loja. Pediu excluir produto no admin.
- **Alternativa rejeitada:** N/A
- **Impacto:** SejaRevendedorPageClient, solicitacaoRevendedorService, solicitacaoRevendedorAdminService, ProdutosAdminPageClient, produtoCentralService
- **Quem decidiu:** Usuario + agente

---

### 17/07/2026 — sinaflor — Gestão de Licenciamento movida para Lic. Exploração

- **Decisão:** Mover o item Gestão de Licenciamento de Exploração (Projetos) do grupo Administração para o grupo Lic. Exploração, junto de Meus Licenciamentos, preservando rota e roles próprias. Atualizar breadcrumb.
- **Motivo:** Organizar a funcionalidade junto ao fluxo de licenciamentos solicitado pelo usuário.
- **Alternativa rejeitada:** N/A
- **Impacto:** Somente menu e breadcrumb do frontend.
- **Quem decidiu:** Usuário

---

### 18/07/2026 — sinaflor

- **Decisão:** HU130 backend: domínio próprio de tramitação de licenciamento (TB_TRAMITE_LIC + catálogos por CD_*, destinatários, anexos, rascunho). Status Em Análise (id=2). Analista vê por destinatário ativo; GO respeita FL_MANTER_ABERTO_UNIDADE. Scripts em SPRINT_19.
- **Motivo:** Implementar HU130 sem acoplar ao tb_situacao_auto de Autorizações, alinhado à Revisão 2 do documento de arquitetura.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 18/07/2026 — sinaflor

- **Decisão:** HU130 listar analistas via SCA2 GET api/unidadeibama/pessoa-orgao?idUnidadeIbama= (unidadeIbama ou idOrgaoAmbiental do processo). Login = CPF ou CNPJ.
- **Motivo:** Usuário forneceu a API oficial do SCA2 que retorna pessoas do órgão.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 18/07/2026 — zenpro — Melhor Envio — app Zen pro Client ID 27245 + token v4

- **Decisão:** Credenciais Melhor Envio atualizadas no Secret Manager: MELHOR_ENVIO_TOKEN v4, MELHOR_ENVIO_CLIENT_ID=27245 (app "Zen pro"), MELHOR_ENVIO_CLIENT_SECRET v2. Redeploy de calcularFreteMelhorEnvio, processarEnvioOutbox e reprocessarEnvioMelhorEnvio para pegar o token novo.
- **Motivo:** Usuário gerou JWT e app OAuth novos no painel Melhor Envio
- **Alternativa rejeitada:** Manter token/app antigo (27166)
- **Impacto:** Cotação e etiquetas passam a usar a conta/app nova; Client ID/Secret só no Secret Manager (não no Git)
- **Quem decidiu:** Usuário

---

### 18/07/2026 — zenpro — Melhor Envio — token v5 válido (401 resolvido)

- **Decisão:** Token anterior (v4) retornava 401 em /api/v2/me. Novo JWT validado com PROD=200; MELHOR_ENVIO_TOKEN atualizado para v5 e redeploy de calcularFreteMelhorEnvio, processarEnvioOutbox, reprocessarEnvioMelhorEnvio. Ambiente continua produção (não sandbox).
- **Motivo:** Usuário regenerou token no painel Melhor Envio após 401 Unauthenticated na etiqueta
- **Alternativa rejeitada:** Manter token v4 inválido
- **Impacto:** Cotação e geração de etiqueta voltam a autenticar na API ME produção
- **Quem decidiu:** Usuário + agente

---

### 18/07/2026 — zenpro — Parcelamento 1x sem juros + limite 3 IA/dia cliente

- **Decisão:** PARCELAMENTO_SEM_JUROS=1 (só à vista sem juros; 2x+ com juros MP). gerarFotoCriativaIA: clientes finais máx. 3 montagens/dia (contador usuarios/{uid}/uso_ia/{yyyy-mm-dd}); revendedor e marca sem teto.
- **Motivo:** Pedido do dono Zen Pro
- **Alternativa rejeitada:** Manter 2x sem juros e IA sem limite
- **Impacto:** Copy checkout atualizada; function gerarFotoCriativaIA redeployada com cota diária
- **Quem decidiu:** Usuário

---

### 18/07/2026 — zenpro — Performance — minInstances checkout/frete + parallel I/O

- **Decisão:** Performance confirmação: minInstances:1 em criarCheckoutMercadoPago e calcularFreteMelhorEnvio (anti cold start); Promise.all na validação de estoque do checkout e nas leituras de produtos do frete; export+upload de artes (combinada/foto/texto) em paralelo no salvarPersonalizacao.
- **Motivo:** Usuário reportou lentidão ao confirmar
- **Alternativa rejeitada:** minInstances em todas as functions; baixar resolução de arte sem medir
- **Impacto:** Checkout/frete mais responsivos; custo idle pequeno das 2 instances mínimas; confirmar personalização mais rápido com texto
- **Quem decidiu:** Usuário + agente

---

### 18/07/2026 — zenpro — Ranking revendedores — filtro semanal

- **Decisão:** Ranking admin de revendedores ganhou filtro Semana (ISO, segunda–domingo) com input type=week + rankingRevendedoresNoIntervalo.
- **Motivo:** Pedido do usuário
- **Alternativa rejeitada:** Só mês/ano/total
- **Impacto:** Admin → Revendedores → Métricas e ranking
- **Quem decidiu:** Usuário

---

### 18/07/2026 — zenpro — Dashboard revendedor + admin login seguro

- **Decisão:** Dashboard do revendedor mostra só nível/compras B2B + atalhos (sem métricas de pedidos da loja). Login /admin sem lista de contas seed. Admin marca: Auth contato.zenpro@icloud.com com papel marca; seed marca@zenpro.test rebaixado para cliente.
- **Motivo:** Revendedor não opera pedidos da loja; segurança do login; novo e-mail admin
- **Alternativa rejeitada:** Manter dashboard de pedidos B2C e contas seed na tela de login
- **Impacto:** Hosting + Auth/Firestore usuarios
- **Quem decidiu:** Usuário

---

### 18/07/2026 — zenpro — Auth — esqueci senha loja e admin

- **Decisão:** Redefinição de senha via sendPasswordResetEmail do Firebase Auth em /login (loja) e /admin/login, botão Esqueci a senha + componente BotaoEsqueciSenha. continueUrl volta para a respectiva tela de login.
- **Motivo:** Pedido do usuário
- **Alternativa rejeitada:** Reset só no console Firebase
- **Impacto:** Hosting; domínio precisa estar em Auth Authorized domains
- **Quem decidiu:** Usuário

---

### 18/07/2026 — LashMatch — Catálogo de cílios — thumbs menores e orientação dos PNGs

- **Decisão:** Quadrados do seletor de modelos na análise ficam compactos e uniformes (64x32). PNGs de variações que estavam invertidos vs clássicos (gatinho/boneca/esquilo) foram rotacionados 180° (jolie: 90°+180°) em assets/lashes.
- **Motivo:** Usuário reportou thumbs grandes demais e imagens de ponta-cabeça no seletor.
- **Alternativa rejeitada:** N/A
- **Impacto:** app/analysisResult.tsx + assets/lashes/*.png das variações
- **Quem decidiu:** Ambos

---

### 18/07/2026 — LashMatch — Cílios — moldura menor e arraste além da borda

- **Decisão:** Moldura rosa dos cílios: ratio 0.40 (antes 0.68), largura inicial ~22% da foto (antes 36%), clamp permite ~90% da moldura fora da borda da foto. Constantes em utils/lashStickerBounds.ts (nativo+web).
- **Motivo:** Usuário não conseguia arrastar o cílio além da borda; moldura grande restringia o clamp.
- **Alternativa rejeitada:** N/A
- **Impacto:** analysisResult.tsx, WebLashSticker.tsx, utils/lashStickerBounds.ts
- **Quem decidiu:** Ambos

---

### 18/07/2026 — LashMatch — Cílios — trim PNG + tamanho padrão na foto

- **Decisão:** PNGs de variações de cílios aparados (trim da transparência) para ocupar a moldura do catálogo e a mesma largura visual na foto. Largura inicial ~30% da foto. Thumb: scale 1.15 no cílio sem aumentar o quadrado.
- **Motivo:** Variações com canvas 2048/3000 pareciam minúsculas no seletor e na foto vs clássicos cropados.
- **Alternativa rejeitada:** N/A
- **Impacto:** assets/lashes/*, utils/lashStickerBounds.ts, analysisResult.tsx, lashImageAspect.ts
- **Quem decidiu:** Ambos

---

### 18/07/2026 — LashMatch — Cílios — moldura alinhada + tamanho inicial menor

- **Decisão:** Moldura rosa 0.92 (envolve o cílio após trim). Largura inicial na foto ~18%. Pinch com clamp 0.35–3.5x. Thumbs do catálogo inalterados.
- **Motivo:** Cílio saía do quadrado rosa na foto; tamanho inicial grande demais.
- **Alternativa rejeitada:** N/A
- **Impacto:** utils/lashStickerBounds.ts, analysisResult.tsx pinch
- **Quem decidiu:** Ambos

---

### 18/07/2026 — LashMatch — Cílios — moldura maior + orientação QA

- **Decisão:** Moldura rosa 1.28 + pad ~6%. Orientação PNG corrigida por QA: rot180 (laminado_boneca, wispy/fox/jolie/hyper gatinho); rot180+mirror (todos esquilo var, wispy_boneca, cisne, wispy_spikes).
- **Motivo:** Usuário: moldura pequena; maioria ponta-cabeça; alguns também espelhados na foto.
- **Alternativa rejeitada:** N/A
- **Impacto:** assets/lashes/*, lashStickerBounds.ts, analysisResult.tsx, WebLashSticker.tsx
- **Quem decidiu:** Ambos

---

### 18/07/2026 — LashMatch — Cílios — restaurar pinça e rotação com dedo

- **Decisão:** Gestos dos cílios: Pan maxPointers(1) para não bloquear pinça/rotação; área de toque mínima 148x96 incluindo moldura rosa.
- **Motivo:** Usuário não conseguia aumentar/diminuir/girar com o dedo.
- **Alternativa rejeitada:** N/A
- **Impacto:** app/analysisResult.tsx LashSticker
- **Quem decidiu:** Ambos

---

### 20/07/2026 — sinaflor — Importação CSV — mensagem clara para extensão inválida

- **Decisão:** Validar apenas nome terminando em .csv (não aceitar MIME application/vnd.ms-excel como CSV). Mensagem unificada: Tipo de arquivo inválido... CSV... Excel (.xls/.xlsx) não são aceitos. Aplicado em madeira tora, inventário CAI, volume total e outros produtos (front + back).
- **Motivo:** Excel salva CSV como .csv.xls ou .xls; MIME ms-excel fazia o front liberar e o usuário via erro genérico de ISO-8859-1.
- **Alternativa rejeitada:** Permitir extensão .xls parseando como CSV
- **Impacto:** Usuário com arquivo Excel/renomeado vê imediatamente que precisa CSV
- **Quem decidiu:** Usuario + agente

---

### 20/07/2026 — sinaflor — Importação CSV — mensagem clara extensão inválida

- **Decisão:** Validar apenas nome terminando em .csv. Mensagem unificada avisando que Excel .xls/.xlsx não são aceitos. Front + back em madeira tora, inventário CAI, volume total e outros produtos.
- **Motivo:** MIME ms-excel liberava .xls e erro caía em fallback ISO-8859-1
- **Alternativa rejeitada:** Permitir extensão .xls parseando como CSV
- **Impacto:** Usuário vê mensagem clara pedindo CSV
- **Quem decidiu:** Usuario + agente

---

### 20/07/2026 — sinaflor — Importação CSV mensagem extensão inválida

- **Decisão:** Validar apenas nome terminando em .csv (não aceitar MIME pplication/vnd.ms-excel como CSV). Mensagem unificada: *Tipo de arquivo inválido. O arquivo deve estar no formato CSV (.csv). Arquivos Excel (.xls ou .xlsx) não são aceitos.* Front + back: madeira tora, inventário CAI, volume total, outros produtos.
- **Motivo:** Excel gera .csv.xls/.xls; MIME liberava no front e o erro caía no fallback genérico de ISO-8859-1.
- **Alternativa rejeitada:** Permitir extensão .xls parseando como CSV.
- **Impacto:** Usuário vê imediatamente que precisa de CSV.
- **Quem decidiu:** Usuario + agente


### 20/07/2026 — sinaflor — Importação inventário CAI — aceitar UTF-8 e ISO-8859-1

- **Decisão:** ImportacaoArvoreInventarioCaiService alinhado à madeira tora: decodificar UTF-8 (com BOM) primeiro, fallback ISO-8859-1; limpar BOM/aspas no cabeçalho; IllegalStateException de layout vira BadRequestAlertException com a mensagem real.
- **Motivo:** Planilha padrão CAI está em UTF-8+BOM e o serviço lia só ISO-8859-1, gerando ï»¿NÂº Ãrvore
- **Alternativa rejeitada:** Manter só ISO-8859-1 e obrigar usuário a converter no Notepad++
- **Impacto:** Planilha padrão Windows UTF-8+BOM importa sem erro de cabeçalho
- **Quem decidiu:** Usuario + agente

---

### 20/07/2026 — LashMatch — Cílios — clássicos (ex-brasileiro) + laminado fio tecnológico + esquilo suave

- **Decisão:** PNGs brasileiro_* / Boneca_brasileiro substituem bases gatinho/boneca/esquilo (rótulo no app: clássico). laminado_boneca atualizado (label Laminado fio tecnológico). Novo esquilo_efeito_suave. Assets convertidos para RGB preto + alpha (padrão tint).
- **Motivo:** Usuário enviou assets e pediu trocar brasileiro por clássico e seguir padrão do app.
- **Alternativa rejeitada:** N/A
- **Impacto:** assets/lashes/{gatinho,boneca,esquilo,laminado_boneca,esquilo_efeito_suave}.png + lashStyleVariations.ts
- **Quem decidiu:** Ambos

---

### 20/07/2026 — LashMatch — Cílios clássicos — orientação e escurecimento

- **Decisão:** gatinho/boneca/esquilo clássicos: rot180 + alpha x3 (mais escuros). laminado_boneca: rot180 + flip horizontal.
- **Motivo:** QA usuário: ponta-cabeça e claros demais; laminado invertido.
- **Alternativa rejeitada:** N/A
- **Impacto:** assets/lashes/{gatinho,boneca,esquilo,laminado_boneca}.png
- **Quem decidiu:** Ambos

---

### 20/07/2026 — LashMatch — Ícone do app — redesign clean

- **Decisão:** Novo ícone app LashMatch: olho minimalista branco + 5 cílios rosa #D63384 em fundo preto, sem flame/estrelas. Fonte em assets/brand/icon-master-source.png; gerados icon/adaptive/splash/favicon via npm run generate:icons.
- **Motivo:** Usuário pediu ícone mais moderno e clean.
- **Alternativa rejeitada:** N/A
- **Impacto:** assets/brand/*, assets/images/{icon,adaptive-icon,splash-icon,favicon}.png
- **Quem decidiu:** Ambos

---

### 21/07/2026 — sinaflor — Gestão — padrão Meus Processos e Aguardando Distribuição

- **Decisão:** Gestão licenciamento: padrão Meus Processos + situação só Aguardando Distribuição; checkbox renomeado para Todos (inverso de meusProcessos); combo órgãos continua CG/AF=todos SCA e demais=unidades vinculadas.
- **Motivo:** Usuário pediu painel só aguardando distribuição, órgãos vinculados (exceto CG/AF), e padrão Meus Processos com check Todos
- **Alternativa rejeitada:** Manter checkbox Meus Processos e listar todas as situações por padrão
- **Impacto:** PainelGestaoLicPersonalizacaoService.configuracaoPadrao, personalizar-painel e gestao-licenciamento-exploracao
- **Quem decidiu:** Usuario + agente

---

### 22/07/2026 — lashmatch — PWA aditivo no Hosting sem impacto nativo

- **Decisão:** PWA no LashMatch web via public/manifest.webmanifest + public/sw.js sem cache + copy-pwa-assets.mjs no export:web + meta em app/+html.tsx. Apps iOS/Android e fluxos web existentes inalterados; SW só registra em HTTPS e não faz respondWith.
- **Motivo:** Usuário pediu instalar via link sem afetar o que já existe (loja + web atual).
- **Alternativa rejeitada:** Workbox/offline-first com cache agressivo; banner de install no app; PWA só por salão.
- **Impacto:** Hosting instalável; headers no-cache para sw/manifest; doc lashmatch-web-plataforma.md
- **Quem decidiu:** Ambos

---

### 22/07/2026 — lashmatch — Banner Instalar app PWA na web

- **Decisão:** PwaInstallPrompt na web: beforeinstallprompt + botão Instalar no Android; dica Safari no iOS; dismiss 7 dias; só Platform.OS web.
- **Motivo:** Usuário pediu opção explícita de instalar ao abrir o link no celular.
- **Alternativa rejeitada:** Só menu do Chrome sem UI própria
- **Impacto:** components/pwa/PwaInstallPrompt.tsx + app/_layout.tsx; nativo inalterado
- **Quem decidiu:** Ambos

---

### 22/07/2026 — lashmatch — Web mobile só via PWA instalado

- **Decisão:** Gate PwaMobileRequireInstall: celular no navegador bloqueado até PWA standalone; desktop e /agendar/termos liberados; nativo intacto.
- **Motivo:** Usuário: não usar web pelo celular sem instalar o app.
- **Alternativa rejeitada:** Banner dismissível permitindo uso no Chrome mobile
- **Impacto:** utils/pwaWeb.ts, components/pwa/PwaMobileRequireInstall.tsx, remove PwaInstallPrompt
- **Quem decidiu:** Ambos

---

### 22/07/2026 — lashmatch — PWA: instalar fix + features nativas

- **Decisão:** BIP cedo no +html; botão Instalar sempre + passos Chrome; SW com respondWith(fetch); PWA standalone libera análise/câmera/assistente e MP Android; remove .web.tsx blockers.
- **Motivo:** Botão não aparecia no Android; usuário quer testar PWA com features do nativo.
- **Alternativa rejeitada:** Manter .web.tsx bloqueando análise no PWA; botão só se BIP já no React
- **Impacto:** pwaWeb, PwaMobileRequireInstall, analysisPlatform, subscriptionPlatform, camera/analysisResult/assistente
- **Quem decidiu:** Ambos

---

### 22/07/2026 — lashmatch — uploadClientPhoto default unique + asProfile

- **Decisão:** uploadClientPhoto: default grava em .../analises/{ts}_{uuid}.jpg; profile.jpg só com asProfile:true (câmera). Histórico ignora URLs profile.jpg.
- **Motivo:** Sem asProfile, cliente antigo ou PWA cacheado ainda sobrescrevia profile.jpg e corrompia o histórico visual.
- **Alternativa rejeitada:** N/A
- **Impacto:** Análises novas no PWA/nativo ficam com foto individual; análises antigas com profile.jpg somem a foto do card (irrecuperáveis).
- **Quem decidiu:** Agente + usuário (bug report PWA)

---

### 22/07/2026 — lashmatch — PWA composite canvas cílios no histórico

- **Decisão:** No PWA, histórico salva foto+cílios via canvas (composeWebLashPhoto), não captureRef.
- **Motivo:** captureRef no web causava tela preta; skip deixava só a foto limpa.
- **Alternativa rejeitada:** N/A
- **Impacto:** Análises novas no PWA passam a gravar cílios no histórico; antigas sem cílios continuam como estão.
- **Quem decidiu:** Ambos

---

### 22/07/2026 — lashmatch — Landing /baixar Android PWA + iPhone App Store

- **Decisão:** Landing /baixar: Android = instalar PWA; iPhone = App Store id6782080036. Página estática public/baixar + rewrite Hosting + rota pública no gate.
- **Motivo:** Usuário pediu land page para divulgar com dois ícones (Android PWA / iPhone loja).
- **Alternativa rejeitada:** N/A
- **Impacto:** Link de divulgação https://lashmatch-627fd.web.app/baixar
- **Quem decidiu:** Ambos

---

### 22/07/2026 — lashmatch — Landing /baixar Android PWA + iPhone App Store

- **Decisão:** Landing /baixar: Android instala PWA; iPhone abre App Store id6782080036. Estática em public/baixar + rewrite Hosting.
- **Motivo:** Pedido do usuário para land page com dois ícones.
- **Alternativa rejeitada:** N/A
- **Impacto:** Divulgação em https://lashmatch-627fd.web.app/baixar
- **Quem decidiu:** Ambos

---

### 22/07/2026 — lashmatch — Domínio lashmatch.com.br no código e env

- **Decisão:** Domínio canônico https://lashmatch.com.br: atualizar EXPO_PUBLIC_PUBLIC_WEB_BASE_URL / AGENDAR / MP_TOKENIZE e EMBEDDED_SIGNUP_PUBLIC_BASE_URL. Manter authDomain *.firebaseapp.com. Auth authorized domains + Hosting SSL no console.
- **Motivo:** Usuário adicionou domínio customizado no Hosting e Auth.
- **Alternativa rejeitada:** N/A
- **Impacto:** Links públicos (agendar, baixar, tokenizar, MP back_url) passam a usar lashmatch.com.br; .web.app continua funcionando.
- **Quem decidiu:** Ambos

---

### 22/07/2026 — sinaflor — Tramitação — catálogo completo tipos e status

- **Decisão:** Catálogo completo de tipos de trâmite e status conforme matriz Paulo (14 trâmites). Códigos CD_TIPO_TRAMITE estáveis; status IDs 1–13. Script 09 incremental para bases que já rodaram 01/02 parciais. Enum TipoTramiteLicEnum e StatusLicEnum atualizados. VISTORIA legado mantido + VISTORIA_PROJETO novo.
- **Motivo:** Usuário pediu inserts dos tipos que faltavam além de Análise e Vistoria
- **Alternativa rejeitada:** N/A
- **Impacto:** SPRINT_19/01, 02, 09 + enums Java
- **Quem decidiu:** Usuario + agente

---

### 22/07/2026 — cortejo — Cortejo web: WhatsApp do salão na sidebar desktop

- **Decisão:** Cortejo web: WhatsApp do salão na sidebar desktop
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/07/2026 — sinaflor

- **Decisão:** 403 é Access Denied do @Secured: finalizar exige GERENTE_OPERACIONAL, GERENTE_AUTORIZADOR ou ANALISTA_TECNICO. CONSULTA_GERAL e ATUACAO_FEDERAL só leem. Não relaxar @Secured em produção; em login-automatico local incluir as roles de escrita da gestão de licenciamento.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 22/07/2026 — cortejo — Cortejo WhatsApp: Vincular cartão + aviso 24h no Conectado

- **Decisão:** Cortejo WhatsApp: Vincular cartão + aviso 24h no Conectado
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 22/07/2026 — cortejo — Confirmações e scroll de formulário na web

- **Decisão:** Na web, nunca usar Alert.alert com botões para confirmar ações; usar confirmAction/confirmDestructive. KeyboardAwareScrollView não usa KeyboardAvoidingView na web.
- **Motivo:** RN Web não exibe/aciona botões de Alert.alert de forma confiável; KeyboardAvoidingView height corta o formulário longo do agendamento.
- **Alternativa rejeitada:** N/A
- **Impacto:** Botão Confirmar e excluir agendamento passam a funcionar na web; formulário rola até o rodapé.
- **Quem decidiu:** Ambos

---

### 22/07/2026 — cortejo — Horário configurável dos lembretes WhatsApp

- **Decisão:** Lembretes WhatsApp passam a ser no dia civil (D-7 e D-1) no horário HH:mm do salão (lembrete7dHorario / lembrete1dHorario, padrão 08:00 BRT). Job */15. UI em Mais → Perfil. Confirmação continua imediata.
- **Motivo:** Pedido: 1 dia / 7 dias antes com horário configurável, não necessariamente 24h exatas.
- **Alternativa rejeitada:** N/A
- **Impacto:** Dona define horário dos lembretes sem mudar a confirmação; salões sem config mantêm 08:00.
- **Quem decidiu:** Ambos

---

### 23/07/2026 — cortejo — Instruções claras cartão Meta no app

- **Decisão:** Painel MetaBillingHelpPanel explica conta Meta correta, computador, erro 'conteúdo não disponível' e caminho manual business.facebook.com + botão Abrir Business Manager.
- **Motivo:** Cliente via link de cartão e recebia tela Meta inacessível sem entendimento no app.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/07/2026 — cortejo — WhatsApp setup: priorizar computador desde o início

- **Decisão:** Banner + alerta no celular pedem configurar WhatsApp/cartão Meta pelo Cortejo no computador desde a 1ª conexão; CTA copia link do painel web.
- **Motivo:** Meta falha fácil no celular; dona precisa ver isso antes de conectar.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/07/2026 — sinaflor

- **Decisão:** Gestão de licenciamento: default de situação do Analista Técnico = Em Análise do Projeto; opções do filtro carregam todas de TB_STATUS_LIC via GET /api/licenciamento/gestao/situacoes
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 23/07/2026 — cortejo+lashmatch — WhatsApp Meta setup só no computador

- **Decisão:** Bloquear Embedded Signup e abertura de links de faturamento Meta no celular (Platform.OS !== web). No app mobile: banner obrigatório + copiar link do painel web; botões Conectar/Resolver/Vincular cartão só no web. LashMatch alinhado ao Cortejo: botão Vincular cartão na Meta + MetaBillingHelpPanel quando número live conectado.
- **Motivo:** Meta (Embedded Signup e Business Manager) falha com frequência no celular (conteúdo não disponível / facebook.com/latest). Usuários tentavam configurar no telefone e travavam.
- **Alternativa rejeitada:** Alert com Continuar no celular (permitia fluxo frágil).
- **Impacto:** Cortejo e LashMatch: app/config/whatsapp, WhatsAppStatusCard, MetaBillingHelpPanel, constants/metaBilling.
- **Quem decidiu:** usuario+agente

---

### 23/07/2026 — cortejo — RevenueCat iOS public key fallback

- **Decisão:** Public SDK keys iOS embutidas como fallback no cliente: Cortejo appl_OnUgUlOyfRrnNAlDDsGUqBpDXXl; LashMatch appl_uwzKNjjesAzYZeKHGSgmEasYuLJ. app.config Cortejo sempre grava extra.REVENUECAT_API_KEY_IOS (nunca vazio).
- **Motivo:** OTA sem env apagava a chave e quebrava IAP no 2º open. Public key pode ficar no app.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/07/2026 — fabrica — Sync docs RAG jul/2026 Cortejo+LashMatch

- **Decisão:** Atualização factual jul/2026 nos docs RAG (sem reescrever canônico): arquitetura-fabrica-ia (seção apps + evolução), cortejo-project, lashmatch-project (novo), whatsapp-salao frontmatter, INDEX. Estrutura e headings antigos preservados.
- **Motivo:** Docs estavam desatualizados para RAG; usuário pediu só alinhar fatos no padrão RAG.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 24/07/2026 — sinaflor — Gestão — Meus Processos alinha situação Em Análise

- **Decisão:** Gestão licenciamento: Meus Processos (padrão) usa situação Em Análise do Projeto; Todos os Processos usa Aguardando Distribuição. Corrige lista vazia na Consulta Geral (atribuídos não ficam em Aguardando Distribuição). UI do checkbox com textos Meus/Todos claros.
- **Motivo:** Usuário CG: desmarcado Todos não trazia processos vinculados
- **Alternativa rejeitada:** Manter Meus Processos + Aguardando Distribuição
- **Impacto:** PainelGestaoLicPersonalizacaoService + front gestao-licenciamento-exploracao / personalizar
- **Quem decidiu:** Usuário + agente

---

### 24/07/2026 — sinaflor — Gestão — Meus/Todos sem forçar situação

- **Decisão:** Checkbox Todos os Processos controla só o vínculo (meusProcessos). Meus Processos = atribuídos ao usuário autenticado, sem injetar Situação. Todos = visão do perfil/esfera; situação padrão Aguardando só no modo Todos. Analista continua Em Análise. Texto da UI alinhado à regra de negócio.
- **Motivo:** Usuário CG desmarcou Todos e ainda vinha filtro de Situação (Em Análise) forçado — fora da regra Meus vs Todos.
- **Alternativa rejeitada:** Forçar Em Análise no Meus Processos
- **Impacto:** painel-gestao-lic-config.model, gestao-licenciamento-exploracao, personalizar-painel, PainelGestaoLicPersonalizacaoService
- **Quem decidiu:** Usuário + agente

---

### 24/07/2026 — sinaflor — Gestão — Meus = só vínculo; Todos = perfil

- **Decisão:** Meus Processos (padrão/null/true): SOMENTE destinatário ativo na tramitação, em qualquer perfil. Todos (meusProcessos=false): regras de perfil/esfera. Front sempre envia boolean. Limpar filtros no modal sincroniza o painel (remove Situação fantasma). Login destinatário aceita CPF com/sem máscara.
- **Motivo:** CG via Meus via outros processos; modal limpo ainda mostrava Aguardando Distribuição nos filtros aplicados.
- **Alternativa rejeitada:** Meus = ampla AND vínculo (e omitir param no Todos)
- **Impacto:** LicenciamentoQueryService.filtraAcessoGestao, TramiteLicDestinatarioRepository, gestao-licenciamento front/resumo
- **Quem decidiu:** Usuário + agente

---

### 24/07/2026 — sinaflor — Tramitação — histórico + aviso manter aberto

- **Decisão:** Tela de tramitação carrega histórico finalizado + rascunho. Nova tramitação inicia com Manter aberto marcado. Hint explica: sem marcar, processo sai da fila da unidade e fica só para analistas atribuídos (Meus Processos).
- **Motivo:** Usuário reabria a tela e não via tramitação já finalizada; e temia perder o processo sem Manter aberto.
- **Alternativa rejeitada:** Só rascunho na tela de tramitação
- **Impacto:** gestao-tramitacao + listar-tramitacoes-adicionadas + tramitacao-analise-projeto
- **Quem decidiu:** Usuário + agente

---

### 24/07/2026 — sinaflor

- **Decisão:** 1) Restaurar checkbox Todos em Tipos e Situação. 2) Alternar Meus/Todos não altera situações. 3) Meus do Gerente Operacional = destinatário OU unidade com FL_MANTER_ABERTO=S.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 24/07/2026 — cortejo — Opt-out WhatsApp por agendamento

- **Decisão:** Campo appointment.enviarWhatsAppCliente (default true). Se false: UI no criar agendamento + CF pula confirmação (marca confirmacaoPuladaEm) e lembretes 7d/1d. Confirmação online pending também grava o flag.
- **Motivo:** Dona pode não querer WhatsApp em um agendamento específico.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 24/07/2026 — cortejo — Confirmação WhatsApp vs walk-in só nome

- **Decisão:** enviarWhatsAppCliente=false só bloqueia confirmação; lembretes 7d/1d independentes. Novo modo walk_in: só nome sem clientId/telefone; confirmação off.
- **Motivo:** Pedido da dona: opt-out só da confirmação + agendar sem cadastrar cliente.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 24/07/2026 — zenpro — Zen Pro — catálogo RockB2B local

- **Decisão:** Zen Pro: catálogo MODELOS + DISPOSITIVOS_PRESETS alinhados ao RockB2B (101 modelos Apple/Samsung/Mi). IDs estáveis iphone-15, samsung-s24, iphone-17-pro-max. Extras Zen (Pixel, foldable, Xiaomi 13-15) mantidos. Seed com marca xiaomi. Sem deploy — teste local.
- **Motivo:** Usuário pediu importar modelos RockB2B e substituir os existentes, manter só os que não estão no Rock
- **Alternativa rejeitada:** Manter so 3 modelos mock
- **Impacto:** modelos.ts, dispositivosPresets.ts, catalogoSeedData, rockb2bPersonalizacao.json, types SEED_CATALOGO
- **Quem decidiu:** Usuário + agente

---

### 24/07/2026 — Zen Pro cameras H5 hardware — tight

- **Decisão:** Cameras de mock personalizacao: extrair do PNG RockB2B H5 com platao apertado no bbox do hardware (lentes/flash), nao no bleed vermelho de impressao. Cor do platao por luminancia media (claro iPhone / escuro Android). Assets em public/molduras/rock/*-camera.png?v=5; cameraPresetId=sem-camera quando ha frame.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 24/07/2026 — Zen Pro H5 punch foto sob camera

- **Decisão:** Padrao personalizacao Zen Pro: molde H5 RockB2B e autoridade. cameraFrameUrl (PNG extraido do frameImage) faz destination-out na arte (foto/texto nao cobrem o modulo) e depois overlay por cima. Mesmo pipeline em CaseEditor, CasePreview e exportCaseArt. Nao usar SVG inventado quando ha frame H5.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 24/07/2026 — zenpro — Mockup de câmera com profundidade sem contaminar a arte

- **Decisão:** Renderizar no CaseEditor e CasePreview a sombra de contato e o filete claro usando o alpha do PNG H5; manter o exportCaseArt apenas com o punch da câmera.
- **Motivo:** Aproximar o preview da aparência física da GoCase preservando a posição exata de lentes e flash e mantendo o arquivo de impressão sem efeitos decorativos.
- **Alternativa rejeitada:** Gravar sombra, hardware e filete diretamente no PNG exportado da arte.
- **Impacto:** Todos os 101 modelos recebem profundidade consistente; a produção continua recebendo somente a área imprimível.
- **Quem decidiu:** usuário e agente Cursor

---

### 25/07/2026 — setmatch — Setmatch — sync Rankings/Calendário Figma

- **Decisão:** Mapear tab trofeu → Rankings (Global + Winner FIXADO) e tab estatisticas → Calendário (PRÓXIMAS/HISTÓRICO) conforme Figma SvZ8vsoadqyC0yz0uUQm6C (27 frames). BottomNav label ativa da 2ª aba = Rankings. Cores bodyLight/textDark centralizadas. Logout no header do Perfil.
- **Motivo:** Figma já tinha 8 telas de rankings/calendário; placeholders quebravam o padrão visual do produto
- **Alternativa rejeitada:** Manter placeholders nas tabs Troféu/Estatísticas
- **Impacto:** app/(tabs)/trofeu.tsx, estatisticas.tsx, BottomNav, colors.ts, setmatch-prd.md, setmatch-project.md
- **Quem decidiu:** Gustavo + agente

---

### 25/07/2026 — setmatch

- **Decisão:** Setmatch: rankings de clubes com solicitação (Winner = ranking próximo em que o usuário já é membro após aceite). Schema clubes/rankings/classificacao/solicitacoes/posts. Wizard idade min 5 + digitável; peso digitável; foto upload imediato com botão Avançar. Feed social + notícias na Home. Seed Firestore (Winner, partidas ranking/amistoso, post). Rules+indexes deployados.
- **Motivo:** Pedido do usuário: lógica completa de cadastro em ranking, clubes para donos de academia, seed real, feed com espaço e notícias.
- **Alternativa rejeitada:** N/A
- **Impacto:** Novas rotas /ranking/novo e /ranking/[id]; trofeu e home reescritos; firestore.rules expandido; maturidade ~82%
- **Quem decidiu:** Ambos

---
### 25/07/2026 — setmatch — Roles admin_clube vs jogador + social amigos

- **Decisão:** Separar login admin de clube (role admin_clube) do jogador; só admin cria clube/ranking/torneio. Jogador tem endereço no wizard, filtro global de esporte (EsporteContext), amizades + feed Amigos + chat amigo/clube. Criar ranking removido do fluxo comum.
- **Motivo:** Pedido do usuário: cadastro de clube pelo admin, filtro por esporte (tênis), endereço para proximidade, conectar amigos e mensagens.
- **Alternativa rejeitada:** Qualquer usuário criar clube/ranking pela aba Troféu
- **Impacto:** Novas rotas /clube e auth admin; coleções amizades/conversas/torneios; rules restritivas; contas seed de teste
- **Quem decidiu:** usuario+agente

---

### 25/07/2026 — setmatch — Admin só por solicitação + fluxos torneio/aulas/celular

- **Decisão:** Admin de clube só via solicitação à Setmatch (sem signup no app). Role admin_clube protegida nas rules. Jogadores filtram rankings/torneios por esporte cadastrados pelos admins. Solicitar ranking e inscrição torneio abrem chat com dono. Interesse em aulas registra + chat (pagamento combinado fora). Celular obrigatório + WhatsApp. Perfil editável; perfil público /jogador/[uid] com stats.
- **Motivo:** Alinhamento com estratégia de negócio: Setmatch controla quem vira admin; clube explica aulas/pagamento
- **Alternativa rejeitada:** Cadastro público de admin no app + pagamento automático de aulas
- **Impacto:** Removido admin-cadastro; torneio/[id]; perfil/editar; interessesAulas; feed jogos amigos; telefone no wizard
- **Quem decidiu:** usuario+agente

---

### 25/07/2026 — setmatch — Pagamentos Mercado Pago aulas/ranking/torneio + setmatchId

- **Decisão:** Checkout Pro (PIX + cartão 1x) via Cloud Functions criarPreferenciaSetmatch + webhookMercadoPagoSetmatch. ID amigável SM-XXXXXX. Dono cadastra regras em clubes.aulas, rankings.pagamento e torneios.pagamento. Coleções pagamentos e matriculas. Admin libera no financeiro. Recorrência MVP = ciclo mensal + vigenteAte e renovação por novo checkout (não preapproval). Token em functions/.env MP_ACCESS_TOKEN (defineString, sem Secret Manager no MVP).
- **Motivo:** Jogador paga no app; dono do clube controla regras, libera e mensagem inscritos; ID legível para matricular alunos.
- **Alternativa rejeitada:** Pagamento só fora do app / preapproval completo / Secret Manager obrigatório antes do primeiro deploy
- **Impacto:** Functions southamerica-east1 deployadas; app precisa EXPO_PUBLIC_MP_FUNCTION_URL; checkout real só após MP_ACCESS_TOKEN
- **Quem decidiu:** gustavo+agente

---

### 25/07/2026 — setmatch — Filtro estrito por esporte + visão Meu clube

- **Decisão:** Esporte ativo persiste em AsyncStorage. Feed/notícias/partidas/torneios filtrados estritamente pelo esporte (posts sem esporte = tenis legado). Post mostra emoji do esporte. Troféu tem chips de esporte. Jogador tem /meus-clubes e /meu-clube/[id] com aulas, rankings e pagamentos só daquele clube; /pagamentos?clubeId= filtra.
- **Motivo:** Usuário pediu: ao clicar tênis só vê tênis; e visão focada no clube onde faz aula/ranking para pagamentos.
- **Alternativa rejeitada:** N/A
- **Impacto:** UX multi-esporte isolada; hub de clube do jogador separado do painel admin
- **Quem decidiu:** Ambos

---

### 26/07/2026 — setmatch — Admin aulas modalidades, fix UI/chat, WhatsApp suporte

- **Decisão:** Button sem width 100% (só alignSelf stretch) para não estourar em row. Torneio chips em ScrollView horizontal com maxHeight. Conversas usam doc ID estável (não query por chave — permission-denied). Modalidades de aula em clubes/{id}/modalidadesAula (individual/duo/trio/quarteto/spozinho/beach). Aluno com desconto%. WhatsApp suporte 19989632897. Admin pode criar inscritos no torneio.
- **Motivo:** Bugs de UI admin + messaging + pedido de cadastro de aulas com desconto e mais clubes
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 26/07/2026 — setmatch — Clube ativo + feed com jogos + aulas aluno + convites

- **Decisão:** ClubeContext paralelo ao EsporteContext; feed unifica posts + partidas; aulas do aluno em rota dedicada /meu-clube/[id]/aulas; desafios com criar/aceitar/placar→partida+post; admin modalidades em FlatList única; rules de conversas corrigidas para get em doc inexistente
- **Motivo:** Usuário pediu clube+esporte no início, feed com jogos, convites, aulas mais claras e scroll de modalidades admin
- **Alternativa rejeitada:** N/A
- **Impacto:** Home/Troféu filtrados por clube; chat funciona na primeira conversa; jogador vê modalidades
- **Quem decidiu:** Ambos

---

### 26/07/2026 — setmatch — Abas dedicadas Aulas e Mensagens para jogador

- **Decisão:** Novas tabs /(tabs)/aulas (matrículas + descobrir clubes) e /(tabs)/mensagens (useConversas → /chat/[id]); Notificações ganhou aba MENSAGENS com conversas recentes; BottomNav com 6 itens compactados
- **Motivo:** Usuário pediu seção separada de aulas e de mensagens em vez de acesso via perfil, e mensagens visíveis em notificações
- **Alternativa rejeitada:** N/A
- **Impacto:** app/(tabs)/aulas.tsx, mensagens.tsx, notificacoes.tsx, _layout.tsx, components/ui/BottomNav.tsx, perfil.tsx
- **Quem decidiu:** Ambos

---

### 26/07/2026 — setmatch — Fix flash wizard + confronto VS + foto perfil + aulas por mensagem

- **Decisão:** 1) Auth: setLoading(true) antes de await no onAuthStateChanged + AuthGuard/wizard/primeiro-acesso esperam perfil — elimina flash da tela idade. 2) Aulas aluno: só mensagem app/WhatsApp com Setmatch ID; clube matricula. 3) Editar perfil com foto (uploadFotoPerfil). 4) Confronto premium: VS com fotos, stats, H2H, formatos (Md3, STB até 10, etc.).
- **Motivo:** Pedido do usuário: sem cadastro direto em aula, sem flash wizard, editar foto, agendar confronto top
- **Alternativa rejeitada:** N/A
- **Impacto:** AuthContext, AuthGuard, wizard/_layout, primeiro-acesso, perfil/editar, desafio/novo, desafio/[id], meu-clube/[id]/aulas, services/desafios, constants/formatosPartida
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Página do produto com seletor de modelos (estilo OBLI)

- **Decisão:** Vitrine personalizável mostra 1 card por produto; clique abre /produto?id= com botões dos modelosCompativeis; Personalizar segue para /personalizar?modelo=&produto=. Rotas também em /{slug}/produto e /revendedor/produto + rewrites Firebase.
- **Motivo:** UX pedida pelo usuário (referência useobli.com.br/capas): escolher o iPhone dentro da página do produto, não N cards na grade.
- **Alternativa rejeitada:** Manter expansão produto×modelo na vitrine; dropdown em vez de botões
- **Impacto:** ProductCard, catalogoProdutos, PersonalizarSection, useLojaPaths, firebase.json, app/produto
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Catálogo capas prontas sem imagens

- **Decisão:** 20 produtos prontos Brave/Smart/MagSafe cadastrados sem imagens; preços 19990/24990; modelosCompativeis por linha; CatalogProductCard aponta para /produto?id=
- **Motivo:** Usuário pediu estrutura do catálogo estilo OBLI sem copiar fotos com direito autoral
- **Alternativa rejeitada:** Usar fotos OBLI no catálogo
- **Impacto:** Firestore produtos/*, CatalogProductCard, seed-capas-pronta-catalogo.ts
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — modelosCompativeis por SKU igual OBLI

- **Decisão:** Cada capa pronta (Brave/Smart/MagSafe) tem lista própria de modelosCompativeis espelhando as variações do produto OBLI correspondente — não uma lista única de 14 iPhones. Seed e Firestore alinhados (ex.: Rosa/Roxa=17; MagSafe Laranja/Pro cores=17 Pro+Max; Desert=16 Pro+Max; Brave Cinza inclui 14 Pro Max e Brave Azul não).
- **Motivo:** Usuário pediu compatibilidade real por capa como na OBLI; seletor na PDP deve mostrar só modelos que aquela SKU cobre.
- **Alternativa rejeitada:** Mesmos 14 modelos em todos os 20 produtos
- **Impacto:** Seletor de iPhone na /produto muda conforme o produto; seed não sobrescreve com lista genérica
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Silhueta iPhone = body mask H5 RockB2B

- **Decisão:** Formato do mock iPhone = silhueta do contorno vermelho externo do frameImage H5 RockB2B. Script process-rockb2b-body-masks.mjs gera {id}-body-mask.png + molduraAspect + caseRadius. CaseFake3dPreview usa CSS mask-image; CasePreview usa destination-in; getCaseLayout usa aspect por modelo. iPhone primeiro (38); Samsung/Xiaomi depois.
- **Motivo:** Cliente quer formato do celular igual ao print-h5 hotCustom, não só a câmera
- **Alternativa rejeitada:** Round-rect genérico igual para todos + botões CSS inventados
- **Impacto:** Preview Na capinha / Vista frontal com botões e cantos iguais ao hotCustom Rock para iPhones
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — useCaseVisual — molde H5 em todo mock

- **Decisão:** useCaseVisual(modeloId) resolve molde H5 (bodyMask + camera + aspect) pelo Provider ou pelo modeloId. CasePreview/CaseFake3d/CaseEditor/export usam o mesmo molde em todos os lugares.
- **Motivo:** Cliente reportou que o formato não parecia o mesmo molde em todos os lugares
- **Alternativa rejeitada:** Depender só do PersonalizacaoVisualProvider — carrinho/checkout/hero ficavam com round-rect e SVG
- **Impacto:** Carrinho, checkout, admin, hero e editor compartilham silhueta/câmera Rock
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Só vista frontal + câmera branca no mock

- **Decisão:** Ver na case = só vista frontal. Módulo de câmera no mock clareado para branco/prata (lightenCameraPlate + CAMERA_MOCK_PLATE). Export de impressão inalterado.
- **Motivo:** Pedido do usuário
- **Alternativa rejeitada:** Toggle Na capinha / Fake3D + câmera escura do PNG H5
- **Impacto:** PreviewCapaModal, CasePreview, CaseEditor, useCameraMockDepth
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Câmera H5 natural sem lighten + clip round-rect

- **Decisão:** Câmeras do mock = PNG H5 exacto (--natural, pixels H5 primeiro, buracos com platô claro). Nunca lightenCameraPlate/recolor em runtime. Branco em volta = só bodyFill/corAparelho sob o punch. CasePreview e CaseEditor usam clip round-rect (usarBodyMask=false) porque body-mask destination-in vazava nas bordas. Assets ?v=15.
- **Motivo:** Usuário: clarear estragou lentes; queria só branco em volta e câmeras iguais ao H5; bordas vazando.
- **Alternativa rejeitada:** lightenCameraPlate em runtime; clip com body-mask H5 no frontal
- **Impacto:** 38 iPhones regenerados; mock frontal limpo; lentes preservadas
- **Quem decidiu:** Usuário + agente

---

### 27/07/2026 — zenpro — Moldura H5 body-mask em todos os lugares

- **Decisão:** Moldura/silhueta do mock = body-mask H5 em todos os lugares (CasePreview, CaseEditor, export). 101 modelos regenerados v=16 com dilate do filete vermelho + morph close + AA; bodyRimUrl para borda no mesmo contorno (não stroke round-rect). Nunca desligar body mask no frontal.
- **Motivo:** Usuário: molde da capinha não estava de acordo com o H5 após ter desligado body mask por vazamento.
- **Alternativa rejeitada:** usarBodyMask=false com round-rect genérico (bordas limpas mas fora do H5)
- **Impacto:** 101 body-mask + body-rim; aspect/radius atualizados; mock segue botões e cantos do print-h5
- **Quem decidiu:** Usuário + agente

---

### 27/07/2026 — zenpro — Sem borda branca no mock H5

- **Decisão:** Mock com molde H5: só silhueta (bodyMask destination-in). Sem bodyRim nem CASE_BORDER branco no preview/editor quando há H5.
- **Motivo:** Usuário: nao deve ter borda branca, só o formato do H5.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Mock full-bleed H5 sem platô cinza

- **Decisão:** Mock H5 = foto full-bleed na silhueta (bodyMask harden). Sem punch/bodyFill no preview. Overlay câmera com platô claro removido (stripCameraIslandPlate) — igual print-h5 laranja. Export mantém punch.
- **Motivo:** Usuário: bordinha cinza atrás não deve ter; foto deve passar toda na marcação como exemplo laranja do H5.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Mock H5 quase bom sem aureola externa

- **Decisão:** Revert mock para punch+bodyFill+overlay H5 completo. Mantém hardenBodyMaskAlpha e clipInset=0 (foto até a borda). Remove sombra/shadowBlur fora do contorno H5 no editor/preview.
- **Motivo:** Usuário: voltar como estava (quase bom); só a foto até a borda H5 e sem cinza/sombra fora do H5.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Admin arte produção H5 + mapItem arte URLs

- **Decisão:** Admin pedidos: mapItem lê arteProducaoUrl/arteFotoUrl/arteTextoUrl. Preview do dono = PNG retangular bleed; botão Gerar arte se faltar. Export produção sem punch. salvarPersonalizacao não engole falha. Storage marca escreve artes-producao.
- **Motivo:** Pedido admin não mostrava artes iguais ao H5
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 27/07/2026 — zenpro — Checkout MP restringe forma + desconto PIX loja/produto

- **Decisão:** Preference Checkout Pro usa mapFormaParaMp: PIX exclui credit/debit/ticket/atm/prepaid + account_money e default pix; cartão exclui boleto/PIX/débito e installments=N escolhido; boleto só ticket. Desconto PIX e max parcelas: lojas/{id}.config.pagamentoPadrao (Admin→Loja marca) como padrão; produto sobrescreve se descontoPixPercentual/maxParcelasCartao > 0, senão herda. Admin pedido: preview CasePreview (mock cliente) + baixar impressão H5 + arte final/só foto/texto.
- **Motivo:** Cliente via PIX via crédito e carteira MP; dono precisa configurar desconto/parcelas por loja e produto; produção precisa arte H5 retangular além do mock.
- **Alternativa rejeitada:** Manter preference sem excluded_payment_types (todas as formas no MP).
- **Impacto:** Deploy functions criarCheckoutMercadoPago + hosting admin/checkout.
- **Quem decidiu:** Usuario + agente

---

### 28/07/2026 — zenpro — Admin pedido: recorte H5 print Rock (só download)

- **Decisão:** Download no pedido admin (dono Zen Pro): exportH5PrintArtBlob — retângulo laranja Rock, foto+texto full bleed (podem sair do contorno), câmera H5, filete vermelho (body-rim). Removidos botões só foto/só texto. Preview do pedido continua CasePreview do cliente. Fluxo do cliente/checkout não muda.
- **Motivo:** Dono precisa do guia igual print-h5 RockB2B para produção
- **Alternativa rejeitada:** Silhueta recortada ou camadas só-foto/só-texto no admin
- **Impacto:** PedidoItemPreview + regenerarArtesPedido; exportCaseArt clip h5-print
- **Quem decidiu:** Usuario + agente

---

### 28/07/2026 — zenpro — Recorte H5 = frameImage Rock print-guide

- **Decisão:** Recorte H5 do admin usa printGuideUrl gerado do frameImage Rock (preto→transparente; mantém vermelho+câmera). Script process-rockb2b-print-guides.mjs para os 101 modelos. Export: laranja + foto/texto + overlay do guia.
- **Motivo:** Usuário: recorte H5 não estava igual ao print-h5 Rock
- **Alternativa rejeitada:** Reconstruir contorno vermelho a partir do body-rim + camera processada
- **Impacto:** public/molduras/rock/*-print-guide.png + rockb2bPersonalizacao + exportCaseArt h5-print
- **Quem decidiu:** Usuario + agente

---

### 28/07/2026 — sinaflor — Gestão — visibilidade Meus/Todos GO e Analista

- **Decisão:** Regra geral: excluir Em Elaboração/Em Elaboração Técnica do Painel de Gestão. GO Todos = órgãos SCA qualquer status. GO Meus = destinatário OU órgão+Aguardando Distribuição OU atuou+manter aberto. Analista Meus = destinatário; Analista Todos = órgãos vinculados. somenteProcessosAtribuidos sempre false para Analista poder marcar Todos.
- **Motivo:** Regras de negócio de visibilidade por perfil definidas pelo usuário (2026-07-28).
- **Alternativa rejeitada:** Analista só Meus; GO Todos ocultando manterAberto=N
- **Impacto:** LicenciamentoQueryService, RestClientUtil, personalizar-painel hint, PROJECT.md, gestao-visibilidade-perfis.md
- **Quem decidiu:** Usuário + agente

---

### 28/07/2026 — sinaflor — Gestão — Todos os Processos visível para Analista

- **Decisão:** Checkbox Todos os Processos sempre visível no personalizar (sem *ngIf). Front força somenteProcessosAtribuidos=false; contexto API também fixa false. Analista passa a ver Todos.
- **Motivo:** Usuário: botão Todos não aparecia para Analista
- **Alternativa rejeitada:** Depender só do flag backend com *ngIf
- **Impacto:** personalizar-painel html/ts parent, PainelGestaoLicPersonalizacaoService
- **Quem decidiu:** Usuário + agente

---

### 29/07/2026 — fabrica — RAG affinity + inject preferred notes

- **Decisão:** Retrieval RAG: afinidade query↔nota + injeção de candidatos preferidos (schemas Cortejo/LashMatch, mapeamento/regras SINAFLOR, erros em crash Chroma). Eval v2: hit@1 66→79%, hit@3 88→98%, hit@5 100%.
- **Motivo:** Misses no eval: schemas fora do top-RRF; decisoes/erros competindo; sinaflor vs erp.
- **Alternativa rejeitada:** N/A
- **Impacto:** rag_retrieval.py hot path; golden aceitaveis gs-015/018; reindex Chroma após DB corrompido.
- **Quem decidiu:** Ambos

---

### 29/07/2026 — fabrica — RAG HTTP na AWS via App Runner (Docker + Terraform)

- **Decisão:** Hospedar o servidor indexar_obsidian_chroma.py --server em AWS App Runner com imagem ECR, índice Chroma no S3 (sync do PC via sync-push.ps1) e autenticação X-RAG-Key. Pacote em obsidian/aws-rag/ (Dockerfile, terraform, scripts).
- **Motivo:** Manter o stack híbrido Chroma+BM25+MiniLM que já passou no eval (~78% hit@1) sem migrar para Bedrock KB; custo alvo US$12-30/mês; backup/remoto do RAG local na porta 7332.
- **Alternativa rejeitada:** Bedrock Knowledge Base, SageMaker endpoint, Lambda+EFS — mais caro ou perda do pipeline local já afinado.
- **Impacto:** Deploy sob demanda: bootstrap → sync-push → build-push → terraform apply. MCP pode apontar RAG_BASE_URL para App Runner.
- **Quem decidiu:** Gustavo + agente

---

### 29/07/2026 — fabrica — RAG App Runner us-east-1 no ar (chromadb 1.5 + health async)

- **Decisão:** RAG em produção em us-east-1 (App Runner https://gmnxgbtjy9.us-east-1.awsapprunner.com): torch CPU, health imediato + warmup async, chromadb 1.5.x alinhado ao PC.
- **Motivo:** Deploy completo pedido pelo usuário; região e versões ajustadas após CREATE_FAILED e panic SQLite.
- **Alternativa rejeitada:** sa-east-1 (App Runner inexistente); torch CUDA (imagem 10GB); chromadb 1.0.x no Docker (incompatível com dump 1.5.x do Windows)
- **Impacto:** Pipeline bootstrap/sync/build/apply validada; /buscar remoto OK. MCP pode usar RAG_BASE_URL + X-RAG-Key.
- **Quem decidiu:** Gustavo + agente

---

### 29/07/2026 — fabrica — MCP rag_buscar aponta para App Runner remoto

- **Decisão:** MCP fabrica-apps e hooks passam a usar App Runner (RAG_BASE_URL + RAG_API_KEY via mcp.json e ~/.cursor/rag-remote.json). server-v2.js e rag-lib.js leem essa config; /health sem key, /buscar com X-RAG-Key.
- **Motivo:** Usuario pediu apontar rag_buscar para a URL remota já validada.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 29/07/2026 — fabrica — RAG AWS: alarmes CloudWatch + restart auto no sync S3

- **Decisão:** Passo 1+2 do RAG AWS: CloudWatch alarms (5xx + latência) via SNS fabrica-rag-alerts; Lambda fabrica-rag-restart-on-chroma dispara StartDeployment quando S3 recebe chroma/chroma.sqlite3. sync-push.ps1 continua indexando no PC.
- **Motivo:** Usuario pediu observabilidade e restart automatico apos sync do indice.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 29/07/2026 — cortejo — Intervalo de horários configurável (slotStepMin)

- **Decisão:** Campo salon.slotStepMin (5–60, padrão 30) no documento do salão. Grade de início no app (generateTimeSlots), availableSlots CF e booking.html usam o mesmo valor. UI em config/horarios com chips 10/15/20/30/60 + personalizado. Duração do serviço permanece independente.
- **Motivo:** Salões pediram grade de 10 em 10 (ou outro passo) sem mudar duração dos serviços.
- **Alternativa rejeitada:** Intervalo por profissional — mais complexo e inconsistente no link público.
- **Impacto:** App OTA + hosting + availableSlots. Salões sem o campo continuam em 30 min.
- **Quem decidiu:** produto + agente

---

### 29/07/2026 — cortejo — Agenda: timeline diária padrão + expandir mês

- **Decisão:** Aba Agenda padrão = visão dia: DayStrip + DayHourTimeline (grade com vazios via slotStepMin + businessHours). Expandir/toggle calendário = visão mês (AgendaCalendar + DayScheduleList). Swipe horizontal muda o dia; toque no slot vazio abre novo com time=HH:mm. Sem Wix Timeline.
- **Motivo:** Cliente pediu timeline diária estilo referência (slots vazios + faixa de dias), mantendo calendário mensal acessível.
- **Alternativa rejeitada:** Wix Timeline / ExpandableCalendar — não mostra slots vazios no passo configurável com tokens Cortejo de forma simples.
- **Impacto:** app/(tabs)/index.tsx; components/agenda/DayStrip.tsx, DayHourTimeline.tsx; utils/dayHourGrid.ts; prefill time em agendamento/[id].
- **Quem decidiu:** produto + agente

---

### 29/07/2026 — cortejo — Editar agendamento + validação cliente + conflito claro

- **Decisão:** Agendamento: botão Editar no detalhe abre o mesmo formulário (isEditing); cadastro de cliente com labels *, erros por campo e texto de bloqueio do botão; TimeSlotGrid mostra ocupados em cinza; checkConflict inclui pending e mensagem com nome/horário.
- **Motivo:** Usuário pediu validações claras, edição e impedir horário já ocupado.
- **Alternativa rejeitada:** Só alert genérico sem editar — insuficiente
- **Impacto:** app/agendamento/[id].tsx, TimeSlotGrid, appointments.checkConflict, timeSlots booked statuses
- **Quem decidiu:** Ambos

---

### 29/07/2026 — cortejo — Editar agendamento + validação cliente

- **Decisão:** Botão Editar no detalhe do agendamento; formulário com campos * e erros; TimeSlotGrid mostra ocupados; checkConflict com pending e mensagem clara.
- **Motivo:** Pedido do usuário: validação cadastro, editar, não agendar horário ocupado.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 29/07/2026 — LashMatch — Tela stack agendamento/[id] no lugar do modal

- **Decisão:** Criar/editar agendamento em app/agendamento/[id].tsx (Expo Router: id=novo|docId, query date=YYYY-MM-DD, time=HH:MM). Fluxo Cliente → Serviço → Funcionária → AgendaCalendar embedded + TimeSlotGrid (gerarSlotsDisponiveis com slotStepMin de usuarios/{uid}) + botão Ver horários. Cancelamento seta status cancelado. Stack.Screen em _layout.tsx.
- **Motivo:** Agenda diária (timeline) abre formulário full-screen com prefill de data/hora; modal na aba ficou insuficiente.
- **Alternativa rejeitada:** Manter formulário só em Modal dentro de agendamentos.tsx
- **Impacto:** app/agendamento/[id].tsx; app/_layout.tsx; utils/gerarSlotsDisponiveis.ts (slotStepMin); navegação desde DayHourTimeline/DayScheduleList
- **Quem decidiu:** produto + agente

---

### 29/07/2026 — lashmatch — LashMatch agenda = padrão Cortejo (UI + rules + publicBooking)

- **Decisão:** LashMatch agenda alinhada ao padrão Cortejo: viewMode day/month (DayStrip+DayHourTimeline), rota /agendamento/[id], slotStepMin em usuarios/{uid} (perfil chips), CF publicBooking + slotsAgendamentoPublico leem slotStepMin, firestore.rules agendamentos create só autenticado dono. Status/path PT mantidos.
- **Motivo:** Paridade UX e segurança do link público sem migrar schema inglês.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 29/07/2026 — cortejo — OTA + iOS 1.0.4 build 21 submit ASC

- **Decisão:** eas.json submit.production.ios.ascAppId=6781006697 para submit non-interactive. OTA + build iOS 1.0.4 (21) com RC appl_OnUg… enviados à ASC.
- **Motivo:** Usuário pediu republicar OTA com public key, build nova e submit.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 30/07/2026 — zenpro — Página produto estilo OBLI — PIX, parcelas e frete

- **Decisão:** ProdutoPageClient exibe preço no padrão OBLI: se descontoPixPercentual > 0 (produto ou loja.pagamentoPadrao), mostra valor PIX em destaque + % de desconto + preço cheio; parcelas = maxParcelasCartao cadastrado (até Nx de R$). Frete CEP/Calcular na própria página (FreteCheckoutSection compacto). Não exibe quantidade em estoque ao cliente.
- **Motivo:** Referência visual OBLI pedida pelo dono; estoque público não deve aparecer; frete e condições de pagamento precisam estar visíveis antes do carrinho.
- **Alternativa rejeitada:** Manter só preço único sem PIX/parcelas/frete na PDP
- **Impacto:** Cliente vê desconto PIX e parcelas do admin + cotação de frete na seleção do produto
- **Quem decidiu:** Usuário + agente

---

### 30/07/2026 — zenpro — Desconto PIX padrão 5% no cadastro de produto

- **Decisão:** Cadastro de produto inicia Desconto PIX em 5% (constante DESCONTO_PIX_PRODUTO_PADRAO / PAGAMENTO_PRODUTO_DEFAULT). Dono pode alterar; 0 = herda padrão da loja. Capinha Nova também grava 5%.
- **Motivo:** Pedido do dono: padrão 5% no campo ao cadastrar produto
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Usuário

---

### 30/07/2026 — cortejo — Agenda: grade segue horário do profissional

- **Decisão:** DayHourTimeline usa agendaGridBusinessHours(members, salon) — une businessHours dos profissionais ativos (tela Horários). Antes usava só salon??DEFAULT 09:00-19:00 e ignorava members/{uid}.businessHours.
- **Motivo:** Dona configurou 06:40-20:00 no profissional; agenda mostrava desde 09:00.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 30/07/2026 — lashmatch — Agenda grade usa horarioTrabalho das funcionárias

- **Decisão:** DayHourTimeline em agendamentos.tsx passa a usar agendaGridBusinessHoursFromFuncionarias(): une horarioTrabalho (dom/seg…) das funcionárias ativas, com fallback usuarios.businessHours e DEFAULT 09h. Mesma classe de bug do Cortejo (grade ignorava horário real).
- **Motivo:** Confirmação do usuário: no LashMatch a grade também caía em 09h porque lia businessHours do usuário/dono, não o horário configurado em Funcionárias.
- **Alternativa rejeitada:** Manter businessHours do usuário como fonte única
- **Impacto:** app OTA LashMatch production; utils/businessHours.ts + agendamentos.tsx
- **Quem decidiu:** produto + agente

---

### 30/07/2026 — sinaflor — Gestão — exportar para todos os perfis

- **Decisão:** Botão exportar da Gestão de Licenciamento usa GESTAO_LICENCIAMENTO_ROLES (todos os perfis). Endpoint /exportacao já aceitava todos; faltava role no *hasAccess do datatable. Export aplica o mesmo filtro de situação da listagem.
- **Motivo:** Usuário pediu exportar igual à lista normal; botão só aparecia para CG
- **Alternativa rejeitada:** Manter export só para Consulta Geral
- **Impacto:** gestao-licenciamento-exploracao.component.html, GestaoLicenciamentoResource.exportar
- **Quem decidiu:** Usuário + agente

---

### 31/07/2026 — cortejo — Agenda multi-serviço + horário da timeline no novo agendamento

- **Decisão:** Agendamento app permite vários serviços (chips multi-select; durationMin = soma; priceTotal = soma; serviceIds/serviceNames arrays). Toque em slot vazio na DayHourTimeline passa ?time=HH:mm e o horário NÃO é limpo ao escolher serviço/profissional (só ao mudar a data). Banner “Horário da agenda” mostra o horário pré-selecionado.
- **Motivo:** Pedido do usuário: mais de um serviço por horário e já levar o horário tocado na grade do dia.
- **Alternativa rejeitada:** Um agendamento por serviço; limpar horário ao mudar profissional
- **Impacto:** app OTA; schema Firestore já tinha serviceIds[]; link público /agendar permanece 1 serviço
- **Quem decidiu:** produto + agente

---

### 31/07/2026 — lashmatch — Multi-serviço + horário timeline no LashMatch (paridade Cortejo)

- **Decisão:** LashMatch app/agendamento/[id].tsx: chips multi-select (servicoIds/servicoNomes + legado servico/servicoId); duração/preço somados; horário da DayHourTimeline via ?time= com banner. Versões store: LashMatch 1.0.2, Cortejo 1.0.5.
- **Motivo:** Pedido: portar alterações e gerar build/submit LashMatch e Cortejo
- **Alternativa rejeitada:** Só Cortejo com multi-serviço
- **Impacto:** EAS iOS build+submit ambos apps
- **Quem decidiu:** produto + agente

---

### 31/07/2026 — cortejo — WhatsApp {{servico}} com todos os serviços do agendamento

- **Decisão:** formatServiceNamesLabel(serviceNames) nas CFs Cortejo (confirmação, lembretes, fallback, push). LashMatch: preferir servicoNomes.join(', ') antes de servicoNome.
- **Motivo:** Multi-serviço salvava array, mas WhatsApp usava só [0].
- **Alternativa rejeitada:** N/A
- **Impacto:** Deploy functions cortejo-app + lashmatch-627fd; OTA opcional client Cortejo
- **Quem decidiu:** Ambos

---

### 31/07/2026 — cortejo — Store 1.0.6 Cortejo + 1.0.3 LashMatch

- **Decisão:** Bump store LashMatch 1.0.3 e Cortejo 1.0.6 com eas build+auto-submit iOS (multi-serviço + horário timeline + WhatsApp {{servico}} multi).
- **Motivo:** Usuário confirmou LashMatch ok e pediu build/submit com versão no código
- **Alternativa rejeitada:** N/A
- **Impacto:** ASC TestFlight ambos apps
- **Quem decidiu:** Ambos

---

### 31/07/2026 — fabrica — Copy Meta: Utility ~R$ 0,035 (LashMatch + Cortejo)

- **Decisão:** Copy WhatsApp Próprio (LashMatch + Cortejo): confirmação/lembrete = templates Utility (~R$ 0,035 BR na tabela Meta), não mais estimativa genérica R$ 0,10. Arquivos planoMarketing, planoWhatsappEscolha, whatsappProprioGuia.
- **Motivo:** Alinhar texto ao rate card oficial e deixar claro que não é Marketing.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 02/08/2026 — lashmatch — Web hosting deve acompanhar app após OTA/build

- **Decisão:** Hosting Firebase (expo export) não atualiza com EAS OTA/build. Após mudanças de UI/copy em LashMatch e Cortejo, rodar export:web + firebase deploy --only hosting nos dois. Deploy 02/08/2026: lashmatch-627fd.web.app e cortejo-app.web.app sincronizados com código do app.
- **Motivo:** Live hosting estava em 29/07 enquanto app já tinha agenda/copy via OTA/submit.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 03/08/2026 — zenpro — Categorias vitrine + campanhas promocionais

- **Decisão:** Vitrine estilo Gocase no visual Zen Pro: categorias fixas termicos/capinhas/personalizadas via produtos.categoriaId; campanhas/{id} com titulo, descricao, produtoIds; nav + páginas /c/[slug] e /promocao?slug=; home com strip de promo e personalizadas no topo. Sem deploy nesta entrega.
- **Motivo:** Pedido do dono para categorias + promoções tipo Gocase e personalizadas não ficarem no fim da home
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Usuário + agente

---

### 03/08/2026 — sinaflor — Tramitação — RN02 tipos avaliação Vistoria

- **Decisão:** RN02 Vistoria: inserts SPRINT_19 (5 tipos VISTORIA_*). ANALISE_POA_AMAZONIA compartilhada. API tipos-avaliacao?idTipoTramite= filtra via TipoAvaliacaoLicEnum. Front libera tramite id=2 e reutiliza formulário com Tipo Avaliação obrigatório. Finalizar define status Em Vistoria quando último item é Vistoria.
- **Motivo:** RN02 Tipo de Avaliação para Vistoria do Projeto
- **Alternativa rejeitada:** Reutilizar só os tipos de Análise no dropdown de Vistoria
- **Impacto:** SPRINT_19/01_tb_tipo_avaliacao_lic_vistoria.sql, TipoAvaliacaoLicEnum, LicenciamentoTramitacaoService/Resource, gestao-tramitacao + tramitacao-analise-projeto, tramitacao.service.ts
- **Quem decidiu:** Usuário + agente

---

### 05/08/2026 — fabrica — Modo agente ERP Cursor (rule + 2 skills)

- **Decisão:** Nível 1 modo ERP no Cursor: rule global ~/.cursor/rules/erp-fabrica.mdc (alwaysApply false + globs) + skills criar-modulo-erp e revisar-pr-erp em ~/.cursor/skills/. Reutiliza notas erp-* já no RAG App Runner e MCP postgres. No repo ERP usar erp-projeto.mdc alwaysApply true (template em erp-agente-modo-cursor.md). Orquestra multi-agente = nível 2 futuro, não bloqueia.
- **Motivo:** Especializar rápido sem 6 agentes; conhecimento ERP já existia no vault.
- **Alternativa rejeitada:** Orquestrador LangGraph/6 workers antes de ter rule/skills
- **Impacto:** Arquivos locais Cursor + nota fabrica/erp-agente-modo-cursor.md + INDEX
- **Quem decidiu:** Ambos

---

### 05/08/2026 — fabrica — RAG mandatory gateway erp-agente-modo-cursor

- **Decisão:** ERP gateway no RAG: detectMandatoryRagDocs id erp-agente-modo em rag-lib.js força query para erp-agente-modo-cursor.md + workflow erp_modo_gateway. Atualizados erp-stack, rag-protocolo, rag-memoria-fabrica.mdc, erp-fabrica.mdc.
- **Motivo:** Garantir que consultas/implementações ERP sempre lembrem rule+skills antes do tema específico.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 05/08/2026 — fabrica — erp-ui-telas baseado em SAP Fiori floorplans

- **Decisão:** Criada erp-ui-telas.md como casca UX estável da fábrica, baseada nos floorplans SAP Fiori (List Report, Object Page, Worklist, Wizard, Overview) adaptados ao Angular 21. Domínio por cliente continua em PRD/modulo.
- **Motivo:** Padrão conceituado de mercado para telas ERP sem amarrar a um cliente.
- **Alternativa rejeitada:** Copiar SAPUI5/OData ou inventar UX sem floorplan
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 05/08/2026 — fabrica — Módulos canônicos produto + estoque (SAP MM simplificado)

- **Decisão:** Criados erp-modulo-produto.md (Material Master mínimo) e erp-modulo-estoque.md (Goods Movements: saldo + ledger append-only, tipos ENTRADA/SAIDA/AJUSTE/TRANSFERENCIA). Baseline fábrica; PRD sobrescreve. Fontes SAP MM + Odoo-like.
- **Motivo:** Agente não inventa domínio do zero; cliente só documenta divergências.
- **Alternativa rejeitada:** Módulos só por cliente sem baseline; ou copiar SAP MM completo com valuation/FI
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 06/08/2026 — fabrica — PRD baseline ERP MVP PT-BR (auth produto estoque)

- **Decisão:** Criado projetos/erp-baseline-prd.md: escopo v1 = auth+tenant+produto+estoque; fase 2 = vendas/financeiro; UI e mensagens PT-BR; SAP só como modelo de processo/Best Practices. Gateway erp-agente-modo + rule + workflow hook apontam para o PRD. INDEX e notas módulo/ui atualizadas.
- **Motivo:** Fechar escopo para o agente não inventar ERP genérico; indexar e sync App Runner.
- **Alternativa rejeitada:** PRD só na cabeça / módulos v1 inventados sem ordem SAP
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 06/08/2026 — sinaflor — HU133/HU134 Arquivar e Desarquivar na tramitação

- **Decisão:** Implementar tipos 7 (Arquivar) e 8 (Desarquivar) reutilizando fila/rascunho/histórico existentes. Disponibilidade via acoesDisponiveis no contexto. Arquivar: GO/GA, despacho+anexo, status Arquivado. Desarquivar: GO/GA/Analista só se Arquivado, restaura statusAnterior do último Arquivar. Bloquear 7+8 na mesma fila. Front: componente tramitacao-arquivamento compartilhado.
- **Motivo:** Atender HU133 e HU134 sem criar fluxo paralelo de tramitação.
- **Alternativa rejeitada:** N/A
- **Impacto:** LicenciamentoTramitacaoService, gestao-tramitacao, novo formulário arquivamento, filtro do dropdown por contexto.
- **Quem decidiu:** Gustavo + agente Cursor

---

### 06/08/2026 — sinaflor — HU133/HU134 Arquivar e Desarquivar

- **Decisão:** Implementar tipos 7 (Arquivar) e 8 (Desarquivar) reutilizando fila/rascunho/histórico. Disponibilidade via acoesDisponiveis. Arquivar: GO/GA, despacho+anexo, status Arquivado. Desarquivar: GO/GA/Analista se Arquivado, restaura statusAnterior do último Arquivar. Bloquear 7+8 na mesma fila.
- **Motivo:** Atender HU133 e HU134 sem fluxo paralelo.
- **Alternativa rejeitada:** N/A
- **Impacto:** LicenciamentoTramitacaoService, gestao-tramitacao, tramitacao-arquivamento
- **Quem decidiu:** Ambos

---

### 06/08/2026 — sinaflor — Reaplicar HU133/HU134 na branch hu132

- **Decisão:** Reaplicado HU133/HU134 na branch feature/hu132 (com Vistoria). Tipos 7/8 via acoesDisponiveis; Arquivar GO/GA; Desarquivar GO/GA/Analista; bloqueio 7+8; status Arquivado ou statusAnterior do último Arquivar.
- **Motivo:** Usuário desfez na branch errada; reimplementar na branch atualizada.
- **Alternativa rejeitada:** N/A
- **Impacto:** LicenciamentoTramitacaoService, gestao-tramitacao, tramitacao-arquivamento na branch hu132
- **Quem decidiu:** Ambos

---

### 07/08/2026 — sinaflor — Corrigir alerta e layout Arquivar/Desarquivar

- **Decisão:** Alertas Arquivar/Desarquivar devem usar o texto literal das HU133/HU134. Layout: neutralizar :host verde do textarea-despacho no formulário de arquivamento (só faz sentido na Análise ao lado dos analistas).
- **Motivo:** Texto inventado estava diferente da HU; bordas verdes do host do despacho apareciam como stubs no layout.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 07/08/2026 — fabrica — RAG fábrica: rerank ON + meta recall + citações

- **Decisão:** Hot path RAG da fábrica: RAG_RERANK=1 por default; 3ª recall por projeto/tags; pools ampliados; resposta com trecho/citacao/projeto; indexar_rapido grava projeto/tags/path. Desligar rerank com RAG_RERANK=0.
- **Motivo:** Melhorar precisão do agente na fábrica (citações + projeto + rerank) sem migrar para RAGFlow.
- **Alternativa rejeitada:** Manter rerank só offline e sem 3ª recall — pior hit em queries com sinaflor/lashmatch.
- **Impacto:** rag_retrieval.py, indexar_obsidian_chroma.py, indexar_rapido.py, rag-retrieval-fabrica.md, arquitetura-fabrica-ia.md
- **Quem decidiu:** Ambos

---

### 07/08/2026 — fabrica — RAG hot path: rerank ON + 3ª recall meta + citações

- **Decisão:** Pipeline :7332 = denso(48)+BM25(48)+meta projeto/tags(32) → RRF → affinity → bge-reranker-v2-m3 (RAG_RERANK=1 default). /buscar devolve trecho, citacao, projeto, path, tags. Filtro ?projeto=. Indexação grava projeto/tags/path; rglob em subpastas.
- **Motivo:** Afinar fábrica sem migrar para RAGFlow: mais acerto em notas de projeto (ex. sinaflor arquivar → tramitacao-arquivar-desarquivar.md#0) aceitando latência/RAM do CrossEncoder.
- **Alternativa rejeitada:** Manter só denso+BM25 sem rerank; ou adotar RAGFlow (~16GB) para uso solo.
- **Impacto:** rag_retrieval.py, indexar_obsidian_chroma.py, indexar_rapido.py, fabrica/rag-retrieval-fabrica.md, arquitetura-fabrica-ia.md
- **Quem decidiu:** Gustavo + agente

---

### 07/08/2026 — fabrica — RAG hot path: rerank ON + 3ª recall meta + citações

- **Decisão:** Pipeline :7332 = denso(48)+BM25(48)+meta projeto/tags(32) → RRF → affinity → bge-reranker-v2-m3 (RAG_RERANK=1 default). /buscar devolve trecho, citacao, projeto, path, tags. Filtro ?projeto=. Indexação grava projeto/tags/path; rglob em subpastas.
- **Motivo:** Afinar fábrica sem migrar para RAGFlow: mais acerto em notas de projeto (ex. sinaflor arquivar → tramitacao-arquivar-desarquivar.md#0) aceitando latência/RAM do CrossEncoder.
- **Alternativa rejeitada:** Manter só denso+BM25 sem rerank; ou adotar RAGFlow (~16GB) para uso solo.
- **Impacto:** rag_retrieval.py, indexar_obsidian_chroma.py, indexar_rapido.py, fabrica/rag-retrieval-fabrica.md, arquitetura-fabrica-ia.md
- **Quem decidiu:** Gustavo + agente

---

### 07/08/2026 — fabrica — App Runner RAG: 4 vCPU / 8GB + rerank ON

- **Decisão:** App Runner fabrica-rag em 4 vCPU (4096) / 8 GB (8192) com RAG_RERANK=1. Índice sync S3 + imagem ECR com hybrid+meta+rerank. Validado: /buscar sinaflor arquivar retorna tramitacao-arquivar-desarquivar.md.
- **Motivo:** Rerank bge + MiniLM + Chroma estoura 4GB; App Runner só oferece 8GB a partir de 4 vCPU.
- **Alternativa rejeitada:** Manter 1 vCPU/4GB com RAG_RERANK=1 (OOM / internal system error) ou 2 vCPU/8GB (combinação inválida no App Runner).
- **Impacto:** aws-rag/terraform/terraform.tfvars, custo App Runner sobe; MCP Cursor continua no App Runner.
- **Quem decidiu:** Gustavo + agente

---

### 07/08/2026 — fabrica — UI web do RAG no App Runner (/)

- **Decisão:** UI HTML estática em aws-rag/static/index.html servida em GET / do App Runner (mesma origem que /buscar). /health enriquecido com chunks, rerank, pools, pipeline. Histórico/latência só no localStorage do browser.
- **Motivo:** Caminho mais fácil sem Firebase: zero CORS, um build-push publica a tela.
- **Alternativa rejeitada:** Firebase Hosting separado (CORS + project ID).
- **Impacto:** indexar_obsidian_chroma.py, aws-rag/Dockerfile, aws-rag/static/index.html, fabrica/aws-rag-app-runner.md
- **Quem decidiu:** Gustavo + agente

---

### 07/08/2026 — fabrica — App Runner crash = CRLF no entrypoint.sh

- **Decisão:** Causa do 'internal system error' recente: entrypoint.sh com CRLF (Windows) — Linux falha com 'exec /app/entrypoint.sh: no such file or directory'. Corrigido para LF + sed no Dockerfile. Rerank permanece OFF no App Runner. UI validada em docker local (health.ui=true).
- **Motivo:** Reprodução local do container mostrou o erro real; App Runner mascara como internal system error.
- **Alternativa rejeitada:** Continuar reiniciando com a mesma imagem CRLF; ou culpar só OOM do rerank.
- **Impacto:** aws-rag/entrypoint.sh, aws-rag/Dockerfile, fabrica/aws-rag-app-runner.md
- **Quem decidiu:** Gustavo + agente

---

### 07/08/2026 — fabrica — UI RAG App Runner no ar (fix CRLF)

- **Decisão:** UI RAG no ar em https://gmnxgbtjy9.us-east-1.awsapprunner.com/ — causa dos crashes era CRLF no entrypoint.sh. Imagem LF publicada; health ui=true, chunks=2079, rerank=false no App Runner.
- **Motivo:** Docker local reproduziu 'exec entrypoint.sh: no such file'; App Runner mascarava como internal system error.
- **Alternativa rejeitada:** Continuar redeploy da imagem com entrypoint CRLF.
- **Impacto:** aws-rag/entrypoint.sh LF, Dockerfile sed, static/index.html
- **Quem decidiu:** Gustavo + agente

---

### 07/08/2026 — setmatch — Aulas online/presencial, professor, torneio dinâmico e perto de mim

- **Decisão:** Coleção aulasPublicadas com role professor no painel /clube; tab Aulas ONLINE/PRESENCIAL; torneio-novo persiste formatoChaves/estrutura/grupos/formatoPartida (preview textual, sem motor de chave); Perto de mim com expo-location + Haversine 25km em /(tabs)/proximos; matrículas listam com donoUid + rules isDonoClube; TAB_BAR_CLEARANCE unificado.
- **Motivo:** Alinhar Figma Aulas/Torneios-Admin, desbloquear matrícula admin (permission-denied) e descoberta geográfica sem Geoqueries Firestore.
- **Alternativa rejeitada:** GeoFirestore / geohash nativo; geração automática completa de árvore de confrontos nesta entrega.
- **Impacto:** Novas rotas aulas-publicar, aula/[id], proximos; schema torneios e usuarios/clubes lat/lng; seed professor Rodrigo Patah.
- **Quem decidiu:** agente+usuario

---

### 07/08/2026 — setmatch — Aulas: listar por professor e filtrar por esporteAtivo

- **Decisão:** ONLINE lista cards de professor (não aulas soltas); toque abre /aula/curso/[donoUid] com módulos→aulas→player. Tudo filtrado por EsporteContext.esporteAtivo. PRESENCIAL lista clubes/quadras do esporte.
- **Motivo:** Escala com vários professores e mantém consistência com o esporte escolhido no app.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** usuario+agente

---

### 07/08/2026 — setmatch — Upload de vídeo de aula no Firebase Storage

- **Decisão:** Professor envia vídeo pela galeria → Storage path aulas/{uid}/; player nativo expo-av. YouTube só como demo/placeholder. Rules storage deployadas (200MB video/*).
- **Motivo:** Aula paga não pode depender de YouTube público; precisa conteúdo hospedado no app.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** usuario+agente

---

### 07/08/2026 — setmatch

- **Decisão:** Aula online paga: aluno paga via MP (tipo aula_online + aulaPublicadaId) ou pede liberação (pagamento pendente + chat). Professor libera no financeiro por donoUid. Feed: foto, comentarios subcoleção, compartilhar in-app (chat) e fora (gate instalar app / deep link post).
- **Motivo:** Usuario pediu fluxo de pedir/pagar aula, descoberta de proximos, e feed com comentario/foto/share externo exigindo app.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 07/08/2026 — setmatch

- **Decisão:** Aula online paga: aluno paga via MP (tipo aula_online + aulaPublicadaId) ou pede liberação (pagamento pendente + chat). Professor libera no financeiro por donoUid. Feed: foto, comentarios, compartilhar in-app e fora (instalar app).
- **Motivo:** Usuario pediu fluxo pedir/pagar aula, proximos e feed social completo.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 07/08/2026 — setmatch

- **Decisão:** Feed social + aula online: pagar MP ou pedir liberacao; proximos na Home; post com foto/comentario/share externo exige app
- **Motivo:** Pedido do usuario sobre liberar/pagar aula, achar pessoas/quadras e feed completo
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 07/08/2026 — setmatch

- **Decisão:** Torneio single-elim vivo em torneios/{id}/confrontos (sorteio+byes+avançar). Perfil com H2H/histórico/badges. Busca avançada /buscar. VS com probabilidade logistic (win rate+H2H+nível). Rules: confrontos + onlyStatsBump V/D.
- **Motivo:** Pedido do usuario com padrao de mercado tennis/padel (chave de clube, perfil competitivo, matchup %).
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 07/08/2026 — setmatch — Admin vê torneios; aluno sem VS; matrículas sempre visíveis

- **Decisão:** 1) /clube/torneios lista torneios por donoUid. 2) Aba Aulas PRESENCIAL lista todas as matrículas do jogador (sem filtro esportes do clube). 3) /clube/alunos usa FlatList única com formulário no header (scroll contínuo). 4) Perfil do aluno via clube abre com contexto=aluno_clube e esconde VsCard/H2H/convidar.
- **Motivo:** Admin não conseguia abrir torneio criado; matrícula sumia pelo filtro de esporte; lista de alunos ficava em área minúscula; perfil competitivo não faz sentido clube→aluno.
- **Alternativa rejeitada:** N/A
- **Impacto:** UX admin e aluno; rota nova /clube/torneios; query param contexto no perfil público.
- **Quem decidiu:** Ambos

---

### 07/08/2026 — setmatch — Inscrição torneio + chave liberada pelo admin

- **Decisão:** Inscrição cria inscritos/{uid} + increment totalInscritos (rules onlyTotalInscritosBump). Lista de inscritos pública no detalhe. Admin libera chave via gerarChaveamento (chaveLiberada:true) em /clube/torneios ou /torneio/[id]; jogadores veem chave após liberação.
- **Motivo:** Inscrição falhava por permission-denied; produto exige ver inscritos e chave só após sorteio do admin.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 07/08/2026 — setmatch — Chaveamento horizontal estilo FotMob

- **Decisão:** Componente ChaveamentoBracket: ScrollView horizontal com colunas por rodada (Oitavas→Quartas→Semi→Final), setas entre fases, cards alinhados em árvore (fase seguinte entre os dois confrontos). Referência: FotMob / apps de esporte.
- **Motivo:** Pedido do usuário: chave passando para o lado, não lista vertical.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 07/08/2026 — setmatch — Aula online só por mensagem; combo de clube com busca

- **Decisão:** Aula paga online: único CTA 'Mensagem para liberar' (chat + pedido no financeiro). ClubeSwitcher virou combo/modal com pesquisa por nome/cidade e filtros Todos / Perto de mim (cidade do perfil) / Meus clubes.
- **Motivo:** Pedido do usuário: liberação só na conversa; seleção de clube mais usável com busca e perto de mim.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 07/08/2026 — setmatch — PWA Setmatch instalável via Firebase Hosting

- **Decisão:** Expo web static → dist-web + manifest/SW/ícones (copy-pwa-assets). Página pública /baixar. Hosting setmatch-app-fabrica.web.app. Scripts npm run export:web e deploy:web.
- **Motivo:** Usuário pediu PWA instalável por link sem loja.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 08/08/2026 — setmatch — Compliance App Store/Play — termos, privacidade, excluir conta

- **Decisão:** Setmatch segue o padrão LashMatch/Cortejo: páginas públicas /privacy /terms /suporte no Hosting; consentimento obrigatório no login/cadastro/admin; Perfil e Painel com Sair + Excluir conta; Cloud Function excluirConta (southamerica-east1) com wipe Firestore/Storage/Auth; idade mínima 13; ITSAppUsesNonExemptEncryption false no app.json.
- **Motivo:** Exigências Apple/Google/LGPD — mesma checklist que permitiu publicar LashMatch e Cortejo.
- **Alternativa rejeitada:** N/A
- **Impacto:** URLs legais para App Store Connect / Play Console; exclusão permanente via Bearer ID token; EXPO_PUBLIC_EXCLUIR_CONTA_URL no .env.
- **Quem decidiu:** agente

---

### 08/08/2026 — setmatch — Migração telas auth/perfil/painel para useT i18n

- **Decisão:** Telas perfil, login, cadastro, admin-login, esqueci-senha, AuthSocialRow e clube/painel passam a usar useT() com chaves existentes em i18n/locales/pt-BR.ts (espelhadas em en-US/es). Strings sem chave (ex.: Gerenciar, Editar clube, Modalidades) ficam hardcoded até haver key.
- **Motivo:** Infra i18n já existia; UI ainda tinha PT hardcoded. Evitar inventar keys novas.
- **Alternativa rejeitada:** N/A
- **Impacto:** Auth, perfil e painel do clube respeitam idioma do LocaleContext.
- **Quem decidiu:** agente

---

### 08/08/2026 — Setmatch i18n — telas onboarding/wizard/tabs com useT

- **Decisão:** Migração de strings user-facing para useT() com chaves de i18n/locales/pt-BR.ts. BottomNav já pronto. Onboarding passou a guardar keys no constants/onboarding.ts. Esportes traduzidos no call site (esporte.*). WizardLayout defaults Continuar/whyInfo via t(). Strings sem chave correspondente foram mantidas em PT.
- **Motivo:** A definir
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---
### 08/08/2026 — setmatch — Migração telas auth/perfil/painel para useT i18n

- **Decisão:** Telas perfil, login, cadastro, admin-login, esqueci-senha, AuthSocialRow e clube/painel usam useT() com chaves de i18n/locales/pt-BR.ts. Sem inventar keys — strings sem chave ficam hardcoded.
- **Motivo:** Infra i18n pronta; UI ainda tinha PT fixo.
- **Alternativa rejeitada:** N/A
- **Impacto:** Auth, perfil e painel do clube seguem LocaleContext.
- **Quem decidiu:** agente

---

### 08/08/2026 — setmatch — i18n pt-BR / en-US / es com LocaleContext

- **Decisão:** Setmatch usa LocaleProvider + dicionários em i18n/locales (pt-BR padrão, en-US, es), persistido em AsyncStorage @setmatch/locale. Seletor no Perfil (LanguagePicker). Hook useT()/useLocale(). Telas principais (tabs, auth, onboarding, wizard, painel) usam t('chave').
- **Motivo:** Permitir trocar idioma do app inteiro para lojas internacionais e usuários multilíngues, sem lib pesada.
- **Alternativa rejeitada:** N/A
- **Impacto:** Novas strings devem entrar nos 3 arquivos de locale. Fallback pt-BR se chave faltando.
- **Quem decidiu:** agente

---

### 08/08/2026 — setmatch — ES ¿¡ correto + EAS preview + ranking rules

- **Decisão:** Espanhol mantém ¿ e ¡ (norma). Ajustes pontuais de ¡ em boas-vindas/CTA. EAS update branch preview publicado. Hosting redeployado. Rules ranking: create admin|professor; update dono|membros; classificacao write auth.
- **Motivo:** Usuário validou ES na tela; pediu update preview + deploy + docs/rank enquanto offline.
- **Alternativa rejeitada:** N/A
- **Impacto:** OTA preview; PWA atualizado; menos permission-denied em ranking para professor/membros.
- **Quem decidiu:** agente

---

### 08/08/2026 — setmatch — Propagar foto/nome do perfil nos docs denormalizados

- **Decisão:** Ao salvar perfil (updatePerfil / wizard), chamar propagarPerfilPublico para atualizar fotoUrl/nome em desafios, amizades, posts, comentarios, conversas.fotos, solicitacoes, classificacao, inscritos e confrontos. Conversas passam a guardar mapa fotos e a UI de mensagens/notificacoes usa Avatar com uri.
- **Motivo:** Foto e nome estavam denormalizados nas coleções sociais; só usuarios/{uid} era atualizado, então desafios e chats antigos ficavam com avatar velho.
- **Alternativa rejeitada:** Buscar sempre usuarios/{uid} em tempo real em cada lista (mais leituras e latência).
- **Impacto:** services/propagarPerfil.ts, AuthContext, mensagens.ts, useConversas, mensagens/notificacoes UI, firestore.rules (comentarios+solicitacoes update), firestore.indexes fieldOverrides collection group
- **Quem decidiu:** Agente + usuario

---

### 08/08/2026 — setmatch — Stripe Checkout + Connect Express no Setmatch

- **Decisão:** Setmatch passa a cobrar via Stripe Checkout (card; PIX se habilitado no Dashboard, senão fallback cartão). Dono do clube conecta conta com Stripe Connect Express no Financeiro; se charges_enabled, destination charge + fee opcional. Secrets em functions/.env STRIPE_SECRET_KEY.
- **Motivo:** Pedido do usuário: integrar Stripe com chaves test e plug fácil da conta do clube; visão global.
- **Alternativa rejeitada:** Manter só Mercado Pago (limitado globalmente) ou exigir PIX antes de shipar
- **Impacto:** functions/src/stripeHandlers.ts, pagamentosSync.ts, utils/stripeCheckout.ts, clube/financeiro, app/pagamento/*, deploy southamerica-east1
- **Quem decidiu:** Usuario + agente

---

### 08/08/2026 — setmatch — Solicitar professor + telefone internacional

- **Decisão:** Formulário /(auth)/solicitar-acesso para professor e admin_clube com coleção solicitacoesAcesso. Telefone global via PhoneInput (DDI + DDD) no wizard, perfil, onboarding admin e editar clube; WhatsApp normaliza com código do país.
- **Motivo:** App global + solicitação explícita de professor com celular internacional.
- **Alternativa rejeitada:** Só WhatsApp sem formulário / telefone só BR
- **Impacto:** PhoneInput, telefoneInternacional, solicitar-acesso, firestore.rules solicitacoesAcesso, wizard/perfil/clube
- **Quem decidiu:** Usuario + agente

---

### 08/08/2026 — setmatch — Suporte in-app WhatsApp + naoLidas em conversas/notificacoes

- **Decisão:** Tela /ajuda com WhatsApp 5519989632897 (SUPPORT_WHATSAPP). Ao enviar mensagem, incrementa conversas.naoLidas.{uidDestinatario}; ao abrir chat zera. Badges em Notificacoes (aba Mensagens), BottomNav, sino Home/Perfil/Trofeu e painel clube/professor.
- **Motivo:** Usuario pediu area de suporte no app e indicador visual de notificacao de mensagem para jogador, professor e dono de clube.
- **Alternativa rejeitada:** N/A
- **Impacto:** app/ajuda.tsx, constants/support.ts, services/mensagens.ts, hooks/useConversas.ts, notificacoes/mensagens/BottomNav/painel
- **Quem decidiu:** Usuario + agente

---

### 09/08/2026 — setmatch — Stripe subscription + promo % por meio

- **Decisão:** Ciclo mensal com cartão usa Checkout mode subscription; PIX mensal continua payment one-shot. Admin grava descontoPixPercent/descontoCartaoPercent em ranking/aulas/torneio; jogador escolhe meio via pagarComEscolhaDeMeio e vê o % off. Webhook invoice.paid renova vigenteAte.
- **Motivo:** Pedido do usuário: cobrança recorrente real e promoção visível por meio de pagamento.
- **Alternativa rejeitada:** Manter só payment + vigenteAte manual; um único Checkout com PIX+cartão e preços diferentes (Stripe não permite preço por método na mesma session).
- **Impacto:** functions criarCheckoutStripe/webhook; utils checkoutComMeio/precoPagamento; telas admin ranking-novo, aulas-regras, torneio-novo; fluxos jogador trofeu/torneio/aulas/pagamentos
- **Quem decidiu:** Ambos

---

### 09/08/2026 — cortejo — Sidebar desktop web com scroll vertical

- **Decisão:** WebDesktopSidebar: ScrollView com minHeight:0 + overflowY:auto no web, showsVerticalScrollIndicator ligado; brand/logout fora do scroll (flexShrink 0). Só desktop web.
- **Motivo:** Telas baixas cortavam Configurações/Links do menu lateral.
- **Alternativa rejeitada:** N/A
- **Impacto:** Hosting cortejo-app; mobile nativo sem mudança
- **Quem decidiu:** Ambos

---

### 12/08/2026 — LashMatch — Web: Meu plano/Pagamentos com volta + guia PDF só pós-assinatura

- **Decisão:** 1) PlanoAccessRedirect não trata /planos?stay=1 como paywall — só plano-escolha força replace tabs. Meu plano e Pagamentos usam voltarParaInicio (replace /(tabs)), não router.back(). 2) WhatsAppProprioPlanExplainer (paywall) sem link do guia PDF; guia só em StatusCard/ConnectGuide com ownPlan=true. Mesmo padrão no Cortejo.
- **Motivo:** Na web, histórico vazio faz back falhar; redirect global expulsava assinante de Meu plano. Guia completo não deve aparecer antes de assinar WhatsApp próprio.
- **Alternativa rejeitada:** Manter router.back() e redirect em qualquer /planos; mostrar guia no Explainer do paywall
- **Impacto:** LashMatch web navegação Meu plano/Pagamentos; LM+Cortejo copy/UI WhatsApp próprio
- **Quem decidiu:** usuario+agente

---

### 12/08/2026 — LashMatch — Link PC WhatsApp = LashMatch web /config/whatsapp

- **Decisão:** shareWebAppLoginLink no LashMatch copia WEB_APP_WHATSAPP_SETUP_URL = {PUBLIC_WEB_BASE}/config/whatsapp (produção: https://lashmatch.com.br/config/whatsapp). Copy Meta orienta: abrir no PC → LashMatch web na seção WhatsApp do studio → terminar conexão/cartão.
- **Motivo:** Usuária deve acessar o web do LashMatch e concluir na seção WhatsApp do salão, não um link genérico ou da Meta.
- **Alternativa rejeitada:** Copiar só a home do web sem deep link
- **Impacto:** Mobile → PC setup WhatsApp próprio
- **Quem decidiu:** usuario+agente

---

### 12/08/2026 — LashMatch — Meta setup só desktop + Pagamentos não cai no Home

- **Decisão:** isWhatsAppMetaSetupAllowed = web E !isMobileWebBrowser (PWA/Android web bloqueados). Banner usa setupAllowed. Pagamentos: Tabs sem href:null (tabBarButton null); MoreMenu push atrasado; href /pagamento; voltarOuInicio.
- **Motivo:** PWA Android era tratado como computador; menu Pagamentos caía no Home por linking.
- **Alternativa rejeitada:** Tratar qualquer Platform.OS===web como PC; href:null nas tabs ocultas
- **Impacto:** LashMatch web mobile + Cortejo WhatsApp setup
- **Quem decidiu:** usuario+agente

---

### 12/08/2026 — LashMatch — Pagamentos fora das tabs (/pagamentos)

- **Decisão:** Tela de Pagamentos fora das tabs em app/pagamentos.tsx (stack), como /planos. Menu e Perfil apontam /pagamentos. (tabs)/pagamento só Redirect. Menu sempre mostra Pagamentos (web sem checkout → aviso use o app).
- **Motivo:** No web, rota nas tabs ocultas caía no Home ao abrir Pagamentos.
- **Alternativa rejeitada:** Manter pagamento só como tab com href null/tabBarButton null
- **Impacto:** Navegação web LashMatch
- **Quem decidiu:** usuario+agente

---

### 12/08/2026 — sinaflor — Ajustes UX tramitação Vistoria/Análise

- **Decisão:** 1) Ordem tipos avaliação na Vistoria: POA Amazônia por último via sort em listarTiposAvaliacao(idTipoTramite=2). 2) Botão Finalizar no formulário de cadastro/edição (salva + modal + gestao-projetos). 3) Mensagem ATENÇÃO única (texto da análise técnica obrigatória) para Análise e Vistoria. 4) Checkbox manter processo aberto herda da última tramitação e sincroniza todas do rascunho.
- **Motivo:** Alinhamento com protótipo/imagem e regras de UX pedidas pelo usuário.
- **Alternativa rejeitada:** N/A
- **Impacto:** Backend: LicenciamentoTramitacaoService. Front: gestao-tramitacao, tramitacao-analise-projeto, tramitacao-arquivamento.
- **Quem decidiu:** usuario+agente

---

### 12/08/2026 — sinaflor — Situação múltipla na gestão de projetos

- **Decisão:** Situação na gestão de licenciamento passa a listar todos os status gerados pelas tramitações ativas (únicos, ordem cronológica), com reticências e tooltip no padrão dos RTs. No finalizar, cada item grava seu próprio statusNovo; statusLic do processo permanece o último para regras/ações.
- **Motivo:** Pedido do cliente: não usar só o último status na coluna Situação.
- **Alternativa rejeitada:** N/A
- **Impacto:** LicenciamentoTramitacaoService, GestaoLicenciamentoResource, TramiteLicRepository, LicenciamentoExploracaoListagemDTO.situacoes, gestao-licenciamento-exploracao (coluna Situação).
- **Quem decidiu:** cliente

---

### 12/08/2026 — sinaflor — Sync manter aberto no histórico finalizado

- **Decisão:** Ao finalizar tramitação, FL_MANTER_ABERTO_UNIDADE do lote é propagado a todas as tramitações ativas. Ao listar histórico, alinha pelo flag da mais recente (exceto Desarquivar), corrigindo inconsistências já gravadas.
- **Motivo:** Cliente: se a última não mantém aberto, as anteriores não podem continuar com tag MANTER ABERTO.
- **Alternativa rejeitada:** N/A
- **Impacto:** LicenciamentoTramitacaoService + TramiteLicRepository.findAtivosByLicenciamento
- **Quem decidiu:** cliente

---

### 12/08/2026 — LashMatch — MoreMenu web: location.assign para Pagamentos

- **Decisão:** No web, menu Mais navega com window.location.assign(href). Hrefs limpos (/pagamentos, /estoque…). Pagamentos em stack /pagamentos.
- **Motivo:** push pós-Modal no Chrome Android descartava a rota e voltava ao Home.
- **Alternativa rejeitada:** router.push apos Modal com delay curto
- **Impacto:** LashMatch Android web/PWA
- **Quem decidiu:** usuario+agente

---

### 12/08/2026 — LashMatch — Android web: sem location.assign; sem flash de planos no boot

- **Decisão:** Navegação SPA com router.replace/push. assign(/) e assign no MoreMenu removidos — causavam remount, flash plano-escolha e volta ao Home. Boot: spinner até plano estável; tabs debouncem paywall 450ms.
- **Motivo:** Reload completo reavaliava auth lento e redirecionava paywall→home.
- **Alternativa rejeitada:** window.location.assign para forçar navegação no Android web
- **Impacto:** LashMatch Android web/PWA
- **Quem decidiu:** usuario+agente

---

### 12/08/2026 — lashmatch — Meu plano e Pagamentos no EAS nativo

- **Decisão:** /planos com assinante sempre mostra Meu plano (nao depende de stay). MoreMenu nativo fecha Modal e navega apos 320ms; web continua navigate-before-close. Pagamentos em /config/pagamentos.
- **Motivo:** EAS: spinner eterno (temAcesso && !stay) e navegacao engolida pelo Modal.
- **Alternativa rejeitada:** Continuar exigindo stay=1 e navegar com Modal aberto no nativo
- **Impacto:** OTA production corrige Meu plano e Pagamentos no app instalado via EAS Update.
- **Quem decidiu:** Ambos

---

### 12/08/2026 — lashmatch — Pagamentos = /assinatura; menu Modal pendingHref

- **Decisão:** Menu Pagamentos aponta para /assinatura (tela completa). /config/pagamentos e /pagamentos só Redirect. MoreMenu nativo navega após Modal fechar via pendingHref.
- **Motivo:** Rota /config/pagamentos + Modal + params stay quebravam abertura no nativo/Expo Go.
- **Alternativa rejeitada:** N/A
- **Impacto:** Pagamentos abre no Expo Go, EAS e web; Meu plano não trava loading branco no Expo Go.
- **Quem decidiu:** Ambos

---

### 13/08/2026 — lashmatch — EAS build+submit LashMatch 13/08/2026

- **Decisão:** Build production iOS+Android EAS concluídos (build 18 iOS / versionCode 6 Android). Submit iOS App Store OK. Android submit bloqueado sem Google Service Account em non-interactive.
- **Motivo:** Pedido do usuário: build e submit LashMatch
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 13/08/2026 — lashmatch — Versão store 1.0.5 + rebuild

- **Decisão:** Bump LashMatch para 1.0.5 (app.json version + android runtimeVersion/versionName/strings, package.json). Regenerar ícones do brand master. Novo build+submit iOS.
- **Motivo:** Train 1.0.4 fechado na Apple; usuário pediu 1.0.5 + ícone nas lojas
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 13/08/2026 — sinaflor — HU135 Solicitar Pagamento de Taxa/Guia

- **Decisão:** HU135 Solicitar Pagamento de Taxa/Guia (tipo 5): reusa tramitacao-arquivamento modo solicitar-pagamento; status AGUARDANDO_PAGAMENTO_TAXA; e-mail ON default; sem manter aberto; alerta RN16; disponível GO/GA/Analista em processo não arquivado.
- **Motivo:** Documento HU135 — acrescentar tramitação mantendo padrão existente.
- **Alternativa rejeitada:** N/A
- **Impacto:** LicenciamentoTramitacaoService, GestaoLicenciamentoResource, gestao-tramitacao, tramitacao-arquivamento. Nota fabrica/tramitacao-solicitar-pagamento-taxa.md
- **Quem decidiu:** usuario+agente

---

### 13/08/2026 — lashmatch — Native release 1.0.6

- **Decisão:** Bump LashMatch para 1.0.6 e EAS build+submit nativo (iOS auto-submit; Android build).
- **Motivo:** Usuário pediu nova versão nativa; 1.0.5 já submetida à Apple
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 14/08/2026 — health-quadra-tech — Trajeto: dois clientes (Next.js + Expo) e um Supabase

- **Decisão:** Produto Trajeto no repo health-quadra-tech. Web = Next.js App Router em apps/web (Vercel) para gestor e psicólogo. Mobile = Expo Router em apps/mobile (Expo Go) para paciente (primário) e psicólogo em campo. Pacote compartilhado de tokens/tipos. Backend único Supabase (Auth + Postgres RLS + Storage). Papel em tabela profiles, nunca em user_metadata. Gestor vê só KPIs operacionais, não conteúdo clínico.
- **Motivo:** PRD original era web-only; stakeholder pediu app nativo desde o início. Dashboard clínico é denso (tabelas, gráficos, sidebar) — Next.js. Paciente usa o celular (quiz, agendar, evolução). Expo-only no web degradaria o painel. Firebase fora da stack do projeto.
- **Alternativa rejeitada:** Expo único (web+mobile) ou só web sem app. Firebase/Firestore (proibido neste repo).
- **Impacto:** Monorepo apps/web + apps/mobile + packages/shared + supabase/. Vercel rootDirectory = apps/web. Schema e RLS desenhados para os dois clientes.
- **Quem decidiu:** Gustavo + agente (pedido explícito de app nativo)

---

### 14/08/2026 — health-quadra-tech — Supabase shoutloud + Vercel health-quadra-tech ligados ao Trajeto

- **Decisão:** Trajeto usa o único projeto Supabase da org shoutloud (ref slaexnytybmgphknwbat, us-west-2). Schema + RLS aplicados via MCP apply_migration. Web Vercel continua o projeto já linkado health-quadra-tech (prj_iFLoaS9YVo87wCyXGZMLfS8QFONd, team shoutloud) via CLI — MCP Vercel não listou projetos.
- **Motivo:** Usuário confirmou MCP Vercel e Supabase conectados. Projeto remoto estava vazio e saudável.
- **Alternativa rejeitada:** Criar outro projeto Supabase só para Trajeto; depender só do MCP Vercel (list_projects vazio nesta conta).
- **Impacto:** Env NEXT_PUBLIC_SUPABASE_* no app web; EXPO_PUBLIC_* no mobile. Root Directory Vercel precisa apontar para apps/web no próximo deploy.
- **Quem decidiu:** Gustavo (MCP conectado) + agente

---

### 14/08/2026 — health-quadra-tech — Vercel Root Directory apps/web em produção

- **Decisão:** Produção Vercel do Trajeto aponta para Next.js em apps/web: framework nextjs, rootDirectory apps/web, sourceFilesOutsideRootDirectory true, env NEXT_PUBLIC_SUPABASE_URL e ANON_KEY. Alias https://health-quadra-tech-shoutloud.vercel.app
- **Motivo:** O deploy anterior servia o HTML placeholder da raiz (0ms). O painel é Next.js.
- **Alternativa rejeitada:** Manter HTML estático na raiz; ou vercel.json com propriedade rootDirectory (inválida no schema da CLI)
- **Impacto:** CLI deploy --prod sobe o app (login, clínica, psico). GitHub shoutlouddev/health-quadra-tech continua ligado; push em main dispara rebuild. MCP Vercel ainda não lista o projeto.
- **Quem decidiu:** Gustavo

---

### 14/08/2026 — health-quadra-tech — Auth Supabase ligado em todas as telas web e mobile

- **Decisão:** Web e Expo usam a mesma conta Supabase: login/signup, RPC bootstrap_workspace e claim_patient_invite, telas leem/gravam Postgres com RLS, botão Voltar em todas as telas. Papel só em profiles. router.replace após login. Gestor no app é um aviso para usar a web.
- **Motivo:** Usuário pediu para sair do mock/localStorage e ligar auth + banco + navegação.
- **Alternativa rejeitada:** Manter mock + login por persona sem Auth; Firebase Auth.
- **Impacto:** apps/web (middleware, lib/auth, telas), apps/mobile (supabase persist, BackBar), RPCs no projeto slaexnytybmgphknwbat. Produção Vercel só atualiza após novo deploy.
- **Quem decidiu:** Gustavo + agente

---

### 14/08/2026 — health-quadra-tech — Confirmação de e-mail: Site URL Vercel + emailRedirectTo /auth/callback

- **Decisão:** Signup web e mobile passam emailRedirectTo para https://health-quadra-tech-shoutloud.vercel.app/auth/callback. A rota troca code/token_hash e chama finishSignup (bootstrap_workspace ou claim_patient_invite a partir de user_metadata). Site URL e Redirect allow list no dashboard Auth precisam apontar para a Vercel — o MCP não altera GoTrue. O remetente "Supabase Auth" só muda com SMTP customizado (Resend). Mobile nunca usa exp:// no redirect do e-mail.
- **Motivo:** Sem emailRedirectTo o GoTrue usa Site URL padrão localhost:3000. Sem allow list, o redirect customizado é ignorado.
- **Alternativa rejeitada:** Desligar confirmação de e-mail (inseguro). Firebase Auth (fora da stack).
- **Impacto:** apps/web/app/auth/callback, LoginForm, CadastroForm, mobile login/cadastro, NEXT_PUBLIC_SITE_URL, EXPO_PUBLIC_SITE_URL
- **Quem decidiu:** Cursor + Gustavo

---

### 14/08/2026 — health-quadra-tech — RLS helpers SECURITY DEFINER para evitar recursão em profiles

- **Decisão:** Helpers current_clinic_id/current_role/current_professional_id passam a SECURITY DEFINER com row_security off para a policy de profiles não recursar.
- **Motivo:** SELECT profiles via PostgREST retornava 500 mesmo com linha existente.
- **Alternativa rejeitada:** Desligar RLS em profiles ou confirmar e-mail no SQL.
- **Impacto:** Login web deixa de voltar para /login após senha correta. Migration 20260814150000.
- **Quem decidiu:** Cursor + Gustavo

---

### 14/08/2026 — health-quadra-tech — Nav por papel + fontes next/font e loading nas rotas

- **Decisão:** next/font no layout, React.cache em getProfile, loading.tsx nas rotas autenticadas. Menu do psicólogo passa a Pacientes e evolução.
- **Motivo:** Login e menus lentos: fonte bloqueante + roundtrip us-west-2 sem feedback. Screenshot do protótipo HTML mistura os 3 papéis; o app logado mostra só o papel da conta.
- **Alternativa rejeitada:** Manter @import do Google Fonts e navegar sem loading.tsx.
- **Impacto:** apps/web layout, globals.css, lib/auth.ts, loading.tsx, AppShell
- **Quem decidiu:** Cursor + Gustavo

---

### 14/08/2026 — health-quadra-tech — Supabase Trajeto em São Paulo (sa-east-1)

- **Decisão:** Novo projeto Supabase `trajeto` (ref fzttsuuzfauqkagscrwc) em sa-east-1. Schema reaplicado (core + insert + bootstrap + fix RLS). App/web/Vercel passam a usar esta URL. Contas do projeto Oregon não foram copiadas: usuário recria login. Projeto Oregon permanece como arquivo.
- **Motivo:** Região do projeto é imutável. Usuários no Brasil; us-west-2 era a maior causa de lentidão restante.
- **Alternativa rejeitada:** N/A
- **Impacto:** Latência BR cai; login antigo (Hotmail/Outlook/Gmail no Oregon) não vale no projeto novo. Site URL do Auth precisa ser setada no dashboard do projeto novo.
- **Quem decidiu:** Gustavo

---

### 14/08/2026 — health-quadra-tech — Signup clínica vs autônomo sem default

- **Decisão:** Cadastro de clínica exige escolha explícita (sem default autônomo). Papel vai em user_metadata.trajeto_role porque `role` conflita com o JWT. Sem papel válido, não assume psicólogo.
- **Motivo:** Formulário nascia com autônomo selecionado; nome da clínica preenchido não mudava o papel. Fallback finishSignup virava psicólogo se metadata.role se perdesse.
- **Alternativa rejeitada:** N/A
- **Impacto:** Conta clínica entra em /clinica (gestão). Autônomo entra em /psico. Conta Gmail atual já era gestor.
- **Quem decidiu:** Gustavo

---

### 14/08/2026 — health-quadra-tech — Vercel gru1 + shell persistente no Trajeto

- **Decisão:** Funções Vercel em gru1 (São Paulo) e layout (workspace) com menu persistente. Páginas só trocam o conteúdo.
- **Motivo:** Cada navegação era RSC da página inteira (AppShell no page) rodando em iad1 contra banco sa-east-1.
- **Alternativa rejeitada:** N/A
- **Impacto:** Clique no menu não remonta o chrome; roundtrip função↔Supabase fica na mesma região.
- **Quem decidiu:** Gustavo

---

### 14/08/2026 — health-quadra-tech — Trajeto — datas BR, validação visível e CRUD

- **Decisão:** Datas sempre dd/mm/aaaa (pt-BR). Formulários com noValidate e erro visível por campo obrigatório. CRUD editar/excluir em invoices, fee_schedules, professionals, appointments, patients e sessions. Migration 20260814160000 com policies DELETE.
- **Motivo:** Pedido do usuário: padrão brasileiro, validação visível e editar/excluir não só em recebimentos/convênios/profissionais.
- **Alternativa rejeitada:** Só HTML required + tooltip nativo; listas só com insert
- **Impacto:** apps/web forms+listas, apps/mobile cadastro/login/sessao/agendar, packages/shared/dates.ts, supabase 20260814160000_record_deletes.sql
- **Quem decidiu:** Usuário + agente

---

### 14/08/2026 — health-quadra-tech — Trajeto — web celular com menu e layout empilhado

- **Decisão:** Web no celular: botão ☰ abre o menu lateral, overlay fecha, campos empilham, tabelas rolam na horizontal. Lançamento a receber vira recebido pelo botão Recebido (ou Editar → Pago).
- **Motivo:** Usuário acessando Vercel no Chrome Android: menu sumia, campos flutuavam, tabela cortava Status.
- **Alternativa rejeitada:** Sidebar off-canvas sem botão — menu invisível no celular
- **Impacto:** apps/web/components/AppShell.tsx, globals.css, layout viewport, InvoiceManager
- **Quem decidiu:** Usuário + agente

---

### 14/08/2026 — health-quadra-tech — Agenda web Trajeto no layout Dia/Mês da fábrica

- **Decisão:** A agenda do psicólogo em /psico/agenda replica o layout Cortejo/LashMatch (DayStrip + DayHourTimeline no modo Dia; calendário compacto + lista no modo Mês), implementado em HTML/CSS Next.js com tokens sage/gold do Trajeto — sem react-native-calendars e sem paleta LashMatch. Grade em packages/shared/agenda.ts: passo 30 min, sessão 50 min, semana 8h–19h, sábado até 13h, domingo fechado. Toque no slot vazio abre o formulário com data/hora preenchidas.
- **Motivo:** Pedido para usar o mesmo layout de agenda dos outros projetos da fábrica, mantendo a identidade visual Trajeto.
- **Alternativa rejeitada:** Tabela semanal do protótipo HTML; lista simples de próximos horários; instalar react-native-calendars na web.
- **Impacto:** apps/web/components/agenda/AgendaBoard.tsx, packages/shared/agenda.ts, globals.css. Agendamento público do paciente (/p/agendar) ainda é lista de slots.
- **Quem decidiu:** Gustavo + agente

---

### 14/08/2026 — health-quadra-tech — Ícones do mockup Trajeto no menu e nas tabs

- **Decisão:** Ícones do prototipo Trajeto (SVG stroke 1.6) viraram o set único: web `components/Icon.tsx` na sidebar, menu do paciente, Voltar/Sair, agenda Dia/Mês e CTAs; app Expo usa os mesmos traços via react-native-svg (Expo Go) nas tabs e no BackBar.
- **Motivo:** O mockup já trazia ícones no menu; a UI real estava só com texto.
- **Alternativa rejeitada:** FontAwesome / ícones genéricos fora do mockup.
- **Impacto:** apps/web/components/Icon.tsx, AppShell, PatientShell, AgendaBoard, login/quiz/cadastro; apps/mobile/components/Icon.tsx + tabs.
- **Quem decidiu:** Gustavo + agente

---

### 14/08/2026 — health-quadra-tech — Lista de sessões SOAP separada da agenda

- **Decisão:** Notas SOAP têm rota /psico/sessoes no menu Sessões. Depois de salvar a nota, o app vai para essa lista. Também aparecem no painel do psicólogo e na ficha do paciente (#sessoes). Agenda só mostra horários (appointments), não notas. Login mobile usa grid 1fr para o card não ficar pela metade.
- **Motivo:** No celular o usuário registrava sessão e não via em lugar nenhum: o histórico só existia numa tabela larga dentro da ficha, sem redirect. O login escondia o painel visual mas mantinha grid 1fr 1fr.
- **Alternativa rejeitada:** Só mostrar sessões na ficha do paciente, ou misturar notas SOAP na grade da agenda.
- **Impacto:** Menu psicólogo: item Sessões. UX login no celular. Cards no lugar da tabela de sessões.
- **Quem decidiu:** Gustavo + agente Cursor

---

### 14/08/2026 — health-quadra-tech — Gráfico SVG GAD-7/PHQ-9 na carteira e na ficha

- **Decisão:** Gráfico de evolução é SVG no visual do mockup (GAD-7 ferrugem, PHQ-9 sage), em /psico/pacientes e na ficha. Eixo Y: escore alto embaixo (melhora sobe). Sem lib extra.
- **Motivo:** A lista não mostrava gráfico; a ficha só listava escores. Um ponto não desenha trajetória.
- **Alternativa rejeitada:** Lista de números sem SVG, ou lib de chart (recharts).
- **Impacto:** Pacientes e evolução deixa de ser só lista. Demo: série semanal no paciente Gabriel.
- **Quem decidiu:** Gustavo + agente Cursor

---

### 14/08/2026 — cortejo

- **Decisão:** Cortejo clientes: busca via filterClientsByQuery com normalizeForSearch (acentos); Editar cadastro usa /config/clientes?editId= e abre modal
- **Motivo:** Filtro vazio por acentos; botão Editar só listava clientes sem abrir ficha de edição
- **Alternativa rejeitada:** N/A
- **Impacto:** utils/client.ts, app/config/clientes.tsx, app/clientes/[id].tsx; OTA production 79daf281; EAS build+submit em andamento
- **Quem decidiu:** Ambos

---
### 14/08/2026 — health-quadra-tech — Agenda desktop semana de trabalho (estilo Teams, cores Trajeto)

- **Decisão:** Na web, /psico/agenda passa a ter duas UIs: abaixo de 1100px permanece Dia/Mês (DayStrip + timeline). A partir de 1100px, semana de trabalho (segunda a sexta) com trilho de mini-calendário à direita do menu ink, grade horária 8h–19h, linha do agora em ouro Trajeto, eventos em sage. Clique no vazio abre o compositor; clique no bloco abre o detalhe em gaveta. O menu lateral continua sendo a borda esquerda da tela — a grade não passa por baixo.
- **Motivo:** Pedido do usuário para deixar a agenda igual ao Calendário do Teams só em computador com tela grande, sem mudar o fluxo no telefone.
- **Alternativa rejeitada:** Usar react-native-calendars ou copiar o tema roxo do Teams. Também rejeitado aplicar a grade de semana no celular.
- **Impacto:** apps/web/components/agenda/AgendaDesktop.tsx + CSS em globals.css (@media min-width 1100px). Helpers mondayOf/workWeekKeys/layoutBlockOnWorkWeek em packages/shared/agenda.ts. Celular inalterado.
- **Quem decidiu:** Gustavo

---

### 15/08/2026 — health-quadra-tech — EAS Update só a partir de apps/mobile

- **Decisão:** EAS Update/Build do Trajeto rodam em apps/mobile. O app.json da raiz foi removido. Slug Expo alinhado ao projeto EAS já criado (@shoutloud/health-quadra-tech). expo-updates vive no workspace mobile, não na raiz.
- **Motivo:** eas update na raiz usou expo/AppEntry.js e procurou ../../App, que não existe. O app é Expo Router em apps/mobile.
- **Alternativa rejeitada:** Deixar EAS na raiz do monorepo ou criar um App.tsx falso só para o AppEntry.
- **Impacto:** Comando: cd apps/mobile; eas update --branch preview. Expo Go não recebe OTA — precisa de development/preview build.
- **Quem decidiu:** Gustavo

---

### 15/08/2026 — health-quadra-tech — eas update na raiz redireciona para apps/mobile

- **Decisão:** app.config.js na raiz do monorepo: se eas update/expo export rodar na raiz, redireciona o export para apps/mobile e grava dist na raiz. extra.eas.projectId vem do app.json do mobile — o CLI não recria um app Expo vazio.
- **Motivo:** O usuário roda eas update na raiz; o Metro usava expo/AppEntry e procurava App.tsx.
- **Alternativa rejeitada:** Criar App.tsx falso na raiz.
- **Impacto:** eas update --branch preview na raiz deixa de falhar com Unable to resolve ../../App. Comando canônico continua cd apps/mobile.
- **Quem decidiu:** Gustavo

---

### 15/08/2026 — health-quadra-tech — Mobile paridade web psico + clinica

- **Decisão:** O app Expo deixou de ter só Hoje/Sessão e um aviso para o gestor. Psicólogo tem abas Hoje, Agenda, Pacientes, Sessões e Financeiro (mais ficha e nota SOAP). Gestor entra em (clinica) com Painel, Equipe, Pacientes, Financeiro e Config. Mesmas tabelas Supabase da web.
- **Motivo:** Usuário pediu as mesmas funcionalidades do web no mobile para psicólogo e clínica.
- **Alternativa rejeitada:** Manter gestão só no computador e sessão rápida no celular.
- **Impacto:** EAS Update preview 8724d912-24a3-426f-aa95-85ff15354032. Login gestor vai para /(clinica).
- **Quem decidiu:** Usuário + agente

---

### 15/08/2026 — health-quadra-tech — Mobile grafico evolucao e menu do mockup

- **Decisão:** Mobile do psicólogo autônomo tem Painel, Agenda, Pacientes, Ficha & evolução (gráfico SVG GAD-7/PHQ-9) e Mais com Registrar sessão, Sessões e Financeiro. Gestor continua só com Painel, Equipe, Pacientes, Financeiro e Config — sem notas clínicas.
- **Motivo:** Mockup 07 Ficha & evolução e menu da imagem; autônomo não gerencia equipe.
- **Alternativa rejeitada:** Só números GAD-7 → PHQ-9 sem gráfico; misturar equipe na conta autônoma.
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 15/08/2026 — health-quadra-tech — Abas Registrar sessao e Ficha evolucao

- **Decisão:** Abas do psicólogo no mobile: Painel, Agenda, Pacientes, Ficha & evolução, Registrar sessão. Ficha & evolução tem menu de pacientes (item dourado) + gráfico + pré-ficha + histórico, como o mockup 07.
- **Motivo:** Usuário pediu que onde era Sessão fosse Registrar sessão e menu igual ao mockup de Ficha & evolução.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 15/08/2026 — health-quadra-tech — Gestor atende + convite de psicólogo + agenda da clínica

- **Decisão:** O dono (gestor) ganha linha em professionals (bootstrap + ensure_gestor_professional + backfill) e acessa o chapéu Psicólogo na web e no app, com RLS clínico ainda em current_professional_id(). Psicólogo da equipe entra por professionals.invite_token + claim_professional_invite (não cria clínica nova). Agenda consolidada em /clinica/agenda e (clinica)/agenda.
- **Motivo:** Caso brasileiro: dono também atende; adicionar profissional não criava login; gestor precisa ver horários de todos sem ler SOAP alheio.
- **Alternativa rejeitada:** Mudar o papel JWT ou deixar gestor ler sessions da clínica. Recusar: quebra sigilo. Segundo perfil/auth por chapéu: excesso para MVP.
- **Impacto:** Migration 20260815180000; web AppShell dual-nav; /equipe/cadastro; mobile HatSwitch + cadastro-equipe; EAS preview.
- **Quem decidiu:** produto + agente

---

### 15/08/2026 — health-quadra-tech — Convite de profissional com papel Psicólogo ou Gestor

- **Decisão:** Tela Profissionais (web e app) usa o card Adicionar novo profissional do mockup: Nome completo, CRP, Papel de acesso (Psicólogo / Gestor) e botão Enviar convite de acesso. Coluna professionals.invite_role persiste o papel; claim_professional_invite cria profiles.role a partir dela.
- **Motivo:** O mockup pedia o formulário à direita com escolha de papel; convite de gestor não podia continuar gravando sempre psicologo.
- **Alternativa rejeitada:** Só mudar o visual e ignorar o papel Gestor; ou reusar specialty em vez de invite_role.
- **Impacto:** Migration 20260815200000 aplicada no projeto trajeto. Web /clinica/profissionais em duas colunas. App (clinica)/profissionais com o mesmo formulário.
- **Quem decidiu:** Usuário + agente

---

### 15/08/2026 — health-quadra-tech — Relatório clínico e operacional + seed demo

- **Decisão:** Relatório clínico (ficha + GAD-7/PHQ-9 + quiz + SOAP) só para o psicólogo da carteira; relatório da clínica só com KPIs/equipe/financeiro, sem SOAP. Texto canônico em packages/shared/report.ts. Web: página + window.print(). Mobile: tela com cards + Share.share (Expo Go, sem lib nativa de PDF). Seed demo em supabase/seed_demo_clientes.sql para Marina, Clara, Pedro e Ana.
- **Motivo:** Mostrar ficha, evolução e exportar relatório na reunião com o cliente, no mesmo padrão visual web/app, sem quebrar o Expo Go nem o sigilo clínico do gestor.
- **Alternativa rejeitada:** PDF nativo (expo-print / react-native-html-to-pdf) — exige dev build. Relatório único com SOAP para o gestor — viola RLS e a regra de dois chapéus.
- **Impacto:** Rotas /psico/pacientes/[id]/relatorio e /clinica/relatorio na web; (psico)/relatorio e (clinica)/relatorio no app. Contas @trajeto.dev passam a ter sessões, escalas, quiz, agenda e invoices.
- **Quem decidiu:** Gustavo + agente

---

### 15/08/2026 — health-quadra-tech — Agenda mobile no padrão fábrica Dia/Mês

- **Decisão:** Agenda nativa do Trajeto no padrão fábrica: react-native-calendars (Calendar, firstDay=1, multi-dot, LocaleConfig pt-BR) + DayStrip + DayHourTimeline (slots 30 min / sessão 50 min de packages/shared/agenda.ts). Visão Dia/Mês, card único, tokens gold/sage. Psicólogo agenda no slot vazio; gestor só vê; paciente escolhe dia no calendário + horários livres. Sem Wix Timeline.
- **Motivo:** Só o mobile estava fora do padrão Cortejo/LashMatch (lista de chips). A web já tinha Dia/Mês.
- **Alternativa rejeitada:** Manter faixa de dias + lista; ou usar o componente Agenda/Timeline da Wix (não gera slots vazios no passo 30 min).
- **Impacto:** Telas (psico)/agenda, (clinica)/agenda e (patient)/agendar. Dependência react-native-calendars (Expo Go).
- **Quem decidiu:** Gustavo + agente

---

### 15/08/2026 — health-quadra-tech — Trajeto mobile volta para Expo SDK 54

- **Decisão:** apps/mobile usa Expo SDK 54 (expo-router ~6.0.24, RN 0.81.5, React 19.1.0). Overrides no package.json da raiz travam expo/react-native no 54. expo-router NUNCA ~54.x neste SDK.
- **Motivo:** Expo Go da App Store e Play Store continua no SDK 54. SDK 57 não abre no iPhone nem no Android da loja; o QR da EAS Update também não é Expo Go. Alinhar com Cortejo/LashMatch para o mesmo fluxo: npx expo start + QR.
- **Alternativa rejeitada:** Manter SDK 57 e pedir Expo Go 57 (Android APK do Go / eas go + TestFlight no iOS) ou build preview APK do Trajeto.
- **Impacto:** Metro QR abre no Expo Go da loja em iPhone e Android, igual aos outros apps da fábrica. Updates EAS antigos do runtime 57 não servem mais para Go.
- **Quem decidiu:** Gustavo

---

### 15/08/2026 — fabrica — RAG Chroma recriado e sync AWS us-east-1 (2026-08-15)

- **Decisão:** Banco Chroma local recriado com indexar_rapido.py --recriar-banco (2387 chunks) e enviado ao S3/App Runner via sync-push.ps1 -SkipIndex -Region us-east-1. INDEX.md (catálogo/rank das notas), Trajeto e rankings Setmatch entram no índice. Delete de chunks passou a usar path para não colidir dois INDEX.md.
- **Motivo:** HNSW local estava corrompido (crash no indexar). App Runner consome o dump do S3 em us-east-1; sa-east-1 não tem App Runner.
- **Alternativa rejeitada:** Só indexar incremental sem recriar, ou sync com região default sa-east-1 do script
- **Impacto:** MCP rag_buscar volta a refletir notas atuais da fábrica e do Trajeto após warmup do App Runner
- **Quem decidiu:** Gustavo + agente

---

### 17/08/2026 — setmatch — App Store 5.1.1 + 3.1.1 sem IAP

- **Decisão:** Corrigir recusa App Store 5.1.1 com purpose string da galeria (exemplo: foto de perfil em Edit Profile / post na Home). Para 3.1.1 sem IAP: no iOS ocultar aulas online pagas (preço, cadeado, chat para liberar). Stripe permanece para serviço presencial (clube, ranking, torneio).
- **Motivo:** Apple rejeitou 1.0 (2): purpose string genérica e vídeo pago fora da IAP. Usuário não quer outro meio de pagamento.
- **Alternativa rejeitada:** Adicionar Apple In-App Purchase para vídeos pagos
- **Impacto:** app.json infoPlist + expo-image-picker; utils/storeCompliance.ts; aulas.tsx, aula/[id], aula/curso; buildNumber 3 (precisa binary novo, não OTA)
- **Quem decidiu:** Ambos

---

### 17/08/2026 — setmatch — Aula online sempre gratuita — sem IAP nem Stripe de vídeo

- **Decisão:** Remover do app inteiro (iOS, Android e web) cobrança de aula online: sem preço, cadeado, checkout aula_online, pedir liberação ou switch 'aula paga'. Vídeo sempre assiste. Stripe fica só para mensalidade presencial, ranking e torneio.
- **Motivo:** Guideline Apple 3.1.1 — conteúdo digital não pode ser cobrado fora da IAP. Usuário pediu para tirar a feature, não só ocultar no iOS.
- **Alternativa rejeitada:** IAP da Apple; ou só esconder aulas pagas no iOS e manter venda no Android.
- **Impacto:** app/aula/[id].tsx, aulas-publicar, aulasPublicadas.ts, i18n, seed, storeCompliance removido, docs compliance/project
- **Quem decidiu:** Usuário + agente

---

### 17/08/2026 — setmatch — Aula online sempre gratuita

- **Decisão:** Aula online sempre grátis no app inteiro. Sem IAP. Stripe só presencial (mensalidade, ranking, torneio).
- **Motivo:** Apple 3.1.1; usuário pediu remover cobrança de vídeo, não só ocultar no iOS.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 17/08/2026 — setmatch — iOS 1.0.0 (5) build+submit ASC

- **Decisão:** EAS iOS production 1.0.0 build 5 (buildNumber 4→5 via autoIncrement) + auto-submit ASC. Android versionCode 2 no app.json, sem submit Play.
- **Motivo:** Resubmit após recusa 5.1.1 e 3.1.1 (aula online paga + purpose string).
- **Alternativa rejeitada:** N/A
- **Impacto:** app.json ios.buildNumber 5; binary em processamento no App Store Connect 6799449067
- **Quem decidiu:** Usuário

---

### 18/08/2026 — setmatch — Login só email/senha (Guideline 4.8)

- **Decisão:** Remover login Google/Apple/Facebook do Setmatch (UI + AuthContext). App Store 4.8: só email/senha. buildNumber 6.
- **Motivo:** Recusa Apple 4.8 no 1.0 (5). Usuário optou por tirar login de terceiro em vez de Sign in with Apple.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Usuário

---

### 19/08/2026 — lashmatch — Templates WhatsApp padronizados em v5

- **Decisão:** Configuração das Functions atualizada para usar agendamento_confirmado_salao_v5 e lembrete_agendamento_salao_v5 (WABA Lash Match).
- **Motivo:** Evitar envio de copy legado v3 no WhatsApp compartilhado do app.
- **Alternativa rejeitada:** N/A
- **Impacto:** Confirmações e lembretes novos passam a usar template v5 aprovado.
- **Quem decidiu:** Ambos

---

### 19/08/2026 — lashmatch — Templates WhatsApp v5 ativos

- **Decisão:** Functions configuradas com WHATSAPP_TEMPLATE_CONFIRMACAO=agendamento_confirmado_salao_v5 e WHATSAPP_TEMPLATE_LEMBRETE=lembrete_agendamento_salao_v5.
- **Motivo:** Eliminar envio com copy legado v3 no WhatsApp compartilhado do app.
- **Alternativa rejeitada:** N/A
- **Impacto:** Novos envios de confirmação/lembrete usam template v5 aprovado.
- **Quem decidiu:** Ambos

---

### 19/08/2026 — lashmatch — Permitir /plano-escolha para assinante

- **Decisão:** PlanoAccessRedirect não deve redirecionar assinantes para tabs ao abrir /plano-escolha.
- **Motivo:** Botões de Pagamentos para trocar tipo de WhatsApp/lembrete estavam voltando para início em vez de abrir a tela de escolha.
- **Alternativa rejeitada:** N/A
- **Impacto:** Fluxo de troca de tipo de plano funciona em Android web/PWA e iOS sem reset de navegação.
- **Quem decidiu:** Ambos

---

### 19/08/2026 — health-quadra-tech — Painel financeiro com gráfico, períodos e ranking por psicólogo

- **Decisão:** Painel financeiro com saldo, Passado/Futuro, filtros Dia/Semana/Mês/Trimestre/Semestre/Ano + intervalo, gráfico SVG sage/ouro e ranking de rentabilidade por psicólogo (gestor). Lógica em packages/shared/finance.ts; web /clinica/financeiro e /psico/financeiro; mobile (clinica)/financeiro e (psico)/financeiro.
- **Motivo:** Pedido de painel com balanço, gráfico, períodos e ranking, no visual Trajeto, web e app.
- **Alternativa rejeitada:** Copiar UI de banco (rosa/azul) ou instalar recharts — quebraria Expo Go e a identidade Trajeto
- **Impacto:** Gestor vê quem mais gera resultado para a clínica; psicólogo vê o próprio líquido. Sem tabela nova.
- **Quem decidiu:** Gustavo + agente

---

### 19/08/2026 — health-quadra-tech — React único 19.1.0 no workspace web — não aliasar no webpack

- **Decisão:** O app web (@trajeto/web) deve usar exatamente react/react-dom 19.1.0 (mesmo override do monorepo Expo). Remover cópias aninhadas em apps/web/node_modules e não criar webpack alias de react/react-dom.
- **Motivo:** Duas versões (19.2.8 aninhado + 19.1.0 hoist) quebravam o prerender do Next (/404 e /_not-found) com TypeError useContext of null. Alias webpack de react para a cópia client também quebrava RSC: next/link chama useContext no dispatcher de servidor.
- **Alternativa rejeitada:** Alias webpack forcando um único path de react — resolve dual package no client mas quebra React Server Components no prerender.
- **Impacto:** Build Next passa (incluindo /_not-found). Deploy Vercel de apps/web precisa do lockfile sem apps/web/node_modules/react@19.2.8.
- **Quem decidiu:** agente

---

### 19/08/2026 — health-quadra-tech — Gráfico financeiro agrupa por vencimento, não por paid_at

- **Decisão:** No horizonte Passado, a série do gráfico usa due_date (depois paid_at/created_at). O extrato já lista vencimento.
- **Motivo:** Marcar como pago grava paid_at = agora. Três lançamentos (fev R$100 + ago R$300 + ago R$200) viravam uma barra de R$600 em agosto e fevereiro zerado.
- **Alternativa rejeitada:** Manter cashflow por paid_at e mostrar coluna Pago em — certo para caixa, mas contradiz o extrato que o usuário lê.
- **Impacto:** Ano/mês passam a bater com as linhas do extrato.
- **Quem decidiu:** usuário + agente

---

### 19/08/2026 — health-quadra-tech — Financeiro: extrato segue filtros; gráfico mês=dias; entrada e saída

- **Decisão:** Filtros Passado/Futuro + período valem no gráfico e no extrato. Mês desenha dias do mês; Ano desenha jan–dez. Gráfico com barra sage (entrada) e ouro (saída/repasse).
- **Motivo:** O filtro Mês ainda plotava 12 meses, o extrato ignorava o recorte, e a linha ouro repetia a entrada.
- **Alternativa rejeitada:** Manter extrato completo e série anual no filtro Mês — confundia com bug de agrupamento.
- **Impacto:** Em agosto+Passado o extrato mostra só os pagos daquele mês. Jan/fev aparecem no recorte Ano. Futuro em agosto não lista o a receber de setembro.
- **Quem decidiu:** usuário

---

### 19/08/2026 — health-quadra-tech — Cadastro do paciente pede CPF e convênio (web + app)

- **Decisão:** No cadastro pelo convite (web /p/cadastro e app /cadastro) o paciente informa CPF obrigatório (máscara + dígito verificador) e se possui convênio (Sim/Não; nome opcional). Colunas patients.cpf, has_convenio, convenio_name. Unique (clinic_id, cpf). RPC claim_patient_invite ganhou p_cpf, p_has_convenio, p_convenio_name. Ficha e relatório no psicólogo (web+app) leem/editam os mesmos campos. Gráfico financeiro já espelhado no app.
- **Motivo:** Pedido do produto: dados fiscais/operacionais no preenchimento do paciente, não só na ficha. Paridade web/app é regra do Trajeto.
- **Alternativa rejeitada:** Só pedir CPF na ficha do psicólogo, ou usar fee_schedules como convênio do paciente (fee_schedules é tabela de preços da clínica).
- **Impacto:** Migration 20260819180000 aplicada em fzttsuuzfauqkagscrwc. Convites antigos passam a exigir CPF no cadastro.
- **Quem decidiu:** usuario + agente

---

### 19/08/2026 — health-quadra-tech — HOLD D3 quiz até justificativa das notas baixas

- **Decisão:** HOLD no diferencial D3 (quiz → pré-ficha). As 4 notas (2×5/5, 1/5 e 2/5) não têm justificativa — não dá para iterar. Não copiar o HTML de exemplo para produção. Próxima evidência: ≥10 pessoas com “por quê” obrigatório se nota ≤3 (instrumento em docs/research/quiz-triagem-psicologia.html). Único ajuste de código: copy do app de “8 minutos” para “2 minutos” (5 perguntas).
- **Motivo:** Risco de adoção no diferencial, não item de escopo. Sem o porquê, polarização n=4 é ruído. O HTML anexo é o instrumento de pesquisa (nota + justificação), não o próximo UI.
- **Alternativa rejeitada:** Tratar as notas 1/5 e 2/5 como pedido de feature (estrelas, matching, quiz novo do HTML) e continuar investindo em D3.
- **Impacto:** Agenda/financeiro/D1 seguem; quiz não ganha matching, estrela nem pergunta extra até a rodada qualitativa.
- **Quem decidiu:** usuario

---

### 19/08/2026 — health-quadra-tech — Reenviar quiz + cadastro visível após convite

- **Decisão:** Clínica e psicólogo (web+app) veem o cadastro completo (CPF, convênio, nascimento, motivo) depois que o paciente aceita o convite. Botão Enviar quiz novamente grava patients.quiz_requested_at e compartilha /p/quiz; o painel do paciente mostra o pedido até ele responder. SOAP continua só no chapéu psicólogo.
- **Motivo:** Pedido do produto: reenviar quiz pelo app e ver todos os dados do cadastro após o convite. Paridade web/app.
- **Alternativa rejeitada:** Só copiar o link do quiz sem gravar pedido, ou mostrar SOAP da casa inteira para o gestor.
- **Impacto:** Migration 20260819190000 (quiz_requested_at) em fzttsuuzfauqkagscrwc. Rotas /clinica/pacientes/[id] e (clinica)/paciente/[id]. Lista do psico no app filtrada por professional_id.
- **Quem decidiu:** usuario

---

### 19/08/2026 — health-quadra-tech — EAS update Trajeto exige conta shoutloud

- **Decisão:** eas update --branch preview do Trajeto só funciona logado como shoutloud. A CLI nesta máquina estava gabrieljorda0 e recebeu Entity not authorized no AppEntity 7ba50e12. Web Vercel --prod sobe independente disso.
- **Motivo:** O projeto EAS é da org shoutloud; RegularUserViewerContext do gabrieljorda0 não tem READ no app.
- **Alternativa rejeitada:** Publicar OTA com a conta gabrieljorda0 ou criar outro projeto EAS.
- **Impacto:** Depois de eas login shoutloud, em apps/mobile: eas update --branch preview. Expo Go precisa estar logado na mesma conta.
- **Quem decidiu:** Gustavo

---

### 19/08/2026 — health-quadra-tech — WhatsApp Cloud API + Daily no browser + quiz periódico

- **Decisão:** M7 no Trajeto via Edge Functions trajeto-notify (JWT) e trajeto-cron (CRON_SECRET). Teleconsulta Daily no browser (mental-health.daily.co) para permanecer no Expo Go. WhatsApp Cloud API com templates UTILITY trajeto_sessao_confirmada, trajeto_lembrete_sessao e trajeto_quiz_triagem; fallback wa.me no padrão Cortejo/LashMatch enquanto a Meta não aprova. Cadência de quiz em quiz_schedules (weekly/biweekly/monthly). Secrets só no dashboard Supabase, nunca no Git. PHONE_ID 1347928901727664; Id do portfólio 1012313901775778 não é WABA.
- **Motivo:** Pedido do Gustavo: lembrete/confirmação/quiz no WhatsApp, agendar online vs presencial com link da sala, templates prontos e quiz automático — sem sair do Expo Go.
- **Alternativa rejeitada:** WebRTC nativo Daily no app (exige EAS dev build) e Z-API. M8–M11 (escalas, tarefas, Receita Saúde, supervisão) ficam para depois.
- **Impacto:** Agendar cria sala Daily se online e tenta WhatsApp; ficha do paciente ganha painel de templates; paciente confirma/remarca no painel. Envio automático só depois de secrets + templates APPROVED.
- **Quem decidiu:** Gustavo + agente

---

### 19/08/2026 — health-quadra-tech — Templates Trajeto no WABA + WhatsApp obrigatório no paciente

- **Decisão:** O envio automático usa só trajeto_sessao_confirmada, trajeto_lembrete_sessao e trajeto_quiz_triagem (UTILITY pt_BR, mesmo formato Graph v23.0 do curl que funcionou). patients.phone passou a NOT NULL e os formulários de convite/cadastro/ficha exigem WhatsApp com DDD.
- **Motivo:** O exemplo lembrete_agendamento confirma que o ID 1012313901775778 é WABA válido, mas o código já monta 5–6 parâmetros. Sem número na ficha o template não sai.
- **Alternativa rejeitada:** Reusar o template de teste lembrete_agendamento (2 variáveis) no envio automático — o texto e as vars não batem com trajeto-notify.
- **Impacto:** WABA 1012313901775778; Edge Functions trajeto-notify/cron; cadastro web+app; migration 20260819220000
- **Quem decidiu:** Agente + usuário

---

### 19/08/2026 — health-quadra-tech — Painel do paciente lista sessões com link Daily

- **Decisão:** Painel do paciente (web /p e app (patient)) lista as próximas sessões com modalidade, status e botão Entrar na chamada (Daily no browser) quando houver video_join_url.
- **Motivo:** Paciente precisa ver agendamentos futuros e o link da teleconsulta depois do login, não só o próximo horário.
- **Alternativa rejeitada:** Manter só a próxima sessão no painel do paciente
- **Impacto:** apps/web/app/p/page.tsx e apps/mobile/app/(patient)/index.tsx
- **Quem decidiu:** Usuário + agente

---

### 19/08/2026 — health-quadra-tech — Link Daily no painel da agenda do psicólogo

- **Decisão:** O botão Entrar na consulta fica no card de detalhe do horário em /psico/agenda (clique no bloco). Se ainda não houver video_join_url, o clique cria a sala Daily e abre no navegador.
- **Motivo:** A psicóloga agenda pela grade e esperava o link no mesmo card; produção só tinha status/excluir.
- **Alternativa rejeitada:** Só mostrar Entrar no painel Hoje quando o URL já existisse.
- **Impacto:** AgendaBoard AppointmentDetail + CSS agenda-join; painel /psico com fallback Abrir na agenda.
- **Quem decidiu:** Gustavo

---

### 19/08/2026 — health-quadra-tech — Filtro de evolução Todos ou um paciente

- **Decisão:** Em Pacientes e evolução o padrão continua Todos os pacientes; dá para filtrar um nome e ver só o GAD-7/PHQ-9 dele. Web: select. Mobile: lista Todos + nomes.
- **Motivo:** Pedido do Gustavo: mostrar evolução de 1 paciente ou deixar como estava.
- **Alternativa rejeitada:** Só um gráfico agregado da carteira, ou forçar sempre um paciente.
- **Impacto:** apps/web/components/EvolutionBoard.tsx, psico/pacientes page, apps/mobile/(psico)/pacientes.tsx
- **Quem decidiu:** Gustavo

---

### 19/08/2026 — fabrica — Chroma staging + lock para não corromper HNSW

- **Decisão:** Indexação em staging (.chroma_db.build) com lock exclusivo; incremental não escreve se a porta 7332 estiver aberta; sync-push default us-east-1. Recriado 2507 chunks e enviado ao S3. Script reparar-chroma.ps1.
- **Motivo:** HNSW no Windows corrompe com dois processos no mesmo PersistentClient; fallback sa-east-1 do sync era perigoso.
- **Alternativa rejeitada:** Continuar indexando no mesmo .chroma_db com o servidor 7332 aberto (causa o 0xC0000005).
- **Impacto:** obsidian/chroma_lock.py, indexar_rapido.py, indexar_obsidian_chroma.py, sync-push.ps1, reparar-chroma.ps1, Dockerfile (COPY chroma_lock.py)
- **Quem decidiu:** Gustavo

---

### 19/08/2026 — fabrica — Chroma staging + lock para não corromper HNSW

- **Decisão:** Indexação em staging (.chroma_db.build) com lock exclusivo; incremental não escreve se a porta 7332 estiver aberta; sync-push default us-east-1. Recriado 2507 chunks e enviado ao S3. Script reparar-chroma.ps1.
- **Motivo:** HNSW no Windows corrompe com dois processos no mesmo PersistentClient; fallback sa-east-1 do sync era perigoso.
- **Alternativa rejeitada:** Continuar indexando no mesmo .chroma_db com o servidor 7332 aberto (causa o 0xC0000005).
- **Impacto:** obsidian/chroma_lock.py, indexar_rapido.py, indexar_obsidian_chroma.py, sync-push.ps1, reparar-chroma.ps1, Dockerfile (COPY chroma_lock.py)
- **Quem decidiu:** Gustavo

---

### 20/08/2026 — health-quadra-tech — Jitsi próprio no VPS; Daily até o domínio responder

- **Decisão:** Jitsi self-host no VPS São Paulo (Docker stable + Let's Encrypt + coturn). App segue abrindo URL no browser (Expo Go). Daily permanece até VIDEO_PROVIDER=jitsi + JITSI_BASE_URL. Pacote em infra/jitsi.
- **Motivo:** Custo baixo (VPS/mês, R$ 0 por chamada), dados de mídia no servidor próprio, mesma UX de Entrar na consulta.
- **Alternativa rejeitada:** meet.jit.si público, WebRTC na mão, ou SDK nativo/EAS só por vídeo.
- **Impacto:** infra/jitsi (setup.sh, TURN, README). trajeto-notify aceita VIDEO_PROVIDER=jitsi sem mudar web/mobile. Daily default.
- **Quem decidiu:** Gustavo

---

### 20/08/2026 — health-quadra-tech — Teleconsulta Trajeto no Jitsi próprio

- **Decisão:** Produção usa Jitsi em https://call.jordaob.com.br. trajeto-notify v5: padrão VIDEO_PROVIDER=jitsi e JITSI_BASE_URL=https://call.jordaob.com.br. Daily só se VIDEO_PROVIDER=daily. URLs antigas daily.co no banco foram reescritas.
- **Motivo:** Teste de ligação em dois dispositivos deu certo; custo por minuto do Daily sai do produto.
- **Alternativa rejeitada:** Manter Daily como padrão até secrets manuais no dashboard
- **Impacto:** Entrar na consulta abre call.jordaob.com.br. VPS Vultr SP continua ligado. Rollback: secret VIDEO_PROVIDER=daily.
- **Quem decidiu:** usuario

---

### 20/08/2026 — health-quadra-tech — Templates WhatsApp Trajeto na WABA Gerenciador S

- **Decisão:** Templates Trajeto criados na WABA 1012313901775778 (nome Gerenciador S), que é a conta do PHONE_ID 1347928901727664. Portfólio empresarial 3566050263560437. Nomes: trajeto_sessao_confirmada, trajeto_lembrete_sessao, trajeto_quiz_triagem (UTILITY pt_BR, PENDING).
- **Motivo:** O número não tinha os 3 modelos do app; só existia o teste lembrete_agendamento.
- **Alternativa rejeitada:** Criar template no phone_number_id; o modelo vive na WABA, não no telefone
- **Impacto:** Envio automático só depois de APPROVED na Meta. Até lá o app segue wa.me.
- **Quem decidiu:** usuario

---

### 20/08/2026 — sinaflor — HU136 Encaminhar outro órgão/unidade

- **Decisão:** Tipo 3: formulário próprio (Finalidade/Esfera/UF/Município/Órgão + despacho + e-mail ON); sem analistas/anexos/manter aberto; só GO; status do processo não muda; ao finalizar atualiza LicenciamentoDadosGerais (órgão/unidade/competência) para permanente e temporária (retorno temporário = fluxo futuro).
- **Motivo:** HU136 RN21 e campos distintos das demais tramitações; destino precisa receber o processo na gestão via filtro de órgão/unidade.
- **Alternativa rejeitada:** Reaproveitar tramitacao-arquivamento ou exigir analistas como na narrativa genérica da HU
- **Impacto:** Script SQL SPRINT_19/03 necessário; componente tramitacao-encaminhar-orgao; acoesDisponiveis inclui 3
- **Quem decidiu:** Ambos

---

### 23/08/2026 — cortejo — Agenda semana Cortejo: empilhar blocos curtos sem chip especial

- **Decisão:** Na visão Semana do Cortejo, stackWeekBlocks empurra o próximo cartão para baixo quando o curto precisa de altura mínima legível — todos com o mesmo estilo accentSoft, sem borda/sombra de seleção. LashMatch: removido só o apptBrief da última alteração; resto intacto.
- **Motivo:** Chip branco com borda fazia o 9:20 parecer selecionado e flutuar por cima; usuário pediu um embaixo do outro, visível, sem marcação especial.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

### 23/08/2026 — fabrica — Limpeza RAG: duplicata i18n + decisoes undefined + ponte schemas

- **Decisão:** Auditoria RAG fabrica 23/08: removida duplicata setmatch-i18n-idiomas-padrao (canônico = setmatch-i18n-padrao); firestore-schemas virou ponte para schemas por app; limpeza de títulos/entradas undefined em decisoes.md; outros.md já era excluído do indexar_rapido.
- **Motivo:** Duplicatas e stubs undefined diluem retrieval do Chroma/App Runner.
- **Alternativa rejeitada:** N/A
- **Impacto:** A definir
- **Quem decidiu:** Ambos

---

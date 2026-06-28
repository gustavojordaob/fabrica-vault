# Erros e Soluções — Fábrica de Software

> Registro automático de erros resolvidos pelo agente.
> Atualizado após cada solução para que a fábrica aprenda.
>
> **Padrões completos (jun/2026):** [[mercadopago-assinatura-ota-padroes]] · [[modulo-ajuda-suporte-expo]]

---

## 09/06/2026 — cortejo — Assinatura MP: cancelou no app mas continuou ativa no Mercado Pago

**Erro:** Cancelamento mostrava "já cancelada" e voltava à paywall; no painel MP duas assinaturas ainda ativas em trial

**Contexto:** `mpCancelarAssinatura` e fluxo de sync após reassinar

**Causa:** Firestore marcado `CANCELLED`/`plan: free` sem PUT na API MP; `alreadyCancelled` confiava `sub.status` local; `mpSyncSubscription` só consultava `mpPreapprovalId` antigo; cada `mpCriarAssinatura` criava nova preapproval sem cancelar as anteriores

**Solução:** `cancelAllActivePreapprovalsForEmail` + `searchActivePreapprovalsByEmail`; cancelar só após sucesso MP; antes de criar nova assinatura cancelar ativas; sync busca assinatura ativa por e-mail; `syncSalonFromPreapproval` com `isMpPreapprovalGrantedAccess` (inclui pending); paywall com "Atualizar acesso"; deploy functions

**Arquivos:** `functions/SRC/mercadoPagoAssinatura.ts`, `functions/SRC/index.ts`, `utils/subscription.ts`, `app/config/plano.tsx`, `app/config/cartao.tsx`, `app/config/cancelamento.tsx`

**Tags:** mercadopago, assinatura, preapproval, paywall, cortejo

---

## 09/06/2026 — cortejo — ReferenceError Property salonId doesn't exist (cartao.tsx)

**Erro:** `ReferenceError: Property 'salonId' doesn't exist` ao abrir tela de cartão

**Contexto:** `app/config/cartao.tsx` após refactor pós-pagamento

**Causa:** Linha `const salonId = useSalonStore(...)` removida mas JSX ainda usava `{!salonId ? ...}`

**Solução:** Restaurar `const salonId = useSalonStore((s) => s.salonId)`

**Arquivos:** `app/config/cartao.tsx`

**Tags:** react-native, zustand, mercadopago, cortejo

---

## 09/06/2026 — cortejo — Property View doesn't exist (cancelamento.tsx)

**Erro:** `ReferenceError: Property 'View' doesn't exist` na tela de cancelamento

**Contexto:** Tela `app/config/cancelamento.tsx`

**Causa:** Componente `View` usado no JSX sem import de `react-native`

**Solução:** Adicionar `View` ao import de `react-native`

**Arquivos:** `app/config/cancelamento.tsx`

**Tags:** react-native, cortejo

---

## 09/06/2026 — cortejo/lashmatch — Módulo ajuda/suporte (padrão reutilizável)

**Contexto:** Adicionar suporte WhatsApp + FAQ nos apps Cortejo e LashMatch

**Padrão:** `constants/support.ts` + `utils/supportContact.ts` + tela `ajuda` + entrada no menu Mais/Perfil; só WhatsApp (sem botão ligar)

**Arquivos:** Cortejo `app/config/ajuda.tsx`, `app/(tabs)/mais.tsx` · LashMatch `app/ajuda.tsx`, `constants/moreMenuItems.ts`, `app/(tabs)/perfilUsuario.tsx`

**Tags:** suporte, whatsapp, expo, cortejo, lashmatch

**Doc:** [[modulo-ajuda-suporte-expo]]

---

## 10/06/2026 — cortejo — Client Id property androidClientId must be defined to use Google auth on this pl

**Erro:** Client Id property androidClientId must be defined to use Google auth on this platform

**Contexto:** Tela de login no Android/Expo Go ao montar Google.useAuthRequest só com webClientId

**Causa:** expo-auth-session no Android exige androidClientId (e iOS exige iosClientId); hook roda mesmo sem IDs configurados

**Solução:** Extrair GoogleSignInButton em componente isolado; isGoogleAuthAvailable() só monta o hook quando o client ID da plataforma existe no .env; login por e-mail segue sem Google

**Arquivos:** components/auth/GoogleSignInButton.tsx, utils/googleAuth.ts, app/(auth)/login.tsx, .env.example

**Tags:** expo, google-auth, android, cortejo

---

## 10/06/2026 — cortejo — FirebaseError: Missing or insufficient permissions ao criar conta/salão

**Erro:** FirebaseError: Missing or insufficient permissions ao criar conta/salão

**Contexto:** Onboarding após createUserWithEmailAndPassword — setDoc em salons/members

**Causa:** firestore.rules exigia isMember para write em members (impossível no primeiro owner) e read em salons sem isSalonOwner para query ownerUid

**Solução:** Adicionar isSalonOwner(salonId); allow read salon se member ou owner; allow create member se uid==auth.uid && isSalonOwner && role==owner; deploy firestore:rules

**Arquivos:** firestore.rules, hooks/useSalonBootstrap.ts

**Tags:** firebase, firestore, rules, onboarding, cortejo

---

## 10/06/2026 — cortejo — Loop infinito no onboarding — cria salão e volta para tela de criação

**Erro:** Loop infinito no onboarding — cria salão e volta para tela de criação

**Contexto:** Após createSalon bem-sucedido, router.replace('/') e index redireciona de volta para onboarding

**Causa:** Race: salonId no Zustand ainda null (bootstrap só roda em onAuthStateChanged, não após criar salão); index usava setTimeout 600ms com salonId stale

**Solução:** createSalon retorna {salonId,salon,member}; onboarding chama setSalonContext e router.replace('/(tabs)'); store com isHydrated; index espera isHydrated antes de rotear; loadSalonContextForUser compartilhado

**Arquivos:** services/onboarding.ts, services/salonContext.ts, stores/salonStore.ts, hooks/useSalonBootstrap.ts, app/index.tsx, app/(auth)/onboarding.tsx

**Tags:** expo-router, zustand, onboarding, race-condition, cortejo

---

## 10/06/2026 — cortejo — getReactNativePersistence is not a function no expo export web

**Erro:** getReactNativePersistence is not a function no expo export web

**Contexto:** npx expo export --platform web para Firebase Hosting

**Causa:** initializeAuth com getReactNativePersistence(AsyncStorage) não existe no bundle web

**Solução:** Platform.OS === 'web' ? getAuth(app) : initializeAuth(app, { persistence: getReactNativePersistence(AsyncStorage) })

**Arquivos:** utils/firebaseConfig.ts

**Tags:** firebase, expo-web, hosting, cortejo

---

## 09/06/2026 — lashmatch — WhatsApp 132001 template não existe

**Erro:** Graph API `132001` — template name does not exist in the translation

**Contexto:** Envio de confirmação/lembrete após migração Meta

**Causa:** `WHATSAPP_PHONE_ID` apontava para número antigo (`1139549772571990`); templates v7/v2 cadastrados no número correto (`1190765630776115`)

**Solução:** Atualizar `WHATSAPP_PHONE_ID` em `functions/.env`, redeploy functions, usar nomes `agendamento_confirmado_v7` e `lembrete_agendamento_v2`

**Arquivos:** `functions/.env`, `functions/SRC/whatsapp.ts`, `docs/whatsapp-business-api.md`

**Tags:** whatsapp, meta, template, lashmatch

---

## 09/06/2026 — lashmatch — WhatsApp 131030 recipient not in allowed list

**Erro:** Graph API `131030` — recipient phone number not in allowed list

**Contexto:** Teste em modo desenvolvimento Meta

**Causa:** Número da cliente não cadastrado como destinatário de teste no painel Meta

**Solução:** Adicionar telefone em WhatsApp → API Setup → "To" (modo dev) ou aguardar número de produção verificado

**Tags:** whatsapp, meta, dev-mode, lashmatch

---

## 12/06/2026 — fabrica — Servidor RAG fecha após carregar modelo (Chroma corrompido)

**Erro:** `python indexar_obsidian_chroma.py --server` volta ao prompt após `Loading weights: 100%` — sem mensagem `Servidor RAG rodando`

**Contexto:** Windows, Chroma 1.5.9, pasta `C:/Users/gusta/obsidian/.chroma_db`

**Causa:** Banco Chroma corrompido ou lock concorrente (exit code `3221225477` / access violation ao abrir `.chroma_db`)

**Solução:**
1. Parar outros processos Python que usem o RAG
2. Renomear `.chroma_db` → `.chroma_db.bak_YYYYMMDD`
3. `python C:/Users/gusta/obsidian/indexar_rapido.py`
4. `python indexar_obsidian_chroma.py --server` (deixar terminal aberto; Ctrl+C para parar)
5. Diagnóstico: `python indexar_obsidian_chroma.py --doctor`

**Arquivos:** `indexar_obsidian_chroma.py`, `indexar_rapido.py`

**Tags:** rag, chroma, windows, fabrica

---

## 13/06/2026 — cortejo — Agente implementou react-native-calendars sem consultar RAG

**Erro:** Agente implementou react-native-calendars sem consultar RAG

**Contexto:** Usuário pediu agenda moderna com calendário. Agente instalou pacote e codou Calendar + lista manual sem rag_buscar nem ler react-native-calendars.md indexado.

**Causa:** Regra global RAG existia mas não havia detecção específica para libs UI (calendário/agenda) nem documento de protocolo com caso de estudo. Agente tratou Chroma/contexto como suficiente e pulou MCP.

**Solução:** Criado rag-protocolo-antes-de-codar.md; bloco MCP em react-native-calendars.md; detectMandatoryRagDocs + workflow implementar_com_guia_rag em rag-lib.js; gate reforçado em rag-pre-tool.js; regra cortejo .cursor/rules/rag-calendario-exemplo.mdc; triggers na regra global rag-memoria-fabrica.mdc

**Arquivos:** obsidian/fabrica/rag-protocolo-antes-de-codar.md, react-native-calendars.md, ~/.cursor/hooks/rag-lib.js, rag-before-prompt.js, rag-pre-tool.js, cortejo/.cursor/rules/rag-calendario-exemplo.mdc

**Tags:** rag, calendario, cortejo, agente, protocolo

---

## 15/06/2026 — cortejo — Assinatura MP: cancelamento falso, paywall travado, duplicatas no painel

**Erro:** Assinatura MP: cancelamento falso, paywall travado, duplicatas no painel

**Contexto:** mpCancelarAssinatura, mpCriarAssinatura, mpSyncSubscription, cartao/plano/cancelamento

**Causa:** Firestore CANCELLED sem PUT no MP; sync só no id antigo; criar assinatura sem cancelar ativas; store não recarregado após pagamento

**Solução:** cancelAllActivePreapprovalsForEmail, searchActivePreapprovalsByEmail, isMpPreapprovalGrantedAccess, paywall Atualizar acesso, cartao sync+loadSalonContext; doc mercadopago-assinatura-ota-padroes.md

**Arquivos:** functions/SRC/mercadoPagoAssinatura.ts, functions/SRC/index.ts, utils/subscription.ts, app/config/*.tsx

**Tags:** mercadopago, assinatura, preapproval, paywall, cortejo

---

## 18/06/2026 — cortejo — arrayUnion() called with invalid data. Unsupported field value: undefined em blo

**Erro:** arrayUnion() called with invalid data. Unsupported field value: undefined em blockedPeriods

**Contexto:** Tela Bloquear agenda ao salvar período no documento do salão

**Causa:** Firestore rejeita undefined em documentos; addBlockedPeriod enviava createdAt: undefined no objeto do arrayUnion

**Solução:** Montar BlockedPeriod omitindo campos opcionais vazios (buildBlockedPeriodDoc); nunca incluir createdAt: undefined

**Arquivos:** services/blockedPeriods.ts

**Tags:** firestore,agenda,bloqueio

---

## 18/06/2026 — cortejo — Duplicate declaration toDateKey no bundler Android

**Erro:** Duplicate declaration toDateKey no bundler Android

**Contexto:** utils/dates.ts após integração blockedPeriodsLogic

**Causa:** Import circular: dates.ts importava toDateKey de @/utils/dates enquanto exportava a mesma função

**Solução:** Remover self-import; isDateBlocked inline sem importar blockedPeriodsLogic

**Arquivos:** utils/dates.ts

**Tags:** metro,typescript,agenda

---

## 18/06/2026 — cortejo — Transaction.set() Unsupported field value: undefined em vendas (clientId)

**Erro:** Transaction.set() Unsupported field value: undefined em vendas (clientId)

**Contexto:** Finalizar venda no PDV

**Causa:** Firestore não aceita undefined em campos opcionais do documento de venda

**Solução:** buildSaleDocument() omite clientId e demais opcionais quando ausentes

**Arquivos:** services/sales.ts

**Tags:** firestore,vendas,pdv

---

## 18/06/2026 — cortejo — Site assinar iPhone: Internal Server Error ao pagar; mensagens feias em CVV/data

**Erro:** Site assinar iPhone: Internal Server Error ao pagar; mensagens feias em CVV/data; recusa com cartão correto

**Contexto:** public/assinar + tokenizar + mpCriarAssinatura no Safari iOS

**Causa:** onAuthStateChanged disparava mpCriarAssinatura 2x com mesmo card_token (token de uso único); token na URL longa no iOS; erros MP repassados como HTTP 500/JSON bruto; sync Firestore sem try/catch gerava 500

**Solução:** Token via sessionStorage + guard checkoutInFlight/wasTokenProcessed; formatMpErrorForUser no backend (400 amigável); try/catch em mpCriarAssinatura; mp-errors.js no tokenizar/assinar; ano 2 dígitos no tokenizar

**Arquivos:** functions/SRC/mercadoPagoAssinatura.ts, functions/SRC/index.ts, public/assinar/index.html, public/assinatura/tokenizar.html, public/assinatura/mp-errors.js, scripts/copy-public-to-dist.mjs

**Tags:** mercadopago, assinatura, ios, safari, cortejo, hosting

---

## 18/06/2026 — cortejo — Pagamento MP aprovado mas plano Pro não liberado no app

**Erro:** Pagamento MP aprovado mas plano Pro não liberado no app

**Contexto:** mpCriarAssinatura, mpSyncSubscription, mpWebhook, assinar site iOS

**Causa:** syncSalonFromPreapproval gravava subscription.payerEmail undefined no Firestore quando MP não retornava payer_email; Firestore rejeita undefined e sync/mpSyncSubscription falhavam silenciosamente

**Solução:** stripUndefinedRecord + payerEmail via hints; mpCriarAssinatura passa payerEmail; só retorna ok se salonHasActiveSubscription; plano.tsx auto-sync ao abrir paywall

**Arquivos:** functions/SRC/mercadoPagoAssinatura.ts, functions/SRC/index.ts, app/config/plano.tsx

**Tags:** mercadopago, assinatura, firestore, paywall, cortejo

---

## 18/06/2026 — cortejo — loadSalonContextForUser consulta por membro falhou permission-denied + assinatur

**Erro:** loadSalonContextForUser consulta por membro falhou permission-denied + assinatura ativa mas app fica na paywall

**Contexto:** Após pagamento MP no site, Firestore tinha plan:pro mas app mostrava tela de assinatura

**Causa:** 1) firestore.rules quebrado sem allow read no salão + sem regra collectionGroup members. 2) syncSalonFromPreapproval falhava com payerEmail undefined. 3) app usava cache AsyncStorage (plan:free) em vez de getDocFromServer após sync.

**Solução:** Corrigir firestore.rules (read salão + collectionGroup members). stripUndefined no sync MP. loadSalonContextForEmailFromServer no boot (index.tsx), plano.tsx e confirmado.tsx. isSalonSubscriptionActive(salon) direto. Deploy firestore:rules cortejo-app.

**Arquivos:** firestore.rules, services/salonContext.ts, app/index.tsx, app/config/plano.tsx, app/plano/confirmado.tsx, functions/SRC/mercadoPagoAssinatura.ts

**Tags:** firestore,permissions,assinatura,mercadopago,cortejo

---

## 20/06/2026 — cortejo — WhatsApp template (#131008) Required parameter missing text / (#132018) newline 

**Erro:** WhatsApp template (#131008) Required parameter missing text / (#132018) newline in param

**Contexto:** Confirmação/lembrete WhatsApp parou — Meta #131008 parâmetro vazio e #132018 newline em template

**Causa:** 

**Solução:** templateTextParam() com fallback — e montarBlocoObservacoesRegras sem \n; {{10}} vazio vira —

**Arquivos:** N/A

**Tags:** whatsapp,meta,template,cortejo

---

## 21/06/2026 — cortejo — Meta template #131008 e #132018 — mensagens não chegam

**Erro:** Meta template #131008 e #132018 — mensagens não chegam

**Contexto:** Envio compartilhado WHATSAPP_PHONE_ID + templates agendamento_confirmado_salao / lembrete_agendamento_salao_v3

**Causa:** Parâmetro {{10}} vazio quando sem observações/regras; quebras de linha no bloco obs+regras

**Solução:** templateTextParam() com fallback '—' para vazio; montarBlocoObservacoesRegras sem \n; documentado em whatsapp-salao-expo-padrao.md

**Arquivos:** functions/SRC/whatsapp.ts, obsidian/fabrica/whatsapp-salao-expo-padrao.md

**Tags:** whatsapp, meta, template, cortejo

---

## 21/06/2026 — cortejo — URL de retorno inválida no Embedded Signup

**Erro:** URL de retorno inválida no Embedded Signup

**Contexto:** Conectar meu WhatsApp — startEmbeddedSignup rejeitava redirectUrl

**Causa:** Linking.createURL('/config/whatsapp') gera exp:// no Expo preview, não aceito pelo backend

**Solução:** Deep link fixo cortejo://config/whatsapp; backend aceita exp+cortejo:// e https://; documentado em whatsapp-salao-expo-padrao.md

**Arquivos:** services/embeddedSignup.ts, functions/SRC/embeddedSignup.ts

**Tags:** whatsapp, embedded-signup, expo, deep-link, cortejo

---

## 21/06/2026 — cortejo — iOS dev build trava no Loader infinito e paywall sem planos

**Erro:** iOS dev build trava no Loader infinito e paywall sem planos

**Contexto:** RevenueCat bootstrap + index.tsx aguardando rcChecked antes de salonId existir

**Causa:** RevenueCatBootstrap só marcava checked após logIn(salonId); index.tsx bloqueava navegação com usesRevenueCatIap() && !rcChecked mesmo sem salonId. Planos vazios: filtro rígido por product id + offerings.current vazio sem fallback.

**Solução:** Marcar checked=false quando iOS sem salonId; timeout 12s no logIn; index/SubscriptionAccessRedirect só aguardam RC com salonId; getOfferings fallback para offering default; pickSubscriptionPackages por store id ou $rc_monthly/$rc_annual; mensagem clara se API key ausente no build.

**Arquivos:** components/RevenueCatBootstrap.tsx, app/index.tsx, utils/subscriptionAccess.ts, components/SubscriptionAccessRedirect.tsx, services/usePurchase.ts, components/subscription/IosAssinaturaView.tsx, utils/revenueCatPackages.ts

**Tags:** revenuecat,ios,iap,loader

---

## 20/06/2026 — cortejo — Agendamento público bloqueado com Pro ativo no iOS

**Erro:** Link `/agendar?salon=...` mostrava "Este salão ainda não possui assinatura ativa" com Pro ativo no app iPhone

**Contexto:** Assinatura iOS via RevenueCat; booking público via `availableSlots` + Firestore

**Causa:** (1) Firestore `plan: free` enquanto entitlement Pro no dispositivo; (2) `salonHasActiveSubscription` bloqueava por `CANCELLED` do MP antes de checar `planExpiresAt`; (3) `revenueCatSyncSubscription` falhava com secret RevenueCat V2 em endpoint API V1 (403)

**Solução:** Sync Firestore em `RevenueCatBootstrap`, `shareSalonBookingLink` e CF com API **V2**; ordem `planExpiresAt` antes de `CANCELLED` em `mercadoPagoAssinatura.ts`; doc em `cortejo-modulos-jun2026-padrao.md` + regra `.cursor/rules/rag-assinatura-padrao.mdc`

**Arquivos:** `functions/SRC/revenueCatSubscription.ts`, `functions/SRC/mercadoPagoAssinatura.ts`, `components/RevenueCatBootstrap.tsx`, `utils/appLinks.ts`, `utils/subscription.ts`

**Tags:** revenuecat, firestore, agendamento, booking, cortejo, ios

---

## 20/06/2026 — cortejo — Trial 16 dias Android vs 14 dias Apple

**Erro:** Copy e período MP em 16 dias; Apple só permite intro offer até TWO_WEEKS (14d); risco de divergência iOS/Android

**Contexto:** `TRIAL_DAYS`, `planoMarketing.ts`, produtos ASC via RevenueCat MCP

**Causa:** Trial MP herdado de 16d; iOS sem número fixo na doc; constantes duplicadas app vs functions

**Solução:** `TRIAL_DAYS = 14` em `constants/planos.ts` e `functions/SRC/planosConfig.ts`; intro `TWO_WEEKS` nos 4 produtos RC; elegibilidade documentada (`hadAndroidTrial` / `hadIosTrial` não resetam ao cancelar)

**Arquivos:** `constants/planos.ts`, `functions/SRC/planosConfig.ts`, `constants/planoMarketing.ts`, `types/tenant.ts`

**Tags:** trial, mercadopago, revenuecat, assinatura, cortejo

---

## 23/06/2026 — cortejo — Falha ao conectar — falha ao acessar essa conta através desse aplicativo

**Erro:** Falha ao conectar — falha ao acessar essa conta através desse aplicativo

**Contexto:** Embedded Signup Coexistence — login Facebook da esposa no fluxo Conectar meu WhatsApp

**Causa:** App Meta (990183433661795) em modo Desenvolvimento: só contas com função no app (Administrador/Developer/Tester) podem fazer FB.login. Testadora no App Store Connect não vale. Conta da esposa precisa estar em developers.facebook.com → Funções do app e aceitar convite.

**Solução:** Meta Developer Console: App LashMatch/Cortejo 990183433661795 → Funções do app → adicionar e-mail Facebook da esposa como Administrador ou Testador; ela aceita convite. Opcional: colocar app em Live após App Review. Também: esposa deve ser admin do Business Manager do WABA/número WhatsApp Business.

**Arquivos:** public/embedded-signup/index.html

**Tags:** whatsapp, embedded-signup, meta, oauth, cortejo

---

## 23/06/2026 — cortejo — Permissions errors no Embedded Signup Meta (app teste)

**Erro:** Permissions errors no Embedded Signup Meta (app teste)

**Contexto:** Fluxo Conectar meu WhatsApp — OAuth/Embedded Signup app Lash match 2 (26656571413984672)

**Causa:** App Meta sem produto WhatsApp configurado, Configuration Embedded Signup sem permissões whatsapp_business_management/messaging, ou conta sem role no Business Manager

**Solução:** Meta Developer: adicionar produto WhatsApp; Facebook Login for Business → Configurations → WhatsApp Embedded Signup com as duas permissões; App Review → Permissões com acesso padrão (dev); Camila Admin no app e no BM do número

**Arquivos:** public/embedded-signup/index.html, obsidian/fabrica/whatsapp-salao-expo-padrao.md

**Tags:** whatsapp, embedded-signup, meta, permissions, cortejo

---

## 23/06/2026 — cortejo — Feche esta aba — OAuth Meta incompleto no mobile

**Erro:** Feche esta aba — OAuth Meta incompleto no mobile

**Contexto:** Embedded Signup Coexistence no celular — browser do app

**Causa:** FB.login popup não devolve controle à página /embedded-signup/; fluxo para no login Facebook sem escolher WABA/número

**Solução:** Redirect OAuth página inteira no mobile; sessionStorage para code; completeEmbeddedSignupWeb na página web; deep link cortejo://config/whatsapp?connected=1; deploy hosting + functions

**Arquivos:** public/embedded-signup/index.html, functions/SRC/embeddedSignup.ts, services/embeddedSignup.ts

**Tags:** whatsapp, embedded-signup, oauth, mobile, cortejo

---

## 23/06/2026 — cortejo — whatsappSalonEnabled true no Firestore mas app continua bloqueado

**Erro:** whatsappSalonEnabled true no Firestore mas app continua bloqueado

**Contexto:** Feature flag platformConfig — Mais → WhatsApp do salão

**Causa:** (1) Doc criado em artifacts/system (caminho errado) em vez de artifacts/cortejo/system/platformConfig; (2) build/OTA antigo com alertWhatsAppOwnNumberInDevelopment hardcoded ignora Firestore; (3) flag false ou tipo string no Console

**Solução:** Path canônico artifacts/{ns}/system/platformConfig; campo boolean true; publicar OTA/build com useWhatsappSalonFeature; onSnapshot para atualização em tempo real; ver whatsapp-salao-expo-padrao.md §14

**Arquivos:** services/platformConfig.ts, hooks/useWhatsappSalonFeature.ts, app/(tabs)/mais.tsx, firestore.rules

**Tags:** whatsapp, feature-flag, firestore, ota, cortejo

---

## 23/06/2026 — cortejo — Invalid App ID no Embedded Signup Meta

**Erro:** Invalid App ID no Embedded Signup Meta

**Contexto:** App teste Lash match 2 — Conectar meu WhatsApp

**Causa:** `META_APP_ID` truncado no `functions/.env` (`2665657141398467` em vez de `26656571413984672` — faltava dígito final)

**Solução:** Conferir ID completo em developers.facebook.com → Básico; atualizar `.env`; `npm run build` + redeploy embedded signup; `META_APP_SECRET` da **mesma** app

**Arquivos:** functions/.env, functions/SRC/embeddedSignup.ts, obsidian/fabrica/whatsapp-salao-expo-padrao.md §17

**Tags:** whatsapp, embedded-signup, meta, cortejo

---

## 23/06/2026 — cortejo — featureType coexistence incorreto no Embedded Signup

**Erro:** featureType `coexistence` incorreto no Embedded Signup

**Contexto:** Extras FB.login / WA_EMBEDDED_SIGNUP

**Causa:** Valor `'coexistence'` no featureType — Meta espera `whatsapp_business_app_onboarding` para fluxo Coexistence

**Solução:** `COEXISTENCE_FEATURE_TYPE=whatsapp_business_app_onboarding` em `functions/.env`; `embeddedSignupPageConfig` retorna featureType correto

**Arquivos:** functions/SRC/embeddedSignup.ts, functions/.env

**Tags:** whatsapp, embedded-signup, meta, cortejo

---

## 23/06/2026 — cortejo — platformConfig criado no caminho errado do Firestore

**Erro:** platformConfig criado no caminho errado do Firestore

**Contexto:** Feature flag whatsappSalonEnabled — Firebase Console

**Causa:** Doc em `artifacts/system` (campo solto no documento `system`) em vez de `artifacts/cortejo/system/platformConfig`

**Solução:** Criar coleção `system` **dentro** do documento `cortejo`; doc `platformConfig` com campo boolean; MCP Firebase `firestore_update_document` ou Console no breadcrumb correto

**Arquivos:** services/platformConfig.ts, firestore.rules, obsidian/fabrica/whatsapp-salao-expo-padrao.md §14

**Tags:** whatsapp, feature-flag, firestore, cortejo

---

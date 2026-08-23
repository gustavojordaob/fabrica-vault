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

## 01/07/2026 — zenpro — Capinha escura tapando foto inteira após efeitos de realismo

**Erro:** Capinha escura tapando foto inteira após efeitos de realismo

**Contexto:** N/A

**Causa:** 

**Solução:** createCameraCutoutOverlay tratava corpo azul inteiro do iphone-overlay.png como recorte escuro. Removido cutout/bezel de corpo; overlay só extrai traços brancos das lentes no topo 30%; máscara só clip; sombra interna max 15% inset 8px; borda fina 2px.

**Arquivos:** N/A

**Tags:** 

---

## 01/07/2026 — zenpro — Reflexo diagonal e lip branco lavavam metade da capinha

**Erro:** Reflexo diagonal e lip branco lavavam metade da capinha

**Contexto:** N/A

**Causa:** 

**Solução:** Removidos specularHighlight e lip; borda reduzida para 28%; sombra interna 8%; placa câmera 18%. Foto nítida sem camadas claras no centro.

**Arquivos:** N/A

**Tags:** 

---

## 01/07/2026 — zenpro — Pedido pago no mock não aparece no admin/revendedor

**Erro:** Pedido pago no mock não aparece no admin/revendedor

**Contexto:** Checkout raiz /checkout gravava em pedidos/ (legado). Admin lista só lojas/{lojaId}/pedidos. CarrinhoProvider duplicado no layout [slug] isolava estado do carrinho.

**Causa:** Fluxo legado criarPedido.ts + admin pedidoAdminService só lê subcoleção por loja; compra pela home / sem slug não vincula lojaId.

**Solução:** Remover CarrinhoProvider aninhado; persistir lojaId/slug no carrinho (sessionStorage); useLojaEfetiva + redirect /checkout → /{slug}/checkout; checkout sempre usa criarPedidoLoja.

**Arquivos:** CarrinhoProvider.tsx, LojaLayoutClient.tsx, CheckoutPageContent.tsx, useLojaEfetiva.ts, carrinhoLojaStorage.ts, LojaCarrinhoBinder.tsx, useLojaPaths.ts

**Tags:** zenpro,multitenant,checkout,pedidos,firestore

---

## 02/07/2026 — zenpro — Preview 'Ver capa' mostra a foto menor que no editor

**Erro:** Preview 'Ver capa' mostra a foto menor que no editor

**Contexto:** Editor 2D base 280px; export/preview em 840px

**Causa:** escalaTransform() em exportCaseArt.ts escalava x/y pelo fator mas mantinha scale igual; como scale é multiplicador do tamanho natural da imagem, a foto saía ~1/3 do tamanho na arte/preview

**Solução:** Multiplicar tambem transform.scale pelo fator (scale * fator) em escalaTransform

**Arquivos:** src/features/personalizacao/exportCaseArt.ts

**Tags:** zenpro, konva, personalizacao, preview, capinha

---

## 02/07/2026 — zenpro — Raiz do site '/' entrava na loja do revendedor visitado antes, nao na loja do do

**Erro:** Raiz do site '/' entrava na loja do revendedor visitado antes, nao na loja do dono

**Contexto:** Multitenant: raiz = loja do dono; /[slug] = revendedor

**Causa:** useLojaEfetiva caia no fallback lojaVinculada (ultima loja salva em storage), fazendo a raiz herdar o revendedor

**Solução:** useLojaEfetiva retorna somente o contexto da rota /[slug]; sem lojaCtx retorna null e consumidores usam MARCA_LOJA_EFETIVA / branding Zen Pro

**Arquivos:** src/features/loja/useLojaEfetiva.ts

**Tags:** zenpro, multitenant, loja, marca, roteamento

---

## 02/07/2026 — zenpro — Preview 'Ver capa' mostra a foto menor que no editor e mockup nao muda por model

**Erro:** Preview 'Ver capa' mostra a foto menor que no editor e mockup nao muda por modelo

**Contexto:** Editor 2D base 280px; export/preview 840px; camera procedural por modeloId

**Causa:** 1) escalaTransform() escalava x/y mas nao o scale (multiplicador do tamanho natural) -> foto ~1/3. 2) getCameraSpec/getCaseFrameSpec so tinham preset iphone-17-pro-max -> todo modelo caia no mesmo fallback

**Solução:** 1) scale*fator em escalaTransform. 2) CAMERA_PRESETS reutilizaveis + PRESET_POR_MODELO + resolver le cameraPresetId de modelo/produto; admin escolhe preset+cor no cadastro do modelo

**Arquivos:** src/features/personalizacao/exportCaseArt.ts, cameraModules.ts, catalogo/personalizacaoVisual.ts, admin/catalogo/modeloAdminService.ts, app/admin/(painel)/modelos/ModeloFormPageClient.tsx

**Tags:** zenpro, konva, personalizacao, preview, capinha, mockup, multitenant

---

## 02/07/2026 —  — zenpro mobile: editor de personalizacao estourava a largura (foto parecia ocupar

**Erro:** zenpro mobile: editor de personalizacao estourava a largura (foto parecia ocupar tudo), menus do admin/loja sumiam para o lado, imagem nao aparecia no checkout mobile e botoes colavam no fim da tela

**Contexto:** Next.js 16 export estatico + Konva; projeto zenpro-capinhas

**Causa:** 

**Solução:** 1) CaseEditor: Stage passou a escalar via ResizeObserver (fitScale = min(1, (largura-24)/W)) mantendo geometria base 280 e transform 1:1. 2) AdminShell e StoreHeader ganharam menu hamburguer (lg:hidden/md:hidden) com painel vertical. 3) Imagem no checkout mobile: fallback sem CORS agora usa cache-buster (?nocors=1) para nao colidir com a request crossOrigin que falha no Safari mobile. 4) Classe .pb-safe (max(1.25rem, env(safe-area-inset-bottom)+.75rem)) nos rodapes de modais e paginas. 5) Selecao de texto: removido stroke/box colorido do CaseTextNode (nao confundir cliente com o visual final).

**Arquivos:** N/A

**Tags:** 

---

## 02/07/2026 — zenpro — No mobile (Safari) o preview Konva 'como ficou sua capinha' nao carregava e no c

**Erro:** No mobile (Safari) o preview Konva 'como ficou sua capinha' nao carregava e no carrinho a foto aparecia no canto superior direito; no upload dava flash de super-zoom antes de ajustar

**Contexto:** CasePreview usava wrapper com transform:scale CSS; CaseEditor mostrava DEFAULT_TRANSFORM antes do cover ser calculado

**Causa:** 

**Solução:** CasePreview passou a escalar o proprio Stage (scaleX/scaleY) em vez de transform CSS. CaseEditor so renderiza a foto principal quando o cover ja foi aplicado para a URL atual (state fitUrl/fotoPronta), eliminando o flash de super-zoom.

**Arquivos:** src/features/personalizacao/CasePreview.tsx, src/features/personalizacao/CaseEditor.tsx

**Tags:** 

---

## 02/07/2026 — zenpro — Admin mobile: botões de ação (Desativar/Inativar, Ver detalhe) das listas ficava

**Erro:** Admin mobile: botões de ação (Desativar/Inativar, Ver detalhe) das listas ficavam tortos e quase intocáveis no celular

**Contexto:** Listas do admin (Tipos, Pedidos, Produtos) usavam tabela com coluna de Ações alinhada à direita; no celular a tabela era larga demais e os botões apertavam/estouravam.

**Causa:** Layout único de tabela para todos os breakpoints; coluna de ações à direita fica inacessível em telas estreitas (mesmo com overflow-x-auto os botões ficam fora da viewport).

**Solução:** Padrão responsivo: tabela em 'hidden sm:block' (desktop) + lista de CARDS empilhados em 'sm:hidden' (mobile), com botões full-width (flex-1, py-2.5, active:bg) fáceis de tocar. Status vira badge. Aplicado em Tipos, Pedidos e Produtos.

**Arquivos:** src/app/admin/(painel)/tipos/TiposAdminPageClient.tsx, src/app/admin/(painel)/pedidos/PedidosAdminPageClient.tsx, src/app/admin/(painel)/produtos/ProdutosAdminPageClient.tsx

**Tags:** zenpro, admin, mobile, responsivo, tabela, cards

---

## 03/07/2026 — zenpro — Revendedor clicava em 'Pedir reposição' e caía no Dashboard, sem abrir a tela de

**Erro:** Revendedor clicava em 'Pedir reposição' e caía no Dashboard, sem abrir a tela de reposição

**Contexto:** Admin multitenant; rota /admin/reposicao existe e ReposicaoPageClient está completo. Link no AdminShell aponta certo.

**Causa:** AdminRouteGuard.revendedorRotaPermitida() tinha whitelist de rotas para revendedor SEM /admin/reposicao. Como revendedor não passa em revendedorPodeAcessarPainelMarca, o guard redirecionava para adminHomePath (=/admin, dashboard).

**Solução:** Adicionar `if (pathname === '/admin/reposicao') return true;` em revendedorRotaPermitida (AdminRouteGuard.tsx). Regra: toda rota nova acessível a revendedor precisa entrar nessa whitelist.

**Arquivos:** src/components/admin/AdminRouteGuard.tsx

**Tags:** zenpro, admin, route-guard, reposicao, revendedor, redirect

---

## 03/07/2026 — zenpro — Revendedor clicava em 'Pedir reposição' e caía no Dashboard, sem abrir a tela de

**Erro:** Revendedor clicava em 'Pedir reposição' e caía no Dashboard, sem abrir a tela de reposição

**Contexto:** Admin multitenant; rota /admin/reposicao existe e ReposicaoPageClient completo; link no AdminShell correto.

**Causa:** AdminRouteGuard.revendedorRotaPermitida() não listava /admin/reposicao; como revendedor não passa em revendedorPodeAcessarPainelMarca, o guard redirecionava para adminHomePath (/admin dashboard).

**Solução:** Adicionar 'if (pathname === /admin/reposicao) return true;' em revendedorRotaPermitida (AdminRouteGuard.tsx). Toda rota nova acessível a revendedor precisa entrar nessa whitelist.

**Arquivos:** src/components/admin/AdminRouteGuard.tsx

**Tags:** zenpro, admin, route-guard, reposicao, revendedor, redirect

---

## 03/07/2026 — cortejo — Error validating verification code. Please make sure your redirect_uri is identi

**Erro:** Error validating verification code. Please make sure your redirect_uri is identical to the one you used in the OAuth dialog request

**Contexto:** Embedded Signup WhatsApp no mobile: Meta diz que vinculou, mas ao finalizar (completeEmbeddedSignupWeb) da erro; whatsapp.status vira 'error'.

**Causa:** No mobile a pagina public/embedded-signup usa launchSignupRedirect() -> OAuth dialog real com redirect_uri=https://cortejo-app.web.app/embedded-signup/. O codigo retornado exige o MESMO redirect_uri na troca por token. Mas exchangeCodeForToken (functions/SRC/embeddedSignup.ts) fazia /oauth/access_token SEM redirect_uri (correto so para code do FB.login JS SDK do desktop).

**Solução:** Passar redirect_uri na troca quando o code veio do redirect: exchangeCodeForToken(code, redirectUri?) inclui &redirect_uri quando presente; executeEmbeddedSignupCompletion e as functions completeEmbeddedSignup/completeEmbeddedSignupWeb propagam redirectUri; index.html seta captured.redirectUri = oauthRedirectUri() quando le code da URL e envia no body. FB.login desktop continua sem redirect_uri (captured.redirectUri null).

**Arquivos:** functions/SRC/embeddedSignup.ts, public/embedded-signup/index.html

**Tags:** whatsapp,embedded-signup,meta,oauth,redirect_uri,cortejo

---

## 03/07/2026 — cortejo — Nao foi possivel identificar a conta WhatsApp Business. Conclua o fluxo Meta ate

**Erro:** Nao foi possivel identificar a conta WhatsApp Business. Conclua o fluxo Meta ate o fim e tente novamente.

**Contexto:** Embedded Signup WhatsApp no mobile (fluxo redirect). Depois de corrigir o redirect_uri, a troca do code por token funciona, mas ao concluir da esse erro ao voltar para /embedded-signup.

**Causa:** No fluxo redirect (mobile) a Meta volta so com ?code na URL, SEM waba_id/phone_number_id (esses so chegam via postMessage WA_EMBEDDED_SIGNUP do popup, que nao existe no redirect). No servidor wabaId fica vazio e fetchWabaIdFromAccessToken usa /me/businesses, que volta vazio porque o token do Embedded Signup tem escopo granular preso a WABA (nao lista businesses).

**Solução:** Adicionar fetchWabaIdViaDebugToken: GET /debug_token?input_token={token}&access_token={appId}|{appSecret} e extrair granular_scopes[].target_ids[0] (whatsapp_business_management, fallback whatsapp_business_messaging). Usar como fonte principal do wabaId em executeEmbeddedSignupCompletion, com /me/businesses como fallback. phone_number_id continua vindo de /{wabaId}/phone_numbers.

**Arquivos:** functions/SRC/embeddedSignup.ts (Cortejo e LashMatch)

**Tags:** whatsapp,embedded-signup,meta,oauth,debug_token,waba,granular_scopes,cortejo,lashmatch

---

## 03/07/2026 — cortejo — WhatsApp conectado (own/live) mas confirmacao/lembrete continua saindo pelo nume

**Erro:** WhatsApp conectado (own/live) mas confirmacao/lembrete continua saindo pelo numero da plataforma (sender: shared)

**Contexto:** Salao adilson-UG26K0 com whatsapp.status=live, effectiveSender=own, phoneNumberId setado, planTier=plano1, planMsgLimit=600, planExpiresAt futuro (assinatura ativa) — mas logs de enviarConfirmacaoAgendamento mostravam sender:shared.

**Causa:** resolveSender (functions/SRC/whatsappSender.ts) usava tenant.plan !== 'pro' como gate. O campo plan do salao estava 'free' mesmo com assinatura ativa (planTier/planExpiresAt) — caso classico iOS/RevenueCat ou grace period onde plan fica 'free' com acesso pago vigente. Assim caia em shared antes de checar own.

**Solução:** resolveSender passou a considerar Pro = plan==='pro' OU subscriptionActive (salonHasActiveSubscription(data), que checa trial/planExpiresAt/MP). tenantFromSalonDoc agora seta subscriptionActive: salonHasActiveSubscription(data). Condicao de own agora so exige wa.status==='live' && phoneNumberId (isPro ja garantido no gate).

**Arquivos:** functions/SRC/whatsappSender.ts

**Tags:** whatsapp,sender,own,shared,plan,planTier,assinatura,resolveSender,cortejo

---

## 03/07/2026 — cortejo — Assinatura MP cancelada zerava plan para 'free' imediatamente, perdendo acesso P

**Erro:** Assinatura MP cancelada zerava plan para 'free' imediatamente, perdendo acesso Pro do grace period (periodo ja pago)

**Contexto:** Salao adilson-UG26K0 (pagador gustavo.jordao@jointecnologia.com.br): assinou plano1, foi cobrado, cancelou 24/06 com currentPeriodEnd/planExpiresAt 29/07. plan ficou 'free' apesar do periodo pago vigente.

**Causa:** mpCancelarAssinatura (index.ts) e syncSalonFromPreapproval (mercadoPagoAssinatura.ts) setavam plan: planActive ? 'pro' : 'free'. Em CANCELLED, planActive=false => plan 'free' na hora, ignorando planExpiresAt futuro (grace). Alem disso resolveSender usava plan==='pro'.

**Solução:** 1) mpCancelarAssinatura: plan = graceValido ? 'pro' : 'free' (graceValido = planExpiresAt > now). 2) syncSalonFromPreapproval: cancelledComGrace (periodEndIso/salonSubscriptionPeriodValid) mantem plan 'pro' e planTier/planMsgLimit; so limpa apos expirar. 3) resolveSender (whatsappSender.ts) passou a usar subscriptionActive = salonHasActiveSubscription(data) (time-aware, cobre trial/periodo/MP/legado) em vez de plan==='pro'. 4) Corrigido dado do salao: plan=pro (planExpiresAt 29/07 futuro).

**Arquivos:** functions/SRC/index.ts, functions/SRC/mercadoPagoAssinatura.ts, functions/SRC/whatsappSender.ts

**Tags:** mercadopago,assinatura,cancelamento,grace-period,plan,planExpiresAt,whatsapp,resolveSender,cortejo

---

## 03/07/2026 — cortejo — (#132001) Template name (agendamento_confirmado_salao_v5) does not exist in pt_B

**Erro:** (#132001) Template name (agendamento_confirmado_salao_v5) does not exist in pt_BR — confirmacao/lembrete falha ao enviar pelo numero proprio do salao (WABA propria)

**Contexto:** Salao com WhatsApp conectado (own/live) e assinatura ativa. resolveSender ja retornava 'own' corretamente, mas o envio de template pela API caía com 132001.

**Causa:** Templates WhatsApp sao por WABA. Os templates v4/v5 (agendamento_confirmado_salao_v5, lembrete_agendamento_salao_v5, lembrete_agendamento_salao_7d_v5) so estao aprovados na WABA da plataforma (numero compartilhado). A WABA propria do salao (Embedded Signup) nao tem esses templates → 132001 ao enviar pelo phoneNumberId do salao.

**Solução:** 1) enviarTemplateWhatsApp: ao falhar com 132001 enviando por numero proprio, faz fallback automatico para o numero compartilhado da plataforma (mensagem nao se perde) e sinaliza templateMissing. 2) Nova funcao provisionSalonWhatsAppTemplates(wabaId) cria os templates v4/v5 (UTILITY, pt_BR) na WABA do salao — idempotente (template ja existe = ok). Chamada na finalizacao do Embedded Signup e sob demanda quando um envio detecta templateMissing (auto-heal). Apos aprovacao da Meta, os proximos envios saem pelo numero proprio. completeEmbeddedSignup* passaram a declarar o secret WHATSAPP_TOKEN.

**Arquivos:** functions/SRC/whatsapp.ts, functions/SRC/whatsappTemplates.ts, functions/SRC/embeddedSignup.ts, functions/SRC/index.ts (Cortejo e espelhado no LashMatch: functions/SRC/whatsapp.ts, embeddedSignup.ts, index.ts)

**Tags:** whatsapp,meta,template,132001,waba,embedded-signup,provisionamento,fallback,cortejo,lashmatch

---

## 03/07/2026 — cortejo — (#132001) Template name (agendamento_confirmado_salao_v5) does not exist in pt_B

**Erro:** (#132001) Template name (agendamento_confirmado_salao_v5) does not exist in pt_BR — confirmacao/lembrete falha ao enviar pelo numero proprio do salao

**Contexto:** Salao com WhatsApp conectado (own/live) e assinatura ativa. resolveSender ja retornava 'own', mas o envio caia com 132001.

**Causa:** Templates WhatsApp sao por WABA. Os templates v4/v5 so estao aprovados na WABA da plataforma; a WABA propria do salao (Embedded Signup) nao os tem.

**Solução:** enviarTemplateWhatsApp faz fallback ao numero compartilhado no 132001 e sinaliza templateMissing; provisionSalonWhatsAppTemplates(wabaId) cria os templates na WABA do salao (idempotente) na conexao e sob demanda (auto-heal). completeEmbeddedSignup* passam a ter o secret WHATSAPP_TOKEN.

**Arquivos:** functions/SRC/whatsapp.ts, whatsappTemplates.ts, embeddedSignup.ts, index.ts (Cortejo + LashMatch)

**Tags:** whatsapp,meta,template,132001,waba,embedded-signup,fallback,cortejo,lashmatch

---

## 04/07/2026 —  — Ver capa falhava; troca entre fotos resetava transform; so uma foto visivel

**Erro:** Ver capa falhava; troca entre fotos resetava transform; so uma foto visivel

**Contexto:** N/A

**Causa:** 

**Solução:** Multi-layer CaseEditor com fotoAtivaId; export multi-foto; load blob URL; fit so na primeira vez (transform padrao); PreviewCapaModal recebe fotos[]

**Arquivos:** N/A

**Tags:** zenpro, personalizacao, konva, preview

---

## 04/07/2026 —  — blob ERR_FILE_NOT_FOUND ao ver capa ao adicionar segunda foto

**Erro:** blob ERR_FILE_NOT_FOUND ao ver capa ao adicionar segunda foto

**Contexto:** N/A

**Causa:** 

**Solução:** useEffect revogava blob URLs a cada mudanca em fotos[]; preview passa a usar fotoUrl Firebase; revoke so no unmount

**Arquivos:** N/A

**Tags:** zenpro, blob, preview, personalizacao

---

## 14/07/2026 — zenpro — Borda da capinha sumia em fotos claras; ao trocar foto a anterior ficava até o u

**Erro:** Borda da capinha sumia em fotos claras; ao trocar foto a anterior ficava até o upload acabar (ou empilhava)

**Contexto:** editor e preview mockup

**Causa:** Stroke único/clarinho sem contraste; Trocar esperava upload Firebase antes de atualizar o state da foto

**Solução:** CASE_BORDER dual com anel escuro mais opaco/grosso; Trocar aplica preview local imediato (substituir ativa) e só depois sobe fotoUrl; Adicionar empilha

**Arquivos:** caseVisualConstants.ts, CaseEditor.tsx, CasePreview.tsx, caseFrame.ts, PersonalizarEditor.tsx

**Tags:** zenpro,personalizacao,borda,trocar-foto

---

## 15/07/2026 — zenpro — Checkout Pro Mercado Pago: botão Pagar cinza / parcelas com juros apesar do site

**Erro:** Checkout Pro Mercado Pago: botão Pagar cinza / parcelas com juros apesar do site dizer 2x sem juros

**Contexto:** Tela Revise o seu pagamento — Visa 1x R$ 61,31 Sem acréscimo, Pagar desabilitado

**Causa:** 1) Self-purchase ou conta incompleta no MP trava o botão. 2) Sem juros não é só copy no app — precisa ativar no painel do vendedor. Preferência também pode travar com total/itens desalinhados ou statement_descriptor inválido.

**Solução:** Ativar parcelamento sem juros no painel MP até 2x. Pagar com outra conta (aba anônima). Preference hardened: alinhar itens ao totalCentavos, descriptor ZENPRO, e-mail do Auth no payer. Docs em docs/mercadopago-zenpro.md + fabrica/mercadopago-integration.md.

**Arquivos:** functions/src/mercadoPagoCheckout.ts, docs/mercadopago-zenpro.md, src/features/pagamentos/pagamentoConfig.ts, obsidian/fabrica/mercadopago-integration.md

**Tags:** mercadopago,checkout-pro,zenpro,parcelas

---

## 15/07/2026 — zenpro — Checkout Pro: Seu pagamento foi recusado (Operação #168027115349)

**Erro:** Checkout Pro: Seu pagamento foi recusado (Operação #168027115349)

**Contexto:** Dois cartões diferentes recusados na tela MP; mensagem recomenda outro meio/dispositivo

**Causa:** status_detail=cc_rejected_high_risk — antifraude do Mercado Pago (não erro de integração do Zen Pro). Conta/comprador/dispositivo com score de risco alto; comum em conta nova ou teste do próprio vendedor.

**Solução:** Confirmar na API GET /v1/payments/{id}. Orientar: PIX/boleto para validar fluxo; pagar com comprador real em outro dispositivo; completar dados da conta vendedor no MP; se persistir, abrir chamado MP com o ID da operação. Código Zen Pro não força essa recusa.

**Arquivos:** functions/src/mercadoPagoCheckout.ts (preference ok)

**Tags:** mercadopago,cc_rejected_high_risk,antifraude,zenpro

---

## 20/07/2026 — sinaflor — ImportacaoMadeiraToraService: return antecipado em processarLinha omitia erro SI

**Erro:** ImportacaoMadeiraToraService: return antecipado em processarLinha omitia erro SISTAXON quando havia outros erros na linha

**Contexto:** N/A

**Causa:** 

**Solução:** Acumular validações (SISTAXON, tora, volume) antes do return final; só monta registro válido se msgs estiver vazia.

**Arquivos:** N/A

**Tags:** 

---

## 22/07/2026 —  — PWA análise: arrastar cílios move a página; expandir foto fica tela preta

**Erro:** PWA análise: arrastar cílios move a página; expandir foto fica tela preta

**Contexto:** N/A

**Causa:** ScrollView captura o gesto no Chrome; Modal do RN-web colapsa layout da Image (absolute + aspectRatio)

**Solução:** WebLashSticker: touchAction none + onDragStateChange pausa ScrollView; fullscreen web usa overlay absoluto com Image contain (nativo mantém Modal)

**Arquivos:** N/A

**Tags:** pwa,web,analysisResult,scroll,modal

---

## 22/07/2026 — lashmatch — PWA abre sempre em pagamentos/assinatura e some análise

**Erro:** PWA abre sempre em pagamentos/assinatura e some análise

**Contexto:** N/A

**Causa:** app/index.tsx após WEB_BOOT_TIMEOUT_MS (4s) decidia rota mesmo com plano ainda loading — temAcessoEfetivo false → /plano-escolha

**Solução:** Timeout só força Login se não houver user; com user espera Firestore. PlanoAccessRedirect devolve às tabs quando temAcessoEfetivo. Detecção PWA ampliada (minimal-ui + sessionStorage).

**Arquivos:** app/index.tsx, components/PlanoAccessRedirect.tsx, utils/pwaWeb.ts

**Tags:** pwa,paywall,plano,analise

---

## 22/07/2026 — lashmatch — PWA análise expandir tela cheia preto trava

**Erro:** PWA análise expandir tela cheia preto trava

**Contexto:** N/A

**Causa:** Fullscreen/Modal no Chrome PWA fica preto e sem fechar confiável

**Solução:** Desabilitar expandir/fullscreen só na web/PWA (botão e toque na foto); nativo mantém Modal.

**Arquivos:** app/analysisResult.tsx

**Tags:** pwa,analysisResult,fullscreen

---

## 22/07/2026 — lashmatch — Foto no histórico da cliente sempre a última análise

**Erro:** Foto no histórico da cliente sempre a última análise

**Contexto:** N/A

**Causa:** uploadClientPhoto sempre gravava em .../clientes/{id}/profile.jpg — cada análise sobrescrevia o mesmo arquivo; histórico apontava para a mesma URL/path e o card ainda fazia fallback para cliente.fotoUrl (sempre a última)

**Solução:** unique:true grava em .../analises/{timestamp}_{uuid}.jpg; analysisResult envia unique; card do histórico usa só item.fotoComCiliosUrl

**Arquivos:** functions/SRC/index.ts uploadClientPhoto; app/analysisResult.tsx; app/clientes/[id].tsx

**Tags:** storage,historico,analise,foto

---

## 22/07/2026 — lashmatch — Tela preta ao clicar Voltar para a Home na análise

**Erro:** Tela preta ao clicar Voltar para a Home na análise

**Contexto:** N/A

**Causa:** Voltar para Home usava router.navigate('/') — no PWA/web o index é splash preto e o redirect para tabs falhava/travava

**Solução:** router.replace('/(tabs)') direto; no web Voltar também vai às tabs; rAF antes de leave

**Arquivos:** app/analysisResult.tsx

**Tags:** pwa,analysisResult,navegacao

---

## 22/07/2026 — lashmatch — Tela preta ao voltar Home da análise (ainda)

**Erro:** Tela preta ao voltar Home da análise (ainda)

**Contexto:** N/A

**Causa:** 1) gate PWA phase pending = View preta sem children ao navegar; 2) captureRef no web travava o save; 3) replace client-side insuficiente no PWA

**Solução:** Sem pending preto; skip captureRef no web; timeout 12s no persist; window.location.assign('/'); index com user → Redirect tabs

**Arquivos:** PwaMobileRequireInstall, analysisResult, index

**Tags:** pwa,tela-preta,analysisResult

---

## 22/07/2026 — lashmatch — PWA tela preta mesmo após reinstalar (cache)

**Erro:** PWA tela preta mesmo após reinstalar (cache)

**Contexto:** N/A

**Causa:** Cache SW/HTML + splash / preto + tabs bootLoading preto ao remount

**Solução:** SW v3 limpa caches; HTML no-cache; start_url /(tabs)/; goHome location.replace /(tabs)/?bust; tabs web sem boot preto

**Arquivos:** sw.js, +html, firebase.json, tabs/_layout, analysisResult, manifest

**Tags:** pwa,cache,sw,tela-preta

---

## 22/07/2026 — lashmatch — PWA sem login e pedindo assinar plano

**Erro:** PWA sem login e pedindo assinar plano

**Contexto:** N/A

**Causa:** start_url /(tabs)/ abria o app sem Login; sem user a Home mostrava TelaBloqueadaPlano (assine) em vez de Login

**Solução:** start_url /; tabs sem user → Login; PlanoAccessRedirect manda Login se !user; index espera plano antes de tabs

**Arquivos:** manifest, index, PlanoAccessRedirect, tabs/_layout

**Tags:** pwa,login,paywall

---

## 22/07/2026 — lashmatch — PWA histórico: todas as análises mostram a última foto

**Erro:** PWA histórico: todas as análises mostram a última foto

**Contexto:** Teste no PWA instalado; cards do histórico da cliente

**Causa:** uploadClientPhoto default gravava profile.jpg; câmera e análises antigas compartilhavam o mesmo path — sobrescrever atualiza todas as URLs. Logs 22/07 ainda mostravam maioria em profile.jpg; unique só às vezes.

**Solução:** Default da function = path único em analises/; só profile.jpg com asProfile:true (câmera). UI ignora fotoComCiliosUrl que aponta para profile.jpg. SW v5.

**Arquivos:** functions/SRC/index.ts; app/camera.tsx; app/clientes/[id].tsx; app/analysisResult.tsx; public/sw.js

**Tags:** pwa,storage,historico,foto,uploadClientPhoto

---

## 22/07/2026 — lashmatch — PWA: todas as análises mostram a última foto

**Erro:** PWA: todas as análises mostram a última foto

**Contexto:** PWA — cards histórico da cliente

**Causa:** Default uploadClientPhoto = profile.jpg; câmera e análises antigas compartilhavam path — sobrescrever muda todas as fotos do histórico. Logs 22/07: maioria ainda em profile.jpg.

**Solução:** Default = path único em analises/; profile.jpg só com asProfile:true (câmera). UI ignora fotoComCiliosUrl de profile.jpg. SW v5.

**Arquivos:** functions/SRC/index.ts; app/camera.tsx; app/clientes/[id].tsx; app/analysisResult.tsx; public/sw.js

**Tags:** pwa,storage,historico,foto

---

## 22/07/2026 — lashmatch — PWA histórico: foto da análise sem cílios

**Erro:** PWA histórico: foto da análise sem cílios

**Contexto:** Histórico da cliente após análise no PWA

**Causa:** No PWA o persist pulava captureRef (travava tela preta) e enviava só fotoFrenteBase64 sem os stickers de cílios

**Solução:** Composite no canvas (composeWebLashPhoto) com transforms dos WebLashSticker + timeout; timeout de save web 18s; SW v6

**Arquivos:** utils/webCompositeLashPhoto.ts; app/analysisResult.tsx; public/sw.js

**Tags:** pwa,historico,cilios,canvas,analysisResult

---

## 22/07/2026 — sinaflor — HttpMessageNotReadableException: Cannot deserialize TramitacaoFinalizarRequestDT

**Erro:** HttpMessageNotReadableException: Cannot deserialize TramitacaoFinalizarRequestDTO out of START_ARRAY token

**Contexto:** POST /api/licenciamento/gestao/{id}/tramitacao/finalizar ao finalizar tramitação na gestão de licenciamento

**Causa:** Front enviava JSON array de TramitacaoHistoricoDTO; back espera objeto { tramitacoes: TramitacaoItemDTO[] }

**Solução:** Ajustar front: TramitacaoService.finalizar envia TramitacaoFinalizarRequestDTO e gestao-tramitacao.component mapeia itens (idTipoTramite, despacho, analistas, ordem...). Também corrigiu URL do PUT rascunho para /{id}/tramitacao/rascunho

**Arquivos:** front_end/src/app/service/tramitacao.service.ts; front_end/.../gestao-tramitacao.component.ts

**Tags:** sinaflor,tramitacao,jackson,angular

---

## 22/07/2026 — sinaflor — Erro genérico ao finalizar tramitação (login analista inválido no mock)

**Erro:** Erro genérico ao finalizar tramitação (login analista inválido no mock)

**Contexto:** Finalizar tramitação — front mostra erro apesar de SCA2 validar sessão

**Causa:** Lista de analistas no front usava mock com login "1","2"… Back valida login como CPF(11)/CNPJ(14) e rejeita com 400. Front mostrava só mensagem genérica. Log SCA2 200 era só validação de sessão antes da chamada.

**Solução:** Passar a buscar analistas no endpoint real GET .../tramitacao/analistas e exibir error.error.title do BadRequestAlertException no toast

**Arquivos:** tramitacao.service.ts; gestao-tramitacao.component.ts

**Tags:** sinaflor,tramitacao,analistas,mock

---

## 22/07/2026 — sinaflor — Toast [object Object] ao finalizar tramitação com 0 itens

**Erro:** Toast [object Object] ao finalizar tramitação com 0 itens

**Contexto:** Usuário finalizava sem tramitações e via [object Object]; pediu zero mock no finalizar

**Causa:** 1) finalizar já era API real mas toast usava MensagemUtil que devolvia o objeto HTTP → [object Object]. 2) ngSwitchCase='1' (string) vs id number impedia adicionar Análise → fila 0. 3) ainda havia mock de tipos/analistas.

**Solução:** Remover mocks; GET /tramitacao/tipos no back; carregar rascunho; ngSwitchCase=1; extrair title do Problem; bloquear finalizar com fila vazia

**Arquivos:** TramitacaoService.ts, gestao-tramitacao.*, LicenciamentoTramitacaoResource, TipoTramiteLicDTO

**Tags:** sinaflor,tramitacao,mock,angular

---

## 22/07/2026 — sinaflor — Http failure response .../tramitacao/finalizar: 403 Forbidden

**Erro:** Http failure response .../tramitacao/finalizar: 403 Forbidden

**Contexto:** 403 Forbidden em POST .../tramitacao/finalizar

**Causa:** @Secured do POST finalizar exige GERENTE_OPERACIONAL, GERENTE_AUTORIZADOR ou ANALISTA_TECNICO. GET analistas também aceita CONSULTA_GERAL e ATUACAO_FEDERAL — por isso listar funcionava e finalizar dava 403. Login automático local não tinha essas authorities.

**Solução:** Explicar diferença de roles; incluir roles de gestão de licenciamento no application-login-automatico.yml para dev. Em usuário SCA real, atribuir perfil de gerente/analista.

**Arquivos:** gateway/.../application-login-automatico.yml

**Tags:** sinaflor,403,roles,tramitacao

---

## 22/07/2026 — cortejo — Botão Confirmar agendamento na web não faz nada; formulário sem scroll

**Erro:** Botão Confirmar agendamento na web não faz nada; formulário sem scroll

**Contexto:** app/agendamento/[id].tsx na web desktop (cortejo-app.web.app)

**Causa:** Alert.alert com múltiplos botões é inconsistente no RN Web (confirmação silenciosa). KeyboardAvoidingView behavior=height na web cortava o conteúdo e impedia scroll/clique no rodapé.

**Solução:** Usar confirmAction/confirmDestructive/alertMessage (window.confirm/alert na web). KeyboardAwareScrollView na web renderiza só ScrollView com flex:1 e indicador de scroll.

**Arquivos:** utils/confirmAction.ts, components/ui/KeyboardAwareScrollView.tsx, app/agendamento/[id].tsx

**Tags:** web,agendamento,Alert,scroll

---

## 22/07/2026 — cortejo — Voltar na tela de planos no iPhone mostra goback em vez de ir para home

**Erro:** Voltar na tela de planos no iPhone mostra goback em vez de ir para home

**Contexto:** Tela de planos no iPhone com assinatura RevenueCat ativa

**Causa:** Voltar em PlanoWhatsAppEscolhaView usava router.replace('/planos?stay=1') (rota inexistente). Header iOS vinha de (tabs) sem título → rótulo estranho tipo goBack.

**Solução:** Voltar sempre replace('/(tabs)'). Header custom Início em plano e plano-escolha. allowBack só com assinatura. Stack.Screen plano-escolha com headerBackTitle Início.

**Arquivos:** components/planos/PlanoWhatsAppEscolhaView.tsx, app/config/plano-escolha.tsx, app/config/plano.tsx, app/_layout.tsx

**Tags:** ios,planos,navegacao,header

---

## 22/07/2026 — cortejo — Compras in-app indisponíveis neste build após OTA; planos somem no segundo open

**Erro:** Compras in-app indisponíveis neste build após OTA; planos somem no segundo open

**Contexto:** iPhone: 1ª abertura ok, após fechar vai para planos com erro compras in-app indisponíveis

**Causa:** eas update local sem REVENUECAT_API_KEY_IOS no env (só no EAS Build como secret). OTA gravava extra vazio e no 2º open isRevenueCatAvailable()=false → paywall + planos sumidos.

**Solução:** Não gravar REVENUECAT vazio no extra do OTA. Republicar eas update com --environment production e EXPO_PUBLIC_REVENUECAT_API_KEY_IOS (plaintext — chave appl_ pública). Fallback Firestore se RC indisponível.

**Arquivos:** app.config.ts, eas.json, utils/subscriptionAccess.ts, components/subscription/IosAssinaturaView.tsx

**Tags:** ios,revenuecat,ota,eas-update

---

## 22/07/2026 — cortejo — Login iOS abre paywall em vez da agenda (race RevenueCat)

**Erro:** Login iOS abre paywall em vez da agenda (race RevenueCat)

**Contexto:** Após logout/login no iPhone com assinatura ativa, abria tela de planos em vez da agenda

**Causa:** Sem salonId, bootstrap chamava setEntitlement(false) → checked=true. Index/tabs viam Pro=false já 'checado' e mandavam para plano-escolha antes do Purchases.logIn(salonId).

**Solução:** Sem salonId: reset() (checked=false). Ao bindar tenant: checked=false até logIn. Tabs aguardam RC. Se Pro confirmar no paywall, replace para /(tabs).

**Arquivos:** components/RevenueCatBootstrap.tsx, app/(tabs)/_layout.tsx, components/SubscriptionAccessRedirect.tsx

**Tags:** ios,revenuecat,login,paywall

---

## 22/07/2026 — cortejo — Plano e assinatura redireciona para agenda; voltar em Mensagens não funciona

**Erro:** Plano e assinatura redireciona para agenda; voltar em Mensagens não funciona

**Contexto:** N/A

**Causa:** Redirect Pro→tabs a partir de plano/plano-escolha impedia gerenciar assinatura. Voltar em mensagens falhava com stack inconsistente após replaces.

**Solução:** Remover bounce Pro→tabs no SubscriptionAccessRedirect. Voltar confiável para Mais em plano/mensagens.

**Arquivos:** components/SubscriptionAccessRedirect.tsx, app/config/plano.tsx, app/config/mensagens.tsx, hooks/useReliableHeaderBack.ts

**Tags:** ios,plano,navegacao,mensagens

---

## 23/07/2026 — lashmatch — LashMatch app/index.tsx Unexpected token - chaves extras no fim do arquivo

**Erro:** LashMatch app/index.tsx Unexpected token - chaves extras no fim do arquivo

**Contexto:** Bloqueou eas update production

**Causa:** 

**Solução:** Remover } } } sobrando após o fechamento do componente Index

**Arquivos:** N/A

**Tags:** 

---

## 24/07/2026 —  — Samsung (S26 Ultra) camera mock com fundo branco/bege no overlay

**Erro:** Samsung (S26 Ultra) camera mock com fundo branco/bege no overlay

**Contexto:** N/A

**Causa:** 

**Solução:** No process-rockb2b-camera-frames.mjs: Android nunca copia fill claro do molde H5. O bege do S26 (L~210-240) era classificado como flash LED e passava. Platô sempre escuro em Android; iPhone mantém claro. Cache ?v=8.

**Arquivos:** N/A

**Tags:** 

---

## 24/07/2026 —  — iPhone camera mock com fundo branco do fill de impressao Rock H5; moldes com 1 c

**Erro:** iPhone camera mock com fundo branco do fill de impressao Rock H5; moldes com 1 contorno vermelho falhavam

**Contexto:** N/A

**Causa:** 

**Solução:** process-rockb2b-camera-frames.mjs v=11: ilha pelo 2o contorno vermelho ou bbox do hardware; remove fill branco neutro por componente conectado (anti-alias); mantem bege Samsung (sat/chroma); pixels do H5 dentro da ilha; punch destination-out no editor

**Arquivos:** N/A

**Tags:** 

---

## 26/07/2026 — setmatch — Missing or insufficient permissions / sem permissão suficiente no Avançar da fot

**Erro:** Missing or insufficient permissions / sem permissão suficiente no Avançar da foto do wizard

**Contexto:** N/A

**Causa:** Update usuarios falhava quando role ausente no doc (role == null) ou saveWizardProfile reescrevia role; Storage também podia negar por request.resource.size em upload REST

**Solução:** Rules: se doc sem role, só permite role jogador; se tem role, deve permanecer igual. Removido role do saveWizardProfile. Storage: size opcional. Deploy firestore:rules + storage.

**Arquivos:** N/A

**Tags:** setmatch,firestore,storage,wizard,foto,permission-denied

---

## 26/07/2026 — setmatch — Admin vê tela de peso e volta; usuário logado vê onboarding de novo

**Erro:** Admin vê tela de peso e volta; usuário logado vê onboarding de novo

**Contexto:** N/A

**Causa:** app/index.tsx ignorava isAdminClube e mandava admin para /(tabs)/home ou /primeiro-acesso (wizard/peso); AuthGuard só corrigia depois. Jogador logado podia ver slides se caísse em /onboarding.

**Solução:** Splash e AuthGuard roteiam por role: admin→clube/painel|onboarding; jogador→home|primeiro-acesso. Logado nunca fica em onboarding/(auth). Wizard/primeiro-acesso bloqueados para admin.

**Arquivos:** N/A

**Tags:** setmatch,auth,onboarding,admin,wizard

---

## 26/07/2026 — setmatch — permission-denied ao abrir/criar conversa (getDoc em doc inexistente)

**Erro:** permission-denied ao abrir/criar conversa (getDoc em doc inexistente)

**Contexto:** abrirOuCriarConversaAmigo/Clube e envio de mensagem no chat

**Causa:** allow read em conversas exigia resource.data.participantes; get em documento que ainda não existe falha porque resource é null

**Solução:** Separar allow get (resource == null OR participante) e allow list; client usa try/catch + setDoc merge; Alert no chat ao falhar envio

**Arquivos:** firestore.rules, services/mensagens.ts, app/chat/[id].tsx

**Tags:** firestore,rules,chat,setmatch

---

## 27/07/2026 — zenpro — account_money cannot be excluded + arte H5 sem borda/com câmera preta

**Erro:** account_money cannot be excluded + arte H5 sem borda/com câmera preta

**Contexto:** Checkout após escolher PIX/cartão; download impressão H5 no pedido admin

**Causa:** 1) Preference excluía payment_method account_money — API MP rejeita. 2) Arte H5 era retângulo com punch sem overlay (buraco preto) e sem body-mask da silhueta.

**Solução:** Remover excluded_payment_methods account_money. Export H5: clip mascara com bodyMaskUrl + destination-out + overlay cameraFrameUrl. Botão Regenerar arte H5 no admin.

**Arquivos:** functions/src/mercadoPagoShared.ts; src/features/personalizacao/exportCaseArt.ts; salvarPersonalizacao.ts; regenerarArtesPedido.ts; PedidoItemPreview.tsx

**Tags:** mercadopago,account_money,zenpro,h5,arte-producao

---

## 28/07/2026 — zenpro — parcelas 4x parecem 1x no MP + CORS regenerar H5

**Erro:** parcelas 4x parecem 1x no MP + CORS regenerar H5

**Contexto:** 4x no site vs tela MP; Regenerar arte H5 CORS; home lenta

**Causa:** 1) Checkout Pro 1ª tela nunca lista parcelas — só após Cartão; preference já tinha installments. 2) getBlob falhava / path firebasestorage.app e não usava proxy baixarArquivoStorage.

**Solução:** Reforçar installments/default_installments + copy UX. loadImage: parse .firebasestorage.app + fallback callable baixarArquivoStorage. Home: dynamic below-fold + carousel só slide ativo/vizinhos.

**Arquivos:** loadImageForCanvasExport.ts, mercadoPagoCheckout.ts, HomeLojaPageContent.tsx, HomeHeroCarousel.tsx

**Tags:** mercadopago,parcelas,cors,storage,performance,zenpro

---

## 28/07/2026 — zenpro — download arte pedido admin muito lento

**Erro:** download arte pedido admin muito lento

**Contexto:** Download arte do cliente / H5 no pedido admin demorava muito

**Causa:** Foto ia pelo proxy Cloud Function (cold start + base64). Fontes todas carregadas. Assets sequenciais. Export 1080px.

**Solução:** Img com crossOrigin anonymous (CORS Storage). Paralelo foto/máscara/câmera. Só fontes usadas. Admin export 720px. Sem blur.

**Arquivos:** loadImageForCanvasExport.ts, exportCaseArt.ts, PedidoItemPreview.tsx

**Tags:** performance,cors,export,zenpro,admin

---

## 29/07/2026 — fabrica — Chroma .chroma_db corrompido — indexar_rapido trava após Loading weights / acces

**Erro:** Chroma .chroma_db corrompido — indexar_rapido trava após Loading weights / access violation

**Contexto:** N/A

**Causa:** 

**Solução:** 1) Parar processos Python usando o RAG. 2) python indexar_rapido.py --recriar-banco (move .chroma_db para .bak-TIMESTAMP e reindexa). 3) Para AWS: .\aws-rag\scripts\sync-push.ps1 -SkipIndex -Bucket fabrica-rag-084029330207-us-east-1 -Region us-east-1 (Lambda reinicia App Runner). Alternativa manual: renomear pasta + indexar_rapido.

**Arquivos:** N/A

**Tags:** rag,chroma,aws,windows

---

## 30/07/2026 — zenpro — Desconto PIX no checkout sempre 0% — total e preference MP sem desconto

**Erro:** Desconto PIX no checkout sempre 0% — total e preference MP sem desconto

**Contexto:** Checkout com PIX selecionado não mostrava desconto nem aplicava no total/preference MP, mesmo com % cadastrado no produto ou loja.

**Causa:** intersecaoPagamentoProdutos usava reduce com seed PAGAMENTO_PRODUTO_DEFAULT (descontoPixPercentual=0); Math.min(0, X) sempre zerava o desconto do produto/loja.

**Solução:** Seed da interseção = primeiro produto do carrinho (configs[0]), não o default global. UI do seletor PIX mostra % de desconto + aviso verde; total com linha de desconto e riscado; pedido/MP já usavam totalPago (agora com valor correto).

**Arquivos:** src/features/pagamentos/pagamentoProduto.ts, src/components/loja/SeletorFormaPagamentoOnline.tsx, src/components/loja/CheckoutPageContent.tsx

**Tags:** pix,checkout,desconto,mercadopago

---

## 30/07/2026 — lashmatch — LashMatch eas update SyntaxError app/index.tsx Unexpected token } linha extra

**Erro:** LashMatch eas update SyntaxError app/index.tsx Unexpected token } linha extra

**Contexto:** N/A

**Causa:** 

**Solução:** Remover chave de fechamento órfã no final de app/index.tsx (copia/cola quebrada).

**Arquivos:** N/A

**Tags:** ota,syntax,expo

---

## 30/07/2026 — sinaflor — ExportacaoException ClassCastException String cannot be cast to Long numeroRegis

**Erro:** ExportacaoException ClassCastException String cannot be cast to Long numeroRegistro FormatterEnum.ID

**Contexto:** N/A

**Causa:** LicenciamentoExploracaoListagemDTO.numeroRegistro é String mas @Propriedade usava FormatterEnum.ID (DRIValueFormatter<String, Long>). Na exportação Jasper faz cast para Long e quebra.

**Solução:** Trocar formatter de numeroRegistro para FormatterEnum.TEXTO_NA (null/vazio → N/A, senão o texto).

**Arquivos:** autorizacao/.../LicenciamentoExploracaoListagemDTO.java

**Tags:** sinaflor,exportacao,jasper,formatter,gestao

---

## 30/07/2026 — sinaflor — ExportacaoException ClassCastException String cannot be cast to Long em numeroRe

**Erro:** ExportacaoException ClassCastException String cannot be cast to Long em numeroRegistro (FormatterEnum.ID)

**Contexto:** Exportação PDF/CSV da Gestão de Licenciamento

**Causa:** numeroRegistro é String mas @Propriedade usava FormatterEnum.ID (espera Long). Jasper faz ClassCastException no export.

**Solução:** Alterar formatter de numeroRegistro para FormatterEnum.TEXTO_NA

**Arquivos:** autorizacao/src/main/java/br/gov/ibama/sinaflor2/service/dto/LicenciamentoExploracaoListagemDTO.java

**Tags:** sinaflor,exportacao,jasper,formatter,gestao

---

## 31/07/2026 — lashmatch — EAS iOS build ERRORED Bundle JavaScript — SyntaxError app/index.tsx Unexpected t

**Erro:** EAS iOS build ERRORED Bundle JavaScript — SyntaxError app/index.tsx Unexpected token } linha 57

**Contexto:** N/A

**Causa:** Chave de fechamento órfã no final de app/index.tsx (regressão após fix anterior)

**Solução:** Remover } extra; validar com expo export; novo eas build --auto-submit

**Arquivos:** app/index.tsx

**Tags:** eas,ios,syntax,build

---

## 03/08/2026 — zenpro — FirebaseError: Missing or insufficient permissions ao ler campanhas

**Erro:** FirebaseError: Missing or insufficient permissions ao ler campanhas

**Contexto:** StoreHeader e PromocoesStrip chamam listarCampanhasAtivas() e recebiam Missing or insufficient permissions

**Causa:** Coleção campanhas era nova; rules locais tinham allow read: if true, mas não tinham sido deployadas — default deny no projeto live.

**Solução:** Deploy firebase deploy --only firestore:rules com match /campanhas/{id} allow read: if true; write se isMarca()

**Arquivos:** firestore.rules

**Tags:** firestore,rules,campanhas,permissions

---

## 07/08/2026 — setmatch — permission-denied ao comentar post no feed

**Erro:** permission-denied ao comentar post no feed

**Contexto:** Usuario tentava comentar em /post/[id]; composer tambem ficava sob a barra de navegacao do Android

**Causa:** Regra match /posts/{postId}/comentarios nao estava deployada no Firebase (default deny). Deploy anterior firestore+storage nao refletiu a subcolecao.

**Solução:** Deploy firestore:rules com allow create/read em posts/{id}/comentarios; paddingBottom com useSafeAreaInsets no composer do post.

**Arquivos:** firestore.rules, app/post/[id].tsx

**Tags:** firestore,rules,feed,comentarios,safe-area,setmatch

---

## 07/08/2026 — setmatch — teclado cobria o composer do chat — não dava para ver o que digitava

**Erro:** teclado cobria o composer do chat — não dava para ver o que digitava

**Contexto:** app/chat/[id].tsx no Android/Expo Go

**Causa:** KeyboardAvoidingView sem behavior no Android + SafeAreaView edges bottom competindo com teclado; falta softwareKeyboardLayoutMode resize

**Solução:** KAV behavior height/padding; edges só top; paddingBottom dinâmico com keyboard listeners; scrollToEnd; app.json android.softwareKeyboardLayoutMode=resize

**Arquivos:** app/chat/[id].tsx, app.json

**Tags:** chat,teclado,KeyboardAvoidingView,android,setmatch

---

## 07/08/2026 — setmatch — permission-denied ao se inscrever no torneio (update totalInscritos)

**Erro:** permission-denied ao se inscrever no torneio (update totalInscritos)

**Contexto:** Jogador não podia update no doc torneios — só dono. Deploy firestore:rules setmatch-app-fabrica.

**Causa:** 

**Solução:** Rules: onlyTotalInscritosBump permite +1 em totalInscritos. inscreverTorneio valida status/duplicata; chat opcional. UI lista inscritos; admin libera chave em /clube/torneios e no detalhe com chaveLiberada.

**Arquivos:** N/A

**Tags:** 

---

## 08/08/2026 — fabrica — chromadb InternalError: Error loading hnsw index / Error constructing hnsw segme

**Erro:** chromadb InternalError: Error loading hnsw index / Error constructing hnsw segment reader

**Contexto:** indexar_rapido.py e MCP falhavam ao abrir .chroma_db; Error loading hnsw index

**Causa:** Índice HNSW do Chroma PersistentClient ficou inconsistente (arquivo de segmento quebrado) — tipicamente após kill/crash do processo ou sync parcial.

**Solução:** python indexar_rapido.py --recriar-banco (move .chroma_db para .chroma_db.bak-* e reindexa do zero). Depois .\aws-rag\scripts\sync-push.ps1 -SkipIndex para S3 us-east-1.

**Arquivos:** obsidian/.chroma_db (recriado); aws-rag/scripts/sync-push.ps1; indexar_rapido.py --recriar-banco

**Tags:** chroma,rag,hnsw,aws

---

## 09/08/2026 — cortejo — Botão Sair no canto da Agenda não funciona no web/desktop

**Erro:** Botão Sair no canto da Agenda não funciona no web/desktop

**Contexto:** N/A

**Causa:** AgendaHeaderActions usava Alert.alert com 2 botões — inconsistente no RN Web (mesmo padrão do bug de confirmar agendamento)

**Solução:** Usar confirmDestructive (window.confirm na web) antes de logout

**Arquivos:** components/AgendaHeaderActions.tsx

**Tags:** web,desktop,logout,alert

---

## 11/08/2026 —  — Tipo de Avaliação inválido para a tramitação selecionada — shouldFinalizarUmaTra

**Erro:** Tipo de Avaliação inválido para a tramitação selecionada — shouldFinalizarUmaTramitacao usava codigo APR

**Contexto:** LicenciamentoTramitacaoServiceTest.shouldFinalizarUmaTramitacao falhava em validarFila; UnnecessaryStubbing era efeito colateral.

**Causa:** 

**Solução:** Atualizar o teste para usar codigo válido do TipoAvaliacaoLicEnum para Análise, ex.: ANALISE_TEC_OBRIGATORIA. APR não existe mais no enum.

**Arquivos:** N/A

**Tags:** sinaflor,tramitacao,teste,junit,tipoavaliacao

---

## 12/08/2026 — lashmatch — LashMatch export:web SyntaxError app/index.tsx Unexpected token } chaves extras

**Erro:** LashMatch export:web SyntaxError app/index.tsx Unexpected token } chaves extras

**Contexto:** N/A

**Causa:** 

**Solução:** Remover chaves de fechamento órfãs no final de app/index.tsx (reapareceu antes do hosting deploy).

**Arquivos:** N/A

**Tags:** hosting,syntax,expo,web

---

## 12/08/2026 — lashmatch — LashMatch PWA Android isWhatsAppMetaSetupAllowed true + Pagamentos menu cai no H

**Erro:** LashMatch PWA Android isWhatsAppMetaSetupAllowed true + Pagamentos menu cai no Home

**Contexto:** N/A

**Causa:** 

**Solução:** isWhatsAppMetaSetupAllowed exige !isMobileWebBrowser. Tabs pagamento: remover href:null (usar tabBarButton null). MoreMenu push com delay; rota /pagamento.

**Arquivos:** N/A

**Tags:** pwa,whatsapp,navegacao,web

---

## 12/08/2026 — lashmatch — O domínio do host JSSDK é desconhecido Facebook LashMatch

**Erro:** O domínio do host JSSDK é desconhecido Facebook LashMatch

**Contexto:** N/A

**Causa:** 

**Solução:** No Meta App 990183433661795 → Login do Facebook → Configurações: adicionar Allowed Domains for JavaScript SDK e App Domains com lashmatch.com.br e lashmatch-627fd.web.app (e firebaseapp.com). Valid OAuth Redirect URIs: https://lashmatch.com.br/embedded-signup/ e https://lashmatch-627fd.web.app/embedded-signup/. Liga Login com SDK JS = Sim.

**Arquivos:** N/A

**Tags:** meta,facebook,jssdk,oauth,whatsapp

---

## 12/08/2026 — lashmatch — LashMatch Mais Pagamentos nao abre Android web PWA cai Home

**Erro:** LashMatch Mais Pagamentos nao abre Android web PWA cai Home

**Contexto:** N/A

**Causa:** 

**Solução:** MoreMenu no web usa window.location.assign apos fechar Modal; hrefs sem /(tabs)/; rota /pagamentos fora das tabs.

**Arquivos:** N/A

**Tags:** pwa,android,navegacao,pagamentos,web

---

## 12/08/2026 — lashmatch — LashMatch Android web tabs piscam planos e voltam Home location.assign

**Erro:** LashMatch Android web tabs piscam planos e voltam Home location.assign

**Contexto:** N/A

**Causa:** 

**Solução:** Remover window.location.assign(/) e assign no MoreMenu (remonta index→paywall→tabs). voltarParaInicio = replace /(tabs). Index/tabs: spinner até plano estável; debounce paywall 450ms.

**Arquivos:** N/A

**Tags:** pwa,android,navegacao,paywall,boot

---

## 12/08/2026 — lashmatch — LashMatch Android web Meu plano e Pagamentos abrem Home

**Erro:** LashMatch Android web Meu plano e Pagamentos abrem Home

**Contexto:** N/A

**Causa:** 

**Solução:** openAppRoute parseia ?stay=1 em params (Expo web ignora query string). MoreMenu navega ANTES de fechar Modal. planos.tsx fallback window.location.search. SW v7.

**Arquivos:** N/A

**Tags:** pwa,android,expo-router,planos,pagamentos

---

## 12/08/2026 — lashmatch — LashMatch Android web Pagamentos vai Home colisao tab pagamento

**Erro:** LashMatch Android web Pagamentos vai Home colisao tab pagamento

**Contexto:** N/A

**Causa:** 

**Solução:** Mover tela para /config/pagamentos (como whatsapp). /pagamentos e tab pagamento só Redirect. Menu/Perfil usam PAGAMENTOS_PATH. SW v8.

**Arquivos:** N/A

**Tags:** pwa,android,expo-router,pagamentos

---

## 12/08/2026 — lashmatch — LashMatch EAS Meu plano tela branca loading; Pagamentos nao abre no nativo

**Erro:** LashMatch EAS Meu plano tela branca loading; Pagamentos nao abre no nativo

**Contexto:** N/A

**Causa:** planos.tsx ficava em spinner enquanto temAcessoEfetivo && !stay; stay falhava no EAS. MoreMenu no nativo navegava com Modal aberto e a navegacao era engolida.

**Solução:** Assinante em /planos sempre verMeu plano (sem spinner eterno nem redirect Home). stay coerente (1/true). MoreMenu nativo: onClose + setTimeout 320ms depois openAppRoute; web mantem navigate-before-close. openAppRoute sempre injeta stay=1 para /planos.

**Arquivos:** N/A

**Tags:** eas,planos,pagamentos,expo-router,modal

---

## 12/08/2026 — lashmatch — Expo Go Meu plano tela branca Expo; Pagamentos nao abre em lugar nenhum

**Erro:** Expo Go Meu plano tela branca Expo; Pagamentos nao abre em lugar nenhum

**Contexto:** N/A

**Causa:** 1) Menu Modal: push apos close engolia no nativo; openAppRoute forçava params em /planos e Expo Go ficava em loading branco. 2) Pagamentos em /config/pagamentos redirecionava para plano-escolha ou nao navegava; tela real consolidada em /assinatura.

**Solução:** MoreMenu: pendingHref apos fechar Modal (nativo) / push antes (web). openAppRoute path simples. PAGAMENTOS_PATH=/assinatura com UI completa; legado /pagamentos e /config/pagamentos Redirect. Sem auto-Redirect plano-escolha. planos timeout 6s forceShow.

**Arquivos:** N/A

**Tags:** expo-go,planos,pagamentos,assinatura,modal

---

## 13/08/2026 — lashmatch — LashMatch Android web nao consegue cancelar assinatura Mercado Pago

**Erro:** LashMatch Android web nao consegue cancelar assinatura Mercado Pago

**Contexto:** N/A

**Causa:** cancelamento.tsx e assinatura.tsx bloqueavam com canUseInAppSubscriptionCheckout() — false no Chrome Android (sem PWA). Usuário via só aviso use o app. Conta gustavojordaob123 já CANCELADO no MP; trial até 19/08 mantém acesso.

**Solução:** Permitir cancelamento MP em qualquer plataforma web. Tela cancelamento mostra status se já CANCELADO. Pagamentos web: inline notice + botão cancelar/ver cancelamento.

**Arquivos:** N/A

**Tags:** assinatura,cancelamento,web,android,mercadopago

---

## 13/08/2026 — lashmatch — LashMatch iOS desloga ao fechar/reabrir o app

**Erro:** LashMatch iOS desloga ao fechar/reabrir o app

**Contexto:** N/A

**Causa:** app/index.tsx iniciava webAuthTimedOut=true no nativo (Platform.OS !== 'web'). Enquanto loading e user ainda null (AsyncStorage restaurando), Redirect/replace para /Login — parecia deslogar ao reabrir o app.

**Solução:** webAuthTimedOut começa false; timeout e force Login só em Platform.OS === 'web'. Nativo espera onAuthStateChanged (authReady).

**Arquivos:** N/A

**Tags:** ios,auth,persistence,boot,index

---

## 14/08/2026 — health-quadra-tech — Type error: Parameter 'cookiesToSet' implicitly has an 'any' type. (utils/supaba

**Erro:** Type error: Parameter 'cookiesToSet' implicitly has an 'any' type. (utils/supabase/server.ts setAll)

**Contexto:** primeiro deploy Next.js em produção (rootDirectory apps/web)

**Causa:** strict: true no tsconfig; createServerClient do @supabase/ssr não infere o tipo de cookiesToSet no next build da Vercel. Localmente o next/plugin mascara o erro.

**Solução:** Tipar cookiesToSet explicitamente e passar options com cast Parameters<typeof cookieStore.set>[2]

**Arquivos:** apps/web/utils/supabase/server.ts

**Tags:** typescript,supabase,ssr,vercel,nextjs

---

## 14/08/2026 — health-quadra-tech — Login Supabase volta para /login; GET /profiles HTTP 500

**Erro:** Login Supabase volta para /login; GET /profiles HTTP 500

**Contexto:** Usuário gustavo_j_14@hotmail.com autenticava na Vercel e a tela de login reaparecia.

**Causa:** Policy profiles_select_self_or_clinic chama current_clinic_id()/current_role(), que faziam SELECT em profiles com SECURITY INVOKER → recursão RLS. PostgREST devolvia HTTP 500. Login 200 + bootstrap 200, mas getProfile falhava e requireProfile/login page mandavam de volta ao /login.

**Solução:** Recriar current_clinic_id, current_role e current_professional_id como SECURITY DEFINER SET row_security = off; revoke anon/public; grant authenticated. Perfil do Hotmail já existia.

**Arquivos:** supabase/migrations/20260814150000_fix_profile_rls_recursion.sql; fabrica/health-quadra-tech-schemas.md

**Tags:** supabase,rls,recursion,login,trajeto

---

## 14/08/2026 — health-quadra-tech — Sessões SOAP invisíveis no celular após registrar; login espremido na metade do 

**Erro:** Sessões SOAP invisíveis no celular após registrar; login espremido na metade do card

**Contexto:** Usuário no celular (Chrome) depois de registrar sessão não achava as notas em lugar nenhum. Screenshot era a tela de login.

**Causa:** Notas SOAP só existiam numa tabela larga dentro da ficha do paciente; após salvar não havia redirect. Agenda lista appointments, não sessions. Login mobile escondia .login-visual mas mantinha grid 1fr 1fr, formulário pela metade.

**Solução:** Menu Sessões em /psico/sessoes; redirect após salvar; cards no histórico; notas no painel; login grid 1fr no mobile

**Arquivos:** apps/web/app/(workspace)/psico/sessoes/page.tsx, AppShell.tsx, ClinicalForms.tsx, ManageRecords.tsx, LoginForm.tsx, globals.css

**Tags:** trajeto,sessoes,mobile,login,soap

---

## 14/08/2026 — cortejo — Filtro de clientes não retorna resultados; Editar cadastro na ficha volta para a

**Erro:** Filtro de clientes não retorna resultados; Editar cadastro na ficha volta para a lista sem abrir edição

**Contexto:** app/config/clientes.tsx busca local; app/clientes/[id].tsx botão Editar cadastro

**Causa:** Busca case-sensitive a acentos (José≠jose) e comparação de telefone com string vazia inconsistente; botão Editar fazia router.push('/config/clientes') sem editId

**Solução:** filterClientsByQuery com normalizeForSearch (NFD) + match nome/sobrenome/telefone (digits>=2); Editar cadastro navega com params.editId e abre FormModalSheet automaticamente

**Arquivos:** utils/client.ts, app/config/clientes.tsx, app/clientes/[id].tsx

**Tags:** clientes,filtro,navegacao,ota

---

## 15/08/2026 — health-quadra-tech — Expo Go tela azul Something went wrong

**Erro:** Expo Go tela azul Something went wrong

**Contexto:** Usuário tentou abrir o app no Expo Go depois do eas update --branch preview.

**Causa:** Dois caminhos: (1) QR do EAS Update/dashboard não abre no Expo Go; (2) apps/mobile sem .env — createClient('', '') lança supabaseUrl is required e o Expo Go mostra Something went wrong.

**Solução:** Criar apps/mobile/.env com EXPO_PUBLIC_SUPABASE_*. Abrir só o QR do npx expo start em apps/mobile. Não usar o QR do expo.dev. Guard em createClient para não crashar sem env.

**Arquivos:** apps/mobile/.env (local), apps/mobile/utils/supabase.ts, apps/mobile/metro.config.js, apps/mobile/babel.config.js

**Tags:** expo-go, eas-update, supabase, env

---

## 15/08/2026 — health-quadra-tech — Project is incompatible with this version of Expo Go — This project requires a n

**Erro:** Project is incompatible with this version of Expo Go — This project requires a newer version of Expo Go

**Contexto:** Usuário abriu Trajeto no Expo Go do Android e viu Project is incompatible / requires a newer version.

**Causa:** O app está no Expo SDK 57. O Expo Go da Play Store ainda é um SDK mais antigo (geralmente 54). Cada build do Expo Go só roda um SDK.

**Solução:** No Android, instalar o Expo Go do SDK 57 em https://expo.dev/go (não esperar a Play Store). Depois npx expo start em apps/mobile. Na App Store o Expo Go para em SDK 54 — iPhone precisa de sign.expo.dev ou baixar o projeto para 54.

**Arquivos:** — (orientação; sem mudança de SDK)

**Tags:** expo-go, sdk-57, android

---

## 15/08/2026 — health-quadra-tech — Salvar nota SOAP no mobile apagava os campos e dizia que o subjetivo estava vazi

**Erro:** Salvar nota SOAP no mobile apagava os campos e dizia que o subjetivo estava vazio

**Contexto:** Aba Sessão do psicólogo. Usuário preenchia subjetivo e tocava Salvar nota.

**Causa:** Após o insert o form zerava os campos e deixava attempted=true, então a validação mostrava Preencha o subjetivo. KeyboardAvoidingView height no Android e useFocusEffect resetando paciente pioravam o estado.

**Solução:** Ler o texto via ref no save; não limpar o form; resetar attempted; ir para a lista de Sessões; KeyboardAvoidingView só no iOS; não resetar paciente selecionado no focus.

**Arquivos:** apps/mobile/app/(psico)/sessao.tsx

**Tags:** trajeto, expo, soap, sessao, mobile

---

## 15/08/2026 — health-quadra-tech — Expo Go tela azul / Something went wrong / Project is incompatible no Android e 

**Erro:** Expo Go tela azul / Something went wrong / Project is incompatible no Android e iPhone

**Contexto:** Trajeto estava em Expo SDK 57. Cortejo/LashMatch no 54. QR do dashboard EAS Update também não abre no Go.

**Causa:** Expo Go da App Store e Play Store ficou no SDK 54. SDK 55+ não foi aprovado nas lojas. EAS Update exige build nativo com o mesmo runtime, não o Expo Go.

**Solução:** Downgrade de apps/mobile para SDK 54 com expo-router ~6 (não ~54). Overrides no monorepo para não puxar expo 57 via @expo/vector-icons. Abrir só o QR do Metro (npx expo start).

**Arquivos:** apps/mobile/package.json, package.json (overrides), apps/mobile/metro.config.js, apps/mobile/components/HatSwitch.tsx, useColorScheme.ts, BackBar.tsx

**Tags:** expo, expo-go, sdk-54, trajeto

---

## 15/08/2026 — health-quadra-tech — Asset not found: apps/mobile/assets/icon.png

**Erro:** Asset not found: apps/mobile/assets/icon.png

**Contexto:** Depois do downgrade para SDK 54, Metro/Expo Go pedia assets/icon.png (template 54). O projeto só tinha assets/images/icon.png (template 57).

**Causa:** Expo Go 54 solicita o ícone no caminho clássico ./assets/icon.png, independente do app.json apontar para ./assets/images/icon.png.

**Solução:** Copiar icon.png e splash-icon.png para apps/mobile/assets/ e apontar app.json icon para ./assets/icon.png. Recarregar o Metro (r).

**Arquivos:** apps/mobile/assets/icon.png, apps/mobile/assets/splash-icon.png, apps/mobile/app.json

**Tags:** expo, expo-go, sdk-54, metro, assets

---

## 15/08/2026 — health-quadra-tech — Login demo Invalid login credentials / credencial inválida

**Erro:** Login demo Invalid login credentials / credencial inválida

**Contexto:** Usuários @trajeto.dev existiam e estavam confirmados, mas a senha gravada no Auth não era Trajeto123.

**Causa:** Contas criadas no Auth com senha diferente da documentada para a demo.

**Solução:** Reset de encrypted_password só nas 4 contas @trajeto.dev para Trajeto123. Contas pessoais Jordao não foram alteradas.

**Arquivos:** auth.users (somente emails @trajeto.dev)

**Tags:** supabase, auth, demo, trajeto

---

## 15/08/2026 — health-quadra-tech — Agenda mês: data, Hoje/Dia/Mês/Novo por cima do calendário

**Erro:** Agenda mês: data, Hoje/Dia/Mês/Novo por cima do calendário

**Contexto:** Tela (psico)/agenda no Expo Go. Calendário de agosto 2026 com botões sobrepostos às semanas 17–31.

**Causa:** AgendaCalendar usava style.height 218. O Calendar do Wix não encolhe as células — a grade transborda e a dayBar fica no meio.

**Solução:** Remover altura fixa. Tema compacto (fontes + margem de semana) como Cortejo. Barra do dia abaixo do mês, com fundo e zIndex.

**Arquivos:** apps/mobile/components/agenda/AgendaCalendar.tsx, AgendaFrame.tsx, lib/calendarLocale.ts

**Tags:** expo, agenda, react-native-calendars, layout

---

## 15/08/2026 — fabrica — indexar_rapido crash HNSW / 0xC0000005 (recorrência)

**Erro:** indexar_rapido.py crasha ao abrir Chroma (HNSW / 0xC0000005) e o RAG remoto fica desatualizado

**Contexto:** Windows + Chroma persistente `.chroma_db`. MCP tentava reindexar após cada decisão. Recorrência do incidente 08/08/2026.

**Causa:** Índice HNSW inconsistente no disco. Dois `INDEX.md` (fábrica e sinaflor) se sobrescreviam porque o delete usava só o nome do arquivo.

**Solução:** `python indexar_rapido.py --recriar-banco` (2387 chunks). Delete passou a usar `path`. `.\aws-rag\scripts\sync-push.ps1 -SkipIndex -Bucket fabrica-rag-084029330207-us-east-1 -Region us-east-1`. App Runner `/health` com `ready: true` e `chunks: 2387`.

**Arquivos:** `indexar_rapido.py`, `fabrica/INDEX.md`, `fabrica/rag-retrieval-fabrica.md`, `fabrica/aws-rag-app-runner.md`

**Tags:** rag, chroma, aws, hnsw

---

## 15/08/2026 — fabrica — indexar_rapido.py crasha ao abrir Chroma (HNSW / 0xC0000005) e o RAG remoto fica

**Erro:** indexar_rapido.py crasha ao abrir Chroma (HNSW / 0xC0000005) e o RAG remoto fica desatualizado

**Contexto:** Windows + Chroma persistente .chroma_db; MCP tentava reindexar após cada decisão

**Causa:** Índice HNSW do Chroma corrompido no disco; dois arquivos INDEX.md se sobrescreviam porque o delete usava só o nome do arquivo

**Solução:** python indexar_rapido.py --recriar-banco; delete por path; sync-push.ps1 -SkipIndex -Bucket fabrica-rag-084029330207-us-east-1 -Region us-east-1

**Arquivos:** C:/Users/gusta/obsidian/indexar_rapido.py, fabrica/INDEX.md, fabrica/rag-retrieval-fabrica.md, fabrica/aws-rag-app-runner.md

**Tags:** rag, chroma, aws, hnsw

---

## 19/08/2026 — lashmatch — Web/PWA: ao clicar 'Escolher outro tipo de WhatsApp' ou 'Mudar tipo de lembrete 

**Erro:** Web/PWA: ao clicar 'Escolher outro tipo de WhatsApp' ou 'Mudar tipo de lembrete (WhatsApp)' em Pagamentos/Assinatura volta ao início e não carrega outros planos.

**Contexto:** N/A

**Causa:** 

**Solução:** Em app/assinatura.tsx, para Platform.OS === 'web', ao clicar o botão de trocar tipo, navegar direto para /assinatura com params {estilo: ...} (alternando proprio/lashmatch) em vez de ir para /plano-escolha. Mantém comportamento antigo em nativo.

**Arquivos:** app/assinatura.tsx,components/PlanoAccessRedirect.tsx

**Tags:** 

---

## 19/08/2026 — lashmatch — Expo Go/nativo: trial ativo, ao clicar 'Meu plano' fica tudo branco (parece reca

**Erro:** Expo Go/nativo: trial ativo, ao clicar 'Meu plano' fica tudo branco (parece recarregar/remount)

**Contexto:** N/A

**Causa:** 

**Solução:** Atualizado hooks/usePlano.ts para normalizar trialFimEm vindo do Firestore como Timestamp/Date (toDate()) ou string para ISO string antes de calcular emPeriodoTrial/temAcessoEfetivo.

**Arquivos:** hooks/usePlano.ts

**Tags:** 

---

## 19/08/2026 — lashmatch — Expo Go (nativo): ao clicar 'Meu plano' a tela fica branca/volta pro splash ao i

**Erro:** Expo Go (nativo): ao clicar 'Meu plano' a tela fica branca/volta pro splash ao invés de carregar /planos

**Contexto:** N/A

**Causa:** 

**Solução:** Atualizado utils/openAppRoute.ts: quando pathname === '/planos' injeta params {stay:'1'} se não houver stay explícito, garantindo visualização explícita no app/planos.tsx.

**Arquivos:** utils/openAppRoute.ts,app/planos.tsx,app/(tabs)/_layout.tsx,constants/moreMenuItems.ts

**Tags:** 

---

## 19/08/2026 — lashmatch — Expo Go preview fica branco ao abrir Meu plano; caminho de navegação do botão de

**Erro:** Expo Go preview fica branco ao abrir Meu plano; caminho de navegação do botão de trial usa router.push('/planos') sem stay=1

**Contexto:** N/A

**Causa:** 

**Solução:** Atualizado app/(tabs)/index.tsx para navegar a /planos com params {stay:'1'} no botão de trial.

**Arquivos:** app/(tabs)/index.tsx,utils/openAppRoute.ts

**Tags:** 

---

## 19/08/2026 — health-quadra-tech — Next.js prerender /404 e /_not-found: TypeError Cannot read properties of null (

**Erro:** Next.js prerender /404 e /_not-found: TypeError Cannot read properties of null (reading useContext) em pages/_error ou chunks do not-found

**Contexto:** Deploy Vercel --prod do Trajeto falhou no prerender após o painel financeiro. Build local compilava e typecheck passava.

**Causa:** Monorepo com Expo (react 19.1.0) + Next 15.5 que puxava react 19.2.8 em apps/web/node_modules. Duas cópias do React no mesmo app: dispatcher null. Alias webpack de react para a cópia client piorava: quebrava RSC (next/link useContext no /_not-found).

**Solução:** 1) Pin react/react-dom 19.1.0 em apps/web/package.json. 2) Remover entradas apps/web/node_modules/react@19.2.8 do package-lock.json. 3) .npmrc legacy-peer-deps=true. 4) NÃO aliasar react no webpack. 5) Manter overrides do root.

**Arquivos:** apps/web/package.json, package-lock.json, .npmrc, apps/web/next.config.ts

**Tags:** next,react,vercel,prerender,monorepo

---

## 19/08/2026 — health-quadra-tech — Gráfico anual empilhava todos os recebimentos pagos no mês atual em vez de segui

**Erro:** Gráfico anual empilhava todos os recebimentos pagos no mês atual em vez de seguir o vencimento do extrato

**Contexto:** Ano 2026: extrato Fev R$100 + Ago R$300 + Ago R$200; gráfico mostrava só Ago R$600.

**Causa:** Horizonte Passado agrupava por paid_at. Marcar Pago grava a data/hora de agora, então vencimentos de fevereiro iam para a barra de agosto.

**Solução:** invoiceDay no passado usa due_date primeiro (depois paid_at/created_at). Texto do gráfico explica que a barra segue o vencimento.

**Arquivos:** packages/shared/finance.ts, apps/web/components/finance/FinanceDashboard.tsx, apps/mobile/components/FinanceDashboard.tsx

**Tags:** financeiro,grafico,due_date,paid_at

---

## 19/08/2026 — health-quadra-tech — Filtros do painel financeiro não refletiam no extrato; mês parecia ano; saída nã

**Erro:** Filtros do painel financeiro não refletiam no extrato; mês parecia ano; saída não aparecia no gráfico

**Contexto:** Mês agosto 2026: KPI R$500 (certo) mas eixo Jan–Dez e extrato com jan/fev/set. Futuro agosto zerado porque o a receber é setembro.

**Causa:** buildSeries de mes usava os 12 meses do ano; InvoiceManager recebia a lista inteira; polyline do chart usava entradas de novo.

**Solução:** filterInvoices no mesmo range/horizon. Série de mês = dias. Ano = 12 meses. Barras sage+ouro. Extrato via statement callback.

**Arquivos:** packages/shared/finance.ts, FinanceDashboard web/mobile, CashflowChart, páginas financeiro

**Tags:** financeiro,filtros,grafico,extrato

---

## 19/08/2026 — health-quadra-tech — Functions cannot be passed directly to Client Components (statement / detailHref

**Erro:** Functions cannot be passed directly to Client Components (statement / detailHref) — digest 983912048 em /clinica/financeiro

**Contexto:** Digest 983912048 em /clinica/financeiro e 621634256 em /clinica/pacientes após deploy --prod. /psico/financeiro e /psico/pacientes com o mesmo padrão.

**Causa:** Páginas Server Component passavam função (statement, detailHref) para Client Components. Next não serializa função e quebra o RSC.

**Solução:** FinanceWorkspace client monta o render prop internamente. PatientManager recebe detailBase string em vez de detailHref.

**Arquivos:** apps/web/components/finance/FinanceWorkspace.tsx, clinica/psico financeiro pages, PatientManager detailBase

**Tags:** next,rsc,financeiro,pacientes,vercel

---

## 19/08/2026 — health-quadra-tech — trajeto-notify CORS + POST 500: Daily exp was in the past rather than in the fut

**Erro:** trajeto-notify CORS + POST 500: Daily exp was in the past rather than in the future

**Contexto:** Psicóloga clicou Entrar na consulta na agenda web (Ana Prado, 08:00 Online) às ~22h.

**Causa:** ensureDailyRoom usava exp = starts_at + 6h. Na sessão das 08:00, ao entrar à noite o exp já estava no passado. Daily recusou, a função lançou exceção não tratada, o gateway devolveu 500 sem CORS. No mobile não há CORS, mas o mesmo 500 impedia abrir a sala.

**Solução:** exp = max(início+6h, agora+4h); try/catch com CORS em todo 500; ação ensure_video_room só para vídeo; web e Expo Go usam o mesmo helper ao entrar.

**Arquivos:** supabase/functions/trajeto-notify/index.ts; apps/web/lib/notify.ts; apps/mobile/lib/notify.ts; AgendaBoard; JoinCallButton; psico/patient web+mobile

**Tags:** daily,cors,edge-function,agenda,expo

---

## 20/08/2026 — health-quadra-tech — Android Bundling failed: Cannot find module 'react-refresh/babel' (babel-preset-

**Erro:** Android Bundling failed: Cannot find module 'react-refresh/babel' (babel-preset-expo)

**Contexto:** expo start no Expo Go Android. Metro falhou ao bundlar expo-router/entry.js no monorepo apps/web (Next) + apps/mobile (Expo SDK 54).

**Causa:** babel-preset-expo faz require('react-refresh/babel') como peer. No workspace npm o pacote ficou aninhado em expo/react-native e não na raiz, então o Babel não resolvia.

**Solução:** Adicionar react-refresh ^0.14.2 como dependência de @trajeto/mobile e npm install na raiz. Confirmado require.resolve a partir de babel-preset-expo.

**Arquivos:** apps/mobile/package.json, package-lock.json

**Tags:** expo, expo-go, babel, metro, react-refresh, monorepo

---

## 20/08/2026 — health-quadra-tech — Unable to resolve ../../../packages/shared/messaging from apps/mobile/app/(patie

**Erro:** Unable to resolve ../../../packages/shared/messaging from apps/mobile/app/(patient)/index.tsx

**Contexto:** expo start Android Expo Go após o fix do react-refresh. Metro bundlou 1630 modules e parou no import relativo.

**Causa:** O caminho ../../../packages/shared a partir de app/(patient) resolve para apps/packages/shared, não para a raiz. Imports relativos quebram em rotas aninhadas do Expo Router.

**Solução:** Dependência @trajeto/shared no mobile; imports iguais à web (@trajeto/shared/messaging etc.); metro extraNodeModules + package exports; tsconfig paths.

**Arquivos:** apps/mobile/package.json, metro.config.js, tsconfig.json, app/(patient)/index.tsx, app/cadastro.tsx, app/(psico)/paciente/[id].tsx, components/PatientWhatsAppPanel.tsx, components/PatientsPanel.tsx, lib/dates.ts, agenda.ts, finance.ts, report.ts, quizRequest.ts

**Tags:** expo, metro, monorepo, shared

---

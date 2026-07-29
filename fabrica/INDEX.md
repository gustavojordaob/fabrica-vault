# 📚 Índice — Base de Conhecimento Fábrica

> Indexar com `indexar_rapido.py` · Data de revisão índice: **23/07/2026**

## Notas criadas

- [[setmatch-rankings-clubes-padrao]] — **clubes + rankings + solicitação + feed social** (Setmatch jul/2026) · `setmatch`, `ranking`, `firestore`
- [[setmatch-pagamentos-mercado-pago]] — **PIX/cartão 1x + setmatchId + regras aulas/ranking/torneio** (Setmatch jul/2026) · `setmatch`, `pagamentos`, `mercadopago`
- [[auth-patterns]] — 10 seção(ões) · `firebase`, `auth`, `seguranca`
- [[checklists-deploy]] — 11 seção(ões) · `checklist`, `deploy`, `qualidade`
- [[firebase-deploy-checklist-padrao]] — **checklist Firebase deploy (functions/rules/hosting)** · `firebase`, `deploy`, `fluxo`
- [[cloud-functions-patterns]] — 12 seção(ões) · `firebase`, `functions`, `backend`
- [[componentes-reutilizaveis]] — 13 seção(ões) · `componentes`, `reutilizacao`, `ui`
- [[context-api-estado]] — 6 seção(ões) · `estado`, `context`, `react`
- [[expo-router-navegacao]] — 31 seção(ões) · `expo`, `router`, `navegacao`
- [[firebase-setup-patterns]] — 29 seção(ões) · `firebase`, `firestore`, `setup`
- [[firestore-schemas]] — 10 seção(ões) · `firestore`, `schema`, `dados`
- [[mercadopago-integration]] — 5 seção(ões) · `pagamentos`, `mercadopago`, `assinatura`
- [[mercadopago-assinatura-ota-padroes]] — **assinatura MP tokenizada, cancel/sync, paywall, erros reais Cortejo** (jun/2026) · `mercadopago`, `preapproval`, `cortejo`
- [[modulo-ajuda-suporte-expo]] — **tela Ajuda + WhatsApp suporte + página pública App Store** (Cortejo/LashMatch) · `suporte`, `expo`
- [[cortejo-modulos-jun2026-padrao]] — **assinatura dual RC+MP, trial 14d, sync Firestore iOS, msgUsage, OTA, auth** (Cortejo jun/2026) · `cortejo`, `assinatura`, `revenuecat`
- [[mcps-cursor-padrao]] — **MCPs Cursor: fabrica-apps, mercadopago, revenuecat, appstore-connect, whatsapp, firebase** · `mcp`, `cursor`, `integracao`
- [[excluir-conta-app-expo-padrao]] — **exclusão permanente de conta LGPD/App Store** (Cortejo/LashMatch) · `lgpd`, `lashmatch`, `cortejo`
- [[outros]] — 76 seção(ões) · `geral`
- [[padroes-fabrica]] — 18 seção(ões) · `padroes`, `fabrica`, `lashmatch`
- [[zenpro-catalogo-variantes-capinha-padrao]] — **catálogo dinâmico modelo × variante (material/preço)** · `zenpro`, `capinha`, `personalizacao`, `firestore`
- [[zenpro-portal-revendedor-b2b]] — **portal único /revendedor + faixas de preço** · `zenpro`, `revendedor`, `b2b`
- [[zenpro-melhor-envio]] — **cotação frete Melhor Envio + peso no produto** · `zenpro`, `frete`, `melhor-envio`
- [[zenpro-estoque-multitenant]] — **estoque central × por loja (inclui loja oficial zenpro)** · `zenpro`, `estoque`, `admin`
- [[zenpro-personalizacao-rockb2b]] — **frames RockB2B como câmera (não só SVG/heurística note→Samsung)** · `zenpro`, `rockb2b`, `personalizacao`, `capinha`
- [[react-native-fundamentos]] — 14 seção(ões) · `react-native`, `fundamentos`, `ui`
- [[react-navigation-patterns]] — 5 seção(ões) · `navegacao`, `react-navigation`, `tabs`
- [[snippets-utilitarios]] — 6 seção(ões) · `snippets`, `utilitarios`, `codigo`
- [[storage-patterns]] — 1 seção(ões) · `firebase`, `storage`, `arquivos`
- [[whatsapp-business-api]] — integração WhatsApp Business API (Meta) single-tenant · `integracao`, `whatsapp`, `meta`, `cloud-functions`
- [[whatsapp-salao-expo-padrao]] — **WhatsApp salão multi-tenant + Embedded Signup Coexistence + feature flag platformConfig + incidentes 23/06** (Cortejo jun/2026) · `whatsapp`, `cortejo`, `expo`, `embedded-signup`
- [[lashmatch-schemas]] — schemas Firestore LashMatch (usuarios, agendamentos, telefoneSalao) · `lashmatch`, `firestore`
- [[lashmatch-modulos-assinatura-jun2026]] — **assinatura dual RC+MP, 2 planos, trial 5d, usuarios/{uid}** (LashMatch jun/2026) · `lashmatch`, `assinatura`, `revenuecat`, `mercadopago`
- [[lashmatch-mercadopago-assinatura]] — MP preapproval Android LashMatch · `lashmatch`, `mercadopago`
- [[lashmatch-revenuecat-assinatura]] — RevenueCat IAP iOS LashMatch · `lashmatch`, `revenuecat`, `ios`
- [[lashmatch-web-plataforma]] — **web Hosting: sem análise, sem checkout in-app, deploy dist/** (LashMatch jun/2026) · `lashmatch`, `expo-web`, `hosting`
- [[agenda-salao-expo-padrao]] — **aba Agenda, slots 30min, bloqueios, horário por profissional, busca cliente** (Cortejo jun/2026) · `agenda`, `cortejo`, `expo`
- [[cortejo-schemas]] — **schema Firestore Cortejo** (salons, members, blockedPeriods) · `cortejo`, `firestore`
- [[rag-protocolo-antes-de-codar]] — protocolo RAG + caso calendário sem consulta · `rag`, `agente`
- [[react-native-calendars]] — lib calendário (Calendar, Agenda, markedDates) · `calendario`, `expo`
- **SINAFLOR2** (`fabrica/sinaflor/`) — Angular 7 + Spring Boot legado IBAMA · ver [[sinaflor/INDEX]]
- [[arquitetura-fabrica-ia]] — **como a fábrica funciona (doc canônico)** · estado jul/2026: Cortejo+LashMatch · `fabrica`, `arquitetura`, `rag`
- [[guia-completo-usuario-fabrica]] — **guia para humano: começar, arquitetura, adicionar especialidade (AWS/Postgres)** · `fabrica`, `guia`, `onboarding`
- `projetos/cortejo-project.md` · `projetos/lashmatch-project.md` — refs técnicas dos apps (RAG)

## Como usar no RAG

1. **Indexar** (após editar notas):
   - **Rápido (só o que mudou):** `python C:/Users/gusta/obsidian/indexar_rapido.py --somente cortejo-modulos-jun2026-padrao.md erros-e-solucoes.md`
   - **Completo (demora — centenas de arquivos):** `python C:/Users/gusta/obsidian/indexar_rapido.py`
2. **Servidor** (deixar rodando na porta 7332): `python C:/Users/gusta/obsidian/indexar_obsidian_chroma.py --server`
3. Consultar via MCP **fabrica-apps** → `rag_buscar()`

> `indexar_obsidian_chroma.py` **não indexa** — só sobe o HTTP. Indexação é **somente** `indexar_rapido.py`.

## MCPs por integração (agente Cursor)

| Tema | MCP obrigatório quando necessário |
|------|-----------------------------------|
| Mercado Pago | **mercadopago** |
| RevenueCat / IAP iOS | **revenuecat** |
| App Store Connect (apps, IAP, review) | **appstore-connect** |
| Firebase (deploy, rules, functions) | **firebase** (plugin) |
| WhatsApp Meta | **whatsapp** |
| SINAFLOR / Angular 7 / Java legado | **fabrica-apps** | `fabrica/sinaflor/*.md` + `projetos/sinaflor-prd.md` |
| GitHub, PR, memória, RAG | **fabrica-apps** |

Guia completo: [[mcps-cursor-padrao]] — **sempre MCP do tema + `rag_buscar` antes de codar**.

## Tags disponíveis

- `#arquivos`
- `#assinatura`
- `#auth`
- `#backend`
- `#checklist`
- `#codigo`
- `#componentes`
- `#context`
- `#dados`
- `#deploy`
- `#estado`
- `#expo`
- `#fabrica`
- `#firebase`
- `#firestore`
- `#functions`
- `#fundamentos`
- `#geral`
- `#integracao`
- `#lashmatch`
- `#mercadopago`
- `#navegacao`
- `#padroes`
- `#pagamentos`
- `#qualidade`
- `#react`
- `#react-native`
- `#react-navigation`
- `#reutilizacao`
- `#router`
- `#schema`
- `#seguranca`
- `#setup`
- `#snippets`
- `#storage`
- `#tabs`
- `#ui`
- `#utilitarios`
- `#whatsapp`
- `#meta`
- `#zapi` (legado — ver [[whatsapp-business-api]])
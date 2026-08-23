---
tags:
  - projeto
  - setmatch
  - estado
atualizado_em: 2026-08-18
firebase: setmatch-app-fabrica
figma: SvZ8vsoadqyC0yz0uUQm6C
repo: gustavojordaob/setmatch-app
hosting: https://setmatch-app-fabrica.web.app
maturidade: 99
---

# Setmatch — estado do projeto

## App Store review (ago/2026)

- Recusa 1.0 (2): **5.1.1** purpose string; **3.1.1** aulas em vídeo pagas fora da IAP — corrigido no build **1.0 (5)**
- Recusa 1.0 (5): **4.8** login de terceiro (Google) sem Sign in with Apple
- Correção 4.8: **sem login social** — só email/senha
- Binário: **1.0.0 (8)** enviado à ASC em 18/08/2026
- Build: https://expo.dev/accounts/gabrieljorda0/projects/setmatch-app/builds/3bc7d0f6-7e22-4c70-97a4-620f45f07a98
- Submit: https://expo.dev/accounts/gabrieljorda0/projects/setmatch-app/submissions/2631b790-37b9-4e12-944f-a84c2173b663
- Gateway fábrica: [[compliance-lojas-apple-google-padrao]]
- Aulas online sempre gratuitas; Stripe só serviço presencial

## Pagamentos — recorrência + promo por meio (jul/2026)

- Ciclo **mensal + cartão** → Stripe Checkout `subscription` (renova e estende `vigenteAte` via `invoice.paid`)
- PIX mensal = cobrança única do mês (Stripe não assina com PIX no BR)
- Admin cadastra `descontoPixPercent` / `descontoCartaoPercent` em ranking, aulas e torneio
- Jogador vê “PIX −X%” / “Cartão −Y%” e escolhe o meio antes do checkout (`pagarComEscolhaDeMeio`)
- Nota: [[setmatch-pagamentos-stripe]]

## Suporte + notificações de mensagem (ago/2026)

- Tela in-app `/ajuda` — WhatsApp `5519989632897` (`constants/support.ts` + `openSupportWhatsApp`)
- Perfil / Painel: “Ajuda e suporte” → `/ajuda` (página Hosting `/suporte` ainda disponível)
- `conversas.naoLidas.{uid}` incrementa ao enviar; zera ao abrir `/chat/[id]`
- Badges: Notificações (aba Mensagens), BottomNav chat, sino Home/Perfil/Troféu, painel professor/admin

## Solicitar professor / telefone global (ago/2026)

- Rota `/(auth)/solicitar-acesso` (professor ou admin_clube) → coleção `solicitacoesAcesso`
- Entrada: login admin → botões Solicitar ser professor / Solicitar admin
- `PhoneInput` com DDI (código do país) + DDD — wizard, perfil, onboarding admin, editar clube
- WhatsApp: número com código do país (legado BR 10–11 dígitos ganha `55`)

## Pagamentos Stripe (ago/2026)

- Provedor principal: **Stripe Checkout** (cartão; PIX se ativo no Dashboard)
- Connect Express: admin em `/clube/financeiro` → Recebimentos Stripe
- Functions: `criarCheckoutStripe`, `confirmarCheckoutStripe`, `webhookStripeSetmatch`, `stripeConnectOnboarding`, `stripeConnectStatus` (southamerica-east1)
- Nota: [[setmatch-pagamentos-stripe]] (substitui fluxo MP no app; MP functions legado)

## Propagar foto/nome (ago/2026)

- Ao salvar perfil (`updatePerfil` / wizard): `services/propagarPerfil.ts` atualiza denormalizados
- Alvos: desafios, amizades, posts, comentarios, conversas (`fotos`/`nomes`), solicitacoes, classificacao, inscritos, confrontos
- UI mensagens/notificações usa `Avatar` com `fotos[outroUid]`
- Rules: autor pode update em comentarios; jogador pode update própria solicitacao (foto/nome)

## Deploy / OTA (ago/2026)

- **EAS Update** branch `preview` — OTA iOS/Android (runtime 1.0.0)
- **Hosting** PWA: https://setmatch-app-fabrica.web.app (+ `/privacy` `/terms` `/suporte` `/baixar`)
- Dashboard update: expo.dev → setmatch-app → updates (branch preview)
- `eas.json`: channels development/preview/production + env `EXCLUIR_CONTA` / Hosting

## i18n (ago/2026)

- `pt-BR` · `en-US` · `es` — `¿`/`¡` corretos no espanhol
- Gate de idioma **antes dos slides** + seletor no Perfil
- Hook `useT()` · dicionários `i18n/locales/*`
- Nota: [[setmatch-i18n-padrao]]

## Rankings — rules (ago/2026)

- Create: admin_clube **ou** professor
- Update ranking: dono ou membro
- `classificacao/*`: write autenticado
- Nota: [[setmatch-rankings-clubes-padrao]]

## Compliance lojas (App Store / Play / LGPD) — ago/2026

- Páginas: `/privacy` · `/terms` · `/suporte` (Hosting)
- Consentimento em login / cadastro / admin-login
- Perfil + Painel clube: Ajuda, Termos, Privacidade, Sair, **Excluir minha conta**
- CF `excluirConta` → `https://southamerica-east1-setmatch-app-fabrica.cloudfunctions.net/excluirConta`
- Idade mínima 13 · `ITSAppUsesNonExemptEncryption: false`
- Nota fábrica: [[setmatch-compliance-lojas-padrao]]

## Esporte + clube ativo

- `EsporteContext` + AsyncStorage `@setmatch/esporteAtivo`
- `ClubeContext` + AsyncStorage `@setmatch/clubeAtivoId` — lista clubes do esporte + “Todos”
- Home + Troféu: `EsporteSwitcher` + `ClubeSwitcher`
- Feed, rankings, torneios e partidas respeitam esporte; clube filtra quando selecionado
- Post grava `esporte` + `clubeId` opcional; resultados de partida viram post `tipo: resultado`

## Aulas (aluno + professor)

- **Aba `/(tabs)/aulas`** — respeita `esporteAtivo` + `EsporteSwitcher` + busca
  - ONLINE: cards de **professor/curso** → `/aula/curso/[donoUid]` (módulos → aulas) → `/aula/[id]` (YouTube)
  - PRESENCIAL: clubes/quadras do esporte + matrículas + interesse
- Admin/professor: `/clube/aulas-publicar` — upload Storage; aula **online sempre grátis** (sem preço, cadeado ou checkout)
- Player `/aula/[id]`: vídeo sempre liberado (nativo ou YouTube/Vimeo)
- Coleção: `aulasPublicadas` com `videoUrl`, `videoStoragePath`; `pago`/`valorOnline` legado (forçados a `false`/`0`)
- Role `professor` → mesmo painel `/clube/*`
- Cobrança Stripe: só aula **presencial** (mensalidade), ranking e torneio

## Feed social

- Composer Home: texto + foto (`posts/{uid}/…` Storage)
- Post: curtidas, comentários (`posts/{id}/comentarios`), compartilhar
- `/post/[id]` — comentários + share para amigo (chat) ou fora do app (precisa instalar)
- Share externo: link + loja — conteúdo só no app autenticado
- Avatar/nome no feed e comentários → `/jogador/[uid]` (stats + info + desafiar/mensagem)

## Perto de mim

- Rota `/(tabs)/proximos` — banner na Home + link “Perto de mim” no feed
- `expo-location` → grava `usuarios.lat/lng` + `localizacaoAtualizadaEm`
- Abas Pessoas | Quadras; raio 25 km; Haversine client-side
- Clubes demo com lat/lng seed (SP / Santos / Campinas)
- Coleção opcional `quadras/{id}`

## Mensagens (aluno)

- **Aba `/(tabs)/mensagens`** — lista de conversas (amigos + clubes) → `/chat/[id]`
- Notificações: aba MENSAGENS com badge de `naoLidas` + destaque visual
- BottomNav: badge no ícone de chat quando há não lidas
- BottomNav: home, partidas, rankings, aulas, chat, perfil
- `TAB_BAR_CLEARANCE` (`constants/tabBar.ts`) em todas as tabs — barra não cobre conteúdo

## Torneios (admin + chave viva)

- `/clube/torneio-novo` — config de chave + pagamento
- `/torneio/[id]` — inscrição + **chaveamento vivo** (`confrontos` subcoleção)
- Admin: **Sortear chave e iniciar** → single-elim + byes (padrão clube/UTR)
- Jogadores/dono: tocam confronto `pronto` → placar → vencedor avança; final define `campeaoUid`
- Services: `services/chaveamentoTorneio.ts`, `utils/chaveamento.ts`

## Perfil público + social competitivo

- `/jogador/[uid]` — stats, H2H, últimas partidas, badges, VS com % vitória
- `/buscar` — nome, cidade, nível, esporte, ID `SM-`
- Badges em `constants/badges.ts` (perfil + jogador)
- Probabilidade: `utils/probabilidade.ts` (logistic win rate + H2H + nível)

## Matrículas (admin)

- Rules: read/update de `matriculas` se aluno, `donoUid` **ou** dono do clube (`isDonoClube`)
- Queries: `useMatriculasDoClube` / `matricularAlunoPorId` filtram `donoUid == auth.uid`

## Convites / desafios

- `/desafio/novo` — **VS** com fotos, comparativo, H2H, formatos
- `/desafio/[id]` — aceitar/recusar + placar
- Home: banner “Convidar para jogar” + jogos no feed

## Auth / wizard

- `onAuthStateChanged` marca `loading` **antes** do await do perfil — evita flash da tela idade
- AuthGuard / wizard / primeiro-acesso esperam `perfil` carregado
- Roles: `jogador` | `admin_clube` | `professor` (+ `tipoAdmin` opcional)

## i18n (pt-BR / en-US / es)

- Hook: `useT()` de `hooks/useI18n` → `LocaleContext`
- Chaves: `i18n/locales/pt-BR.ts` (+ en-US, es)
- Migrado: `perfil`, `login`, `cadastro`, `admin-login`, `esqueci-senha`, `AuthSocialRow`, `clube/painel` (títulos/hello/logout/ações com key)
- Já i18n: BottomNav, LegalConsent, AccountComplianceLinks, LanguagePicker

## Perfil

- `/perfil/editar` — nome, telefone, endereço **e foto** (`uploadFotoPerfil`)

## Chat

- Rules: `get` em conversa inexistente permitido (`resource == null`)
- `setDoc(..., { merge: true })` + Alert de erro no composer

## Meu clube (jogador)

- `/meus-clubes` — lista clubes com vínculo
- `/meu-clube/[id]` — regras, aulas, rankings, pagamentos, chat
- `/pagamentos?clubeId=` — filtro opcional

## Estratégia de papéis

| Papel | Como nasce | App |
|-------|------------|-----|
| Jogador | Cadastro público | Tabs + wizard |
| Admin clube | Equipe Setmatch → `role: admin_clube` | Painel `/clube/*` |
| Professor | Equipe Setmatch → `role: professor` | Mesmo painel (aulas online sem clube físico obrigatório) |

## ID amigável

`usuarios.setmatchId` = `SM-XXXXXX` — Perfil, pagamentos, admin adiciona aluno.

| Conta teste | ID |
|-------------|-----|
| jogador.teste | `SM-JOG001` |
| amigo.teste | `SM-AMI002` |
| admin.clube | `SM-ADM003` |
| Rodrigo Patah (professor) | `SM-RPATAH` |

## Pagamentos (Mercado Pago)

- Functions: `criarPreferenciaSetmatch` + `webhookMercadoPagoSetmatch` (southamerica-east1)
- Coleções: `pagamentos`, `matriculas`
- Admin: regras aulas, alunos por ID, financeiro, msg inscritos torneio
- **Pendente:** `functions/.env` → `MP_ACCESS_TOKEN` e redeploy

Ver: `fabrica/setmatch-pagamentos-mercado-pago.md`

## Contas teste

| Papel | Email | Senha |
|-------|-------|-------|
| Jogador | `jogador.teste@setmatch.app` | `Setmatch@123` |
| Amigo | `amigo.teste@setmatch.app` | `Setmatch@123` |
| Admin | `admin.clube@setmatch.app` | `Setmatch@123` |
| Professor | `rodrigo.patah@setmatch.app` | `SetmatchRodrigo2026!` |

WhatsApp suporte (solicitar admin): **19989632897**

Professor seed: **Rodrigo Joaquim Patah Batista** — Orlando, FL — 4 aulas online (Módulo 1 Aulas 1–3, Módulo 2 Aula 1) em `aulasPublicadas`.

Clubes demo: Arena Tennis + Smash Padel Moema + Arena Beach Santos + Raquetinha Campinas (com lat/lng).

## Rotas chave

- Admin/professor: `clube/painel`, `aulas-publicar`, `aulas-modalidades`, `alunos`, `financeiro`, `torneio-novo`, `torneio-mensagens`, `ranking-novo`
- Jogador: `aulas`, `aula/[id]`, `proximos`, `pagamentos`, `torneio/[id]`, `ranking/[id]`, `perfil`

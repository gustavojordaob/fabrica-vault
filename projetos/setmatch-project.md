---
tags:
  - projeto
  - setmatch
  - estado
atualizado_em: 2026-07-26
firebase: setmatch-app-fabrica
figma: SvZ8vsoadqyC0yz0uUQm6C
repo: gustavojordaob/setmatch-app
maturidade: 95
---

# Setmatch — estado do projeto

## Esporte + clube ativo

- `EsporteContext` + AsyncStorage `@setmatch/esporteAtivo`
- `ClubeContext` + AsyncStorage `@setmatch/clubeAtivoId` — lista clubes do esporte + “Todos”
- Home + Troféu: `EsporteSwitcher` + `ClubeSwitcher`
- Feed, rankings, torneios e partidas respeitam esporte; clube filtra quando selecionado
- Post grava `esporte` + `clubeId` opcional; resultados de partida viram post `tipo: resultado`

## Aulas (aluno)

- **Aba `/(tabs)/aulas`** — hub do aluno: minhas aulas (matrículas) + descobrir clubes do esporte
- `/meu-clube/[id]/aulas` — aluno **não se matricula sozinho**: mensagem no app ou WhatsApp (com Setmatch ID); clube cadastra em `/clube/alunos`
- Admin: `/clube/aulas-modalidades` — formulário + lista em **um único scroll**

## Mensagens (aluno)

- **Aba `/(tabs)/mensagens`** — lista de conversas (amigos + clubes) → `/chat/[id]`
- Notificações: aba MENSAGENS mostra conversas recentes (ultimoTexto) com link pro chat
- BottomNav: 6 itens — home, trofeu, aulas, mensagens, estatisticas, perfil

## Convites / desafios

- `/desafio/novo` — **VS** com fotos, comparativo (win rate/nível), H2H, formatos (`constants/formatosPartida.ts`: Md3, Md3+STB10, Md5, 2 sets, pro set, TB10)
- `/desafio/[id]` — card VS + formato/local/quando + aceitar/recusar + placar
- Home: banner “Convidar para jogar” + jogos no feed
- Perfil jogador: botão “Convidar para jogar”

## Auth / wizard

- `onAuthStateChanged` marca `loading` **antes** do await do perfil — evita flash da tela idade
- AuthGuard / wizard / primeiro-acesso esperam `perfil` carregado

## Perfil

- `/perfil/editar` — nome, telefone, endereço **e foto** (`uploadFotoPerfil`)


## Chat

- Rules: `get` em conversa inexistente permitido (`resource == null`) — corrige permission-denied ao abrir chat novo
- `setDoc(..., { merge: true })` + Alert de erro no composer

## Meu clube (jogador)

- `/meus-clubes` — lista clubes com vínculo (ranking / aula / pagamento)
- `/meu-clube/[id]` — regras, aulas (entrada), rankings, pagamentos **daquele clube**, chat
- `/pagamentos?clubeId=` — filtro opcional

## Estratégia de papéis

| Papel | Como nasce | App |
|-------|------------|-----|
| Jogador | Cadastro público | Tabs + wizard (telefone + endereço) |
| Admin clube | Solicita à Setmatch → equipe cria Auth + `role: admin_clube` | Só **login** admin → painel `/clube/*` |

Cada clube tem **um admin**. Rankings/torneios/aulas com **regras de pagamento** cadastradas pelo dono. Jogadores pagam no app (Mercado Pago: PIX + cartão 1x).

## ID amigável

`usuarios.setmatchId` = `SM-XXXXXX` — Perfil, pagamentos, admin adiciona aluno.

| Conta teste | ID |
|-------------|-----|
| jogador.teste | `SM-JOG001` |
| amigo.teste | `SM-AMI002` |
| admin.clube | `SM-ADM003` |

## Pagamentos (Mercado Pago)

- Functions: `criarPreferenciaSetmatch` + `webhookMercadoPagoSetmatch` (southamerica-east1)
- Coleções: `pagamentos`, `matriculas`
- Admin: regras aulas, alunos por ID, financeiro (liberar), msg inscritos torneio
- Jogador: pagar em ranking/aulas/torneio + `/pagamentos`
- Recorrência MVP: ciclo mensal + renovação por novo checkout (não preapproval)
- **Pendente:** preencher `functions/.env` → `MP_ACCESS_TOKEN` e redeploy

Ver: `fabrica/setmatch-pagamentos-mercado-pago.md`

## Fluxos

1. **Ranking** — solicitar → chat + cobrança se `pagamento.ativo`
2. **Torneio** — inscrição → PIX/cartão 1x + regras/prazo do dono + msg em massa
3. **Aulas** — interesse → mensalidade se clube.aulas.ativo
4. **Social** — amigos, feed, WhatsApp
5. **Perfil** — editar; ID Setmatch visível

## Contas teste

| Papel | Email | Senha |
|-------|-------|-------|
| Jogador | `jogador.teste@setmatch.app` | `Setmatch@123` |
| Amigo | `amigo.teste@setmatch.app` | `Setmatch@123` |
| Admin | `admin.clube@setmatch.app` | `Setmatch@123` |

WhatsApp suporte (solicitar admin): **19989632897**

Clubes demo do admin: Arena Tennis + Smash Padel Moema + Arena Beach Santos + Raquetinha Campinas.

Admin: modalidades de aula (trio/beach/spozinho…) + aluno com desconto; Msg inscritos com chips corrigidos; chat com doc ID estável.

## Rotas chave

- Admin: `clube/painel`, `aulas-regras`, `alunos`, `financeiro`, `torneio-mensagens`, `ranking-novo`, `torneio-novo`
- Jogador: `pagamentos`, `torneio/[id]`, `ranking/[id]`, `perfil`

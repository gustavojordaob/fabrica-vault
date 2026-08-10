---
tags:
  - fabrica
  - setmatch
  - ranking
  - firestore
atualizado_em: 2026-08-08
---

# Setmatch — Rankings, clubes, roles e social (padrão)

> **Agente Cursor — use MCP antes de codar**
> `rag_buscar("setmatch admin clube torneios aulas celular")`
> `buscar_historico("setmatch admin solicitacao torneio")`

Repo: `setmatch-app` · Firebase: `setmatch-app-fabrica`

## Roles

| role | Quem cria | Onde |
|------|-----------|------|
| `jogador` | Signup público | App comum |
| `admin_clube` | **Só equipe Setmatch** (Console) após solicitação | Login admin → `/clube/*` |
| `professor` | Equipe Setmatch | Mesmo painel `/clube/*` (aulas + ranking/torneio) |

**Proibido:** signup admin no app. Rules: `create` só com `role == jogador`; `update` não pode mudar `role`.

## Firestore — rankings (ago/2026)

| Path | Permissão |
|------|-----------|
| `rankings` create | `admin_clube` **ou** `professor` + `donoUid == auth.uid` |
| `rankings` update | dono **ou** uid em `membros[]` |
| `rankings` delete | só dono |
| `rankings/{id}/classificacao/{uid}` | read/write se autenticado (placares / sync) |
| `solicitacoes` | create pelo jogador (`uid`); update só `donoUid` |

Deploy: `firebase deploy --only firestore:rules --project setmatch-app-fabrica`

## Fluxos sem falha

```
Admin (criado pela Setmatch)
  → cadastra clube / rankings / torneios

Jogador (esporte ativo = tênis etc. — persistido)
  → Home/Troféu: só feed, notícias, rankings e torneios daquele esporte
  → Post no feed carrega emoji do esporte
  → Meus clubes → hub por clube (aulas, rankings, pagamentos daquele clube)
  → Solicitar ranking → solicitacao + chat com dono
  → Inscrever torneio → inscritos/{uid} + chat
  → Quero aulas → matrícula + pagamento mensal (se clube.aulas.ativo) + chat
  → Amigos → feed jogos dos amigos
  → Toque jogador → stats + WhatsApp (telefone obrigatório)
  → Meus pagamentos → ID SM-… + checkout Mercado Pago
```

## Pagamentos

Ver `setmatch-pagamentos-mercado-pago.md` — Checkout Pro PIX/cartão 1x; admin libera no financeiro.

## Celular

Campo `telefone` no wizard, onboarding admin e editar perfil. `utils/whatsapp.ts`.

## Checklist

- [x] Sem admin-cadastro público
- [x] Torneios list/filter/inscription
- [x] Ranking request → chat
- [x] Interesse aulas
- [x] Feed jogos amigos
- [x] Perfil editável + público
- [x] Rules deploy
- [x] Pagamentos MP (functions + UI) — falta token real
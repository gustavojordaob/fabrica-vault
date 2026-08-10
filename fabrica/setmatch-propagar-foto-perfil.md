---
tags:
  - fabrica
  - setmatch
  - perfil
  - firestore
atualizado_em: 2026-08-09
---

# Setmatch — Propagar foto/nome do perfil

> **Agente Cursor — use MCP antes de codar**
> `rag_buscar("setmatch propagar foto perfil denormalizada")`
> `buscar_historico("foto perfil desafios conversas")`

Repo: `setmatch-app` · Firebase: `setmatch-app-fabrica`

## Problema

`fotoUrl` / nomes são **denormalizados** em desafios, amizades, posts, conversas, ranking, torneio. Atualizar só `usuarios/{uid}` deixa avatares antigos nas listas históricas.

## Solução

`services/propagarPerfil.ts` → `propagarPerfilPublico({ uid, fotoUrl, nome? })`

Chamado em:

- `AuthContext.updatePerfil` (quando muda foto ou nome)
- `AuthContext.saveWizardProfile` (foto do wizard)

## Checklist ao copiar para outro app

- [ ] Listar todos os campos denormalizados de foto/nome
- [ ] Batch update (máx ~400 ops) + `set` merge onde o doc pode não existir
- [ ] Collection group + `fieldOverrides` COLLECTION_GROUP se precisar
- [ ] Rules: autor/dono pode atualizar o próprio lado do doc
- [ ] Conversas: mapa `fotos.{uid}` (dot notation no update) + Avatar com `uri`
- [ ] Não substituir o mapa `fotos` inteiro no merge (apaga outras chaves)

## Arquivos

- `services/propagarPerfil.ts`
- `contexts/AuthContext.tsx`
- `services/mensagens.ts` · `hooks/useConversas.ts`
- `app/(tabs)/mensagens.tsx` · `notificacoes.tsx`
- `firestore.rules` · `firestore.indexes.json`

---
tags:
  - fabrica
  - setmatch
  - aulas
  - torneios
  - geolocalizacao
atualizado_em: 2026-08-07
---

# Setmatch — Aulas online/presencial, torneio dinâmico e perto de mim

> **Agente Cursor — use MCP antes de codar**
> `rag_buscar("setmatch aulas online professor aulasPublicadas")`
> `buscar_historico("setmatch torneio chaveamento perto de mim")`

Repo: `setmatch-app` · Firebase: `setmatch-app-fabrica` · Figma: `SvZ8vsoadqyC0yz0uUQm6C`

## Roles

| role | Painel | Observação |
|------|--------|------------|
| `admin_clube` | `/clube/*` | Clube físico |
| `professor` | mesmo `/clube/*` | Aulas online sem clube obrigatório |
| `jogador` | tabs | Consome aulas + perto de mim |

`AuthContext.isAdminClube` = `admin_clube` **ou** `professor`.

## Coleção `aulasPublicadas`

```
origemTipo: 'clube' | 'professor'
origemId, origemNome, donoUid
modo: 'online' | 'presencial'
esporte, titulo, descricao, bannerUrl?
// online: modulo, ordem, videoUrl, duracaoMin?
// presencial: cidade, local?, valorMensal?
ativo, criadoEm
```

- Admin: `app/clube/aulas-publicar.tsx`
- Player: `app/(tabs)/aulas.tsx` (toggle ONLINE/PRESENCIAL) + `app/aula/[id].tsx`

## Torneio admin dinâmico

- Constants: `constants/chaveamentosTorneio.ts` — formatos de chave, definição, mata, grupos, formatos de partida por esporte, `previewEstruturaTorneio`
- UI: `app/clube/torneio-novo.tsx`
- Persistido em `torneios`: `formatoChaves`, `definicaoChave`, `estruturaMata`, `gruposConfig`, `formatoPartidaId`, `estruturaPreview`, `bannerUrl`
- **Fora do MVP:** motor que gera confrontos rodada a rodada

## Matrículas (permission-denied)

Queries admin **sempre** com `where('donoUid','==', auth.uid)`.
Rules: read se aluno **ou** `donoUid` **ou** `isDonoClube(clubeId)`.

## Perto de mim

- `expo-location` + `services/localizacao.ts` + Haversine `utils/geo.ts`
- Rota `/(tabs)/proximos` — Pessoas | Quadras, raio 25 km
- Campos `lat`, `lng`, `localizacaoAtualizadaEm` em `usuarios` e `clubes`
- Plugin em `app.json` com texto de permissão

## BottomNav

- `constants/tabBar.ts` → `TAB_BAR_CLEARANCE` / `TAB_BAR_HEIGHT`
- ScrollViews das tabs usam o clearance; BottomNav `zIndex` alto + `pointerEvents="box-none"`

## Checklist próximo app

- [ ] Role professor/admin compartilhando painel
- [ ] Conteúdo publicado em coleção própria (`aulasPublicadas`)
- [ ] Torneio: chips de chave + preview textual antes do motor de árvore
- [ ] Matrículas: filtrar por `donoUid` nas queries
- [ ] Location: permissão → salvar coords → Haversine client-side
- [ ] Tab bar absoluta: clearance único

## Conta seed professor

Ver `projetos/setmatch-project.md` — Rodrigo Patah (`rodrigo.patah@setmatch.app`).

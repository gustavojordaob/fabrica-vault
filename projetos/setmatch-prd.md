---
tags:
  - projeto
  - prd
  - setmatch
  - mvp
stack: React Native + Expo + Firebase
status: em-desenvolvimento-ativo
criado_em: 2026-05-11
atualizado_em: 2026-07-25
figma: SvZ8vsoadqyC0yz0uUQm6C
---

# Setmatch — PRD v2.2 (Rankings + Feed)

## Status: Em desenvolvimento ativo

> App de tênis, padel, raquetinha e beachtênis para desafiar jogadores, registrar resultados, entrar em rankings de clubes e acompanhar o feed da comunidade.

**Nome:** Setmatch  
**Plataforma:** iOS + Android + Web (React Native + Expo SDK 54)  
**Backend:** Firebase (`setmatch-app-fabrica`)  
**Repo:** `gustavojordaob/setmatch-app`  
**Figma:** [fileKey `SvZ8vsoadqyC0yz0uUQm6C`](https://www.figma.com/design/SvZ8vsoadqyC0yz0uUQm6C) — 1 página, **27 frames**

---

## Tokens de design (Figma)

| Token | Valor | Uso |
|-------|-------|-----|
| primary / background | `#255943` | Fundo geral, header home |
| accent / CTA | `#C7D941` | Botões pill, tab ativa, títulos Rankings/Calendário |
| surface | `#1E3D2B` | Cards wizard |
| surfaceDark | `#1A1A1A` | Bottom nav, chips, cards notificação |
| bodyLight | `#F5F5F5` | Corpo da Home |
| textPrimary | `#FFFFFF` | Títulos em fundo escuro |
| textDark | `#255943` | Títulos em fundo claro |
| textMutedDark | `#888888` | Texto secundário em fundo claro |
| textOnAccent | `#1A1A1A` | Texto em botão lima |
| pillMuted | `#D9D9D9` | Capsule username no ranking |
| borderRadius botão | `60` | `Radius.pill`, height `56` |
| borderRadius bottom nav | `40` | `BottomNav` |

Implementação: `constants/colors.ts`, `constants/typography.ts`, `constants/radius.ts`.

### Componentes UI

- `Button` — primary / outline / ghost + `ButtonFooter`
- `Input` — label, olho senha
- `BottomNav` — 4 abas: Home, **Rankings**, Estatísticas, Perfil
- `Avatar` — sm/md/lg/xl + verified
- `RankingCard` — Global / Winner (FIXADO)
- `RecentMatchCard` — vitória + sets
- `ScrollPicker` / `RulerPicker` — wizard

---

## Inventário Figma (27 frames)

### Fluxo autenticado / onboarding (19)

| Frame | Nome Figma | Rota | Status |
|-------|------------|------|--------|
| 1:2 | Launch | `app/index.tsx` | ✅ |
| 1:3–1:7 | Onboarding 1–4 | `app/onboarding/index.tsx` | ✅ |
| 1:8 | Log in | `app/(auth)/login.tsx` | ✅ |
| 1:9 | Sign Up | `app/(auth)/cadastro.tsx` | ✅ |
| 1:10 | Forgot Password | `app/(auth)/esqueci-senha.tsx` | ✅ |
| 1:11 | First Log in | `app/primeiro-acesso.tsx` | ✅ |
| 1:12 | Age | `app/wizard/idade.tsx` | ✅ digitável + min 5 |
| 1:13 | Gender | `app/wizard/genero.tsx` | ✅ |
| 1:14 | Weight | `app/wizard/peso.tsx` | ✅ digitável |
| 1:15 | Height | `app/wizard/altura.tsx` | ✅ |
| 1:16 | Goal | `app/wizard/esportes.tsx` | ✅ |
| 1:17 | Activity Level | `app/wizard/nivel.tsx` | ✅ |
| 2:588 | Upload Foto | `app/wizard/foto.tsx` | ✅ upload imediato + preview + Avançar |
| 1:18 | Home | `app/(tabs)/home.tsx` | ✅ feed social + notícias + partidas reais |
| 1:19 | Profile | `app/(tabs)/perfil.tsx` | ✅ + logout no header |
| 1:20 | Notifications | `app/(tabs)/notificacoes.tsx` | ✅ |

### Rankings / calendário (8) — sync 25/07/2026

| Frame | Nome Figma | Rota | Status |
|-------|------------|------|--------|
| 65:2 | Rankings - Inicial | `app/(tabs)/trofeu.tsx` | ✅ Meus + próximos + solicitar + criar clube |
| 65:85 / 70:89 | Rankings - Selecionado | `app/ranking/[id].tsx` | ✅ classificação real |
| 65:214 | Rankings - Perfil Selecionado | (próximo) | 🔄 |
| 70:156 | Rankings - Solicitação | `trofeu` + `services/rankings` | ✅ solicitar / aceitar / recusar |
| 70:238 | Rankings - Calendário - Histórico | `estatisticas` | ✅ partidas reais |
| 70:352 | Rankings - Calendário - Próximas | `estatisticas` | ✅ empty state |
| 70:472 | Rankings - Calendário - Agendamento | (próximo) | 🔄 |

---

## Fluxo de navegação

```
Launch → Onboarding (4) → Login/Cadastro
  → Primeiro acesso (onboardingOk=false) → Wizard (7) → Home
Tabs: Home | Rankings (trofeu) | Estatísticas/Calendário | Perfil
Rankings: criar clube (`/ranking/novo`) · detalhe (`/ranking/[id]`)
Notificações: via sino (rota oculta)
```

### Lógica Winner / clubes

1. Dono de academia cria clube + ranking (`/ranking/novo`)
2. Jogadores veem **Rankings próximos**, buscam e **Solicitam**
3. Dono aceita → jogador entra em `membros[]` + `classificacao/{uid}`
4. **Meus rankings** (ex.: Winner) = rankings onde o usuário já é membro (FIXADO)
5. Partidas `tipo: ranking|amistoso` alimentam Home e Calendário

---

## Firebase

| Serviço | Detalhe |
|---------|---------|
| Projeto | `setmatch-app-fabrica` |
| Auth | Google (`expo-auth-session`) + e-mail/senha |
| Storage | `usuarios/{uid}/perfil_*.jpg` — upload nativo via REST + `Uint8Array` |
| Firestore | `usuarios`, `desafios`, `partidas`, `clubes`, `rankings` (+ `classificacao`), `solicitacoes`, `posts` |

---

## Pendências

1. Agendamento de próximas partidas (frame 70:472)
2. Perfil do adversário a partir do ranking (frame 65:214)
3. Role explícito `donoAcademia` (hoje qualquer auth pode criar clube)
4. `AppContainer` web maxWidth
5. Editar perfil end-to-end
6. Ícones de modalidade na Home (vetor Figma vs emoji)

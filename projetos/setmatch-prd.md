---
tags:
  - projeto
  - prd
  - setmatch
  - mvp
stack: React Native + Expo + Firebase
status: em-desenvolvimento-ativo
criado_em: 2026-05-11
atualizado_em: 2026-05-23
---

# Setmatch — PRD v2.0 (Figma implementado)

## Status: Em desenvolvimento ativo

> App de tênis, padel, raquetinha e beachtênis para desafiar jogadores, registrar resultados e acompanhar estatísticas.

**Nome:** Setmatch  
**Plataforma:** iOS + Android + Web (React Native + Expo SDK 54)  
**Backend:** Firebase (`setmatch-app-fabrica`)  
**Repo:** `gustavojordaob/setmatch-app`  
**Branch principal de feature:** `feature/figma-full-implementation`

---

## Tokens de design reais (Figma — pixel-perfect)

| Token | Valor | Uso |
|-------|-------|-----|
| primary / background | `#255943` | Fundo geral, header home |
| accent / CTA | `#C7D941` | Botões pill, tab ativa, destaques |
| surface | `#1E3D2B` | Cards wizard (nível) |
| surfaceDark | `#1A1A1A` | Bottom nav, chips, cards notificação |
| textPrimary | `#FFFFFF` | Títulos |
| textSecondary | `#FFFFFF99` | Subtítulos |
| textOnAccent | `#1A1A1A` | Texto em botão lima |
| input bg | `rgba(255,255,255,0.15)` | Campos login/cadastro |
| placeholder | `#FFFFFF60` | Inputs |
| borderRadius botão | `60` | `Radius.pill`, height `56` |
| borderRadius input | `30` | `Input` |
| borderRadius bottom nav | `40` | `BottomNav` |

Implementação: `constants/colors.ts`, `constants/typography.ts`, `constants/radius.ts`.

### Componentes UI

- `components/ui/Button.tsx` — primary / outline / ghost
- `components/ui/Input.tsx` — label, olho senha
- `components/ui/BottomNav.tsx` — 4 abas (Home, Troféu, Estatísticas, Perfil)
- `components/ui/Avatar.tsx` — sm/md/lg/xl + verified badge
- `components/wizard/ScrollPicker.tsx` — idade
- `components/wizard/RulerPicker.tsx` — peso/altura + UnitToggle
- `components/home/RecentMatchCard.tsx` — card partida home

---

## Assets

| Arquivo | Uso |
|---------|-----|
| `assets/Vector.png` | Ícone logo (bolinha) — splash + onboarding slides 1–3 |
| `assets/onboarding/Onboarding_1.png` | Slide 1 — raquete |
| `assets/onboarding/Onboarding_2.png` | Slide 2 — quadra |
| `assets/onboarding/Onboarding_3.png` | Slide 3 — jogador sacando |
| `assets/onboarding/onborading_4.png` | Slide 4 — fundo + overlay + CTA |
| `assets/Launch.png` | Splash fullscreen |
| `assets/onboarding/slide1.jpg` … `slide4.jpg` | Placeholders (cópia dos PNG) |

Onboarding: `app/onboarding/index.tsx` — `FlatList` horizontal com `pagingEnabled`, 4 slides.

---

## Telas implementadas (19)

| # | Tela | Rota | Status |
|---|------|------|--------|
| 1 | Launch (Splash) | `app/index.tsx` | ✅ `assets/Launch.png` fullscreen |
| 2–5 | Onboarding 1–4 | `app/onboarding/index.tsx` | ✅ Imagens Figma + swipe |
| 6 | Log In | `app/(auth)/login.tsx` | ✅ pixel-perfect (G/Apple/F, inputs) |
| 7 | Sign Up | `app/(auth)/cadastro.tsx` | ✅ 4 campos + Criar Conta |
| 8 | Forgot Password | `app/(auth)/esqueci-senha.tsx` | ✅ |
| 9 | First Log In | `app/primeiro-acesso.tsx` | ✅ Bem Vindo {nome} + Vamos Lá |
| 10 | Age | `app/wizard/idade.tsx` | ✅ |
| 11 | Gender | `app/wizard/genero.tsx` | ✅ Male / Female círculos |
| 12 | Weight | `app/wizard/peso.tsx` | ✅ |
| 13 | Height | `app/wizard/altura.tsx` | ✅ |
| 14 | Goal (esportes) | `app/wizard/esportes.tsx` | ✅ |
| 15 | Activity Level | `app/wizard/nivel.tsx` | ✅ |
| 16 | Upload Foto | `app/wizard/foto.tsx` | 🔄 UI ok; Storage depende do Console |
| 17 | Home | `app/(tabs)/home.tsx` | ✅ header verde + card vitória + feed |
| 18 | Profile | `app/(tabs)/perfil.tsx` | ✅ stats círculos + grid badges |
| 19 | Notifications | `app/(tabs)/notificacoes.tsx` | ✅ LEMBRETES/SISTEMA + mock |
| — | Troféu (tab) | `app/(tabs)/trofeu.tsx` | 🔄 placeholder |
| — | Estatísticas (tab) | `app/(tabs)/estatisticas.tsx` | 🔄 placeholder |

### Telas MVP legado (pós-wizard)

| Tela | Rota | Status |
|------|------|--------|
| Análise oponente | `app/jogador/[uid].tsx` | ✅ |
| Novo desafio | `app/desafio/novo.tsx` | ✅ |
| Detalhe desafio | `app/desafio/[id].tsx` | ✅ |
| Registrar resultado | `app/partida/registrar/[desafioId].tsx` | ✅ |
| Desafios (tab oculta) | `app/(tabs)/desafios.tsx` | ✅ |

---

## Fluxo de navegação

```
Launch (splash)
  → Onboarding (4 slides, swipe; CTA → Login)
  → Login / Cadastro / Esqueci senha
  → [auth] → Primeiro acesso (se onboardingOk = false)
  → Wizard (7 passos)
  → Home (tabs: Home, Troféu, Estatísticas, Perfil — BottomNav custom)
  → Notificações via sino no header (rota oculta na tab bar)
```

**AuthGuard:** usuário logado sai de onboarding/auth; sem wizard completo → `primeiro-acesso` → wizard.

---

## Wizard de perfil

| Passo | Tela | Comportamento |
|-------|------|----------------|
| 1 | idade | Scroll horizontal, número grande accent |
| 2 | genero | Male / Female (círculos ♂ ♀) |
| 3 | peso | Régua KG/LB |
| 4 | altura | Régua CM/INCH |
| 5 | esportes | 4 pills — múltipla escolha (Tênis, Padel, Raquetinha, Beachtênis) |
| 6 | nivel | 3 opções radio |
| 7 | foto | Upload câmera/galeria → Storage |

Ao concluir: `onboardingOk: true` no Firestore.

---

## Schema Firestore

### `usuarios/{uid}`

```
nome: string
email: string
fotoUrl: string | null
esportes: string[]
idade: number
genero: string
peso: number
altura: number
nivel: string
vitorias: number
derrotas: number
torneios: number
onboardingOk: boolean
criadoEm: timestamp
ultimoAcesso: timestamp
```

### Outras coleções

- `desafios/{id}` — desafios entre jogadores
- `partidas/{id}` — resultados registrados

---

## Firebase

| Serviço | Detalhe |
|---------|---------|
| Projeto | `setmatch-app-fabrica` |
| Auth | Google (`expo-auth-session`) + e-mail/senha |
| Storage | `usuarios/{uid}/perfil_*.jpg` — bucket `setmatch-app-fabrica.firebasestorage.app` |
| Firestore | `usuarios`, `desafios`, `partidas` |

---

## Regras da fábrica aplicadas

- `expo-auth-session` (não `@react-native-google-signin`)
- `initializeAuth` + `AsyncStorage` (`utils/firebaseConfig.ts`)
- Upload foto: `fetch` → `arrayBuffer` → `Blob` → `uploadBytes`
- Cores centralizadas em `constants/colors.ts` (sem hex em telas)
- Expo Router file-based (`app/`)

---

## Pendências conhecidas

1. Habilitar Firebase Storage no Console + `firebase deploy --only storage`
2. Validação pixel-perfect vs Figma (MCP Pro/Dev para rate limits)
3. `AppContainer` web com `maxWidth` (padrão fábrica RN Web)
4. Editar perfil — implementar fluxo real

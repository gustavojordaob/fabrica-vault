---
tags:
  - cortejo
  - expo
  - web
  - hosting
fonte: repo cortejo
atualizado_em: 2026-06-09
projeto: Cortejo
firebase_project: cortejo-app
links:
  - "[[cortejo-schemas]]"
  - "[[mercadopago-assinatura-ota-padroes]]"
---

# Cortejo — App web desktop (Expo + Firebase Hosting)

## Objetivo

Mesmo app React Native no browser (`https://cortejo-app.web.app`), com login Firebase e todas as telas do dono do salão. Em viewport ≥ 1024px: sidebar fixa + área principal (sem bottom tabs).

## Stack

| Peça | Detalhe |
|------|---------|
| Export | `npm run export:web` → `dist/` |
| Hosting | `firebase.json` → `public: dist`, rewrite SPA `**` → `/index.html` |
| Auth | Email/senha + Google (mesmo `firebaseConfig`) |
| Pagamento web | `config/cartao` → redirect same-tab para `tokenizar.html` → volta com `?token=` |

## Arquivos principais

| Arquivo | Função |
|---------|--------|
| `constants/webLayout.ts` | Breakpoint 1024, largura sidebar 248px |
| `hooks/useWebLayout.ts` | `isWeb`, `isDesktopWeb`, `width` |
| `utils/webNavigation.ts` | `shouldShowWebSidebar`, `isWebNavActive` |
| `components/layout/WebDesktopFrame.tsx` | Sidebar + conteúdo |
| `components/layout/WebDesktopSidebar.tsx` | Nav principal + configurações |
| `components/layout/WebAuthLayout.tsx` | Login centralizado (max 440px) |
| `app/+html.tsx` | Meta/título/cor de fundo web |
| `app/_layout.tsx` | Envolve `Stack` com `WebDesktopFrame` |
| `app/(tabs)/_layout.tsx` | `tabBarStyle: { display: 'none' }` em desktop |

## Rotas públicas (sem sidebar)

- `/agendar?salon=` — booking HTML/React público
- `/assinar`, `/assinatura/tokenizar` — checkout iOS / token MP
- `/(auth)/*` — login e onboarding

## Deploy (obrigatório após mudanças web)

```powershell
Set-Location c:\Users\gusta\projetos\cortejo
npm run export:web
npx firebase-tools deploy --only hosting --project cortejo-app
```

> OTA/EAS **não** atualiza o site — só export + hosting deploy.

## Checklist agente

- [ ] Sidebar só em rotas autenticadas (`shouldShowWebSidebar`)
- [ ] Tab bar oculta em `isDesktopWeb`
- [ ] Logout chama `useSalonStore.clear()` (index + `authSession`)
- [ ] Cartão na web: `window.location.href` para tokenizar, não `openAuthSessionAsync`
- [ ] `EXPO_PUBLIC_AGENDAR_PUBLIC_BASE_URL` alinhado ao domínio hosting
- [ ] Fonte **Ionicons** em `dist/assets/fonts/Ionicons.ttf` + `@font-face` em `app/+html.tsx` + `useIconFonts` no `_layout`

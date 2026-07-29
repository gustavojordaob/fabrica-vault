---
tags:
  - lashmatch
  - expo-web
  - hosting
  - analise
fonte: LashMatch (jun/2026)
projeto: LashMatch
atualizado_em: 2026-07-22
links:
  - "[[react-native-web-patterns]]"
  - "[[lashmatch-modulos-assinatura-jun2026]]"
  - "[[agenda-salao-expo-padrao]]"
---

> **Agente Cursor — consultar ANTES de alterar comportamento web LashMatch**
>
> 1. `rag_buscar("lashmatch web análise mobile only")`
> 2. Ler `utils/analysisPlatform.ts` e `utils/subscriptionPlatform.ts`
> 3. Deploy: `npm run export:web` → `firebase deploy --only hosting`

# LashMatch — Web (Expo + Firebase Hosting)

URL produção: **https://lashmatch-627fd.web.app**

## O que funciona na web

- Login / cadastro
- Clientes (lista + perfil + **histórico de análises em leitura**)
- Agenda, funcionárias, serviços, link público `/agendar`
- Estoque, financeiro, guias (mapeamentos, curvatura)
- Perfil, ajuda, termos

## O que NÃO funciona na web (somente app iOS/Android)

| Módulo | Helper | Comportamento web |
|--------|--------|-------------------|
| **Análises** (IA + manual + câmera + assistente) | `canUseClientAnalysis()` | Rotas bloqueadas; **sem** card "Iniciar Nova Análise" na Home |
| **Assinatura / pagamento in-app** | `canUseInAppSubscriptionCheckout()` | Redirect para `/planos` com aviso mobile-only |

Mesmo padrão arquitetural: flag em `utils/*Platform.ts` + rotas `.web.tsx` ou guard na UI.

## Análises — implementação (jun/2026)

```typescript
// utils/analysisPlatform.ts
export function canUseClientAnalysis(): boolean {
  return Platform.OS === 'ios' || Platform.OS === 'android';
}
```

### UI

- `app/(tabs)/index.tsx` — card "Iniciar Nova Análise" **só** se `canUseClientAnalysis()`; na web **não renderiza nada** (nem aviso com o mesmo título)
- `components/WebDesktopPanel.tsx` — **sem** atalho "Nova análise" nas ações rápidas

### Rotas bloqueadas (`.web.tsx`)

| Arquivo | Efeito |
|---------|--------|
| `app/camera.web.tsx` | Tela de aviso + Voltar |
| `app/assistente/_layout.web.tsx` | Bloqueia todos os passos do assistente |
| `app/analysisResult.web.tsx` | Bloqueia resultado (IA e manual) |

Componente de aviso (URL direta): `components/analysis/IaAnalysisMobileOnlyNotice.tsx` → export `AnalysisMobileOnlyNotice`.

### Nativo (inalterado)

- `app/camera.tsx`, `app/analysisResult.tsx`, `app/assistente/*` — fluxo completo no app.

## PWA (celular só instalado — desktop livre)

Aditivo no Hosting. **Não** altera App Store / Play nem o runtime nativo.

| Peça | Onde |
|------|------|
| Manifest | `public/manifest.webmanifest` → copiado para `dist-web` |
| Service worker | `public/sw.js` — **sem cache** (só instala; rede normal) |
| Ícones | `scripts/copy-pwa-assets.mjs` gera `/icons/pwa-192.png`, `pwa-512.png`, `apple-touch-icon.png` |
| HTML | `app/+html.tsx` — link manifest + meta Apple + `register('/sw.js')` só em HTTPS |
| Headers | `firebase.json` — `Cache-Control: no-cache` em `/sw.js` e `/manifest.webmanifest` |
| Gate | `PwaMobileRequireInstall` + `utils/pwaWeb.ts` |

**Regra:** no **celular**, o app web **só** em modo instalado (standalone). Navegador mobile → tela “Instale o LashMatch” com botão **sempre visível** (captura cedo de `beforeinstallprompt` no `+html.tsx`; se o Chrome não disparar, passos ⋮ → Instalar app).

- **Desktop** web: liberado sem instalar (análises/câmera ainda só no PWA ou nativo)
- **PWA instalado:** `canUseClientAnalysis()` e checkout MP (Android) liberados — paridade com nativo o quanto a web permite (sem RevenueCat/IAP iOS; câmera via browser)
- **Nativo** loja: inalterado
- **Exceções** no celular: `/agendar`, `/baixar`, privacidade/termos, `/embedded-signup`
- SW: `fetch` → `respondWith(fetch(...))` (rede pura, critério Chrome)

## Landing de divulgação (`/baixar`)

URL: **https://lashmatch-627fd.web.app/baixar**

Página estática em `public/baixar/index.html` (não passa pelo SPA).

| Botão | Destino |
|-------|---------|
| **Android** | Instala PWA (`beforeinstallprompt` ou abre `/` com passos Chrome) |
| **iPhone** | [App Store LashMatch](https://apps.apple.com/br/app/lashmatch/id6782080036) |

- Rewrite Hosting: `/baixar` → `/baixar/index.html`
- Gate PWA: `/baixar` em `PUBLIC_PATH_PREFIXES` (`utils/pwaWeb.ts`)
- Copiado no `scripts/copy-pwa-assets.mjs` após `export:web`

## Deploy web

```powershell
cd C:\Users\gusta\LashMatch
npm run export:web
firebase deploy --only hosting
```

- `firebase.json` → `hosting.public`: **`dist-web`**
- `export:web` já chama `scripts/copy-pwa-assets.mjs` (manifest, SW, ícones, `tokenizar.html`, `baixar/`)
- Rewrites SPA: `**` → `/index.html` (arquivos reais como `/sw.js` têm prioridade)
- PowerShell: usar `;` em vez de `&&` se necessário

## Erros conhecidos (web + análise)

| Problema | Causa | Solução |
|----------|-------|---------|
| Tela preta em `analysisResult` na web | Reanimated + `resolveAssetSource` | **Não** suportar análise na web — usar `.web.tsx` bloqueado |
| URL gigante após câmera | `fotoFrenteBase64` nos params da rota | `sessionStorage` via `utils/assistenteSession.ts` (só mobile) |
| Card "Iniciar Nova Análise" na web | Deploy antigo ou aviso com mesmo título | `canUseClientAnalysis()` + remover atalho desktop |

## Checklist agente

- [ ] Nunca reintroduzir fluxo manual/IA na web sem decisão explícita
- [ ] Home web sem card nem texto "Iniciar Nova Análise"
- [ ] `WebDesktopPanel` sem atalho de análise
- [ ] Histórico em `clientes/[id].tsx` pode permanecer **somente leitura**
- [ ] Após mudança web: `export:web` + deploy hosting

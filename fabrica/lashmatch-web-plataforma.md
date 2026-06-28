---
tags:
  - lashmatch
  - expo-web
  - hosting
  - analise
fonte: LashMatch (jun/2026)
projeto: LashMatch
atualizado_em: 2026-06-09
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

## Deploy web

```powershell
cd C:\Users\gusta\LashMatch
npm run export:web
firebase deploy --only hosting
```

- `firebase.json` → `hosting.public`: **`dist`**
- Rewrites SPA: `**` → `/index.html`
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

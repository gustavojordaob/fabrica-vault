---
tags:
  - setmatch
  - lgpd
  - app-store
  - play-store
  - expo
atualizado_em: 2026-08-18
---

> **Agente Cursor — use MCP antes de codar**
> `rag_buscar("setmatch excluir conta privacy terms suporte")`
> `buscar_historico("setmatch compliance lojas")`
> Ver também [[excluir-conta-app-expo-padrao]] · [[modulo-ajuda-suporte-expo]]

# Setmatch — Compliance lojas (App Store / Play)

Repo: `setmatch-app` · Firebase: `setmatch-app-fabrica`

## URLs públicas (Hosting)

| Página | URL |
|--------|-----|
| Privacidade | https://setmatch-app-fabrica.web.app/privacy |
| Termos | https://setmatch-app-fabrica.web.app/terms |
| Suporte | https://setmatch-app-fabrica.web.app/suporte |

Arquivos: `public/privacy|terms|suporte/index.html` · copiados por `scripts/copy-pwa-assets.mjs` no `deploy:web`.

## App

| Item | Onde |
|------|------|
| Constantes | `constants/legal.ts` |
| URL CF | `utils/config.ts` → `getExcluirContaUrl()` / `EXPO_PUBLIC_EXCLUIR_CONTA_URL` |
| Consentimento | `components/legal/LegalConsent.tsx` em login, cadastro, admin-login |
| Conta | `components/legal/AccountComplianceLinks.tsx` em Perfil + Painel clube |
| Hook | `hooks/useDeleteAccount.ts` + `services/account.ts` |
| Idade mín. | `IDADE_MINIMA_APP = 13` no wizard |
| iOS encryption | `app.json` → `ITSAppUsesNonExemptEncryption: false` |
| Photo library purpose string | `NSPhotoLibraryUsageDescription` + plugin `expo-image-picker` — exemplo: foto de perfil em Editar perfil / post na Home |
| Aulas online | **Sempre gratuitas** no app (sem IAP). Stripe só serviço presencial |
| Login | Só **email/senha** (sem Google/Apple/Facebook) — Guideline 4.8 |

## App Store 4.8 (ago/2026)

Com login de terceiro (Google) a Apple exige Sign in with Apple. Setmatch **removeu** os botões sociais: cadastro/login só com email e senha. Novo build nativo obrigatório.

## App Store 3.1.1 (ago/2026)

Sem In-App Purchase: o app **não cobra vídeo/aula online** em nenhuma plataforma. Removido preço, cadeado, “mensagem para liberar” e checkout `aula_online`. Mensalidade de aula **presencial**, ranking e torneio (serviço na quadra) seguem no Stripe.

Build iOS precisa ser **nativo** (purpose string não vai em OTA). `ios.buildNumber` incrementado.

## Cloud Function

```
POST https://southamerica-east1-setmatch-app-fabrica.cloudfunctions.net/excluirConta
Authorization: Bearer <Firebase ID token>
```

Código: `functions/src/deleteAccount.ts` + export `excluirConta` em `functions/src/index.ts`.

Wipe: storage `usuarios/{uid}/`, clubes do dono (+ rankings/torneios), pagamentos/matrículas/desafios/partidas/posts/amizades/conversas, `usuarios/{uid}`, `auth.deleteUser`.

## Checklist App Store Connect / Play

- [ ] Privacy Policy URL = `/privacy`
- [ ] Terms / EULA = `/terms` (ou padrão Apple)
- [ ] Support URL = `/suporte`
- [ ] Account deletion path documentado (Perfil → Excluir)
- [ ] Idade rating / não direcionado a crianças &lt; 13

## Deploy

```powershell
Set-Location functions; npm run build; Set-Location ..
npx firebase-tools deploy --only functions:excluirConta --project setmatch-app-fabrica
npm run deploy:web
```

---

*Última atualização: 08/08/2026*

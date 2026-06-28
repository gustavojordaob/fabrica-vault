---
tags:
  - firebase
  - deploy
  - checklist
  - fluxo
  - fabrica
atualizado_em: 2026-06-28
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **firebase** — `firebase_update_environment` com project ID do `.firebaserc`
> 2. MCP **fabrica-apps** — `rag_buscar("firebase deploy checklist")`
> 3. Regra global: `firebase-deploy-checklist.mdc` (hooks pré/pós deploy)

# Firebase — checklist de deploy (padrão fábrica)

Quando pedir **deploy**, **subir functions**, **publicar hosting** ou **atualizar rules**, siga esta ordem no **workspace aberto** (project ID via `.firebaserc` — nunca hardcodar projeto de outro app).

## Antes do deploy

1. **MCP Firebase** — `firebase_update_environment({ project_dir, active_project })`
2. Confirmar **cwd na raiz** do repo (onde está `firebase.json` + `.firebaserc`)
3. Conferir **alias** correto em `.firebaserc` (`default` / `prod`)

### Cloud Functions

```powershell
Set-Location functions
npm run build
Set-Location ..
firebase deploy --only "functions:NOME1,functions:NOME2"
```

- Params em `functions/.env` (templates WhatsApp, etc.) — variáveis vazias quebram deploy non-interactive
- Secrets via `firebase functions:secrets:set NOME` — **nunca** no Git
- PowerShell: ao deployar várias functions, use **aspas** na lista (`--only "functions:a,functions:b"`)

### Firestore

```powershell
firebase deploy --only firestore:rules
firebase deploy --only firestore:indexes
```

### Hosting (Expo web)

```powershell
npx expo export --platform web
firebase deploy --only hosting
```

## Depois do deploy (obrigatório validar)

| O que deployou | Validação |
|----------------|-----------|
| Functions | `firebase functions:log` + teste HTTP se houver `testar*` |
| Rules | Operação no app que antes falhava (permission-denied) |
| Hosting | Abrir `https://<project-id>.web.app` |

## Nunca

- Declarar "deploy ok" sem saída `Deploy complete!` ou exit code 0
- Deploy de functions **sem** `npm run build` antes
- Usar project ID de outro app da conversa
- Rodar `firebase deploy` fora da raiz do workspace aberto

## Hooks Cursor (automático)

| Momento | Script | Função |
|---------|--------|--------|
| Comando `firebase` | `firebase-shell-gate.js` | Checklist + project ID antes do deploy |
| Pós-deploy | `firebase-deploy-post.js` | Logs, URL web.app, próximos passos |

Ver também: [[firebase-setup-patterns]] · [[cloud-functions-patterns]] · [[checklists-deploy]]

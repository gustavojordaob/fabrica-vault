---
tags:
  - lgpd
  - app-store
  - firebase
  - expo
  - cortejo
  - lashmatch
fonte: cortejo + lashmatch (jun/2026)
---

> **Obrigatório Apple / LGPD:** app deve permitir exclusão permanente da conta e dos dados pessoais.

# Excluir conta — padrão Expo + Cloud Functions (Cortejo / LashMatch)

## Arquitetura

```
App (Perfil / Mais)
  → Alert.confirm "Excluir permanentemente"
  → POST excluirConta (Bearer Firebase ID token)
Cloud Function
  1. verifyIdToken
  2. cancelar assinaturas MP ativas (e-mail + id salvo)
  3. apagar Storage (prefixo do usuário)
  4. apagar Firestore (subcoleções + perfil)
  5. admin.auth().deleteUser(uid)
App
  → signOut (ignorar erro se usuário já removido)
  → router.replace('/Login')
```

## Arquivos por projeto

| Camada | Cortejo | LashMatch |
|--------|---------|-----------|
| Hook | `hooks/useDeleteAccount.ts` | idem |
| Service | `services/account.ts` | idem |
| URL | `utils/config.ts` → `getExcluirContaUrl()` | idem |
| UI | `(tabs)/mais.tsx` + `config/conta.tsx` | `(tabs)/perfilUsuario.tsx` |
| Backend | `functions/SRC/deleteAccount.ts` + `excluirConta` | idem |
| Env | `EXPO_PUBLIC_EXCLUIR_CONTA_URL` | idem |

## Firestore apagado

### Cortejo (`artifacts/cortejo/salons/{salonId}`)

Proprietário: salão inteiro + subcoleções (`members`, `clients`, `appointments`, …) + Storage `salons/{salonId}/`.

Membro equipe: só documento em `members` (não apaga o salão).

### LashMatch (`artifacts/{appId}/users/{uid}`)

- `usuarios/{uid}`
- Subcoleções: `clientes` (+ `historicoAnalises` por cliente), `agendamentos`, `servicos`, `funcionarias`, `estoque`, `vendas`, `despesas`, `pagamentos`, `resumoLembretes`
- Storage: `artifacts/{appId}/users/{uid}/`

`appNamespaceId` = `app.options.appId` (body) ou `usuarios.artifactsAppNamespaceId` ou secret `ARTIFACTS_APP_NAMESPACE_ID`.

## Mercado Pago

Antes de apagar dados: cancelar preapprovals ativos (`PUT status: cancelled`) — busca por `payer_email` + id em `plano.mp_preapproval_id` (LashMatch) ou `subscription.mpPreapprovalId` (Cortejo).

## Variáveis

```bash
EXPO_PUBLIC_EXCLUIR_CONTA_URL=https://us-central1-<PROJECT>.cloudfunctions.net/excluirConta
```

Hosting (opcional): rewrite `/api/excluirConta` → function (Cortejo e LashMatch).

## Deploy

```bash
cd functions && npm run build
firebase deploy --only functions:excluirConta --project <PROJECT_ID>
```

## Checklist

- [ ] Botão visível no perfil / mais (variante danger)
- [ ] Alert com texto claro (irreversível + cancelamento assinatura)
- [ ] Function cancela MP antes de delete Firestore
- [ ] `admin.auth().deleteUser` após dados apagados
- [ ] `EXPO_PUBLIC_EXCLUIR_CONTA_URL` no `.env`
- [ ] Deploy da function após alterar backend

---

*Última atualização: jun/2026*

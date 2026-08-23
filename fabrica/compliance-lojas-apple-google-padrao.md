---
tags:
  - fabrica
  - app-store
  - play-store
  - compliance
  - gateway
  - expo
atualizado_em: 2026-08-18
status: ativo
---

> **Agente Cursor — GATEWAY de aplicativo (ler PRIMEIRO)**
>
> `rag_buscar("compliance lojas apple google 4.8 3.1.1 purpose string login")`
> `buscar_historico("app store recusa guideline IAP login")`
>
> Qualquer app Expo/RN (Setmatch, LashMatch, Cortejo, novo): **antes** de auth social, pagamento, mídia, permissões ou `eas build`/`submit`.
>
> Casos reais: Setmatch 1.0 (2) **5.1.1** + **3.1.1**; Setmatch 1.0 (5) **4.8**.

# Compliance lojas — Apple App Store + Google Play

Checklist para a IA **identificar o que falta** e não repetir recusa. Não substitui a nota do projeto (`*-compliance-lojas-padrao.md`).

## Quando este guia é obrigatório

| Pedido do usuário | O que checar neste MD |
|-------------------|------------------------|
| Login Google / Facebook / Apple “em breve” | **4.8** |
| Pagar conteúdo digital (vídeo, aula online, créditos, unlock) | **3.1.1** / Play Billing |
| Assinatura in-app | IAP (iOS) + Billing (Android) ou só serviço real |
| Foto, câmera, galeria, localização | Purpose strings específicas |
| Excluir conta / LGPD | Account deletion + URLs públicas |
| `eas build` / submit loja | Versão nativa + Info.plist + este checklist |

**OTA (`eas update`) não atualiza** Info.plist, entitlements, ícone nativo, Sign in with Apple capability. Recusa de permissão / login nativo **exige build novo** + `ios.buildNumber` / `android.versionCode` incrementados.

## Apple — impedimentos que já nos derrubaram

### 4.8 — Login Services

Se o app oferece **login de terceiro** (Google, Facebook, etc.) como opção equivalente, precisa de **outro login** que:

- coleta só nome + e-mail;
- permite **esconder o e-mail** (Hide My Email);
- não rastreia ads sem consentimento.

**Sign in with Apple** cumpre. **Email/senha da própria conta NÃO cumpre** o 4.8 (a Apple não aceita isso como substituto do Google).

**Duas saídas válidas:**

1. Implementar **Sign in with Apple de verdade** (capability no bundle + Firebase Apple provider + botão funcional no iOS), **ou**
2. **Remover** todos os logins de terceiro (Google/Facebook) **e** botões “em breve” da Apple. Só email/senha.

**Proibido:** botão Apple que abre “em breve”. Reviewer vê o ícone e aplica 4.8.

Setmatch (ago/2026): saiu Google/Apple/Facebook da UI e do `AuthContext`.

### 3.1.1 — In-App Purchase

Conteúdo **digital** consumido no app (vídeo, aula online, créditos, desbloqueio de feature) **não** pode ser cobrado só com Stripe/Mercado Pago no iOS.

| Tipo | Pode Stripe/MP no iOS? | Precisa IAP? |
|------|------------------------|--------------|
| Vídeo / aula **online** / unlock digital | Não | Sim, ou **tirar a cobrança** |
| Mensalidade de aula **presencial**, ranking/torneio **na quadra**, serviço físico | Sim (serviço real) | Não |
| Assinatura de software (LashMatch/Cortejo iOS) | Não | RevenueCat / StoreKit |

Setmatch: aula online **sempre grátis**; Stripe só presencial / ranking / torneio.

### 5.1.1 — Purpose string (privacidade)

`NSPhotoLibraryUsageDescription` (e equivalentes de câmera/localização) **não** pode ser genérico (“para melhorar a experiência”).

Tem que dizer **o que o app faz** + **exemplo de tela**:

> Setmatch uses your photo library so you can choose a profile picture on Edit Profile, or attach a photo to a post on Home.

Vale o plugin `expo-image-picker` **e** `infoPlist` no `app.json`. Reviewer no **iPad** mesmo com `supportsTablet: false`.

### Outros Apple (checklist)

- [ ] Privacy Policy + Terms + Support **URLs públicas** no App Store Connect
- [ ] Excluir conta no app (Guideline 5.1.1(v) / LGPD) — [[excluir-conta-app-expo-padrao]]
- [ ] `ITSAppUsesNonExemptEncryption: false` se não usa crypto além de HTTPS
- [ ] Idade mínima coerente (não “crianças” se o app não é kids)
- [ ] Conta demo na Review Information (email + senha que funcionam)
- [ ] Após recusa: **novo `buildNumber`**, anexar o IPA, responder no Resolution Center (só texto sem binário novo **não** resolve 4.8/3.1.1/5.1.1)

## Google Play — espelho

- **Digital goods** no Android também exigem Google Play Billing (não só Stripe), se for conteúdo in-app.
- **Data safety** tem que bater com o que o app coleta (Google Sign-In, foto, localização).
- Permissões de foto/mídia: declaração no Play Console + texto no app.
- Excluir conta e política de privacidade públicas — mesmo espírito da Apple.
- `android.versionCode` sobe em **todo** AAB novo.

## O que a IA deve varrer no código (antes do submit)

```text
1. Login: existe Google/Facebook/Apple na UI? Apple é real ou "em breve"?
   → 4.8
2. Há preço / cadeado / checkout em vídeo, aula online, crédito, feature digital?
   → 3.1.1 (iOS) / Play Billing (Android)
3. ImagePicker / Location / Camera: purpose string com exemplo de tela?
4. Perfil: Excluir conta + links Termos/Privacidade/Suporte?
5. app.json: version (marketing) + ios.buildNumber + android.versionCode
   únicos vs o último binário na loja
6. Mudou Info.plist / plugin nativo? OTA não basta — eas build nativo
```

## Versão no código (obrigatório a cada submit)

| Campo | Arquivo | Quando sobe |
|-------|---------|-------------|
| `expo.version` | `app.json` | Nova versão de marketing na loja (1.0.0 → 1.0.1) |
| `ios.buildNumber` | `app.json` | **Todo** IPA novo (Apple recusa build repetido) |
| `android.versionCode` | `app.json` | **Todo** AAB novo |
| `eas.json` `autoIncrement` | production | Pode somar +1 **além** do bump local — conferir o número no log (`Bumping ... to N`) |

App Store: recusa de **1.0 (5)** → mesmo `version` `1.0.0` + `buildNumber` novo. Só mude `expo.version` se for criar **versão nova** no App Store Connect.

## Resposta típica na Review (depois do binário novo)

**4.8 (removeu social):**  
We removed all third-party login options. Users sign in with email and password only.

**3.1.1 (tirou digital pago):**  
Paid digital video/classes were removed. Remaining charges are in-person services.

**5.1.1:**  
Purpose string now states the exact screens (example: Edit Profile / Home post).

## Apps da fábrica

| App | Decisão vigente |
|-----|-----------------|
| Setmatch | Sem social login; aula online grátis; Stripe presencial |
| LashMatch / Cortejo | iOS assinatura = RevenueCat; Android pode MP — ver notas de cada um |

## Checklist copiável (app novo)

- [ ] Sem Google/Facebook **ou** Sign in with Apple real no iOS
- [ ] Sem cobrança de bem digital fora da IAP/Play Billing
- [ ] Purpose strings com tela + ação
- [ ] `/privacy` `/terms` `/suporte` no Hosting
- [ ] Excluir conta
- [ ] Demo account na Review
- [ ] buildNumber / versionCode incrementados
- [ ] `rag_buscar` desta nota **antes** de `eas build`

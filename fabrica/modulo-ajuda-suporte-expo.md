---
tags:
  - suporte
  - ajuda
  - whatsapp
  - expo
  - app-store
  - hosting
fonte: cortejo (jun/2026)
---

> **Não confundir** com WhatsApp Business API para clientes do salão ([[whatsapp-business-api]]).  
> Este módulo é **suporte ao desenvolvedor/dona do app** (dúvidas sobre o produto).

# Módulo Ajuda e Suporte — padrão Expo (Cortejo / LashMatch)

## Página pública (App Store / Play Store)

Obrigatória na Apple: **URL de suporte** acessível sem login.

| Item | Cortejo |
|------|---------|
| Suporte | `https://cortejo-app.web.app/suporte` |
| Privacidade | `https://cortejo-app.web.app/privacidade` |
| Arquivo repo | `public/suporte/index.html`, `public/privacidade/index.html` |
| Deploy | `scripts/copy-public-to-dist.mjs` → `dist/suporte/` + `firebase deploy --only hosting` |
| Constantes app | `constants/support.ts` — `SUPPORT_PAGE_URL`, `PRIVACY_PAGE_URL`, `SUPPORT_EMAIL` |

**App Store Connect:** colar URL de suporte e privacidade nos metadados do app.

## Estrutura de arquivos (copiar para novos projetos)

```
constants/support.ts       # telefone, e-mail, URLs públicas, mensagem WhatsApp
utils/supportContact.ts    # openSupportWhatsApp() via Linking + wa.me
public/suporte/index.html  # página pública (Hosting)
public/privacidade/index.html
app/config/ajuda.tsx       # in-app (Expo Router)
```

### `constants/support.ts`

```typescript
export const SUPPORT_PHONE_E164 = '5519989632897';
export const SUPPORT_PHONE_DISPLAY = '(19) 98963-2897';
export const SUPPORT_EMAIL = 'contato@exemplo.com.br';
export const SUPPORT_PAGE_URL = 'https://<projeto>.web.app/suporte';
export const PRIVACY_PAGE_URL = 'https://<projeto>.web.app/privacidade';
export const SUPPORT_WHATSAPP_MESSAGE = 'Olá! Preciso de ajuda com o app NomeDoApp.';
```

### `utils/supportContact.ts`

- URL: `https://wa.me/${E164}?text=${encodeURIComponent(message)}`
- `Linking.canOpenURL` antes de `openURL`
- `Alert.alert` em falha
- **Sem botão "Ligar"** (`tel:`) — decisão de produto jun/2026 (só WhatsApp)

### Tela `ajuda.tsx`

- `SafeAreaView` + `ScrollView`
- Card contato: ícone headset, telefone, e-mail, botão **Chamar no WhatsApp**
- Botão **Abrir página de suporte** → `Linking.openURL(SUPPORT_PAGE_URL)`
- FAQ: array `{ q, a }[]` com `.map()` — perguntas específicas do app (agenda, assinatura, IA, etc.)
- Cores: seguir identidade do app (Cortejo `#6B4226`, LashMatch `#D63384` / dark `#000` + `#1a1a1a`)

## Navegação

| Projeto | Entrada no menu |
|---------|-----------------|
| **Cortejo** | `(tabs)/mais.tsx` → `router.push('/config/ajuda')` |
| **LashMatch** | `constants/moreMenuItems.ts` + `perfilUsuario.tsx` (excluir conta no perfil) |

Registrar rota no `app/_layout.tsx`:

```typescript
<Stack.Screen name="config/ajuda" options={{ title: 'Ajuda', headerBackTitle: 'Mais' }} />
// LashMatch: name="ajuda"
```

## Checklist ao adicionar em projeto novo

- [ ] `public/suporte/index.html` + `public/privacidade/index.html` (estilo marca)
- [ ] `copy-public-to-dist.mjs` copia ambos para `dist/`
- [ ] `constants/support.ts` com URLs do projeto Firebase Hosting
- [ ] URLs no App Store Connect / Play Console
- [ ] `openSupportWhatsApp` testado em dispositivo físico
- [ ] Link no menu "Mais" / Perfil
- [ ] FAQ com 3–5 perguntas reais do produto
- [ ] Sem `tel:` / botão ligar (salvo pedido explícito)
- [ ] Não commitar alteração de telefone sem confirmar com o dono do produto

## Referência de implementação

- Cortejo: `app/config/ajuda.tsx`, `app/(tabs)/mais.tsx`, `public/suporte/index.html`
- LashMatch: `app/ajuda.tsx`, `constants/moreMenuItems.ts`
- Visão geral assinatura + limites: [[cortejo-modulos-jun2026-padrao]]

---

*Última atualização: jun/2026*

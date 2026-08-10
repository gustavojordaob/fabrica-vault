---
tags:
  - setmatch
  - i18n
  - expo
atualizado_em: 2026-08-08
---

> **Agente Cursor — use MCP antes de codar**
> `rag_buscar("setmatch i18n idioma locale")`
> `buscar_historico("setmatch idioma")`

# Setmatch — i18n (pt-BR / en-US / es)

Repo: `setmatch-app`

## Arquitetura

```
LocaleProvider (app/_layout.tsx)
  → AsyncStorage @setmatch/locale
  → createTranslator(locale)
  → useT() / useLocale()
```

| Item | Path |
|------|------|
| Context | `contexts/LocaleContext.tsx` |
| Dicts | `i18n/locales/pt-BR.ts`, `en-US.ts`, `es.ts` |
| Hook | `hooks/useI18n.ts` → `useT`, `useLocale` |
| UI seletor | `components/legal/LanguagePicker.tsx` (Perfil / Painel via AccountComplianceLinks) |
| Gate pré-slides | `components/onboarding/LanguageGate.tsx` — primeira tela do `/onboarding` antes da apresentação |

## Idiomas

| Código | Label |
|--------|--------|
| `pt-BR` | Português (Brasil) — **padrão** |
| `en-US` | English (US) |
| `es` | Español |

Fallback: se chave faltar no idioma ativo, usa `pt-BR`, depois a própria chave.

## Uso

```tsx
import { useT } from '../hooks/useI18n';

const t = useT();
<Text>{t('perfil.title')}</Text>
Alert.alert(t('common.error'), t('common.saveFailed'));
t('primeiroAcesso.welcomeName', { name });
```

## Regra para agentes

1. Toda string nova de UI → adicionar nos **3** dicionários
2. Nunca hardcodar PT em tela já migrada
3. Evitar sombrear `t` (`onChangeText={(text) => ...}` / `const termo = ...`)

## Checklist

- [ ] Chave em pt-BR + en-US + es
- [ ] `useT()` no componente
- [ ] Interpolação `{{var}}` se necessário
- [ ] Seletor visível no Perfil

---

*Última atualização: 08/08/2026*

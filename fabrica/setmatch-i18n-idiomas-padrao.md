---
tags:
  - setmatch
  - i18n
  - expo
atualizado_em: 2026-08-08
---

> **Agente Cursor — use MCP antes de codar**
> `rag_buscar("setmatch i18n idioma locale pt-BR en-US es")`
> `buscar_historico("setmatch idioma")`

# Setmatch — idiomas (pt-BR / en-US / es)

Repo: `setmatch-app`

## Arquitetura

```
LocaleProvider (app/_layout.tsx)
  → AsyncStorage @setmatch/locale
  → createTranslator(locale) → t(key, params?)
LanguagePicker no Perfil (AccountComplianceLinks)
```

| Idioma | Código | Default |
|--------|--------|---------|
| Português (Brasil) | `pt-BR` | ✅ |
| English (US) | `en-US` | |
| Español | `es` | |

## Arquivos

- `contexts/LocaleContext.tsx` — `useLocale`, `useT`
- `i18n/index.ts` — `createTranslator`, fallback pt-BR
- `i18n/locales/pt-BR.ts` · `en-US.ts` · `es.ts`
- `components/legal/LanguagePicker.tsx`

## Regra para agentes

1. Toda string nova de UI → chave nos **3** dicionários
2. Interpolação: `t('primeiroAcesso.welcomeName', { name })` com `{{name}}` no texto
3. Não usar `i18next` — Context leve + AsyncStorage
4. Evitar shadowing: não declarar `const t = ...` local se já existe `useT()`

## Checklist

- [ ] Chave em pt-BR, en-US e es
- [ ] `useT()` no componente
- [ ] Seletor visível no Perfil / Painel (via AccountComplianceLinks)

---

*Última atualização: 08/08/2026*

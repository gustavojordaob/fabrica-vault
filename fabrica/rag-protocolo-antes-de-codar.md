---
tags:
  - rag
  - protocolo
  - agente
  - libs-externas
fonte: incidente Cortejo 09/06/2026
---

> **Agente Cursor — leia isto quando for implementar UI, lib npm ou feature nova**
>
> Este documento existe porque um agente implementou `react-native-calendars` no **Cortejo** **sem** consultar `react-native-calendars.md` indexado no RAG — escolheu `Calendar` + lista manual quando o guia já documentava `Agenda`, `ExpandableCalendar`, `LocaleConfig` pt-BR e padrões de `markedDates`.

---

# Protocolo RAG — antes de qualquer resposta

> **Escopo:** toda mensagem do usuário (simples ou complexa), não só código.  
> **Canônico:** [[arquitetura-fabrica-ia]] § Protocolo RAG universal.

## Quando dispara (obrigatório)

| Situação | Ação MCP |
|----------|----------|
| **Qualquer pergunta ou pedido** | `rag_buscar` + `buscar_historico` |
| Erro / bug | + `buscar_solucao` |
| `npx expo install` + UI | `rag_buscar("<pacote>")` + guia em `fabrica/` |
| Calendário / agenda | ver tabela abaixo |
| Nova feature | + PRD do projeto |

**Exceção:** cumprimento puro (`oi`, `obrigado`) sem pedido.

**Se RAG vazio:** julgamento próprio + código do repo; opcional avisar que não havia nota.

**Regra:** contexto Chroma injetado pelo hook **não substitui** MCP antes de `Write` / `Shell`.

---

## Checklist em 4 passos (copiar mentalmente)

1. **Buscar** — MCP `rag_buscar` com query específica da lib (não só palavras genéricas do usuário).
2. **Histórico** — MCP `buscar_historico` no mesmo tema (implementações passadas, decisões).
3. **Escolher** — comparar componentes/APIs do guia vs o que o usuário pediu (ex.: `Calendar` vs `Agenda` vs `ExpandableCalendar`).
4. **Codar** — só então criar arquivos; ao terminar: `salvar_decisao` + `indexar_rapido.py`.

---

## Caso de estudo — Cortejo, agenda com calendário (09/06/2026)

### O que o usuário pediu

Modernizar a aba Agenda com `react-native-calendars`.

### O que o agente fez (errado)

- Instalou o pacote e codou direto (`Calendar`, `markedDates`, grid de horários manual).
- **Não** chamou `rag_buscar` nem leu `react-native-calendars.md`.
- **Não** avaliou `Agenda` (calendário + lista por dia) nem `ExpandableCalendar` (UX iOS).

### O que existia no RAG e foi ignorado

Arquivo: `obsidian/fabrica/react-native-calendars.md`

- Tabela de componentes (`Calendar`, `Agenda`, `ExpandableCalendar`, `Timeline`, `CalendarProvider`).
- `LocaleConfig` pt-BR (`firstDay: 1`, meses em português).
- Padrão `markedDates` com dots e seleção.
- Tema dark alinhado a apps da fábrica (LashMatch / Cortejo).

### O que deveria ter sido feito

```text
1. rag_buscar("react-native-calendars Calendar Agenda markedDates tema")
2. buscar_historico("agenda calendario cortejo")
3. Decidir: aba Agenda → provavelmente Agenda ou ExpandableCalendar + AgendaList
4. Implementar com LocaleConfig + tema tokens Cortejo (#6B4226)
5. salvar_decisao("Cortejo — componente calendário escolhido e por quê")
```

### Correção sistêmica (para não repetir)

- Hooks `rag-lib.js`: `detectMandatoryRagDocs()` + workflow `implementar_com_guia_rag`.
- Gate `rag-pre-tool.js`: mensagem extra quando lib/UI detectada.
- Este arquivo indexado no Chroma.
- Entrada em `erros-e-solucoes.md` + `decisoes.md`.

---

## Pacotes com guia dedicado na fábrica

| Pacote / tema | Arquivo Obsidian |
|---------------|------------------|
| react-native-calendars | `react-native-calendars.md` |
| Mercado Pago | `mercadopago-integration.md` |
| Firebase | `firebase-setup-patterns.md` |
| WhatsApp Meta | `whatsapp-business-api.md` |
| Expo Router | `expo-router-navegacao.md` |
| Cloud Functions | `cloud-functions-patterns.md` |

Se o pacote não estiver na tabela: `rag_buscar("<nome>")` — pode haver seção em `padroes-fabrica.md` ou nota do projeto.

---

## Frases que o agente NÃO deve dizer

- "Vou consultar o RAG" (faça silenciosamente).
- "O Chroma já injetou contexto" como desculpa para pular MCP.
- "Implemento direto porque é simples" — libs de UI raramente são triviais.

---

## Indexação

Após editar qualquer `.md` em `obsidian/fabrica/`:

```powershell
python C:/Users/gusta/obsidian/indexar_rapido.py
```

Servidor Chroma (se offline):

```powershell
python C:/Users/gusta/obsidian/indexar_obsidian_chroma.py --server
```

---
tags:
  - fabrica
  - erp
  - ui
  - angular
  - telas
  - fiori
atualizado_em: 2026-08-05
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. `rag_buscar("erp agente modo cursor")` → [[erp-agente-modo-cursor]]
> 2. `rag_buscar("erp ui telas")` → **esta nota** (casca UX — estável, **não** por cliente)
> 3. `rag_buscar("erp angular")` → [[erp-angular-estrutura]]
> 4. Domínio do produto → PRD / `erp-modulo-*` (aí sim varia por cliente)
>
> Fonte conceitual: **SAP Fiori Design Guidelines** (floorplans). Adaptado à stack Angular 21 da fábrica — não copiar UI5/OData literalmente.

# ERP — padrão de telas (casca UX)

**Esta nota é a casca.** Lista / filtro / detalhe / form / confirmação / permissão na UI.  
**Não** documenta regra de negócio de estoque/venda — isso é módulo/PRD.  
**Idioma da UI:** português (Brasil) — ver [[../projetos/erp-baseline-prd]].

## Fontes (conceituadas)

| Fonte | O que aproveitamos |
|-------|-------------------|
| [SAP Fiori — floorplans](https://www.sap.com/design-system/fiori-design-web/) | List Report, Object Page, Worklist, Wizard, Overview |
| [When to use which floorplan](https://www.sap.com/design-system/fiori-design-web/v1-136/page-types/floorplans/when-to-use-which-floorplan) | Qual layout para qual tarefa |
| Fábrica | Angular standalone + signals ([[erp-angular-estrutura]]) |

Não usamos SAPUI5 obrigatório — só o **modelo mental** de páginas.

---

## Mapa tarefa → floorplan (fábrica)

| Tarefa do usuário | Floorplan Fiori | Na nossa SPA Angular |
|-------------------|-----------------|----------------------|
| Achar / filtrar / agir em muitos registros | **List Report** | `lista-*.component` + barra de filtros + tabela |
| Fila de trabalho (itens a processar) | **Worklist** | Lista sem filtro pesado; foco em ações por linha |
| Ver / criar / editar **um** objeto | **Object Page** | Rota detalhe + seções (abas ou âncoras) + form |
| Fluxo longo / pouco familiar (3–8 passos) | **Wizard** | Stepper + resumo final antes de gravar |
| Painel do dia (KPIs + atalhos) | **Overview** | Dashboard com cards (opcional no MVP) |
| Ir direto a um objeto por código | **Initial Page** | Busca rápida (código/SKU) → navega ao detalhe |

Padrão mais comum no ERP da fábrica: **List Report → Object Page** (lista → detalhe/form).

---

## 1. List Report (lista + filtro)

### Estrutura da página

```
[ Título + ações primárias (Novo) ]
[ Filter bar: busca + filtros + Limpar + Aplicar ]
[ Tabela / grid ]
[ Paginação ou infinite scroll ]
[ Empty / loading / erro ]
```

### Regras

- **Filtro antes de sobrecarregar:** busca textual + 2–5 filtros relevantes (status, período, filial). Não 20 filtros no MVP.
- **Aplicar explícito** em filtros pesados (data/range); busca textual pode ser debounce.
- **Colunas:** só as que ajudam a **identificar e decidir**; detalhe vai no Object Page.
- **Ações de linha:** Ver / Editar / (mais) — só se a permissão permitir (ver §5).
- **Ação de massa:** opcional; só com seleção + confirmação.
- **Empty state:** mensagem + CTA “Novo” se `podeCriar`.
- **Loading:** skeleton/spinner na área da tabela, não tela branca.
- **Erro de API:** toast/banner + retry; não sumir com a filter bar.

### Pastas (alinhar Angular)

```
features/<entidade>/
├── lista-<entidade>.component.ts
├── <entidade>.service.ts
├── <entidade>.model.ts
└── <entidade>.routes.ts
```

---

## 2. Object Page (detalhe / form)

### Estrutura

```
[ Header: título + status + ações (Salvar / Cancelar / …) ]
[ Seções: Dados gerais | Itens | Histórico | … ]
[ Footer sticky em modo edição: Salvar + Cancelar ]
```

### Modos

| Modo | Comportamento |
|------|----------------|
| **Visualizar** | Campos read-only; botão Editar se `podeEditar` |
| **Criar** | Form vazio; Salvar = POST; Cancelar = volta lista (confirma se dirty) |
| **Editar** | Form preenchido; Salvar = PUT/PATCH; Cancelar = confirma se dirty |

### Regras

- Validação **no form** (required, formato) + mensagens do **backend** (negócio) sem perder o que o usuário digitou.
- **Dirty check:** sair sem salvar → diálogo “Descartar alterações?”.
- Dinheiro / quantidades: máscara alinhada a `numeric` / `BigDecimal` ([[erp-postgres-schema]], [[erp-transacao-dominio]]).
- Objeto complexo: seções/abas; wizard só se ≥3 passos e fluxo pouco familiar.

---

## 3. Confirmação (ações destrutivas ou irreversíveis)

Usar **diálogo modal** (não só `confirm()` nativo) quando:

- Excluir / inativar
- Cancelar documento que gera estorno
- Aprovar / rejeitar com efeito contábil ou de estoque

### Conteúdo mínimo do diálogo

1. O que vai acontecer (1 frase)
2. Identificação do objeto (código/nome)
3. Se houver efeito colateral (ex.: “estorna estoque”) — **dizer**
4. Botões: **Cancelar** (secundário) + **Confirmar** (destrutivo/primário)

Sem confirmação para Salvar rotineiro de form (salvo regra do cliente no PRD).

---

## 4. Worklist vs List Report

| | List Report | Worklist |
|--|-------------|----------|
| Uso | Cadastro / consulta ampla | “Minha fila” (pendentes, a aprovar) |
| Filtro | Rico | Pouco ou pré-fixado |
| Meta | Encontrar | Processar |

---

## 5. Permissões na UI (casca)

A UI **esconde ou desabilita**; o **backend autoriza de verdade**.

| Capacidade | UI |
|------------|-----|
| `podeListar` | Sem rota/menu se false |
| `podeCriar` | Esconde “Novo”; bloqueia rota `/novo` |
| `podeEditar` | Esconde Editar / Salvar |
| `podeExcluir` | Esconde Excluir |
| `podeAprovar` | Esconde ação de aprovação |

- Nunca confiar só no front.
- Botão visível + 403 da API → mensagem clara (“sem permissão”), não tela quebrada.
- Fonte das claims: token / endpoint `/me` — ver [[erp-auth-login]].

---

## 6. Estados obrigatórios em toda tela de dados

| Estado | Obrigatório |
|--------|-------------|
| Loading | Sim |
| Empty | Sim (lista) |
| Erro | Sim |
| Sucesso (toast após salvar) | Sim |
| Forbidden (403) | Sim se rota sensível |

---

## 7. O que NÃO vai nesta nota

- Campos e fluxos de **estoque/venda/fiscal** → `erp-modulo-*` + PRD do cliente
- Cores/marca do cliente → opcional `erp-design-system.md` ou token no repo
- Widgets SAPUI5 / OData annotations — fora do stack Angular da fábrica

---

## Checklist do agente (antes do PR)

- [ ] Escolheu List Report vs Object Page vs Wizard vs Worklist
- [ ] Lista tem filtro + empty + loading + erro
- [ ] Form tem dirty check + validação + mensagens de API
- [ ] Ação destrutiva tem diálogo com efeito colateral explícito
- [ ] Ações respeitam permissões na UI
- [ ] Feature em `features/<entidade>/` ([[erp-angular-estrutura]])

## Queries RAG

```
rag_buscar("erp ui telas")
rag_buscar("erp angular padrao")
buscar_historico("erp tela lista form")
```

## Links

- [[erp-agente-modo-cursor]] · [[erp-angular-estrutura]] · [[erp-stack]] · [[erp-auth-login]] · [[erp-modulo-produto]] · [[erp-modulo-estoque]]
- SAP Fiori Design System (web): https://www.sap.com/design-system/fiori-design-web/

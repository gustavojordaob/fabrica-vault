---
tags:
  - sinaflor
  - gestao
  - licenciamento
  - visibilidade
  - perfil
atualizado_em: 2026-07-28
projeto: SINAFLOR2
links:
  - "[[spring-backend]]"
  - "[[../projetos/sinaflor-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. `rag_buscar("sinaflor gestao visibilidade Meus Todos Gerente Analista")`
> 2. `buscar_historico("sinaflor gestao Meus processos")`
> 3. Código: `LicenciamentoQueryService.filtraAcessoGestao` + `excluirEmElaboracaoGestao`

# Painel de Gestão — visibilidade por perfil

Repo: `autorizacao/.../LicenciamentoQueryService.java`  
Front hint: `personalizar-painel-gestao-lic.component.html`  
Flag UI Todos: sempre **false**; checkbox **Todos os Processos** sempre visível no personalizar (Analista incluso).

## Regra geral (todos os perfis)

- **Não** listar Em Elaboração / Em Elaboração Técnica.
- Implementação: `statusLic` nulo **e** `numeroRegistro` nulo → excluídos (`excluirEmElaboracaoGestao`).

## Gerente Operacional

| Aba | Visão |
|-----|--------|
| **Todos** | Processos dos órgãos do usuário (SCA), qualquer status (exceto elaboração) |
| **Meus** | Destinatário ativo **OU** órgão + Aguardando Distribuição **OU** órgão + tramite ativo com `FL_MANTER_ABERTO=S` e `loginExecutor` = usuário |

## Analista Técnico

| Aba | Visão |
|-----|--------|
| **Meus** | Processos tramitados para ele (`TB_TRAMITE_LIC_DESTINATARIO` ativo) |
| **Todos** | Processos dos órgãos aos quais está vinculado (qualquer status, exceto elaboração) |

## Critério Meus vs Todos

- Front: `meusProcessos=true` (padrão) = Meus; `meusProcessos=false` = Todos.
- Não forçar situação ao alternar Meus/Todos.

## Checklist

- [ ] Em Elaboração não aparece no painel
- [ ] Analista vê checkbox Todos os Processos
- [ ] GO Meus inclui fila Aguardando Distribuição do órgão
- [ ] GO/Analista Todos = órgão, sem ocultar por `manterAberto=N`

---
tags:
  - sinaflor
  - tramitacao
  - encaminhar
  - orgao
  - unidade
  - hu136
fonte: sinaflor2
atualizado_em: 2026-08-20
projeto: SINAFLOR2
links:
  - "[[tramitacao-arquivar-desarquivar]]"
  - "[[tramitacao-solicitar-pagamento-taxa]]"
  - "[[spring-backend]]"
  - "[[mapeamento-frontend-backend]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor tramitacao encaminhar outro orgao HU136")` + `buscar_historico("sinaflor encaminhar orgao")`
> 2. Código: `LicenciamentoTramitacaoService` + `gestao-tramitacao` + `tramitacao-encaminhar-orgao`
> 3. SQL: `autorizacao/.../db/scripts/SPRINT_19/03_tb_tramite_lic_encaminhar.sql`
> 4. Projeto **legado** — não modernizar sem pedido explícito

# Tramitação — Encaminhar para outro Órgão/Unidade (HU136)

## Catálogo

| ID | Tipo | Status resultante |
|----|------|-------------------|
| 3 | Encaminhar para outro Órgão/Unidade | **mantém** o status atual (não muda situação) |

## Campos (diferenças vs Análise/Arquivar)

| Tem | Não tem |
|-----|---------|
| Finalidade (`PERMANENTE` / `TEMPORARIA`) | Analistas (RN21 proíbe) |
| Esfera (1 Fed / 2 Est / 3 Mun) | Anexos |
| UF, Município, Órgão/Unidade | Manter processo aberto |
| Despacho | Tipo de avaliação |
| E-mail (default **ON**) | |

## Regras de negócio

### Quem pode (somente GO)

- Disponível se processo **não** está Arquivado e tem `numeroRegistro`
- Perfil: **apenas Gerente Operacional**

### Finalidade

- **PERMANENTE** — mudança definitiva do órgão/unidade do projeto; unidade anterior perde tramitação
- **TEMPORARIA** — envio para análise específica com retorno futuro ao órgão competente (retorno = fluxo futuro; neste HU o destino já recebe o processo)

### Ao finalizar

- Atualiza `LicenciamentoDadosGerais`: `idOrgaoAmbiental`, `unidadeIbama`, `descricaoUnidadeIbama`, `idCompetencia` (esfera)
- Persiste destino em `TB_TRAMITE_LIC` (colunas HU136)
- Alerta fixo: processo vai ao GO da unidade indicada
- Sucesso (só essa ação na fila): `Tramitações realizadas com sucesso.`

## Backend

- `acoesDisponiveis` inclui `3` via `podeExecutarEncaminharOutroOrgao`
- `validarEncaminhamento` + `aplicarEncaminhamentoOrgao`
- `resolverStatusDoItem`: tipo 3 → status corrente
- Flag manter aberto: tipo 3 fora do sync do lote (como Desarquivar/Pagamento)

## Frontend

- Componente `app-tramitacao-encaminhar-orgao`
- `implementados` inclui `3`; `*ngSwitchCase="3"`
- Órgãos: `LicenciamentoExploracaoService.buscarOrgaosAmbientais(esfera, uf, municipio)`
- Municípios: `getMun(codigoUF)` + `UFEnumImpl`

## Checklist

- [ ] Só GO vê a ação; GA/Analista não
- [ ] Processo Arquivado: ação **não** aparece
- [ ] Sem analistas, sem anexos, sem manter aberto; e-mail ON
- [ ] PERMANENTE/TEMPORARIA atualizam órgão/unidade do projeto
- [ ] Rodar script SQL `03_tb_tramite_lic_encaminhar.sql` antes de testar

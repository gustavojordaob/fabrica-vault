---
tags:
  - sinaflor
  - tramitacao
  - arquivar
  - desarquivar
  - hu133
  - hu134
fonte: sinaflor2
atualizado_em: 2026-08-06
projeto: SINAFLOR2
links:
  - "[[spring-backend]]"
  - "[[mapeamento-frontend-backend]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor tramitacao arquivar desarquivar")` + `buscar_historico("sinaflor arquivar")`
> 2. Código: `LicenciamentoTramitacaoService` + `gestao-tramitacao` + `tramitacao-arquivamento`
> 3. Projeto **legado** — não modernizar sem pedido explícito

# Tramitação — Arquivar (HU133) e Desarquivar (HU134)

## Catálogo

| ID | Tipo | Status resultante |
|----|------|-------------------|
| 7 | Arquivar | `StatusLicEnum.ARQUIVADO` (7) |
| 8 | Desarquivar | Status **anterior** ao último Arquivar ativo (`TB_TRAMITE_LIC.statusAnterior`) |

## Regras de negócio

### Arquivar (GO / GA)

- Disponível se processo **não** está Arquivado e tem `numeroRegistro`
- Sem tipo de avaliação e sem analistas
- Despacho **obrigatório** + **≥1 anexo**
- Checkbox “Manter aberto” visível (default ON); e-mail **oculto** (false)
- Não pode coexistir com Desarquivar na mesma fila/rascunho
- Mensagem de sucesso: `Arquivamento salvo com sucesso.`

### Desarquivar (GO / GA / Analista)

- Disponível **somente** se status = Arquivado
- Despacho + ≥1 anexo obrigatórios
- E-mail visível (default ON); “Manter aberto” **oculto** (false)
- Restaura `statusAnterior` do último trâmite Arquivar ativo
- Mensagem: `Desarquivamento salvo com sucesso.`

## Backend

- `GET .../tramitacao/contexto` → `acoesDisponiveis` inclui 1/2 (Análise/Vistoria), 7 e/ou 8 conforme perfil/status
- `validarFila`: analistas/tipo avaliação só para Análise e Vistoria; anexos obrigatórios para 7/8; bloqueia 7+8 juntos
- `resolverStatusNovo`: aplica transição na ordem da fila (Arquivar/Desarquivar/Vistoria/Análise)
- `TramiteLicRepository.findAtivosByLicenciamentoAndTipo` — recupera último Arquivar

## Frontend

- Dropdown filtra por `acoesDisponiveis` ∩ tipos `{1,2,7,8}`
- `app-tramitacao-arquivamento` com `modo="arquivar"|"desarquivar"`
- `app-anexar-arquivos-tramitacao`: inputs `obrigatorio` + `validarInputs`
- Alerta amarelo **acima da combo** Ações/Tramitações (quando tipo 7 ou 8)
- Despacho + “Escolha uma ou mais opções” **lado a lado** (mesmo padrão Análise: `ui-g-6` + caixa verde do `:host` do despacho)
- Textos: HU133/HU134 (mock Confluence)

## Checklist

- [ ] GO/GA vê Arquivar em processo não arquivado
- [ ] Analista **não** vê Arquivar
- [ ] Processo Arquivado: só Desarquivar (GO/GA/Analista)
- [ ] Finalizar Arquivar → status Arquivado + histórico
- [ ] Finalizar Desarquivar → status anterior ao arquivamento
- [ ] Fila com Arquivar + Desarquivar rejeitada no front e no back

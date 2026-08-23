---
tags:
  - sinaflor
  - tramitacao
  - pagamento
  - taxa
  - guia
  - hu135
fonte: sinaflor2
atualizado_em: 2026-08-13
projeto: SINAFLOR2
links:
  - "[[tramitacao-arquivar-desarquivar]]"
  - "[[spring-backend]]"
  - "[[mapeamento-frontend-backend]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor tramitacao solicitar pagamento taxa HU135")` + `buscar_historico("sinaflor pagamento taxa")`
> 2. Código: `LicenciamentoTramitacaoService` + `gestao-tramitacao` + `tramitacao-arquivamento` (`modo="solicitar-pagamento"`)
> 3. Projeto **legado** — não modernizar sem pedido explícito

# Tramitação — Solicitar Pagamento de Taxa/Guia (HU135)

## Catálogo

| ID | Tipo | Status resultante |
|----|------|-------------------|
| 5 | Solicitar Pagamento de Taxa/Guia de Recolhimento | `StatusLicEnum.AGUARDANDO_PAGAMENTO_TAXA` (5) |

## Regras de negócio

### Quem pode (GO / GA / Analista)

- Disponível se processo **não** está Arquivado e tem `numeroRegistro`
- Sem tipo de avaliação e sem analistas
- Despacho **obrigatório** + **≥1 anexo** (guia)
- Checkbox **Enviar e-mail** visível (default ON); **Manter aberto** oculto (false)
- Alerta (título + texto HU135 RN16) acima da combo Ações/Tramitações
- Mensagem de sucesso (só essa ação na fila): `Tramitações realizadas com sucesso.`

### Observação

- O Sinaflor **não** valida pagamento automaticamente (mensagem de atenção na tela).
- Reaproveita `app-tramitacao-arquivamento` com `modo="solicitar-pagamento"` (mesmo layout de Desarquivar: e-mail + anexos + despacho).

## Backend

- `GET .../tramitacao/contexto` → `acoesDisponiveis` inclui `5` via `podeExecutarSolicitarPagamentoTaxa`
- `validarFila`: anexos obrigatórios para tipo 5
- `resolverStatusDoItem`: tipo 5 → `AGUARDANDO_PAGAMENTO_TAXA`
- Flag manter aberto: tipo 5 tratado como Desarquivar (não propaga sync do lote)

## Frontend

- `implementados` inclui `5`
- `*ngSwitchCase="5"` → `modo="solicitar-pagamento"`
- Alertas: `tituloAlertaArquivamento` / `mensagemAlertaArquivamento`

## Checklist

- [ ] GO/GA/Analista vê a ação em processo não arquivado
- [ ] Processo Arquivado: ação **não** aparece
- [ ] Finalizar → status Aguardando Pagamento de Taxa/Guia + histórico
- [ ] E-mail marcado por padrão; sem “Manter aberto”
- [ ] Alerta informativo permanente durante o preenchimento

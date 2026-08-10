---
tags:
  - fabrica
  - erp
  - modulo
  - estoque
  - inventory
  - sap-mm
  - goods-movement
atualizado_em: 2026-08-05
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. `rag_buscar("erp agente modo cursor")` → [[erp-agente-modo-cursor]]
> 2. `rag_buscar("erp ui telas")` → [[erp-ui-telas]]
> 3. `rag_buscar("erp modulo estoque")` → **esta nota**
> 4. `rag_buscar("erp transacao")` → [[erp-transacao-dominio]] (**obrigatório** em movimento)
> 5. Produto: [[erp-modulo-produto]]
> 6. Cliente diverge? → PRD (quando baixa estoque, multi-depósito, lote…)
>
> **Baseline da fábrica.** Escopo: [[../projetos/erp-baseline-prd]]. UI em **português (Brasil)**.  
> Fontes: **SAP MM Inventory / Goods Movements** (GR, GI, transfer, movement type) + ideias Odoo Stock. Quantidade + razão do movimento; valor contábil completo = fase posterior.

# ERP — módulo canônico: Estoque (Inventory mínimo)

No SAP, **Inventory Management** atualiza quantidade (e valor) a cada **goods movement**, classificado por **movement type**. Aqui: saldo por produto (+ depósito opcional) e **ledger de movimentos** imutável.

## Escopo MVP (fábrica)

| Inclui | Não inclui (PRD / fase 2) |
|--------|---------------------------|
| Saldo atual por produto | WMS / picking avançado |
| Movimentos: entrada, saída, ajuste, transferência | Tipos 101/201… literais SAP |
| Bloqueio se saldo insuficiente na saída | Consignação, QI, blocked stock |
| 1 depósito default (`DEPOSITO_PADRAO`) | Multi-planta completa |
| ACID no lançamento | Contabilização FI automática |

---

## Conceitos (SAP → fábrica)

| SAP MM | Fábrica |
|--------|---------|
| Goods Receipt (GR) | `tipo = ENTRADA` |
| Goods Issue (GI) | `tipo = SAIDA` |
| Stock transfer | `tipo = TRANSFERENCIA` (origem→destino) |
| Transfer posting / adjustment | `tipo = AJUSTE` (inventário / correção) |
| Movement type | `motivo` ou `tipo_movimento` (varchar) — tabela domínio opcional |
| Storage location | `deposito` |
| Stock quantity | `saldo_estoque.quantidade` |
| Material document | `movimento_estoque` (+ itens se precisar) |

**Regra de ouro:** saldo **nunca** é editado na mão na UI. Só via movimento (como documento de material no SAP).

---

## Tabelas (schema do tenant)

```sql
CREATE TABLE deposito (
    id            BIGSERIAL PRIMARY KEY,
    codigo        VARCHAR(32) NOT NULL,
    nome          VARCHAR(120) NOT NULL,
    ativo         BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em     TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_deposito_codigo UNIQUE (codigo)
);

-- Seed sugerido: ('PADRAO', 'Depósito padrão')

CREATE TABLE saldo_estoque (
    id            BIGSERIAL PRIMARY KEY,
    produto_id    BIGINT NOT NULL REFERENCES produto(id),
    deposito_id   BIGINT NOT NULL REFERENCES deposito(id),
    quantidade    NUMERIC(15,4) NOT NULL DEFAULT 0,
    versao        BIGINT NOT NULL DEFAULT 0,  -- lock otimista
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_saldo_produto_deposito UNIQUE (produto_id, deposito_id),
    CONSTRAINT ck_saldo_qtd CHECK (quantidade >= 0)
);

CREATE TABLE movimento_estoque (
    id              BIGSERIAL PRIMARY KEY,
    tipo            VARCHAR(20) NOT NULL,  -- ENTRADA | SAIDA | AJUSTE | TRANSFERENCIA
    produto_id      BIGINT NOT NULL REFERENCES produto(id),
    deposito_id     BIGINT NOT NULL REFERENCES deposito(id),
    deposito_destino_id BIGINT REFERENCES deposito(id), -- só TRANSFERENCIA
    quantidade      NUMERIC(15,4) NOT NULL,
    custo_unitario  NUMERIC(15,2),
    documento_ref   VARCHAR(64),   -- NF, pedido, inventário…
    motivo          VARCHAR(80),
    usuario_id      BIGINT,
    criado_em       TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_mov_tipo CHECK (tipo IN ('ENTRADA','SAIDA','AJUSTE','TRANSFERENCIA')),
    CONSTRAINT ck_mov_qtd CHECK (quantidade > 0)
);

CREATE INDEX ix_mov_produto_criado ON movimento_estoque (produto_id, criado_em DESC);
CREATE INDEX ix_saldo_produto ON saldo_estoque (produto_id);
```

---

## Regras de negócio (MVP)

1. Só movimenta se `produto.controla_estoque = true`.
2. **ENTRADA / AJUSTE+** → soma saldo (AJUSTE com sinal: preferir tipo SAIDA/ENTRADA ou campo `sinal` — MVP: AJUSTE informa `quantidade` e `sentido` IN/OUT no service).
3. **SAIDA** → subtrai; se `quantidade > saldo` → `EstoqueInsuficienteException` ([[erp-transacao-dominio]]).
4. **TRANSFERENCIA** → mesma transação: −origem +destino; falha = rollback total.
5. Atualizar `saldo_estoque` com **lock otimista** (`versao`) ou `SELECT … FOR UPDATE` na linha do saldo.
6. Movimento é **append-only** (não UPDATE/DELETE de histórico; estorno = novo movimento inverso).

### Fronteira @Transactional

Qualquer service que altera saldo + grava movimento = **um** `@Transactional` no service de aplicação (ex. `EstoqueMovimentoService.lancar`).  
Se vier de venda/NF: o service de cima (Venda/Nota) abre a transação e chama estoque — ver exemplo em [[erp-transacao-dominio]].

---

## APIs (REST mínimo)

| Método | Rota | Nota |
|--------|------|------|
| GET | `/api/estoques?produtoId=&depositoId=` | Saldos |
| GET | `/api/estoques/movimentos?produtoId=&de=` | Extrato |
| POST | `/api/estoques/movimentos` | Body: tipo, produto, depósito, qtd, motivo… |

Permissões: `estoque:consultar`, `estoque:movimentar` (e separar ajuste se quiser).

---

## Telas ([[erp-ui-telas]])

| Tela | Floorplan | Conteúdo |
|------|-----------|----------|
| Saldos | List Report | Produto, depósito, qtd · filtro · alerta baixo (opcional `minimo` no PRD) |
| Extrato | List Report / Object | Movimentos do produto |
| Novo movimento | Object Page ou dialog | Tipo + qtd + motivo · confirmação se SAIDA/AJUSTE |
| Transferência | Form curto | Origem, destino, qtd · confirmação |

---

## Extensões típicas no PRD (por cliente)

- Baixa na **venda** vs na **NF de saída**
- Estoque mínimo / ponto de pedido
- Lote / validade
- Multi-depósito obrigatório
- Custo médio móvel a cada entrada (MAP do SAP)

## Queries RAG

```
rag_buscar("erp modulo estoque")
rag_buscar("erp transacao atomica")
buscar_historico("movimento estoque goods movement")
```

## Links

- [[erp-modulo-produto]] · [[erp-ui-telas]] · [[erp-transacao-dominio]] · [[erp-postgres-schema]] · [[erp-agente-modo-cursor]]
- SAP Goods Movements / Inventory Management (conceitual): learning.sap.com

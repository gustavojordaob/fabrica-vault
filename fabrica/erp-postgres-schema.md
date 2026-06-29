---
tags:
  - fabrica
  - erp
  - postgresql
  - schema
  - banco
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — convenções de schema Postgres (padrão fábrica)

> PostgreSQL 18. Consultar `rag_buscar("erp postgres schema convencao")` antes de
> criar tabela ou migration.

## Nomenclatura

| Item | Padrão | Exemplo |
|------|--------|---------|
| Tabela | singular, snake_case | `pedido`, `item_pedido`, `conta_pagar` |
| Coluna | snake_case | `cliente_id`, `criado_em`, `valor_total` |
| PK | `id` | `id BIGSERIAL PRIMARY KEY` |
| FK | `<entidade>_id` | `cliente_id`, `produto_id` |
| Índice | `ix_<tabela>_<colunas>` | `ix_pedido_cliente_id` |
| Unique | `uq_<tabela>_<colunas>` | `uq_cliente_cnpj` |
| Schema tenant | `tenant_<slug>` | `tenant_acme` |

---

## Tipos canônicos (não negociável)

| Dado | Postgres | NUNCA usar |
|------|----------|------------|
| Dinheiro / valor | `numeric(15,2)` | ❌ `money`, `float`, `real`, `double` |
| Quantidade fracionada | `numeric(15,4)` | ❌ float |
| Data + hora | `timestamptz` | ❌ `timestamp` sem tz |
| Data | `date` | |
| Texto curto | `varchar(n)` com n real | ❌ `text` pra tudo |
| Texto livre/grande | `text` | |
| Booleano | `boolean` | ❌ char('S'/'N') |
| Identificador externo | `uuid` (se precisar) | |
| Enum de domínio | `varchar` + check, ou tabela de domínio | ❌ enum nativo do PG (difícil migrar) |

> `money` do Postgres é problemático (depende de locale). Sempre `numeric` pra fiscal.

---

## Colunas de auditoria (toda tabela)

```sql
CREATE TABLE pedido (
    id          BIGSERIAL PRIMARY KEY,
    cliente_id  BIGINT NOT NULL REFERENCES cliente(id),
    status      VARCHAR(20) NOT NULL,
    valor_total NUMERIC(15,2) NOT NULL DEFAULT 0,
    versao      BIGINT NOT NULL DEFAULT 0,        -- @Version (lock otimista)
    criado_em   TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_pedido_status CHECK (status IN ('RASCUNHO','CONFIRMADO','CANCELADO'))
);

CREATE INDEX ix_pedido_cliente_id ON pedido(cliente_id);
```

---

## Integridade referencial — use de verdade

- **Sempre FK** entre entidades relacionadas. O banco é a última linha de defesa contra dado órfão (num ERP isso é dinheiro/fiscal).
- **`ON DELETE`** explícito: `RESTRICT` por padrão (não deixa apagar com filho), `CASCADE` só onde o filho não existe sem o pai (ex: `item_pedido` → `pedido`).
- **Check constraints** pra invariantes simples (status válido, valor ≥ 0). Não confie só na app.

---

## Multi-tenant: o tenant é o schema, não a coluna

No nosso modelo (schema-por-tenant), **as tabelas NÃO têm `tenant_id`**. O isolamento
é o schema. `tenant_acme.pedido` e `tenant_xyz.pedido` são tabelas fisicamente
separadas. Isso simplifica as queries (sem filtro de tenant em todo `WHERE`).

Exceção: o schema `master` tem a tabela `tenant` (catálogo). Ver [[erp-migrations-flyway]].

---

## Índices — onde colocar

- Toda **FK** ganha índice (Postgres não cria automático).
- Colunas usadas em **filtro frequente** (status, data, cliente).
- **Índice composto** na ordem dos filtros mais seletivos primeiro.
- Não encha de índice: cada um custa em escrita. ERP escreve muito.

---

## O que NUNCA fazer

- ❌ **`float`/`double`/`money` pra valor monetário.** Sempre `numeric(15,2)`.
- ❌ **`timestamp` sem timezone.** Sempre `timestamptz`.
- ❌ **Tabela sem FK** "pra ir mais rápido". Dado órfão em ERP é prejuízo.
- ❌ **Adicionar `tenant_id` nas tabelas** — no nosso modelo o tenant é o schema.
- ❌ **Enum nativo do Postgres** pra status que muda — varchar + check é mais fácil de evoluir.
- ❌ **FK sem índice** — query de join fica lenta conforme cresce.

---

## Golden set sugerido

```
{"id":"erp-pg-01","query":"qual tipo postgres para dinheiro no erp","esperado_nota":"erp-postgres-schema.md","tipo":"padrao"}
{"id":"erp-pg-02","query":"as tabelas do erp tem tenant_id","esperado_nota":"erp-postgres-schema.md","tipo":"padrao"}
{"id":"erp-pg-03","query":"convencao de nome de tabela coluna fk erp","esperado_nota":"erp-postgres-schema.md","tipo":"padrao"}
```

## Links
- [[erp-stack]] · [[erp-multitenancy-spring]] · [[erp-transacao-dominio]] · [[erp-migrations-flyway]]

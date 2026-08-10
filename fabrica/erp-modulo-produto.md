---
tags:
  - fabrica
  - erp
  - modulo
  - produto
  - material-master
  - sap
atualizado_em: 2026-08-05
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. `rag_buscar("erp agente modo cursor")` → [[erp-agente-modo-cursor]]
> 2. `rag_buscar("erp ui telas")` → [[erp-ui-telas]]
> 3. `rag_buscar("erp modulo produto")` → **esta nota**
> 4. `rag_buscar("erp postgres schema")` + MCP postgres
> 5. Cliente diverge? → PRD do produto sobrescreve (campos, UOM, grades…)
>
> **Baseline da fábrica — não é o ERP de um cliente.**  
> Escopo MVP: [[../projetos/erp-baseline-prd]] (v1). UI e mensagens em **português (Brasil)**.  
> Fontes conceituais: **SAP Material Master (MM)** + práticas comuns Odoo Product. Simplificado para Angular/Spring/Postgres da fábrica.

# ERP — módulo canônico: Produto (Material Master mínimo)

No SAP, o **Material Master** é a fonte central de dados do material (compras, estoque, vendas, contábil). Aqui reduzimos ao **MVP de cadastro** que todo ERP da fábrica precisa.

## Escopo MVP (fábrica)

| Inclui | Não inclui (deixar pro PRD / fase 2) |
|--------|--------------------------------------|
| Cadastro de produto/SKU | MRP, planejamento de compra |
| Código, nome, UOM, ativo | Grades (cor/tamanho) complexas |
| Controle se movimenta estoque | Lote/série obrigatórios |
| Custo de referência (numeric) | Valuation class / razão contábil SAP |
| Soft delete / inativação | Multi-planta com preço por planta |

---

## Conceitos (mapeamento SAP → fábrica)

| SAP MM | Nossa tabela / ideia |
|--------|----------------------|
| Material | `produto` |
| Material number | `codigo` (único no tenant) |
| Base unit of measure | `unidade` (UN, KG, CX…) |
| Material type (simplificado) | `tipo` opcional: `MERCADORIA`, `SERVICO`, `INSUMO` |
| Plant / Storage location | Fase 2 → ver [[erp-modulo-estoque]] (`deposito`) |
| Standard / Moving average price | MVP: `custo_medio` ou `custo_padrao` (um só no início) |

---

## Tabelas (schema do tenant)

Convenções: [[erp-postgres-schema]].

```sql
CREATE TABLE produto (
    id              BIGSERIAL PRIMARY KEY,
    codigo          VARCHAR(64) NOT NULL,
    nome            VARCHAR(200) NOT NULL,
    descricao       TEXT,
    unidade         VARCHAR(10) NOT NULL DEFAULT 'UN',
    tipo            VARCHAR(20) NOT NULL DEFAULT 'MERCADORIA',
    controla_estoque BOOLEAN NOT NULL DEFAULT TRUE,
    custo_padrao    NUMERIC(15,2) NOT NULL DEFAULT 0,
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    versao          BIGINT NOT NULL DEFAULT 0,
    criado_em       TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em   TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_produto_codigo UNIQUE (codigo),
    CONSTRAINT ck_produto_tipo CHECK (tipo IN ('MERCADORIA','SERVICO','INSUMO')),
    CONSTRAINT ck_produto_custo CHECK (custo_padrao >= 0)
);

CREATE INDEX ix_produto_nome ON produto (nome);
CREATE INDEX ix_produto_ativo ON produto (ativo);
```

### Regras de dados

- `SERVICO` → em geral `controla_estoque = false` (não gera movimento).
- **Não apagar** produto com movimento/pedido: `ativo = false` (inativação).
- `codigo` imutável após primeiro movimento (ou só com permissão admin — definir no PRD).

---

## APIs (REST mínimo)

| Método | Rota | Permissão |
|--------|------|-----------|
| GET | `/api/produtos?q=&ativo=` | `produto:listar` |
| GET | `/api/produtos/{id}` | `produto:listar` |
| POST | `/api/produtos` | `produto:criar` |
| PUT | `/api/produtos/{id}` | `produto:editar` |
| POST | `/api/produtos/{id}/inativar` | `produto:editar` |

DTO na borda (records) — [[erp-spring-camadas]]. Nunca expor entidade JPA.

---

## Telas ([[erp-ui-telas]])

| Tela | Floorplan | Conteúdo |
|------|-----------|----------|
| Lista | List Report | Filtro: busca, ativo, tipo · colunas: código, nome, UOM, custo, ativo |
| Detalhe/Form | Object Page | Criar / editar / visualizar · inativar com confirmação |

Permissões UI: esconder Novo/Editar/Inativar conforme claims ([[erp-auth-login]]).

---

## O que o cliente sobrescreve no PRD

- Campos fiscais (NCM, CFOP default)
- Grade / variantes
- Multi-empresa preço
- Integração e-commerce

## Queries RAG

```
rag_buscar("erp modulo produto")
rag_buscar("erp ui telas")
buscar_historico("produto material master")
```

## Links

- [[erp-modulo-estoque]] · [[erp-ui-telas]] · [[erp-postgres-schema]] · [[erp-transacao-dominio]] · [[erp-agente-modo-cursor]]
- SAP Material Master (conceitual): learning.sap.com / SAP Press Material Master

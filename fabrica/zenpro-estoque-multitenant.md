---
tags:
  - zenpro
  - estoque
  - multitenant
  - firestore
atualizado_em: 2026-07-15
repo: C:/Users/gusta/projetos/zenpro
---

# Zen Pro — estoque (loja oficial)

> **Agente Cursor — use MCP antes de codar**
>
> - `rag_buscar("zenpro estoque loja central")`
> - `buscar_historico("estoque zenpro")`
>
> PROJECT: [[../projetos/zenpro-project]]

## Modelo atual (15/07/2026)

- **Só a marca** gerencia estoque (`Admin → Estoque`), na loja oficial `zenpro`.
- **Revendedor** não aloca estoque nem vê Estoque no admin — compra no `/revendedor` e acompanha vendas no dash/pedidos.
- Site B2C `/` e portal B2B usam `lojas/zenpro/estoque`.

## Camadas (sync)

```
produtos/{produtoId}.estoqueCentral
lojas/zenpro/estoque/{produtoId}.quantidade
```

Salvar em Estoque (ou quantidade no form de produto) atualiza **as duas**.

```
disponivel = min(estoqueCentral, estoqueLojaZenPro)
```

**Bug corrigido:** catálogo em `/` chama `listarProdutosLojaAtivos` sem `lojaId` → tratava loja como 0 → “Esgotado”. Agora default = `MARCA_LOJA_ID`.

Cases `personalizavel: true`: sem controle numérico (sob encomenda).

## Checklist

- [ ] Admin marca → Estoque → salvar quantidade
- [ ] Site `/` mostra disponível (não esgotado)
- [ ] Nav revendedor sem link Estoque
- [ ] Guard bloqueia `/admin/estoque` para revendedor

# Zen Pro — portal B2B do revendedor

> **Agente Cursor — use MCP antes de codar**
> - `rag_buscar("zenpro revendedor b2b portal faixas")`
> - `buscar_historico("zenpro site revendedor")`

**Repo:** `C:/Users/gusta/projetos/zenpro`

## Modelo

| Canal | URL | Preço | Quem acessa |
|-------|-----|-------|-------------|
| B2C | `/` | `precoBaseCentavos` | Público |
| B2B | `/revendedor` | faixas / `precoRevendedorCentavos` | `papel === "revendedor"` (marca também inspeciona) |

Pedidos B2B → `lojas/zenpro/pedidos` com `canal: "revendedor_b2b"`.

## Acesso (anti-bounce)

- `PapelUsuarioProvider`: `papelResolvido` — não decidir acesso antes de ler Firestore
- `RevendedorB2BGuard`: espera papel; sem redirect para `/?aviso=somente-revendedor`
- `EntrarComoRevendedorLink`: logado → `/revendedor` (nunca aviso enquanto carrega)
- Header/AuthLink: botão **Admin** / **Painel admin** se `podeAcessarPortalRevendedor`

## Níveis + benefícios no checkout

- Config: `lojas/zenpro.config.niveisRevendedor`
- Volume = compras pagas na Zen Pro (B2B + reposição)
- Carrinho/checkout B2B: `useBeneficiosCheckoutB2b` aplica `% desconto` e mostra frete grátis
- Pedido grava `beneficioNivel` + `totalCentavos` já com desconto

## Ranking admin (Revendedores)

- Filtros: Semana (input `type=week`) | Mês (input `type=month`) | Ano | Total
- Filtro por vendedor (select)
- Semana/mês específicos: `rankingRevendedoresNoIntervalo` / `rankingRevendedoresNoMes`

## Produto (Firestore)

- `precoRevendedorCentavos` — obrigatório no cadastro
- `pedidoMinimoRevendedorCentavos` — mínimo da linha (qty × unitário)
- `faixasPrecoRevendedor: { quantidadeMin, quantidadeMax|null, precoCentavos }[]`

Helper: `src/features/revendedor/precoRevendedorFaixas.ts`

## Checklist próximo app / mudança

- [ ] Guard + banner “site do revendedor”
- [ ] Rewrites hosting antes do `/*` catch-all
- [ ] Carrinho com `quantidade` + recalcular faixa
- [ ] Preview: clip moldura arredondada (não canvas 9:16)
- [ ] Esperar papel no guard (sem race com aviso)
- [ ] Benefícios do nível no checkout B2B
- [ ] Ranking com mês + vendedor

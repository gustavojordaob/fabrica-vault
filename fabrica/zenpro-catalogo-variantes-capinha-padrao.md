# Zen Pro — catálogo dinâmico: modelo × variante (material)

> **Agente Cursor — use MCP antes de codar**
> - `rag_buscar("zenpro catalogo variantes capinha material")`
> - `buscar_historico("personalizacao produto modelo")`

**Repo:** `C:/Users/gusta/projetos/zenpro`

## Problema

Precisamos vender **várias capinhas** (couro, silicone, acrílico…) para **vários celulares**, cada uma com **preço próprio**, sem hardcodar no front.

## Arquitetura (3 camadas)

| Camada | Firestore | Responsabilidade |
|--------|-----------|------------------|
| **Aparelho** | `modelos/{id}` | Geometria, máscara PNG, overlay, dimensões, `personalizacao.corAparelho` |
| **Variante (SKU)** | `produtos/{id}` | Nome, preço, `material`, `personalizavel`, `modelosCompativeis[]`, opcional `visualPersonalizacao` |
| **Visual runtime** | código | `resolverVisualPersonalizacao()` — produto > modelo > SPECS em `caseFrame.ts` / `cameraModules.ts` |

## Fluxo loja → editor

1. Vitrine: `listarProdutosPersonalizaveisAtivos()` → **1 card por produto** (não expande por modelo).
2. Card → `/produto?id={produtoId}` (ou `/{slug}/produto?id=`).
3. Página do produto: botões com `modelosCompativeis` → **Personalizar** → `/personalizar?modelo=&produto=`.
4. `carregarContextoPersonalizacao(modeloId, produtoId)` → modelo + produto + visual resolvido.
5. `PersonalizacaoVisualProvider` envolve editor/preview.
6. Carrinho salva `produtoId`, `material`, `precoCentavos` na personalização.

Arquivos: `src/app/produto/ProdutoPageClient.tsx`, `useLojaPaths().produto`.

## Arquivos-chave

- `src/features/catalogo/personalizacaoVisual.ts` — resolver + tipos Firestore
- `src/features/catalogo/personalizacaoContext.ts` — contexto do editor
- `src/features/catalogo/materiaisCapinha.ts` — lista de materiais (admin)
- `src/features/loja/catalogoProdutos.ts` — vitrine dinâmica
- `src/features/personalizacao/PersonalizacaoVisualContext.tsx` — React context

## Admin — como adicionar

### Novo celular
1. Admin → Modelos → máscara + overlay + dimensões
2. (Opcional) cor do aparelho no mock 2D
3. (Opcional) overrides em `personalizacao` no Firestore

### Nova variante de capinha
1. Admin → Produtos → marcar **personalizável**
2. Escolher **material** e **preço**
3. Selecionar **modelos compatíveis** (pode ser vários aparelhos no mesmo SKU)

## Seed de exemplo

Três variantes iPhone 17 Pro Max no mock/seed:
- `cap-iphone17-couro` — R$ 89,90
- `cap-iphone17-silicone` — R$ 49,90
- `cap-iphone17-acrilico` — R$ 64,90

Rodar: `npm run seed:multitenant` (ou script equivalente no repo).

## Checklist — copiar para próximo app de capinha

- [ ] `modelos/` com mask + overlay por aparelho
- [ ] `produtos/` personalizáveis com `material` + `modelosCompativeis[]`
- [ ] URL `?modelo=&produto=` no editor
- [ ] Carrinho/pedido persiste `produtoId` + preço da variante
- [ ] SPECS fallback em código só para dev/offline
- [ ] `PersonalizacaoVisualProvider` no fluxo de edição

## Dimensões do modelo → aspecto da capa + molde na produção

*Atualizado em 02/07/2026*

> **Agente Cursor — use MCP antes de codar:** `rag_buscar("zenpro capinha dimensao aspecto mascara molde exportCaseArt getCaseLayout")` + `buscar_historico("zenpro capinha mascara molde")`.

## Como funciona

A proporção da capa deriva de `larguraPx × alturaPx` do modelo (`modelos/{id}`). Base compartilhada: `getCaseLayout(280, larguraPx, alturaPx)` → `molduraW=280` fixo, `molduraH` proporcional. Usada IGUAL em CaseEditor, CasePreview, PreviewCapaModal e exportCaseArt. Como molduraW é sempre 280, o `transform` salvo mapeia 1:1 em qualquer aspecto.

## Molde (máscara) por modelo

- Admin sobe `maskUrl` (molde PNG) por modelo no form de modelos.
- `resolverVisualPersonalizacao(modeloId, { assets: { larguraPx, alturaPx, maskUrl } })` retorna larguraPx/alturaPx/maskUrl no ResolvedPersonalizacaoVisual.
- exportCaseArt recorta a arte com `opts.maskUrl` (fallback máscara iPhone).
- **Canvas taint:** máscara remota (Storage) via `loadImageForCanvasExport` (fetch→blob→objectURL), nunca img.crossOrigin cru, senão toDataURL quebra.

## Persistência

Personalizacao e ConfigPersonalizacaoMascaraModelo ganharam larguraPx/alturaPx/maskUrl. personalizacaoParaConfig grava; personalizacaoDeFirestore lê. Carrinho/checkout/admin passam dims por props ao CasePreview (fora do provider).

## Checklist p/ próximo app de capinha

1. Modelo com larguraPx/alturaPx reais + maskUrl (molde).
2. Base única getCaseLayout(280, larguraPx, alturaPx) em editor/preview/export.
3. Persistir dims+mask na personalização; previews fora do provider recebem via props.
4. Máscara de produção sempre via loadImageForCanvasExport (evita taint).

---

---
projeto: Zen Pro
tipo: referencia-tecnica
stack: Next.js 16 (static export) + Firebase
firebase: zenpro-capinhas
hosting: https://usezenpro.com.br
hosting_alias: https://zenpro-capinhas.web.app
repo: C:/Users/gusta/projetos/zenpro
atualizado_em: 2026-07-27
links:
  - "[[../fabrica/capinhas-personalizacao]]"
  - "[[../fabrica/zenpro-catalogo-variantes-capinha-padrao]]"
  - "[[../fabrica/zenpro-estoque-multitenant]]"
  - "[[../fabrica/zenpro-personalizacao-rockb2b]]"
---

# Zen Pro — PROJECT (referência técnica)

> **Fonte de verdade:** esta nota + docs em `zenpro/docs/` e `obsidian/fabrica/`.  
> O `CLAUDE.md` no repo Git é só **ponte** para a fábrica.

---

## Visão rápida

E-commerce de **cases personalizadas** com multitenant: marca Zen Pro vende na raiz (`/`) e revendedores em `/{slug}`.

| Público | Onde compra | Pedidos em |
|---------|-------------|------------|
| Cliente final | `/` ou `/{slug}` | `lojas/{lojaId}/pedidos` |
| Marca (dona) | Admin + loja oficial | `lojas/zenpro/pedidos` |
| Revendedor | `/{slug}` + admin | `lojas/{lojaId}/pedidos` |

### Catálogo capas prontas (jul/2026)

Linha **Brave / Smart / MagSafe** (20 SKUs) em `produtos/` — sem imagens ainda; upload no admin. Preços R$ 199,90 (Brave/Smart) e R$ 249,90 (MagSafe). **`modelosCompativeis` por SKU** espelha as variações reais da OBLI (ex.: Rosa = só 17; Desert = 16 Pro/Max; Brave Cinza ≠ Brave Azul). Página `/produto?id=`. Seed: `scripts/seed-capas-pronta-catalogo.ts`.

### Mock formato H5 (iPhone — jul/2026)

Além da câmera, silhueta do aparelho vem do contorno externo RockB2B (`bodyMaskUrl` + `molduraAspect`). Script: `process-rockb2b-body-masks.mjs --only=iphone`. Fake 3D usa `mask-image`; preview Konva usa `destination-in`.

---

## Stack

- **Frontend:** Next.js 16, `output: export`, Konva (editor)
- **Firebase:** Auth, Firestore, Storage, Hosting, Functions (`us-central1`)
- **Pagamentos:** Mercado Pago Checkout Pro — preference **restringe** à forma escolhida (PIX só PIX; cartão Nx; boleto). Desconto PIX / max parcelas: `lojas.config.pagamentoPadrao` + override em `produtos.pagamento` (0/null = herda loja). Docs: `docs/mercadopago-zenpro.md`
- **NF:** Focus NFe (opcional, fila automática após pagamento)
- **Rastreio:** manual no admin hoje; Melhor Envio = próximo passo

---

## Lojas e estoque (importante)

A marca **também é uma loja** no Firestore: `lojas/zenpro`.

| Camada | Onde | Quem edita |
|--------|------|------------|
| **Estoque central** | `produtos/{id}.estoqueCentral` | Marca em **Admin → Produtos** |
| **Estoque na loja** | `lojas/{lojaId}/estoque/{produtoId}` | Marca em **Admin → Estoque** (por loja) |
| **Disponível venda** | `min(central, estoqueLoja)` | Calculado — produtos personalizáveis = sob encomenda |

**Admin → Estoque:** dropdown inclui **Zen Pro (loja oficial)** + revendedores. Padrão ao abrir = loja oficial.

Pedidos da home (`/`) gravam em `lojas/zenpro/pedidos`.

---

## Coleções Firestore (principais)

| Coleção | Uso |
|---------|-----|
| `produtos`, `modelos_celular`, `tipos`, `marcas`, `modelos` | Catálogo central (marca escreve) |
| `lojas/{lojaId}` | Marca + revendedores (`slug`, `config`, `donoUid`) |
| `lojas/{lojaId}/pedidos` | Pedidos por loja |
| `lojas/{lojaId}/estoque` | Quantidade alocada por loja |
| `usuarios/{uid}` | Perfil cliente + `papel` marca\|revendedor |
| `pedidos_reposicao` | Reposição B2B revendedor → marca |
| `notas_fiscais_outbox` | Fila emissão NF |
| `emails_outbox` | E-mails automáticos (aprovação revendedor) |

---

## Cloud Functions

| Função | Status |
|--------|--------|
| `gerarFotoCriativaIA` | Deployada |
| `processarEmailOutbox` | Pronta |
| `decrementarEstoquePedidoLoja` | Pronta (mock/presencial no create; MP no webhook) |
| `criarCheckoutMercadoPago` | Código pronto — precisa `MP_ACCESS_TOKEN` |
| `webhookMercadoPago` | Código pronto — cadastrar URL no painel MP |
| `processarNotaFiscalOutbox` | Código pronto — precisa `FOCUS_NFE_*` |
| Melhor Envio | Não implementado |

---

## Admin (marca)

| Rota | Função |
|------|--------|
| `/admin/produtos` | Catálogo + **estoque central** |
| `/admin/estoque` | Estoque **por loja** (zenpro + revendedores) |
| `/admin/pedidos` | Pedidos multitenant |
| `/admin/reposicao` | Reposição B2B |
| `/admin/revendedores` | CRUD revendedores |
| `/admin/modelos` | Modelos de celular + preset câmera |

**Admin → Produtos (jul/2026):** paginação client-side (`PaginationBar`) + checkbox por linha, seleção da página inteira e **exclusão em lote**.

---

## Loja pública

| Rota | Função |
|------|--------|
| `/` | Home marca |
| `/personalizar` | Editor case |
| `/produto?id=` | Página do produto + seletor de modelos (iPhone) |
| `/checkout` | Pagamento MP |
| `/meus-pedidos` | Status + rastreio + NF |
| `/{slug}/*` | Loja revendedor (mesmas telas) |

### Listagens da loja (jul/2026)

| Seção | Filtros | Paginação |
|-------|---------|-----------|
| `PersonalizarSection` | Busca, marca, **modelo (todo o catálogo, não só o que tem produto)**, material, ordenação | `PaginationBar` |
| `ProdutosSection` | Busca, categoria, ordenação | `PaginationBar` |

`src/components/ui/PaginationBar.tsx` é compartilhado (loja + admin): `fatiaPagina`, `totalPaginasDe`, `numerosVisiveis`. Trocar filtro/ordenação reseta para a página 1.

### Preview da personalização

Modal “Ver na case” = **vista frontal** (`CasePreview`). Câmera do mock em tom branco/prata. Detalhes em `fabrica/zenpro-personalizacao-rockb2b.md`.

---

## Documentação

| Onde | Conteúdo |
|------|----------|
| `zenpro/docs/mercadopago-zenpro.md` | Pagamentos MP |
| `zenpro/docs/nota-fiscal-rastreio-automatico.md` | NF + rastreio |
| `zenpro/docs/multitenant-fundacao.md` | Fundação multitenant |
| `fabrica/zenpro-estoque-multitenant.md` | Estoque central vs por loja |
| `fabrica/capinhas-personalizacao.md` | Editor Konva |
| `fabrica/decisoes.md` | Filtrar "zenpro" |

---

## Maturidade (jul/2026)

| Área | % |
|------|---|
| Loja + personalização | ~90 (filtros, paginação, preview na capinha) |
| Admin + catálogo | ~92 (paginação + exclusão em lote) |
| Pagamentos MP | ~70 (código ok, falta config prod) |
| NF automática | ~50 (fila ok, falta Focus) |
| Rastreio automático | ~30 (manual) |

---

## RAG obrigatório

Antes de codar: `rag_buscar("zenpro …")` + `buscar_historico`  
Após decisão: `salvar_decisao` + `indexar_rapido.py`

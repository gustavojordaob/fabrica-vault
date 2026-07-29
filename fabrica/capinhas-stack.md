---
tags:
  - fabrica
  - capinhas
  - stack
  - nextjs
  - firebase
  - ecommerce
atualizado_em: 2026-07-01
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# Capinhas — stack e arquitetura (padrão fábrica)

> Projeto NOVO: loja web de capinhas personalizadas. Cliente sobe foto e alinha
> na capinha, compra. Consultar `rag_buscar("capinhas stack")` antes de codar.
> NÃO é app mobile (sem Expo). NÃO é a stack ERP (sem Spring/Postgres).

## O que o produto é (em fatias)

1. **Loja** — catálogo de capinhas + modelos de celular + carrinho + checkout.
2. **Personalização** — sobe foto, arrasta/zoom/posiciona na capinha, preview. Ver [[capinhas-personalizacao]].
3. **Revendedores + painel admin** (multi-tenant) — **FASE 2, não agora.**
4. **NF + fiscal** — via emissor externo (Focus NFe / eNotas), **última fatia.**

> Foco atual: **Fatia 1 + 2** (loja + personalização), sem admin. É a demo pro cliente.

## Stack FIXA

| Camada | Escolha | Observação |
|--------|---------|------------|
| **Framework** | **Next.js** (App Router) | web SSR, bom pra e-commerce + SEO |
| **Linguagem** | TypeScript | |
| **Auth** | Firebase Auth | email/senha + Google |
| **Banco** | Firestore | produtos, pedidos, personalizações |
| **Arquivos** | Firebase Storage | fotos que o cliente sobe |
| **Pagamento** | Mercado Pago | já dominado (Cortejo/LashMatch) |
| **Estilo** | Tailwind CSS | |
| **Preview capinha** | Canvas / SVG no browser | sem processamento no servidor |
| **Deploy** | Vercel ou Firebase Hosting | |
| **NF (fase 4)** | Focus NFe / eNotas (integração) | NÃO emitir NF-e próprio |

## Estrutura do projeto

```
capinhas/
├── src/
│   ├── app/                     ← Next.js App Router
│   │   ├── page.tsx             ← home/vitrine
│   │   ├── produtos/            ← catálogo
│   │   ├── personalizar/[modelo]/ ← EDITOR (foto + ajuste) — o "uau"
│   │   ├── carrinho/
│   │   ├── checkout/
│   │   └── api/                 ← rotas server (webhook MP, criar pagamento)
│   ├── lib/
│   │   ├── firebase.ts          ← init (auth, firestore, storage)
│   │   └── mercadopago.ts
│   ├── components/
│   └── features/
│       ├── loja/
│       └── personalizacao/      ← editor de capinha
└── ...
```

## Firestore — coleções (fase 1)

```
modelos_celular/{id}        → { marca, modelo, template_url, area_util, area_camera }
produtos/{id}               → { nome, tipo, preco, imagens[], ativo }
personalizacoes/{id}        → { foto_url, modelo_id, transform:{x,y,scale,rotation}, criado_em }
pedidos/{id}                → { itens[], total, status, cliente, pagamento_id, criado_em }
```

> Fase 1 é **single-tenant** (uma loja só). Multi-tenant (revendedores) é Fase 2 —
> quando chegar lá, provavelmente `lojas/{lojaId}/...` ou schema por revendedor.
> NÃO desenhar multi-tenant agora; adia complexidade.

## Ordem de construção (para mostrar rápido)

| Passo | O quê | Por quê primeiro |
|-------|-------|------------------|
| 1 | **Editor de personalização** (sobe foto, ajusta, preview) | é o diferencial; demo que vende |
| 2 | Catálogo + página de modelo | contexto do editor |
| 3 | Carrinho + checkout Mercado Pago | fechar a venda |
| 4 | Auth (login/cadastro cliente) | pode vir depois do fluxo de compra |
| — | Admin/revendedor, NF | FASE 2, não agora |

## O que NÃO fazer (agora)

- ❌ Expo / React Native — é web, Next.js.
- ❌ Stack ERP (Spring/Postgres) — é outro projeto.
- ❌ Multi-tenant / painel revendedor — Fase 2.
- ❌ Emitir NF-e próprio — integrar emissor, e só na fase 4.
- ❌ Processar imagem no servidor — o ajuste é no browser (canvas/SVG).
- ❌ Construir loja inteira antes de validar o editor com o cliente.

## Golden set sugerido

```
{"id":"cap-stack-01","query":"qual stack do projeto de capinhas web","esperado_nota":"capinhas-stack.md","esperado_secao":null,"tipo":"padrao"}
{"id":"cap-stack-02","query":"capinhas usa expo ou next js","esperado_nota":"capinhas-stack.md","esperado_secao":null,"tipo":"padrao"}
{"id":"cap-stack-03","query":"ordem de construir a loja de capinhas","esperado_nota":"capinhas-stack.md","esperado_secao":null,"tipo":"fluxo"}
```

## Links
- [[capinhas-personalizacao]]

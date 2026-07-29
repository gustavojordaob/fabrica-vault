---
tags:
  - fabrica
  - capinhas
  - multitenant
  - revendedores
  - firestore
  - security-rules
atualizado_em: 2026-07-01
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# Capinhas — arquitetura multi-tenant / revendedores (padrão fábrica)

> Rede de revendedores: a MARCA é dona no topo, cada revendedor é uma LOJA isolada
> com URL própria. Consultar `rag_buscar("capinhas multitenant revendedor")` antes
> de mexer em loja, pedido, permissão ou regra de segurança. Ver [[capinhas-stack]].

## Modelo de negócio (o que define tudo)

| Papel | O que vê / faz |
|-------|----------------|
| **Marca (dono / admin master)** | vê TUDO: todas as lojas, todos os pedidos. Gerencia o catálogo central e os revendedores (cria, ativa, desativa). |
| **Revendedor (dono de uma loja)** | vê SÓ a própria loja e os próprios pedidos. Vende os produtos DA MARCA (não cria produtos). |
| **Cliente final** | compra no site de um revendedor via URL própria. Sem login de admin. |

Decisões-chave:
- **Produtos são CENTRAIS** (da marca). Revendedor NÃO cria produto — revende o catálogo.
- **Pedidos são POR LOJA** (isolados entre revendedores).
- **Cada revendedor tem URL própria** (slug): `site.com/{slug}`.
- **Marca vê tudo; revendedores são isolados entre si.**

## Schema Firestore

```
# CENTRAIS (da marca — todos os revendedores leem, só a marca escreve)
produtos/{produtoId}         → { nome, descricao, preco_base, imagens[], ativo }
modelos_celular/{modeloId}   → { marca, modelo, mask_url, overlay_url, ativo }

# POR LOJA (cada revendedor)
lojas/{lojaId}               → {
    nome, slug,              # slug = URL (site.com/{slug}), único
    dono_uid,                # uid do revendedor (Firebase Auth)
    ativo,
    config: { logo, cor, whatsapp, ... },
    # opcional: preco_ajuste / margem por loja
}
lojas/{lojaId}/pedidos/{id}  → {
    itens: [{ produtoId, modeloId, personalizacaoId, preco, qtd }],
    total, status,           # aguardando_pagamento | pago | producao | enviado
    cliente: { nome, contato, endereco },
    pagamento: { provider, id, status },
    criado_em
}

# PERSONALIZAÇÕES (a foto que o cliente montou)
personalizacoes/{id}         → { fotoUrl, modeloId, transform:{x,y,scale,rotation}, criado_em }
```

> Por que produtos centrais e não `lojas/{id}/produtos`: o revendedor vende o
> catálogo da marca. Duplicar produto em cada loja seria pesadelo de manutenção
> (mudou o preço → atualizar em N lojas). Central = uma fonte de verdade.

## Usuários e papéis

```
usuarios/{uid} → { nome, email, papel, lojaId? }
  papel: "marca"        → admin master (vê tudo)
  papel: "revendedor"   → dono de uma loja (lojaId aponta a loja dele)
```

- No login, lê `usuarios/{uid}` → descobre papel e lojaId.
- `marca` acessa /admin completo. `revendedor` acessa /admin restrito à lojaId dele.

## Roteamento por URL (o site do revendedor)

```
site.com/{slug}              → loja do revendedor (produtos centrais + branding da loja)
site.com/{slug}/personalizar/{modelo}
site.com/{slug}/carrinho
```

Fluxo: slug da URL → busca `lojas` where slug == {slug} → pega lojaId → renderiza a
loja daquele revendedor (catálogo central + config/branding da loja). O pedido nasce
com essa lojaId.

> Next.js: rota dinâmica `app/[slug]/...`. Resolver o slug no layout, disponibilizar
> lojaId via context para as páginas filhas.

## SEGURANÇA — o ponto que NÃO pode errar

O isolamento entre revendedores vive nas **Security Rules do Firestore**, NÃO só no
front. Filtrar por lojaId só no código = revendedor abre o console e vê pedido dos
outros. As regras são a autoridade.

```javascript
// firestore.rules (esboço)
function papel() {
  return get(/databases/$(database)/documents/usuarios/$(request.auth.uid)).data.papel;
}
function minhaLoja() {
  return get(/databases/$(database)/documents/usuarios/$(request.auth.uid)).data.lojaId;
}

match /produtos/{id} {
  allow read: if true;                       // catálogo público (loja mostra)
  allow write: if request.auth != null && papel() == 'marca';  // só a marca edita
}

match /lojas/{lojaId} {
  allow read: if true;                       // slug/branding público
  allow write: if request.auth != null &&
    (papel() == 'marca' || minhaLoja() == lojaId);

  match /pedidos/{pedidoId} {
    // marca vê tudo; revendedor só a própria loja
    allow read, write: if request.auth != null &&
      (papel() == 'marca' || minhaLoja() == lojaId);
  }
}
```

> Regra de ouro: **marca → tudo; revendedor → só `minhaLoja()`**. Todo acesso a
> pedido valida isso no servidor (rules), nunca confia no front.

## Pedido mostra a capinha personalizada

O revendedor (e a marca) veem, no pedido, como o cliente montou a capinha:
- O pedido referencia `personalizacaoId` → `{ fotoUrl, modeloId, transform }`.
- Renderizar com o MESMO componente do editor (foto + transform sobre a máscara do
  modelo). Ver [[capinhas-personalizacao]]. Componente reutilizável: editor E
  visualização de pedido usam o mesmo render.

## Ordem de construção (fatiado, revisar entre cada)

| Fatia | O quê |
|-------|-------|
| 1 | Schema + Security Rules (lojas, usuarios, papéis) — a FUNDAÇÃO |
| 2 | Auth + papéis: login que distingue marca vs revendedor |
| 3 | /admin da MARCA: CRUD produtos central + gerenciar lojas/revendedores |
| 4 | /admin do REVENDEDOR: ver seus pedidos (com a capinha personalizada) |
| 5 | Roteamento `/{slug}`: site público do revendedor |
| 6 | Pedido nasce com lojaId; marca vê todos, revendedor os seus |

## O que NUNCA fazer

- ❌ Filtrar lojaId só no front — isolamento vive nas Security Rules.
- ❌ Duplicar produtos por loja — catálogo é central da marca.
- ❌ Revendedor criar/editar produto — só a marca edita o catálogo.
- ❌ Pedido sem lojaId — todo pedido pertence a uma loja.
- ❌ Slug não-único — dois revendedores com mesma URL quebra o roteamento.
- ❌ Confiar no papel vindo do front — validar `usuarios/{uid}.papel` no servidor/rules.
- ❌ Renderizar capinha do pedido com código diferente do editor — reusar o componente.

## Golden set sugerido

```
{"id":"cap-mt-01","query":"como funciona multi tenant revendedor capinhas","esperado_nota":"capinhas-multitenant.md","esperado_secao":null,"tipo":"padrao"}
{"id":"cap-mt-02","query":"produtos sao por loja ou central da marca","esperado_nota":"capinhas-multitenant.md","esperado_secao":null,"tipo":"padrao"}
{"id":"cap-mt-03","query":"regra seguranca firestore isolar pedido revendedor","esperado_nota":"capinhas-multitenant.md","esperado_secao":null,"tipo":"solucao"}
{"id":"cap-mt-04","query":"url propria slug loja revendedor next js","esperado_nota":"capinhas-multitenant.md","esperado_secao":null,"tipo":"padrao"}
{"id":"cap-mt-05","query":"marca ve tudo revendedor ve so a loja dele","esperado_nota":"capinhas-multitenant.md","esperado_secao":null,"tipo":"padrao"}
```

## Links
- [[capinhas-stack]] · [[capinhas-personalizacao]]

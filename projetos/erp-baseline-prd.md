---
tags:
  - fabrica
  - erp
  - prd
  - mvp
  - baseline
  - escopo
  - portugues
  - sap-best-practices
atualizado_em: 2026-08-06
autor: Gustavo
status: ativo
tipo_doc: prd
---

> **GATEWAY DE ESCOPO — ERP baseline (fábrica)**
>
> Antes de scaffold ou módulo novo:
>
> 1. `rag_buscar("erp agente modo cursor")` → [[erp-agente-modo-cursor]]
> 2. `rag_buscar("erp baseline prd mvp escopo")` → **esta nota**
> 3. Módulos canônicos: [[erp-modulo-produto]] · [[erp-modulo-estoque]]
> 4. Telas: [[erp-ui-telas]] · Auth: [[erp-auth-login]] · Tenant: [[erp-multitenancy-spring]]
>
> **Idioma do produto:** português (Brasil) em telas, menus, mensagens, labels.  
> **SAP / Best Practices:** só modelo de processo e ordem de escopo — não UI em inglês.

# ERP — PRD baseline (escopo MVP da fábrica)

**Palavras-chave RAG:** erp baseline prd, escopo mvp erp, módulos v1 auth tenant produto estoque, fase 2 vendas financeiro, sap best practices scope, erp português brasil.

Documento de **seleção de escopo** (como scope items SAP Best Practices), enxuto para a fábrica.  
Cliente real: copiar para `projetos/<cliente>-prd.md` e listar só o que **diverge**.

---

## 1. Visão

ERP web multi-tenant (schema por cliente) para gestão operacional BR: cadastros, estoque e (depois) vendas/financeiro.  
Stack: [[erp-stack]] — Spring Boot + Angular + PostgreSQL.

## 2. Idioma e localização (obrigatório)

| Camada | Padrão |
|--------|--------|
| UI (Angular) | Português (Brasil) — menus, botões, validação, empty states |
| Mensagens API / erros de negócio | Português (Brasil) |
| Documentação Obsidian / PRD | Português |
| Nomes de tabela/coluna | snake_case em português (`produto`, `movimento_estoque`) — já canônico |
| Código Java/TS (classes técnicas) | inglês ou português consistente no repo; **não** misturar labels de tela em inglês |
| Conceitos SAP (Material Master, GR/GI) | só na documentação de padrão, não na UI |

Fuso e formato: `America/Sao_Paulo`, datas `dd/MM/yyyy`, dinheiro `R$` / `numeric(15,2)`.

---

## 3. Escopo v1 (entra)

Ordem inspirada em **SAP Best Practices** (master data → inventory), não inventada:

| # | Módulo | Equivalente conceitual SAP | Nota fábrica | Entrega |
|---|--------|----------------------------|--------------|---------|
| 1 | Autenticação + tenant | Org / usuário / mandante | [[erp-auth-login]] · [[erp-multitenancy-spring]] | Login JWT, schema por cliente, provisionar tenant |
| 2 | Produto | Material Master (mínimo) | [[erp-modulo-produto]] | CRUD + inativar · List Report + Object Page |
| 3 | Estoque | Goods Movements / IM | [[erp-modulo-estoque]] | Depósito padrão, saldo, movimentos, ACID |

Telas seguem [[erp-ui-telas]] (Fiori → lista/filtro/form/confirmação/permissões), textos em **PT-BR**.

### Critério de pronto (v1)

- [ ] Usuário faz login e só vê dados do próprio tenant  
- [ ] Cadastra produto (código, nome, unidade, ativo)  
- [ ] Lança entrada / saída / ajuste / transferência com saldo coerente  
- [ ] Saída com saldo insuficiente falha com mensagem em português  
- [ ] UI 100% PT-BR nos fluxos acima  

---

## 4. Fora do v1 (fase 2+)

| Módulo | Motivo de adiar |
|--------|-----------------|
| **Cliente / parceiro** (Business Partner) | Só se houver venda no mesmo PRD; senão com vendas |
| **Vendas** (pedido / NF saída) | Precisa produto + estoque estáveis |
| **Financeiro** (contas a pagar/receber) | Depois do documento comercial |
| Compras / MRP / WMS / fiscal completo (NFe, SPED) | Explicitamente fora do baseline |
| Grades, lote, série, multi-planta avançado | Extensão no PRD do cliente |

---

## 5. Mapa de consultas RAG (agente)

```
rag_buscar("erp baseline prd mvp escopo")
rag_buscar("erp agente modo cursor")
rag_buscar("erp modulo produto")
rag_buscar("erp modulo estoque")
rag_buscar("erp ui telas")
rag_buscar("erp login auth jwt")
buscar_historico("erp mvp v1")
```

## 6. Próximo passo técnico (não este arquivo)

Scaffold `erp-<nome>/` com `backend/` + `frontend/` + `.cursor/rules/erp-projeto.mdc` — só **depois** deste escopo fechado. Ver [[erp-stack]] e [[erp-agente-modo-cursor]].

## Links

- [[erp-agente-modo-cursor]] · [[erp-stack]] · [[erp-ui-telas]]  
- [[erp-modulo-produto]] · [[erp-modulo-estoque]] · [[erp-auth-login]] · [[erp-transacao-dominio]]

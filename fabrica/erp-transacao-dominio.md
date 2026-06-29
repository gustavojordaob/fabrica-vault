---
tags:
  - fabrica
  - erp
  - transacao
  - spring
  - acid
  - dominio
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — transação e consistência (padrão fábrica)

> O que separa ERP sério de CRUD. Consultar `rag_buscar("erp transacao atomica")`
> antes de qualquer operação que cruze módulos (estoque, financeiro, fiscal).

## Princípio

Operação que toca **mais de um módulo** tem que ser **tudo-ou-nada**. Ex: confirmar
nota de entrada → dá baixa de estoque + gera contas a pagar + lança contábil. Se
qualquer passo falha, **nada** é gravado. É o coração do ERP.

---

## Regras de @Transactional

| Onde | Regra |
|------|-------|
| Service público que escreve | `@Transactional` |
| Service que só lê | `@Transactional(readOnly = true)` |
| Controller | **nunca** `@Transactional` |
| Método privado | `@Transactional` **não funciona** (proxy Spring) — extraia pra outro bean |

### Operação que cruza módulos = uma transação

```java
@Service
class NotaEntradaService {
    private final EstoqueService estoque;
    private final FinanceiroService financeiro;
    private final ContabilService contabil;
    // construtor...

    @Transactional   // a fronteira atômica é AQUI
    public void confirmar(NotaEntrada nota) {
        estoque.darEntrada(nota.getItens());          // passo 1
        financeiro.gerarContasPagar(nota);            // passo 2
        contabil.lancar(nota.partidasDobradas());     // passo 3
        // se o passo 3 lançar exceção, 1 e 2 sofrem ROLLBACK juntos
    }
}
```

Os sub-services **não** abrem transação própria pra isso — eles participam da
transação do chamador (propagation REQUIRED, o default). A atomicidade é do método
de cima.

---

## Exceções e rollback

```java
// rollback acontece por padrão SÓ em RuntimeException.
// Para checked exception, declare:
@Transactional(rollbackFor = NotaFiscalInvalidaException.class)
public void confirmar(...) { ... }
```

Prefira **exceções de domínio não-checadas** (estendendo RuntimeException) — rollback automático e código mais limpo:

```java
public class EstoqueInsuficienteException extends RuntimeException {
    public EstoqueInsuficienteException(Long produtoId) {
        super("estoque insuficiente para produto " + produtoId);
    }
}
```

---

## Concorrência — lock onde o dado disputa

Baixa de estoque sob concorrência precisa de lock pessimista, senão dois pedidos
vendem a mesma peça:

```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("select s from SaldoEstoque s where s.produtoId = :id")
Optional<SaldoEstoque> lockSaldo(@Param("id") Long produtoId);
```

Para edição de tela longa (otimista), use `@Version`:

```java
@Entity class Pedido {
    @Version private Long versao;   // detecta edição concorrente
}
```

---

## Tipos que não podem errar no ERP

| Dado | Tipo Java | Tipo Postgres | Por quê |
|------|-----------|---------------|---------|
| Dinheiro | `BigDecimal` | `numeric(15,2)` | **NUNCA** `double`/`float` — erro de arredondamento vira problema fiscal |
| Data/hora | `Instant` / `LocalDate` | `timestamptz` / `date` | timezone-aware |
| Quantidade fracionada | `BigDecimal` | `numeric` | idem dinheiro |

---

## O que NUNCA fazer

- ❌ **`@Transactional` em método privado ou chamado internamente** — o proxy do Spring não intercepta. Extraia pra um bean separado.
- ❌ **Transação no controller** — a fronteira é o service.
- ❌ **`double`/`float` pra dinheiro ou quantidade.** Sempre `BigDecimal` / `numeric`.
- ❌ **Cada sub-passo abrir transação própria** (`REQUIRES_NEW`) numa operação que deveria ser atômica — quebra o tudo-ou-nada.
- ❌ **Baixa de estoque/saldo sem lock** sob concorrência — vende duas vezes a mesma peça.
- ❌ **Transação longa segurando lock** enquanto espera input do usuário — use `@Version` (otimista) pra telas.

---

## Golden set sugerido

```
{"id":"erp-tx-01","query":"como deixar baixa estoque e financeiro atomico","esperado_nota":"erp-transacao-dominio.md","tipo":"padrao"}
{"id":"erp-tx-02","query":"transactional em metodo privado nao funciona","esperado_nota":"erp-transacao-dominio.md","tipo":"solucao"}
{"id":"erp-tx-03","query":"qual tipo usar para dinheiro no erp","esperado_nota":"erp-transacao-dominio.md","tipo":"padrao"}
{"id":"erp-tx-04","query":"dois pedidos vendendo mesma peca lock","esperado_nota":"erp-transacao-dominio.md","tipo":"solucao"}
```

## Links
- [[erp-stack]] · [[erp-spring-camadas]] · [[erp-postgres-schema]]

---
tags:
  - fabrica
  - erp
  - testes
  - junit
  - mockito
  - testcontainers
  - backend
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — testes backend (padrão fábrica)

> Java 25 + Spring Boot 4.1. Consultar `rag_buscar("erp teste backend")` antes de
> escrever ou pedir teste. Num ERP, teste de regra de negócio e transação não é opcional.

## Pirâmide (o que testar com o quê)

| Nível | Ferramenta | Testa | Velocidade |
|-------|-----------|-------|------------|
| **Unitário** | JUnit 5 + Mockito + AssertJ | Regra de negócio do service/domínio, sem banco | rápido (ms) |
| **Repositório/JPA** | `@DataJpaTest` + Testcontainers | Query, mapeamento, constraint | médio |
| **Integração** | `@SpringBootTest` + Testcontainers | Fluxo controller→service→banco real | lento |

Regra: **muito unitário, alguns de integração.** Não inverta a pirâmide.

---

## Stack de teste (pom.xml)

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>   <!-- JUnit5 + Mockito + AssertJ -->
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>postgresql</artifactId>
  <scope>test</scope>
</dependency>
```

---

## Unitário — regra de negócio, banco mockado

```java
@ExtendWith(MockitoExtension.class)
class PedidoServiceTest {

    @Mock PedidoRepository repo;
    @Mock EstoqueService estoque;
    @InjectMocks PedidoService service;

    @Test
    void deveCriarPedidoReservandoEstoque() {
        var req = new CriarPedidoRequest(1L, List.of(new ItemPedidoRequest(10L, 2)));
        when(repo.save(any())).thenAnswer(inv -> inv.getArgument(0));

        Pedido pedido = service.criar(req);

        assertThat(pedido.getStatus()).isEqualTo(StatusPedido.RASCUNHO);
        verify(estoque).reservar(pedido);          // garante que cruzou o módulo
        verify(repo).save(pedido);
    }

    @Test
    void deveFalharQuandoEstoqueInsuficiente() {
        var req = new CriarPedidoRequest(1L, List.of(new ItemPedidoRequest(10L, 999)));
        doThrow(new EstoqueInsuficienteException(10L)).when(estoque).reservar(any());

        assertThatThrownBy(() -> service.criar(req))
            .isInstanceOf(EstoqueInsuficienteException.class);
        verify(repo, never()).save(any());          // nada gravado
    }
}
```

> Teste unitário **não sobe Spring nem banco.** Mocka as dependências. É onde mora
> a maior parte da cobertura.

---

## Repositório — banco Postgres real (Testcontainers)

```java
@DataJpaTest
@Testcontainers
@AutoConfigureTestDatabase(replace = Replace.NONE)   // usa o container, não H2
class PedidoRepositoryTest {

    @Container @ServiceConnection                      // Spring Boot 4: liga sozinho
    static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:18");

    @Autowired PedidoRepository repo;

    @Test
    void deveBuscarPorClienteEStatus() {
        repo.save(Pedido.novo(1L));
        var achados = repo.findByClienteIdAndStatus(1L, StatusPedido.RASCUNHO);
        assertThat(achados).hasSize(1);
    }
}
```

> **Postgres real, não H2.** ERP usa recursos do Postgres (numeric, timestamptz,
> constraints) que o H2 finge mal. Testar em H2 dá falso verde.

---

## Integração — transação atômica de verdade

```java
@SpringBootTest
@Testcontainers
class NotaEntradaIT {

    @Container @ServiceConnection
    static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:18");

    @Autowired NotaEntradaService service;
    @Autowired EstoqueRepository estoqueRepo;
    @Autowired ContaPagarRepository contaRepo;

    @Test
    void confirmarDeveSerAtomico() {
        var nota = notaComItemQueFalhaNoContabil();
        assertThatThrownBy(() -> service.confirmar(nota)).isInstanceOf(...);

        // o ROLLBACK tem que ter desfeito estoque E financeiro
        assertThat(estoqueRepo.count()).isZero();
        assertThat(contaRepo.count()).isZero();
    }
}
```

> Este é o teste que prova o "tudo-ou-nada" de [[erp-transacao-dominio]]. Num ERP,
> esse tipo de teste vale mais que dez de CRUD.

---

## O que sempre testar num ERP

- ✅ Toda **regra de negócio** do domínio (cálculo, invariante, transição de status).
- ✅ Toda **operação que cruza módulos** (atomicidade — teste de integração).
- ✅ **Concorrência** onde há lock (dois pedidos na mesma peça).
- ✅ **Tipos críticos** (arredondamento de `numeric`, timezone de `timestamptz`).

## O que NUNCA fazer

- ❌ **Testar repositório com H2.** Use Testcontainers + Postgres 18 real.
- ❌ **`@SpringBootTest` pra testar regra de negócio** — é lento; use unitário com mock.
- ❌ **Teste sem assert de rollback** numa operação atômica — não prova nada.
- ❌ **Mockar o que você quer testar** (mockar o próprio service sob teste).
- ❌ **Pular teste de transação** "porque funciona na mão" — é o que mais quebra em ERP.

---

## Nomenclatura

- Unitário/JPA: `<Classe>Test.java`
- Integração: `<Fluxo>IT.java` (IT = Integration Test; roda no `failsafe`, não no `surefire`)
- Método: `deve<ComportamentoEsperado>Quando<Condicao>` (pt-br, descritivo)

---

## Golden set sugerido

```
{"id":"erp-test-01","query":"como testar regra de negocio service erp","esperado_nota":"erp-testes-backend.md","tipo":"padrao"}
{"id":"erp-test-02","query":"testar repositorio com h2 ou postgres real","esperado_nota":"erp-testes-backend.md","tipo":"solucao"}
{"id":"erp-test-03","query":"como testar transacao atomica rollback","esperado_nota":"erp-testes-backend.md","tipo":"padrao"}
{"id":"erp-test-04","query":"testcontainers postgres spring boot","esperado_nota":"erp-testes-backend.md","tipo":"padrao"}
```

## Links
- [[erp-stack]] · [[erp-spring-camadas]] · [[erp-transacao-dominio]]

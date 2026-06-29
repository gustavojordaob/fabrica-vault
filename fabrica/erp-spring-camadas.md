---
tags:
  - fabrica
  - erp
  - spring
  - java
  - camadas
  - backend
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — camadas backend Spring (padrão fábrica)

> Java 25 + Spring Boot 4.1. Consultar `rag_buscar("erp camadas spring")` antes de
> criar controller/service/repository novo.

## Fluxo de uma requisição

```
Controller  → recebe/devolve DTO, valida entrada, sem regra de negócio
   Service  → regra de negócio, @Transactional, orquestra repositories
Repository  → Spring Data JPA, acesso a dados, sem regra
   Domain   → entidades JPA + lógica de domínio própria
      DTO   → records na borda (request/response), nunca expõe entidade
```

Regra de ouro: **dependência só aponta pra dentro.** Controller conhece Service; Service conhece Repository; ninguém de fora conhece entidade JPA.

---

## Código de referência

### DTO = record (Java 25)

```java
public record CriarPedidoRequest(
    @NotNull Long clienteId,
    @NotEmpty List<ItemPedidoRequest> itens
) {}

public record PedidoResponse(Long id, String status, BigDecimal total) {
    public static PedidoResponse de(Pedido p) {
        return new PedidoResponse(p.getId(), p.getStatus().name(), p.getTotal());
    }
}
```

### Controller — fino, só borda

```java
@RestController
@RequestMapping("/api/pedidos")
class PedidoController {
    private final PedidoService service;
    PedidoController(PedidoService service) { this.service = service; }

    @PostMapping
    ResponseEntity<PedidoResponse> criar(@Valid @RequestBody CriarPedidoRequest req) {
        Pedido p = service.criar(req);
        return ResponseEntity.status(CREATED).body(PedidoResponse.de(p));
    }

    @GetMapping("/{id}")
    PedidoResponse buscar(@PathVariable Long id) {
        return PedidoResponse.de(service.buscar(id));
    }
}
```

### Service — regra de negócio + transação

```java
@Service
class PedidoService {
    private final PedidoRepository repo;
    private final EstoqueService estoque;
    PedidoService(PedidoRepository repo, EstoqueService estoque) {
        this.repo = repo; this.estoque = estoque;
    }

    @Transactional
    public Pedido criar(CriarPedidoRequest req) {
        Pedido pedido = Pedido.novo(req.clienteId());
        req.itens().forEach(i -> pedido.adicionarItem(i.produtoId(), i.qtd()));
        estoque.reservar(pedido);        // cruza módulo → mesma transação
        return repo.save(pedido);
    }

    @Transactional(readOnly = true)
    public Pedido buscar(Long id) {
        return repo.findById(id)
            .orElseThrow(() -> new RecursoNaoEncontradoException("pedido", id));
    }
}
```

### Repository — Spring Data, sem regra

```java
interface PedidoRepository extends JpaRepository<Pedido, Long> {
    List<Pedido> findByClienteIdAndStatus(Long clienteId, StatusPedido status);
}
```

### Domain — entidade com comportamento (não anêmica)

```java
@Entity @Table(name = "pedido")
class Pedido {
    @Id @GeneratedValue(strategy = IDENTITY) private Long id;
    @Enumerated(STRING) private StatusPedido status;
    @OneToMany(mappedBy = "pedido", cascade = ALL) private List<ItemPedido> itens = new ArrayList<>();

    static Pedido novo(Long clienteId) { /* factory */ }
    void adicionarItem(Long produtoId, int qtd) { /* invariante de domínio aqui */ }
    BigDecimal getTotal() { return itens.stream().map(ItemPedido::subtotal)
        .reduce(BigDecimal.ZERO, BigDecimal::add); }
}
```

### Tratamento de erro centralizado

```java
@RestControllerAdvice
class ApiExceptionHandler {
    @ExceptionHandler(RecursoNaoEncontradoException.class)
    ProblemDetail naoEncontrado(RecursoNaoEncontradoException e) {
        return ProblemDetail.forStatusAndDetail(NOT_FOUND, e.getMessage());
    }
}
```

---

## O que NUNCA fazer

- ❌ **Regra de negócio no controller.** Controller só traduz HTTP ↔ DTO.
- ❌ **Retornar entidade JPA na API.** Sempre DTO. Entidade vaza schema e causa lazy-loading fora de transação.
- ❌ **`@Autowired` em campo.** Injeção por construtor (testável, final, sem proxy mágico).
- ❌ **Entidade anêmica** (só getter/setter). Invariante de domínio mora na entidade.
- ❌ **Repository chamando outro repository pra "montar regra".** Isso é trabalho do service.
- ❌ **`@Transactional` no controller.** Transação é fronteira de service. Ver [[erp-transacao-dominio]].

---

## Golden set sugerido

```
{"id":"erp-cam-01","query":"onde fica regra de negocio controller service","esperado_nota":"erp-spring-camadas.md","tipo":"padrao"}
{"id":"erp-cam-02","query":"posso retornar entidade jpa na api","esperado_nota":"erp-spring-camadas.md","tipo":"padrao"}
{"id":"erp-cam-03","query":"injecao de dependencia construtor ou autowired","esperado_nota":"erp-spring-camadas.md","tipo":"padrao"}
```

## Links
- [[erp-stack]] · [[erp-transacao-dominio]] · [[erp-testes-backend]]

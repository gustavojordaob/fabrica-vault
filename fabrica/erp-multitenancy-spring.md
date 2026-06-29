---
tags:
  - fabrica
  - erp
  - multitenancy
  - spring
  - hibernate
  - schema
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — multi-tenancy por SCHEMA (padrão fábrica)

> Peça central da arquitetura do ERP. Consultar `rag_buscar("erp multitenant schema")`
> antes de mexer em conexão, datasource ou qualquer coisa que toque tenant.

## Modelo

Um banco Postgres. Dentro dele:

- **Schema `master`** — catálogo de tenants: quem existe, qual schema, qual versão de migration. Login resolve aqui.
- **Um schema por cliente** — `tenant_<slug>` (ex: `tenant_acme`), cada um com TODAS as tabelas do ERP.

A cada request, o tenant é resolvido (do JWT) e o Hibernate troca o `search_path`/schema da conexão. Mesmo código de service/repository serve todos os tenants.

---

## Fluxo por request

```
JWT chega → filtro extrai tenantId → TenantContext.set(tenantId)
   → Hibernate CurrentTenantIdentifierResolver lê o context
   → MultiTenantConnectionProvider faz SET search_path TO tenant_<id>
   → query roda no schema certo
   → no fim do request: TenantContext.clear()
```

---

## Código de referência

### TenantContext (ThreadLocal)

```java
public final class TenantContext {
    private static final ThreadLocal<String> CURRENT = new ThreadLocal<>();
    private TenantContext() {}
    public static void set(String tenantId) { CURRENT.set(tenantId); }
    public static String get() { return CURRENT.get(); }
    public static void clear() { CURRENT.remove(); }
}
```

> Java 25: dá pra evoluir pra `ScopedValue` (melhor com virtual threads, sem risco
> de vazar ThreadLocal). Comece com ThreadLocal; migre se usar virtual threads no hot path.

### Resolver — diz ao Hibernate qual tenant é o atual

```java
@Component
public class TenantResolver implements CurrentTenantIdentifierResolver<String> {
    @Override public String resolveCurrentTenantIdentifier() {
        String t = TenantContext.get();
        return (t != null) ? t : "master"; // fallback explícito
    }
    @Override public boolean validateExistingCurrentSessions() { return true; }
}
```

### ConnectionProvider — troca o schema na conexão

```java
@Component
public class SchemaMultiTenantConnectionProvider
        implements MultiTenantConnectionProvider<String> {

    private final DataSource dataSource;
    public SchemaMultiTenantConnectionProvider(DataSource ds) { this.dataSource = ds; }

    @Override public Connection getAnyConnection() throws SQLException {
        return dataSource.getConnection();
    }
    @Override public Connection getConnection(String tenantId) throws SQLException {
        Connection conn = dataSource.getConnection();
        // identificador validado (whitelist) — ver "nunca faça" abaixo
        conn.createStatement().execute("SET search_path TO " + sanitize(tenantId));
        return conn;
    }
    @Override public void releaseConnection(String tenantId, Connection conn) throws SQLException {
        conn.createStatement().execute("SET search_path TO master");
        conn.close();
    }
    // ... releaseAnyConnection, supportsAggressiveRelease, isUnwrappableAs, unwrap

    private String sanitize(String tenantId) {
        if (!tenantId.matches("^[a-z0-9_]+$"))   // só schema válido
            throw new IllegalArgumentException("tenant inválido: " + tenantId);
        return tenantId;
    }
}
```

### application.yml

```yaml
spring:
  jpa:
    properties:
      hibernate:
        multiTenancy: SCHEMA
  datasource:
    url: jdbc:postgresql://localhost:5432/erp
    hikari:
      maximum-pool-size: 10   # UM pool só — é o mesmo banco
```

### Filtro web — popula o contexto

```java
@Component
public class TenantFilter extends OncePerRequestFilter {
    @Override protected void doFilterInternal(HttpServletRequest req,
            HttpServletResponse res, FilterChain chain) throws ... {
        try {
            String tenantId = extrairDoJwt(req); // do token validado pelo Security
            TenantContext.set(tenantId);
            chain.doFilter(req, res);
        } finally {
            TenantContext.clear();   // SEMPRE limpar
        }
    }
}
```

---

## O que NUNCA fazer

- ❌ **Passar o schema/tenant como parâmetro de método de service.** O tenant vem do contexto, não da assinatura. Service não sabe de tenant.
- ❌ **Concatenar tenantId cru no SQL sem validar** (`SET search_path TO ` + input). É SQL injection. Sempre `sanitize()` com whitelist `^[a-z0-9_]+$`.
- ❌ **Esquecer o `TenantContext.clear()`** no fim do request. Vaza tenant pra próxima request na mesma thread → cliente vê dado de outro.
- ❌ **Pool por tenant.** É o mesmo banco; um HikariCP só. (Banco-por-tenant seria diferente — não é o nosso caso.)
- ❌ **Rodar migration sem iterar todos os schemas.** Ver [[erp-migrations-flyway]].

---

## Golden set sugerido

```
{"id":"erp-mt-01","query":"como troca de schema por tenant no hibernate","esperado_nota":"erp-multitenancy-spring.md","tipo":"padrao"}
{"id":"erp-mt-02","query":"onde guardar o tenant atual da request","esperado_nota":"erp-multitenancy-spring.md","tipo":"padrao"}
{"id":"erp-mt-03","query":"erp vaza dado entre clientes thread","esperado_nota":"erp-multitenancy-spring.md","tipo":"solucao"}
```

## Links
- [[erp-stack]] · [[erp-migrations-flyway]] · [[erp-postgres-schema]]

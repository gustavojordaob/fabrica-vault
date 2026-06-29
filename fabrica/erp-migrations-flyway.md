---
tags:
  - fabrica
  - erp
  - flyway
  - migrations
  - multitenancy
  - postgresql
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — migrations Flyway por schema (padrão fábrica)

> O ponto mais delicado do multi-tenant por schema. Consultar
> `rag_buscar("erp migration por schema tenant")` antes de qualquer mudança de schema.

## Problema

Schema-por-tenant significa que **toda** mudança de schema precisa rodar em **N schemas**
(um por cliente) + no `master`. Se você rodar só num, os tenants ficam em versões
divergentes — o pior estado possível. Por isso a migration é **orquestrada**, não manual.

---

## Estrutura de migrations

```
src/main/resources/db/migration/
├── master/          ← catálogo de tenants (roda 1x)
│   └── V1__catalogo_tenants.sql
└── tenant/          ← schema de CADA cliente (roda em todos)
    ├── V1__init.sql
    ├── V2__add_tabela_estoque.sql
    └── V3__...
```

Duas "linhas" de migration separadas: o catálogo `master` evolui sozinho; o schema de
tenant é o baseline aplicado a todo cliente.

---

## Catálogo (schema master)

```sql
-- master/V1__catalogo_tenants.sql
CREATE TABLE master.tenant (
    id          BIGSERIAL PRIMARY KEY,
    slug        VARCHAR(40) NOT NULL UNIQUE,   -- vira nome do schema: tenant_<slug>
    razao_social VARCHAR(200) NOT NULL,
    schema_name VARCHAR(63) NOT NULL UNIQUE,
    versao_schema VARCHAR(20),                 -- versão Flyway aplicada
    ativo       BOOLEAN NOT NULL DEFAULT true,
    criado_em   TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## Orquestrador — aplica em todos os schemas

```java
@Component
public class TenantMigrationRunner {
    private final DataSource dataSource;
    private final TenantCatalogRepository catalogo;
    // construtor...

    /** Roda no boot e ao provisionar tenant novo. */
    public void migrarTodosOsTenants() {
        List<String> schemas = catalogo.listarSchemasAtivos();
        List<String> falharam = new ArrayList<>();
        for (String schema : schemas) {
            try {
                migrarUmSchema(schema);
            } catch (Exception e) {
                falharam.add(schema + ": " + e.getMessage());
            }
        }
        if (!falharam.isEmpty())
            throw new MigrationException("Schemas que falharam: " + falharam);
        // ↑ visibilidade: você SABE quais tenants ficaram pra trás
    }

    private void migrarUmSchema(String schema) {
        Flyway.configure()
            .dataSource(dataSource)
            .schemas(schema)
            .locations("classpath:db/migration/tenant")
            .load()
            .migrate();
    }
}
```

> Regra: o boot da aplicação roda `migrarTodosOsTenants()`. Nenhum tenant atende
> request antes de estar na versão de schema atual.

---

## Provisionar cliente novo

```java
@Transactional
public Tenant provisionar(String slug, String razaoSocial) {
    String schema = "tenant_" + slug;          // já validado: ^[a-z0-9_]+$
    jdbc.execute("CREATE SCHEMA " + schema);    // 1. cria schema
    migrarUmSchema(schema);                     // 2. aplica todas as migrations
    Tenant t = catalogo.save(new Tenant(slug, razaoSocial, schema)); // 3. registra no master
    return t;
}
```

Onboarding = `CREATE SCHEMA` + migrations + registro. Automatizado desde o dia 1 —
nunca manual.

---

## Convenções de migration

- **Imutável depois de aplicada.** Migration que já rodou em produção NUNCA é editada. Erro → nova migration corretiva.
- **Versionada e sequencial:** `V<n>__descricao.sql`. Sem pular número.
- **Idempotência onde der:** `CREATE TABLE IF NOT EXISTS` é tentador, mas o Flyway já controla — prefira migration limpa e deixe o Flyway versionar.
- **Repeatable migrations** (`R__`) só pra views/funções que podem reexecutar.

---

## O que NUNCA fazer

- ❌ **Rodar migration manualmente em um schema só.** Sempre via orquestrador, em todos.
- ❌ **Editar migration já aplicada em produção.** Quebra o checksum do Flyway e diverge tenants.
- ❌ **Provisionar tenant criando schema na mão** sem rodar as migrations — cliente nasce com schema incompleto.
- ❌ **Deixar a app atender request com tenant em versão de schema antiga.** Migra no boot, antes de abrir a porta.
- ❌ **`tenant_` + input sem validar** no `CREATE SCHEMA` — SQL injection. Whitelist `^[a-z0-9_]+$`.

---

## Golden set sugerido

```
{"id":"erp-fw-01","query":"como rodar migration em todos os schemas de tenant","esperado_nota":"erp-migrations-flyway.md","tipo":"padrao"}
{"id":"erp-fw-02","query":"provisionar cliente novo schema erp","esperado_nota":"erp-migrations-flyway.md","tipo":"fluxo"}
{"id":"erp-fw-03","query":"posso editar migration ja aplicada","esperado_nota":"erp-migrations-flyway.md","tipo":"solucao"}
```

## Links
- [[erp-stack]] · [[erp-multitenancy-spring]] · [[erp-postgres-schema]]

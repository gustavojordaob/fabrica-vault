---
tags:
  - fabrica
  - erp
  - stack
  - java
  - angular
  - postgresql
  - spring
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — stack canônica (padrão fábrica)

> **Especialidade ERP-web.** Diferente do padrão Expo/Firebase dos apps de salão.
> Agente: consultar `rag_buscar("erp stack")` antes de codar backend, front ou schema.

ERP web **sério, transacional, multi-tenant**. Não é app mobile, não vai pra loja.

---

## Versões FIXAS (não improvisar)

| Camada | Versão | Observação |
|--------|--------|------------|
| **Java** | **25 LTS** | OpenJDK/Temurin (gratuito). Suporte até ~2030. NÃO usar 26 (não-LTS). |
| **Spring Boot** | **4.1.x** | Sobre Spring Framework 7. Baseline Java 17, roda Java 25 first-class. |
| **Build** | **Maven** | `pom.xml`. Wrapper `mvnw` versionado. |
| **PostgreSQL** | **18.x** | NÃO usar 19 (beta até set/out 2026). |
| **Migrations** | **Flyway** | SQL versionado. Ver [[erp-migrations-flyway]]. |
| **ORM** | **Hibernate 7 / Spring Data JPA** | Multi-tenancy por SCHEMA. Ver [[erp-multitenancy-spring]]. |
| **Angular** | **21 LTS** | Signal-first, zoneless, standalone. LTS até maio/2027. |
| **Node (build Angular)** | LTS atual | Só pra buildar o front. |
| **Testes back** | JUnit 5 + Mockito + AssertJ + Testcontainers | Ver [[erp-testes-backend]]. |
| **Testes front** | **Vitest** | Production-ready no Angular 21 (NÃO Karma). |

---

## Decisões de arquitetura travadas

- **Multi-tenant por SCHEMA** (um banco Postgres, um schema por cliente + schema `master` de catálogo). Modelo mandante/client (estilo SAP). Ver [[erp-multitenancy-spring]].
- **Transação ACID** nos pontos que cruzam módulos (estoque + financeiro + fiscal = atômico). Ver [[erp-transacao-dominio]].
- **Camadas:** controller → service → repository → domain, com DTO na borda. Ver [[erp-spring-camadas]].
- **Front separado do back:** Angular SPA consome API REST do Spring. Repositórios separados (ou monorepo com 2 pastas), nunca misturados.

---

## Estrutura de repositórios

```
erp-<cliente-ou-produto>/
├── backend/                 ← Spring Boot 4.1 (Maven)
│   ├── pom.xml
│   ├── src/main/java/br/com/fabrica/erp/
│   │   ├── ErpApplication.java
│   │   ├── config/          ← multitenancy, security, beans
│   │   ├── tenant/          ← TenantContext, resolver, filtro
│   │   └── <modulo>/        ← controller, service, repository, domain, dto
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   └── db/migration/    ← Flyway (master + tenant)
│   └── src/test/java/...
└── frontend/                ← Angular 22
    ├── package.json
    └── src/app/
        ├── core/            ← interceptors, guards, services globais
        ├── shared/          ← componentes reutilizáveis
        └── features/<modulo>/
```

---

## O que NÃO fazer

- ❌ Reaproveitar o `criar_projeto_completo` / scaffold Expo da fábrica — é React Native, não serve aqui.
- ❌ Usar Firestore "pra começar rápido". ERP é relacional. Decisão registrada.
- ❌ Angular com NgModules / Zone.js / Karma — padrão morto no Angular 22.
- ❌ Java 26 (não-LTS) ou Postgres 19 (beta) em produção.
- ❌ Misturar código do front e do back no mesmo módulo Maven.

---

## Golden set sugerido (adicionar em fabrica/eval/golden-set.jsonl)

```
{"id":"erp-01","query":"qual versao de java spring postgres angular do erp","esperado_nota":"erp-stack.md","tipo":"padrao"}
{"id":"erp-02","query":"erp usa firestore ou banco relacional","esperado_nota":"erp-stack.md","tipo":"padrao"}
```

## Links

- [[erp-multitenancy-spring]] · [[erp-spring-camadas]] · [[erp-transacao-dominio]]
- [[erp-migrations-flyway]] · [[erp-postgres-schema]] · [[erp-angular-estrutura]] · [[erp-testes-backend]]

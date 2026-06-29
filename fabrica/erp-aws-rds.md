---
tags:
  - fabrica
  - erp
  - aws
  - rds
  - postgresql
  - infra
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — PostgreSQL na AWS / RDS (padrão fábrica)

> Infra do banco do ERP. Consultar `rag_buscar("erp aws rds postgres")` antes de
> configurar conexão, credencial ou deploy de banco.

## Stack de banco

- **RDS PostgreSQL 18** (região `sa-east-1` / São Paulo).
- Um banco `erp`, multi-tenant por **schema** (ver [[erp-multitenancy-spring]]).
- Para produção: **Multi-AZ** (failover), backups automáticos, `deletion protection` ligado.

---

## Usuários do banco (separação por papel)

| Usuário | Quem usa | Permissão |
|---------|----------|-----------|
| `app_runtime` | a aplicação Spring | DML nos schemas de tenant (SELECT/INSERT/UPDATE/DELETE), sem DDL |
| `app_migrate` | só CI/CD (Flyway) | DDL (CREATE/ALTER) — roda migrations |
| `app_readonly` | **MCP postgres** | só SELECT — inspeção do schema pelo agente |

> Princípio: o MCP e o agente **nunca** usam credencial que escreve. `app_readonly`
> é defesa em profundidade junto com o guard do MCP.

---

## Conexão — SSL é obrigatório no RDS

```
# connection string (exemplo)
jdbc:postgresql://erp.xxxx.sa-east-1.rds.amazonaws.com:5432/erp?sslmode=require
```

- **`sslmode=require`** (no mínimo). Para verificação completa: `verify-full` + CA bundle da AWS (`rds-ca-rsa2048-g1`).
- Baixar o CA bundle da região e apontar no cliente.
- Spring (`application.yml`): `spring.datasource.url` com `?sslmode=require`.

---

## Credenciais — NUNCA no código

| Ambiente | Onde a credencial vive |
|----------|------------------------|
| Produção | **AWS Secrets Manager** (a app lê no boot via SDK ou IAM) |
| CI | Secret do pipeline (GitHub Actions secret) |
| Dev local | `.env` **não versionado** (no `.gitignore`) |

- **Jamais** commitar senha/connection string. Nem no `application.yml`, nem no MCP.
- IAM database authentication é o ideal (token temporário em vez de senha fixa) — avaliar pra `app_runtime`.

---

## Security group / rede

- RDS **não** público. Subnet privada.
- Security group libera porta 5432 **só** de: a VPC da aplicação (Lambda/EC2/ECS) e, em dev, o IP fixo do seu PC (não `0.0.0.0/0`).
- O MCP postgres roda na sua máquina → o IP do dev precisa estar liberado pra ele conectar no RDS de dev/homolog.

---

## Pool de conexões

- Spring: **HikariCP**, `maximum-pool-size` dimensionado ao `max_connections` do RDS (não estoure). Um pool só (multi-tenant por schema = mesmo banco).
- MCP postgres: pool pequeno (2–3 conexões), `statement_timeout` curto, transação `READ ONLY`.
- Atenção ao `max_connections` da classe da instância RDS — instância pequena tem limite baixo. Se for serverless/Lambda no futuro, usar **RDS Proxy** (pooling gerenciado).

---

## Checklist de banco novo (ambiente)

- [ ] RDS PostgreSQL 18 criado, Multi-AZ se produção
- [ ] Subnet privada + security group restrito (sem `0.0.0.0/0`)
- [ ] SSL forçado (`rds.force_ssl = 1` no parameter group)
- [ ] Usuários `app_runtime`, `app_migrate`, `app_readonly` criados com grants corretos
- [ ] Credenciais no Secrets Manager (prod) / `.env` ignorado (dev)
- [ ] Backups automáticos + `deletion protection`
- [ ] `app_migrate` roda Flyway (ver [[erp-migrations-flyway]])
- [ ] MCP postgres configurado com `app_readonly` (ver README do mcp-postgres)
- [ ] `salvar_decisao` registrando a config

---

## O que NUNCA fazer

- ❌ **Connection string/senha no código ou no git.** Secrets Manager / env.
- ❌ **RDS público** (`Publicly accessible = yes`) ou security group `0.0.0.0/0`.
- ❌ **Conexão sem SSL** no RDS.
- ❌ **Usar `app_migrate` ou `app_runtime` no MCP.** O MCP usa `app_readonly`.
- ❌ **Estourar `max_connections`** somando os pools (app + MCP + CI).

---

## Golden set sugerido

```
{"id":"erp-aws-01","query":"como conectar erp no rds postgres aws","esperado_nota":"erp-aws-rds.md","tipo":"integracao"}
{"id":"erp-aws-02","query":"onde guardar senha do banco aws","esperado_nota":"erp-aws-rds.md","tipo":"padrao"}
{"id":"erp-aws-03","query":"qual usuario o mcp postgres usa","esperado_nota":"erp-aws-rds.md","tipo":"padrao"}
```

## Links
- [[erp-stack]] · [[erp-multitenancy-spring]] · [[erp-migrations-flyway]] · [[erp-postgres-schema]]

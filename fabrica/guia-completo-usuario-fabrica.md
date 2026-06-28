---
tags:
  - fabrica
  - arquitetura
  - guia
  - onboarding
  - mcp
  - rag
autor: Gustavo
atualizado_em: 2026-06-28
status: guia-usuario
links:
  - "[[arquitetura-fabrica-ia]]"
  - "[[mcps-cursor-padrao]]"
  - "[[INDEX]]"
---

# Guia completo — Fábrica de Apps com IA

> **Para você (Gustavo):** documento para ler, imprimir ou copiar para outro computador.  
> **Para agentes Cursor:** consultar também `rag_buscar("arquitetura fabrica guia")`.

---

## Sumário

1. [O que é a fábrica](#1-o-que-é-a-fábrica)
2. [Arquitetura hoje (jun/2026)](#2-arquitetura-hoje-jun2026)
3. [Como começar a usar](#3-como-começar-a-usar)
4. [Dia a dia — fluxos que você repete](#4-dia-a-dia--fluxos-que-você-repete)
5. [Como adicionar uma especialidade nova](#5-como-adicionar-uma-especialidade-nova)
6. [Exemplo completo: AWS + PostgreSQL](#6-exemplo-completo-aws--postgresql)
7. [RAG — como funciona por dentro](#7-rag--como-funciona-por-dentro)
8. [Troubleshooting rápido](#8-troubleshooting-rápido)
9. [Mapa de pastas](#9-mapa-de-pastas)
10. [Pitch de 30 segundos](#10-pitch-de-30-segundos)

---

## 1. O que é a fábrica

Você não usa IA como “ChatGPT que cola código”. Montou um **sistema** onde:

| Peça | Função |
|------|--------|
| **Cursor** | IDE com agente que edita código |
| **Obsidian** (`fabrica/`) | Sua base de conhecimento — padrões, erros, decisões |
| **RAG (Chroma)** | Busca semântica nas notas (~80 ms por query) |
| **MCP fabrica-apps** | Ferramentas: GitHub, PR, memória, RAG |
| **MCPs por tema** | Firebase, WhatsApp, Mercado Pago, RevenueCat… |
| **Hooks + Rules** | Impedem a IA de codar sem consultar a fábrica |

**Stack padrão dos apps:** React Native (Expo) + Firebase.  
**Apps de referência:** LashMatch, Cortejo.

**Frase:** a IA segue **seus** padrões; você foca em produto e teste.

---

## 2. Arquitetura hoje (jun/2026)

### Diagrama mental

```
VOCÊ (prompt no Cursor)
        │
        ▼
┌───────────────────┐
│  Hooks automáticos │  ← Chroma + gate antes de Write/Shell
└─────────┬─────────┘
          ▼
┌───────────────────┐
│  Agente Cursor    │  ← Rules (.mdc) sempre ativas
└─────────┬─────────┘
          │
    ┌─────┴─────┬─────────────┬──────────────┐
    ▼           ▼             ▼              ▼
 fabrica-apps  firebase    mercadopago    whatsapp …
    │           │             │              │
    ▼           ▼             ▼              ▼
 Obsidian     Deploy       API real      Templates Meta
 + GitHub     Firestore    assinaturas
 + RAG :7332
```

### Camadas

| Camada | Onde | Para quê |
|--------|------|----------|
| **Conhecimento** | `C:/Users/gusta/obsidian/fabrica/*.md` | Fonte da verdade humana |
| **Memória de erros** | `fabrica/erros-e-solucoes.md` | Não repetir bug |
| **Decisões** | `fabrica/decisoes.md` | Por que escolheu X |
| **Indexação** | `indexar_rapido.py` | Único script que grava no Chroma |
| **Servidor busca** | `indexar_obsidian_chroma.py --server` | HTTP em `127.0.0.1:7332` |
| **MCP central** | `fabrica-apps-mcp/server-v2.js` | Ponte Cursor ↔ RAG ↔ GitHub |
| **Hooks** | `~/.cursor/hooks/` | Automação que a IA não pode ignorar |
| **Rules globais** | `~/.cursor/rules/*.mdc` | Regras fixas (RAG, Firebase, doc) |
| **Projetos** | `C:/Users/gusta/projetos/` | Código dos apps |

### RAG híbrido (estado atual)

Decisão registrada: **RAG hot path híbrido + fallback honesto**.

| Etapa | O quê | Hot path (MCP) |
|-------|-------|----------------|
| 1 | Busca **densa** (Chroma + embeddings) | ✅ |
| 2 | Busca **BM25** (palavras-chave) | ✅ |
| 3 | **RRF** — fusão dos dois rankings | ✅ |
| 4 | Filtro PRD (`*-prd.md` em queries de padrão) | ✅ |
| 5 | **Rerank** (`bge-reranker-v2-m3`) | ❌ só eval offline (`RAG_RERANK=1`) |

- **BM25** construído **uma vez** no boot/reindex (~50–80 ms/query).
- **`rag_buscar`** e **`buscar_historico`** usam `127.0.0.1:7332` (não `localhost` — Windows IPv6 atrasa ~2 s).
- **Servidor offline** → aviso claro + comando para subir. **Sem** fallback no `CLAUDE.md` (monólito abandonado).

**Métricas (golden set v2, hot path):** hit@1 52% · hit@3 92% · MRR 0.71.

---

## 3. Como começar a usar

### Pré-requisitos (máquina nova)

| Item | Instalar / configurar |
|------|------------------------|
| Cursor | Com MCP habilitado |
| Node.js | MCP + hooks |
| Python 3 | Chroma + scripts RAG |
| Git | Clone dos repos |
| Obsidian | Opcional (edita `.md`; RAG lê direto) |
| Firebase CLI | `npx -y firebase-tools@latest` |
| Conta GitHub | Token no MCP |

**Repos que você precisa clonar:**

```powershell
# Vault Obsidian (KB + scripts RAG)
git clone https://github.com/gustavojordaob/fabrica-vault.git C:/Users/gusta/obsidian

# MCP central
git clone https://github.com/gustavojordaob/fabrica-apps-mcp.git C:/Users/gusta/fabrica-apps-mcp

# Apps (exemplos)
git clone ... C:/Users/gusta/projetos/LashMatch
git clone ... C:/Users/gusta/projetos/cortejo
```

### Configuração única do Cursor

**1. MCP** — arquivo `C:/Users/gusta/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "fabrica-apps": {
      "command": "node",
      "args": ["C:/Users/gusta/fabrica-apps-mcp/server-v2.js"],
      "env": {
        "GITHUB_TOKEN": "seu-token",
        "GITHUB_USER": "gustavojordaob",
        "FABRICA_PATH": "C:/Users/gusta/fabrica-apps-mcp"
      }
    }
  }
}
```

Adicione outros MCPs conforme [[mcps-cursor-padrao]] (mercadopago, revenuecat, firebase plugin, whatsapp).

**2. Hooks** — `C:/Users/gusta/.cursor/hooks.json` (copie da máquina principal ou do vault se versionado).

**3. Rules globais** — pasta `C:/Users/gusta/.cursor/rules/` com pelo menos:

- `rag-memoria-fabrica.mdc`
- `firebase-projeto-dinamico.mdc`
- `firebase-deploy-checklist.mdc`
- `documentacao-automatica-fabrica.mdc`

### Primeiro boot (toda sessão de dev)

```powershell
# Terminal 1 — servidor RAG (deixar aberto)
python C:/Users/gusta/obsidian/indexar_obsidian_chroma.py --server

# Se editou notas no Obsidian desde a última vez:
python C:/Users/gusta/obsidian/indexar_rapido.py
```

**Teste:**

1. Cursor → MCP → `fabrica-apps` → Restart
2. No chat: peça ao agente `rag_buscar("firebase deploy checklist")`
3. Deve retornar hits do Obsidian em **< 200 ms**, não aviso de offline

### Criar seu primeiro app pela fábrica

No chat do Cursor (com MCP ativo):

```
criar_projeto_completo
  nomeApp: "Meu Salão"
  descricao: "App de agenda para salão de beleza"
  publicoAlvo: "Donas de salão"
```

O MCP faz:

1. Repo no GitHub
2. Branch `feature/setup-inicial`
3. `PROJECT.md`, `.cursorrules`, rules do projeto
4. Pull Request
5. `git clone` em `C:/Users/gusta/projetos/`
6. Scaffold local

**Depois:** abra a pasta clonada no Cursor e peça telas (`obter_prompt_agente` ux → firebase → frontend → qa).

### Abrir app existente

1. Cursor → **File → Open Folder** → `C:/Users/gusta/projetos/LashMatch` (ou cortejo)
2. Confirme `.firebaserc` na raiz (hooks detectam project ID sozinhos)
3. Suba o RAG (`--server`)
4. Trabalhe normalmente — hooks consultam RAG antes de codar

---

## 4. Dia a dia — fluxos que você repete

### Perguntar / implementar algo

```
Você: "Implementa lembrete WhatsApp no agendamento"

Agente (automático):
  1. rag_buscar("agendamento whatsapp lembrete")
  2. buscar_historico("whatsapp agendamento")
  3. MCP whatsapp (se LashMatch/Cortejo)
  4. Lê código do repo
  5. Implementa seguindo fabrica/whatsapp-business-api.md
  6. salvar_decisao ou registrar_erro_solucao se aplicável
  7. Atualiza nota em fabrica/ se padrão reutilizável
```

### Feature nova em app existente

```
planejar_feature → criar_feature → código → publicar_funcionalidade → PR
```

### Depois de corrigir um bug

```
registrar_erro_solucao  →  reindexa RAG automaticamente
```

### Depois de decisão importante

```
salvar_decisao  →  reindexa RAG automaticamente
```

### Deploy Firebase

1. Abrir repo com `firebase.json` + `.firebaserc`
2. Agente chama `firebase_update_environment` (MCP plugin)
3. Seguir [[firebase-deploy-checklist-padrao]]
4. Hook pós-deploy lembra validação

### Comandos que você usa todo dia

```powershell
# RAG
python C:/Users/gusta/obsidian/indexar_obsidian_chroma.py --server
python C:/Users/gusta/obsidian/indexar_rapido.py   # após editar Obsidian

# App
cd C:/Users/gusta/projetos/LashMatch
npx expo start

# Deploy web
npx expo export --platform web
firebase deploy --only hosting

# Eval RAG (opcional, ao mudar retrieval)
python C:/Users/gusta/obsidian/fabrica/eval/run_baseline.py --regua v2
```

---

## 5. Como adicionar uma especialidade nova

Quando você quiser que a fábrica “saiba” de algo novo — **AWS**, **PostgreSQL**, **Stripe**, **Supabase**, etc. — siga este **protocolo em 7 passos**. Não pule etapas: a inteligência da fábrica vem da **nota + MCP + rule + índice**.

### Passo 1 — Decidir o tipo de integração

| Tipo | O que criar | Exemplo |
|------|-------------|---------|
| **A. Só conhecimento** | Nota `.md` na fábrica | Padrão de schema SQL, checklist RDS |
| **B. API consultável** | MCP novo ou remoto | AWS CLI wrapper, Stripe MCP oficial |
| **C. Híbrido (recomendado)** | Nota + MCP | PostgreSQL: doc de schema + MCP que roda queries read-only |

### Passo 2 — Criar a nota canônica no Obsidian

Arquivo: `C:/Users/gusta/obsidian/fabrica/<tema>-integration.md`

**Template obrigatório no topo:**

```markdown
---
tags: [integracao, aws, postgresql, fabrica]
atualizado_em: 2026-06-28
projeto: fabrica
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **<nome-do-mcp>** — consultar estado real
> 2. MCP **fabrica-apps** — `rag_buscar("<tema>")` + `buscar_historico("<tema>")`
> 3. Ler esta nota + código referenciado
> 4. Só então editar infra ou código

# <Título> — padrão fábrica

## Quando usar
## Arquitetura
## Variáveis / credenciais (sem secrets no Git)
## Checklist copiável
## Referência de código (repo/pasta)
## Erros comuns
```

Entrada em `fabrica/INDEX.md` → seção correspondente.

### Passo 3 — MCP (se a integração precisa de API real)

**Opção A — MCP remoto** (como Mercado Pago / RevenueCat):

```json
"meu-servico": {
  "url": "https://...",
  "headers": { "Authorization": "Bearer ${env:MEU_TOKEN}" }
}
```

**Opção B — MCP local Node** (como fabrica-apps):

```
C:/Users/gusta/projetos/mcp-aws-postgres/
  package.json
  src/index.js    ← expõe tools: list_tables, run_read_query, describe_rds...
```

Registrar em `~/.cursor/mcp.json`:

```json
"aws-postgres": {
  "command": "node",
  "args": ["C:/Users/gusta/projetos/mcp-aws-postgres/dist/index.js"],
  "env": {
    "AWS_REGION": "sa-east-1",
    "PGHOST": "xxx.rds.amazonaws.com",
    "PGUSER": "app_readonly"
  }
}
```

Secrets (`PGPASSWORD`, `AWS_SECRET_ACCESS_KEY`) → variáveis de ambiente do sistema ou Cursor secrets — **nunca** no Git.

### Passo 4 — Rule Cursor (quando o tema for frequente)

Arquivo: `~/.cursor/rules/<tema>-integracao.mdc` ou `.cursor/rules/` do projeto.

Exemplo mínimo:

```markdown
---
description: PostgreSQL na AWS — MCP + RAG obrigatório
alwaysApply: false
globs: ["**/db/**", "**/*.sql", "**/prisma/**"]
---

Antes de alterar schema ou queries PostgreSQL:
1. MCP aws-postgres (se existir)
2. rag_buscar("postgresql schema padrao")
3. Nota fabrica/postgresql-aws-integration.md
```

### Passo 5 — Hook (opcional, só se quiser gate forte)

Em `rag-lib.js`, adicionar palavras-chave em `detectMandatoryRagDocs`:

```javascript
// exemplo
if (/postgresql|rds|aws/.test(query)) {
  mandatoryDocs.push('postgresql-aws-integration.md');
}
```

Só faça isso se a integração for crítica e você já viu a IA ignorar a nota.

### Passo 6 — Indexar e registrar decisão

```powershell
python C:/Users/gusta/obsidian/indexar_rapido.py
```

No Cursor:

```
salvar_decisao
  projeto: "fabrica"
  titulo: "Nova especialidade AWS PostgreSQL"
  decisao: "..."
  motivo: "..."
```

### Passo 7 — Validar

- [ ] `rag_buscar("<tema>")` retorna a nota nova no top-3
- [ ] MCP responde (se criou MCP)
- [ ] Agente em projeto teste segue MCP + RAG antes de codar
- [ ] Golden set: adicionar 1–2 pares em `fabrica/eval/golden-set.jsonl` (opcional mas recomendado)

---

## 6. Exemplo completo: AWS + PostgreSQL

Cenário: você quer apps que usem **RDS PostgreSQL na AWS** em vez de (ou além de) Firestore.

### 6.1 Nota `fabrica/postgresql-aws-integration.md`

Conteúdo mínimo que a IA precisa:

```markdown
# PostgreSQL na AWS — padrão fábrica

## Stack
- RDS PostgreSQL 15 (sa-east-1)
- Acesso: usuário `app_readonly` (MCP) + `app_migrate` (CI only)
- ORM sugerido: Drizzle ou Prisma (decidir por projeto)

## Conexão (Cloud Function / backend)
- Secret: `DATABASE_URL` no Firebase Secrets ou AWS Secrets Manager
- Pool: max 5 conexões por instância serverless
- Nunca expor connection string no app mobile

## Schema padrão multi-tenant
- `tenants(id, name, ...)`
- `appointments(tenant_id, ..., FOREIGN KEY tenant_id)`
- Row Level Security se usar Supabase; em RDS, filtrar `tenant_id` na app layer

## MCP aws-postgres (ferramentas)
| Tool | Uso |
|------|-----|
| `pg_list_tables` | schema público |
| `pg_describe_table` | colunas + tipos |
| `pg_run_readonly` | SELECT only (sem DDL) |

## Checklist novo projeto com Postgres
- [ ] RDS criado, security group só VPC/Lambda
- [ ] Migrations versionadas (`migrations/001_init.sql`)
- [ ] Nota de schema em `fabrica/<app>-schemas-postgres.md`
- [ ] MCP configurado + testado
- [ ] `salvar_decisao` registrando escolha RDS vs Firestore

## Quando NÃO usar Postgres na fábrica
- App mobile Expo padrão salão → Firestore continua default (offline, rules, já documentado)
- Postgres faz sentido: relatórios pesados, BI, integração legado, SINAFLOR-like
```

### 6.2 MCP mínimo (estrutura)

```
mcp-aws-postgres/
├── package.json
├── src/
│   ├── index.js          # servidor MCP stdio
│   └── pg-client.js      # pool pg, só SELECT
└── README.md
```

Tools expostas:

| name | description |
|------|-------------|
| `pg_list_tables` | Lista tabelas do schema `public` |
| `pg_describe_table` | `\d` equivalente |
| `pg_run_readonly` | Executa SELECT (bloqueia INSERT/UPDATE/DELETE/DROP) |

### 6.3 Atualizar `mcps-cursor-padrao.md`

Adicionar linha na tabela:

| Tema | MCP | Doc |
|------|-----|-----|
| PostgreSQL / RDS AWS | **aws-postgres** | [[postgresql-aws-integration]] |

### 6.4 Rule global (snippet)

Arquivo `~/.cursor/rules/postgresql-aws.mdc`:

```markdown
---
description: PostgreSQL AWS — consultar MCP e RAG antes de schema/SQL
globs: ["**/*.sql", "**/drizzle/**", "**/prisma/**"]
---

- MCP **aws-postgres** para inspecionar banco real
- `rag_buscar("postgresql aws schema")` antes de migrations
- Firestore continua default para apps Expo salão — Postgres só se PRD disser
```

### 6.5 Primeiro uso no chat

```
Quero adicionar relatório financeiro em PostgreSQL no app X.

Agente deve:
1. rag_buscar("postgresql aws")
2. MCP pg_list_tables
3. Propor migration + Cloud Function read-only
4. Documentar em fabrica/x-schemas-postgres.md
5. salvar_decisao
```

---

## 7. RAG — como funciona por dentro

### Fluxo de indexação

```
fabrica/*.md  +  projetos/*-prd.md
        │
        ▼
 indexar_rapido.py
   • chunk por seção
   • metadado tipo_doc: padrao | spec | solucao | eval
   • exclui fabrica/eval/ do índice
        │
        ▼
   .chroma_db/  (embeddings)
        │
        ▼
 indexar_obsidian_chroma.py --server
   • carrega Chroma + BM25 (warmup)
   • HTTP GET /buscar?q=...
        │
        ▼
 MCP rag_buscar / buscar_historico
```

### Ferramentas de memória (MCP fabrica-apps)

| Ferramenta | Grava onde | Reindexa? |
|------------|------------|-----------|
| `salvar_decisao` | `decisoes.md` | Sim |
| `registrar_erro_solucao` | `erros-e-solucoes.md` | Sim |
| `atualizar_padrao` | nota `.md` indicada | Sim |
| `buscar_solucao` | lê erros + RAG | — |

### O que NÃO é base de conhecimento

| Arquivo | Papel |
|---------|-------|
| `CLAUDE.md` no repo do app | Ponte curta (~50 linhas) — Cursor injeta, **não indexar como KB** |
| `docs/archive/CLAUDE-monolito-historico.md` | Histórico — não usar |
| Fallback TF-IDF antigo | **Removido** — servidor offline = aviso |

### Avaliação de qualidade (harness)

| Arquivo | Função |
|---------|--------|
| `fabrica/eval/golden-set.jsonl` | 25 perguntas + nota esperada + `aceitaveis` |
| `fabrica/eval/run_baseline.py` | Mede hit@1, hit@3, MRR |
| `fabrica/eval/report-baseline-v2.json` | Baseline oficial |

Use ao mudar retrieval ou indexação.

---

## 8. Troubleshooting rápido

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| `Servidor RAG offline` | `:7332` parado | `python .../indexar_obsidian_chroma.py --server` |
| Query lenta (~2 s) | MCP usa `localhost` | Usar `127.0.0.1` (já corrigido no MCP hotpath) |
| IA codou sem padrão | Não chamou RAG | Verificar hooks + restart Cursor |
| Deploy Firebase errado | Project ID de outro app | Abrir repo certo; `.firebaserc` |
| RAG acha doc velho | Não reindexou | `indexar_rapido.py` |
| MCP fabrica-apps morto | Node crash | Cursor → MCP → Restart |
| Resposta genérica demais | Nota não existe | Criar `fabrica/<tema>.md` + indexar |

**Healthcheck:**

```powershell
python C:/Users/gusta/obsidian/indexar_obsidian_chroma.py --server
# Em outro terminal:
curl "http://127.0.0.1:7332/buscar?q=arquitetura+fabrica"
```

---

## 9. Mapa de pastas

```
C:/Users/gusta/
├── .cursor/
│   ├── mcp.json                 ← MCPs (fabrica, firebase, MP, RC…)
│   ├── rules/                   ← regras globais .mdc
│   └── hooks/                   ← automação RAG + Firebase
│
├── obsidian/                    ← REPO fabrica-vault (GitHub)
│   ├── fabrica/                 ← 📚 BASE DE CONHECIMENTO
│   │   ├── guia-completo-usuario-fabrica.md   ← ESTE ARQUIVO
│   │   ├── arquitetura-fabrica-ia.md          ← doc técnico canônico
│   │   ├── mcps-cursor-padrao.md
│   │   ├── INDEX.md
│   │   ├── decisoes.md
│   │   ├── erros-e-solucoes.md
│   │   └── … (padrões por tema)
│   ├── projetos/                ← PRDs (lashmatch-prd, cortejo-prd)
│   ├── indexar_rapido.py
│   └── indexar_obsidian_chroma.py
│
├── fabrica-apps-mcp/
│   └── server-v2.js             ← MCP central (~28 tools)
│
└── projetos/
    ├── LashMatch/
    └── cortejo/
```

**Baixar / levar para outro PC:**

1. Clone `fabrica-vault` → pasta `obsidian`
2. Clone `fabrica-apps-mcp`
3. Copie `~/.cursor/mcp.json`, `rules/`, `hooks/` (ou exporte do PC principal)
4. Configure tokens (GitHub, Firebase, Meta…) nas env vars
5. Rode `pip install` deps do RAG + `indexar_rapido.py` + `--server`

---

## 10. Pitch de 30 segundos

> “Montei uma fábrica de apps: o Cursor consulta meu Obsidian antes de codar, cria repositório e PR sozinho, lembra dos erros que já corrigi, e segue o mesmo stack Expo + Firebase em todo projeto. Busca híbrida (semântica + BM25) responde em ~80 ms. Se o servidor cai, eu sei na hora — não mascarar com doc velho. Eu foco em produto e teste; a IA foca em padrão, memória e Git. Quando quero uma especialidade nova — AWS, Postgres, Stripe — sigo o protocolo: nota + MCP + rule + indexar.”

---

## Links relacionados (no Obsidian)

- [[arquitetura-fabrica-ia]] — documentação técnica detalhada (hooks, eval, diagramas)
- [[mcps-cursor-padrao]] — MCPs configurados hoje
- [[rag-protocolo-antes-de-codar]] — antes de usar lib externa
- [[padroes-fabrica]] — padrões Expo/Firebase
- [[INDEX]] — índice completo da base

---

*Autor: Gustavo · Última atualização: 28/jun/2026*

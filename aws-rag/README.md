# Fábrica RAG na AWS (App Runner)

> Pacote completo: Docker + Terraform + scripts PowerShell.
> Path escolhido: **App Runner + ECR + S3** (~US$ 12–30/mês), sem Bedrock/SageMaker.
>
> **Região: `us-east-1`** — App Runner **não existe** em `sa-east-1`.

## Produção (jul/2026)

| | |
|--|--|
| URL | `https://gmnxgbtjy9.us-east-1.awsapprunner.com` |
| Health | `GET /health` → `{ ok, ready }` |
| Buscar | `GET /buscar?q=...` + header `X-RAG-Key` |
| API key | `cd aws-rag/terraform; terraform output -raw rag_api_key` |

## O que sobe

| Recurso | Função |
|---------|--------|
| **ECR** `fabrica-rag` | Imagem Docker (Python + MiniLM + Chroma client) |
| **S3** `fabrica-rag-<account>` | Índice `.chroma_db` sincronizado do PC |
| **App Runner** | HTTP `/health` + `/buscar?q=` (header `X-RAG-Key`) |

Build context = pasta **`obsidian/`** (não `aws-rag/` sozinha).

```text
obsidian/
├── indexar_*.py, rag_retrieval.py
├── .chroma_db/          ← gerado local, sync → S3
└── aws-rag/
    ├── Dockerfile
    ├── entrypoint.sh    ← baixa chroma do S3 no boot
    ├── requirements.txt
    ├── terraform/
    └── scripts/
```

## Pré-requisitos

1. Conta AWS + CLI (`aws configure`)
2. Terraform ≥ 1.5
3. Docker Desktop
4. Python local com deps da fábrica (para `indexar_rapido.py`)

## Deploy (ordem)

### 1) Infra parcial (ECR + S3 + IAM) — sem App Runner ainda

```powershell
cd C:\Users\gusta\obsidian\aws-rag\terraform
Copy-Item terraform.tfvars.example terraform.tfvars
# edite region/cpu se quiser

terraform init
terraform apply -target=aws_ecr_repository.rag `
  -target=aws_s3_bucket.rag `
  -target=aws_s3_bucket_versioning.rag `
  -target=aws_s3_bucket_public_access_block.rag `
  -target=aws_s3_bucket_server_side_encryption_configuration.rag `
  -target=aws_iam_role.apprunner_ecr `
  -target=aws_iam_role_policy_attachment.apprunner_ecr `
  -target=aws_iam_role.apprunner_instance `
  -target=aws_iam_role_policy.apprunner_s3 `
  -target=random_password.rag_api_key
```

Ou: `..\scripts\bootstrap.ps1`

### 2) Indexar vault + subir Chroma pro S3

```powershell
cd C:\Users\gusta\obsidian
.\aws-rag\scripts\sync-push.ps1
```

### 3) Build e push da imagem

```powershell
.\aws-rag\scripts\build-push.ps1
```

Primeiro build demora (baixa torch + modelo HuggingFace na imagem).

### 4) Criar App Runner

```powershell
cd aws-rag\terraform
terraform apply
```

Anote:

```powershell
terraform output service_url
terraform output buscar_url
terraform output -raw rag_api_key
```

### 5) Testar

```powershell
cd C:\Users\gusta\obsidian
.\aws-rag\scripts\test-remote.ps1
```

### 6) Apontar o MCP Cursor

Em `~/.cursor/mcp.json` (servidor `fabrica-apps`), configure a URL remota se o MCP aceitar env, por exemplo:

```json
"env": {
  "RAG_BASE_URL": "https://xxxxx.us-east-1.awsapprunner.com",
  "RAG_API_KEY": "<terraform output -raw rag_api_key>"
}
```

O MCP local continua podendo usar `http://127.0.0.1:7332` no PC; remoto é para outro notebook / CI / backup.

## Atualizar o índice (após editar Obsidian)

```powershell
cd C:\Users\gusta\obsidian
.\aws-rag\scripts\sync-push.ps1
```

O upload de `chroma/chroma.sqlite3` dispara a Lambda `fabrica-rag-restart-on-chroma`, que reinicia o App Runner sozinho.

Alarmes: SNS `fabrica-rag-alerts` (confirme o e-mail no inbox). Force manual só se precisar:

```powershell
aws apprunner start-deployment --service-arn <ARN> --region us-east-1
```

## Custo aproximado (us-east-1)

| Item | Estimativa |
|------|------------|
| App Runner 1 vCPU / 4 GB (quase idle) | ~US$ 15–25/mês |
| ECR + S3 | < US$ 2 |
| Transferência | baixa (só sync ocasional) |

Use `sa-east-1` se preferir latência BR (um pouco mais caro).

## Segurança

- `/buscar` exige `X-RAG-Key` quando `RAG_API_KEY` está setado (Terraform sempre seta).
- `/health` é público (sem dados).
- S3 sem acesso público; App Runner só lê o bucket.

## Destroy

```powershell
cd aws-rag\terraform
# esvazie S3 se necessário; force_delete no ECR se quiser
terraform destroy
```

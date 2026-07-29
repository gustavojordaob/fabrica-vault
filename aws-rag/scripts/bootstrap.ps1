# Fase 1: ECR + S3 + IAM (sem App Runner — precisa da imagem no ECR antes)
# Uso:
#   cd C:\Users\gusta\obsidian
#   .\aws-rag\scripts\bootstrap.ps1

$ErrorActionPreference = "Stop"
$TfDir = Resolve-Path (Join-Path $PSScriptRoot "..\terraform")
Set-Location $TfDir

if (-not (Test-Path "terraform.tfvars")) {
  Copy-Item "terraform.tfvars.example" "terraform.tfvars"
  Write-Host "Criado terraform.tfvars a partir do example — revise se quiser." -ForegroundColor Yellow
}

Write-Host "=== terraform init ===" -ForegroundColor Cyan
terraform init

Write-Host "`n=== terraform apply (targets: ECR+S3+IAM) ===" -ForegroundColor Cyan
terraform apply `
  -target=aws_ecr_repository.rag `
  -target=aws_ecr_lifecycle_policy.rag `
  -target=aws_s3_bucket.rag `
  -target=aws_s3_bucket_versioning.rag `
  -target=aws_s3_bucket_public_access_block.rag `
  -target=aws_s3_bucket_server_side_encryption_configuration.rag `
  -target=aws_iam_role.apprunner_ecr `
  -target=aws_iam_role_policy_attachment.apprunner_ecr `
  -target=aws_iam_role.apprunner_instance `
  -target=aws_iam_role_policy.apprunner_s3 `
  -target=random_password.rag_api_key

Write-Host "`nPróximos passos:" -ForegroundColor Green
Write-Host "  1. cd ..\.. ; .\aws-rag\scripts\sync-push.ps1"
Write-Host "  2. .\aws-rag\scripts\build-push.ps1"
Write-Host "  3. cd aws-rag\terraform ; terraform apply"
Write-Host "  4. .\aws-rag\scripts\test-remote.ps1"

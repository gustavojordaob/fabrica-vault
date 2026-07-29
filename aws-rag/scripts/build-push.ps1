# Build da imagem + push ECR
# Pre-requisito: terraform apply (cria ECR) + Docker Desktop rodando
# Uso (na pasta obsidian):
#   .\aws-rag\scripts\build-push.ps1

param(
  [string]$Tag = "latest",
  [string]$Region = ""
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$TfDir = Join-Path $Root "aws-rag\terraform"
Set-Location $Root

Push-Location $TfDir
$Repo = terraform output -raw ecr_repository_url
if (-not $Region) {
  $Region = terraform output -raw aws_region 2>$null
  if (-not $Region) { $Region = "sa-east-1" }
}
Pop-Location

if (-not $Repo) { throw "ECR vazio - rode terraform apply em aws-rag/terraform" }

$Account = ($Repo -split "\.")[0]
Write-Host "ECR:    $Repo"
Write-Host "Region: $Region"
Write-Host "Tag:    $Tag"

Write-Host "`n=== docker login ECR ===" -ForegroundColor Cyan
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin "$Account.dkr.ecr.$Region.amazonaws.com"
if ($LASTEXITCODE -ne 0) { throw "docker login falhou" }

Write-Host "`n=== docker build ===" -ForegroundColor Cyan
docker build -f aws-rag/Dockerfile -t "fabrica-rag:$Tag" .
if ($LASTEXITCODE -ne 0) { throw "docker build falhou" }

docker tag "fabrica-rag:$Tag" "${Repo}:${Tag}"
Write-Host "`n=== docker push ===" -ForegroundColor Cyan
docker push "${Repo}:${Tag}"
if ($LASTEXITCODE -ne 0) { throw "docker push falhou" }

Write-Host "`nOK: ${Repo}:${Tag}" -ForegroundColor Green
Write-Host "Se o App Runner ja existe, rode start-deployment ou terraform apply com image_tag=$Tag"

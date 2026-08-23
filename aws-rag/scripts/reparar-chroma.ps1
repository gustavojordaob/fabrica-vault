# Recria o Chroma local (HNSW) e publica no S3 us-east-1 (App Runner).
# Uso (na pasta obsidian):
#   .\aws-rag\scripts\reparar-chroma.ps1

param(
  [string]$Region = "us-east-1",
  [string]$Bucket = ""
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $Root

if (-not $Bucket) {
  Push-Location (Join-Path $Root "aws-rag\terraform")
  $Bucket = (terraform output -raw s3_bucket 2>$null)
  Pop-Location
}
if (-not $Bucket) {
  $Bucket = "fabrica-rag-084029330207-us-east-1"
}

Write-Host "=== Recriar Chroma (staging) + sync S3 $Region / $Bucket ===" -ForegroundColor Cyan
python (Join-Path $Root "indexar_rapido.py") --recriar-banco
if ($LASTEXITCODE -ne 0) { throw "indexar_rapido --recriar-banco falhou (exit $LASTEXITCODE)" }

& (Join-Path $PSScriptRoot "sync-push.ps1") -SkipIndex -Region $Region -Bucket $Bucket
if ($LASTEXITCODE -ne 0) { throw "sync-push falhou" }

Write-Host "`nAguarde o Lambda reiniciar o App Runner, depois:" -ForegroundColor Yellow
Write-Host "  .\aws-rag\scripts\test-remote.ps1 -Query `"trajeto daily agenda`""

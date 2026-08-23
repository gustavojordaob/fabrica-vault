# PowerShell — sobe índice Chroma local para o S3 do Terraform
# Uso (na pasta obsidian):
#   .\aws-rag\scripts\sync-push.ps1
#   .\aws-rag\scripts\sync-push.ps1 -SkipIndex

param(
  [switch]$SkipIndex,
  [string]$Region = "",
  [string]$Bucket = ""
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $Root

if (-not $Bucket -or -not $Region) {
  Push-Location (Join-Path $Root "aws-rag\terraform")
  if (-not $Bucket) {
    $Bucket = (terraform output -raw s3_bucket 2>$null)
  }
  if (-not $Region) {
    $Region = (terraform output -raw aws_region 2>$null)
  }
  Pop-Location
}

if (-not $Bucket) { throw "Informe -Bucket ou rode terraform apply antes (output s3_bucket)." }
if (-not $Region) { $Region = "us-east-1" }

Write-Host "Root:   $Root"
Write-Host "Bucket: $Bucket"
Write-Host "Region: $Region"

if (-not $SkipIndex) {
  Write-Host "`n=== indexar_rapido.py ===" -ForegroundColor Cyan
  python (Join-Path $Root "indexar_rapido.py")
  if ($LASTEXITCODE -ne 0) { throw "indexar_rapido falhou" }
}

$Chroma = Join-Path $Root ".chroma_db"
if (-not (Test-Path $Chroma)) { throw "Pasta .chroma_db não existe. Rode indexar_rapido.py" }

Write-Host "`n=== aws s3 sync chroma → s3://$Bucket/chroma/ ===" -ForegroundColor Cyan
aws s3 sync $Chroma "s3://$Bucket/chroma/" --region $Region --delete
if ($LASTEXITCODE -ne 0) { throw "s3 sync falhou" }

# Opcional: espelho do vault (debug / reindex futuro no cloud)
$Fabrica = Join-Path $Root "fabrica"
$Projetos = Join-Path $Root "projetos"
if (Test-Path $Fabrica) {
  aws s3 sync $Fabrica "s3://$Bucket/vault/fabrica/" --region $Region --exclude "eval/*" --exclude "aws-rag/*"
}
if (Test-Path $Projetos) {
  aws s3 sync $Projetos "s3://$Bucket/vault/projetos/" --region $Region
}

Write-Host "`nOK. Chroma no S3. O App Runner reinicia sozinho (Lambda no upload de chroma.sqlite3)." -ForegroundColor Green
Write-Host "  Se precisar forçar: aws apprunner start-deployment --service-arn <ARN> --region $Region"

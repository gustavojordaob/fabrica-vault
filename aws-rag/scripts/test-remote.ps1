# Testa o RAG remoto (health + buscar)
# Uso:
#   .\aws-rag\scripts\test-remote.ps1
#   .\aws-rag\scripts\test-remote.ps1 -Query "como fazer auth firebase"

param(
  [string]$Query = "login email senha firebase expo",
  [string]$BaseUrl = "",
  [string]$ApiKey = ""
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$TfDir = Join-Path $Root "aws-rag\terraform"

if (-not $BaseUrl -or -not $ApiKey) {
  Push-Location $TfDir
  if (-not $BaseUrl) { $BaseUrl = (terraform output -raw service_url) }
  if (-not $ApiKey) { $ApiKey = (terraform output -raw rag_api_key) }
  Pop-Location
}

$BaseUrl = $BaseUrl.TrimEnd("/")
Write-Host "GET $BaseUrl/health"
$h = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get
$h | ConvertTo-Json

$q = [uri]::EscapeDataString($Query)
Write-Host "`nGET $BaseUrl/buscar?q=..."
$headers = @{ "X-RAG-Key" = $ApiKey }
$r = Invoke-RestMethod -Uri "$BaseUrl/buscar?q=$q&n=3" -Headers $headers -Method Get
$r | ForEach-Object { Write-Host ("- " + $_.arquivo + " (" + $_.similaridade + ")") }

$ErrorActionPreference = 'Stop'
$port = if ($env:APP_PORT) { $env:APP_PORT } else { '8080' }
foreach ($path in @('/health','/api/products','/api/customers','/api/orders')) {
    $url = "http://localhost:$port$path"
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 15
    if ($response.StatusCode -ne 200) { throw "Falha: $url" }
    Write-Host "OK $url"
}
Write-Host 'Rotas verificadas.'

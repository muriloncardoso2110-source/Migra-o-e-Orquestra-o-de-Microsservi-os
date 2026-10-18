Set-Location (Join-Path $PSScriptRoot '..')
docker compose down
if ($LASTEXITCODE -ne 0) { throw 'Falha ao parar o ambiente' }

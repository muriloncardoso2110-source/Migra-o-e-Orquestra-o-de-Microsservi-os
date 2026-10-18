$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
docker info | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Docker nao esta acessivel. Abra o Docker Desktop.' }
docker compose up -d --build
if ($LASTEXITCODE -ne 0) { throw 'Falha ao iniciar containers.' }
Write-Host 'Acesse http://localhost:8080 e execute scripts/testar.ps1'

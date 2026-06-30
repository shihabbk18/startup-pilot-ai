Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Starting StartupPilot AI local stack..."
docker compose -f "$PSScriptRoot\..\docker-compose.yml" up --build


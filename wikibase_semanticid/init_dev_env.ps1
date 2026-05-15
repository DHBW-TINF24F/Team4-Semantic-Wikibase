$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

Write-Host "Starting docker compose stack..."
docker compose up -d

$containerName = "wbs-deploy-wikibase-1"
Write-Host "Waiting for container '$containerName' to become healthy..."

$maxRetries = 120
$retry = 0

while ($true) {
    $status = docker inspect --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}unknown{{end}}" $containerName 2>$null
    if ($status -eq "healthy") {
        break
    }

    $retry++
    if ($retry -ge $maxRetries) {
        throw "Timeout waiting for healthy status on $containerName. Last status: $status"
    }

    Start-Sleep -Seconds 5
}

Write-Host "Container is healthy. Seeding Main Page..."
docker compose exec -T wikibase sh -lc 'php /var/www/html/maintenance/edit.php "Main Page" < /setup/homepage.html'

Write-Host "Running CirrusSearch UpdateSearchIndexConfig..."
docker compose exec -T wikibase sh -lc '
if [ -f /var/www/html/extensions/CirrusSearch/maintenance/UpdateSearchIndexConfig.php ]; then
  php /var/www/html/extensions/CirrusSearch/maintenance/UpdateSearchIndexConfig.php
else
  php /var/www/html/maintenance/run.php CirrusSearch:UpdateSearchIndexConfig
fi
'

Write-Host "Running CirrusSearch ForceSearchIndex..."
docker compose exec -T wikibase sh -lc '
if [ -f /var/www/html/extensions/CirrusSearch/maintenance/ForceSearchIndex.php ]; then
  php /var/www/html/extensions/CirrusSearch/maintenance/ForceSearchIndex.php --skipLinks --indexOnSkip
else
  php /var/www/html/maintenance/run.php CirrusSearch:ForceSearchIndex -- --skipLinks --indexOnSkip
fi
'

Write-Host "Development environment initialized successfully."

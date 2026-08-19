# Script PowerShell pour rafraichir les donnees du DWH
# Usage: .\refresh_dwh.ps1

Write-Host "Rafraichissement du DWH en cours..." -ForegroundColor Cyan

# 1. Verifier que Docker est actif
Write-Host "`n[1/3] Verification de Docker..." -ForegroundColor Yellow
$containers = docker-compose ps --services --filter "status=running"
if ($containers.Count -lt 3) {
    Write-Host "Demarrage des conteneurs..." -ForegroundColor Yellow
    docker-compose up -d
    Start-Sleep -Seconds 5
}

# 2. Executer les extractions via Airflow CLI
Write-Host "`n[2/3] Extraction des donnees..." -ForegroundColor Yellow
$dags = @(
    "esofa_extract_categories",
    "esofa_extract_products",
    "esofa_extract_customers",
    "esofa_extract_sales"
)

foreach ($dag in $dags) {
    Write-Host "  -> Declenchement $dag..." -ForegroundColor Gray
    docker-compose exec -T airflow airflow dags trigger $dag
    Start-Sleep -Seconds 2
}

Write-Host "  Attente de la fin des extractions (60s)..." -ForegroundColor Green
Start-Sleep -Seconds 60

# 3. Rafraichir dbt
Write-Host "`n[3/3] Transformation des donnees (dbt)..." -ForegroundColor Yellow
Set-Location "D:\Projet Stage M2\dwh_project"
dbt run
dbt test

Write-Host "`nRafraichissement termine!" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:8501" -ForegroundColor Cyan
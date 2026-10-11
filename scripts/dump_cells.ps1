$projectDir = Split-Path $PSScriptRoot -Parent
$nbPath = Join-Path $projectDir "notebooks/PharmaForce360_Data_Generator.ipynb"

if (-not (Test-Path $nbPath)) {
    Write-Host "Notebook not found at: $nbPath" -ForegroundColor Red
    exit 1
}

$json = Get-Content -Raw -Encoding UTF8 $nbPath | ConvertFrom-Json

for ($i = 0; $i -lt $json.cells.Count; $i++) {
    $c = $json.cells[$i]
    if ($c.cell_type -eq 'code') {
        Write-Host "================================================================================"
        Write-Host "CELL $i CODE (Lines: $($c.source.Count))"
        Write-Host "================================================================================"
        $src = $c.source -join ''
        Write-Host $src
    }
}

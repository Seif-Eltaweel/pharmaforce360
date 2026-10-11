$projectDir = Split-Path $PSScriptRoot -Parent
$nbPath = Join-Path $projectDir "notebooks/PharmaForce360_Data_Generator.ipynb"

if (-not (Test-Path $nbPath)) {
    Write-Host "Notebook not found at: $nbPath" -ForegroundColor Red
    exit 1
}

$json = Get-Content -Raw -Encoding UTF8 $nbPath | ConvertFrom-Json
Write-Host "Total cells: $($json.cells.Count)"
$codeNum = 1
for ($i = 0; $i -lt $json.cells.Count; $i++) {
    $c = $json.cells[$i]
    if ($c.cell_type -eq 'code') {
        $first = if ($c.source.Count -gt 0) { $c.source[0].Trim() } else { "EMPTY" }
        Write-Host "Code Cell $codeNum [Index $i]: $first"
        $codeNum++
    }
}

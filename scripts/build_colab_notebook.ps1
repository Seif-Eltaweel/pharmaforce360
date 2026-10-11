# PowerShell Wrapper to generate PharmaForce360_Data_Generator.ipynb
param (
    [string]$ScriptDir = $PSScriptRoot
)

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Building PharmaForce 360 Google Colab Data Generator Notebook" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if ($pythonCmd) {
    $scriptPath = Join-Path $ScriptDir "generate_colab_notebook.py"
    & python $scriptPath
    Write-Host "`nNotebook successfully created at:" -ForegroundColor Green
    Write-Host "   - 02_PharmaForce360/notebooks/PharmaForce360_Data_Generator.ipynb" -ForegroundColor Yellow
    Write-Host "`nNext Step: Upload this notebook to Google Colab and select 'Runtime > Run all'." -ForegroundColor Cyan
} else {
    Write-Host "Python was not found in PATH." -ForegroundColor Red
}

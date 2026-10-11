$bim = Get-Content 'd:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.SemanticModel\model.bim' -Raw | ConvertFrom-Json
$distRels = $bim.model.relationships | Where-Object { $_.toTable -eq 'dim_distributor' -or $_.fromTable -eq 'dim_distributor' }

foreach ($r in $distRels) {
    Write-Host "$($r.name): $($r.fromTable).$($r.fromColumn) -> $($r.toTable).$($r.toColumn) (isActive = $($r.isActive))"
}

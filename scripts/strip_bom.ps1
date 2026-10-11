param(
    [string]$TargetFolder = "d:\portfolio2026\02_PharmaForce360\powerbi"
)

$fixedCount = 0
$totalCount = 0

Get-ChildItem -Path $TargetFolder -Recurse -File | ForEach-Object {
    $totalCount++
    $fileBytes = [System.IO.File]::ReadAllBytes($_.FullName)
    if ($fileBytes.Length -ge 3 -and $fileBytes[0] -eq 0xEF -and $fileBytes[1] -eq 0xBB -and $fileBytes[2] -eq 0xBF) {
        $cleanBytes = New-Object byte[] ($fileBytes.Length - 3)
        [System.Array]::Copy($fileBytes, 3, $cleanBytes, 0, $cleanBytes.Length)
        [System.IO.File]::WriteAllBytes($_.FullName, $cleanBytes)
        Write-Host "Stripped BOM: $($_.FullName)"
        $fixedCount++
    }
}

Write-Host "Finished checking $totalCount files."
Write-Host "Removed UTF-8 BOM from $fixedCount files."

# Verification check
$remaining = 0
Get-ChildItem -Path $TargetFolder -Recurse -File | ForEach-Object {
    $checkBytes = [System.IO.File]::ReadAllBytes($_.FullName)
    if ($checkBytes.Length -ge 3 -and $checkBytes[0] -eq 0xEF -and $checkBytes[1] -eq 0xBB -and $checkBytes[2] -eq 0xBF) {
        Write-Warning "File still has BOM: $($_.FullName)"
        $remaining++
    }
}

if ($remaining -eq 0) {
    Write-Host "VERIFICATION SUCCESS: All files are completely BOM-free!" -ForegroundColor Green
} else {
    Write-Error "VERIFICATION FAILED: $remaining files still contain BOM."
}

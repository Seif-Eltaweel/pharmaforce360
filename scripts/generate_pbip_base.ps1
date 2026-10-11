# ==============================================================================
# PharmaForce 360° Commercial Intelligence Suite — Power BI Project (.pbip) Generator
# Greater Cairo Pharmaceutical Market | Kimball Star Schema Architecture
# ==============================================================================

param(
    [string]$TargetDir = "d:\portfolio2026\02_PharmaForce360\powerbi",
    [string]$DataDir = "d:\portfolio2026\02_PharmaForce360\data"
)

Write-Host ">>> Initializing PharmaForce 360° PBIP Generator..." -ForegroundColor Cyan
Write-Host "Target Directory: $TargetDir"
Write-Host "Data Directory:   $DataDir"

# Ensure root & nested directories exist
$dirsToCreate = @(
    $TargetDir,
    (Join-Path $TargetDir "PharmaForce360.Report"),
    (Join-Path $TargetDir "PharmaForce360.Report\.pbi"),
    (Join-Path $TargetDir "PharmaForce360.Report\StaticResources"),
    (Join-Path $TargetDir "PharmaForce360.Report\StaticResources\RegisteredResources"),
    (Join-Path $TargetDir "PharmaForce360.SemanticModel"),
    (Join-Path $TargetDir "PharmaForce360.SemanticModel\.pbi"),
    (Join-Path $TargetDir "PharmaForce360.SemanticModel\definition"),
    (Join-Path $TargetDir "PharmaForce360.SemanticModel\definition\tables"),
    (Join-Path $TargetDir "PharmaForce360.SemanticModel\definition\cultures")
)

foreach ($d in $dirsToCreate) {
    if (-not (Test-Path $d)) {
        New-Item -Path $d -ItemType Directory -Force | Out-Null
    }
}

# UTF-8 without BOM encoding (required by Power BI Desktop .pbip format)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# ------------------------------------------------------------------------------
# 1. Root .pbip File
# ------------------------------------------------------------------------------
$pbipPath = Join-Path $TargetDir "PharmaForce360.pbip"
$pbipJson = @{
    version = "1.0"
    artifacts = @(
        @{
            report = @{
                path = "PharmaForce360.Report"
            }
        }
    )
    settings = @{
        enableAutoRecovery = $true
    }
} | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($pbipPath, $pbipJson, $utf8NoBom)
Write-Host "  [+] Created: PharmaForce360.pbip" -ForegroundColor Green

# ------------------------------------------------------------------------------
# 2. Report Definition Pointer (definition.pbir)
# ------------------------------------------------------------------------------
$pbirPath = Join-Path $TargetDir "PharmaForce360.Report\definition.pbir"
$pbirJson = @{
    version = "1.0"
    datasetReference = @{
        byPath = @{
            path = "../PharmaForce360.SemanticModel"
        }
        byConnection = $null
    }
} | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($pbirPath, $pbirJson, $utf8NoBom)
Write-Host "  [+] Created: definition.pbir" -ForegroundColor Green

# ------------------------------------------------------------------------------
# 3. Semantic Model Definition Pointer (definition.pbism)
# ------------------------------------------------------------------------------
$pbismPath = Join-Path $TargetDir "PharmaForce360.SemanticModel\definition.pbism"
$pbismJson = @{
    version = "1.0"
} | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($pbismPath, $pbismJson, $utf8NoBom)
Write-Host "  [+] Created: definition.pbism" -ForegroundColor Green

# Local settings
$localSettings = @{ version = "1.0" } | ConvertTo-Json
[System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.Report\.pbi\localSettings.json"), $localSettings, $utf8NoBom)
[System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.SemanticModel\.pbi\localSettings.json"), $localSettings, $utf8NoBom)
[System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.SemanticModel\.pbi\editorSettings.json"), $localSettings, $utf8NoBom)

# ------------------------------------------------------------------------------
# 4. Custom Theme JSON (Clinical & Corporate Aesthetic)
# ------------------------------------------------------------------------------
$themeObj = @{
    name = "PharmaForce360_Clinical"
    dataColors = @(
        "#0A2540", # Deep Navy (Primary)
        "#00A3E0", # Clinical Cyan (Brand Primary)
        "#00B4D8", # Medical Teal
        "#10B981", # Success / Above Target
        "#F59E0B", # Warning Amber
        "#EF4444", # Danger / Churn Risk
        "#6366F1", # Indigo / KOLs
        "#8B5CF6", # Violet / AI Copilot
        "#3B82F6", # Sky Blue
        "#14B8A6", # Emerald
        "#F97316", # Orange
        "#64748B"  # Slate Neutral
    )
    background = "#F8FAFC"
    foreground = "#0F172A"
    tableAccent = "#00A3E0"
    visualStyles = @{
        "*" = @{
            "*" = @{
                "*" = @{
                    responsive = $true
                }
                background = @(
                    @{
                        color = @{ solid = @{ color = "#FFFFFF" } }
                        transparency = 0
                    }
                )
                border = @(
                    @{
                        color = @{ solid = @{ color = "#E2E8F0" } }
                        radius = 8
                    }
                )
                visualHeader = @(
                    @{
                        foreground = @{ solid = @{ color = "#0A2540" } }
                    }
                )
            }
        }
        page = @{
            "*" = @{
                background = @(
                    @{
                        color = @{ solid = @{ color = "#F8FAFC" } }
                        transparency = 0
                    }
                )
            }
        }
    }
}
$themeJson = $themeObj | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText((Join-Path $TargetDir "theme.json"), $themeJson, $utf8NoBom)
[System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.Report\StaticResources\RegisteredResources\PharmaForce360Theme.json"), $themeJson, $utf8NoBom)
Write-Host "  [+] Created: theme.json & RegisteredResources/PharmaForce360Theme.json" -ForegroundColor Green

Write-Host ">>> Basic infrastructure created successfully." -ForegroundColor Cyan

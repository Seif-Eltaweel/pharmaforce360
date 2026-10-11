function New-TextBoxVisual {
    param([string]$Name, [int]$X, [int]$Y, [int]$W, [int]$H, [string]$Text)
    return @{
        name = $Name
        x = $X; y = $Y; z = 500; width = $W; height = $H
        text = $Text
    }
}

$v = New-TextBoxVisual -Name "Header" -X 20 -Y 15 -W 1240 -H 65 -Text "Executive Commercial and IQVIA Audit"
Write-Host "Success: $($v.name) -> $($v.text)"

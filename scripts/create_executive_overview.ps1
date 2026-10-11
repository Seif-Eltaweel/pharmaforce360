# ==============================================================================
# Script: create_executive_overview.ps1
# Creates the exact Executive Overview Dashboard (Page 1) matching the design image
# ==============================================================================

param(
    [string]$ReportJsonPath = "d:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\report.json"
)

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function New-ShapeVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 0,
        [string]$ShapeType = "rectangle",
        [string]$FillColor = "#071E54",
        [int]$RoundRadius = 0,
        [string]$BorderColor = "#071E54"
    )

    $tileShape = if ($RoundRadius -gt 0) { "'roundRectangle'" } else { "'$ShapeType'" }
    
    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "shape"
            drillFilterOtherVisuals = $true
            objects = @{
                shape = @(
                    @{
                        properties = @{
                            tileShape = @{ expr = @{ Literal = @{ Value = $tileShape } } }
                            roundPercentage = @{ expr = @{ Literal = @{ Value = "${RoundRadius}D" } } }
                        }
                    }
                )
                fill = @(
                    @{
                        properties = @{
                            fillColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'$FillColor'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                        }
                    }
                )
                outline = @(
                    @{
                        properties = @{
                            lineColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'$BorderColor'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                            weight = @{ expr = @{ Literal = @{ Value = "1D" } } }
                        }
                    }
                )
            }
        }
    }

    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

function New-TextVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 100,
        [string]$Text = "",
        [string]$Color = "#FFFFFF",
        [string]$FontSize = "11pt",
        [string]$FontFamily = "Segoe UI Semibold",
        [string]$BgColor = $null,
        [string]$BorderColor = $null,
        [int]$BorderRadius = 0
    )

    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "textbox"
            drillFilterOtherVisuals = $true
            objects = @{
                general = @(
                    @{
                        properties = @{
                            paragraphs = @(
                                @{
                                    textRuns = @(
                                        @{
                                            value = $Text
                                            textStyle = @{
                                                fontFamily = $FontFamily
                                                fontSize = $FontSize
                                                color = $Color
                                            }
                                        }
                                    )
                                }
                            )
                        }
                    }
                )
            }
        }
    }

    if ($BgColor) {
        $cfg.singleVisual["vcObjects"] = @{
            background = @(
                @{
                    properties = @{
                        color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'$BgColor'" } } } } }
                        transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                    }
                }
            )
        }
        if ($BorderColor) {
            $cfg.singleVisual.vcObjects["border"] = @(
                @{
                    properties = @{
                        color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'$BorderColor'" } } } } }
                        radius = @{ expr = @{ Literal = @{ Value = "${BorderRadius}D" } } }
                    }
                }
            )
        }
    }

    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

function New-SlicerVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 200,
        [string]$TableName,
        [string]$ColumnName,
        [string]$TitleText
    )

    $queryRef = "$TableName.$ColumnName"
    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "slicer"
            projections = @{
                Values = @( @{ queryRef = $queryRef } )
            }
            prototypeQuery = @{
                Version = 2
                From = @( @{ Name = "t"; Entity = $TableName; Type = 0 } )
                Select = @(
                    @{
                        Column = @{
                            Expression = @{ SourceRef = @{ Source = "t" } }
                            Property = $ColumnName
                        }
                        Name = $queryRef
                    }
                )
            }
            drillFilterOtherVisuals = $true
            objects = @{
                data = @(
                    @{
                        properties = @{
                            mode = @{ expr = @{ Literal = @{ Value = "'Dropdown'" } } }
                        }
                    }
                )
                header = @(
                    @{
                        properties = @{
                            text = @{ expr = @{ Literal = @{ Value = "'$TitleText'" } } }
                            fontColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0A2540'" } } } } }
                            textSize = @{ expr = @{ Literal = @{ Value = "10D" } } }
                            fontFamily = @{ expr = @{ Literal = @{ Value = "'Segoe UI Semibold'" } } }
                        }
                    }
                )
            }
            vcObjects = @{
                background = @(
                    @{
                        properties = @{
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#FFFFFF'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                        }
                    }
                )
                border = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#E2E8F0'" } } } } }
                            radius = @{ expr = @{ Literal = @{ Value = "8D" } } }
                        }
                    }
                )
            }
        }
    }

    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

function New-KpiCardVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 300,
        [string]$MeasureName,
        [string]$CardTitle
    )

    $queryRef = "_Measures.$MeasureName"
    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "card"
            projections = @{
                Values = @( @{ queryRef = $queryRef } )
            }
            prototypeQuery = @{
                Version = 2
                From = @( @{ Name = "m"; Entity = "_Measures"; Type = 0 } )
                Select = @(
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = $MeasureName
                        }
                        Name = $queryRef
                    }
                )
            }
            drillFilterOtherVisuals = $true
            objects = @{
                labels = @(
                    @{
                        properties = @{
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0F172A'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "22D" } } }
                            fontFamily = @{ expr = @{ Literal = @{ Value = "'Segoe UI Bold'" } } }
                        }
                    }
                )
                categoryLabels = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "false" } } }
                        }
                    }
                )
            }
            vcObjects = @{
                title = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            text = @{ expr = @{ Literal = @{ Value = "'$CardTitle'" } } }
                            fontColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#64748B'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "10D" } } }
                            fontFamily = @{ expr = @{ Literal = @{ Value = "'Segoe UI Semibold'" } } }
                            alignment = @{ expr = @{ Literal = @{ Value = "'Center'" } } }
                        }
                    }
                )
                background = @(
                    @{
                        properties = @{
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#FFFFFF'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                        }
                    }
                )
                border = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#E2E8F0'" } } } } }
                            radius = @{ expr = @{ Literal = @{ Value = "8D" } } }
                        }
                    }
                )
            }
        }
    }

    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

function New-LineAreaChartVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 300,
        [string]$TitleText = "Gross Revenue and Market Share"
    )

    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "lineChart"
            projections = @{
                Category = @(
                    @{
                        queryRef = "dim_date.Month"
                        active = $true
                    }
                )
                Y = @(
                    @{
                        queryRef = "_Measures.Total Revenue EGP"
                    }
                )
                Y2 = @(
                    @{
                        queryRef = "_Measures.IMS Market Share Pct"
                    }
                )
            }
            prototypeQuery = @{
                Version = 2
                From = @(
                    @{ Name = "d"; Entity = "dim_date"; Type = 0 },
                    @{ Name = "m"; Entity = "_Measures"; Type = 0 }
                )
                Select = @(
                    @{
                        Column = @{
                            Expression = @{ SourceRef = @{ Source = "d" } }
                            Property = "Month"
                        }
                        Name = "dim_date.Month"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "Total Revenue EGP"
                        }
                        Name = "_Measures.Total Revenue EGP"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "IMS Market Share Pct"
                        }
                        Name = "_Measures.IMS Market Share Pct"
                    }
                )
            }
            drillFilterOtherVisuals = $true
            objects = @{
                lineStyles = @(
                    @{
                        properties = @{
                            shadeArea = @{ expr = @{ Literal = @{ Value = "true" } } }
                            strokeWidth = @{ expr = @{ Literal = @{ Value = "3D" } } }
                        }
                    }
                )
                dataPoint = @(
                    @{
                        properties = @{
                            fill = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#00C2FF'" } } } } }
                        }
                        selector = @{
                            data = @(
                                @{
                                    dataViewWildcard = @{
                                        matchingOption = 1
                                    }
                                }
                            )
                        }
                    }
                )
            }
            vcObjects = @{
                title = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            text = @{ expr = @{ Literal = @{ Value = "'$TitleText'" } } }
                            fontColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0A2540'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "12D" } } }
                            fontFamily = @{ expr = @{ Literal = @{ Value = "'Segoe UI Semibold'" } } }
                        }
                    }
                )
                background = @(
                    @{
                        properties = @{
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#FFFFFF'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                        }
                    }
                )
                border = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#E2E8F0'" } } } } }
                            radius = @{ expr = @{ Literal = @{ Value = "8D" } } }
                        }
                    }
                )
            }
        }
    }

    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

function New-MapVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 300,
        [string]$TitleText = "Top Performing Cairo Bricks (Spatial Distribution)"
    )

    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "shapeMap"
            projections = @{
                Category = @( @{ queryRef = "dim_brick_territory.Brick_Name"; active = $true } )
                ColorSaturation = @( @{ queryRef = "_Measures.Total Revenue EGP" } )
                Tooltips = @(
                    @{ queryRef = "dim_brick_territory.Zone" },
                    @{ queryRef = "dim_brick_territory.Tier" },
                    @{ queryRef = "_Measures.Total Revenue EGP" },
                    @{ queryRef = "_Measures.IMS Market Share Pct" },
                    @{ queryRef = "_Measures.Evolution Index EI" },
                    @{ queryRef = "_Measures.Target Attainment Pct" }
                )
            }
            prototypeQuery = @{
                Version = 2
                From = @(
                    @{ Name = "b"; Entity = "dim_brick_territory"; Type = 0 },
                    @{ Name = "m"; Entity = "_Measures"; Type = 0 }
                )
                Select = @(
                    @{
                        Column = @{
                            Expression = @{ SourceRef = @{ Source = "b" } }
                            Property = "Brick_Name"
                        }
                        Name = "dim_brick_territory.Brick_Name"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "Total Revenue EGP"
                        }
                        Name = "_Measures.Total Revenue EGP"
                    },
                    @{
                        Column = @{
                            Expression = @{ SourceRef = @{ Source = "b" } }
                            Property = "Zone"
                        }
                        Name = "dim_brick_territory.Zone"
                    },
                    @{
                        Column = @{
                            Expression = @{ SourceRef = @{ Source = "b" } }
                            Property = "Tier"
                        }
                        Name = "dim_brick_territory.Tier"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "IMS Market Share Pct"
                        }
                        Name = "_Measures.IMS Market Share Pct"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "Evolution Index EI"
                        }
                        Name = "_Measures.Evolution Index EI"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "Target Attainment Pct"
                        }
                        Name = "_Measures.Target Attainment Pct"
                    }
                )
            }
            drillFilterOtherVisuals = $true
            objects = @{
                shape = @(
                    @{
                        properties = @{
                            map = @{
                                type = @{ expr = @{ Literal = @{ Value = "'custom'" } } }
                                name = @{ expr = @{ Literal = @{ Value = "'cairo_commercial_bricks'" } } }
                            }
                            projection = @{ expr = @{ Literal = @{ Value = "'mercator'" } } }
                        }
                    }
                )
                dataLabels = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0A2540'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "8D" } } }
                        }
                    }
                )
                dataPoint = @(
                    @{
                        properties = @{
                            fillMin = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#EF4444'" } } } } }
                            fillMid = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#E2E8F0'" } } } } }
                            fillMax = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#00A3E0'" } } } } }
                        }
                    }
                )
            }
            vcObjects = @{
                title = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            text = @{ expr = @{ Literal = @{ Value = "'$TitleText'" } } }
                            fontColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0A2540'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "11D" } } }
                            fontFamily = @{ expr = @{ Literal = @{ Value = "'Segoe UI Semibold'" } } }
                        }
                    }
                )
                background = @(
                    @{
                        properties = @{
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#FFFFFF'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                        }
                    }
                )
                border = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#E2E8F0'" } } } } }
                            radius = @{ expr = @{ Literal = @{ Value = "8D" } } }
                        }
                    }
                )
            }
        }
    }


    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

function New-BarChartVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 300,
        [string]$TitleText = "Cairo Brick Performance"
    )

    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "clusteredBarChart"
            projections = @{
                Category = @( @{ queryRef = "dim_brick_territory.Brick_Name"; active = $true } )
                Y = @( @{ queryRef = "_Measures.IMS Market Share Pct" } )
            }
            prototypeQuery = @{
                Version = 2
                From = @(
                    @{ Name = "b"; Entity = "dim_brick_territory"; Type = 0 },
                    @{ Name = "m"; Entity = "_Measures"; Type = 0 }
                )
                Select = @(
                    @{
                        Column = @{
                            Expression = @{ SourceRef = @{ Source = "b" } }
                            Property = "Brick_Name"
                        }
                        Name = "dim_brick_territory.Brick_Name"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "IMS Market Share Pct"
                        }
                        Name = "_Measures.IMS Market Share Pct"
                    }
                )
            }
            drillFilterOtherVisuals = $true
            objects = @{
                labels = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0F172A'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "9D" } } }
                        }
                    }
                )
                dataPoint = @(
                    @{
                        properties = @{
                            fill = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#00A3E0'" } } } } }
                        }
                    }
                )
            }
            vcObjects = @{
                title = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            text = @{ expr = @{ Literal = @{ Value = "'$TitleText'" } } }
                            fontColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0A2540'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "11D" } } }
                            fontFamily = @{ expr = @{ Literal = @{ Value = "'Segoe UI Semibold'" } } }
                        }
                    }
                )
                background = @(
                    @{
                        properties = @{
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#FFFFFF'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                        }
                    }
                )
                border = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#E2E8F0'" } } } } }
                            radius = @{ expr = @{ Literal = @{ Value = "8D" } } }
                        }
                    }
                )
            }
        }
    }

    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

function New-ColumnChartVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 300,
        [string]$TitleText = "Distributor Market Share"
    )

    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "clusteredColumnChart"
            projections = @{
                Category = @( @{ queryRef = "dim_distributor.Distributor_Name"; active = $true } )
                Y = @( @{ queryRef = "_Measures.IMS Market Share Pct" } )
            }
            prototypeQuery = @{
                Version = 2
                From = @(
                    @{ Name = "d"; Entity = "dim_distributor"; Type = 0 },
                    @{ Name = "m"; Entity = "_Measures"; Type = 0 }
                )
                Select = @(
                    @{
                        Column = @{
                            Expression = @{ SourceRef = @{ Source = "d" } }
                            Property = "Distributor_Name"
                        }
                        Name = "dim_distributor.Distributor_Name"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "IMS Market Share Pct"
                        }
                        Name = "_Measures.IMS Market Share Pct"
                    }
                )
            }
            drillFilterOtherVisuals = $true
            objects = @{
                labels = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0F172A'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "9D" } } }
                        }
                    }
                )
                dataPoint = @(
                    @{
                        properties = @{
                            fill = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#00A3E0'" } } } } }
                        }
                    }
                )
            }
            vcObjects = @{
                title = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            text = @{ expr = @{ Literal = @{ Value = "'$TitleText'" } } }
                            fontColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0A2540'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "11D" } } }
                            fontFamily = @{ expr = @{ Literal = @{ Value = "'Segoe UI Semibold'" } } }
                        }
                    }
                )
                background = @(
                    @{
                        properties = @{
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#FFFFFF'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                        }
                    }
                )
                border = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#E2E8F0'" } } } } }
                            radius = @{ expr = @{ Literal = @{ Value = "8D" } } }
                        }
                    }
                )
            }
        }
    }

    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

function New-ComboChartVisual {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [double]$W,
        [double]$H,
        [double]$Z = 300,
        [string]$TitleText = "Call Attainment Tier Segmentation"
    )

    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = $Z; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "lineClusteredColumnComboChart"
            projections = @{
                Category = @( @{ queryRef = "dim_doctor.Classification"; active = $true } )
                Y = @( @{ queryRef = "_Measures.Total Field Visits" } )
                Y2 = @( @{ queryRef = "_Measures.Plan Adherence Pct" } )
            }
            prototypeQuery = @{
                Version = 2
                From = @(
                    @{ Name = "doc"; Entity = "dim_doctor"; Type = 0 },
                    @{ Name = "m"; Entity = "_Measures"; Type = 0 }
                )
                Select = @(
                    @{
                        Column = @{
                            Expression = @{ SourceRef = @{ Source = "doc" } }
                            Property = "Classification"
                        }
                        Name = "dim_doctor.Classification"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "Total Field Visits"
                        }
                        Name = "_Measures.Total Field Visits"
                    },
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = "Plan Adherence Pct"
                        }
                        Name = "_Measures.Plan Adherence Pct"
                    }
                )
            }
            drillFilterOtherVisuals = $true
            objects = @{
                dataPoint = @(
                    @{
                        properties = @{
                            fill = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#00B4D8'" } } } } }
                        }
                    }
                )
                lineStyles = @(
                    @{
                        properties = @{
                            strokeWidth = @{ expr = @{ Literal = @{ Value = "3D" } } }
                        }
                    }
                )
            }
            vcObjects = @{
                title = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            text = @{ expr = @{ Literal = @{ Value = "'$TitleText'" } } }
                            fontColor = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#0A2540'" } } } } }
                            fontSize = @{ expr = @{ Literal = @{ Value = "11D" } } }
                            fontFamily = @{ expr = @{ Literal = @{ Value = "'Segoe UI Semibold'" } } }
                        }
                    }
                )
                background = @(
                    @{
                        properties = @{
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#FFFFFF'" } } } } }
                            transparency = @{ expr = @{ Literal = @{ Value = "0D" } } }
                        }
                    }
                )
                border = @(
                    @{
                        properties = @{
                            show = @{ expr = @{ Literal = @{ Value = "true" } } }
                            color = @{ solid = @{ color = @{ expr = @{ Literal = @{ Value = "'#E2E8F0'" } } } } }
                            radius = @{ expr = @{ Literal = @{ Value = "8D" } } }
                        }
                    }
                )
            }
        }
    }

    return @{
        x = $X; y = $Y; z = $Z; width = $W; height = $H
        filters = "[]"
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
    }
}

# ------------------------------------------------------------------------------
# Assemble Visual Containers for Executive Overview Page
# ------------------------------------------------------------------------------
Write-Host ">>> Generating Executive Overview Visual Containers..." -ForegroundColor Cyan

$execVisuals = @()

# 1. Left Sidebar Background Shape
$execVisuals += New-ShapeVisual -Name "Sidebar_Background" -X 0 -Y 0 -W 205 -H 720 -Z 0 -FillColor "#071E54" -BorderColor "#071E54"

# 2. Sidebar Header Logo
$execVisuals += New-TextVisual -Name "Sidebar_Brand" -X 10 -Y 16 -W 185 -H 55 -Z 100 -Text "⚕️ PharmaForce 360°" -Color "#FFFFFF" -FontSize "14pt" -FontFamily "Segoe UI Bold"

# 3. Sidebar Active Pill for "Executive Overview"
$execVisuals += New-ShapeVisual -Name "Sidebar_Active_Pill" -X 10 -Y 138 -W 185 -H 42 -Z 50 -FillColor "#00A3E0" -RoundRadius 10 -BorderColor "#00A3E0"
$execVisuals += New-TextVisual -Name "Sidebar_Nav_1_Active" -X 18 -Y 145 -W 170 -H 32 -Z 100 -Text "⊞  Executive Overview" -Color "#FFFFFF" -FontSize "11pt" -FontFamily "Segoe UI Semibold"

# 4. Sidebar Inactive Menu Items
$execVisuals += New-TextVisual -Name "Sidebar_Nav_2" -X 18 -Y 198 -W 175 -H 32 -Z 100 -Text "👨‍⚕️  Doctors (KOLs)" -Color "#CFE0F5" -FontSize "10.5pt"
$execVisuals += New-TextVisual -Name "Sidebar_Nav_3" -X 18 -Y 248 -W 175 -H 32 -Z 100 -Text "👥  Medical Representatives" -Color "#CFE0F5" -FontSize "10.5pt"
$execVisuals += New-TextVisual -Name "Sidebar_Nav_4" -X 18 -Y 298 -W 175 -H 32 -Z 100 -Text "🗺️  Bricks" -Color "#CFE0F5" -FontSize "10.5pt"
$execVisuals += New-TextVisual -Name "Sidebar_Nav_5" -X 18 -Y 348 -W 175 -H 32 -Z 100 -Text "📅  Visits" -Color "#CFE0F5" -FontSize "10.5pt"
$execVisuals += New-TextVisual -Name "Sidebar_Nav_6" -X 18 -Y 398 -W 175 -H 32 -Z 100 -Text "💊  Drugs & Comparisons" -Color "#CFE0F5" -FontSize "10.5pt"
$execVisuals += New-TextVisual -Name "Sidebar_Nav_7" -X 18 -Y 448 -W 175 -H 32 -Z 100 -Text "📦  Distributors & Stock" -Color "#CFE0F5" -FontSize "10.5pt"
$execVisuals += New-TextVisual -Name "Sidebar_Nav_8" -X 18 -Y 498 -W 175 -H 32 -Z 100 -Text "💳  Expenses & Budget" -Color "#CFE0F5" -FontSize "10.5pt"

# 5. Top Live Model Pill Badge
$execVisuals += New-TextVisual -Name "Badge_LiveModel" -X 520 -Y 8 -W 260 -H 26 -Z 200 -Text "🟢 Live Model: 24-Month Active Run" -Color "#007399" -FontSize "9.5pt" -BgColor "#E6F7FB" -BorderColor "#89DAF4" -BorderRadius 13

# 6. Top 4 Dropdown Slicers
$execVisuals += New-SlicerVisual -Name "Slicer_Line" -X 215 -Y 38 -W 254 -H 44 -Z 200 -TableName "dim_product" -ColumnName "Therapeutic_Line" -TitleText "Line: Cardio-Metabolic"
$execVisuals += New-SlicerVisual -Name "Slicer_Zone" -X 481 -Y 38 -W 254 -H 44 -Z 200 -TableName "dim_brick_territory" -ColumnName "Zone" -TitleText "Zone: Greater Cairo"
$execVisuals += New-SlicerVisual -Name "Slicer_Period" -X 747 -Y 38 -W 254 -H 44 -Z 200 -TableName "dim_date" -ColumnName "Year" -TitleText "Period: 2025-2026"
$execVisuals += New-SlicerVisual -Name "Slicer_Tier" -X 1013 -Y 38 -W 257 -H 44 -Z 200 -TableName "dim_doctor" -ColumnName "Classification" -TitleText "Tier: Class A"

# 7. 4 Modern KPI Cards + Left Accent Color Indicator Shapes
# Card 1: Gross Revenue
$execVisuals += New-ShapeVisual -Name "Accent_Kpi1" -X 215 -Y 88 -W 5 -H 88 -Z 350 -FillColor "#00A3E0" -BorderColor "#00A3E0"
$execVisuals += New-KpiCardVisual -Name "Kpi_GrossRevenue" -X 215 -Y 88 -W 254 -H 88 -Z 300 -MeasureName "Total Revenue EGP" -CardTitle "Gross Revenue"

# Card 2: Market Share
$execVisuals += New-ShapeVisual -Name "Accent_Kpi2" -X 481 -Y 88 -W 5 -H 88 -Z 350 -FillColor "#00B4D8" -BorderColor "#00B4D8"
$execVisuals += New-KpiCardVisual -Name "Kpi_MarketShare" -X 481 -Y 88 -W 254 -H 88 -Z 300 -MeasureName "IMS Market Share Pct" -CardTitle "Market Share"

# Card 3: Call Attainment
$execVisuals += New-ShapeVisual -Name "Accent_Kpi3" -X 747 -Y 88 -W 5 -H 88 -Z 350 -FillColor "#0070BA" -BorderColor "#0070BA"
$execVisuals += New-KpiCardVisual -Name "Kpi_CallAttainment" -X 747 -Y 88 -W 254 -H 88 -Z 300 -MeasureName "Plan Adherence Pct" -CardTitle "Call Attainment"

# Card 4: High-Risk KOLs
$execVisuals += New-ShapeVisual -Name "Accent_Kpi4" -X 1013 -Y 88 -W 5 -H 88 -Z 350 -FillColor "#00A3E0" -BorderColor "#00A3E0"
$execVisuals += New-KpiCardVisual -Name "Kpi_HighRiskKOLs" -X 1013 -Y 88 -W 257 -H 88 -Z 300 -MeasureName "High Churn Risk Doctor Count" -CardTitle "High-Risk KOLs"

# 8. Middle Row:
# Chart Left: Gross Revenue and Market Share Area Wave Chart
$execVisuals += New-LineAreaChartVisual -Name "Chart_RevenueMarketShare" -X 215 -Y 184 -W 670 -H 250 -Z 300 -TitleText "Gross Revenue and Market Share"

# Chart Right: Top Performing Cairo Bricks Map
$execVisuals += New-MapVisual -Name "Chart_SpatialMap" -X 897 -Y 184 -W 373 -H 250 -Z 300 -TitleText "Top Performing Cairo Bricks (Spatial Distribution)"

# 9. Bottom Row:
# Chart 1: Cairo Brick Ranking Horizontal Bar Chart
$execVisuals += New-BarChartVisual -Name "Chart_BrickRanking" -X 215 -Y 442 -W 340 -H 266 -Z 300 -TitleText "Cairo Briking Cairo Brick"

# Chart 2: Distributor Market Share Vertical Column Chart
$execVisuals += New-ColumnChartVisual -Name "Chart_DistributorShare" -X 567 -Y 442 -W 300 -H 266 -Z 300 -TitleText "Distributor Market Share"

# Chart 3: Call Attainment Tier Segmentation Combo Chart
$execVisuals += New-ComboChartVisual -Name "Chart_CallAttainmentTier" -X 879 -Y 442 -W 391 -H 266 -Z 300 -TitleText "Call Attainment Tier Segmentation"

Write-Host "  [+] Total Visual Containers compiled: $($execVisuals.Count)" -ForegroundColor Green

# ------------------------------------------------------------------------------
# Update report.json with the new Executive Overview Page as Page 1 (ordinal: 0)
# ------------------------------------------------------------------------------
$rawJson = Get-Content $ReportJsonPath -Raw
$reportObj = ConvertFrom-Json $rawJson

$execSection = [PSCustomObject]@{
    name = "Section_Executive_Overview"
    displayName = "Executive Overview"
    ordinal = 0
    displayOption = 0
    width = 1280.00
    height = 720.00
    config = "{}"
    filters = "[]"
    visualContainers = $execVisuals
}

# Filter out old placeholders and duplicate Executive Overview sections
$otherSections = @($reportObj.sections | Where-Object { $_.name -notin @("7c530dfe2e5f210efc7a", "85f5414383a50c8df334", "Section_Executive_Overview", "Section_ExecOverview") })

# Re-order ordinals
$finalSections = @($execSection)
$curOrd = 1
foreach ($sec in $otherSections) {
    $sec.ordinal = $curOrd
    $curOrd++
    $finalSections += $sec
}

$reportObj.sections = $finalSections

# Convert back to JSON and write with UTF-8 without BOM
$updatedJson = $reportObj | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($ReportJsonPath, $updatedJson, $utf8NoBom)

Write-Host ">>> Successfully updated $ReportJsonPath!" -ForegroundColor Green
Write-Host ">>> Executive Overview is now Page 1 with $($execVisuals.Count) tailored visuals matching the design image." -ForegroundColor Green

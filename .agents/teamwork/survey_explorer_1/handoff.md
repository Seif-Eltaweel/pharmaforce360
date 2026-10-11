# Handoff Report: Requirement R1 Theme Hardening & Static Resources Investigation

**Agent**: Survey Explorer 1 (`survey_explorer_1`)  
**Mission**: Investigate Theme Hardening & Static Resources for Requirement R1  
**Target Project**: PharmaForce 360° Commercial Intelligence Suite (Power BI PBIP)  
**Date**: 2026-10-11T05:25:00Z  

---

## 1. Observation

### 1.1 Existing Theme Files & Current `visualStyles` Configuration
Two primary theme definition files were located in the workspace:
1. `D:\portfolio2026\02_PharmaForce360\powerbi\theme.json` (Lines 19–70)
2. `D:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\RegisteredResources\PharmaForce360Theme.json` (Lines 19–70)

Both files contain the exact same `visualStyles` structure:
```json
  "visualStyles": {
    "page": {
      "*": {
        "background": [
          {
            "transparency": 0,
            "color": {
              "solid": {
                "color": "#F8FAFC"
              }
            }
          }
        ]
      }
    },
    "*": {
      "*": {
        "background": [
          {
            "transparency": 0,
            "color": {
              "solid": {
                "color": "#FFFFFF"
              }
            }
          }
        ],
        "visualHeader": [
          {
            "foreground": {
              "solid": {
                "color": "#0A2540"
              }
            }
          }
        ],
        "*": {
          "responsive": true
        },
        "border": [
          {
            "radius": 8,
            "color": {
              "solid": {
                "color": "#E2E8F0"
              }
            }
          }
        ]
      }
    }
  }
```

**Direct Observations:**
- Neither theme file has any entry for `actionButton`, `shape`, or `image` in `visualStyles`.
- The wildcard rule `"*": { "*": { ... } }` (lines 34–69) unconditionally sets `"transparency": 0` with `#FFFFFF` and `"border"` with radius 8 and color `#E2E8F0`.
- In `powerbi/PharmaForce360.Report/report.json`:
  - Line 2: `"themeCollection":{"baseTheme":{"name":"CY24SU08","type":2,"version":{"visual":"1.8.92","report":"2.0.92","page":"1.3.92"}},"customTheme":{"name":"PharmaForce360Theme","type":0,"version":{"visual":"2.13.0","report":"3.4.0","page":"2.3.1"}}}`
  - Line 906: `"theme": "PharmaForce360Theme"`
  This links the PBIP report directly to `StaticResources/RegisteredResources/PharmaForce360Theme.json`.

---

### 1.2 Inventory of the 8 SVG Navigation Backdrop Assets
All 8 vector assets exist and were verified in two locations:
- Primary PBIP Path: `D:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\RegisteredResources\`
- Asset Library Path: `D:\portfolio2026\02_PharmaForce360\data\assets\navigation\`

| # | File Name | File Size | SVG Dimensions | Active Highlight Pill Position | Target Page Section |
|---|---|---|---|---|---|
| 1 | `nav_sidebar_overview.svg` | 9,397 bytes | `240 x 720 px` | `x="12" y="134" width="216" height="40" rx="10"` | `Section_Executive_Overview` |
| 2 | `nav_sidebar_doctors.svg` | 9,397 bytes | `240 x 720 px` | `x="12" y="188" width="216" height="40" rx="10"` | `Section_Doctors_KOLs` |
| 3 | `nav_sidebar_medical_reps.svg` | 9,397 bytes | `240 x 720 px` | `x="12" y="242" width="216" height="40" rx="10"` | `Section_Medical_Reps` |
| 4 | `nav_sidebar_bricks.svg` | 9,397 bytes | `240 x 720 px` | `x="12" y="296" width="216" height="40" rx="10"` | `Section_Bricks_Territory` |
| 5 | `nav_sidebar_visits.svg` | 9,397 bytes | `240 x 720 px` | `x="12" y="350" width="216" height="40" rx="10"` | `Section_Visits_Activity` |
| 6 | `nav_sidebar_drugs.svg` | 9,397 bytes | `240 x 720 px` | `x="12" y="404" width="216" height="40" rx="10"` | `Section_Commercial_IQVIA` |
| 7 | `nav_sidebar_distributors.svg` | 9,397 bytes | `240 x 720 px` | `x="12" y="458" width="216" height="40" rx="10"` | `Section_Distributors_Stock` |
| 8 | `nav_sidebar_expenses.svg` | 9,397 bytes | `240 x 720 px` | `x="12" y="512" width="216" height="40" rx="10"` | `Section_Expenses_Budget` |

**Direct Verification of SVG Contents:**
- Header (line 1 of each SVG): `<svg xmlns="http://www.w3.org/2000/svg" width="240" height="720" viewBox="0 0 240 720">`
- Gradient definition: `#071E54` -> `#0A2568` -> `#071945` (deep navy)
- Caduceus emblem & branding: "PharmaForce 360°"
- Menu items at calibrated vertical offsets Y = 134, 188, 242, 296, 350, 404, 458, 512
- Active pill: `fill="url(#activePillGradient)" stroke="#38BDF8" stroke-width="1"`
- Inactive items: stroke `#9BB3D6`, text `#C8DCF5`
- Active item: stroke `#FFFFFF`, text `#FFFFFF` font-weight 600

---

### 1.3 Static Resource Registration in `report.json`
In `D:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\report.json` (lines 4–23):
```json
  "resourcePackages": [
    {
      "resourcePackage": {
        "disabled": false,
        "items": [
          {
            "name": "cairo_basemap829787130905711.png",
            "path": "cairo_basemap829787130905711.png",
            "type": 100
          },
          {
            "name": "cairo_commercial_bricks5739189556477071.geojson",
            "path": "cairo_commercial_bricks5739189556477071.geojson",
            "type": 200
          }
        ],
        "name": "RegisteredResources",
        "type": 1
      }
    },
    {
      "resourcePackage": {
        "disabled": false,
        "items": [
          {
            "name": "CY24SU08",
            "path": "BaseThemes/CY24SU08.json",
            "type": 202
          }
        ],
        "name": "SharedResources",
        "type": 2
      }
    }
  ]
```
**Direct Observation:**
None of the 8 SVG files are currently registered under `resourcePackages[0].resourcePackage.items`. Only the PNG basemap (`type: 100`) and the GeoJSON brick boundaries (`type: 200`) are registered.

---

### 1.4 Navigation Elements and Wildcard Styling Violations in `report.json`
In `report.json`:
- `Section_Executive_Overview` currently has visual containers defined at `X <= 240`:
  - `Nav_Sidebar_Bg` (shape): `x: 0.00, y: 0.00, width: 205.00, height: 720.00`
  - `Nav_Brand_Logo` (textbox): `x: 10.00, y: 16.00, width: 185.00, height: 55.00`
  - `Nav_Active_Pill` (shape): `x: 10.00, y: 138.00, width: 185.00, height: 42.00`
  - `Nav_Item_1_Active` through `Nav_Item_8` (textboxes): `x: 18.00, y: 145..498, width: 170..175, height: 32.00`
- Due to the theme wildcard rule `"*": {"*": {...}}`, these textboxes and shapes inherit an opaque `#FFFFFF` background and `#E2E8F0` border, causing the "White Box" regression.
- Furthermore, analytical visuals collide into the sidebar area (`X < 252`):
  - `Slicer_Line`: `x: 226.40, y: 18.80`
  - `Accent_Kpi_1`: `x: 226.40, y: 68.80`
  - `Card_Gross_Revenue`: `x: 226.40, y: 68.80`
  - `Chart_Brick_Ranking`: `x: 215.00, y: 442.00`
  - `Chart_Revenue_MarketShare`: `x: 215.00, y: 183.75`

---

## 2. Logic Chain

1. **Root Cause Analysis of the "White Box" Regression**:
   - Power BI visual style hierarchy resolves from specific visual types to wildcard `"*"` fallbacks.
   - Because `actionButton`, `shape`, and `image` are missing from `visualStyles` in `powerbi/theme.json` and `PharmaForce360Theme.json` (Obs 1.1), Power BI applies the fallback `"*": {"*": {"background": [{"transparency": 0, "color": {"solid": {"color": "#FFFFFF"}}}], "border": [{"radius": 8, "color": {"solid": {"color": "#E2E8F0"}}}]}}`.
   - When navigation elements (e.g. shapes, textboxes, image backgrounds, action buttons) are rendered, Power BI places an opaque white rectangle with a grey border behind and around each one, obscuring the navy sidebar gradient and creating unsightly cards.

2. **Remediation via Explicit Type Overrides**:
   - By declaring explicit rules for `"actionButton"`, `"shape"`, and `"image"` under `"visualStyles"`, Power BI matches these specific types first and bypasses the wildcard fallback.
   - Setting `"background": [{"transparency": 100}]` and `"border": [{"show": false}]` ensures these visual types are 100% transparent and borderless by default.
   - Analytical visuals (e.g., `card`, `slicer`, `lineChart`, `clusteredBarChart`) continue to match `"*"` and retain their clean white container card styling (`#FFFFFF` background, `#E2E8F0` border with 8px radius).

3. **Asset Registration Requirement**:
   - Power BI PBIP requires static resources embedded in visuals (like `image` visuals referencing local assets) to be listed in `report.json` under `resourcePackages[0].resourcePackage.items` with `type: 100` (Obs 1.3).
   - Although all 8 SVG assets are already placed in `StaticResources/RegisteredResources/` (Obs 1.2), they cannot be resolved cleanly by PBIP image visual references unless registered in `report.json`.

---

## 3. Proposed Patches

### 3.1 Theme Hardening Patch (`powerbi/theme.json` and `PharmaForce360Theme.json`)
The following block must be inserted into `"visualStyles"` in both `powerbi/theme.json` and `powerbi/PharmaForce360.Report/StaticResources/RegisteredResources/PharmaForce360Theme.json`:

```json
    "actionButton": {
      "*": {
        "background": [
          {
            "transparency": 100
          }
        ],
        "border": [
          {
            "show": false
          }
        ]
      }
    },
    "shape": {
      "*": {
        "background": [
          {
            "transparency": 100
          }
        ],
        "border": [
          {
            "show": false
          }
        ]
      }
    },
    "image": {
      "*": {
        "background": [
          {
            "transparency": 100
          }
        ],
        "border": [
          {
            "show": false
          }
        ]
      }
    },
```

#### Full Target `visualStyles` Block:
```json
  "visualStyles": {
    "page": {
      "*": {
        "background": [
          {
            "transparency": 0,
            "color": {
              "solid": {
                "color": "#F8FAFC"
              }
            }
          }
        ]
      }
    },
    "actionButton": {
      "*": {
        "background": [
          {
            "transparency": 100
          }
        ],
        "border": [
          {
            "show": false
          }
        ]
      }
    },
    "shape": {
      "*": {
        "background": [
          {
            "transparency": 100
          }
        ],
        "border": [
          {
            "show": false
          }
        ]
      }
    },
    "image": {
      "*": {
        "background": [
          {
            "transparency": 100
          }
        ],
        "border": [
          {
            "show": false
          }
        ]
      }
    },
    "*": {
      "*": {
        "background": [
          {
            "transparency": 0,
            "color": {
              "solid": {
                "color": "#FFFFFF"
              }
            }
          }
        ],
        "visualHeader": [
          {
            "foreground": {
              "solid": {
                "color": "#0A2540"
              }
            }
          }
        ],
        "*": {
          "responsive": true
        },
        "border": [
          {
            "radius": 8,
            "color": {
              "solid": {
                "color": "#E2E8F0"
              }
            }
          }
        ]
      }
    }
  }
```

---

### 3.2 `report.json` Resource Registration Patch
In `powerbi/PharmaForce360.Report/report.json`, under `resourcePackages[0].resourcePackage.items`, add the 8 SVG files:

```json
          {
            "name": "nav_sidebar_overview.svg",
            "path": "nav_sidebar_overview.svg",
            "type": 100
          },
          {
            "name": "nav_sidebar_doctors.svg",
            "path": "nav_sidebar_doctors.svg",
            "type": 100
          },
          {
            "name": "nav_sidebar_medical_reps.svg",
            "path": "nav_sidebar_medical_reps.svg",
            "type": 100
          },
          {
            "name": "nav_sidebar_bricks.svg",
            "path": "nav_sidebar_bricks.svg",
            "type": 100
          },
          {
            "name": "nav_sidebar_visits.svg",
            "path": "nav_sidebar_visits.svg",
            "type": 100
          },
          {
            "name": "nav_sidebar_drugs.svg",
            "path": "nav_sidebar_drugs.svg",
            "type": 100
          },
          {
            "name": "nav_sidebar_distributors.svg",
            "path": "nav_sidebar_distributors.svg",
            "type": 100
          },
          {
            "name": "nav_sidebar_expenses.svg",
            "path": "nav_sidebar_expenses.svg",
            "type": 100
          }
```

---

### 3.3 Visual Container Image Definition Syntax for Each Page's Sidebar
In each section of `report.json`, the sidebar image visual must be added at `(0, 0, 240, 720)` with Z-order `10.0` as follows:

```json
{
  "config": "{\"name\":\"Nav_Sidebar_Bg\",\"layouts\":[{\"id\":0,\"position\":{\"x\":0.0,\"y\":0.0,\"width\":240.0,\"height\":720.0,\"z\":10.0}}],\"singleVisual\":{\"visualType\":\"image\",\"drillFilterOtherVisuals\":true,\"objects\":{\"image\":[{\"properties\":{\"sourceFile\":{\"image\":{\"name\":{\"expr\":{\"Literal\":{\"Value\":\"'nav_sidebar_<page>.svg'\"}}},\"url\":{\"expr\":{\"ResourcePackageItem\":{\"PackageName\":\"RegisteredResources\",\"PackageType\":1,\"ItemName\":\"nav_sidebar_<page>.svg\"}}},\"scaling\":{\"expr\":{\"Literal\":{\"Value\":\"'Normal'\"}}}}}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"transparency\":{\"expr\":{\"Literal\":{\"Value\":\"100D\"}}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]}}}",
  "filters": "[]",
  "height": 720.00,
  "width": 240.00,
  "x": 0.00,
  "y": 0.00,
  "z": 10.00
}
```

---

## 4. Caveats

1. **UTF-8 BOM Pitfall**:
   Both theme files and `report.json` must strictly remain BOM-free UTF-8. Using PowerShell standard redirection (`>` or `Out-File`) can inject UTF-16LE or UTF-8 BOM, which breaks Power BI PBIP parsing. The existing `scripts/strip_bom.py` utility can be used for verification.
2. **Dual Theme Maintenance**:
   Both `powerbi/theme.json` (workspace root theme) and `powerbi/PharmaForce360.Report/StaticResources/RegisteredResources/PharmaForce360Theme.json` (registered custom theme) must be updated simultaneously to prevent divergence when opening the project directly in Power BI Desktop vs re-importing themes.
3. **Defense-in-Depth Visual Container Properties**:
   While theme hardening fixes default inheritance, each navigation `actionButton` and `image` visual in `report.json` should still explicitly set `"vcObjects": {"background": [{"properties": {"transparency": {"expr": {"Literal": {"Value": "100D"}}}}}], "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]}` to guarantee zero regression even if a theme is unloaded.

---

## 5. Conclusion

1. **Root Cause Confirmed**: The "White Box" defect is caused by the global wildcard rule `"*": {"*": { "background": [{"transparency": 0, "color": {"solid": {"color": "#FFFFFF"}}}], "border": [{"radius": 8, "color": {"solid": {"color": "#E2E8F0"}}}] }}` in `theme.json` and `PharmaForce360Theme.json`, combined with the absence of explicit `visualStyles` for `actionButton`, `shape`, and `image`.
2. **Assets Ready**: All 8 SVG navigation sidebar backdrops (`nav_sidebar_overview.svg` through `nav_sidebar_expenses.svg`) are present, verified at `240 x 720 px` with correct active highlights at Y = 134, 188, 242, 296, 350, 404, 458, 512.
3. **Registration Gap Identified**: The 8 SVGs must be registered in `report.json` under `resourcePackages[0].resourcePackage.items` with `type: 100`.
4. **Implementation Plan Ready**: The exact JSON patches for theme hardening and `report.json` resource registration are fully defined and ready for the implementation agent.

---

## 6. Verification Method

1. **Theme JSON Syntax and Schema Check**:
   - Inspect `powerbi/theme.json` and `PharmaForce360Theme.json` using `view_file` to confirm that `"visualStyles"` contains `actionButton`, `shape`, and `image` overrides with `"transparency": 100` and `"border": [{"show": false}]`.
   - Ensure the JSON is valid with no trailing commas or syntax errors.
2. **Resource Registration Check**:
   - Inspect `report.json` lines 4–35 to confirm all 8 SVG files are present under `resourcePackages[0].resourcePackage.items` with `"type": 100`.
3. **BOM Verification**:
   - Verify files do not start with `\xef\xbb\xbf` (BOM-free UTF-8).

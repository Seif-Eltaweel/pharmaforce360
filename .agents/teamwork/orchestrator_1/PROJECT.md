# Project: PharmaForce 360° Navigation Bar and Canvas Layer Architecture

## Architecture
- **PBIP Report Definition**: `powerbi/PharmaForce360.Report/report.json`
- **Theme Definitions**: `powerbi/theme.json` and `powerbi/PharmaForce360.Report/StaticResources/RegisteredResources/PharmaForce360Theme.json`
- **Static SVG Resources**: `powerbi/PharmaForce360.Report/StaticResources/RegisteredResources/nav_sidebar_*.svg`
- **Canvas Dimensions**: 1280 x 720 px
- **Navigation Rail**: Width = 240 px, X ∈ [0, 240]
- **Horizontal Clearance**: Analytical visuals reside at X >= 252 px (12 px gutter)
- **Canvas Vertical Bands**:
  - Band 1 (Dropdown Slicers): Y ∈ [16, 62] (Height = 46)
  - Band 2 (KPI Summary Cards): Y ∈ [72, 160] (Height = 88)
  - Band 3 (Upper Charts): Y ∈ [172, 428] (Height = 256)
  - Band 4 (Lower Charts): Y ∈ [440, 704] (Height = 264)
- **Native Action Buttons**: 8 buttons per page at X = 12, W = 216, H = 40, Y ∈ [134, 188, 242, 296, 350, 404, 458, 512], Z ∈ [100..800], `drillFilterOtherVisuals: true`, `pageNavigation` action binding.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Theme Hardening for ActionButtons | Explicit `"background": [{"transparency": 100}]` and `"border": [{"show": false}]` for `actionButton` in theme files | M1 | ORIGINAL_REQUEST § R1 |
| 2 | Theme Hardening for Shapes & Images | Explicit `"background": [{"transparency": 100}]` and `"border": [{"show": false}]` for `shape` and `image` in theme files | M1 | ORIGINAL_REQUEST § R1 |
| 3 | Static SVG Registration in report.json | Register all 8 `nav_sidebar_*.svg` assets in `resourcePackages[0].resourcePackage.items` with `type: 100` | M1 | ORIGINAL_REQUEST § R1, Survey |
| 4 | Executive Overview Sidebar Replacement | Replace 11 legacy static visuals with `nav_sidebar_overview.svg` at (0, 0, 240, 720) and 8 `actionButton` visuals | M2 | ORIGINAL_REQUEST § R2 |
| 5 | Executive Overview Grid Calibration | Shift slicers, KPI cards, accent shapes, and charts to X >= 252 px and align with vertical bands | M2 | ORIGINAL_REQUEST § R3 |
| 6 | 8-Domain Page Architecture Creation | Ensure all 8 target domain pages exist with exact internal section IDs and display names | M3, M4 | ORIGINAL_REQUEST § R2 |
| 7 | Analytical Domains 02-05 Navigation & Grid | Inject SVG sidebars and 8 action buttons, calibrate visuals to X >= 252 on Sections 02, 03, 04, 05 | M3 | ORIGINAL_REQUEST § R2, R3 |
| 8 | Analytical Domains 06-08 Navigation & Grid | Inject SVG sidebars and 8 action buttons, calibrate visuals to X >= 252 on Sections 06, 07, 08 | M4 | ORIGINAL_REQUEST § R2, R3 |
| 9 | UTF-8 BOM-Free Schema & JSON Validation | Validate PBIP JSON syntax, encoding, and structure without regressions | M5 | ORIGINAL_REQUEST § R4 |
| 10 | Coordinate Compliance Audit Matrix | Generate audited matrix asserting visual boundaries, X>=252, Y bands, and actionButton navigation targets | M5 | ORIGINAL_REQUEST § R4 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Global Theme Hardening & Resource Registration | `powerbi/theme.json`, `PharmaForce360Theme.json`, and `report.json` resourcePackages | None | DONE |
| M2 | Executive Overview Modernization & Grid Calibration | Modernize Section_Executive_Overview with SVG sidebar, 8 action buttons, and X>=252 grid alignment | M1 | IN_PROGRESS |
| M3 | Analytical Domains 02–05 Implementation & Calibration | Configure Sections 02–05 (Doctors, Reps, Bricks, Visits) with SVG sidebars, action buttons, and X>=252 grid | M1, M2 | PLANNED |
| M4 | Analytical Domains 06–08 Implementation & Calibration | Configure Sections 06–08 (Commercial, Stock, Expenses) with SVG sidebars, action buttons, and X>=252 grid | M1, M2 | PLANNED |
| M5 | Coordinate Compliance Audit & Integrity Verification | Schema validation, coordinate compliance matrix generation, test suite verification, and audit sign-off | M1, M2, M3, M4 | PLANNED |

## Interface Contracts
### Visual Containers ↔ Power BI Native ActionButtons
- Visual Type: `actionButton`
- Geometry: X=12.0, Width=216.0, Height=40.0
- Y Offsets:
  1. Overview: Y=134.0, Target: `Section_Executive_Overview`
  2. Doctors: Y=188.0, Target: `Section_Doctors_KOLs`
  3. Reps: Y=242.0, Target: `Section_Medical_Reps`
  4. Bricks: Y=296.0, Target: `Section_Bricks_Territory`
  5. Visits: Y=350.0, Target: `Section_Visits_Activity`
  6. Drugs/Commercial: Y=404.0, Target: `Section_Commercial_IQVIA`
  7. Distributors: Y=458.0, Target: `Section_Distributors_Stock`
  8. Expenses: Y=512.0, Target: `Section_Expenses_Budget`
- Properties: `drillFilterOtherVisuals: true`, `pageNavigation` action binding
- Visual Container Styling: Transparency `100D`, Border `false`

### Visual Containers ↔ SVG Sidebar Backdrop
- Visual Type: `image`
- Geometry: X=0.0, Y=0.0, Width=240.0, Height=720.0, Z=10.0
- Resource Binding: `ResourcePackageItem` in `RegisteredResources`
- Visual Container Styling: Transparency `100D`, Border `false`

### Analytical Visuals ↔ Canvas Layout
- Geometry: Strict $X \ge 252.0$ px
- Slicers: $Y \in [16, 62]$, $H = 46$
- KPI Cards: $Y \in [72, 160]$, $H = 88$
- Upper Charts: $Y \in [172, 428]$, $H = 256$
- Lower Charts: $Y \in [440, 704]$, $H = 264$

## Code Layout
- `powerbi/theme.json` — Root theme definition
- `powerbi/PharmaForce360.Report/StaticResources/RegisteredResources/PharmaForce360Theme.json` — Registered report theme
- `powerbi/PharmaForce360.Report/report.json` — Primary PBIP report layout and visual definitions
- `powerbi/PharmaForce360.Report/StaticResources/RegisteredResources/` — SVG backdrop assets and basemaps

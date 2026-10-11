# 🧭 Survey Specification Report: Navigation Geometry, Action Button Specs, & Coordinate Compliance Matrix

> **Author**: Survey Explorer 3 (`survey_spec_miner_3`)  
> **Workspace**: `D:\portfolio2026\02_PharmaForce360\`  
> **Target Artifact**: `D:\portfolio2026\02_PharmaForce360\.agents\teamwork\survey_spec_miner_3\handoff.md`  
> **Date**: 2026-10-11  
> **Milestone**: Milestone 1 - Architectural Survey & Spec Mining  

---

## 1. Observation

Direct observations extracted from the specification documents, project configuration, and PBIP source files:

### 1.1. Reference Documents Inspected
* **`D:\portfolio2026\02_PharmaForce360\.agents\teamwork\ORIGINAL_REQUEST.md`**:
  * Line 5: *"Apply the Navigation Bar and Canvas Layer Architecture Specification (`docs/navigation_bar_specification.md`) across all 8 analytical report pages in the PharmaForce 360° Power BI PBIP project..."*
  * Lines 17-19 (R2): *"Incorporate the 240x720 px SVG sidebar backdrop assets from `StaticResources/RegisteredResources/` across all 8 analytical pages... overlaying 8 transparent native Power BI `actionButton` visuals per page at calibrated vertical coordinates (Y: 134, 188, 242, 296, 350, 404, 458, 512) with functional `pageNavigation` action bindings."*
  * Lines 20-22 (R3): *"Calibrate all visual containers (slicers at Y: 16-62, KPI summary cards at Y: 72-160, and analytical charts in subsequent grid bands) to maintain clean horizontal clearance starting at X >= 252 px, ensuring zero overlap with the 240 px navigation rail."*
  * Lines 23-25 (R4): *"Perform JSON schema and syntax validation on modified PBIP files (`report.json` and `theme.json`)... and generate an audited coordinate compliance matrix verifying that visual boundaries and navigation targets adhere strictly to the specification."*
  * Lines 32-44 (Acceptance Criteria): Explicitly defines acceptance criteria for theme overrides, 8-page internal section naming, visual positions, and layout compliance.

* **`D:\portfolio2026\02_PharmaForce360\docs\navigation_bar_specification.md`**:
  * Lines 48-60: Table mapping 8 domains to target page display names and internal section names:
    * 1: `Executive Overview` -> `Section_Executive_Overview`
    * 2: `02 Doctors and KOL Insights` -> `Section_Doctors_KOLs`
    * 3: `03 Medical Representatives` -> `Section_Medical_Reps`
    * 4: `04 Brick Territory Dynamics` -> `Section_Bricks_Territory`
    * 5: `05 Field Detailing and Visits` -> `Section_Visits_Activity`
    * 6: `06 Commercial and IQVIA Audit` -> `Section_Commercial_IQVIA`
    * 7: `07 Supply Chain and Stock-Out` -> `Section_Distributors_Stock`
    * 8: `08 Promotional ROI and Budget` -> `Section_Expenses_Budget`
  * Lines 125-151 (Section 4.1): Complete coordinate reference table specifying:
    * Sidebar Backdrop: `image` at `(0, 0, 240, 720)`, `Z = 10`
    * Buttons 1 to 8: `actionButton` at `X = 12`, `W = 216`, `H = 40`, `Y = 134, 188, 242, 296, 350, 404, 458, 512`, `Z = 100, 200, 300, 400, 500, 600, 700, 800`
    * Slicers 1 to 4: `slicer` at `Y = 16`, `H = 46`, `X = 252, 508, 764, 1020`, `W = 246, 246, 246, 244`, `Z = 1010, 1020, 1030, 1040`
    * KPI Cards 1 to 4: `card` at `Y = 72`, `H = 88`, `X = 252, 508, 764, 1020`, `W = 246, 246, 246, 244`, `Z = 1110, 1120, 1130, 1140`
    * Upper Chart Tier: `Y = 172`, `H = 256`, `X = 252, 872`, `W = 610, 392`, `Z = 1210, 1220`
    * Lower Chart Tier: `Y = 440`, `H = 264`, `X = 252, 592, 902`, `W = 330, 300, 362`, `Z = 1310, 1320, 1330`
  * Lines 154-206 (Section 5): Full JSON snippet for `actionButton` container with `singleVisual` action property `pageNavigation`.
  * Lines 210-224 (Section 6): Asset inventory mapping SVG files in `StaticResources/RegisteredResources/`.

### 1.2. Existing PBIP Report & Resource Inspection
* **`D:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\report.json`**:
  * Line 4-22: `resourcePackages` lists registered resources:
    ```json
    {
      "resourcePackage": {
        "disabled": false,
        "items": [
          { "name": "cairo_basemap829787130905711.png", "path": "cairo_basemap829787130905711.png", "type": 100 },
          { "name": "cairo_commercial_bricks5739189556477071.geojson", "path": "cairo_commercial_bricks5739189556477071.geojson", "type": 200 }
        ],
        "name": "RegisteredResources",
        "type": 1
      }
    }
    ```
  * Lines 39-905: Report sections currently present:
    * `761d32def22bced79044` (`Page 2`, 0 visuals)
    * `Section2` (`02 Commercial and IQVIA Audit`, 10 visuals)
    * `Section3` (`03 Field Force and Detailing`, 10 visuals)
    * `Section4` (`04 Brick and Pharmacy Dynamics`, 10 visuals)
    * `Section5` (`05 AI Prescriber Copilot`, 10 visuals)
    * `Section_Executive_Overview` (`Executive Overview`, 19 visuals)
    * `cd062f19f9ca363f1198` (`Page 1`, 2 visuals)
  * Visuals in `Section_Executive_Overview` currently suffer from:
    * Legacy sidebar shape `Nav_Sidebar_Bg` at `X = 0`, `W = 205`, `Z = 0`.
    * Legacy textbox menu items `Nav_Item_1_Active` to `Nav_Item_8` at `X = 18`, `W = 170-175`, `Y = 145, 198, 248, 298, 348, 398, 448, 498`.
    * Analytical slicers positioned at `X = 226.40`, colliding with the 240 px rail!
    * Analytical KPI cards positioned at `X = 226.40`, `Y = 68.80`, colliding horizontally with the rail (`226.40 < 240`) and vertically overlapping slicers (`Y = 18.80 + 44 = 62.80` vs `Y = 68.80`).
    * Lower charts positioned at `X = 215.00`, encroaching 25 px into the 240 px rail.

* **`D:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\RegisteredResources\`**:
  * Confirmed physical presence of all 8 vector SVG backdrops:
    * `nav_sidebar_overview.svg`
    * `nav_sidebar_doctors.svg`
    * `nav_sidebar_medical_reps.svg`
    * `nav_sidebar_bricks.svg`
    * `nav_sidebar_visits.svg`
    * `nav_sidebar_drugs.svg`
    * `nav_sidebar_distributors.svg`
    * `nav_sidebar_expenses.svg`
  * Direct inspection of `nav_sidebar_overview.svg` confirmed:
    * Vector viewBox: `0 0 240 720`
    * Active pill coordinates: `x="12" y="134" width="216" height="40" rx="10"`
    * Spacing between rows: exactly 54 px pitch (134, 188, 242, 296, 350, 404, 458, 512).

---

## 2. Logic Chain

From the direct observations above, the technical requirements for Navigation Geometry, Action Button Specs, Canvas Layout, and Audit Verification are derived systematically:

### 2.1. Logic Chain for Power BI Native `actionButton` Schema
1. **Observation**: In `navigation_bar_specification.md` (lines 154-206) and `ORIGINAL_REQUEST.md` (lines 34-36), 8 action buttons per page are specified to overlay the SVG backdrop.
2. **Inference**: In Power BI Desktop PBIP format, visuals within `sections[].visualContainers[]` contain:
   - Outer properties: `x`, `y`, `width`, `height`, `z`, `filters`, `config` (serialized JSON string).
   - Inner `config` object: `name`, `layouts[0].position`, and `singleVisual`.
3. **Configuration Details**:
   - `visualType`: `"actionButton"`
   - `drillFilterOtherVisuals`: `true`
   - Interaction action: Under `objects.action[0].properties`, `type` must be `'pageNavigation'` and `pageNavigation.page` must be the literal section name (e.g. `'Section_Executive_Overview'`).
   - Visual container styling (`vcObjects`): To prevent white card borders/backgrounds from showing over the SVG backdrop, `vcObjects.background` must specify `"transparency": { "expr": { "Literal": { "Value": "100D" } } }` and `vcObjects.border` must specify `"show": { "expr": { "Literal": { "Value": "false" } } }`.
   - Title, Icon, Text: Because the vector SVG backdrop already renders pixel-perfect icons, typography, and active pill states, the `actionButton` must NOT render text, icons, or fill colors. It functions as an invisible interactive hit-test zone with mouse-pointer feedback and `pageNavigation` execution.

### 2.2. Logic Chain for SVG Background Visual Schema
1. **Observation**: `docs/navigation_bar_specification.md` (lines 127-129, 210-224) and `report.json` (lines 612, 894) show how static images are embedded.
2. **Inference**: 
   - Visual container outer properties: `x = 0.00`, `y = 0.00`, `width = 240.00`, `height = 720.00`, `z = 10.00`.
   - Visual type: `"image"`.
   - Resource binding: In PBIP, image visuals reference assets via `ResourcePackageItem` targeting `PackageName: "RegisteredResources"`, `PackageType: 1`, and `ItemName: "nav_sidebar_<page>.svg"`.
   - `scaling`: `'Fit'` or `'Normal'`.
   - `vcObjects`: Background transparency `100D` and border `false` to avoid theme interference.
   - Resource package registration: The 8 SVGs must be declared in `report.json` under `resourcePackages[0].resourcePackage.items` with `type: 100` so Power BI Desktop resolves them from `StaticResources/RegisteredResources/`.
   - Z-Order hierarchy: `z = 10.00` ensures the backdrop visual sits strictly behind all action buttons (`z = 100.00` to `800.00`), ensuring click events reach the buttons.

### 2.3. Logic Chain for Canvas Grid Layout & Clearance
1. **Observation**: The navigation rail occupies $X \in [0, 240]$ px. `ORIGINAL_REQUEST.md` (R3) mandates horizontal clearance $X \ge 252$ px for all analytical visuals.
2. **Inference**:
   - Rail width = 240 px. Margin / Gutter = 12 px ($252 - 240 = 12$ px).
   - Canvas width = 1280 px. Content area = $1280 - 252 = 1028$ px. Leaving 16 px right margin gives active content grid width = 1012 px ($X \in [252, 1264]$ px).
   - Zero-collision vertical banding:
     - Band 1 (Dropdown Slicers): $Y \in [16, 62]$ px (Height = 46 px).
     - Vertical Gap 1: $72 - 62 = 10$ px clearance.
     - Band 2 (KPI Metric Summary Cards): $Y \in [72, 160]$ px (Height = 88 px).
     - Vertical Gap 2: $172 - 160 = 12$ px clearance.
     - Band 3 (Upper Analytical Tier): $Y \in [172, 428]$ px (Height = 256 px).
     - Vertical Gap 3: $440 - 428 = 12$ px clearance.
     - Band 4 (Lower Analytical Tier): $Y \in [440, 704]$ px (Height = 264 px).
     - Bottom margin: $720 - 704 = 16$ px clearance.
   - Every analytical visual is guaranteed zero collision with both the navigation rail and adjacent bands.

### 2.4. Logic Chain for Coordinate Compliance Audit Matrix (R4)
1. **Observation**: Acceptance criteria R4 demands:
   - Schema validation.
   - BOM-free UTF-8 encoding.
   - An audited coordinate compliance matrix documenting X, Y, W, H, Z-order, and navigation target for every visual across all 8 pages.
2. **Inference**: The audit matrix requires a concrete data schema with exact mathematical assertions (validation rules) that can be verified automatically by an auditor script or manual inspection.

---

## 3. Specifications & Architecture Deliverables

### 3.1. Power BI Native `actionButton` Container Specifications

#### 3.1.1. Specification Table for 8 Navigation Action Buttons

| # | Visual Name (`name`) | Target Domain | Target Page Display Name | Target Internal Section (`report.json`) | X | Y | Width | Height | Z-Order | Action Binding |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | `Nav_Btn_Overview` | Executive Overview | `Executive Overview` | `Section_Executive_Overview` | `12.0` | `134.0` | `216.0` | `40.0` | `100.0` | `pageNavigation` |
| **2** | `Nav_Btn_Doctors` | Doctors (KOLs) | `02 Doctors and KOL Insights` | `Section_Doctors_KOLs` | `12.0` | `188.0` | `216.0` | `40.0` | `200.0` | `pageNavigation` |
| **3** | `Nav_Btn_MedicalReps` | Medical Representatives | `03 Medical Representatives` | `Section_Medical_Reps` | `12.0` | `242.0` | `216.0` | `40.0` | `300.0` | `pageNavigation` |
| **4** | `Nav_Btn_Bricks` | Bricks | `04 Brick Territory Dynamics` | `Section_Bricks_Territory` | `12.0` | `296.0` | `216.0` | `40.0` | `400.0` | `pageNavigation` |
| **5** | `Nav_Btn_Visits` | Visits | `05 Field Detailing and Visits` | `Section_Visits_Activity` | `12.0` | `350.0` | `216.0` | `40.0` | `500.0` | `pageNavigation` |
| **6** | `Nav_Btn_Drugs` | Drugs & Comparisons | `06 Commercial and IQVIA Audit` | `Section_Commercial_IQVIA` | `12.0` | `404.0` | `216.0` | `40.0` | `600.0` | `pageNavigation` |
| **7** | `Nav_Btn_Distributors`| Distributors & Stock | `07 Supply Chain and Stock-Out` | `Section_Distributors_Stock` | `12.0` | `458.0` | `216.0` | `40.0` | `700.0` | `pageNavigation` |
| **8** | `Nav_Btn_Expenses` | Expenses & Budget | `08 Promotional ROI and Budget` | `Section_Expenses_Budget` | `12.0` | `512.0` | `216.0` | `40.0` | `800.0` | `pageNavigation` |

#### 3.1.2. Complete PBIP JSON Visual Container Schema (`actionButton`)
Below is the exact container schema to be placed into `sections[].visualContainers[]`:

```json
{
  "x": 12.00,
  "y": 134.00,
  "width": 216.00,
  "height": 40.00,
  "z": 100.00,
  "filters": "[]",
  "config": "{\"name\":\"Nav_Btn_Overview\",\"layouts\":[{\"id\":0,\"position\":{\"x\":12.0,\"y\":134.0,\"width\":216.0,\"height\":40.0,\"z\":100.0}}],\"singleVisual\":{\"visualType\":\"actionButton\",\"drillFilterOtherVisuals\":true,\"objects\":{\"action\":[{\"properties\":{\"type\":{\"expr\":{\"Literal\":{\"Value\":\"'pageNavigation'\"}}},\"pageNavigation\":{\"page\":{\"expr\":{\"Literal\":{\"Value\":\"'Section_Executive_Overview'\"}}}}}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"transparency\":{\"expr\":{\"Literal\":{\"Value\":\"100D\"}}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]}}}"
}
```

*Note on Configuration Escaping*: In `report.json`, the `config` field is a serialized JSON string. When parsed as a JSON object, the internal configuration is:

```json
{
  "name": "Nav_Btn_Overview",
  "layouts": [
    {
      "id": 0,
      "position": {
        "x": 12.0,
        "y": 134.0,
        "width": 216.0,
        "height": 40.0,
        "z": 100.0
      }
    }
  ],
  "singleVisual": {
    "visualType": "actionButton",
    "drillFilterOtherVisuals": true,
    "objects": {
      "action": [
        {
          "properties": {
            "type": { "expr": { "Literal": { "Value": "'pageNavigation'" } } },
            "pageNavigation": {
              "page": { "expr": { "Literal": { "Value": "'Section_Executive_Overview'" } } }
            }
          }
        }
      ]
    },
    "vcObjects": {
      "background": [
        {
          "properties": {
            "transparency": { "expr": { "Literal": { "Value": "100D" } } }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ]
    }
  }
}
```

---

### 3.2. SVG Sidebar Backdrop Visual Container Specifications

#### 3.2.1. Page-to-Asset Binding Matrix

| Page # | Internal Section Name | Target Page Display Name | SVG Asset Name (`RegisteredResources`) | Dimensions | Position `(X, Y, W, H)` | Z-Order |
|---|---|---|---|---|---|---|
| **1** | `Section_Executive_Overview` | `Executive Overview` | `nav_sidebar_overview.svg` | `240 x 720` | `(0, 0, 240, 720)` | `10.0` |
| **2** | `Section_Doctors_KOLs` | `02 Doctors and KOL Insights` | `nav_sidebar_doctors.svg` | `240 x 720` | `(0, 0, 240, 720)` | `10.0` |
| **3** | `Section_Medical_Reps` | `03 Medical Representatives` | `nav_sidebar_medical_reps.svg` | `240 x 720` | `(0, 0, 240, 720)` | `10.0` |
| **4** | `Section_Bricks_Territory` | `04 Brick Territory Dynamics` | `nav_sidebar_bricks.svg` | `240 x 720` | `(0, 0, 240, 720)` | `10.0` |
| **5** | `Section_Visits_Activity` | `05 Field Detailing and Visits` | `nav_sidebar_visits.svg` | `240 x 720` | `(0, 0, 240, 720)` | `10.0` |
| **6** | `Section_Commercial_IQVIA` | `06 Commercial and IQVIA Audit` | `nav_sidebar_drugs.svg` | `240 x 720` | `(0, 0, 240, 720)` | `10.0` |
| **7** | `Section_Distributors_Stock` | `07 Supply Chain and Stock-Out` | `nav_sidebar_distributors.svg` | `240 x 720` | `(0, 0, 240, 720)` | `10.0` |
| **8** | `Section_Expenses_Budget` | `08 Promotional ROI and Budget` | `nav_sidebar_expenses.svg` | `240 x 720` | `(0, 0, 240, 720)` | `10.0` |

#### 3.2.2. Complete PBIP JSON Visual Container Schema (`image`)
Below is the container schema to be placed into `sections[].visualContainers[]`:

```json
{
  "x": 0.00,
  "y": 0.00,
  "width": 240.00,
  "height": 720.00,
  "z": 10.00,
  "filters": "[]",
  "config": "{\"name\":\"Nav_Sidebar_Backdrop\",\"layouts\":[{\"id\":0,\"position\":{\"x\":0.0,\"y\":0.0,\"width\":240.0,\"height\":720.0,\"z\":10.0}}],\"singleVisual\":{\"visualType\":\"image\",\"drillFilterOtherVisuals\":true,\"objects\":{\"image\":[{\"properties\":{\"sourceFile\":{\"image\":{\"name\":{\"expr\":{\"Literal\":{\"Value\":\"'nav_sidebar_overview.svg'\"}}},\"url\":{\"expr\":{\"ResourcePackageItem\":{\"PackageName\":\"RegisteredResources\",\"PackageType\":1,\"ItemName\":\"nav_sidebar_overview.svg\"}}},\"scaling\":{\"expr\":{\"Literal\":{\"Value\":\"'Fit'\"}}}}}}}]}},\"vcObjects\":{\"background\":[{\"properties\":{\"transparency\":{\"expr\":{\"Literal\":{\"Value\":\"100D\"}}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]}}}"
}
```

#### 3.2.3. Resource Package Declarations in `report.json`
To allow Power BI to resolve the SVG items, `resourcePackages[0].resourcePackage.items` must contain the 8 asset descriptors:

```json
{
  "resourcePackage": {
    "disabled": false,
    "items": [
      { "name": "cairo_basemap829787130905711.png", "path": "cairo_basemap829787130905711.png", "type": 100 },
      { "name": "cairo_commercial_bricks5739189556477071.geojson", "path": "cairo_commercial_bricks5739189556477071.geojson", "type": 200 },
      { "name": "nav_sidebar_overview.svg", "path": "nav_sidebar_overview.svg", "type": 100 },
      { "name": "nav_sidebar_doctors.svg", "path": "nav_sidebar_doctors.svg", "type": 100 },
      { "name": "nav_sidebar_medical_reps.svg", "path": "nav_sidebar_medical_reps.svg", "type": 100 },
      { "name": "nav_sidebar_bricks.svg", "path": "nav_sidebar_bricks.svg", "type": 100 },
      { "name": "nav_sidebar_visits.svg", "path": "nav_sidebar_visits.svg", "type": 100 },
      { "name": "nav_sidebar_drugs.svg", "path": "nav_sidebar_drugs.svg", "type": 100 },
      { "name": "nav_sidebar_distributors.svg", "path": "nav_sidebar_distributors.svg", "type": 100 },
      { "name": "nav_sidebar_expenses.svg", "path": "nav_sidebar_expenses.svg", "type": 100 }
    ],
    "name": "RegisteredResources",
    "type": 1
  }
}
```

---

### 3.3. Canvas Grid Layout & Multi-Band Geometry (1280 x 720 Canvas)

#### 3.3.1. Grid Architecture Geometry Blueprint

```
0            240 252                                                      1264 1280
+--------------+-------------------------------------------------------------+
|              | [ Slicer 1 ]     [ Slicer 2 ]     [ Slicer 3 ]     [ Slic 4 ]|  Y: 16 - 62  (H: 46)
|              | ----------------------------------------------------------- |  [Gap: 10 px]
|              | [ KPI 1 Card ]   [ KPI 2 Card ]   [ KPI 3 Card ]   [ KPI 4 ] |  Y: 72 - 160 (H: 88)
|  NAVIGATION  | ----------------------------------------------------------- |  [Gap: 12 px]
|  SIDEBAR     | [                                           ] [            ]|
|  RAIL        | [        Upper Primary Chart                ] [ Upper Map/ ]|  Y: 172 - 428 (H: 256)
|  (W: 240 px) | [                                           ] [ Chart      ]|
|              | ----------------------------------------------------------- |  [Gap: 12 px]
|              | [ Lower Chart 1 ]   [ Lower Chart 2 ]   [ Lower Chart 3 ]   |  Y: 440 - 704 (H: 264)
+--------------+-------------------------------------------------------------+
                                                                                 [Bottom Margin: 16 px]
```

#### 3.3.2. Detailed Coordinate Specifications for Canonical Analytical Visuals

| Band / Category | Visual Role | Visual Type | X | Y | Width | Height | Z-Order | Boundary Formula Verification |
|---|---|---|---|---|---|---|---|---|
| **Nav Rail** | Sidebar SVG | `image` | `0` | `0` | `240` | `720` | `10` | $X+W=240 \le 240$, $Y+H=720 \le 720$ |
| **Nav Rail** | Button 1 | `actionButton` | `12` | `134` | `216` | `40` | `100` | $X+W=228 < 240$, $Y+H=174$ |
| **Nav Rail** | Button 2 | `actionButton` | `12` | `188` | `216` | `40` | `200` | $X+W=228 < 240$, $Y+H=228$ |
| **Nav Rail** | Button 3 | `actionButton` | `12` | `242` | `216` | `40` | `300` | $X+W=228 < 240$, $Y+H=282$ |
| **Nav Rail** | Button 4 | `actionButton` | `12` | `296` | `216` | `40` | `400` | $X+W=228 < 240$, $Y+H=336$ |
| **Nav Rail** | Button 5 | `actionButton` | `12` | `350` | `216` | `40` | `500` | $X+W=228 < 240$, $Y+H=390$ |
| **Nav Rail** | Button 6 | `actionButton` | `12` | `404` | `216` | `40` | `600` | $X+W=228 < 240$, $Y+H=444$ |
| **Nav Rail** | Button 7 | `actionButton` | `12` | `458` | `216` | `40` | `700` | $X+W=228 < 240$, $Y+H=498$ |
| **Nav Rail** | Button 8 | `actionButton` | `12` | `512` | `216` | `40` | `800` | $X+W=228 < 240$, $Y+H=552$ |
| **Slicers Band** | Slicer 1 (Line) | `slicer` | `252` | `16` | `246` | `46` | `1010` | $X \ge 252$, $Y+H=62 \le 62$ |
| **Slicers Band** | Slicer 2 (Zone) | `slicer` | `508` | `16` | `246` | `46` | `1020` | $X \ge 252$, $Y+H=62 \le 62$ |
| **Slicers Band** | Slicer 3 (Period) | `slicer` | `764` | `16` | `246` | `46` | `1030` | $X \ge 252$, $Y+H=62 \le 62$ |
| **Slicers Band** | Slicer 4 (Tier) | `slicer` | `1020`| `16` | `244` | `46` | `1040` | $X+W=1264 \le 1280$ |
| **KPI Band** | KPI 1 (Revenue) | `card` | `252` | `72` | `246` | `88` | `1110` | $X \ge 252$, $Y+H=160 \le 160$ |
| **KPI Band** | KPI 2 (Market Share)| `card` | `508` | `72` | `246` | `88` | `1120` | $X \ge 252$, $Y+H=160 \le 160$ |
| **KPI Band** | KPI 3 (Attainment) | `card` | `764` | `72` | `246` | `88` | `1130` | $X \ge 252$, $Y+H=160 \le 160$ |
| **KPI Band** | KPI 4 (Risk KOLs) | `card` | `1020`| `72` | `244` | `88` | `1140` | $X+W=1264 \le 1280$ |
| **Upper Charts** | Primary Wave Chart | `lineChart` | `252` | `172` | `610` | `256` | `1210` | $X \ge 252$, $Y+H=428 \le 428$ |
| **Upper Charts** | Spatial Map/Secondary| `shapeMap` | `872` | `172` | `392` | `256` | `1220` | $X+W=1264 \le 1280$ |
| **Lower Charts** | Chart 1 (Ranking) | `clusteredBarChart` | `252` | `440` | `330` | `264` | `1310` | $X \ge 252$, $Y+H=704 \le 704$ |
| **Lower Charts** | Chart 2 (Distributor)| `clusteredColumnChart` | `592` | `440` | `300` | `264` | `1320` | $X \ge 252$, $Y+H=704 \le 704$ |
| **Lower Charts** | Chart 3 (Attainment) | `lineClusteredColumnComboChart` | `902` | `440` | `362` | `264` | `1330` | $X+W=1264 \le 1280$ |

---

### 3.4. Coordinate Compliance Audit Matrix Schema & Verification Checklist (R4)

To satisfy **Acceptance Criteria R4**, the implementation and testing agents must execute automated compliance verification against this formal audit schema.

#### 3.4.1. Audit Matrix Data Schema
Every visual across all pages must be logged in an audit report with the following 10 fields:

```typescript
interface VisualCoordinateAuditRecord {
  pageInternalName: string;      // e.g. "Section_Executive_Overview"
  pageDisplayName: string;       // e.g. "Executive Overview"
  visualContainerName: string;   // e.g. "Nav_Btn_Overview" or visual GUID
  visualType: string;            // e.g. "actionButton", "image", "slicer", "card", etc.
  x: number;                     // X coordinate in pixels
  y: number;                     // Y coordinate in pixels
  width: number;                 // Width in pixels
  height: number;                // Height in pixels
  zOrder: number;                // Z-order layering value
  navigationTarget?: string;     // Internal section target (for actionButtons)
  complianceStatus: "PASS" | "FAIL"; // Verification status
  failureReason?: string;        // Specific rule violated if FAIL
}
```

#### 3.4.2. Ten Mathematical Verification Rules & Checklist

| Rule ID | Rule Name | Mathematical Assertion / Validation Condition | Required Action if Violated |
|---|---|---|---|
| **RULE-01** | **Sidebar Backdrop Placement** | For `visualType == "image"` with name `Nav_Sidebar_Backdrop`: $X = 0 \land Y = 0 \land W = 240 \land H = 720 \land Z = 10$. | Relocate/resize image backdrop to exact rail boundaries. |
| **RULE-02** | **Action Button Boundaries** | For all 8 `actionButton` visuals: $X = 12 \land W = 216 \land H = 40 \land Y \in \{134, 188, 242, 296, 350, 404, 458, 512\}$. | Adjust button coordinates to fit SVG pill slots. |
| **RULE-03** | **Z-Order Layer Separation** | $Z_{\text{backdrop}} < Z_{\text{buttons}} < Z_{\text{slicers}} < Z_{\text{kpi}} < Z_{\text{charts}}$ ($10 < 100..800 < 1010..1040 < 1110..1140 < 1210..1330$). | Reassign Z-order sequence. |
| **RULE-04** | **Horizontal Rail Clearance** | For all non-sidebar visuals ($v \notin \{\text{sidebar}, \text{actionButton}\}$): $X \ge 252 \land X + W \le 1280$. | Shift visual rightward to $X \ge 252$ and constrain right edge $\le 1264$. |
| **RULE-05** | **Slicers Band Confinement** | For all slicer visuals: $Y \ge 16 \land Y + H \le 62$. | Set $Y = 16, H = 46$ to prevent collision with KPI cards. |
| **RULE-06** | **KPI Cards Band Confinement** | For all KPI card visuals: $Y \ge 72 \land Y + H \le 160$. | Set $Y = 72, H = 88$ maintaining 10 px clearance from slicers. |
| **RULE-07** | **Main Content Band Confinement**| For all chart/table visuals: $Y \ge 172 \land Y + H \le 704$. | Set $Y \ge 172$, upper tier $H \le 256$, lower tier $Y \ge 440, H \le 264$. |
| **RULE-08** | **Action Target Valid Existence** | For every `actionButton`: `targetSection` $\in$ set of existing internal section names in `report.json`. | Fix target section name to matching 8 internal page names. |
| **RULE-09** | **Transparency Enforcement** | For all `actionButton`, `image`, and `shape` within rail: `vcObjects.background.transparency == 100D` and `border.show == false`. | Inject explicit transparency and hide border in `vcObjects`. |
| **RULE-10** | **File Integrity & Encoding** | `report.json` and `theme.json` must parse cleanly as valid JSON without BOM (`utf-8`). | Validate via JSON parser and verify BOM header is absent. |

---

## 4. Caveats

1. **Section Renaming Dependencies**:
   - `report.json` currently has sections named `Section2`, `Section3`, `Section4`, `Section5`, and two unconfigured pages `Page 1` (`cd062f19f9ca363f1198`) and `Page 2` (`761d32def22bced79044`).
   - When renaming these sections to `Section_Doctors_KOLs`, `Section_Medical_Reps`, `Section_Bricks_Territory`, `Section_Visits_Activity`, `Section_Commercial_IQVIA`, `Section_Distributors_Stock`, and `Section_Expenses_Budget`, all navigation target bindings across all 8 pages must match these exact names verbatim.
2. **Legacy Visual Cleanup**:
   - In `Section_Executive_Overview`, legacy visuals (`Nav_Sidebar_Bg`, `Nav_Brand_Logo`, `Nav_Active_Pill`, and `Nav_Item_1_Active` to `Nav_Item_8`) must be removed or replaced by the single SVG backdrop visual and the 8 transparent action buttons to avoid duplicate visual container overhead.
3. **Shape Map packaged GeoJSON binding**:
   - The spatial map visuals in `report.json` reference `cairo_commercial_bricks5739189556477071.geojson`. Modifying sections must preserve this binding without disturbing the map resource package.

---

## 5. Conclusion

The specification survey for Navigation Geometry, Action Button Specs, Canvas Grid Layout, and Coordinate Compliance Matrix is complete and fully verified against the design documentation and physical PBIP assets:
1. **Action Buttons**: 8 buttons at $X = 12$, $W = 216$, $H = 40$ with $Y \in \{134, 188, 242, 296, 350, 404, 458, 512\}$, $Z \in [100, 800]$, `drillFilterOtherVisuals: true`, `100D` transparency, and `pageNavigation` action binding.
2. **SVG Backdrop**: 1 vector image visual per page at $(0, 0, 240, 720)$, $Z = 10$, bound to `nav_sidebar_<page>.svg` in `RegisteredResources`.
3. **Canvas Grid**: Rigid horizontal boundary $X \ge 252$ px, providing 1012 px width for analytical visuals, partitioned into Slicers ($Y: 16-62$), KPIs ($Y: 72-160$), and Charts ($Y: 172-704$) with zero overlap.
4. **Compliance Audit**: Defined 10-field matrix schema and 10 mathematical verification rules for automated acceptance audit.

---

## 6. Verification Method

To independently verify the findings in this report:

1. **Verify Physical SVG Asset Coordinates**:
   - Inspect SVG assets: `powerbi/PharmaForce360.Report/StaticResources/RegisteredResources/nav_sidebar_overview.svg`
   - Confirm active pill coordinates: `<rect x="12" y="134" width="216" height="40" rx="10" ...>`
   - Confirm viewBox: `0 0 240 720`.
2. **Verify Specification Document**:
   - View `docs/navigation_bar_specification.md` lines 125-151 and 154-206.
   - Confirm coordinate reference table and action button schema matching this report.
3. **Verify Canvas Boundaries**:
   - Mathematical check: $X_{\text{rail}} = 240$, $X_{\text{clearance}} = 252 \ge 240$.
   - Slicers band: $16 \le Y \le 62$. KPI band: $72 \le Y \le 160$ ($72 - 62 = 10$ px clearance). Charts band: $172 \le Y \le 704$ ($172 - 160 = 12$ px clearance).

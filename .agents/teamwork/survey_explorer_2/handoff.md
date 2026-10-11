# PBIP Report Structure & Analytical Pages Investigation Report (Requirements R2 & R3)

> **Agent**: Survey Explorer 2 (`teamwork_preview_explorer`)  
> **Working Directory**: `D:\portfolio2026\02_PharmaForce360\.agents\teamwork\survey_explorer_2\`  
> **Parent**: `orchestrator_1` (Conversation ID: `177edf21-9ef8-4c4c-8bbf-cd906fdef733`)  
> **Scope**: Investigation of PBIP Report Structure, Analytical Pages, and Visual Containers for Requirements R2 & R3.

---

## 1. Observation

### 1.1. PBIP File Locations & Structure
Direct inspection of the file tree and PBIP definitions revealed:
* **Primary Report Definition**: `powerbi/PharmaForce360.Report/report.json` (907 lines, 90,901 bytes, UTF-8 JSON).
* **PBIR Pointer**: `powerbi/PharmaForce360.Report/definition.pbir` pointing to `../PharmaForce360.SemanticModel`.
* **Theme Reference in `report.json`**:
  * Line 2: `"customTheme": {"name": "PharmaForce360Theme", "type": 0, "version": {"visual": "2.13.0", "report": "3.4.0", "page": "2.3.1"}}`
  * Line 906: `"theme": "PharmaForce360Theme"`
* **Resource Packages in `report.json`** (`lines 4–38`):
  ```json
  "resourcePackages": [
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
    },
    ...
  ]
  ```
  *Observed Fact*: Only `cairo_basemap` and `cairo_commercial_bricks` are registered in `resourcePackages`. None of the SVG sidebars are registered yet.
* **Physical Static Assets on Disk**:
  In `powerbi/PharmaForce360.Report/StaticResources/RegisteredResources/`, all 8 SVG sidebar files physically exist with dimensions `width="240" height="720" viewBox="0 0 240 720"`:
  1. `nav_sidebar_overview.svg`
  2. `nav_sidebar_doctors.svg`
  3. `nav_sidebar_medical_reps.svg`
  4. `nav_sidebar_bricks.svg`
  5. `nav_sidebar_visits.svg`
  6. `nav_sidebar_drugs.svg`
  7. `nav_sidebar_distributors.svg`
  8. `nav_sidebar_expenses.svg`

---

### 1.2. Report Section & Page Enumeration in `report.json`
`report.json` defines exactly **7 sections** (`lines 39–905`), not 8:

| # | Internal Section ID (`name`) | Display Name (`displayName`) | Ordinal | DisplayOption | Visual Containers Count | Status / Notes |
|---|---|---|---|---|---|---|
| **0** | `761d32def22bced79044` | `Page 2` | 2 | 1 (Hidden) | 0 | Empty hidden page |
| **1** | `Section2` | `02 Commercial and IQVIA Audit` | 3 | 0 (Visible) | 14 | Legacy Commercial domain |
| **2** | `Section3` | `03 Field Force and Detailing` | 4 | 0 (Visible) | 14 | Legacy Reps + Visits domain |
| **3** | `Section4` | `04 Brick and Pharmacy Dynamics` | 5 | 0 (Visible) | 14 | Legacy Bricks + Distributors domain |
| **4** | `Section5` | `05 AI Prescriber Copilot` | 6 | 0 (Visible) | 14 | Legacy Doctors + Expenses domain |
| **5** | `Section_Executive_Overview` | `Executive Overview` | *(none)* | 0 (Visible) | 29 | Target Executive domain (`activeSectionIndex: 0`) |
| **6** | `cd062f19f9ca363f1198` | `Page 1` | 1 | 1 (Hidden) | 2 | Hidden ShapeMap + Basemap page |

---

### 1.3. Audit of the 8 Target Analytical Pages

| Target Domain # | Specification Target Internal Name | Specification Target Display Name | Current Existence in `report.json` | Current Equivalent in `report.json` | Compliance Status |
|---|---|---|---|---|---|
| **1** | `Section_Executive_Overview` | `Executive Overview` | **Present** | `Section_Executive_Overview` (lines 603–874) | **EXISTS** (Needs sidebar modernization & X>=252 calibration) |
| **2** | `Section_Doctors_KOLs` | `02 Doctors and KOL Insights` | **Missing** | Part of `Section5` ("05 AI Prescriber Copilot") | **NON-COMPLIANT** (Missing dedicated page) |
| **3** | `Section_Medical_Reps` | `03 Medical Representatives` | **Missing** | Part of `Section3` ("03 Field Force and Detailing") | **NON-COMPLIANT** (Missing dedicated page) |
| **4** | `Section_Bricks_Territory` | `04 Brick Territory Dynamics` | **Missing** | Part of `Section4` ("04 Brick and Pharmacy Dynamics") | **NON-COMPLIANT** (Missing dedicated page) |
| **5** | `Section_Visits_Activity` | `05 Field Detailing and Visits` | **Missing** | Part of `Section3` ("03 Field Force and Detailing") | **NON-COMPLIANT** (Missing dedicated page) |
| **6** | `Section_Commercial_IQVIA` | `06 Commercial and IQVIA Audit` | **Misconfigured** | `Section2` ("02 Commercial and IQVIA Audit") | **NON-COMPLIANT** (Internal name is `Section2`, display name is `02 Commercial...`) |
| **7** | `Section_Distributors_Stock` | `07 Supply Chain and Stock-Out` | **Missing** | Part of `Section4` ("04 Brick and Pharmacy Dynamics") | **NON-COMPLIANT** (Missing dedicated page) |
| **8** | `Section_Expenses_Budget` | `08 Promotional ROI and Budget` | **Missing** | Part of `Section5` ("05 AI Prescriber Copilot") | **NON-COMPLIANT** (Missing dedicated page) |

---

### 1.4. Visual Container Analysis by Section

#### Section 5: `Section_Executive_Overview` (29 visuals total, lines 603–874)

##### Existing Sidebar Visuals (11 visuals — All Legacy / Deprecated):
* `Nav_Sidebar_Bg` (shape, lines 818–826): `x: 0, y: 0, width: 205, height: 720, z: 0`. **Violates 240px width spec**.
* `Nav_Brand_Logo` (textbox, lines 737–745): `x: 10, y: 16, width: 185, height: 55, z: 2000`. Text: `"⚕ PharmaForce 360°"`.
* `Nav_Active_Pill` (shape, lines 728–736): `x: 10, y: 138, width: 185, height: 42, z: 1000`.
* `Nav_Item_1_Active` (textbox, lines 746–754): `x: 18, y: 145, width: 170, height: 32, z: 3000`.
* `Nav_Item_2` (textbox, lines 755–763): `x: 18, y: 198, width: 175, height: 32, z: 4000`.
* `Nav_Item_3` (textbox, lines 764–772): `x: 18, y: 248, width: 175, height: 32, z: 5000`.
* `Nav_Item_4` (textbox, lines 773–781): `x: 18, y: 298, width: 175, height: 32, z: 6000`.
* `Nav_Item_5` (textbox, lines 782–790): `x: 18, y: 348, width: 175, height: 32, z: 7000`.
* `Nav_Item_6` (textbox, lines 791–799): `x: 18, y: 398, width: 175, height: 32, z: 8000`.
* `Nav_Item_7` (textbox, lines 800–808): `x: 18, y: 448, width: 175, height: 32, z: 9000`.
* `Nav_Item_8` (textbox, lines 809–817): `x: 18, y: 498, width: 175, height: 32, z: 10000`.
* **Action Buttons**: **ZERO `actionButton` visuals exist**. All items are static textboxes.

##### Analytical Visual Containers (18 visuals):
| Visual Name | Visual Type | Current X | Current Y | Width | Height | Z-Order | Spec Target X, Y, W, H | Coordinate Compliance / Violations |
|---|---|---|---|---|---|---|---|---|
| `Slicer_Line` | `slicer` | **226.40** | 18.80 | 254.00 | 44.00 | 11000 | (252, 16, 246, 46) | **VIOLATION**: X=226.40 < 252 (intrudes into 240px rail buffer by 13.6px). |
| `Slicer_Zone` | `slicer` | 492.40 | 18.80 | 254.00 | 44.00 | 12000 | (508, 16, 246, 46) | Needs slight shift to align with 252+246 grid. |
| `Slicer_Period` | `slicer` | 758.40 | 18.80 | 254.00 | 44.00 | 13000 | (764, 16, 246, 46) | Needs shift to align with grid. |
| `Slicer_Tier` | `slicer` | 1024.40 | 18.80 | 257.00 | 44.00 | 14000 | (1020, 16, 244, 46) | Needs shift to align with grid. |
| `Accent_Kpi_1` | `shape` | **226.40** | **68.80** | 5.00 | 88.00 | 23000 | (252, 72, 5, 88) | **VIOLATIONS**: X=226.40 < 252; Y=68.80 < 72. |
| `Card_Gross_Revenue` | `card` | **226.40** | **68.80** | 254.00 | 88.00 | 15000 | (252, 72, 246, 88) | **VIOLATIONS**: X=226.40 < 252; Y=68.80 < 72. |
| `Accent_Kpi_2` | `shape` | 492.40 | **68.80** | 5.00 | 88.00 | 24000 | (508, 72, 5, 88) | Y=68.80 < 72. |
| `Card_Market_Share` | `card` | 492.40 | **68.80** | 254.00 | 88.00 | 16000 | (508, 72, 246, 88) | Y=68.80 < 72. |
| `Accent_Kpi_3` | `shape` | 758.40 | **68.80** | 5.00 | 88.00 | 25000 | (764, 72, 5, 88) | Y=68.80 < 72. |
| `Card_Call_Attainment`| `card` | 758.40 | **68.80** | 254.00 | 88.00 | 17000 | (764, 72, 246, 88) | Y=68.80 < 72. |
| `Accent_Kpi_4` | `shape` | 1024.40 | **68.80** | 5.00 | 88.00 | 26000 | (1020, 72, 5, 88) | Y=68.80 < 72. |
| `Card_High_Risk_KOLs` | `card` | 1024.40 | **68.80** | 257.00 | 88.00 | 18000 | (1020, 72, 244, 88) | Y=68.80 < 72. |
| `Chart_Revenue_MarketShare` | `lineChart` | **215.00** | 183.75 | 611.25 | 250.00 | 19000 | (252, 172, 610, 256) | **VIOLATION**: X=215.00 < 252 (intrudes 25px into sidebar rail 0-240). |
| `1a9429b8f386195c3689` | `image` (basemap)| 867.50 | 172.65 | 387.91 | 266.10 | 27000 | (872, 172, 392, 256) | Minor recalibration needed. |
| `bbd908fa5bfdfc29dabb` | `shapeMap` | 867.50 | 180.15 | 393.75 | 255.00 | 28000 | (872, 172, 392, 256) | Minor recalibration needed. |
| `Chart_Brick_Ranking`| `clusteredBarChart`| **215.00** | 442.00 | 340.00 | 266.00 | 20000 | (252, 440, 330, 264) | **VIOLATION**: X=215.00 < 252 (intrudes 25px into sidebar rail 0-240). |
| `Chart_Distributor_Share`| `clusteredColumnChart`| 567.00 | 442.00 | 300.00 | 266.00 | 21000 | (592, 440, 300, 264) | X >= 252 (OK). Shift needed. |
| `Chart_Attainment_Tier`| `lineClusteredColumnComboChart`| 879.00 | 442.00 | 391.00 | 266.00 | 22000 | (902, 440, 362, 264) | X >= 252 (OK). Shift needed. |

---

#### Sections 1, 2, 3, 4: `Section2`, `Section3`, `Section4`, `Section5` (14 visuals each)
Across all 4 legacy sections, an identical layout template was used:
1. **Header Textbox**: `Header_*`:
   * Coordinates: `x: 20.00, y: 15.00, width: 1240.00, height: 65.00, z: 0.00`
   * **MAJOR COLLISION**: Spans from X=20 across to X=1260, completely colliding with the entire 240px navigation rail!
2. **Top 5 Metric Cards**:
   * `Card_S*_1`: `x: 20.00, y: 90.00, width: 235.00, height: 105.00, z: 5000.00` (**VIOLATION**: sits entirely at X: 20–255, completely colliding with the 240px navigation rail).
   * `Card_S*_2`: `x: 270.00, y: 90.00, width: 235.00, height: 105.00, z: 6000.00` (X >= 252, OK).
   * `Card_S*_3`: `x: 520.00, y: 90.00, width: 235.00, height: 105.00, z: 7000.00` (X >= 252, OK).
   * `Card_S*_4`: `x: 770.00, y: 90.00, width: 235.00, height: 105.00, z: 8000.00` (X >= 252, OK).
   * `Card_S*_5`: `x: 1020.00, y: 90.00, width: 240.00, height: 105.00, z: 9000.00` (X >= 252, OK).
3. **Mid-canvas Charts/Cards & Titles**:
   * Left Title `Title_S*_Chart1`: `x: 20.00, y: 215.00, height: 35.00` (**VIOLATION**: X=20).
   * Left Card/Chart Visual: `x: 20.00, y: 255.00, height: 220.00` (**VIOLATION**: X=20).
   * Right Title `Title_S*_Chart2`: X >= 500 (OK).
   * Right Card/Chart Visual: X >= 500 (OK).
4. **Bottom-canvas Charts/Cards & Titles**:
   * Left Title `Title_S*_Chart3`: `x: 20.00, y: 495.00, height: 35.00` (**VIOLATION**: X=20).
   * Left Card/Chart Visual: `x: 20.00, y: 535.00, height: 165.00` (**VIOLATION**: X=20).
   * Right Title `Title_S*_Chart4`: X >= 610 (OK).
   * Right Card/Chart Visual: X >= 610 (OK).
5. **Sidebar Assets & Action Buttons**:
   * **ZERO sidebar visuals exist on `Section2`, `Section3`, `Section4`, or `Section5`**.
   * **ZERO actionButton visuals exist**.
   * **ZERO top dropdown slicers exist**.

---

## 2. Logic Chain

1. **Premise 1 (Requirement R2)**: Requirement R2 mandates an Eight-Domain Navigation Rail across 8 analytical pages (`Section_Executive_Overview`, `Section_Doctors_KOLs`, `Section_Medical_Reps`, `Section_Bricks_Territory`, `Section_Visits_Activity`, `Section_Commercial_IQVIA`, `Section_Distributors_Stock`, `Section_Expenses_Budget`), each containing the corresponding `nav_sidebar_<page>.svg` asset at `(0, 0, 240, 720)` and 8 transparent `actionButton` visuals at X=12, W=216, H=40, Y=(134, 188, 242, 296, 350, 404, 458, 512).
2. **Observation Step 1**: In `report.json`, only 7 sections exist. Only `Section_Executive_Overview` has the target internal section ID. `Section2` corresponds to `Section_Commercial_IQVIA` but is misnamed. The remaining 6 target analytical pages (`Section_Doctors_KOLs`, `Section_Medical_Reps`, `Section_Bricks_Territory`, `Section_Visits_Activity`, `Section_Distributors_Stock`, `Section_Expenses_Budget`) do not exist as independent sections in `report.json`.
3. **Observation Step 2**: On `Section_Executive_Overview`, the existing sidebar is constructed using 11 deprecated, static visuals (`Nav_Sidebar_Bg` at width 205, `Nav_Brand_Logo` textbox, `Nav_Active_Pill` shape, and 8 textboxes). There are no `actionButton` visuals. On the other pages (`Section2`, `Section3`, `Section4`, `Section5`), there are zero sidebar visuals and zero action buttons.
4. **Premise 2 (Requirement R3)**: Requirement R3 mandates that all analytical visual containers (slicers at Y: 16–62, KPI cards at Y: 72–160, and charts in subsequent bands) strictly observe horizontal clearance at `X >= 252 px` with zero overlap with the 240px navigation rail.
5. **Observation Step 3**: On `Section_Executive_Overview`:
   * `Slicer_Line`, `Accent_Kpi_1`, and `Card_Gross_Revenue` reside at `X = 226.40`, directly invading the 240px sidebar buffer.
   * `Chart_Revenue_MarketShare` and `Chart_Brick_Ranking` reside at `X = 215.00`, deeply colliding (by 25 px) with the 240px sidebar.
   * `Card_Gross_Revenue`, `Card_Market_Share`, `Card_Call_Attainment`, and `Card_High_Risk_KOLs` sit at `Y = 68.80`, which is 3.2px above the Y: 72 boundary.
6. **Observation Step 4**: On `Section2`, `Section3`, `Section4`, and `Section5`:
   * Each has a full-width header (`Header_*`) at `X = 20`, spanning across the sidebar space.
   * Each has its primary KPI metric card (`Card_S*_1`) at `X = 20`, entirely within the 240px sidebar rail.
   * Each has 4 chart/title elements on the left side positioned at `X = 20`.
   * None of these pages have top slicers at Y: 16–62; their headers occupy Y: 15–80 and KPI cards occupy Y: 90–195.
7. **Conclusion Step**: Therefore, the current report state has severe structural gaps (only 1 of 8 target pages has correct internal naming, 0 of 8 pages have SVG sidebars or actionButtons), and extensive layout collisions (every single page violates X >= 252, and legacy pages place major visuals at X = 20).

---

## 3. Caveats

* **Caveat 1 — Semantic Model Measure Bindings**: The visual containers on legacy pages `Section2`, `Section3`, `Section4`, `Section5` reference authentic measures in `_Measures` (e.g. `_Measures.Total Revenue EGP`, `_Measures.Total Field Visits`, `_Measures.Total Pharmacy Audits`, `_Measures.High Churn Risk Doctor Count`). When decomposing or creating the 8 target pages, these queryRefs should be retained to preserve valid semantic model binding.
* **Caveat 2 — Resource Package Registration**: The 8 SVG files in `StaticResources/RegisteredResources/` must be registered in `report.json` under `resourcePackages[0].resourcePackage.items` as `type: 100` (or the appropriate resource item type) so that image visuals referencing them can be cleanly resolved by Power BI.
* **Caveat 3 — Hidden Pages (`Page 1`, `Page 2`)**: `Page 1` (`cd062f19f9ca363f1198`) contains a standalone ShapeMap of Greater Cairo bricks; `Page 2` (`761d32def22bced79044`) is empty. They are marked `displayOption: 1` (hidden) and do not collide with user navigation, but should either be cleaned up or retained as hidden auxiliary pages.

---

## 4. Conclusion

1. **Page Architecture Deficit**: `report.json` currently contains only 5 visible analytical pages (`Section_Executive_Overview`, `Section2`, `Section3`, `Section4`, `Section5`). To meet Acceptance Criteria for R2, the report structure must be expanded to exactly 8 analytical domain pages matching the specification:
   * `Section_Executive_Overview`
   * `Section_Doctors_KOLs`
   * `Section_Medical_Reps`
   * `Section_Bricks_Territory`
   * `Section_Visits_Activity`
   * `Section_Commercial_IQVIA` (migrate from `Section2`)
   * `Section_Distributors_Stock`
   * `Section_Expenses_Budget`
2. **Navigation Rail Implementation Required**:
   * On `Section_Executive_Overview`: Delete the 11 legacy visuals (`Nav_Sidebar_Bg`, `Nav_Brand_Logo`, `Nav_Active_Pill`, `Nav_Item_1_Active` through `Nav_Item_8`).
   * On all 8 pages: Inject the SVG sidebar image visual at `(0, 0, 240, 720, z: 10)` pointing to `nav_sidebar_<page>.svg`.
   * On all 8 pages: Inject 8 transparent `actionButton` visuals at `X = 12, width = 216, height = 40`, with `Y = [134, 188, 242, 296, 350, 404, 458, 512]`, configured with `drillFilterOtherVisuals: true` and `pageNavigation` bound to each corresponding domain page.
3. **Canvas Layout Calibration Required (X >= 252 px)**:
   * `Section_Executive_Overview`:
     - Slicers: Shift `Slicer_Line` from X=226.40 to 252 (W: 246, Y: 16, H: 46); recalibrate `Slicer_Zone` (X=508), `Slicer_Period` (X=764), `Slicer_Tier` (X=1020).
     - KPI Cards & Accent Shapes: Shift `Card_Gross_Revenue` & `Accent_Kpi_1` from X=226.40 to 252 (W: 246, Y: 72, H: 88); shift Y from 68.80 to 72 for all 4 cards and accent shapes.
     - Charts: Shift `Chart_Revenue_MarketShare` from X=215.00 to 252 (W: 610, Y: 172, H: 256); shift `Chart_Brick_Ranking` from X=215.00 to 252 (W: 330, Y: 440, H: 264); align distributor and attainment charts and ShapeMap to spec.
   * Other 7 Pages:
     - Remove or adjust the 1240px wide header textboxes currently starting at X=20.
     - Relocate left-aligned cards and charts from X=20 to `X >= 252`.
     - Standardize the 4 top dropdown slicers (Y: 16–62) and KPI cards (Y: 72–160).

---

## 5. Verification Method

### 5.1. File Inspection
1. **JSON Syntax & Structure Check**:
   View `powerbi/PharmaForce360.Report/report.json` to verify valid JSON formatting without BOM.
2. **Page Enumeration Verification**:
   Check `report.json` -> `"sections"` array:
   * Verify all 8 section names: `Section_Executive_Overview`, `Section_Doctors_KOLs`, `Section_Medical_Reps`, `Section_Bricks_Territory`, `Section_Visits_Activity`, `Section_Commercial_IQVIA`, `Section_Distributors_Stock`, `Section_Expenses_Budget`.
3. **Sidebar Visual & Action Button Audit**:
   For each section in `"sections"`:
   * Verify presence of SVG image visual at `x: 0, y: 0, width: 240, height: 720`.
   * Verify exactly 8 `actionButton` visuals at `x: 12, width: 216, height: 40` at `y: [134, 188, 242, 296, 350, 404, 458, 512]`.
   * Verify each button has `"pageNavigation"` action pointing to the corresponding section name.
4. **Coordinate Boundary Assertion**:
   * For every visual where `x < 240`: Assert it is either the sidebar SVG image (`width: 240`) or one of the 8 navigation `actionButton` visuals (`x: 12, width: 216`).
   * For all other visuals (slicers, KPI cards, charts): Assert `x >= 252.0`.
   * For slicers: Assert `y >= 16` and `y + height <= 64`.
   * For KPI cards: Assert `y >= 72` and `y + height <= 162`.

### 5.2. Invalidation Conditions
This investigation report is invalidated if:
* The report PBIP structure is located at a different path than `powerbi/PharmaForce360.Report/report.json`.
* The project requirements permit fewer than 8 analytical domain pages.
* Power BI action buttons cannot be embedded as native visuals in PBIP `report.json`.

# Original User Request

## 2026-10-11T04:52:08Z

Apply the Navigation Bar and Canvas Layer Architecture Specification (`docs/navigation_bar_specification.md`) across all 8 analytical report pages in the PharmaForce 360° Power BI PBIP project, eliminating white-box styling regressions, embedding vector SVG sidebars, configuring interactive native action buttons, and calibrating the 1280x720 canvas layout.

Working directory: D:\portfolio2026\02_PharmaForce360
Integrity mode: development

Specification reference: `docs/navigation_bar_specification.md`

## Requirements

### R1. Global Theme Hardening & Transparency Enforcement
Update `powerbi/theme.json` and registered report theme resources to enforce explicit 100% background transparency and disable borders for `actionButton`, `shape`, and `image` visual types, preventing wildcard container styling from creating opaque white cards or borders around navigation elements.

### R2. Eight-Domain Navigation Rail & Action Button Architecture
Incorporate the 240x720 px SVG sidebar backdrop assets from `StaticResources/RegisteredResources/` across all 8 analytical pages (`Section_Executive_Overview`, `Section_Doctors_KOLs`, `Section_Medical_Reps`, `Section_Bricks_Territory`, `Section_Visits_Activity`, `Section_Commercial_IQVIA`, `Section_Distributors_Stock`, `Section_Expenses_Budget`), overlaying 8 transparent native Power BI `actionButton` visuals per page at calibrated vertical coordinates (Y: 134, 188, 242, 296, 350, 404, 458, 512) with functional `pageNavigation` action bindings.

### R3. Canvas Grid Alignment & Collision Elimination
Calibrate all visual containers (slicers at Y: 16-62, KPI summary cards at Y: 72-160, and analytical charts in subsequent grid bands) to maintain clean horizontal clearance starting at X >= 252 px, ensuring zero overlap with the 240 px navigation rail.

### R4. Integrity Verification & Coordinate Compliance Audit
Perform JSON schema and syntax validation on modified PBIP files (`report.json` and `theme.json`), ensuring BOM-free UTF-8 encoding, valid Power BI visual definitions, and generate an audited coordinate compliance matrix verifying that visual boundaries and navigation targets adhere strictly to the specification.

## Acceptance Criteria

### Theme Styling
- [ ] `powerbi/theme.json` and `StaticResources/RegisteredResources/PharmaForce360Theme.json` include explicit overrides for `actionButton`, `shape`, and `image` with `"transparency": 100` and `"border": [{"show": false}]`.
- [ ] No visual within the sidebar coordinates (X <= 240) inherits an opaque white background (`#FFFFFF`) or card border.

### Page Navigation & Routing Structure
- [ ] All 8 analytical domains exist in `report.json` with matching internal names (`Section_Executive_Overview`, `Section_Doctors_KOLs`, `Section_Medical_Reps`, `Section_Bricks_Territory`, `Section_Visits_Activity`, `Section_Commercial_IQVIA`, `Section_Distributors_Stock`, `Section_Expenses_Budget`) and appropriate display names.
- [ ] Each of the 8 pages contains the corresponding `nav_sidebar_<page>.svg` background visual at `(0, 0, 240, 720)`.
- [ ] Each of the 8 pages contains 8 distinct `actionButton` visuals at X=12, width=216, height=40, positioned at Y=134, 188, 242, 296, 350, 404, 458, and 512 with `drillFilterOtherVisuals: true` and active `pageNavigation` actions.

### Canvas Layout Compliance
- [ ] All analytical slicers, KPI metric cards, and chart visuals reside strictly at X >= 252 px.
- [ ] Visual vertical positions strictly avoid overlap between top slicers (Y: 16-62) and KPI cards (Y: 72-160).

### Schema & Verification Deliverables
- [ ] `report.json` and `theme.json` parse cleanly without syntax errors and preserve valid PBIP structure.
- [ ] A coordinate compliance audit table is generated documenting the X, Y, W, H, Z-order, and navigation target for every visual across all 8 pages.

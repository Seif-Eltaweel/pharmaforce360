# 📊 Page Specification: 08 Promotional ROI and Budget (Expenses & Budget)
## PharmaForce 360° Commercial Intelligence Suite (Power BI PBIP)

> **Document Type**: Technical Page Specification & Visual Layout Architecture  
> **Target Page Name**: `08 Promotional ROI and Budget`  
> **Internal Section Name**: `Section_Expenses_Budget`  
> **Report Canvas**: 1280 x 720 px (16:9 HD Display Ratio)  
> **File Artifact**: `docs/spec_08_expenses_budget.md`  
> **Navigation Index**: Menu Item 8 of 8 (Active Pill at Y: 512)  
> **Generated Design Artifact**: `expenses_budget_dashboard_1791698721515.jpg`

---

## 🎯 1. Page Purpose & Analytical Objective

The **Promotional ROI and Budget** page serves as the commercial financial cockpit and governance engine for field investments across Greater Cairo. It enables Commercial Directors, Medical Advisors, and Regional Sales Managers to:
1. **Track Marketing Budget Execution**: Compare allocated promotional budgets against actual utilized investments across Egyptian pharmaceutical territories.
2. **Detect Free-Rider Leakage**: Identify non-compliant doctors who receive promotional benefits (sponsorships, congress travel, clinic branding, CME honoraria) without delivering incremental prescription lift.
3. **Audit Promotional ROI**: Quantify incremental Rx volume and revenue generated per EGP spent.
4. **Inspect Prescriber-Level Compliance**: Deep-dive into individual doctor profiles via an interactive Right Inspector Panel displaying compliance personas, historical logs, and real-time approval status.

---

## 🗺️ 2. Global Canvas & Navigation Layer

* **Canvas Dimensions**: `1280 x 720 px`
* **Background Theme**: `#F8FAFC` (Clinical light grey), with white rounded cards (`#FFFFFF`, border `#E2E8F0`, border-radius: 8px).
* **Navigation Sidebar**:
  * **Backdrop**: Vector SVG asset `StaticResources/RegisteredResources/nav_sidebar_expenses.svg` positioned at `(0, 0, 240, 720)`.
  * **Active Pill**: Item 8 highlighted (`Y: 512, H: 40, X: 12, W: 216`) with cyan pill glow `#00A3E0`.
  * **Buttons**: 8 native Power BI transparent `actionButton` visuals at Y coordinates `[134, 188, 242, 296, 350, 404, 458, 512]` bound to `pageNavigation`.
* **Analytical Canvas Boundary**: Starts at `X >= 252 px`, giving a usable analytical width of `1012 px` (X: 252 to 1264).

---

## 🎛️ 3. Visual Layout & Component Coordinate Blueprint

```
+-------------------------------------------------------------------------------------------------------------------------+
| [NAV SIDEBAR] | [TOP FILTER BAR] (X: 252, Y: 16, W: 1012, H: 46)                                                        |
| (0, 0, 240,   | Zone: Greater Cairo | Brick: Dokki & Mohandessin | Expense Category: All | Doctor Persona: All          |
|  720)         +-------------------------------------------------------------------------------+-------------------------+
|               | [TOP KPI CARDS] (Y: 72, H: 88)                                                | [RIGHT INSPECTOR PANEL] |
| 1. Overview   | Card 1: Total Budget (X: 252, W: 172)                                         | (X: 980, Y: 72,         |
| 2. Doctors    | Card 2: Utilized Spend & % (X: 432, W: 172)                                   |  W: 284, H: 632)        |
| 3. Reps       | Card 3: Free-Rider Leakage % (X: 612, W: 172)                                 |                         |
| 4. Bricks     | Card 4: Promotional ROI Ratio (X: 792, W: 172)                                | • Doctor Profile Card   |
| 5. Visits     +-------------------------------------------------------------------------------+   - Dr. Tamer Hosny     |
| 6. Drugs      | [UPPER ANALYTICAL CHART] (X: 252, Y: 172, W: 712, H: 256)                     |   - Free Rider Alert    |
| 7. Stock      | Monthly Budget vs Actual Spend with Rx Lift Trendline (Combo Bar + Line)      | • Quick Stats Cards     |
| 8. Expenses   +-------------------------------------------------------------------------------+ • Category Donut Chart  |
|    [ACTIVE]   | [LOWER ANALYTICAL CHART] (X: 252, Y: 440, W: 712, H: 264)                     | • Recent Expense Log    |
|               | Doctor Persona Breakdown & Free-Rider Leakage by Expense Category (Bar Chart) |   Audit Table           |
+-------------------------------------------------------------------------------------------------------------------------+
```

### Detailed Coordinate & Geometry Table

| # | Visual Name | Visual Type | Internal Identifier | X | Y | Width | Height | Z-Order | Primary Data Field / Measure |
|---|---|---|---|---|---|---|---|---|---|
| **01** | `Nav_Sidebar_Expenses` | `image` | `bg_nav_expenses` | 0 | 0 | 240 | 720 | 10 | `nav_sidebar_expenses.svg` |
| **02** | `Filter_Zone` | `slicer` | `slicer_zone` | 252 | 16 | 246 | 46 | 1010 | `dim_brick_territory[Zone]` |
| **03** | `Filter_Brick` | `slicer` | `slicer_brick` | 506 | 16 | 246 | 46 | 1020 | `dim_brick_territory[Brick_Name]` |
| **04** | `Filter_Category` | `slicer` | `slicer_expense_category` | 760 | 16 | 246 | 46 | 1030 | `fact_dr_expense[Expense_Category]` |
| **05** | `Filter_Persona` | `slicer` | `slicer_doctor_persona` | 1014 | 16 | 250 | 46 | 1040 | `fact_dr_expense[Doctor_Persona]` |
| **06** | `KPI_Total_Budget` | `card` | `kpi_total_budget` | 252 | 72 | 172 | 88 | 1110 | `[Total Promotional Budget EGP]` |
| **07** | `KPI_Utilized_Spend` | `card` | `kpi_utilized_spend` | 432 | 72 | 172 | 88 | 1120 | `[Total Promotional Expense EGP]`, `[Budget Utilized Pct]` |
| **08** | `KPI_Free_Rider_Leakage` | `card` | `kpi_leakage_pct` | 612 | 72 | 172 | 88 | 1130 | `[Free Rider Budget Leakage Pct]`, `[Free Rider Expense EGP]` |
| **09** | `KPI_Promotional_ROI` | `card` | `kpi_promotional_roi` | 792 | 72 | 172 | 88 | 1140 | `[Promotional ROI Ratio]` |
| **10** | `Chart_Budget_Vs_Spend_Trend` | `lineClusteredColumnCombo` | `chart_budget_trend` | 252 | 172 | 712 | 256 | 1210 | X: `dim_date[Month_Name_Short]`, Columns: `[Budget]`, `[Spend]`, Line: `[Incremental Rx Lift Units]` |
| **11** | `Chart_Persona_Leakage_Category` | `barChart` (Stacked) | `chart_persona_leakage` | 252 | 440 | 712 | 264 | 1220 | Y: `fact_dr_expense[Expense_Category]`, X: `[Total Promotional Expense EGP]`, Legend: `fact_dr_expense[Doctor_Persona]` |
| **12** | `Panel_Prescriber_Header` | `textbox` / `shape` | `panel_header_card` | 980 | 72 | 284 | 120 | 1310 | Doctor Avatar, Name, Specialty, Free Rider Alert Badge |
| **13** | `Panel_Quick_Stats` | `card` | `panel_quick_stats` | 980 | 200 | 284 | 80 | 1320 | `[Total Spent: 28,500 EGP]`, `[Promotional ROI: 0.8x]` |
| **14** | `Panel_Category_Donut` | `donutChart` | `panel_category_donut` | 980 | 288 | 284 | 180 | 1330 | Values: `[Total Promotional Expense EGP]`, Legend: `fact_dr_expense[Expense_Category]` |
| **15** | `Panel_Expense_Audit_Grid` | `tableEx` | `panel_audit_grid` | 980 | 476 | 284 | 228 | 1340 | Columns: `Expense_Date`, `Category`, `Amount_EGP`, `Approval_Status` |

---

## 📈 4. DAX Measures Specification

### 4.1. Core Budget & Spend Measures
```dax
Total Promotional Budget EGP = 
CALCULATE(
    SUM(fact_rep_targets[Promotional_Budget_Allocation_EGP]),
    ALLSELECTED(dim_date)
)

Total Promotional Expense EGP = 
SUM(fact_dr_expense[Amount_Of_Money_EGP])

Budget Utilized Pct = 
DIVIDE([Total Promotional Expense EGP], [Total Promotional Budget EGP], 0)
```

### 4.2. Free-Rider Leakage & Persona Compliance Measures
```dax
Free Rider Expense EGP = 
CALCULATE(
    [Total Promotional Expense EGP],
    fact_dr_expense[Is_Free_Rider] = TRUE()
)

Free Rider Budget Leakage Pct = 
DIVIDE([Free Rider Expense EGP], [Total Promotional Expense EGP], 0)

Free Rider Doctor Count = 
CALCULATE(
    DISTINCTCOUNT(fact_dr_expense[Doctor_ID]),
    fact_dr_expense[Is_Free_Rider] = TRUE()
)

Loyal Champion Expense EGP = 
CALCULATE(
    [Total Promotional Expense EGP],
    fact_dr_expense[Doctor_Persona] = "Loyal Champion"
)
```

### 4.3. Promotional ROI & Lift Measures
```dax
Incremental Rx Lift Units = 
SUM(fact_dr_expense[Incremental_Rx_Lift_Units])

Promotional Incremental Revenue EGP = 
SUMX(
    fact_dr_expense,
    fact_dr_expense[Incremental_Rx_Lift_Units] * 150 -- Benchmark Average Drug Realization Price
)

Promotional ROI Ratio = 
DIVIDE(
    [Promotional Incremental Revenue EGP],
    [Total Promotional Expense EGP],
    0
)
```

---

## 🔄 5. Interactivity, Cross-Filtering & Drill-Down Rules

1. **Category Bar Selection**: Clicking any category in the lower horizontal bar chart (e.g., `Congress Sponsorship`) filters the upper Monthly Trend to reflect spending on that category only, and restricts the Right Inspector Panel audit ledger to congress-related events.
2. **Doctor / Prescriber Selection**: Selecting a prescriber from any analytical visual populates the Right Inspector Panel with that specific doctor's compliance persona, historical spending breakdown, and approval log.
3. **Free-Rider Warning Threshold**:
   - If `Free Rider Budget Leakage Pct` exceeds **15%**, the KPI badge renders with an amber/red warning (`#EF4444`).
   - If `Promotional ROI Ratio` is above **3.0x**, the KPI badge renders with a success indicator (`#10B981`).
4. **Theme Transparency Integrity**:
   - Every button, card, and background in coordinates `X < 240` inherits `transparency: 100` and `border: false`.
   - Visual cards in `X >= 252` maintain clean white background `#FFFFFF` with `#E2E8F0` subtle borders and 8px corner radius.

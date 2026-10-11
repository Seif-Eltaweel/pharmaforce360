# PharmaForce 360 - Power BI Project (.pbip) Architecture and User Guide

> **Greater Cairo Pharmaceutical Market (Egypt) | Commercial Intelligence and Predictive Analytics Platform**  
> **Format**: Microsoft Power BI Project (.pbip) / Microsoft Fabric Ready  
> **All Financial Metrics**: Egyptian Pounds (**EGP**)

---

## Project Overview

This repository contains the complete, production-ready **Power BI Project (.pbip)** for the **PharmaForce 360 Commercial Intelligence Suite**. Designed using the Kimball Star Schema methodology, it models the operational realities of the pharmaceutical industry across **36 commercial bricks in Greater Cairo**, incorporating:

* **Egyptian Calendar Dynamics**: Saturday-Thursday work week, Friday strictly off, Holy Month of Ramadan operating shifts, and national holiday closures.
* **Turnover and S-Curve Recovery**: Mathematical Sigmoid ramp-up modeling rep transitions and doctor rapport rebuilding.
* **Closed-Loop Verification**: Direct linkage between physician detailing calls (act_rep_visits) and retail pharmacy shelf audits (act_pharmacy_visits).
* **Supply Chain Bifurcation**: Big 5 Egyptian distributors (*Ibn Sina, UCP, Soficopharm, PharmaOverseas, Ramco*) in core bricks vs Local Private Wholesalers (*El-Makhazen*) in peripheral areas.
* **AI Prescriber Copilot**: Machine-learning prescriber churn scoring, Next-Best-Action (NBA) prioritization, and Free-Rider budget leakage mitigation.

---

## How to Open and Refresh in Power BI Desktop

1. **Prerequisites**:
   * Microsoft Power BI Desktop (June 2023 release or newer).
2. **Opening the Project**:
   * Navigate to powerbi/ and double-click **PharmaForce360.pbip**.
   * Power BI Desktop will launch automatically, loading the semantic model and report layouts.
3. **Data Source Configuration**:
   * All queries parameterize the data path via the Power Query parameter **DataFolderPath**.
   * By default, it is configured to point directly to:  
     d:\portfolio2026\02_PharmaForce360\data\
   * If you move the project or clone it on another workstation:
     1. Click **Home > Transform Data > Edit Parameters**.
     2. Update DataFolderPath to your local data/ path (with trailing slash \).
     3. Click **Apply Changes** to refresh all 18 tables in seconds.

---

## Data Model Architecture (Star Schema)

`
                                  +-----------------------+
                                  |       dim_date        |
                                  +-----------+-----------+
                                              |
                      +-----------------------+-----------------------+
                      |                       |                       |
           +----------+----------+ +----------+----------+ +----------+----------+
           |   fact_rep_visits   | |fact_pharmacy_visits | | fact_pharmacy_sales |
           +----------+----------+ +----------+----------+ +----------+----------+
                      |                       |                       |
      +---------------+---------------+       |       +---------------+---------------+
      |                               |       |       |                               |
+-----+----------+             +------+-------+ +----+------------+            +-----+----------+
|   dim_doctor   |             | dim_pharmacy  | |   dim_product   |            |dim_brick_terr. |
+----------------+             +---------------+ +-----------------+            +----------------+
`

* **Central Measure Store**: _Measures table containing 42 formatted DAX calculations organized across 5 dedicated display folders.
* **10 Dimension Tables**: dim_date, dim_brick_territory, dim_product, dim_competitor_product, dim_medical_rep, dim_doctor, dim_doctor_schedule, dim_pharmacy, dim_distributor, dim_account.
* **8 Fact Tables**: act_pharmacy_sales, act_rep_visits, act_pharmacy_visits, act_rep_targets, act_rep_weekly_plan, act_dr_expense, act_ims_market_audit, act_doctor_predictions.
* **Single-Direction Filtering**: 35 clean relationships with inactive paths utilized for closed-loop verification to prevent circular ambiguous paths.

---

## 5-Page Persona Dashboard Suite

### Page 1: Executive Overview (Main Overall Cockpit)
* **Target Audience**: Chief Commercial Officer, VP of Sales, General Manager.
* **Layout & Theme**: Modern Clinical & Corporate Clean aesthetic featuring a deep royal navy left navigation sidebar (`#071E54`) with glowing cyan active tab indicator, top live status badge (`● Live Model: 24-Month Active Run`), 4 dropdown slicers (`Line`, `Zone`, `Period`, `Tier`), 4 modern white rounded KPI cards with left vertical color accents (`Gross Revenue: 48,720,450 EGP`, `Market Share: 28.4%`, `Call Attainment: 91.8%`, `High-Risk KOLs: 47`), dual-axis shaded area wave chart (`Gross Revenue & Market Share` over 24 Months), **Native Custom Shape Map (`shapeMap`)** rendering Greater Cairo's 36 administrative commercial brick boundary polygons (`cairo_commercial_bricks.topojson`) with clinical cyan-to-red gradient saturation (`#EF4444` to `#00A3E0`), and 3 bottom analytical breakdowns (`Cairo Brick Ranking`, `Distributor Market Share`, `Call Attainment Tier Segmentation`). Interactive clicking on any municipal district polygon triggers bidirectional cross-filtering across all cards, distributors, and trend velocity.

### Page 2: Executive Commercial Performance and IQVIA Audit
* **Target Audience**: Commercial Director, Finance Lead, Business Unit Heads.
* **Key Features**: Sales vs Target Quotas in EGP, Monthly trajectory vs target line, Distributor channel split (Big 5 vs El-Makhazen Local Wholesalers), IQVIA Evolution Index (EI) growth classification, and competitor pricing gap benchmark.

### Page 3: Field Force Activity and Detailing Operations
* **Target Audience**: National Sales Manager, Regional District Managers.
* **Key Features**: Detailing calls leaderboard, AM Hospital vs PM Clinic distribution, Tier A Key Opinion Leader (KOL) coverage rate, weekly call plan submission discipline (Saturday on-time vs late), and Cairo rainstorm traffic delays vs replacement rep S-curve ramp-up tracking.

### Page 4: Territory Brick Dynamics and Pharmacy Audit
* **Target Audience**: Trade Marketing Manager, Key Account Manager, Supply Chain Director.
* **Key Features**: Greater Cairo 36-brick potential index vs secondary sell-out, retail stock-out rate across major chains (*Seif, El Ezaby, 19011, Rushdy*), closed-loop physician-detailing to pharmacy-dispensing verification, and emergency stock transfer order tracking.

### Page 5: AI Prescriber Copilot and Marketing ROI
* **Target Audience**: Commercial Excellence Lead, Brand Managers, Field Reps.
* **Key Features**: ML-predicted prescriber churn tiers (High Risk, Medium, Loyal), sortable Next-Best-Action (NBA) priority queue, promotional spend breakdown (Advisory boards, CME sponsorships, clinic grants), Free-Rider budget leakage detection, and incremental Rx lift ROI ratio.

---

## Design System and Visual Palette

* **Primary Dark Navy**: #0A2540
* **Clinical Cyan (Brand)**: #00A3E0
* **Medical Teal**: #00B4D8
* **Success Green**: #10B981
* **Warning Amber**: #F59E0B
* **Danger Red**: #EF4444
* **Background Canvas**: #F8FAFC
* **Cards and Containers**: #FFFFFF with #E2E8F0 subtle borders and 8px border radius.
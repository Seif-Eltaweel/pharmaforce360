# 🏥 PharmaForce 360° Commercial Intelligence Suite

> **Greater Cairo Pharmaceutical Market (Egypt) | Commercial Intelligence & Predictive Analytics Platform**

[![Power BI](https://img.shields.io/badge/Power_BI-PBIP_Format-F2C811?logo=powerbi&logoColor=black)](powerbi/PharmaForce360.pbip)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](requirements.txt)
[![Data Model](https://img.shields.io/badge/Architecture-Kimball_Star_Schema-2563EB)](sql/)
[![Market](https://img.shields.io/badge/Market-Greater_Cairo_EGP-059669)](data/maps/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Overview

**PharmaForce 360°** is an end-to-end commercial operations and predictive intelligence suite tailored specifically for the pharmaceutical industry in Egypt. Modeling the **Greater Cairo Pharmaceutical Market**, it mirrors the real-world operational workflows of pharmaceutical manufacturers, medical sales representatives, key opinion leaders (KOLs), panel pharmacies, and primary pharmaceutical distributors (*Ibn Sina, UCP, Soficopharm, PharmaOverseas, Ramco*).

All financial and commercial metrics are strictly modeled in **Egyptian Pounds (EGP)**.

---

## 🏛️ System Architecture & Data Model

The analytical platform is designed around a high-performance **Star Schema (Kimball Methodology)**:

```
                                  ┌───────────────────────┐
                                  │       dim_date        │
                                  └───────────┬───────────┘
                                              │
                      ┌───────────────────────┼───────────────────────┐
                      │                       │                       │
           ┌──────────┴──────────┐ ┌──────────┴──────────┐ ┌──────────┴──────────┐
           │   fact_rep_visits   │ │fact_pharmacy_visits │ │ fact_pharmacy_sales │
           └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                      │                       │                       │
      ┌───────────────┴───────────────┐       │       ┌───────────────┴───────────────┐
      │                               │       │       │                               │
┌─────┴──────────┐             ┌──────┴───────┴┐ ┌────┴────────────┐            ┌─────┴──────────┐
│   dim_doctor   │             │ dim_pharmacy  │ │   dim_product   │            │dim_brick_terr. │
└────────────────┘             └───────────────┘ └─────────────────┘            └────────────────┘
```

### Core Entities & Dimensions
* **`dim_date`**: 24 months (2025–2026), Saturday–Thursday work week (Friday off), Egyptian national holidays, and Holy Month of Ramadan operating hours.
* **`dim_brick_territory`**: 36 Greater Cairo commercial bricks across Cairo, Giza, and southern Qalyubia mapped across 6 zones with centroid GPS coordinates and socioeconomic tiers (Tiers 1–3).
* **`dim_account`**: 113 key institutional healthcare accounts (University Teaching Hospitals, MoHP Specialized Institutes, Military Complexes, and Private Hospital Groups).
* **`dim_distributor`**: Top 5 Egyptian distributors (*Ibn Sina, United Company of Pharmacists - UCP, Soficopharm, PharmaOverseas, Ramco*) + parallel wholesale distributors (*المخازن*).
* **`dim_product` & `dim_competitor_product`**: Cardiovascular and Respiratory/CNS product portfolios with EGP pricing and direct market rivals (*Concor, Crestor, Jardiance, Vastarel, Symbicort, Cipralex, Singulair*).
* **`dim_medical_rep`**: Field medical representatives with hierarchy, territory assignments, and tenure tracking.
* **`dim_doctor` & `dim_doctor_schedule`**: Healthcare professionals across specialties with pivoted weekly shift timetables and clinic catchment zones.
* **`dim_pharmacy`**: Panel pharmacies with footfall tiers and distributor affiliations.

### Transactional & Analytical Facts
* **`fact_rep_weekly_plan`**: Rep weekly detailing targets and submission compliance.
* **`fact_rep_visits`**: ~45,000 field detailing interactions (AM institutional visits vs PM private clinics).
* **`fact_pharmacy_visits`**: ~15,000 pharmacy verification audits and stock-out tracking.
* **`fact_pharmacy_sales`**: Monthly secondary sales revenue in EGP incorporating territory potential and supply shifts.
* **`fact_rep_targets`**: Quota assignments per representative and product line in EGP.
* **`fact_dr_expense`**: Promotional investments, CME sponsorships, and compliance personas.
* **`fact_ims_market_audit`**: Audited IQVIA brick market shares and Evolution Index (EI).
* **`fact_doctor_predictions`**: Predictive ML churn scoring and Next-Best-Action (NBA) prescriber prioritization.

---

## 📂 Directory Structure

```text
02_PharmaForce360/
├── README.md                                # Project documentation and operational guide
├── requirements.txt                         # Python dependencies for ML & data generation
├── scripts/                                 # Generator, build wrapper & inspection tools
│   ├── generate_colab_notebook.py           # Programmatic 21-cell notebook compiler
│   ├── build_colab_notebook.ps1             # PowerShell wrapper to compile notebook
│   ├── inspect_nb.ps1                       # Notebook cell structure validator
│   └── dump_cells.ps1                       # Cell source code extractor
├── notebooks/
│   └── PharmaForce360_Data_Generator.ipynb  # 21-cell Google Colab modular data generator
├── data/                                    # Generated CSV datasets & zipped archives
├── sql/                                     # Analytical star schema DDL & queries
├── powerbi/                                 # DAX formulas, data model definitions, & themes
└── docs/                                    # Data dictionary, taxonomy & handoff specs
    └── HANDOFF.md                           # Implementation handoff and cell architecture spec
```

---

## 🚀 Execution & Quickstart

### Option A: Google Colab Synthetic Data Generation
1. Upload [notebooks/PharmaForce360_Data_Generator.ipynb](file:///d:/portfolio2026/02_PharmaForce360/notebooks/PharmaForce360_Data_Generator.ipynb) to **Google Colab**.
2. Run cells sequentially (Cells 1 through 21).
3. The final cell bundles all 15 CSVs into `pharmaforce360_cairo_dataset.zip` and triggers an automatic browser download.
4. Extract the CSV files into the [data/](file:///d:/portfolio2026/02_PharmaForce360/data) folder.

### Local Python Environment
```bash
cd 02_PharmaForce360
pip install -r requirements.txt
```

### Option B: Power BI Desktop Project (.pbip)
1. Open the [powerbi/](file:///d:/portfolio2026/02_PharmaForce360/powerbi) directory.
2. Double-click [PharmaForce360.pbip](file:///d:/portfolio2026/02_PharmaForce360/powerbi/PharmaForce360.pbip) in **Power BI Desktop**.
3. The project auto-connects to the CSV datasets in [data/](file:///d:/portfolio2026/02_PharmaForce360/data) via the `DataFolderPath` parameter with 19 tables, 35 relationships, 42 DAX measures, and a 5-page persona-driven dashboard suite.
4. Detailed documentation is available in [powerbi/README_POWERBI.md](file:///d:/portfolio2026/02_PharmaForce360/powerbi/README_POWERBI.md) and [powerbi/dax_measures.md](file:///d:/portfolio2026/02_PharmaForce360/powerbi/dax_measures.md).

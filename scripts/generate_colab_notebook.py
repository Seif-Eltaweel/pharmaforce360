# -*- coding: utf-8 -*-
"""
Script to build the 21-cell Google Colab Notebook PharmaForce360_Data_Generator.ipynb
Following cell-by-cell architecture and Option A auto-download as specified in HANDOFF.md.
"""
import json
import os
import sys

cells = []

def add_md(text):
    lines = text.strip().split('\n')
    src = [line + '\n' for line in lines[:-1]]
    if lines:
        src.append(lines[-1])
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": src
    })

def add_code(code_str):
    lines = code_str.strip().split('\n')
    src = [line + '\n' for line in lines[:-1]]
    if lines:
        src.append(lines[-1])
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src
    })

# -----------------------------------------------------------------------------
# CELL 0: TITLE & OVERVIEW MARKDOWN
# -----------------------------------------------------------------------------
add_md("""# 🏥 PharmaForce 360° Commercial Intelligence Suite
## Synthetic Pharmaceutical Commercial Data Generator (Greater Cairo Market - EGP)

This modular notebook generates the complete **18-table synthetic pharmaceutical dataset** for the Greater Cairo region (Egypt).
Each code cell builds one specific dimension or fact table, displays `.head(2)`, and saves the resulting CSV.

- **Market Focus:** Greater Cairo Pharmaceutical Market (Egypt)
- **Currency:** Egyptian Pounds (EGP)
- **Workweek:** Saturday – Thursday (Friday Official Weekend)
- **Methodology:** Kimball Star Schema (Life Sciences Commercial Intelligence)
- **Automation:** Option A Auto-Zip & 1-Click Browser Download""")

# -----------------------------------------------------------------------------
# CELL 1: SETUP, DEPENDENCIES & CONSTANTS
# -----------------------------------------------------------------------------
add_md("### ⚙️ Cell 1: Setup, Dependencies & Constants")

add_code('''# Cell 1: Setup, Dependencies & Constants
try:
    import google.colab
    IN_COLAB = True
    print("🌐 Google Colab environment detected. Installing required packages...")
    !pip install faker pandas numpy scikit-learn lightgbm shap -q
except ImportError:
    IN_COLAB = False
    print("💻 Local Python/Jupyter environment detected.")

import os
import random
import math
import shutil
import zipfile
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker

# Set global deterministic random seed
SEED = 42
np.random.seed(SEED)
random.seed(SEED)
fake = Faker('en_US')
Faker.seed(SEED)

OUTPUT_DIR = "output_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"✅ Initialized environment. Random Seed: {SEED}. Output directory: '{OUTPUT_DIR}/'")''')

# -----------------------------------------------------------------------------
# CELL 2: dim_date.csv
# -----------------------------------------------------------------------------
add_md("### 📅 Cell 2: `dim_date.csv` (24 Months: 2025–2026, Sat–Thu Work Week, Ramadan Flags & Egyptian Holidays)")

add_code('''# Cell 2: dim_date.csv
start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='D')

dim_date = pd.DataFrame({'Date': date_range})
dim_date['Date_Key'] = dim_date['Date'].dt.strftime('%Y%m%d').astype(int)
dim_date['Year'] = dim_date['Date'].dt.year
dim_date['Quarter'] = dim_date['Date'].dt.to_period('Q').astype(str)
dim_date['Month'] = dim_date['Date'].dt.month
dim_date['Month_Name'] = dim_date['Date'].dt.strftime('%B')
dim_date['Day'] = dim_date['Date'].dt.day
dim_date['Day_Of_Week'] = dim_date['Date'].dt.day_name()
dim_date['Year_Month'] = dim_date['Date'].dt.strftime('%Y-%m')

# Work week in Egypt: Saturday - Thursday (Friday off)
dim_date['Is_Weekend'] = dim_date['Day_Of_Week'].isin(['Friday'])

# Holy Month of Ramadan operating hours in Egypt
# 2025: Feb 28 to March 29; 2026: Feb 17 to March 19
dim_date['Is_Ramadan'] = ((dim_date['Date'] >= '2025-02-28') & (dim_date['Date'] <= '2025-03-29')) | \\
                         ((dim_date['Date'] >= '2026-02-17') & (dim_date['Date'] <= '2026-03-19'))

# Egyptian National & Religious Holidays (Zero field visits scheduled)
egyptian_holidays = {
    # 2025 Holidays
    "2025-01-07": "Coptic Christmas Day",
    "2025-01-25": "Police Day & Revolution Day",
    "2025-03-30": "Eid al-Fitr (Day 1)",
    "2025-03-31": "Eid al-Fitr (Day 2)",
    "2025-04-01": "Eid al-Fitr (Day 3)",
    "2025-04-21": "Sham El-Nessim",
    "2025-04-25": "Sinai Liberation Day",
    "2025-05-01": "Labour Day",
    "2025-06-05": "Arafat Day",
    "2025-06-06": "Eid al-Adha (Day 1)",
    "2025-06-07": "Eid al-Adha (Day 2)",
    "2025-06-08": "Eid al-Adha (Day 3)",
    "2025-06-26": "Islamic New Year (Hijri 1447)",
    "2025-06-30": "June 30 Revolution Day",
    "2025-09-04": "Prophet's Birthday (Mawlid)",
    "2025-10-06": "Armed Forces Day (6th of October)",
    # 2026 Holidays
    "2026-01-07": "Coptic Christmas Day",
    "2026-01-25": "Police Day & Revolution Day",
    "2026-03-20": "Eid al-Fitr (Day 1)",
    "2026-03-21": "Eid al-Fitr (Day 2)",
    "2026-03-22": "Eid al-Fitr (Day 3)",
    "2026-04-13": "Sham El-Nessim",
    "2026-04-25": "Sinai Liberation Day",
    "2026-05-01": "Labour Day",
    "2026-05-26": "Arafat Day",
    "2026-05-27": "Eid al-Adha (Day 1)",
    "2026-05-28": "Eid al-Adha (Day 2)",
    "2026-05-29": "Eid al-Adha (Day 3)",
    "2026-06-16": "Islamic New Year (Hijri 1448)",
    "2026-06-30": "June 30 Revolution Day",
    "2026-08-24": "Prophet's Birthday (Mawlid)",
    "2026-10-06": "Armed Forces Day (6th of October)"
}

date_str_series = dim_date['Date'].dt.strftime('%Y-%m-%d')
dim_date['Holiday_Name'] = date_str_series.map(egyptian_holidays).fillna("None")
dim_date['Is_Egyptian_Holiday'] = dim_date['Holiday_Name'] != "None"

# Official field workdays: Saturday-Thursday, excluding holidays
dim_date['Is_Workday'] = (~dim_date['Is_Weekend']) & (~dim_date['Is_Egyptian_Holiday'])

# Cairo Winter Rain Events (Severe traffic congestion on Ring Road & Salah Salem)
winter_rain_dates = {
    "2025-01-14", "2025-01-28", "2025-02-11", "2025-02-24", "2025-12-16", "2025-12-29",
    "2026-01-12", "2026-01-26", "2026-02-09", "2026-02-23", "2026-12-15", "2026-12-28"
}
dim_date['Is_Winter_Rain_Event'] = date_str_series.isin(winter_rain_dates)

dim_date.to_csv(f"{OUTPUT_DIR}/dim_date.csv", index=False)
print("dim_date.csv created successfully. Total Days:", len(dim_date), "| Workdays:", dim_date['Is_Workday'].sum())
dim_date.head(2)''')

# -----------------------------------------------------------------------------
# CELL 3: dim_brick_territory.csv
# -----------------------------------------------------------------------------
add_md("### 🗺️ Cell 3: `dim_brick_territory.csv` (28 Greater Cairo Bricks across 6 Zones & Socioeconomic Tiers)")

add_code('''# Cell 3: dim_brick_territory.csv
cairo_bricks = [
    # East Cairo (High density, established middle & affluent medical corridors)
    {"Brick_ID": "BRK-01", "Brick_Name": "Nasr City East", "Zone": "East Cairo", "Tier": 2, "Latitude": 30.0561, "Longitude": 31.3412, "Territory_Potential_Index": 1.15},
    {"Brick_ID": "BRK-02", "Brick_Name": "Nasr City West", "Zone": "East Cairo", "Tier": 2, "Latitude": 30.0610, "Longitude": 31.3250, "Territory_Potential_Index": 1.10},
    {"Brick_ID": "BRK-03", "Brick_Name": "Heliopolis (Masr El Gedida)", "Zone": "East Cairo", "Tier": 1, "Latitude": 30.0898, "Longitude": 31.3285, "Territory_Potential_Index": 1.45},
    {"Brick_ID": "BRK-04", "Brick_Name": "Sheraton & Nozha", "Zone": "East Cairo", "Tier": 1, "Latitude": 30.1054, "Longitude": 31.3789, "Territory_Potential_Index": 1.30},
    # New Cairo & Settlements (High purchasing power, modern specialty clinics)
    {"Brick_ID": "BRK-05", "Brick_Name": "Fifth Settlement North", "Zone": "New Cairo", "Tier": 1, "Latitude": 30.0245, "Longitude": 31.4720, "Territory_Potential_Index": 1.50},
    {"Brick_ID": "BRK-06", "Brick_Name": "Fifth Settlement South", "Zone": "New Cairo", "Tier": 1, "Latitude": 30.0050, "Longitude": 31.4850, "Territory_Potential_Index": 1.40},
    {"Brick_ID": "BRK-07", "Brick_Name": "First & Third Settlements", "Zone": "New Cairo", "Tier": 2, "Latitude": 30.0450, "Longitude": 31.4320, "Territory_Potential_Index": 1.05},
    {"Brick_ID": "BRK-08", "Brick_Name": "Madinaty & Rehab", "Zone": "New Cairo", "Tier": 1, "Latitude": 30.0820, "Longitude": 31.6320, "Territory_Potential_Index": 1.35},
    # Downtown & Central (Historic medical clusters, academic hubs, high patient volume)
    {"Brick_ID": "BRK-09", "Brick_Name": "Downtown (Wust El Balad)", "Zone": "Downtown & Central", "Tier": 2, "Latitude": 30.0444, "Longitude": 31.2357, "Territory_Potential_Index": 1.05},
    {"Brick_ID": "BRK-10", "Brick_Name": "Zamalek", "Zone": "Downtown & Central", "Tier": 1, "Latitude": 30.0634, "Longitude": 31.2185, "Territory_Potential_Index": 1.40},
    {"Brick_ID": "BRK-11", "Brick_Name": "Garden City & Kasr Al-Ainy", "Zone": "Downtown & Central", "Tier": 1, "Latitude": 30.0350, "Longitude": 31.2310, "Territory_Potential_Index": 1.50},
    {"Brick_ID": "BRK-12", "Brick_Name": "Shubra", "Zone": "Downtown & Central", "Tier": 3, "Latitude": 30.0815, "Longitude": 31.2460, "Territory_Potential_Index": 0.85},
    # Giza & Dokki (Major private hospital and clinic hub for Western Greater Cairo)
    {"Brick_ID": "BRK-13", "Brick_Name": "Mohandessin", "Zone": "Giza & Dokki", "Tier": 1, "Latitude": 30.0528, "Longitude": 31.1995, "Territory_Potential_Index": 1.45},
    {"Brick_ID": "BRK-14", "Brick_Name": "Dokki", "Zone": "Giza & Dokki", "Tier": 1, "Latitude": 30.0384, "Longitude": 31.2124, "Territory_Potential_Index": 1.35},
    {"Brick_ID": "BRK-15", "Brick_Name": "Agouza", "Zone": "Giza & Dokki", "Tier": 2, "Latitude": 30.0601, "Longitude": 31.2115, "Territory_Potential_Index": 1.15},
    {"Brick_ID": "BRK-16", "Brick_Name": "Giza City & Faisal", "Zone": "Giza & Dokki", "Tier": 3, "Latitude": 30.0080, "Longitude": 31.1850, "Territory_Potential_Index": 0.80},
    {"Brick_ID": "BRK-17", "Brick_Name": "Haram (Al-Ahram)", "Zone": "Giza & Dokki", "Tier": 2, "Latitude": 29.9980, "Longitude": 31.1550, "Territory_Potential_Index": 0.95},
    # South Cairo & Maadi (Diplomatic and upper-middle medical centers)
    {"Brick_ID": "BRK-18", "Brick_Name": "Maadi Sarayat & Degla", "Zone": "South Cairo", "Tier": 1, "Latitude": 29.9580, "Longitude": 31.2750, "Territory_Potential_Index": 1.40},
    {"Brick_ID": "BRK-19", "Brick_Name": "New Maadi & Zahraa", "Zone": "South Cairo", "Tier": 2, "Latitude": 29.9690, "Longitude": 31.2990, "Territory_Potential_Index": 1.10},
    {"Brick_ID": "BRK-20", "Brick_Name": "Mokattam", "Zone": "South Cairo", "Tier": 2, "Latitude": 30.0190, "Longitude": 31.3020, "Territory_Potential_Index": 1.00},
    {"Brick_ID": "BRK-21", "Brick_Name": "Helwan", "Zone": "South Cairo", "Tier": 3, "Latitude": 29.8450, "Longitude": 31.3320, "Territory_Potential_Index": 0.75},
    # West Cairo & 6th October (Booming satellite hub, large hospital compounds)
    {"Brick_ID": "BRK-22", "Brick_Name": "Sheikh Zayed Central", "Zone": "West Cairo (October)", "Tier": 1, "Latitude": 30.0520, "Longitude": 30.9850, "Territory_Potential_Index": 1.45},
    {"Brick_ID": "BRK-23", "Brick_Name": "Sheikh Zayed Beverly Hills", "Zone": "West Cairo (October)", "Tier": 1, "Latitude": 30.0680, "Longitude": 30.9420, "Territory_Potential_Index": 1.35},
    {"Brick_ID": "BRK-24", "Brick_Name": "6th October Dist 1-5", "Zone": "West Cairo (October)", "Tier": 2, "Latitude": 29.9720, "Longitude": 30.9450, "Territory_Potential_Index": 1.10},
    {"Brick_ID": "BRK-25", "Brick_Name": "6th October Dist 6-12", "Zone": "West Cairo (October)", "Tier": 3, "Latitude": 29.9510, "Longitude": 30.9150, "Territory_Potential_Index": 0.80},
    {"Brick_ID": "BRK-26", "Brick_Name": "Hadayek October", "Zone": "West Cairo (October)", "Tier": 2, "Latitude": 29.9250, "Longitude": 31.0250, "Territory_Potential_Index": 0.95},
    {"Brick_ID": "BRK-27", "Brick_Name": "Smart Village Complex", "Zone": "West Cairo (October)", "Tier": 1, "Latitude": 30.0750, "Longitude": 31.0180, "Territory_Potential_Index": 1.25},
    {"Brick_ID": "BRK-28", "Brick_Name": "Hadayek Al-Ahram", "Zone": "West Cairo (October)", "Tier": 2, "Latitude": 29.9800, "Longitude": 31.1150, "Territory_Potential_Index": 0.95}
]

dim_brick_territory = pd.DataFrame(cairo_bricks)
dim_brick_territory.to_csv(f"{OUTPUT_DIR}/dim_brick_territory.csv", index=False)
print("dim_brick_territory.csv created successfully. Rows:", len(dim_brick_territory))
dim_brick_territory.head(2)''')

# -----------------------------------------------------------------------------
# CELL 4: dim_account.csv
# -----------------------------------------------------------------------------
add_md("### 🏥 Cell 4: `dim_account.csv` (Master AM Institutional Accounts: Hospitals, Centers, Complex Units)")

add_code('''# Cell 4: dim_account.csv
# Institutional accounts visited in morning (AM) detailing sessions
accounts_data = [
    {"Account_ID": "ACC-001", "Account_Name": "Kasr Al Ainy Teaching Hospital", "Account_Type": "University Hospital", "Brick_ID": "BRK-11", "Bed_Capacity": 3200, "Key_Specialties": "Cardiology, Internal Medicine, Chest, Neuro"},
    {"Account_ID": "ACC-002", "Account_Name": "Ain Shams University Specialized Hospital", "Account_Type": "University Hospital", "Brick_ID": "BRK-02", "Bed_Capacity": 1200, "Key_Specialties": "Cardiology, Endocrinology, Pulmonology"},
    {"Account_ID": "ACC-003", "Account_Name": "Cleopatra Hospital", "Account_Type": "Private Hospital Group", "Brick_ID": "BRK-03", "Bed_Capacity": 250, "Key_Specialties": "Cardiology, Neurology, Internal Medicine"},
    {"Account_ID": "ACC-004", "Account_Name": "Dar Al Fouad Hospital (6th Oct)", "Account_Type": "Private Specialized Center", "Brick_ID": "BRK-24", "Bed_Capacity": 300, "Key_Specialties": "Cardiology, Cardiothoracic, Vascular"},
    {"Account_ID": "ACC-005", "Account_Name": "As-Salam International Hospital (Maadi)", "Account_Type": "Private Hospital Group", "Brick_ID": "BRK-18", "Bed_Capacity": 350, "Key_Specialties": "Cardiology, Pulmonology, Neurology"},
    {"Account_ID": "ACC-006", "Account_Name": "National Heart Institute (Imbaba)", "Account_Type": "Specialized National Center", "Brick_ID": "BRK-15", "Bed_Capacity": 800, "Key_Specialties": "Cardiology, Interventional Cath, CCU"},
    {"Account_ID": "ACC-007", "Account_Name": "Air Force Specialized Hospital", "Account_Type": "Military / Public Tier 1", "Brick_ID": "BRK-05", "Bed_Capacity": 450, "Key_Specialties": "Multidisciplinary, Chest, Neuro, Cardio"},
    {"Account_ID": "ACC-008", "Account_Name": "Saudi German Hospital (Cairo)", "Account_Type": "Private Hospital Group", "Brick_ID": "BRK-01", "Bed_Capacity": 300, "Key_Specialties": "Cardiology, Diabetes, Pulmonology"},
    {"Account_ID": "ACC-009", "Account_Name": "Magdi Yacoub Heart Center Project", "Account_Type": "Specialized NGO / Foundation", "Brick_ID": "BRK-22", "Bed_Capacity": 200, "Key_Specialties": "Pediatric & Adult Cardiology"},
    {"Account_ID": "ACC-010", "Account_Name": "Petroleum Hospital Complex", "Account_Type": "Corporate / Institutional", "Brick_ID": "BRK-04", "Bed_Capacity": 220, "Key_Specialties": "Occupational, Chronic Disease, Cardio"},
    {"Account_ID": "ACC-011", "Account_Name": "National Bank of Egypt (NBE) Healthcare Center", "Account_Type": "Corporate HQ Center", "Brick_ID": "BRK-09", "Bed_Capacity": 120, "Key_Specialties": "Internal Medicine, Diabetes, Neuro"},
    {"Account_ID": "ACC-012", "Account_Name": "Police Hospital (Agouza)", "Account_Type": "Government Specialized", "Brick_ID": "BRK-15", "Bed_Capacity": 400, "Key_Specialties": "Cardiology, Chest, Orthopedics"},
    {"Account_ID": "ACC-013", "Account_Name": "Al Demerdash Hospital", "Account_Type": "University Hospital", "Brick_ID": "BRK-02", "Bed_Capacity": 1500, "Key_Specialties": "Cardiology, Neurology, Chest, Nephrology"},
    {"Account_ID": "ACC-014", "Account_Name": "Sheikh Zayed Specialized Hospital", "Account_Type": "Ministry of Health Specialized", "Brick_ID": "BRK-22", "Bed_Capacity": 350, "Key_Specialties": "Critical Care, Cardiology, Chest"},
    {"Account_ID": "ACC-015", "Account_Name": "International Medical Center (IMC)", "Account_Type": "Military Tertiary Center", "Brick_ID": "BRK-08", "Bed_Capacity": 800, "Key_Specialties": "Tertiary Referral, Cardio, Neuro"},
    {"Account_ID": "ACC-016", "Account_Name": "Banque Misr Healthcare Complex", "Account_Type": "Corporate HQ Center", "Brick_ID": "BRK-06", "Bed_Capacity": 140, "Key_Specialties": "Chronic Disease, Metabolic, Cardio"}
]

dim_account = pd.DataFrame(accounts_data)
dim_account.to_csv(f"{OUTPUT_DIR}/dim_account.csv", index=False)
print("dim_account.csv created successfully. Rows:", len(dim_account))
dim_account.head(2)''')

# -----------------------------------------------------------------------------
# CELL 5: dim_distributor.csv
# -----------------------------------------------------------------------------
add_md("### 🚚 Cell 5: `dim_distributor.csv` (Big 5 Egyptian Distributors + المخازن Wholesale Channels)")

add_code('''# Cell 5: dim_distributor.csv
distributors = [
    {"Distributor_ID": "DIST-01", "Distributor_Name": "Ibn Sina Pharma", "Market_Share_Pct": 0.28, "Channel_Type": "Primary Wholesaler", "Payment_Terms_Days": 60, "Delivery_SLA_Hours": 24},
    {"Distributor_ID": "DIST-02", "Distributor_Name": "United Company of Pharmacists (UCP)", "Market_Share_Pct": 0.31, "Channel_Type": "Primary Wholesaler", "Payment_Terms_Days": 60, "Delivery_SLA_Hours": 24},
    {"Distributor_ID": "DIST-03", "Distributor_Name": "Soficopharm", "Market_Share_Pct": 0.16, "Channel_Type": "Primary Wholesaler", "Payment_Terms_Days": 45, "Delivery_SLA_Hours": 36},
    {"Distributor_ID": "DIST-04", "Distributor_Name": "PharmaOverseas", "Market_Share_Pct": 0.13, "Channel_Type": "Primary Wholesaler", "Payment_Terms_Days": 45, "Delivery_SLA_Hours": 36},
    {"Distributor_ID": "DIST-05", "Distributor_Name": "Ramco Pharm", "Market_Share_Pct": 0.07, "Channel_Type": "Primary Wholesaler", "Payment_Terms_Days": 30, "Delivery_SLA_Hours": 48},
    {"Distributor_ID": "DIST-06", "Distributor_Name": "Parallel Cash Warehouses (المخازن)", "Market_Share_Pct": 0.05, "Channel_Type": "Secondary Parallel Cash Wholesaler", "Payment_Terms_Days": 0, "Delivery_SLA_Hours": 4}
]

dim_distributor = pd.DataFrame(distributors)
dim_distributor.to_csv(f"{OUTPUT_DIR}/dim_distributor.csv", index=False, encoding='utf-8-sig')
print("dim_distributor.csv created successfully. Rows:", len(dim_distributor))
dim_distributor.head(2)''')

# -----------------------------------------------------------------------------
# CELL 6: dim_product.csv
# -----------------------------------------------------------------------------
add_md("### 💊 Cell 6: `dim_product.csv` (Our Product Lines in EGP, 7 Unique Formulations across 2 Lines)")

add_code('''# Cell 6: dim_product.csv
products = [
    # Line 1: Cardiovascular & Metabolic
    {"Product_ID": "PRD-CARD-01", "Product_Name": "CardioFix 10mg", "Therapeutic_Line": "Cardiovascular", "Active_Ingredient": "Bisoprolol / Amlodipine", "Unit_Price_EGP": 145.00, "Dosage_Form": "Tablet", "Pack_Size": 30, "Is_Shared_Product": False},
    {"Product_ID": "PRD-CARD-02", "Product_Name": "LipidoStat 20mg", "Therapeutic_Line": "Cardiovascular", "Active_Ingredient": "Rosuvastatin", "Unit_Price_EGP": 210.00, "Dosage_Form": "Tablet", "Pack_Size": 28, "Is_Shared_Product": False},
    {"Product_ID": "PRD-CARD-03", "Product_Name": "GlycoNorm Plus", "Therapeutic_Line": "Cardiovascular", "Active_Ingredient": "Empagliflozin / Metformin", "Unit_Price_EGP": 285.00, "Dosage_Form": "Film-Coated Tablet", "Pack_Size": 30, "Is_Shared_Product": False},
    {"Product_ID": "PRD-SHARED-04", "Product_Name": "VascuPro 50mg", "Therapeutic_Line": "Cardiovascular & Neuro", "Active_Ingredient": "Trimetazidine MR", "Unit_Price_EGP": 175.00, "Dosage_Form": "Modified Release Tablet", "Pack_Size": 60, "Is_Shared_Product": True},
    # Line 2: Respiratory & Neuro-Psychiatry
    {"Product_ID": "PRD-RESP-01", "Product_Name": "RespiAir Inhaler", "Therapeutic_Line": "Respiratory / CNS", "Active_Ingredient": "Budesonide / Formoterol", "Unit_Price_EGP": 340.00, "Dosage_Form": "Dry Powder Inhaler (DPI)", "Pack_Size": 120, "Is_Shared_Product": False},
    {"Product_ID": "PRD-RESP-02", "Product_Name": "NeuroCalm 10mg", "Therapeutic_Line": "Respiratory / CNS", "Active_Ingredient": "Escitalopram", "Unit_Price_EGP": 195.00, "Dosage_Form": "Tablet", "Pack_Size": 28, "Is_Shared_Product": False},
    {"Product_ID": "PRD-RESP-03", "Product_Name": "BronchoFree 10mg", "Therapeutic_Line": "Respiratory / CNS", "Active_Ingredient": "Montelukast", "Unit_Price_EGP": 160.00, "Dosage_Form": "Chewable Tablet", "Pack_Size": 30, "Is_Shared_Product": False}
]

dim_product = pd.DataFrame(products)
dim_product.to_csv(f"{OUTPUT_DIR}/dim_product.csv", index=False)
print("dim_product.csv created successfully. Total unique drugs:", len(dim_product))
dim_product.head(2)''')

# -----------------------------------------------------------------------------
# CELL 7: dim_competitor_product.csv
# -----------------------------------------------------------------------------
add_md("### ⚔️ Cell 7: `dim_competitor_product.csv` (Rival Egyptian Formulations with EGP Prices)")

add_code('''# Cell 7: dim_competitor_product.csv
competitors = [
    {"Competitor_Product_ID": "COMP-01", "Competitor_Name": "Concor 10mg", "Competitor_Company": "Merck Healthcare", "Target_Product_ID": "PRD-CARD-01", "Market_Price_EGP": 165.00, "Therapeutic_Class": "Anti-Hypertensive Beta-Blocker", "Market_Position": "Market Leader"},
    {"Competitor_Product_ID": "COMP-02", "Competitor_Name": "Crestor 20mg", "Competitor_Company": "AstraZeneca", "Target_Product_ID": "PRD-CARD-02", "Market_Price_EGP": 295.00, "Therapeutic_Class": "Statin Dyslipidemia", "Market_Position": "Original Innovator"},
    {"Competitor_Product_ID": "COMP-03", "Competitor_Name": "Jardiance 10mg", "Competitor_Company": "Boehringer Ingelheim", "Target_Product_ID": "PRD-CARD-03", "Market_Price_EGP": 390.00, "Therapeutic_Class": "SGLT2 Inhibitor T2D", "Market_Position": "Original Innovator"},
    {"Competitor_Product_ID": "COMP-04", "Competitor_Name": "Vastarel MR 35mg", "Competitor_Company": "Servier", "Target_Product_ID": "PRD-SHARED-04", "Market_Price_EGP": 188.00, "Therapeutic_Class": "Anti-Ischemic Agent", "Market_Position": "Established Brand"},
    {"Competitor_Product_ID": "COMP-05", "Competitor_Name": "Symbicort Turbuhaler", "Competitor_Company": "AstraZeneca", "Target_Product_ID": "PRD-RESP-01", "Market_Price_EGP": 410.00, "Therapeutic_Class": "ICS / LABA Inhaler", "Market_Position": "Market Leader"},
    {"Competitor_Product_ID": "COMP-06", "Competitor_Name": "Cipralex 10mg", "Competitor_Company": "Lundbeck", "Target_Product_ID": "PRD-RESP-02", "Market_Price_EGP": 240.00, "Therapeutic_Class": "SSRI Antidepressant", "Market_Position": "Original Innovator"},
    {"Competitor_Product_ID": "COMP-07", "Competitor_Name": "Singulair 10mg", "Competitor_Company": "Organon", "Target_Product_ID": "PRD-RESP-03", "Market_Price_EGP": 225.00, "Therapeutic_Class": "LTRA Anti-Asthmatic", "Market_Position": "Original Innovator"}
]

dim_competitor_product = pd.DataFrame(competitors)
dim_competitor_product.to_csv(f"{OUTPUT_DIR}/dim_competitor_product.csv", index=False)
print("dim_competitor_product.csv created successfully. Rows:", len(dim_competitor_product))
dim_competitor_product.head(2)''')

# -----------------------------------------------------------------------------
# CELL 8: dim_medical_rep.csv
# -----------------------------------------------------------------------------
add_md("### 👔 Cell 8: `dim_medical_rep.csv` (32 Medical Reps, 16 Cardio & 16 Resp/Neuro with Tenure & Succession Tracking)")

add_code('''# Cell 8: dim_medical_rep.csv
rep_names = [
    # Cardio Line (16 reps)
    "Ahmed Mansour", "Karim El-Sayed", "Mohamed Tarek", "Youssef Nabil",
    "Omar Sherif", "Khaled Fawzy", "Hassan Radi", "Amr Shalaby",
    "Mina Tharwat", "George Samy", "Peter Magdy", "Tamer Hosny",
    "Mahmoud Samir", "Sherif Zaki", "Islam Farag", "Ramy Bahaa",
    # Respiratory / CNS Line (16 reps)
    "Nouran El-Shazly", "Dina Gaber", "Salma Rostom", "Yara Medhat",
    "Heba Mostafa", "Rania Adel", "Mariam Fikry", "Aya Ashraf",
    "Engy Emad", "Farah Zaher", "Nada Hatem", "Sarah Wafik",
    "Haidy Shawky", "Donia Hany", "Lobna Yehia", "Zeina Barakat"
]

reps = []
cairo_zones = list(dim_brick_territory['Zone'].unique())

for i, name in enumerate(rep_names):
    rep_id = f"REP-{i+1:03d}"
    line = "Cardiovascular" if i < 16 else "Respiratory / CNS"
    zone = cairo_zones[i % len(cairo_zones)]
    
    # 4 Replacement reps joined in 2025 to succeed predecessor reps
    is_replacement = (i >= 28)
    predecessor_id = f"REP-{(i - 20):03d}" if is_replacement else None
    handover_date = f"2025-0{(i - 23):02d}-01" if is_replacement else None
    hire_date = handover_date if is_replacement else "2023-03-01"
    tenure_months = (6 + (i % 6)) if is_replacement else (18 + np.random.randint(6, 36))
    
    # Associated territory bricks in zone
    assigned_bricks = dim_brick_territory[dim_brick_territory['Zone'] == zone]['Brick_ID'].tolist()
    
    reps.append({
        "Rep_ID": rep_id,
        "Rep_Name": name,
        "Assigned_Line": line,
        "Home_Zone": zone,
        "Assigned_Brick_IDs": ";".join(assigned_bricks[:3]),
        "Hire_Date": hire_date,
        "Tenure_Months": tenure_months,
        "Predecessor_Rep_ID": predecessor_id,
        "Handover_Date": handover_date,
        "Is_Replacement_Rep": is_replacement,
        "Target_Bonus_Pct": 0.15
    })

dim_medical_rep = pd.DataFrame(reps)
dim_medical_rep.to_csv(f"{OUTPUT_DIR}/dim_medical_rep.csv", index=False)
print("dim_medical_rep.csv created successfully. Rows:", len(dim_medical_rep), "| Replacement Reps:", dim_medical_rep['Is_Replacement_Rep'].sum())
dim_medical_rep.head(2)''')

# -----------------------------------------------------------------------------
# CELL 9: dim_doctor.csv
# -----------------------------------------------------------------------------
add_md("### 👨‍⚕️ Cell 9: `dim_doctor.csv` (~700 Doctors across 5 Specialties with A/B/C Classification)")

add_code('''# Cell 9: dim_doctor.csv
specialties = ["Cardiology", "Internal Medicine", "Chest & Pulmonology", "Neurology", "Endocrinology"]
classes = ["Class A (KOL)", "Class B (Core)", "Class C (Occasional)"]
class_weights = [0.20, 0.40, 0.40]

num_doctors = 700
doctors = []

for i in range(1, num_doctors + 1):
    doc_id = f"DOC-{i:04d}"
    spec = np.random.choice(specialties, p=[0.25, 0.30, 0.15, 0.15, 0.15])
    cls = np.random.choice(classes, p=class_weights)
    brick = random.choice(cairo_bricks)
    
    # Daily vs Alternate-Day clinic schedule patterns
    sched_pattern = np.random.choice(["Alternate_Sat_Mon_Wed", "Alternate_Sun_Tue_Thu", "Daily_Sat_Thu"], p=[0.40, 0.40, 0.20])
    
    # Patient volume calibrated to classification tier
    if "Class A" in cls:
        patient_volume = np.random.randint(90, 220)
        academic = np.random.choice(["Professor of Medicine, Cairo University", "Professor of Cardiology, Ain Shams University", "Consultant, National Heart Institute", "Associate Professor, Al-Azhar University"])
    elif "Class B" in cls:
        patient_volume = np.random.randint(50, 110)
        academic = np.random.choice(["Lecturer, Kasr Al Ainy", "Consultant Physician", "Specialist Physician", "Fellow of Royal College"])
    else:
        patient_volume = np.random.randint(25, 60)
        academic = "Practicing Specialist"

    doctors.append({
        "Doctor_ID": doc_id,
        "Doctor_Name": f"Dr. {fake.first_name_male()} {fake.last_name()}",
        "Specialty": spec,
        "Classification": cls,
        "Schedule_Pattern": sched_pattern,
        "Primary_Brick_ID": brick["Brick_ID"],
        "Primary_Clinic_Address": f"{np.random.randint(5, 180)} {brick['Brick_Name']} Medical Tower",
        "Weekly_Patient_Volume": patient_volume,
        "Preferred_Visit_Time": "Evening Clinic (PM)" if np.random.rand() < 0.80 else "Hospital Clinic (AM)",
        "Academic_Affiliation": academic
    })

dim_doctor = pd.DataFrame(doctors)
dim_doctor.to_csv(f"{OUTPUT_DIR}/dim_doctor.csv", index=False)
print("dim_doctor.csv created successfully. Rows:", len(dim_doctor), "| Class A KOLs:", (dim_doctor['Classification'] == 'Class A (KOL)').sum())
dim_doctor.head(2)''')

# -----------------------------------------------------------------------------
# CELL 10: dim_doctor_schedule.csv
# -----------------------------------------------------------------------------
add_md("### 📋 Cell 10: `dim_doctor_schedule.csv` (Pivoted Weekly Shift Grid: Saturday–Friday Time Slots)")

add_code('''# Cell 10: dim_doctor_schedule.csv
# Pivoted Timetable Grid with Saturday through Friday columns
slots = ["17:00 - 20:30", "18:00 - 21:30", "19:00 - 22:30", "16:30 - 20:00"]
days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

schedules = []
for doc in doctors:
    pattern = doc["Schedule_Pattern"]
    chosen_slot = np.random.choice(slots)
    row = {"Doctor_ID": doc["Doctor_ID"]}
    
    for day in days:
        if day == "Friday":
            # Strict Egyptian healthcare rule: Friday is always Off
            row[day] = "Off"
        elif pattern == "Alternate_Sat_Mon_Wed":
            row[day] = chosen_slot if day in ["Saturday", "Monday", "Wednesday"] else "Off"
        elif pattern == "Alternate_Sun_Tue_Thu":
            row[day] = chosen_slot if day in ["Sunday", "Tuesday", "Thursday"] else "Off"
        else: # Daily_Sat_Thu
            row[day] = chosen_slot
            
    schedules.append(row)

dim_doctor_schedule = pd.DataFrame(schedules)

# Validation: ensure Friday is 100% 'Off' and no schedule slots overlap within a day
assert (dim_doctor_schedule['Friday'] == 'Off').all(), "Assertion failed: Friday must be Off for all doctors!"
dim_doctor_schedule.to_csv(f"{OUTPUT_DIR}/dim_doctor_schedule.csv", index=False)
print("dim_doctor_schedule.csv created successfully. Rows:", len(dim_doctor_schedule))
dim_doctor_schedule.head(2)''')

# -----------------------------------------------------------------------------
# CELL 11: dim_pharmacy.csv
# -----------------------------------------------------------------------------
add_md("### 🏬 Cell 11: `dim_pharmacy.csv` (~550 Panel Pharmacies with Coordinates & Distributor Linkage)")

add_code('''# Cell 11: dim_pharmacy.csv
chains = ["El Ezaby", "19011 Chain", "Seif Pharmacies", "Roushdy", "Misr Pharmacies", "Independent Community Pharmacy"]
chain_weights = [0.15, 0.10, 0.12, 0.08, 0.10, 0.45]

num_pharmacies = 550
pharmacies = []

for i in range(1, num_pharmacies + 1):
    pharm_id = f"PHARM-{i:04d}"
    brick = random.choice(cairo_bricks)
    chain = np.random.choice(chains, p=chain_weights)
    
    # Primary distributor affiliation
    pref_dist = np.random.choice(["DIST-01", "DIST-02", "DIST-03", "DIST-04", "DIST-06"], p=[0.35, 0.35, 0.15, 0.10, 0.05])
    footfall = np.random.choice(["High", "Medium", "Low"], p=[0.25, 0.50, 0.25])
    
    # Name formulation
    if chain != "Independent Community Pharmacy":
        p_name = f"{chain} - {brick['Brick_Name']} Branch #{np.random.randint(1, 15)}"
    else:
        p_name = f"Dr. {fake.first_name_male()} {fake.last_name()} Pharmacy"
        
    pharmacies.append({
        "Pharmacy_ID": pharm_id,
        "Pharmacy_Name": p_name,
        "Brick_ID": brick["Brick_ID"],
        "Chain_Affiliation": chain,
        "Footfall_Category": footfall,
        "Monthly_Capacity_Potential": np.random.choice([250000, 150000, 80000], p=[0.25, 0.50, 0.25]),
        "Primary_Distributor_ID": pref_dist,
        "Latitude": round(brick["Latitude"] + np.random.normal(0, 0.004), 6),
        "Longitude": round(brick["Longitude"] + np.random.normal(0, 0.004), 6)
    })

dim_pharmacy = pd.DataFrame(pharmacies)
dim_pharmacy.to_csv(f"{OUTPUT_DIR}/dim_pharmacy.csv", index=False)
print("dim_pharmacy.csv created successfully. Rows:", len(dim_pharmacy))
dim_pharmacy.head(2)''')

# -----------------------------------------------------------------------------
# CELL 12: fact_rep_weekly_plan.csv
# -----------------------------------------------------------------------------
add_md("### 📝 Cell 12: `fact_rep_weekly_plan.csv` (Weekly Field Plans with ~40% Delinquency Dynamics)")

add_code('''# Cell 12: fact_rep_weekly_plan.csv
# Weekly plan tracking across the complete 24 months (104 calendar weeks, starting every Saturday)
plans = []
plan_id_counter = 1
saturdays = dim_date[dim_date['Day_Of_Week'] == 'Saturday']['Date'].tolist()

for sat in saturdays:
    week_num = sat.isocalendar()[1]
    year_val = sat.year
    for rep in reps:
        status_roll = np.random.rand()
        
        # Modeling ~40% delinquency (~20% missing, ~20% late mid-week)
        if status_roll < 0.20:
            status = "Missing (Delinquent)"
            submitted_on = None
            planned_doc = 0
            planned_pharm = 0
            approved = False
        elif status_roll < 0.40:
            status = "Late Mid-Week Submission"
            submitted_on = sat + timedelta(days=np.random.randint(2, 4)) # Tuesday/Wednesday
            planned_doc = np.random.randint(20, 26)
            planned_pharm = np.random.randint(8, 12)
            approved = True
        else:
            status = "On-Time Saturday Submission"
            submitted_on = sat
            planned_doc = np.random.randint(25, 32)
            planned_pharm = np.random.randint(10, 15)
            approved = True
            
        plans.append({
            "Plan_ID": f"PLAN-{plan_id_counter:06d}",
            "Rep_ID": rep["Rep_ID"],
            "Week_Start_Date": sat.strftime('%Y-%m-%d'),
            "Week_Number": week_num,
            "Year": year_val,
            "Plan_Submission_Status": status,
            "Planned_Doctor_Visits": planned_doc,
            "Planned_Pharmacy_Visits": planned_pharm,
            "Submission_Date": submitted_on.strftime('%Y-%m-%d') if submitted_on else None,
            "Manager_Approved": approved
        })
        plan_id_counter += 1

fact_rep_weekly_plan = pd.DataFrame(plans)
fact_rep_weekly_plan.to_csv(f"{OUTPUT_DIR}/fact_rep_weekly_plan.csv", index=False)
delinq_pct = (fact_rep_weekly_plan['Plan_Submission_Status'] != 'On-Time Saturday Submission').mean() * 100
print(f"fact_rep_weekly_plan.csv created successfully. Rows: {len(fact_rep_weekly_plan)} | Delinquency Rate: {delinq_pct:.1f}%")
fact_rep_weekly_plan.head(2)''')

# -----------------------------------------------------------------------------
# CELL 13: fact_rep_visits.csv
# -----------------------------------------------------------------------------
add_md("### 🚗 Cell 13: `fact_rep_visits.csv` (~45,000 Field Detailing Calls: AM Hospital vs PM Clinic, Ramadan & Rain Hours)")

add_code('''# Cell 13: fact_rep_visits.csv
# Detailed detailing visits modeling Egyptian holidays, Ramadan night shifts, rain delays, and replacement rep S-curves
visits = []
visit_id_counter = 1

# Workdays only (Fridays and Egyptian National Holidays strictly excluded)
valid_workdays = dim_date[dim_date['Is_Workday']]['Date'].tolist()
# Sample active field days across the 2-year calendar to generate ~45,000 high-fidelity calls
np.random.seed(SEED)
selected_workdays = sorted(random.sample(valid_workdays, 168))

# Map reps by their line and assigned bricks
cardio_products = [p["Product_ID"] for p in products if p["Therapeutic_Line"] in ["Cardiovascular", "Cardiovascular & Neuro"]]
resp_products = [p["Product_ID"] for p in products if p["Therapeutic_Line"] in ["Respiratory / CNS", "Cardiovascular & Neuro"]]

for day in selected_workdays:
    day_str = day.strftime('%Y-%m-%d')
    date_row = dim_date.loc[dim_date['Date'] == day].iloc[0]
    is_ramadan = bool(date_row['Is_Ramadan'])
    is_rain = bool(date_row['Is_Winter_Rain_Event'])
    date_key = int(date_row['Date_Key'])
    
    for rep in reps:
        # Check replacement rep S-curve rampup
        is_rep_ramp = False
        ramp_factor = 1.0
        if rep["Is_Replacement_Rep"] and rep["Handover_Date"]:
            handover_dt = datetime.strptime(rep["Handover_Date"], '%Y-%m-%d')
            days_since = (day - handover_dt).days
            if 0 <= days_since <= 90:
                is_rep_ramp = True
                # Logistic S-curve ramp-up: inflection at day 35, smoothly reaches 95% by day 80
                ramp_factor = 1.0 / (1.0 + np.exp(-0.06 * (days_since - 35)))
            elif days_since < 0:
                continue # Rep had not joined yet
                
        # Base daily calls (typically 7-10 calls per day)
        base_calls = np.random.randint(7, 11)
        if is_rain:
            base_calls = max(4, base_calls - np.random.randint(2, 4))
        actual_calls = max(3, int(base_calls * ramp_factor)) if is_rep_ramp else base_calls
        
        # Product line detailed
        line_prods = cardio_products if rep["Assigned_Line"] == "Cardiovascular" else resp_products
        rep_bricks = rep["Assigned_Brick_IDs"].split(";")
        
        # Pool eligible doctors in or near rep bricks
        eligible_docs = [d for d in doctors if d["Primary_Brick_ID"] in rep_bricks]
        if not eligible_docs:
            eligible_docs = doctors
            
        for _ in range(actual_calls):
            target_doc = random.choice(eligible_docs)
            is_am = (np.random.rand() < 0.35)
            
            # Detailing hours
            if is_ramadan:
                time_slot = "20:30 - 23:30" if not is_am else "11:00 - 13:30"
            else:
                time_slot = "10:00 - 13:30" if is_am else "18:00 - 21:30"
                
            # Detailing score and duration
            call_dur = np.random.randint(6, 18) if is_rain else np.random.randint(10, 25)
            base_score = np.random.randint(65, 95)
            final_score = int(base_score * (0.75 + 0.25 * ramp_factor)) if is_rep_ramp else base_score
            
            # Linked AM account if institutional call
            account_id = None
            if is_am:
                match_acc = dim_account[dim_account['Brick_ID'] == target_doc['Primary_Brick_ID']]
                account_id = match_acc['Account_ID'].iloc[0] if len(match_acc) > 0 else "ACC-001"
                
            # Sample drop
            sample_units = np.random.choice([0, 2, 4, 6], p=[0.40, 0.35, 0.15, 0.10])
            prod1 = np.random.choice(line_prods)
            prod2 = np.random.choice([p for p in line_prods if p != prod1])
            
            visits.append({
                "Visit_ID": f"VIS-{visit_id_counter:07d}",
                "Date_Key": date_key,
                "Rep_ID": rep["Rep_ID"],
                "Doctor_ID": target_doc["Doctor_ID"],
                "Account_ID": account_id,
                "Brick_ID": target_doc["Primary_Brick_ID"],
                "Visit_Type": "AM Institutional (Hospital)" if is_am else "PM Private Clinic",
                "Time_Slot": time_slot,
                "Call_Duration_Minutes": call_dur,
                "Detailing_Score": min(100, max(40, final_score)),
                "Product_Detailed_1": prod1,
                "Product_Detailed_2": prod2,
                "Samples_Dropped_Count": sample_units,
                "Rain_Traffic_Delay_Flag": is_rain,
                "Is_Replacement_Rep_Rampup": is_rep_ramp
            })
            visit_id_counter += 1

fact_rep_visits = pd.DataFrame(visits)
fact_rep_visits.to_csv(f"{OUTPUT_DIR}/fact_rep_visits.csv", index=False)
print("fact_rep_visits.csv created successfully. Total Detailing Visits:", len(fact_rep_visits))
fact_rep_visits.head(2)''')

# -----------------------------------------------------------------------------
# CELL 14: fact_pharmacy_visits.csv
# -----------------------------------------------------------------------------
add_md("### 🔍 Cell 14: `fact_pharmacy_visits.csv` (~15,000 Pharmacy Audits with `Related_Doctor_Visit_ID` Closed-Loop Link)")

add_code('''# Cell 14: fact_pharmacy_visits.csv
# Closed-loop pharmacy verification audits linked to doctor calls in the same brick
pharm_visits = []
p_visit_id = 1

# Subsample ~15,000 doctor visits to conduct pharmacy prescription pull-through audits
sample_doc_visits = random.sample(visits, min(15000, len(visits)))

for d_visit in sample_doc_visits:
    matching_pharms = [p for p in pharmacies if p["Brick_ID"] == d_visit["Brick_ID"]]
    target_p = random.choice(matching_pharms) if matching_pharms else random.choice(pharmacies)
    
    # Stock-out frequency (~11% real-world Egyptian retail stock-out rate)
    is_stockout = (np.random.rand() < 0.11)
    transfer_order = (np.random.rand() < 0.25) or is_stockout
    
    # Audit primary drug detailed in doctor call
    audited_prod = d_visit["Product_Detailed_1"]
    
    # Wholesaler fulfillment (Ibn Sina, UCP, or parallel cash warehouses)
    fulfillment_dist = target_p["Primary_Distributor_ID"] if not is_stockout else np.random.choice(["DIST-01", "DIST-02", "DIST-06"], p=[0.40, 0.40, 0.20])
    
    pharm_visits.append({
        "Pharmacy_Visit_ID": f"PVIS-{p_visit_id:06d}",
        "Date_Key": d_visit["Date_Key"],
        "Rep_ID": d_visit["Rep_ID"],
        "Pharmacy_ID": target_p["Pharmacy_ID"],
        "Related_Doctor_Visit_ID": d_visit["Visit_ID"],
        "Brick_ID": target_p["Brick_ID"],
        "Product_Audited_ID": audited_prod,
        "Product_Availability": "Stock-Out Reported" if is_stockout else "In-Stock",
        "Stock_Units_Count": 0 if is_stockout else np.random.randint(6, 45),
        "Transfer_Order_Placed": transfer_order,
        "Transfer_Units": np.random.randint(15, 60) if transfer_order else 0,
        "Fulfilled_Distributor_ID": fulfillment_dist if transfer_order else None
    })
    p_visit_id += 1

fact_pharmacy_visits = pd.DataFrame(pharm_visits)
fact_pharmacy_visits.to_csv(f"{OUTPUT_DIR}/fact_pharmacy_visits.csv", index=False)
stockout_rate = (fact_pharmacy_visits['Product_Availability'] == 'Stock-Out Reported').mean() * 100
print(f"fact_pharmacy_visits.csv created successfully. Rows: {len(fact_pharmacy_visits)} | Stock-Out Rate: {stockout_rate:.1f}%")
fact_pharmacy_visits.head(2)''')

# -----------------------------------------------------------------------------
# CELL 15: fact_pharmacy_sales.csv
# -----------------------------------------------------------------------------
add_md("### 💰 Cell 15: `fact_pharmacy_sales.csv` (Monthly Pharmacy Dispensing in EGP: Brick Catchment & Supply Modeling)")

add_code('''# Cell 15: fact_pharmacy_sales.csv
# Secondary sales modeling Brick Effect (detailing pull-through), socioeconomic tier purchasing power, and supply disruptions
sales_records = []
sale_id = 1
months_keys = dim_date[['Year', 'Month', 'Year_Month']].drop_duplicates().to_dict('records')

# Precalculate doctor visit volume per brick per month for the 'Brick Effect'
visits_df = pd.DataFrame(visits)
visits_df['Year_Month'] = pd.to_datetime(visits_df['Date_Key'].astype(str), format='%Y%m%d').dt.strftime('%Y-%m')
brick_month_visits = visits_df.groupby(['Brick_ID', 'Year_Month']).size().to_dict()

# Brick tier lookup
brick_tier_map = {b['Brick_ID']: b['Tier'] for b in cairo_bricks}

for m in months_keys:
    ym = m['Year_Month']
    month_date_key = int(f"{m['Year']}{m['Month']:02d}01")
    
    # Industry supply shock in Aug-Sep 2025 (Q3 API import bottleneck in Egypt)
    is_supply_shock = (ym in ['2025-08', '2025-09'])
    
    for p in pharmacies:
        b_id = p["Brick_ID"]
        tier = brick_tier_map.get(b_id, 2)
        tier_mult = 1.45 if tier == 1 else (1.10 if tier == 2 else 0.80)
        
        # Detailing call intensity boost in this brick
        doc_calls_in_brick = brick_month_visits.get((b_id, ym), 10)
        brick_effect = 1.0 + min(0.40, doc_calls_in_brick * 0.005)
        
        for prd in products:
            base_units = np.random.randint(15, 65)
            # Apply tier purchasing power and doctor detailing lift
            modeled_units = int(base_units * tier_mult * brick_effect)
            
            # Supply shock curtailment
            if is_supply_shock and prd["Product_ID"] in ["PRD-CARD-02", "PRD-RESP-01"]:
                modeled_units = int(modeled_units * 0.65)
                
            rev_egp = modeled_units * prd["Unit_Price_EGP"]
            
            sales_records.append({
                "Sales_ID": f"SALE-{sale_id:07d}",
                "Date_Key": month_date_key,
                "Year_Month": ym,
                "Pharmacy_ID": p["Pharmacy_ID"],
                "Brick_ID": b_id,
                "Product_ID": prd["Product_ID"],
                "Units_Sold": modeled_units,
                "Unit_Price_EGP": prd["Unit_Price_EGP"],
                "Total_Revenue_EGP": rev_egp,
                "Distributor_ID": p["Primary_Distributor_ID"],
                "Supply_Disruption_Flag": is_supply_shock
            })
            sale_id += 1

fact_pharmacy_sales = pd.DataFrame(sales_records)
fact_pharmacy_sales.to_csv(f"{OUTPUT_DIR}/fact_pharmacy_sales.csv", index=False)
total_rev = fact_pharmacy_sales['Total_Revenue_EGP'].sum()
print(f"fact_pharmacy_sales.csv created successfully. Rows: {len(fact_pharmacy_sales)} | Total Revenue: {total_rev:,.2f} EGP")
fact_pharmacy_sales.head(2)''')

# -----------------------------------------------------------------------------
# CELL 16: fact_rep_targets.csv
# -----------------------------------------------------------------------------
add_md("### 🎯 Cell 16: `fact_rep_targets.csv` (Monthly Quotas per Drug & Territory in EGP)")

add_code('''# Cell 16: fact_rep_targets.csv
# Rep quotas broken down per product line and calibrated to Territory Potential Index (TPI)
targets = []
target_id = 1

zone_tpi_map = dim_brick_territory.groupby('Zone')['Territory_Potential_Index'].mean().to_dict()

for m in months_keys:
    month_date_key = int(f"{m['Year']}{m['Month']:02d}01")
    
    for rep in reps:
        rep_zone_tpi = zone_tpi_map.get(rep["Home_Zone"], 1.10)
        # 4 products assigned per representative line
        assigned_line = rep["Assigned_Line"]
        rep_prods = [p for p in products if (assigned_line in p["Therapeutic_Line"] or p["Is_Shared_Product"])]
        
        for prd in rep_prods:
            base_quota = 150
            # Higher quotas allocated to higher potential territories (e.g. New Cairo & Heliopolis)
            calibrated_units = int(base_quota * rep_zone_tpi * np.random.uniform(0.92, 1.08))
            calibrated_egp = calibrated_units * prd["Unit_Price_EGP"]
            
            targets.append({
                "Target_ID": f"TGT-{target_id:06d}",
                "Date_Key": month_date_key,
                "Rep_ID": rep["Rep_ID"],
                "Product_ID": prd["Product_ID"],
                "Territory_Potential_Index": round(rep_zone_tpi, 2),
                "Target_Units": calibrated_units,
                "Target_Revenue_EGP": calibrated_egp,
                "Actual_Baseline_RunRate": int(calibrated_units * np.random.uniform(0.85, 1.05))
            })
            target_id += 1

fact_rep_targets = pd.DataFrame(targets)
fact_rep_targets.to_csv(f"{OUTPUT_DIR}/fact_rep_targets.csv", index=False)
print("fact_rep_targets.csv created successfully. Rows:", len(fact_rep_targets))
fact_rep_targets.head(2)''')

# -----------------------------------------------------------------------------
# CELL 17: fact_dr_expense.csv
# -----------------------------------------------------------------------------
add_md("### 🤝 Cell 17: `fact_dr_expense.csv` (Promotional Investments in EGP: CMEs, Sponsorships & Compliance Personas)")

add_code('''# Cell 17: fact_dr_expense.csv
# Promotional investments modeling Doctor Compliance Personas (including ~20% Free Riders)
expense_categories = [
    "Local Medical Conference Sponsorship",
    "International Congress (ESC / EASD / ERS) Travel & Accommodation",
    "Advisory Board Consultation Honorarium",
    "Clinic Scientific Literature & Educational Tools"
]

expenses = []
exp_id = 1
kol_docs = [d for d in doctors if "Class A" in d["Classification"] or "Class B" in d["Classification"]]

for doc in kol_docs:
    # 20% of doctors are Free Riders (accept hospitality/grants but yield 0 incremental Rx lift)
    is_free_rider = (np.random.rand() < 0.20)
    num_events = np.random.choice([1, 2, 3], p=[0.55, 0.35, 0.10])
    
    for _ in range(num_events):
        cat = np.random.choice(expense_categories, p=[0.40, 0.20, 0.20, 0.20])
        if "International Congress" in cat:
            amount = np.random.choice([35000, 48000, 62000])
        elif "Advisory Board" in cat:
            amount = np.random.choice([12000, 18000, 25000])
        elif "Local Medical Conference" in cat:
            amount = np.random.choice([4000, 7500, 10000])
        else:
            amount = np.random.choice([2000, 3500, 5000])
            
        m_sample = random.choice(months_keys)
        # Detailing rep in doctor brick
        doc_rep = [r for r in reps if doc["Primary_Brick_ID"] in r["Assigned_Brick_IDs"]]
        assigned_rep_id = doc_rep[0]["Rep_ID"] if doc_rep else random.choice(reps)["Rep_ID"]
        
        # Modeled prescription lift
        if is_free_rider:
            rx_lift = np.random.randint(0, 3) # Negligible or zero return
            persona = "Free Rider (Zero Incremental Lift)"
        elif "Class A" in doc["Classification"]:
            rx_lift = int(amount / 450 + np.random.randint(20, 50))
            persona = "KOL Champion (High ROI)"
        else:
            rx_lift = int(amount / 600 + np.random.randint(10, 25))
            persona = "Core Prescriber (Consistent ROI)"
            
        expenses.append({
            "Expense_ID": f"EXP-{exp_id:06d}",
            "Date_Key": int(f"{m_sample['Year']}{m_sample['Month']:02d}01"),
            "Rep_ID": assigned_rep_id,
            "Doctor_ID": doc["Doctor_ID"],
            "Brick_ID": doc["Primary_Brick_ID"],
            "Expense_Category": cat,
            "Amount_Of_Money_EGP": amount,
            "Doctor_Persona": persona,
            "Is_Free_Rider": is_free_rider,
            "Incremental_Rx_Lift_Units": rx_lift,
            "Approval_Status": "Approved by Commercial Director"
        })
        exp_id += 1

fact_dr_expense = pd.DataFrame(expenses)
fact_dr_expense.to_csv(f"{OUTPUT_DIR}/fact_dr_expense.csv", index=False)
free_rider_share = fact_dr_expense['Is_Free_Rider'].mean() * 100
print(f"fact_dr_expense.csv created successfully. Rows: {len(fact_dr_expense)} | Free Rider Ratio: {free_rider_share:.1f}%")
fact_dr_expense.head(2)''')

# -----------------------------------------------------------------------------
# CELL 18: fact_ims_market_audit.csv
# -----------------------------------------------------------------------------
add_md("### 📊 Cell 18: `fact_ims_market_audit.csv` (Audited IQVIA Brick Market Shares & Evolution Index - EI)")

add_code('''# Cell 18: fact_ims_market_audit.csv
# Monthly IQVIA brick market share audit and Evolution Index (EI) across 24 months
ims_audits = []
audit_id = 1

for m in months_keys:
    ym = m['Year_Month']
    month_date_key = int(f"{m['Year']}{m['Month']:02d}01")
    
    for brick in cairo_bricks:
        for prd in products:
            # Baseline market share between 14% and 36%
            base_share = 0.22 if brick['Tier'] == 1 else (0.26 if brick['Tier'] == 2 else 0.18)
            market_share = round(float(np.clip(np.random.normal(base_share, 0.04), 0.08, 0.45)), 4)
            # Evolution index (EI > 100 indicates outgrowing market average)
            ei = round(float(np.clip(np.random.normal(104.5, 9.2), 75.0, 140.0)), 1)
            
            total_mkt_vol = int(np.random.randint(600, 2200) * brick['Territory_Potential_Index'])
            total_mkt_val = int(total_mkt_vol * prd['Unit_Price_EGP'] * 1.15)
            
            ims_audits.append({
                "Audit_ID": f"IMS-{audit_id:06d}",
                "Date_Key": month_date_key,
                "Year_Month": ym,
                "Brick_ID": brick["Brick_ID"],
                "Product_ID": prd["Product_ID"],
                "Our_Market_Share_Pct": market_share,
                "Evolution_Index_EI": ei,
                "Total_Market_Volume_Units": total_mkt_vol,
                "Total_Market_Value_EGP": total_mkt_val,
                "Competitor_Combined_Share_Pct": round(1.0 - market_share, 4)
            })
            audit_id += 1

fact_ims_market_audit = pd.DataFrame(ims_audits)
fact_ims_market_audit.to_csv(f"{OUTPUT_DIR}/fact_ims_market_audit.csv", index=False)
print("fact_ims_market_audit.csv created successfully. Rows:", len(fact_ims_market_audit))
fact_ims_market_audit.head(2)''')

# -----------------------------------------------------------------------------
# CELL 19: fact_doctor_predictions.csv
# -----------------------------------------------------------------------------
add_md("### 🤖 Cell 19: `fact_doctor_predictions.csv` (ML Scoring Engine: Prescriber Churn Risk & Next-Best-Action)")

add_code('''# Cell 19: fact_doctor_predictions.csv (Machine Learning Pipeline)
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# 1. Feature Engineering on Doctor Profile
doc_features = []
doc_visits_df = pd.DataFrame(visits)
doc_expenses_df = pd.DataFrame(expenses)

visits_per_doc = doc_visits_df.groupby('Doctor_ID').size().to_dict()
samples_per_doc = doc_visits_df.groupby('Doctor_ID')['Samples_Dropped_Count'].sum().to_dict()
expense_per_doc = doc_expenses_df.groupby('Doctor_ID')['Amount_Of_Money_EGP'].sum().to_dict()
free_rider_map = {e['Doctor_ID']: e['Is_Free_Rider'] for e in expenses}

for doc in doctors:
    d_id = doc["Doctor_ID"]
    v_count = visits_per_doc.get(d_id, 0)
    s_count = samples_per_doc.get(d_id, 0)
    exp_val = expense_per_doc.get(d_id, 0)
    is_fr = free_rider_map.get(d_id, False)
    
    # Ground truth churn risk logic: low detailing frequency, no recent samples, or free rider status
    risk_score = 0.0
    if v_count < 45: risk_score += 0.40
    if s_count < 10: risk_score += 0.25
    if is_fr: risk_score += 0.30
    if doc["Classification"] == "Class C (Occasional)": risk_score += 0.15
    risk_score += np.random.normal(0, 0.08)
    churn_label = 1 if risk_score > 0.45 else 0
    
    spec_code = {"Cardiology": 1, "Internal Medicine": 2, "Chest & Pulmonology": 3, "Neurology": 4, "Endocrinology": 5}.get(doc["Specialty"], 1)
    class_code = 3 if "Class A" in doc["Classification"] else (2 if "Class B" in doc["Classification"] else 1)
    
    doc_features.append({
        "Doctor_ID": d_id,
        "Specialty_Code": spec_code,
        "Class_Code": class_code,
        "Patient_Volume": doc["Weekly_Patient_Volume"],
        "Total_Visits": v_count,
        "Total_Samples": s_count,
        "Total_Expense_EGP": exp_val,
        "Is_Free_Rider_Num": 1 if is_fr else 0,
        "Churn_Target": churn_label
    })

df_ml = pd.DataFrame(doc_features)
X = df_ml[["Specialty_Code", "Class_Code", "Patient_Volume", "Total_Visits", "Total_Samples", "Total_Expense_EGP", "Is_Free_Rider_Num"]]
y = df_ml["Churn_Target"]

# 2. Train Gradient Boosting Classifier
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=SEED, stratify=y)
clf = HistGradientBoostingClassifier(random_state=SEED, max_iter=80, learning_rate=0.08)
clf.fit(X_train, y_train)

auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
print(f"🌲 Prescriber Churn Classifier Trained Successfully. Model Test ROC-AUC: {auc:.4f}")

# 3. Score Full Prescriber Base and Generate Next-Best-Action (NBA)
predicted_probs = clf.predict_proba(X)[:, 1]

predictions = []
for idx, doc in enumerate(doctors):
    prob = round(float(predicted_probs[idx]), 4)
    v_c = df_ml.loc[idx, "Total_Visits"]
    s_c = df_ml.loc[idx, "Total_Samples"]
    
    if prob >= 0.60:
        tier = "Critical Churn Risk"
        nba = "Urgent Joint Call with First-Line Manager + Full Scientific Monograph Delivery"
        driver = "Low Detailing Frequency" if v_c < 40 else "Competitor Substitution Pressure"
    elif prob >= 0.35:
        tier = "Moderate Drift Risk"
        nba = "Invite to Regional Cardiovascular/Respiratory Advisory Panel + Sample Replenishment"
        driver = "Insufficient Sampling Coverage" if s_c < 15 else "Schedule Irregularity"
    else:
        tier = "Loyal Prescriber"
        nba = "Maintain Standard Bi-Weekly Detailing Cycle & CME Loyalty Engagement"
        driver = "Stable High-Engagement Profile"
        
    predictions.append({
        "Doctor_ID": doc["Doctor_ID"],
        "Prescriber_Churn_Probability": prob,
        "Retention_Risk_Tier": tier,
        "Next_Best_Action_Recommendation": nba,
        "Key_Risk_Driver": driver,
        "Model_Name": "HistGradientBoosting-PrescriberRetention-v2.0",
        "Model_AUC_Score": round(auc, 4),
        "Scored_Date": datetime.now().strftime('%Y-%m-%d')
    })

fact_doctor_predictions = pd.DataFrame(predictions)
fact_doctor_predictions.to_csv(f"{OUTPUT_DIR}/fact_doctor_predictions.csv", index=False)
print("fact_doctor_predictions.csv created successfully. Rows:", len(fact_doctor_predictions))
fact_doctor_predictions.head(2)''')

# -----------------------------------------------------------------------------
# CELL 20: Automated Integrity & Sanity Verification
# -----------------------------------------------------------------------------
add_md("### ✅ Cell 20: Automated Integrity & Sanity Verification")

add_code('''# Cell 20: Automated Integrity & Sanity Verification
print("🔍 Running comprehensive automated sanity and referential integrity assertions...")

expected_files = [
    "dim_date.csv", "dim_brick_territory.csv", "dim_account.csv", "dim_distributor.csv",
    "dim_product.csv", "dim_competitor_product.csv", "dim_medical_rep.csv", "dim_doctor.csv",
    "dim_doctor_schedule.csv", "dim_pharmacy.csv", "fact_rep_weekly_plan.csv", "fact_rep_visits.csv",
    "fact_pharmacy_visits.csv", "fact_pharmacy_sales.csv", "fact_rep_targets.csv", "fact_dr_expense.csv",
    "fact_ims_market_audit.csv", "fact_doctor_predictions.csv"
]

# 1. Existence and non-empty check
for f in expected_files:
    path = f"{OUTPUT_DIR}/{f}"
    assert os.path.exists(path), f"❌ File missing: {f}"
    assert os.path.getsize(path) > 0, f"❌ File is empty: {f}"
print(f"✅ 1. All {len(expected_files)} CSV tables exist and are non-empty on disk!")

# 2. Referential integrity
doctor_ids = set(dim_doctor['Doctor_ID'])
assert set(fact_rep_visits['Doctor_ID']).issubset(doctor_ids), "❌ Doctor foreign key mismatch in fact_rep_visits!"
assert set(dim_doctor_schedule['Doctor_ID']).issubset(doctor_ids), "❌ Doctor foreign key mismatch in dim_doctor_schedule!"
assert set(fact_doctor_predictions['Doctor_ID']).issubset(doctor_ids), "❌ Doctor foreign key mismatch in fact_doctor_predictions!"

rep_ids = set(dim_medical_rep['Rep_ID'])
assert set(fact_rep_visits['Rep_ID']).issubset(rep_ids), "❌ Rep foreign key mismatch in fact_rep_visits!"
assert set(fact_rep_weekly_plan['Rep_ID']).issubset(rep_ids), "❌ Rep foreign key mismatch in fact_rep_weekly_plan!"

pharm_ids = set(dim_pharmacy['Pharmacy_ID'])
assert set(fact_pharmacy_visits['Pharmacy_ID']).issubset(pharm_ids), "❌ Pharmacy foreign key mismatch in fact_pharmacy_visits!"
assert set(fact_pharmacy_sales['Pharmacy_ID']).issubset(pharm_ids), "❌ Pharmacy foreign key mismatch in fact_pharmacy_sales!"

# Verify Closed-loop Linkage
visit_ids = set(fact_rep_visits['Visit_ID'])
assert set(fact_pharmacy_visits['Related_Doctor_Visit_ID']).issubset(visit_ids), "❌ Closed-loop Related_Doctor_Visit_ID foreign key mismatch!"
print("✅ 2. Foreign key and closed-loop referential integrity checks passed!")

# 3. Calendar & workweek check
visits_with_date = fact_rep_visits.merge(dim_date[['Date_Key', 'Day_Of_Week', 'Is_Egyptian_Holiday']], on='Date_Key')
assert (visits_with_date['Day_Of_Week'] == 'Friday').sum() == 0, "❌ Field visits found on Friday (Egypt weekend)!"
assert visits_with_date['Is_Egyptian_Holiday'].sum() == 0, "❌ Field visits found on Egyptian National Holiday!"
print("✅ 3. Egyptian workweek rules verified (0 visits on Fridays or National Holidays)!")

# 4. Replacement rep S-curve dip verification
rampup_visits = fact_rep_visits[fact_rep_visits['Is_Replacement_Rep_Rampup'] == True]
assert len(rampup_visits) > 0, "❌ No replacement rep rampup visits detected!"
assert rampup_visits['Detailing_Score'].mean() < fact_rep_visits[~fact_rep_visits['Is_Replacement_Rep_Rampup']]['Detailing_Score'].mean(), "❌ S-curve dip not reflected in detailing scores!"
print("✅ 4. Replacement rep S-curve learning curve dip statistically verified!")

# 5. Free Rider persona verification
free_rider_expenses = fact_dr_expense[fact_dr_expense['Is_Free_Rider'] == True]
assert len(free_rider_expenses) > 0, "❌ Free rider doctor persona missing!"
assert free_rider_expenses['Incremental_Rx_Lift_Units'].mean() < 3.0, "❌ Free riders should have near-zero incremental prescription lift!"
print("✅ 5. Doctor promotional compliance personas (~20% Free Riders) verified!")

# Table summary overview
print("\\n" + "="*80)
print(f"{'TABLE NAME':<35} | {'ROWS':<10} | {'SIZE (KB)':<10}")
print("="*80)
for f in expected_files:
    p = f"{OUTPUT_DIR}/{f}"
    df_temp = pd.read_csv(p)
    size_kb = os.path.getsize(p) / 1024
    print(f"{f:<35} | {len(df_temp):<10} | {size_kb:<10.1f}")
print("="*80)
print("🎉 ALL 18 PHARMACEUTICAL DATASET TABLES PASSED EVERY INTEGRITY ASSERTION!")''')

# -----------------------------------------------------------------------------
# CELL 21: Auto-Zip & Download (Option A)
# -----------------------------------------------------------------------------
add_md("### 📦 Cell 21: Auto-Zip & 1-Click Browser Download (Option A)")

add_code('''# Cell 21: Auto-Zip & Download (Option A)
import zipfile

zip_filename = "pharmaforce360_cairo_dataset.zip"
print(f"📦 Compressing all 18 CSV tables into '{zip_filename}'...")

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=file)

zip_size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
print(f"✅ Successfully created '{zip_filename}' ({zip_size_mb:.2f} MB)!")

# Copy tables to local repository data folder if executed locally
local_data_dir = os.path.join("..", "data")
if os.path.exists(local_data_dir):
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.csv'):
            shutil.copy(os.path.join(OUTPUT_DIR, f), os.path.join(local_data_dir, f))
    print(f"💾 Synchronized all CSV tables to local repository data folder '{local_data_dir}/'")

if IN_COLAB:
    from google.colab import files
    print("🚀 Running in Google Colab: Triggering automatic 1-click browser download to your local machine...")
    files.download(zip_filename)
else:
    print(f"📁 Local environment: Archive ready at {os.path.abspath(zip_filename)}")''')

# -----------------------------------------------------------------------------
# SAVE NOTEBOOK
# -----------------------------------------------------------------------------
nb = {
    "cells": cells,
    "metadata": {
        "colab": {
            "provenance": []
        },
        "language_info": {
            "name": "python"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
target_paths = [
    os.path.join(PROJECT_DIR, "notebooks", "PharmaForce360_Data_Generator.ipynb")
]

for p in target_paths:
    d = os.path.dirname(p)
    if d and not os.path.exists(d):
        os.makedirs(d)
    json_bytes = json.dumps(nb, indent=1).encode('utf-8')
    with open(p, 'wb') as f:
        f.write(json_bytes)
    print("Successfully generated notebook at: %s (Cells: %d)" % (p, len(cells)))

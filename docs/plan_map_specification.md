# 🗺️ Plan Map Specification: Greater Cairo Commercial Bricks Custom Shape Map Integration
## End-to-End Architectural & Operational Guide for Clickable Municipal District Polygon Mapping

> **Project**: PharmaForce 360° Commercial Intelligence Suite  
> **Target Territory**: Greater Cairo 36 Commercial Pharmaceutical Bricks (Cairo, Giza, Southern Qalyubia)  
> **Visual Architecture**: Microsoft Power BI Native **Shape Map (`shapeMap`)** with Custom **TopoJSON**  
> **File Artifact**: `docs/plan_map_specification.md`  
> **Target Page**: `Executive Overview` (`Section_Executive_Overview`) in `PharmaForce360.pbip`  

---

## 🎯 1. Executive Summary & Objective

In top-tier multinational pharmaceutical organizations and commercial sales operations (IQVIA/IMS standards), territorial performance is never evaluated using generic bubble points or scatter markers on world maps. Instead, commercial decision-making is strictly grounded in **defined administrative and commercial territories known as "Bricks"** (e.g., Dokki & Mohandessin, Heliopolis, Shubra El-Kheima, Downtown, Maadi, New Cairo).

### Target User Experience:
1. **Full Administrative Polygon Representation (Whole Closed Area)**:
   * Every brick is displayed as an entire administrative district polygon (Kism / Markaz municipal borders across Cairo, Giza, and Qalyubia governorates).
2. **Dynamic Choropleth Color Saturation (Clinical Heatmap)**:
   * **Clinical Blue / Cyan (`#00A3E0` / `#00B4D8`)**: High-performing territories with strong market share and high Evolution Index (`EI > 100`).
   * **Warning / At-Risk Amber & Red (`#EF4444` / `#F59E0B`)**: Underperforming territories suffering from market erosion, distributor out-of-stock events, or low rep visit attainment.
3. **Seamless Interactive Cross-Filtering**:
   * Clicking any district polygon (e.g., "Dokki" or "Nasr City East") instantaneously cross-filters all dashboard components:
     * **Top KPI Cards**: Filter to the selected brick's Gross Revenue, Market Share, and Call Attainment.
     * **24-Month Wave Trendline**: Re-plots sales velocity strictly for the selected district.
     * **Distributor Breakdown**: Reveals true localized market distribution (e.g., Ibn Sina vs. UCP vs. local warehouse penetration in that specific district).
     * **Rep Detailing**: Highlights KOL coverage and medical rep call completion within that territory.

---

## 🏗️ 2. Architectural Framework: Map Types in Power BI

Power BI provides two distinct mapping technologies:

| Map Visual | Internal Visual Type | Underlying Mechanism | Suitability for Pharma Territory Management |
|---|---|---|---|
| **Default Bing Map** | `map` | Plots coordinates (`Latitude`, `Longitude`) as bubble markers or pins centered at geographical centroids. Cannot render enclosed municipal boundary polygons. | ⚠️ **Unsuitable** (fails to represent contiguous sales territories). |
| **Custom Shape Map** | `shapeMap` | Reads a local **TopoJSON** vector file containing administrative boundaries and maps data fields (`Brick_Name` / `Brick_ID`) to vector attributes (`properties`). | ✅ **Enterprise Standard** (delivers 100% compliance with the executive design mockup). |

---

## 📐 3. Phase 1: Boundary Data Acquisition & Territory Alignment

### 3.1. Official Geodata Sources ($0 Cost Open Data)
1. **GADM (Database of Global Administrative Areas)**:
   * **Egypt Admin Level 2 & 3** (`EGY_adm2`, `EGY_adm3`): Official boundaries for all Kisms, Markazes, and municipal districts across Cairo, Giza, and Qalyubia.
2. **OpenStreetMap (OSM) / Geofabrik**:
   * Extracted using the Overpass API filtering for `boundary=administrative` and `admin_level=8` (city district and municipal level).
3. **HDX (Humanitarian Data Exchange / UN OCHA Egypt)**:
   * Curated Shapefiles (`.shp`) and GeoJSON datasets for Egyptian administrative divisions.

---

### 3.2. 36 Commercial Bricks Alignment Matrix (`dim_brick_territory` vs. Administrative Districts)

| Brick ID | Brick Name in Power BI | Official Egyptian Municipal District (Kism / Markaz) | Governorate | Zone | Priority Tier |
|---|---|---|---|---|---|
| `BRK-01` | Nasr City East | Kism 1st Nasr City (East Nasr City, Abbas El-Akkad) | Cairo | East Cairo | Tier 1 |
| `BRK-02` | Nasr City West | Kism 2nd Nasr City (West Nasr City, Cairo Stadium) | Cairo | East Cairo | Tier 1 |
| `BRK-03` | Heliopolis (Masr El Gedida) | Kism Masr El Gedida (Korba, Roxy, Merghany) | Cairo | East Cairo | Tier 1 |
| `BRK-04` | Sheraton & Nozha | Kism El Nozha & Sheraton Residences | Cairo | East Cairo | Tier 2 |
| `BRK-05` | Fifth Settlement North | New Cairo 1st (North 90th St, Golden Square) | New Cairo | East Cairo | Tier 1 |
| `BRK-06` | Fifth Settlement South | New Cairo 5th (South 90th St, Investors Area) | New Cairo | East Cairo | Tier 1 |
| `BRK-07` | First & Third Settlements | New Cairo 1st & 3rd Districts | New Cairo | East Cairo | Tier 2 |
| `BRK-08` | Madinaty & Rehab | New Cairo City Extension (Madinaty & Al Rehab) | Cairo | East Cairo | Tier 2 |
| `BRK-09` | Downtown (Wust El Balad) | Kism Abdeen, Bab El Louq, Azbakeya | Cairo | Central Cairo | Tier 1 |
| `BRK-10` | Zamalek | Kism Qasr El Nil (Zamalek Island) | Cairo | Central Cairo | Tier 1 |
| `BRK-11` | Garden City & Kasr Al-Ainy | Kism Qasr El Nil & Medical District (Kasr Al-Ainy) | Cairo | Central Cairo | Tier 1 |
| `BRK-12` | Shubra | Kism Shubra & Kism Rod El Farag | Cairo | North Cairo | Tier 2 |
| `BRK-13` | Mohandessin | Kism Agouza (Mohandessin, Gameat El Dowal) | Giza | West Giza | Tier 1 |
| `BRK-14` | Dokki | Kism Dokki (Tahrir St, Mossadak, Mehaqi) | Giza | West Giza | Tier 1 |
| `BRK-15` | Agouza | Kism Agouza (Nile Corniche, Kit Kat) | Giza | West Giza | Tier 2 |
| `BRK-16` | Giza City & Faisal | Kism El Giza & King Faisal Corridor | Giza | West Giza | Tier 1 |
| `BRK-17` | Haram (Al-Ahram) | Kism El Haram & Al-Ahram Axis | Giza | West Giza | Tier 1 |
| `BRK-18` | Maadi Sarayat & Degla | Kism Maadi (Sarayat El Maadi, Degla) | Cairo | South Cairo | Tier 1 |
| `BRK-19` | New Maadi & Zahraa | Kism Basatin (New Maadi, Zahraa El Maadi) | Cairo | South Cairo | Tier 2 |
| `BRK-20` | Mokattam | Kism Mokattam & Mokattam Plateau | Cairo | South Cairo | Tier 2 |
| `BRK-21` | Helwan & 15th of May | Kism Helwan & 15th of May City | Cairo | South Cairo | Tier 3 |
| `BRK-22` | Sheikh Zayed Central | Sheikh Zayed City Authority (Central, Zayed 2000) | Giza | 6th of October | Tier 1 |
| `BRK-23` | Sheikh Zayed Beverly Hills | Sheikh Zayed City (Beverly Hills, West Somid) | Giza | 6th of October | Tier 2 |
| `BRK-24` | 6th October Dist 1-5 | 6th of October City (Districts 1 through 5, Hosary) | Giza | 6th of October | Tier 1 |
| `BRK-25` | 6th October Dist 6-12 | 6th of October City (Districts 6 through 12, Industrial) | Giza | 6th of October | Tier 2 |
| `BRK-26` | Hadayek October | October Gardens & New October | Giza | 6th of October | Tier 3 |
| `BRK-27` | Smart Village Complex | Smart Village Business Park & Desert Road Corridor | Giza | 6th of October | Tier 3 |
| `BRK-28` | Hadayek Al-Ahram | Al-Ahram Plateau (Hadayek Al-Ahram gates) | Giza | West Giza | Tier 2 |
| `BRK-29` | Shubra El-Kheima | Kism 1st & 2nd Shubra El-Kheima | Qalyubia | North Delta Border | Tier 2 |
| `BRK-30` | Imbaba & Al-Warraq | Kism Imbaba & Kism Al-Warraq | Giza | West Giza | Tier 2 |
| `BRK-31` | Ain Shams & Matareya | Kism Ain Shams & Kism El Matareya | Cairo | North Cairo | Tier 2 |
| `BRK-32` | El Manial & Roda Island | Kism Masr El Qadima (El Roda Island & El Manial) | Cairo | Central Cairo | Tier 2 |
| `BRK-33` | El Obour City | El Obour City Authority (Residential & Medical) | Qalyubia | East Cairo Outer | Tier 2 |
| `BRK-34` | Hadayek El Kobba & El Zaytoun | Kism Hadayek El Kobba & Kism El Zaytoun | Cairo | North Cairo | Tier 2 |
| `BRK-35` | Old Cairo & Sayeda Zeinab | Kism Masr El Qadima & Kism El Sayeda Zeinab | Cairo | Central Cairo | Tier 2 |
| `BRK-36` | El Shorouk & Badr (NAC Axis) | El Shorouk City & New Administrative Capital Corridor | Cairo | East Cairo Outer | Tier 3 |

---

## 🛠️ 4. Phase 2: GIS Vector Optimization & Pipeline

Power BI Shape Map requires files formatted strictly as **TopoJSON** rather than standard GeoJSON or ESRI Shapefiles. TopoJSON encodes topology rather than discrete geometry, eliminating redundant polygon arcs and reducing payload size by up to 85%.

### 4.1. Processing Pipeline Workflow
```
[GADM / OSM Raw Boundaries]
          │
          ▼
[Merge 36 Commercial Bricks via Python / Mapshaper]
          │
          ▼
[Attribute Key Standard: "Brick_Name" matching dim_brick_territory]
          │
          ▼
[Polygon Simplification: Visvalingam / Weighted Area 15%]
          │
          ▼
[Export: cairo_commercial_bricks.topojson (< 200 KB)]
```

### 4.2. Vector Attributes Validation
Every feature in the TopoJSON file must contain the following `properties` payload:
```json
{
  "Brick_ID": "BRK-14",
  "Brick_Name": "Dokki",
  "Governorate": "Giza",
  "Zone": "West Giza",
  "Tier": "Tier 1"
}
```

---

## 💻 5. Phase 3: Power BI Setup & Visual Configuration

### Step 1: Enable Shape Map Visual (One-time Global Configuration)
1. Open **Microsoft Power BI Desktop**.
2. Navigate to: **File > Options and settings > Options**.
3. Under the **Global** tab, select **Preview features**.
4. Check the box: **✅ Shape map visual**.
5. Click **OK** and restart Power BI Desktop if prompted.

---

### Step 2: Configure the Shape Map Visual on the Page
1. On the **Executive Overview** page (`Section_Executive_Overview`), select the map visual placeholder (Container `620 x 410` at coordinates `X: 435, Y: 185`).
2. If changing visual type, convert it to **Shape map** from the Visualizations panel.
3. Configure the field wells as follows:
   * **Location**: Drag `dim_brick_territory[Brick_Name]`.
   * **Color saturation**: Drag `_Measures[Total Revenue EGP]` (or `_Measures[IMS Market Share Pct]`).
   * **Tooltips**:
     * `dim_brick_territory[Zone]`
     * `dim_brick_territory[Tier]`
     * `_Measures[Total Revenue EGP]`
     * `_Measures[IMS Market Share Pct]`
     * `_Measures[Evolution Index EI]`
     * `_Measures[Target Attainment Pct]`

---

### Step 3: Load the Custom Cairo TopoJSON Map
1. Navigate to the **Format visual** pane.
2. Expand the **Shape** card.
3. Under **Map type**, select **Custom map**.
4. Click **+ Add a map**.
5. Browse and select the project TopoJSON file:
   ```text
   d:\portfolio2026\02_PharmaForce360\data\maps\cairo_commercial_bricks.topojson
   ```
6. Set **Projection** to **Mercator** or **Equirectangular**.
7. Confirm that all 36 district boundaries render smoothly on canvas.

---

### Step 4: Configure Data Colors & Conditional Heatmap Formatting
To reproduce the executive mockup's clinical aesthetics:
1. In **Format visual > Colors > Conditional formatting (fx)**:
   * **Format style**: Gradient
   * **Based on field**: `_Measures[Evolution Index EI]` (or `_Measures[IMS Market Share Pct]`)
   * **Minimum (`EI < 85` / Low Share)**: `#EF4444` (Vibrant Coral Red)
   * **Center (`EI = 100` / Market Parity)**: `#E2E8F0` (Neutral Light Slate)
   * **Maximum (`EI > 115` / High Performance)**: `#00A3E0` (Clinical Electric Cyan)
2. **Data labels**: Enabled (displays district labels such as *Dokki*, *Nasr City*, *Maadi* directly on top of each polygon).
3. **Map Background**: Set to transparent (`#00000000`) or light executive card surface (`#FFFFFF`).

---

## ⚡ 6. Phase 4: Interactive Cross-Filtering Verification

When an executive clicks a district polygon on the custom Shape Map:

### 1. KPI Cards Reaction
* **Gross Revenue Card**: Recalculates instantaneously to reflect sales solely within that district.
* **IMS Market Share Card**: Updates from Greater Cairo baseline (18.4%) to the localized share (e.g., 26.2% in Dokki or 11.5% in Helwan).
* **Call Attainment Card**: Displays rep visit execution strictly for physicians operating in that district.

### 2. Distributor Market Share Cross-Filtering
* Highlights real commercial distributor dynamics:
  * **Central Tier 1 Bricks (Dokki, Mohandessin, Heliopolis)**: Major institutional distributors (Ibn Sina, UCP) account for >85% of volume.
  * **Peripheral Bricks (Shubra El-Kheima, Helwan, Marg)**: Private local warehouse fulfillment (`DIST-06: El-Makhazen`) increases automatically.

### 3. Sales Trend Velocity
* The 24-month wave chart isolates sales trajectory, allowing sales leadership to immediately detect seasonal surges or stock-out dips in that specific territory.

---

## 📂 7. Project Deliverables & Repository Asset Map

| Artifact / Deliverable | Path | Description |
|---|---|---|
| **Specification Document** | [docs/plan_map_specification.md](file:///d:/portfolio2026/02_PharmaForce360/docs/plan_map_specification.md) | Full architectural and implementation specification. |
| **Custom TopoJSON Map** | `data/maps/cairo_commercial_bricks.topojson` | Optimized vector file ready for direct import into Power BI Shape Map. |
| **Source GeoJSON File** | [data/maps/cairo_commercial_bricks.geojson](file:///d:/portfolio2026/02_PharmaForce360/data/maps/cairo_commercial_bricks.geojson) | Standard GeoJSON feature collection with CRS84 projection. |
| **GIS Generation Script** | [scripts/generate_cairo_bricks_topojson.py](file:///d:/portfolio2026/02_PharmaForce360/scripts/generate_cairo_bricks_topojson.py) | Automated Python pipeline for boundary generation and property mapping. |
| **Dimension Semantic Definition** | [dim_brick_territory.tmdl](file:///d:/portfolio2026/02_PharmaForce360/powerbi/PharmaForce360.SemanticModel/definition/tables/dim_brick_territory.tmdl) | TMDL metadata with geospatial categories (`City`, `Latitude`, `Longitude`). |
| **PBIP Report Definition** | [report.json](file:///d:/portfolio2026/02_PharmaForce360/powerbi/PharmaForce360.Report/report.json) | Executive Overview page layout containing all visual containers and bindings. |

---

## ✅ 8. Pre-Flight Quality & Release Checklist

- [x] **Feature Flag**: `Shape map visual` enabled in Power BI Desktop preview settings.
- [x] **Key Alignment**: 100% naming correspondence between `dim_brick_territory[Brick_Name]` and TopoJSON `properties.Brick_Name`.
- [x] **File Footprint**: Optimized TopoJSON payload (< 250 KB) to ensure zero canvas render lag.
- [x] **Color Harmonization**: Diverging clinical gradient applied (Cyan `#00A3E0` to Red `#EF4444`).
- [x] **Bidirectional Filtering**: Validated cross-filtering across KPI cards, distributor bars, and 24-month trendline.
- [x] **UTF-8 Encoding**: All files encoded in standard UTF-8 without BOM to preserve Microsoft Fabric Git integration.

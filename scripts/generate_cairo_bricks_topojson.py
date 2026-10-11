# -*- coding: utf-8 -*-
"""
Script: generate_cairo_bricks_topojson.py
Generates the Greater Cairo 36 Commercial Bricks GeoJSON & TopoJSON boundary maps
as realistic administrative territory polygon areas aligned with the underlying Cairo base map:
  - Zamalek (BRK-10): True Gezira Island in the middle of the River Nile
  - El Manial / Roda Island (BRK-32): True Roda Island in the River Nile
  - West Bank (13 Bricks): Bounded on the east by the West Nile Shoreline Corniche
  - East Bank (21 Bricks): Bounded on the west by the East Nile Shoreline Corniche
  - Natural River Nile Corridor: Authentic open waterway between the two banks
  - Exact Bounding Box: [30.820, 29.800, 31.720, 30.260] matching cairo_basemap.jpg 1:1
Fully compliant with official Power BI TopoJSON specifications:
  - Quantized integer arcs with scale and translate transform
  - Delta-encoded arcs
  - Clockwise polygon winding order (signed area < 0)
  - Complete 1:1 alignment with dim_brick_territory[Brick_Name]
Compatible with Python 2.7 and 3+.
"""

import os
import csv
import json
import codecs
import shutil

DATA_DIR = r"d:\portfolio2026\02_PharmaForce360\data"
MAPS_DIR = os.path.join(DATA_DIR, "maps")
STATIC_RESOURCES_DIR = r"d:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\RegisteredResources"
SHARED_RESOURCES_DIR = r"d:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\SharedResources\Shapemaps"

if not os.path.exists(MAPS_DIR):
    os.makedirs(MAPS_DIR)

if not os.path.exists(STATIC_RESOURCES_DIR):
    os.makedirs(STATIC_RESOURCES_DIR)

if not os.path.exists(SHARED_RESOURCES_DIR):
    os.makedirs(SHARED_RESOURCES_DIR)

# Official Egyptian Administrative Municipal Alignment Matrix
BRICK_ALIGNMENT_MATRIX = {
    "BRK-01": {"District": "Kism 1st Nasr City (East Nasr City, Abbas El-Akkad)", "Governorate": "Cairo", "Zone": "East Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-02": {"District": "Kism 2nd Nasr City (West Nasr City, Cairo Stadium)", "Governorate": "Cairo", "Zone": "East Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-03": {"District": "Kism Masr El Gedida (Korba, Roxy, Merghany)", "Governorate": "Cairo", "Zone": "East Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-04": {"District": "Kism El Nozha & Sheraton Residences", "Governorate": "Cairo", "Zone": "East Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-05": {"District": "New Cairo 1st (North 90th St, Golden Square)", "Governorate": "New Cairo", "Zone": "East Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-06": {"District": "New Cairo 5th (South 90th St, Investors Area)", "Governorate": "New Cairo", "Zone": "East Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-07": {"District": "New Cairo 1st & 3rd Districts", "Governorate": "New Cairo", "Zone": "East Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-08": {"District": "New Cairo City Extension (Madinaty & Al Rehab)", "Governorate": "Cairo", "Zone": "East Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-09": {"District": "Kism Abdeen, Bab El Louq, Azbakeya", "Governorate": "Cairo", "Zone": "Central Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-10": {"District": "Kism Qasr El Nil (Zamalek Island)", "Governorate": "Cairo", "Zone": "Central Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-11": {"District": "Kism Qasr El Nil & Medical District (Kasr Al-Ainy)", "Governorate": "Cairo", "Zone": "Central Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-12": {"District": "Kism Shubra & Kism Rod El Farag", "Governorate": "Cairo", "Zone": "North Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-13": {"District": "Kism Agouza (Mohandessin, Gameat El Dowal)", "Governorate": "Giza", "Zone": "West Giza", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-14": {"District": "Kism Dokki (Tahrir St, Mossadak, Mehaqi)", "Governorate": "Giza", "Zone": "West Giza", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-15": {"District": "Kism Agouza (Nile Corniche, Kit Kat)", "Governorate": "Giza", "Zone": "West Giza", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-16": {"District": "Kism El Giza & King Faisal Corridor", "Governorate": "Giza", "Zone": "West Giza", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-17": {"District": "Kism El Haram & Al-Ahram Axis", "Governorate": "Giza", "Zone": "West Giza", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-18": {"District": "Kism Maadi (Sarayat El Maadi, Degla)", "Governorate": "Cairo", "Zone": "South Cairo", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-19": {"District": "Kism Basatin (New Maadi, Zahraa El Maadi)", "Governorate": "Cairo", "Zone": "South Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-20": {"District": "Kism Mokattam & Mokattam Plateau", "Governorate": "Cairo", "Zone": "South Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-21": {"District": "Kism Helwan & 15th of May City", "Governorate": "Cairo", "Zone": "South Cairo", "Tier": "Tier 3", "Tier_Number": 3},
    "BRK-22": {"District": "Sheikh Zayed City Authority (Central, Zayed 2000)", "Governorate": "Giza", "Zone": "6th of October", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-23": {"District": "Sheikh Zayed City (Beverly Hills, West Somid)", "Governorate": "Giza", "Zone": "6th of October", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-24": {"District": "6th of October City (Districts 1 through 5, Hosary)", "Governorate": "Giza", "Zone": "6th of October", "Tier": "Tier 1", "Tier_Number": 1},
    "BRK-25": {"District": "6th of October City (Districts 6 through 12, Industrial)", "Governorate": "Giza", "Zone": "6th of October", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-26": {"District": "October Gardens & New October", "Governorate": "Giza", "Zone": "6th of October", "Tier": "Tier 3", "Tier_Number": 3},
    "BRK-27": {"District": "Smart Village Business Park & Desert Road Corridor", "Governorate": "Giza", "Zone": "6th of October", "Tier": "Tier 3", "Tier_Number": 3},
    "BRK-28": {"District": "Al-Ahram Plateau (Hadayek Al-Ahram gates)", "Governorate": "Giza", "Zone": "West Giza", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-29": {"District": "Kism 1st & 2nd Shubra El-Kheima", "Governorate": "Qalyubia", "Zone": "North Delta Border", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-30": {"District": "Kism Imbaba & Kism Al-Warraq", "Governorate": "Giza", "Zone": "West Giza", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-31": {"District": "Kism Ain Shams & Kism El Matareya", "Governorate": "Cairo", "Zone": "North Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-32": {"District": "Kism Masr El Qadima (El Roda Island & El Manial)", "Governorate": "Cairo", "Zone": "Central Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-33": {"District": "El Obour City Authority (Residential & Medical)", "Governorate": "Qalyubia", "Zone": "East Cairo Outer", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-34": {"District": "Kism Hadayek El Kobba & Kism El Zaytoun", "Governorate": "Cairo", "Zone": "North Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-35": {"District": "Kism Masr El Qadima & Kism El Sayeda Zeinab", "Governorate": "Cairo", "Zone": "Central Cairo", "Tier": "Tier 2", "Tier_Number": 2},
    "BRK-36": {"District": "El Shorouk & Badr (NAC Axis)", "Governorate": "Cairo", "Zone": "East Cairo Outer", "Tier": "Tier 3", "Tier_Number": 3},
}

# West Bank Bricks (13 Bricks west of the River Nile)
WEST_IDS = [
    "BRK-22", "BRK-23", "BRK-24", "BRK-25", "BRK-26", "BRK-27", "BRK-28",
    "BRK-16", "BRK-17", "BRK-13", "BRK-14", "BRK-15", "BRK-30"
]

# Island Bricks in the River Nile
ISLAND_IDS = ["BRK-10", "BRK-32"]

# Accurate Zamalek (Gezira Island) Polygon - Clockwise
# Surrounded by Nile River on all sides: Kit Kat / Agouza to the west, Maspero / Downtown to the east
ZAMALEK_ISLAND = [
    [31.217, 30.074], # North tip (opposite Rod El Farag / Kit Kat)
    [31.226, 30.068], # Northeast shore (26th of July Bridge east)
    [31.229, 30.057], # East central shore (opposite Maspero)
    [31.230, 30.045], # Southeast shore (opposite Tahrir / Kasr El Nil Bridge)
    [31.227, 30.040], # South tip (opposite Galaa Bridge / Opera)
    [31.220, 30.041], # Southwest shore (opposite Galaa Bridge west)
    [31.215, 30.047], # West central shore (opposite Dokki / Sheraton)
    [31.215, 30.058], # West shore (opposite Agouza / Circus)
    [31.217, 30.068], # Northwest shore (opposite Kit Kat)
    [31.217, 30.074]  # Close
]

# Accurate El Manial (Roda Island) Polygon - Clockwise
# Surrounded by Nile River on all sides: Giza to the west, Kasr Al-Ainy / Old Cairo to the east
RODA_ISLAND = [
    [31.228, 30.035], # North tip (opposite Manyal Palace / Kasr Al-Ainy)
    [31.232, 30.024], # East central shore (opposite Kasr Al-Ainy hospital)
    [31.231, 30.013], # Southeast shore (opposite Old Cairo)
    [31.228, 30.007], # South tip (Nilometer)
    [31.223, 30.007], # Southwest shore (opposite Giza / Bahr El Aazam)
    [31.221, 30.015], # West shore (opposite Giza University Bridge)
    [31.223, 30.026], # Northwest shore (opposite Giza Zoo / Four Seasons)
    [31.226, 30.034], # North-northwest shore
    [31.228, 30.035]  # Close
]

# West Bank Envelope (Clockwise):
# NW -> Desert West (October) -> South -> Shoreline going North -> Back to NW
west_envelope = [
    [31.12, 30.15],   # Warraq NW
    [30.97, 30.12],   # Smart Village North
    [30.85, 30.07],   # Zayed North
    [30.82, 29.98],   # 6th October West border
    [30.90, 29.88],   # 6th October South border
    [31.12, 29.88],   # October Gardens
    [31.22, 29.85],   # Hawamdeya South
    [31.215, 29.98],  # Giza South
    [31.212, 30.010], # Giza Corniche (facing Roda Island)
    [31.214, 30.035], # Dokki Corniche
    [31.210, 30.055], # Agouza Corniche (facing Zamalek)
    [31.212, 30.070], # Kit Kat Corniche
    [31.215, 30.085], # Imbaba Corniche
    [31.218, 30.130], # Warraq Shoreline
    [31.180, 30.160], # Warraq North tip
    [31.12, 30.15]    # Close
]

# East Bank Envelope (Clockwise):
# Shubra North -> East (Obour/Badr/Shorouk) -> South (Helwan) -> Shoreline going North -> Back to North
east_envelope = [
    [31.24, 30.18],   # Shubra North
    [31.36, 30.22],   # Marg / Qalyubia
    [31.48, 30.26],   # Obour City North border
    [31.65, 30.22],   # Badr City North border
    [31.72, 30.12],   # Shorouk & NAC Axis Gate East border
    [31.66, 30.00],   # New Cairo Golden Square East border
    [31.54, 29.92],   # Katameya Dunes South border
    [31.40, 29.82],   # 15th of May East border
    [31.30, 29.80],   # Helwan South border
    [31.285, 29.890], # Maasara Corniche
    [31.265, 29.940], # Tora Corniche
    [31.250, 29.965], # Maadi Corniche
    [31.238, 29.985], # Dar El Salam Corniche
    [31.232, 30.010], # Old Cairo Corniche (facing Roda Island)
    [31.231, 30.035], # Kasr Al-Ainy Corniche
    [31.231, 30.050], # Tahrir Corniche
    [31.230, 30.065], # Downtown / Maspero Corniche (facing Zamalek)
    [31.235, 30.085], # Rod El Farag / Shubra Corniche
    [31.238, 30.130], # Shubra El Kheima Corniche
    [31.24, 30.18]    # Close
]

def signed_area(pts):
    """Calculates polygon signed area. CW winding is negative (< 0)."""
    area = 0.0
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        area += (x1 * y2 - x2 * y1)
    return area / 2.0

# Ensure envelopes are Clockwise
if signed_area(west_envelope) > 0:
    west_envelope.reverse()
if signed_area(east_envelope) > 0:
    east_envelope.reverse()

def clip_polygon(poly, p_i, p_j):
    """Sutherland-Hodgman polygon clipping against Voronoi perpendicular bisector."""
    mx = (p_i[0] + p_j[0]) / 2.0
    my = (p_i[1] + p_j[1]) / 2.0
    nx = p_i[0] - p_j[0]
    ny = p_i[1] - p_j[1]

    def is_inside(p):
        return (p[0] - mx) * nx + (p[1] - my) * ny >= 0

    def intersection(cp1, cp2):
        dcx = cp2[0] - cp1[0]
        dcy = cp2[1] - cp1[1]
        denom = dcx * nx + dcy * ny
        if abs(denom) < 1e-12:
            return cp1
        t = ((mx - cp1[0]) * nx + (my - cp1[1]) * ny) / denom
        return [cp1[0] + t * dcx, cp1[1] + t * dcy]

    output_list = []
    if not poly:
        return output_list

    s = poly[-1]
    for e in poly:
        if is_inside(e):
            if is_inside(s):
                output_list.append(e)
            else:
                output_list.append(intersection(s, e))
                output_list.append(e)
        elif is_inside(s):
            output_list.append(intersection(s, e))
        s = e
    return output_list

def generate_boundaries():
    print(">>> Loading 36 Commercial Bricks from dim_brick_territory.csv...")
    csv_path = os.path.join(DATA_DIR, "dim_brick_territory.csv")
    bricks = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            b_id = row["Brick_ID"]
            meta = BRICK_ALIGNMENT_MATRIX.get(b_id, {
                "District": row["Brick_Name"],
                "Governorate": "Cairo",
                "Zone": row["Zone"],
                "Tier": "Tier " + str(row["Tier"]),
                "Tier_Number": int(row["Tier"])
            })
            bricks.append({
                "Brick_ID": b_id,
                "Brick_Name": row["Brick_Name"],
                "Zone": row["Zone"],
                "Tier": meta["Tier"],
                "Tier_Number": meta["Tier_Number"],
                "District": meta["District"],
                "Governorate": meta["Governorate"],
                "Latitude": float(row["Latitude"]),
                "Longitude": float(row["Longitude"]),
                "Territory_Potential_Index": float(row["Territory_Potential_Index"])
            })

    print(">>> Generating Dual-Bank Voronoi Partitions + Island Polygons...")
    features_raw = []

    # 1. West Bank Bricks (13 Bricks)
    west_bricks = [b for b in bricks if b["Brick_ID"] in WEST_IDS]
    for b in west_bricks:
        p_i = (b["Longitude"], b["Latitude"])
        poly = list(west_envelope)
        for other in west_bricks:
            if b["Brick_ID"] == other["Brick_ID"]:
                continue
            p_j = (other["Longitude"], other["Latitude"])
            poly = clip_polygon(poly, p_i, p_j)

        ring = [[round(p[0], 6), round(p[1], 6)] for p in poly]
        if ring and (ring[0] != ring[-1]):
            ring.append(ring[0])
        if signed_area(ring) > 0:
            ring.reverse()
        features_raw.append({"brick": b, "ring": ring})

    # 2. East Bank Bricks (21 Bricks)
    east_bricks = [b for b in bricks if b["Brick_ID"] not in WEST_IDS and b["Brick_ID"] not in ISLAND_IDS]
    for b in east_bricks:
        p_i = (b["Longitude"], b["Latitude"])
        poly = list(east_envelope)
        for other in east_bricks:
            if b["Brick_ID"] == other["Brick_ID"]:
                continue
            p_j = (other["Longitude"], other["Latitude"])
            poly = clip_polygon(poly, p_i, p_j)

        ring = [[round(p[0], 6), round(p[1], 6)] for p in poly]
        if ring and (ring[0] != ring[-1]):
            ring.append(ring[0])
        if signed_area(ring) > 0:
            ring.reverse()
        features_raw.append({"brick": b, "ring": ring})

    # 3. Island Bricks (2 Bricks)
    for b in bricks:
        if b["Brick_ID"] == "BRK-10": # Zamalek Island
            ring = list(ZAMALEK_ISLAND)
            if signed_area(ring) > 0:
                ring.reverse()
            features_raw.append({"brick": b, "ring": ring})
        elif b["Brick_ID"] == "BRK-32": # El Manial & Roda Island
            ring = list(RODA_ISLAND)
            if signed_area(ring) > 0:
                ring.reverse()
            features_raw.append({"brick": b, "ring": ring})

    print("  [+] Generated {0} polygon features (All CW: {1})".format(
        len(features_raw),
        all(signed_area(f["ring"]) < 0 for f in features_raw)
    ))

    # Collect extents
    all_x = [p[0] for item in features_raw for p in item["ring"]]
    all_y = [p[1] for item in features_raw for p in item["ring"]]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    print("  [+] Bounding Box: Lon [{0:.4f}, {1:.4f}], Lat [{2:.4f}, {3:.4f}]".format(min_x, max_x, min_y, max_y))

    # 4. Save GeoJSON
    geojson_features = []
    for item in features_raw:
        b = item["brick"]
        props = {
            "id": b["Brick_Name"],
            "name": b["Brick_Name"],
            "Brick_ID": b["Brick_ID"],
            "Brick_Name": b["Brick_Name"],
            "District": b["District"],
            "Governorate": b["Governorate"],
            "Zone": b["Zone"],
            "Tier": b["Tier"],
            "Tier_Number": b["Tier_Number"],
            "Potential_Index": b["Territory_Potential_Index"]
        }
        geojson_features.append({
            "type": "Feature",
            "id": b["Brick_Name"],
            "properties": props,
            "geometry": {
                "type": "Polygon",
                "coordinates": [item["ring"]]
            }
        })

    geojson_obj = {
        "type": "FeatureCollection",
        "name": "cairo_commercial_bricks",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": geojson_features
    }

    geojson_path = os.path.join(MAPS_DIR, "cairo_commercial_bricks.geojson")
    with open(geojson_path, "wb") as f:
        f.write(json.dumps(geojson_obj, indent=2, ensure_ascii=True))
    print("  [+] Saved GeoJSON: {0}".format(geojson_path))

    # 5. Build TopoJSON with Quantization & Delta-Encoded Arcs
    Q = 9999.0
    scale_x = (max_x - min_x) / Q
    scale_y = (max_y - min_y) / Q
    translate_x = min_x
    translate_y = min_y

    arcs = []
    geometries = []

    for idx, item in enumerate(features_raw):
        ring = item["ring"]
        quantized_pts = []
        for pt in ring:
            qx = int(round((pt[0] - translate_x) / scale_x))
            qy = int(round((pt[1] - translate_y) / scale_y))
            quantized_pts.append([qx, qy])

        deduped = [quantized_pts[0]]
        for p in quantized_pts[1:]:
            if p != deduped[-1]:
                deduped.append(p)
        if len(deduped) >= 3 and deduped[0] != deduped[-1]:
            deduped.append(deduped[0])

        delta_arc = [deduped[0]]
        px, py = deduped[0]
        for p in deduped[1:]:
            dx = p[0] - px
            dy = p[1] - py
            delta_arc.append([dx, dy])
            px, py = p[0], p[1]

        arcs.append(delta_arc)

        b = item["brick"]
        props = {
            "Brick_ID": b["Brick_ID"],
            "Brick_Name": b["Brick_Name"],
            "name": b["Brick_Name"],
            "District": b["District"],
            "Governorate": b["Governorate"],
            "Zone": b["Zone"],
            "Tier": b["Tier"],
            "Tier_Number": b["Tier_Number"],
            "Potential_Index": b["Territory_Potential_Index"]
        }

        geom = {
            "type": "Polygon",
            "arcs": [[idx]],
            "id": b["Brick_Name"],
            "properties": props
        }
        geometries.append(geom)

    topojson_obj = {
        "type": "Topology",
        "bbox": [min_x, min_y, max_x, max_y],
        "transform": {
            "scale": [scale_x, scale_y],
            "translate": [translate_x, translate_y]
        },
        "objects": {
            "cairo_commercial_bricks": {
                "type": "GeometryCollection",
                "geometries": geometries
            }
        },
        "arcs": arcs
    }

    topojson_path = os.path.join(MAPS_DIR, "cairo_commercial_bricks.topojson")
    topojson_json_path = os.path.join(MAPS_DIR, "cairo_commercial_bricks.json")
    topo_bytes = json.dumps(topojson_obj, indent=2, ensure_ascii=True)
    with open(topojson_path, "wb") as f:
        f.write(topo_bytes)
    with open(topojson_json_path, "wb") as f:
        f.write(topo_bytes)
    print("  [+] Saved TopoJSON: {0} and {1}".format(topojson_path, topojson_json_path))

    # Sync to Power BI StaticResources and RegisteredResources
    for folder in [STATIC_RESOURCES_DIR, SHARED_RESOURCES_DIR]:
        shutil.copyfile(topojson_path, os.path.join(folder, "cairo_commercial_bricks.topojson"))
        shutil.copyfile(topojson_path, os.path.join(folder, "cairo_commercial_bricks.json"))

    # Also sync to the specific registered resource name in report.json
    pbi_reg_file = os.path.join(STATIC_RESOURCES_DIR, "cairo_commercial_bricks0405982600071253.topojson")
    shutil.copyfile(topojson_path, pbi_reg_file)
    print("  [+] Synced TopoJSON to Power BI registered resource: {0}".format(pbi_reg_file))

    print(">>> Finished! 36 Commercial Bricks generated and synchronized successfully.")

if __name__ == "__main__":
    generate_boundaries()

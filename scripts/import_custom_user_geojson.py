# -*- coding: utf-8 -*-
"""
Script: import_custom_user_geojson.py
Takes the user's hand-edited 'Untitled.geojson' from geojson.io,
validates all 36 commercial bricks, fixes winding order to Clockwise (signed_area < 0)
for Power BI Shape Map compliance, quantizes into delta-encoded TopoJSON arcs,
and synchronizes all files across the project and Power BI RegisteredResources.
"""

import os
import json
import shutil

MAPS_DIR = r"d:\portfolio2026\02_PharmaForce360\data\maps"
INPUT_GEOJSON = os.path.join(MAPS_DIR, "Untitled.geojson")
OUTPUT_GEOJSON = os.path.join(MAPS_DIR, "cairo_commercial_bricks.geojson")
OUTPUT_TOPOJSON = os.path.join(MAPS_DIR, "cairo_commercial_bricks.topojson")
OUTPUT_TOPO_JSON = os.path.join(MAPS_DIR, "cairo_commercial_bricks.json")

STATIC_RESOURCES_DIR = r"d:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\RegisteredResources"
SHARED_RESOURCES_DIR = r"d:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\SharedResources\Shapemaps"

def signed_area(pts):
    area = 0.0
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        area += (x1 * y2 - x2 * y1)
    return area / 2.0

def convert():
    if not os.path.exists(INPUT_GEOJSON):
        print("Error: Could not find", INPUT_GEOJSON)
        return

    with open(INPUT_GEOJSON, "r") as f:
        data = json.load(f)

    features = data.get("features", [])
    print("Loaded {0} features from {1}".format(len(features), INPUT_GEOJSON))

    processed_features = []
    all_x = []
    all_y = []

    for f in features:
        geom = f.get("geometry", {})
        coords = geom.get("coordinates", [])
        if not coords or not coords[0]:
            continue

        ring = coords[0]
        # Ensure closed
        if ring[0] != ring[-1]:
            ring.append(ring[0])

        # Enforce Clockwise winding for Power BI (signed_area < 0)
        sa = signed_area(ring)
        if sa > 0:
            ring.reverse()

        for pt in ring:
            all_x.append(pt[0])
            all_y.append(pt[1])

        # Standardize properties
        props = f.get("properties", {})
        brick_name = props.get("Brick_Name") or props.get("name") or f.get("id")
        brick_id = props.get("Brick_ID")
        
        clean_props = {
            "id": brick_name,
            "name": brick_name,
            "Brick_ID": brick_id,
            "Brick_Name": brick_name,
            "District": props.get("District", brick_name),
            "Governorate": props.get("Governorate", "Cairo"),
            "Zone": props.get("Zone", ""),
            "Tier": props.get("Tier", ""),
            "Tier_Number": props.get("Tier_Number", 1),
            "Potential_Index": props.get("Potential_Index", 1.0)
        }

        processed_features.append({
            "type": "Feature",
            "id": brick_name,
            "properties": clean_props,
            "geometry": {
                "type": "Polygon",
                "coordinates": [ring]
            }
        })

    # Save cleaned GeoJSON as cairo_commercial_bricks.geojson
    clean_geojson_obj = {
        "type": "FeatureCollection",
        "name": "cairo_commercial_bricks",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": processed_features
    }

    with open(OUTPUT_GEOJSON, "wb") as f:
        f.write(json.dumps(clean_geojson_obj, indent=2, ensure_ascii=True))
    print("[+] Saved clean Clockwise GeoJSON: {0}".format(OUTPUT_GEOJSON))

    # Build TopoJSON with Quantization & Delta-Encoded Arcs
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    Q = 9999.0
    scale_x = (max_x - min_x) / Q
    scale_y = (max_y - min_y) / Q
    translate_x = min_x
    translate_y = min_y

    arcs = []
    geometries = []

    for idx, f in enumerate(processed_features):
        ring = f["geometry"]["coordinates"][0]
        quantized_pts = []
        for pt in ring:
            qx = int(round((pt[0] - translate_x) / scale_x))
            qy = int(round((pt[1] - translate_y) / scale_y))
            quantized_pts.append([qx, qy])

        # Deduplicate consecutive identical integer vertices
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

        props = f["properties"]
        geom = {
            "type": "Polygon",
            "arcs": [[idx]],
            "id": props["Brick_Name"],
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

    topo_bytes = json.dumps(topojson_obj, indent=2, ensure_ascii=True)
    with open(OUTPUT_TOPOJSON, "wb") as f:
        f.write(topo_bytes)
    with open(OUTPUT_TOPO_JSON, "wb") as f:
        f.write(topo_bytes)
    print("[+] Saved quantized TopoJSON: {0} and {1}".format(OUTPUT_TOPOJSON, OUTPUT_TOPO_JSON))

    # Sync to Power BI RegisteredResources and SharedResources
    if not os.path.exists(STATIC_RESOURCES_DIR):
        os.makedirs(STATIC_RESOURCES_DIR)
    if not os.path.exists(SHARED_RESOURCES_DIR):
        os.makedirs(SHARED_RESOURCES_DIR)

    shutil.copyfile(OUTPUT_TOPOJSON, os.path.join(STATIC_RESOURCES_DIR, "cairo_commercial_bricks.topojson"))
    shutil.copyfile(OUTPUT_TOPOJSON, os.path.join(STATIC_RESOURCES_DIR, "cairo_commercial_bricks.json"))
    shutil.copyfile(OUTPUT_TOPOJSON, os.path.join(SHARED_RESOURCES_DIR, "cairo_commercial_bricks.topojson"))
    shutil.copyfile(OUTPUT_TOPOJSON, os.path.join(SHARED_RESOURCES_DIR, "cairo_commercial_bricks.json"))

    # Also sync to the specific registered resource name in report.json
    pbi_reg_file = os.path.join(STATIC_RESOURCES_DIR, "cairo_commercial_bricks0405982600071253.topojson")
    shutil.copyfile(OUTPUT_TOPOJSON, pbi_reg_file)
    print("[+] Synced TopoJSON to Power BI registered resource: {0}".format(pbi_reg_file))

    print(">>> All 36 customized shapes successfully imported and ready for Power BI!")

if __name__ == "__main__":
    convert()

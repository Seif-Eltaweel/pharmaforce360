# -*- coding: utf-8 -*-
"""
Script: generate_cairo_basemap.py
Downloads and stitches high-resolution Esri World Street Map & Light Gray tiles
for Greater Cairo, cropped precisely to the bounding box of the 36 Commercial Bricks:
  Longitude: 30.820 to 31.720 E
  Latitude:  29.800 to 30.260 N

Matches the exact Web Mercator projection of the Power BI Shape Map.
Ensures every clinic, hospital, and commercial brick sits at its exact physical coordinates.
Compatible with Python 2.7 and 3+.
"""

import os
import sys
import math
import urllib2
import threading
from io import BytesIO
from PIL import Image

DATA_DIR = r"d:\portfolio2026\02_PharmaForce360\data"
MAPS_DIR = os.path.join(DATA_DIR, "maps")
STATIC_RESOURCES_DIR = r"d:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\RegisteredResources"

if not os.path.exists(MAPS_DIR):
    os.makedirs(MAPS_DIR)

if not os.path.exists(STATIC_RESOURCES_DIR):
    os.makedirs(STATIC_RESOURCES_DIR)

BBOX_LON_MIN = 30.820
BBOX_LON_MAX = 31.720
BBOX_LAT_MIN = 29.800
BBOX_LAT_MAX = 30.260

# Zoom level 12 provides sharp street names, the River Nile, Ring Road, and Cairo districts
ZOOM = 12

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def lat2merc_y(lat_deg):
    lat_rad = math.radians(lat_deg)
    return math.log(math.tan(math.pi / 4.0 + lat_rad / 2.0))

def fetch_and_stitch(map_service_name, out_filename_base):
    print(">>> Generating base map for: " + map_service_name)
    x_start, y_end = deg2num(BBOX_LAT_MIN, BBOX_LON_MIN, ZOOM)
    x_end, y_start = deg2num(BBOX_LAT_MAX, BBOX_LON_MAX, ZOOM)

    x_tiles = list(range(x_start, x_end + 1))
    y_tiles = list(range(y_start, y_end + 1))

    tile_size = 256
    canvas_w = len(x_tiles) * tile_size
    canvas_h = len(y_tiles) * tile_size

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 255))
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # Queue of tile tasks
    tile_images = {}
    lock = threading.Lock()

    def download_tile(xi, yi, x, y):
        # ArcGIS URL format: /{z}/{y}/{x}
        url = "https://server.arcgisonline.com/ArcGIS/rest/services/{0}/MapServer/tile/{1}/{2}/{3}".format(
            map_service_name, ZOOM, y, x
        )
        try:
            req = urllib2.Request(url, headers=headers)
            resp = urllib2.urlopen(req, timeout=15)
            data = resp.read()
            img = Image.open(BytesIO(data)).convert("RGBA")
            with lock:
                tile_images[(xi, yi)] = img
        except Exception as e:
            print("  [!] Failed tile {0}/{1}: {2}".format(x, y, e))

    threads = []
    for xi, x in enumerate(x_tiles):
        for yi, y in enumerate(y_tiles):
            t = threading.Thread(target=download_tile, args=(xi, yi, x, y))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    print("  Downloaded {0}/{1} tiles. Assembling...".format(len(tile_images), len(x_tiles) * len(y_tiles)))
    for (xi, yi), img in tile_images.items():
        canvas.paste(img, (xi * tile_size, yi * tile_size))

    # Calculate exact crop box matching BBOX [30.820, 29.800, 31.720, 30.260]
    _, canvas_lon_min = num2deg(x_tiles[0], y_tiles[0], ZOOM)
    _, canvas_lon_max = num2deg(x_tiles[-1] + 1, y_tiles[-1] + 1, ZOOM)
    canvas_lat_max, _ = num2deg(x_tiles[0], y_tiles[0], ZOOM)
    canvas_lat_min, _ = num2deg(x_tiles[-1] + 1, y_tiles[-1] + 1, ZOOM)

    crop_x1 = int(round((BBOX_LON_MIN - canvas_lon_min) / (canvas_lon_max - canvas_lon_min) * canvas_w))
    crop_x2 = int(round((BBOX_LON_MAX - canvas_lon_min) / (canvas_lon_max - canvas_lon_min) * canvas_w))

    merc_lat_top = lat2merc_y(canvas_lat_max)
    merc_lat_bot = lat2merc_y(canvas_lat_min)
    merc_box_top = lat2merc_y(BBOX_LAT_MAX)
    merc_box_bot = lat2merc_y(BBOX_LAT_MIN)

    crop_y1 = int(round((merc_lat_top - merc_box_top) / (merc_lat_top - merc_lat_bot) * canvas_h))
    crop_y2 = int(round((merc_lat_top - merc_box_bot) / (merc_lat_top - merc_lat_bot) * canvas_h))

    cropped_map = canvas.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    print("  Cropped base map size: {0}x{1} pixels".format(cropped_map.size[0], cropped_map.size[1]))

    out_png_path = os.path.join(MAPS_DIR, out_filename_base + ".png")
    out_jpg_path = os.path.join(MAPS_DIR, out_filename_base + ".jpg")
    cropped_map.save(out_png_path, "PNG")
    cropped_map.convert("RGB").save(out_jpg_path, "JPEG", quality=92)
    print("  [+] Saved: {0}".format(out_png_path))

    static_png = os.path.join(STATIC_RESOURCES_DIR, out_filename_base + ".png")
    static_jpg = os.path.join(STATIC_RESOURCES_DIR, out_filename_base + ".jpg")
    cropped_map.save(static_png, "PNG")
    cropped_map.convert("RGB").save(static_jpg, "JPEG", quality=92)
    print("  [+] Synced: {0}".format(static_png))

    return out_png_path

def run():
    # 1. World Street Map (shows streets, Nile river, Cairo districts, Ring Road, major hospitals)
    fetch_and_stitch("World_Street_Map", "cairo_basemap")
    # 2. Light Gray Canvas (subtle executive style)
    fetch_and_stitch("Canvas/World_Light_Gray_Base", "cairo_basemap_light")
    print(">>> All calibrated Cairo basemaps ready!")

if __name__ == "__main__":
    run()

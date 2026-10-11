"""
Milestone 2 — Executive Overview modernization (docs/navigation_bar_specification.md).

- Removes the legacy 205 px sidebar (Nav_Sidebar_Bg, Nav_Active_Pill, Nav_Brand_Logo, Nav_Item_*).
- Adds the 240x720 SVG backdrop (nav_sidebar_overview.svg) as an image visual.
- Adds 8 transparent actionButton visuals with pageNavigation bindings (spec section 5).
- Repositions slicers / KPI cards / charts to the spec coordinate table (section 4.1).

Idempotent: safe to re-run. Writes BOM-free UTF-8 with CRLF, 2-space indent (matches PBIP file).
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPORT = REPO / "powerbi" / "PharmaForce360.Report" / "report.json"
SECTION = "Section_Executive_Overview"

LEGACY_PREFIXES = ("Nav_Item_", "Nav_Sidebar_Bg", "Nav_Active_Pill", "Nav_Brand_Logo")
NEW_NAV_PREFIXES = ("Nav_Btn_", "Nav_Sidebar_Svg")

BUTTONS = [
    ("Nav_Btn_Overview", 134, "Section_Executive_Overview", "Executive Overview"),
    ("Nav_Btn_Doctors", 188, "Section_Doctors_KOLs", "Doctors (KOLs)"),
    ("Nav_Btn_MedReps", 242, "Section_Medical_Reps", "Medical Representatives"),
    ("Nav_Btn_Bricks", 296, "Section_Bricks_Territory", "Bricks"),
    ("Nav_Btn_Visits", 350, "Section_Visits_Activity", "Visits"),
    ("Nav_Btn_Drugs", 404, "Section_Commercial_IQVIA", "Drugs & Market Comparisons"),
    ("Nav_Btn_Distributors", 458, "Section_Distributors_Stock", "Distributors & Stock"),
    ("Nav_Btn_Expenses", 512, "Section_Expenses_Budget", "Expenses & Budget"),
]

# name -> (x, y, w, h, z)  — spec section 4.1 (accent bars ride on their KPI card)
LAYOUT = {
    "Slicer_Line": (252, 16, 246, 46, 1010),
    "Slicer_Zone": (508, 16, 246, 46, 1020),
    "Slicer_Period": (764, 16, 246, 46, 1030),
    "Slicer_Tier": (1020, 16, 244, 46, 1040),
    "Card_Gross_Revenue": (252, 72, 246, 88, 1110),
    "Card_Market_Share": (508, 72, 246, 88, 1120),
    "Card_Call_Attainment": (764, 72, 246, 88, 1130),
    "Card_High_Risk_KOLs": (1020, 72, 244, 88, 1140),
    "Accent_Kpi_1": (252, 72, 5, 88, 1111),
    "Accent_Kpi_2": (508, 72, 5, 88, 1121),
    "Accent_Kpi_3": (764, 72, 5, 88, 1131),
    "Accent_Kpi_4": (1020, 72, 5, 88, 1141),
    "Chart_Revenue_MarketShare": (252, 172, 610, 256, 1210),
    "1a9429b8f386195c3689": (872, 172, 392, 256, 1215),  # Cairo basemap image (under shape map)
    "bbd908fa5bfdfc29dabb": (872, 172, 392, 256, 1220),  # Cairo shape map
    "Chart_Brick_Ranking": (252, 440, 330, 264, 1310),
    "Chart_Distributor_Share": (592, 440, 300, 264, 1320),
    "Chart_Attainment_Tier": (902, 440, 362, 264, 1330),
}


def lit(v: str) -> dict:
    return {"expr": {"Literal": {"Value": v}}}


def container(name: str, x, y, w, h, z, single_visual: dict) -> dict:
    cfg = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": float(x), "y": float(y), "width": float(w),
                                             "height": float(h), "z": float(z)}}],
        "singleVisual": single_visual,
    }
    return {"config": json.dumps(cfg, separators=(",", ":"), ensure_ascii=False),
            "filters": "[]", "height": float(h), "width": float(w),
            "x": float(x), "y": float(y), "z": float(z)}


def transparent_vc() -> dict:
    return {
        "background": [{"properties": {"show": lit("false"), "transparency": lit("100D")}}],
        "border": [{"properties": {"show": lit("false")}}],
        "dropShadow": [{"properties": {"show": lit("false")}}],
        "visualHeader": [{"properties": {"show": lit("false")}}],
    }


def sidebar_image() -> dict:
    sv = {
        "visualType": "image",
        "drillFilterOtherVisuals": True,
        "objects": {"image": [{"properties": {"sourceFile": {"image": {
            "name": lit("'nav_sidebar_overview.svg'"),
            "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources",
                                                      "PackageType": 1,
                                                      "ItemName": "nav_sidebar_overview.svg"}}},
            "scaling": lit("'Fit'"),
        }}}}]},
        "vcObjects": {**transparent_vc(),
                      "padding": [{"properties": {k: lit("0D") for k in ("top", "bottom", "left", "right")}}]},
    }
    return container("Nav_Sidebar_Svg", 0, 0, 240, 720, 10, sv)


def nav_button(name, y, target, label, z) -> dict:
    off = lit("false")
    clear = lit("100D")
    states = [None, "default", "hover", "selected", "disabled"]

    def per_state(props: dict) -> list:
        return [{"properties": props} if s is None else {"properties": props, "selector": {"id": s}}
                for s in states]

    sv = {
        "visualType": "actionButton",
        "drillFilterOtherVisuals": True,
        "objects": {
            "icon": [{"properties": {"shapeType": lit("'blank'")}, "selector": {"id": "default"}}],
            # Fill/outline are set both unscoped and per state; with only the 'default' selector,
            # Power BI still drew its built-in white fill + grey outline.
            "fill": per_state({"show": off, "transparency": clear}),
            "outline": per_state({"show": off, "transparency": clear, "weight": lit("0D")}),
            "text": per_state({"show": off}),
            "glow": [{"properties": {"show": off}}],
            "shadow": [{"properties": {"show": off}}],
            "action": [{"properties": {
                "show": lit("true"),
                # Power BI's actual page-navigation schema (spec section 5's
                # 'pageNavigation.page' form is not what Power BI Desktop reads):
                "type": lit("'PageNavigation'"),
                "navigationSection": lit(f"'{target}'"),
                "tooltip": lit(f"'Go to {label}'"),
            }}],
        },
        "vcObjects": transparent_vc(),
    }
    return container(name, 12, y, 216, 40, z, sv)


def apply_position(vc: dict, x, y, w, h, z) -> None:
    cfg = json.loads(vc["config"])
    for lay in cfg.get("layouts", []):
        lay["position"].update({"x": float(x), "y": float(y), "width": float(w),
                                "height": float(h), "z": float(z)})
    vc["config"] = json.dumps(cfg, separators=(",", ":"), ensure_ascii=False)
    vc.update({"x": float(x), "y": float(y), "width": float(w), "height": float(h), "z": float(z)})


_NUM = "@@PBINUM@@"
_NUM_RE = re.compile(r'"' + _NUM + r'([^"]*?)' + _NUM + r'"')


def load(raw: bytes):
    """Parse JSON keeping each float's original text so re-serialisation is byte-identical."""
    return json.loads(raw.decode("utf-8-sig"), parse_float=lambda s: f"{_NUM}{s}{_NUM}")


def dump(data) -> bytes:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    text = _NUM_RE.sub(lambda m: m.group(1), text)
    return text.replace("\n", "\r\n").encode("utf-8")


def main() -> None:
    raw = REPORT.read_bytes()
    data = load(raw)
    if dump(data) != raw.lstrip(b"\xef\xbb\xbf"):
        print("WARNING: serializer round-trip differs from on-disk formatting (diff may be noisy).")

    backup = REPORT.with_suffix(".json.bak_pre_m2")
    if not backup.exists():
        shutil.copy2(REPORT, backup)

    sec = next(s for s in data["sections"] if s["name"] == SECTION)
    kept, removed = [], []
    for vc in sec["visualContainers"]:
        n = json.loads(vc["config"]).get("name", "")
        (removed if n.startswith(LEGACY_PREFIXES + NEW_NAV_PREFIXES) else kept).append(vc)
        if n in LAYOUT and vc in kept:
            apply_position(vc, *LAYOUT[n])

    names = {json.loads(v["config"]).get("name") for v in kept}
    missing = set(LAYOUT) - names
    if missing:
        raise SystemExit(f"Expected visuals not found on {SECTION}: {sorted(missing)}")

    new = [sidebar_image()] + [nav_button(n, y, t, l, 100 * (i + 1)) for i, (n, y, t, l) in enumerate(BUTTONS)]
    sec["visualContainers"] = new + kept

    REPORT.write_bytes(dump(data))
    print(f"Removed {len([r for r in removed])} legacy/old nav visuals, added {len(new)}, repositioned {len(LAYOUT)}.")
    print(f"Backup: {backup}")


if __name__ == "__main__":
    main()

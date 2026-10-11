"""
Core models, parsers, and verification utilities for PharmaForce 360° E2E testing.
Validates Power BI PBIP report definitions, themes, and canvas layout compliance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ==============================================================================
# Specification Constants & Configuration
# ==============================================================================

REPO_ROOT = Path(__file__).resolve().parent.parent

PATH_THEME_ROOT = REPO_ROOT / "powerbi" / "theme.json"
PATH_THEME_REGISTERED = (
    REPO_ROOT
    / "powerbi"
    / "PharmaForce360.Report"
    / "StaticResources"
    / "RegisteredResources"
    / "PharmaForce360Theme.json"
)
PATH_REPORT_JSON = (
    REPO_ROOT / "powerbi" / "PharmaForce360.Report" / "report.json"
)
DIR_REGISTERED_RESOURCES = (
    REPO_ROOT
    / "powerbi"
    / "PharmaForce360.Report"
    / "StaticResources"
    / "RegisteredResources"
)
DIR_DATA_ASSETS_NAV = REPO_ROOT / "data" / "assets" / "navigation"

# 8 Analytical Domains defined in docs/navigation_bar_specification.md
DOMAIN_MAPPING: Dict[str, Dict[str, Any]] = {
    "Section_Executive_Overview": {
        "index": 1,
        "display_name": "Executive Overview",
        "svg_asset": "nav_sidebar_overview.svg",
        "button_y": 134.0,
    },
    "Section_Doctors_KOLs": {
        "index": 2,
        "display_name": "02 Doctors and KOL Insights",
        "svg_asset": "nav_sidebar_doctors.svg",
        "button_y": 188.0,
    },
    "Section_Medical_Reps": {
        "index": 3,
        "display_name": "03 Medical Representatives",
        "svg_asset": "nav_sidebar_medical_reps.svg",
        "button_y": 242.0,
    },
    "Section_Bricks_Territory": {
        "index": 4,
        "display_name": "04 Brick Territory Dynamics",
        "svg_asset": "nav_sidebar_bricks.svg",
        "button_y": 296.0,
    },
    "Section_Visits_Activity": {
        "index": 5,
        "display_name": "05 Field Detailing and Visits",
        "svg_asset": "nav_sidebar_visits.svg",
        "button_y": 350.0,
    },
    "Section_Commercial_IQVIA": {
        "index": 6,
        "display_name": "06 Commercial and IQVIA Audit",
        "svg_asset": "nav_sidebar_drugs.svg",
        "button_y": 404.0,
    },
    "Section_Distributors_Stock": {
        "index": 7,
        "display_name": "07 Supply Chain and Stock-Out",
        "svg_asset": "nav_sidebar_distributors.svg",
        "button_y": 458.0,
    },
    "Section_Expenses_Budget": {
        "index": 8,
        "display_name": "08 Promotional ROI and Budget",
        "svg_asset": "nav_sidebar_expenses.svg",
        "button_y": 512.0,
    },
}

# 8 Button Definitions per Page
ACTION_BUTTON_SPECS: List[Dict[str, Any]] = [
    {
        "slot": 1,
        "y": 134.0,
        "target": "Section_Executive_Overview",
        "label": "Executive Overview",
    },
    {
        "slot": 2,
        "y": 188.0,
        "target": "Section_Doctors_KOLs",
        "label": "Doctors (KOLs)",
    },
    {
        "slot": 3,
        "y": 242.0,
        "target": "Section_Medical_Reps",
        "label": "Medical Reps",
    },
    {
        "slot": 4,
        "y": 296.0,
        "target": "Section_Bricks_Territory",
        "label": "Bricks",
    },
    {
        "slot": 5,
        "y": 350.0,
        "target": "Section_Visits_Activity",
        "label": "Visits",
    },
    {
        "slot": 6,
        "y": 404.0,
        "target": "Section_Commercial_IQVIA",
        "label": "Drugs & Comparisons",
    },
    {
        "slot": 7,
        "y": 458.0,
        "target": "Section_Distributors_Stock",
        "label": "Distributors & Stock",
    },
    {
        "slot": 8,
        "y": 512.0,
        "target": "Section_Expenses_Budget",
        "label": "Expenses & Budget",
    },
]

BUTTON_GEOMETRY = {
    "x": 12.0,
    "width": 216.0,
    "height": 40.0,
}

SIDEBAR_IMAGE_GEOMETRY = {
    "x": 0.0,
    "y": 0.0,
    "width": 240.0,
    "height": 720.0,
}

CANVAS_DIMENSIONS = {
    "width": 1280.0,
    "height": 720.0,
}

SIDEBAR_WIDTH_PX = 240.0
ANALYTICAL_MIN_X_PX = 252.0  # 12 px clearance gutter

VERTICAL_BANDS = {
    "slicers": {"min_y": 16.0, "max_y": 62.0, "nominal_h": 46.0},
    "kpi_cards": {"min_y": 72.0, "max_y": 160.0, "nominal_h": 88.0},
    "upper_charts": {"min_y": 172.0, "max_y": 428.0, "nominal_h": 256.0},
    "lower_charts": {"min_y": 440.0, "max_y": 704.0, "nominal_h": 264.0},
}


# ==============================================================================
# Helper Parsing Functions
# ==============================================================================

def clean_literal_value(val: Any) -> str:
    """Extract and unwrap literal string value from Power BI expression."""
    if val is None:
        return ""
    s = str(val).strip()
    if s.startswith("'") and s.endswith("'"):
        s = s[1:-1]
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    return s.strip()


def parse_numeric_literal(val: Any) -> Optional[float]:
    """Parse numeric literal from Power BI expression (e.g. '100D', '0D', 100)."""
    if val is None:
        return None
    s = str(val).strip().rstrip("DdFf")
    try:
        return float(s)
    except ValueError:
        return None


def parse_bool_literal(val: Any) -> Optional[bool]:
    """Parse boolean literal from Power BI expression (e.g. 'false', False)."""
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    if s in ("false", "'false'", '"false"'):
        return False
    if s in ("true", "'true'", '"true"'):
        return True
    return None


# ==============================================================================
# Data Models
# ==============================================================================

@dataclass
class VisualContainer:
    name: str
    visual_type: str
    x: float
    y: float
    width: float
    height: float
    z: float
    drill_filter_other_visuals: bool = False
    action_type: Optional[str] = None
    action_target: Optional[str] = None
    bg_transparency: Optional[float] = None
    bg_color: Optional[str] = None
    border_show: Optional[bool] = None
    image_resource_name: Optional[str] = None
    raw_config: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_in_sidebar(self) -> bool:
        """Visual resides inside or touches the 240px sidebar zone."""
        return self.x < SIDEBAR_WIDTH_PX

    @property
    def is_action_button(self) -> bool:
        return self.visual_type == "actionButton"

    @property
    def is_sidebar_backdrop(self) -> bool:
        return (
            self.visual_type == "image"
            and abs(self.x) < 1.0
            and abs(self.y) < 1.0
            and abs(self.width - SIDEBAR_IMAGE_GEOMETRY["width"]) < 2.0
            and abs(self.height - SIDEBAR_IMAGE_GEOMETRY["height"]) < 2.0
        )


@dataclass
class ReportSection:
    name: str
    display_name: str
    ordinal: int
    visuals: List[VisualContainer] = field(default_factory=list)

    @property
    def action_buttons(self) -> List[VisualContainer]:
        return [v for v in self.visuals if v.is_action_button]

    @property
    def sidebar_backdrop(self) -> Optional[VisualContainer]:
        for v in self.visuals:
            if v.is_sidebar_backdrop:
                return v
        return None

    @property
    def analytical_visuals(self) -> List[VisualContainer]:
        """Visuals that belong to the analytical report canvas (excluding sidebar)."""
        return [
            v for v in self.visuals
            if not v.is_action_button and not v.is_sidebar_backdrop
        ]


@dataclass
class ReportModel:
    sections: Dict[str, ReportSection]
    registered_resources: List[Dict[str, Any]]
    raw_json: Dict[str, Any]


@dataclass
class ThemeModel:
    name: str
    raw_json: Dict[str, Any]
    visual_styles: Dict[str, Any]


# ==============================================================================
# Model Parsers & Loader Functions
# ==============================================================================

def check_bom_free_utf8(path: Path) -> Tuple[bool, str]:
    """Verify that file is valid UTF-8 without Byte Order Mark (BOM)."""
    if not path.is_file():
        return False, f"File does not exist: {path}"
    raw_bytes = path.read_bytes()
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        return False, "File has UTF-8 BOM (EF BB BF) header"
    if raw_bytes.startswith(b"\xff\xfe") or raw_bytes.startswith(b"\xfe\xff"):
        return False, "File has UTF-16 BOM header"
    try:
        raw_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        return False, f"UTF-8 decoding failed: {e}"
    return True, "Valid BOM-free UTF-8"


def parse_visual_container(vc: Dict[str, Any]) -> VisualContainer:
    """Parse a single PBIP visual container dict into structured model."""
    raw_config = {}
    config_val = vc.get("config", "{}")
    if isinstance(config_val, str):
        try:
            raw_config = json.loads(config_val)
        except Exception:
            raw_config = {}
    elif isinstance(config_val, dict):
        raw_config = config_val

    name = raw_config.get("name", vc.get("name", "Unnamed_Visual"))
    layouts = raw_config.get("layouts", [{}])
    pos = layouts[0].get("position", {}) if layouts else {}

    # Extract coordinates, preferring layouts position, fallback to root vc
    x = float(pos.get("x", vc.get("x", 0.0)))
    y = float(pos.get("y", vc.get("y", 0.0)))
    width = float(pos.get("width", vc.get("width", 0.0)))
    height = float(pos.get("height", vc.get("height", 0.0)))
    z = float(pos.get("z", vc.get("z", 0.0)))

    single_visual = raw_config.get("singleVisual", {})
    visual_type = single_visual.get("visualType", vc.get("visualType", "unknown"))
    drill_filter = single_visual.get("drillFilterOtherVisuals", False)

    objects = single_visual.get("objects", {})
    vc_objects = single_visual.get("vcObjects", {})

    # Action binding parsing
    action_type = None
    action_target = None
    action_list = objects.get("action", [])
    if action_list and isinstance(action_list, list):
        action_props = action_list[0].get("properties", {})
        type_expr = action_props.get("type", {}).get("expr", {}).get("Literal", {}).get("Value")
        action_type = clean_literal_value(type_expr)
        # Power BI writes 'PageNavigation'; normalise to the spec's 'pageNavigation'.
        if action_type.lower() == "pagenavigation":
            action_type = "pageNavigation"
        page_expr = (
            action_props.get("pageNavigation", {})
            .get("page", {})
            .get("expr", {})
            .get("Literal", {})
            .get("Value")
        )
        if page_expr is None:  # Power BI's real property name
            page_expr = (
                action_props.get("navigationSection", {})
                .get("expr", {})
                .get("Literal", {})
                .get("Value")
            )
        action_target = clean_literal_value(page_expr)

    # Background transparency and border
    bg_transparency = None
    bg_color = None
    bg_list = vc_objects.get("background", [])
    if bg_list and isinstance(bg_list, list):
        bg_props = bg_list[0].get("properties", {})
        trans_val = bg_props.get("transparency", {}).get("expr", {}).get("Literal", {}).get("Value")
        if trans_val is not None:
            bg_transparency = parse_numeric_literal(trans_val)
        color_val = bg_props.get("color", {}).get("solid", {}).get("color", "")
        if isinstance(color_val, dict):
            color_val = color_val.get("expr", {}).get("Literal", {}).get("Value", "")
        bg_color = clean_literal_value(color_val)

    border_show = None
    border_list = vc_objects.get("border", [])
    if border_list and isinstance(border_list, list):
        border_props = border_list[0].get("properties", {})
        show_val = border_props.get("show", {}).get("expr", {}).get("Literal", {}).get("Value")
        border_show = parse_bool_literal(show_val)

    # Image resource parsing
    image_resource_name = None
    img_list = objects.get("image", [])
    if img_list and isinstance(img_list, list):
        img_props = img_list[0].get("properties", {})
        src_file = img_props.get("sourceFile", {}).get("image", {})
        # check url expr ResourcePackageItem
        url_expr = src_file.get("url", {}).get("expr", {}).get("ResourcePackageItem", {})
        if url_expr:
            image_resource_name = url_expr.get("ItemName")
        if not image_resource_name:
            name_expr = src_file.get("name", {}).get("expr", {}).get("Literal", {}).get("Value")
            image_resource_name = clean_literal_value(name_expr)

    return VisualContainer(
        name=name,
        visual_type=visual_type,
        x=x,
        y=y,
        width=width,
        height=height,
        z=z,
        drill_filter_other_visuals=bool(drill_filter),
        action_type=action_type,
        action_target=action_target,
        bg_transparency=bg_transparency,
        bg_color=bg_color,
        border_show=border_show,
        image_resource_name=image_resource_name,
        raw_config=raw_config,
    )


def load_report_model(path: Path = PATH_REPORT_JSON) -> ReportModel:
    """Load and parse report.json into ReportModel."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract registered resources
    registered_items: List[Dict[str, Any]] = []
    for pkg in data.get("resourcePackages", []):
        r_pkg = pkg.get("resourcePackage", {})
        if r_pkg.get("name") == "RegisteredResources":
            registered_items = r_pkg.get("items", [])
            break

    # Extract sections
    sections: Dict[str, ReportSection] = {}
    for sec_data in data.get("sections", []):
        sec_name = sec_data.get("name", "")
        display_name = sec_data.get("displayName", "")
        ordinal = sec_data.get("ordinal", 0)

        visuals: List[VisualContainer] = []
        for vc_data in sec_data.get("visualContainers", []):
            visuals.append(parse_visual_container(vc_data))

        sections[sec_name] = ReportSection(
            name=sec_name,
            display_name=display_name,
            ordinal=ordinal,
            visuals=visuals,
        )

    return ReportModel(
        sections=sections,
        registered_resources=registered_items,
        raw_json=data,
    )


def load_theme_model(path: Path) -> ThemeModel:
    """Load and parse a theme JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    name = data.get("name", "")
    visual_styles = data.get("visualStyles", {})
    return ThemeModel(name=name, raw_json=data, visual_styles=visual_styles)


# ==============================================================================
# Collision & Layout Audit Utilities
# ==============================================================================

def check_bounding_box_overlap(
    v1: VisualContainer,
    v2: VisualContainer,
    tolerance_px: float = 2.0,
) -> bool:
    """
    Check if two visual bounding boxes intersect beyond the given tolerance.
    Tolerance allows touching edges without false-positive collision flag.
    """
    # Overlap along X
    x_overlap = min(v1.x + v1.width, v2.x + v2.width) - max(v1.x, v2.x)
    # Overlap along Y
    y_overlap = min(v1.y + v1.height, v2.y + v2.height) - max(v1.y, v2.y)

    return (x_overlap > tolerance_px) and (y_overlap > tolerance_px)


def audit_section_coordinates(sec: ReportSection) -> List[Dict[str, Any]]:
    """Audit every visual in a report section and verify specification adherence."""
    results: List[Dict[str, Any]] = []

    for v in sec.visuals:
        is_sidebar_element = v.is_action_button or v.is_sidebar_backdrop

        # Check X clearance
        x_compliant = True
        notes = []
        if not is_sidebar_element:
            if v.x < ANALYTICAL_MIN_X_PX:
                x_compliant = False
                notes.append(f"X={v.x:.1f} violates clearance (X < {ANALYTICAL_MIN_X_PX})")

        # Canvas bounds check
        bounds_compliant = (
            v.x >= 0.0
            and v.y >= 0.0
            and (v.x + v.width) <= CANVAS_DIMENSIONS["width"] + 1.0
            and (v.y + v.height) <= CANVAS_DIMENSIONS["height"] + 1.0
        )
        if not bounds_compliant:
            notes.append(f"Exceeds canvas 1280x720 bounds (X+W={v.x+v.width}, Y+H={v.y+v.height})")

        results.append({
            "section_name": sec.name,
            "section_display": sec.display_name,
            "visual_name": v.name,
            "visual_type": v.visual_type,
            "x": v.x,
            "y": v.y,
            "width": v.width,
            "height": v.height,
            "z": v.z,
            "is_sidebar": is_sidebar_element,
            "action_target": v.action_target,
            "x_compliant": x_compliant,
            "bounds_compliant": bounds_compliant,
            "status": "PASS" if (x_compliant and bounds_compliant) else "FAIL",
            "notes": "; ".join(notes) if notes else "Compliant",
        })

    return results


def format_audit_table_markdown(audit_entries: List[Dict[str, Any]]) -> str:
    """Format visual coordinate audit entries into an ASCII/Markdown table."""
    headers = [
        "Section",
        "Visual Name",
        "Type",
        "X",
        "Y",
        "W",
        "H",
        "Z",
        "Target",
        "Status",
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for e in audit_entries:
        sec_short = e["section_name"].replace("Section_", "")
        v_name = (e["visual_name"][:24] + "..") if len(e["visual_name"]) > 26 else e["visual_name"]
        v_type = e["visual_type"]
        target = e["action_target"] or "-"
        if len(target) > 20:
            target = target.replace("Section_", "")
        row = [
            sec_short,
            v_name,
            v_type,
            f"{e['x']:.1f}",
            f"{e['y']:.1f}",
            f"{e['width']:.1f}",
            f"{e['height']:.1f}",
            f"{int(e['z'])}",
            target,
            e["status"],
        ]
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)

# -*- coding: utf-8 -*-
"""
generate_navigation_svgs.py
Generates 8 pixel-perfect SVG sidebar assets matching the PharmaForce 360 mockup.
One SVG is generated per active page state to provide zero-distortion vector rendering.
"""

import os
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

OUTPUT_DIRS = [
    r"D:\portfolio2026\02_PharmaForce360\data\assets\navigation",
    r"D:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\StaticResources\RegisteredResources"
]

NAV_ITEMS = [
    {
        "id": "overview",
        "label": "Executive Overview",
        "icon_type": "grid",
        "y": 134
    },
    {
        "id": "doctors",
        "label": "Doctors (KOLs)",
        "icon_type": "doctor",
        "y": 188
    },
    {
        "id": "medical_reps",
        "label": "Medical Representatives",
        "icon_type": "reps",
        "y": 242
    },
    {
        "id": "bricks",
        "label": "Bricks",
        "icon_type": "map",
        "y": 296
    },
    {
        "id": "visits",
        "label": "Visits",
        "icon_type": "calendar",
        "y": 350
    },
    {
        "id": "drugs",
        "label": "Drugs & Market Comparisons",
        "icon_type": "capsule",
        "y": 404
    },
    {
        "id": "distributors",
        "label": "Distributors & Stock",
        "icon_type": "box",
        "y": 458
    },
    {
        "id": "expenses",
        "label": "Expenses & Budget",
        "icon_type": "wallet",
        "y": 512
    }
]

def render_icon(icon_type, is_active, base_y):
    color = "#FFFFFF" if is_active else "#9BB3D6"
    accent = "#38BDF8" if is_active else "#6487B8"
    cy = base_y + 20
    
    if icon_type == "grid":
        return f"""
        <g stroke="{color}" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="26" y="{cy-8}" width="6.5" height="6.5" rx="1.5" />
            <rect x="35.5" y="{cy-8}" width="6.5" height="6.5" rx="1.5" />
            <rect x="26" y="{cy+1.5}" width="6.5" height="6.5" rx="1.5" />
            <rect x="35.5" y="{cy+1.5}" width="6.5" height="6.5" rx="1.5" />
        </g>
        """
    elif icon_type == "doctor":
        return f"""
        <g stroke="{color}" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="34" cy="{cy-4}" r="4" />
            <path d="M26 {cy+9} C26 {cy+4} 29.5 {cy+3} 34 {cy+3} C38.5 {cy+3} 42 {cy+4} 42 {cy+9}" />
            <path d="M29 {cy-1} V{cy+3} C29 {cy+6} 39 {cy+6} 39 {cy+3} V{cy-1}" stroke="{accent}" stroke-width="1.3" />
        </g>
        """
    elif icon_type == "reps":
        return f"""
        <g stroke="{color}" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="31" cy="{cy-4}" r="3.5" />
            <path d="M24 {cy+9} C24 {cy+5} 27 {cy+4} 31 {cy+4} C35 {cy+4} 38 {cy+5} 38 {cy+9}" />
            <circle cx="39" cy="{cy-6}" r="2.8" stroke="{accent}" />
            <path d="M37 {cy+1} C39 {cy+1} 44 {cy+2} 44 {cy+7}" stroke="{accent}" />
        </g>
        """
    elif icon_type == "map":
        return f"""
        <g stroke="{color}" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="25,{cy-7} 31,{cy-5} 37,{cy-7} 43,{cy-5} 43,{cy+8} 37,{cy+6} 31,{cy+8} 25,{cy+6}" />
            <line x1="31" y1="{cy-5}" x2="31" y2="{cy+8}" stroke="{accent}" />
            <line x1="37" y1="{cy-7}" x2="37" y2="{cy+6}" stroke="{accent}" />
        </g>
        """
    elif icon_type == "calendar":
        return f"""
        <g stroke="{color}" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <rect x="25" y="{cy-7}" width="18" height="16" rx="2.5" />
            <line x1="25" y1="{cy-2}" x2="43" y2="{cy-2}" stroke="{accent}" />
            <line x1="29" y1="{cy-9}" x2="29" y2="{cy-6}" />
            <line x1="39" y1="{cy-9}" x2="39" y2="{cy-6}" />
            <path d="M29 {cy+3} L32 {cy+6} L39 {cy}" stroke="{color}" stroke-width="1.8" />
        </g>
        """
    elif icon_type == "capsule":
        return f"""
        <g stroke="{color}" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <path d="M26 {cy+6} L37 {cy-5} A4.5 4.5 0 0 0 31 {cy-11} L20 {cy} A4.5 4.5 0 0 0 26 {cy+6} Z" />
            <line x1="25" y1="{cy-4}" x2="33" y2="{cy+4}" stroke="{accent}" stroke-width="1.5" />
        </g>
        """
    elif icon_type == "box":
        return f"""
        <g stroke="{color}" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <path d="M34 {cy-8} L43 {cy-3.5} L34 {cy+1} L25 {cy-3.5} Z" />
            <path d="M25 {cy-3.5} V{cy+6} L34 {cy+10.5} V{cy+1}" stroke="{accent}" />
            <path d="M43 {cy-3.5} V{cy+6} L34 {cy+10.5}" />
        </g>
        """
    elif icon_type == "wallet":
        return f"""
        <g stroke="{color}" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <rect x="24" y="{cy-6}" width="20" height="15" rx="3" />
            <path d="M24 {cy-2} H44" stroke="{accent}" />
            <circle cx="39" cy="{cy+3}" r="1.5" fill="{color}" />
        </g>
        """
    return ""

def generate_sidebar_svg(active_id):
    items_markup = []
    
    for item in NAV_ITEMS:
        is_active = (item["id"] == active_id)
        y = item["y"]
        label = escape(item["label"])  # '&' must be '&amp;' or the SVG is invalid XML
        icon_html = render_icon(item["icon_type"], is_active, y)
        
        if is_active:
            pill = f"""
            <!-- Active item pill -->
            <rect x="12" y="{y}" width="216" height="40" rx="10" fill="url(#activePillGradient)" stroke="#38BDF8" stroke-width="1" />
            <!-- Inner subtle glow -->
            <rect x="13" y="{y+1}" width="214" height="38" rx="9" fill="none" stroke="#7DD3FC" stroke-opacity="0.3" stroke-width="1" />
            """
            text_fill = "#FFFFFF"
            font_weight = "600"
            font_size = "11.5px"
        else:
            pill = ""
            text_fill = "#C8DCF5"
            font_weight = "500"
            font_size = "11.5px"
            
        text_html = f"""
        <text x="52" y="{y+25}" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif" 
              font-size="{font_size}" font-weight="{font_weight}" fill="{text_fill}">{label}</text>
        """
        
        items_markup.append(f"""
        <!-- Menu Item: {label} -->
        <g id="menu_{item['id']}">
            {pill}
            {icon_html}
            {text_html}
        </g>
        """)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="240" height="720" viewBox="0 0 240 720">
    <defs>
        <!-- Deep rich navy background gradient -->
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#071E54" />
            <stop offset="60%" stop-color="#0A2568" />
            <stop offset="100%" stop-color="#071945" />
        </linearGradient>
        
        <!-- Active cyan/azure pill gradient matching mockup -->
        <linearGradient id="activePillGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#00A3E0" />
            <stop offset="100%" stop-color="#0077B6" />
        </linearGradient>
        
        <!-- Caduceus glow / accent -->
        <linearGradient id="brandCyan" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#38BDF8" />
            <stop offset="100%" stop-color="#00A3E0" />
        </linearGradient>
    </defs>

    <!-- Sidebar Main Background -->
    <rect x="0" y="0" width="240" height="720" fill="url(#bgGradient)" />
    
    <!-- Right subtle border separator -->
    <line x1="239.5" y1="0" x2="239.5" y2="720" stroke="#16326E" stroke-width="1" />

    <!-- BRAND / LOGO SECTION -->
    <g id="brand_header" transform="translate(18, 22)">
        <!-- Caduceus Medical Emblem -->
        <g stroke="url(#brandCyan)" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <!-- Center Staff -->
            <line x1="16" y1="6" x2="16" y2="38" stroke="#FFFFFF" stroke-width="2" />
            <circle cx="16" cy="4" r="2.5" fill="#38BDF8" stroke="#FFFFFF" stroke-width="1" />
            
            <!-- Dual Coiled Serpents -->
            <path d="M10 14 C13 10 19 10 22 14 C25 18 19 22 16 24 C13 22 7 18 10 14 Z" stroke-width="1.6" />
            <path d="M10 26 C13 22 19 22 22 26 C25 30 19 34 16 36 C13 34 7 30 10 26 Z" stroke-width="1.6" />
            
            <!-- Wing Spreads -->
            <path d="M16 11 C11 7 4 8 2 12 C6 14 11 13 16 14" stroke-width="1.5" />
            <path d="M16 11 C21 7 28 8 30 12 C26 14 21 13 16 14" stroke-width="1.5" />
        </g>

        <!-- Brand Text -->
        <text x="42" y="22" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif" 
              font-size="16px" font-weight="700" fill="#FFFFFF" letter-spacing="0.3px">PharmaForce</text>
        <text x="42" y="38" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif" 
              font-size="15px" font-weight="600" fill="#38BDF8">360°</text>
    </g>

    <!-- Subtle horizontal separator below logo -->
    <line x1="16" y1="88" x2="224" y2="88" stroke="#163470" stroke-width="0.8" stroke-dasharray="3,3" />

    <!-- NAVIGATION MENU ITEMS -->
    {''.join(items_markup)}

    <!-- BOTTOM SYSTEM BADGE / COPYRIGHT -->
    <g id="sidebar_footer" transform="translate(18, 680)">
        <circle cx="8" cy="8" r="3" fill="#10B981" />
        <text x="18" y="11" font-family="'Segoe UI', sans-serif" font-size="9px" font-weight="500" fill="#6487B8">v2.4 Greater Cairo Market</text>
    </g>
</svg>"""
    return svg_content

def main():
    print(">>> Generating 8 SVG Sidebar Navigation Assets...")
    for out_dir in OUTPUT_DIRS:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            print(f"Created directory: {out_dir}")
            
        for item in NAV_ITEMS:
            svg_data = generate_sidebar_svg(item["id"])
            ET.fromstring(svg_data)  # raises if not well-formed XML (Power BI shows a broken image)
            filename = f"nav_sidebar_{item['id']}.svg"
            filepath = os.path.join(out_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(svg_data)
            print(f"  [+] Generated: {filepath}")

    print(">>> All 8 SVG assets successfully generated!")

if __name__ == "__main__":
    main()

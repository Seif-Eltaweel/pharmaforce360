# -*- coding: utf-8 -*-
"""
Script: generate_executive_overview.py
Generates the Executive Overview dashboard page matching the visual mockup image
for the PharmaForce 360 Power BI Project (.pbip). Compatible with Python 2.7 and Python 3+.
"""

import json
import codecs

REPORT_JSON_PATH = r"d:\portfolio2026\02_PharmaForce360\powerbi\PharmaForce360.Report\report.json"

def make_shape_visual(name, x, y, w, h, z=0, fill_color="#071E54", border_color="#071E54", round_radius=0):
    tile_shape = "'roundRectangle'" if round_radius > 0 else "'rectangle'"
    round_val = "{0}D".format(round_radius)
    fill_val = "'{0}'".format(fill_color)
    border_val = "'{0}'".format(border_color)

    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "shape",
            "drillFilterOtherVisuals": True,
            "objects": {
                "shape": [
                    {
                        "properties": {
                            "tileShape": {"expr": {"Literal": {"Value": tile_shape}}},
                            "roundPercentage": {"expr": {"Literal": {"Value": round_val}}}
                        }
                    }
                ],
                "fill": [
                    {
                        "properties": {
                            "fillColor": {"solid": {"color": {"expr": {"Literal": {"Value": fill_val}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "outline": [
                    {
                        "properties": {
                            "lineColor": {"solid": {"color": {"expr": {"Literal": {"Value": border_val}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}},
                            "weight": {"expr": {"Literal": {"Value": "1D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }


def make_text_visual(name, x, y, w, h, z=100, text="", color="#FFFFFF", font_size="11pt", font_family="Segoe UI Semibold", bg_color=None, border_color=None, border_radius=0):
    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "textbox",
            "drillFilterOtherVisuals": True,
            "objects": {
                "general": [
                    {
                        "properties": {
                            "paragraphs": [
                                {
                                    "textRuns": [
                                        {
                                            "value": text,
                                            "textStyle": {
                                                "fontFamily": font_family,
                                                "fontSize": font_size,
                                                "color": color
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }

    if bg_color:
        bg_val = "'{0}'".format(bg_color)
        cfg["singleVisual"]["vcObjects"] = {
            "background": [
                {
                    "properties": {
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": bg_val}}}}},
                        "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                    }
                }
            ]
        }
        if border_color:
            border_val = "'{0}'".format(border_color)
            radius_val = "{0}D".format(border_radius)
            cfg["singleVisual"]["vcObjects"]["border"] = [
                {
                    "properties": {
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": border_val}}}}},
                        "radius": {"expr": {"Literal": {"Value": radius_val}}}
                    }
                }
            ]

    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }


def make_slicer_visual(name, x, y, w, h, z=200, table_name="dim_product", column_name="Therapeutic_Line", title_text="Line: Cardio-Metabolic"):
    query_ref = "{0}.{1}".format(table_name, column_name)
    title_val = "'{0}'".format(title_text)
    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "slicer",
            "projections": {
                "Values": [{"queryRef": query_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "t", "Entity": table_name, "Type": 0}],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "t"}},
                            "Property": column_name
                        },
                        "Name": query_ref
                    }
                ]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "data": [
                    {
                        "properties": {
                            "mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}
                        }
                    }
                ],
                "header": [
                    {
                        "properties": {
                            "text": {"expr": {"Literal": {"Value": title_val}}},
                            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0A2540'"}}}}},
                            "textSize": {"expr": {"Literal": {"Value": "10D"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Semibold'"}}}
                        }
                    }
                ]
            },
            "vcObjects": {
                "background": [
                    {
                        "properties": {
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                            "radius": {"expr": {"Literal": {"Value": "8D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }


def make_kpi_card_visual(name, x, y, w, h, z=300, measure_name="Total Revenue EGP", card_title="Gross Revenue"):
    query_ref = "_Measures.{0}".format(measure_name)
    title_val = "'{0}'".format(card_title)
    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Values": [{"queryRef": query_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "m", "Entity": "_Measures", "Type": 0}],
                "Select": [
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": measure_name
                        },
                        "Name": query_ref
                    }
                ]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "labels": [
                    {
                        "properties": {
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "22D"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Bold'"}}}
                        }
                    }
                ],
                "categoryLabels": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "false"}}}
                        }
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": title_val}}},
                            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#64748B'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "10D"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Semibold'"}}},
                            "alignment": {"expr": {"Literal": {"Value": "'Center'"}}}
                        }
                    }
                ],
                "background": [
                    {
                        "properties": {
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                            "radius": {"expr": {"Literal": {"Value": "8D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }


def make_line_area_chart(name, x, y, w, h, z=300, title_text="Gross Revenue and Market Share"):
    title_val = "'{0}'".format(title_text)
    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "lineChart",
            "projections": {
                "Category": [{"queryRef": "dim_date.Month", "active": True}],
                "Y": [{"queryRef": "_Measures.Total Revenue EGP"}],
                "Y2": [{"queryRef": "_Measures.IMS Market Share Pct"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "d", "Entity": "dim_date", "Type": 0},
                    {"Name": "m", "Entity": "_Measures", "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "d"}},
                            "Property": "Month"
                        },
                        "Name": "dim_date.Month"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "Total Revenue EGP"
                        },
                        "Name": "_Measures.Total Revenue EGP"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "IMS Market Share Pct"
                        },
                        "Name": "_Measures.IMS Market Share Pct"
                    }
                ]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "lineStyles": [
                    {
                        "properties": {
                            "shadeArea": {"expr": {"Literal": {"Value": "true"}}},
                            "strokeWidth": {"expr": {"Literal": {"Value": "3D"}}}
                        }
                    }
                ],
                "dataPoint": [
                    {
                        "properties": {
                            "fill": {"solid": {"color": {"expr": {"Literal": {"Value": "'#00C2FF'"}}}}}
                        },
                        "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": title_val}}},
                            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0A2540'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Semibold'"}}}
                        }
                    }
                ],
                "background": [
                    {
                        "properties": {
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                            "radius": {"expr": {"Literal": {"Value": "8D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }


def make_map_visual(name, x, y, w, h, z=300, title_text="Top Performing Cairo Bricks (Spatial Distribution)"):
    title_val = "'{0}'".format(title_text)
    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "shapeMap",
            "projections": {
                "Category": [{"queryRef": "dim_brick_territory.Brick_Name", "active": True}],
                "ColorSaturation": [{"queryRef": "_Measures.Total Revenue EGP"}],
                "Tooltips": [
                    {"queryRef": "dim_brick_territory.Zone"},
                    {"queryRef": "dim_brick_territory.Tier"},
                    {"queryRef": "_Measures.Total Revenue EGP"},
                    {"queryRef": "_Measures.IMS Market Share Pct"},
                    {"queryRef": "_Measures.Evolution Index EI"},
                    {"queryRef": "_Measures.Target Attainment Pct"}
                ]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "b", "Entity": "dim_brick_territory", "Type": 0},
                    {"Name": "m", "Entity": "_Measures", "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "b"}},
                            "Property": "Brick_Name"
                        },
                        "Name": "dim_brick_territory.Brick_Name"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "Total Revenue EGP"
                        },
                        "Name": "_Measures.Total Revenue EGP"
                    },
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "b"}},
                            "Property": "Zone"
                        },
                        "Name": "dim_brick_territory.Zone"
                    },
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "b"}},
                            "Property": "Tier"
                        },
                        "Name": "dim_brick_territory.Tier"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "IMS Market Share Pct"
                        },
                        "Name": "_Measures.IMS Market Share Pct"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "Evolution Index EI"
                        },
                        "Name": "_Measures.Evolution Index EI"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "Target Attainment Pct"
                        },
                        "Name": "_Measures.Target Attainment Pct"
                    }
                ]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "shape": [
                    {
                        "properties": {
                            "map": {
                                "type": {"expr": {"Literal": {"Value": "'custom'"}}},
                                "name": {"expr": {"Literal": {"Value": "'cairo_commercial_bricks'"}}}
                            },
                            "projection": {"expr": {"Literal": {"Value": "'mercator'"}}}
                        }
                    }
                ],
                "dataLabels": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0A2540'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "8D"}}}
                        }
                    }
                ],
                "dataPoint": [
                    {
                        "properties": {
                            "fillMin": {"solid": {"color": {"expr": {"Literal": {"Value": "'#EF4444'"}}}}},
                            "fillMid": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                            "fillMax": {"solid": {"color": {"expr": {"Literal": {"Value": "'#00A3E0'"}}}}}
                        }
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": title_val}}},
                            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0A2540'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "11D"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Semibold'"}}}
                        }
                    }
                ],
                "background": [
                    {
                        "properties": {
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                            "radius": {"expr": {"Literal": {"Value": "8D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }



def make_bar_chart(name, x, y, w, h, z=300, title_text="Cairo Briking Cairo Brick"):
    title_val = "'{0}'".format(title_text)
    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "clusteredBarChart",
            "projections": {
                "Category": [{"queryRef": "dim_brick_territory.Brick_Name", "active": True}],
                "Y": [{"queryRef": "_Measures.IMS Market Share Pct"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "b", "Entity": "dim_brick_territory", "Type": 0},
                    {"Name": "m", "Entity": "_Measures", "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "b"}},
                            "Property": "Brick_Name"
                        },
                        "Name": "dim_brick_territory.Brick_Name"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "IMS Market Share Pct"
                        },
                        "Name": "_Measures.IMS Market Share Pct"
                    }
                ]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "labels": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "9D"}}}
                        }
                    }
                ],
                "dataPoint": [
                    {
                        "properties": {
                            "fill": {"solid": {"color": {"expr": {"Literal": {"Value": "'#00A3E0'"}}}}}
                        }
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": title_val}}},
                            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0A2540'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "11D"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Semibold'"}}}
                        }
                    }
                ],
                "background": [
                    {
                        "properties": {
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                            "radius": {"expr": {"Literal": {"Value": "8D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }


def make_column_chart(name, x, y, w, h, z=300, title_text="Distributor Market Share"):
    title_val = "'{0}'".format(title_text)
    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "clusteredColumnChart",
            "projections": {
                "Category": [{"queryRef": "dim_distributor.Distributor_Name", "active": True}],
                "Y": [{"queryRef": "_Measures.IMS Market Share Pct"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "d", "Entity": "dim_distributor", "Type": 0},
                    {"Name": "m", "Entity": "_Measures", "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "d"}},
                            "Property": "Distributor_Name"
                        },
                        "Name": "dim_distributor.Distributor_Name"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "IMS Market Share Pct"
                        },
                        "Name": "_Measures.IMS Market Share Pct"
                    }
                ]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "labels": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "9D"}}}
                        }
                    }
                ],
                "dataPoint": [
                    {
                        "properties": {
                            "fill": {"solid": {"color": {"expr": {"Literal": {"Value": "'#00A3E0'"}}}}}
                        }
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": title_val}}},
                            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0A2540'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "11D"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Semibold'"}}}
                        }
                    }
                ],
                "background": [
                    {
                        "properties": {
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                            "radius": {"expr": {"Literal": {"Value": "8D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }


def make_combo_chart(name, x, y, w, h, z=300, title_text="Call Attainment Tier Segmentation"):
    title_val = "'{0}'".format(title_text)
    cfg = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "z": z, "width": w, "height": h}
            }
        ],
        "singleVisual": {
            "visualType": "lineClusteredColumnComboChart",
            "projections": {
                "Category": [{"queryRef": "dim_doctor.Classification", "active": True}],
                "Y": [{"queryRef": "_Measures.Total Field Visits"}],
                "Y2": [{"queryRef": "_Measures.Plan Adherence Pct"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "doc", "Entity": "dim_doctor", "Type": 0},
                    {"Name": "m", "Entity": "_Measures", "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "doc"}},
                            "Property": "Classification"
                        },
                        "Name": "dim_doctor.Classification"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "Total Field Visits"
                        },
                        "Name": "_Measures.Total Field Visits"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": "Plan Adherence Pct"
                        },
                        "Name": "_Measures.Plan Adherence Pct"
                    }
                ]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "dataPoint": [
                    {
                        "properties": {
                            "fill": {"solid": {"color": {"expr": {"Literal": {"Value": "'#00B4D8'"}}}}}
                        }
                    }
                ],
                "lineStyles": [
                    {
                        "properties": {
                            "strokeWidth": {"expr": {"Literal": {"Value": "3D"}}}
                        }
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": title_val}}},
                            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0A2540'"}}}}},
                            "fontSize": {"expr": {"Literal": {"Value": "11D"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Semibold'"}}}
                        }
                    }
                ],
                "background": [
                    {
                        "properties": {
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                            "radius": {"expr": {"Literal": {"Value": "8D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "width": float(w),
        "height": float(h),
        "filters": "[]",
        "config": json.dumps(cfg, separators=(',', ':'))
    }


def main():
    print(">>> Generating Tailored Visuals for Executive Overview...")
    visuals = []

    # 1. Left Navigation Sidebar Background
    visuals.append(make_shape_visual("Nav_Sidebar_Bg", 0, 0, 205, 720, z=0, fill_color="#071E54", border_color="#071E54"))

    # 2. Sidebar Header Brand / Logo
    visuals.append(make_text_visual("Nav_Brand_Logo", 10, 16, 185, 55, z=100, text=u"\u2695 PharmaForce 360\u00b0", color="#FFFFFF", font_size="14pt", font_family="Segoe UI Bold"))

    # 3. Sidebar Menu: Active "Executive Overview" Pill
    visuals.append(make_shape_visual("Nav_Active_Pill", 10, 138, 185, 42, z=50, fill_color="#00A3E0", border_color="#00A3E0", round_radius=10))
    visuals.append(make_text_visual("Nav_Item_1_Active", 18, 145, 170, 32, z=100, text=u"\u229e  Executive Overview", color="#FFFFFF", font_size="11pt", font_family="Segoe UI Semibold"))

    # 4. Sidebar Inactive Menu Items
    menu_items = [
        (u"Doctors (KOLs)", 198),
        (u"Medical Representatives", 248),
        (u"Bricks", 298),
        (u"Visits", 348),
        (u"Drugs & Comparisons", 398),
        (u"Distributors & Stock", 448),
        (u"Expenses & Budget", 498)
    ]
    for idx, (label, y_pos) in enumerate(menu_items, start=2):
        visuals.append(make_text_visual("Nav_Item_{0}".format(idx), 18, y_pos, 175, 32, z=100, text=label, color="#CFE0F5", font_size="10pt"))

    # 5. Top Live Model Pill Badge
    visuals.append(make_text_visual("Badge_Live_Model", 520, 8, 260, 26, z=200, text=u"\u25cf Live Model: 24-Month Active Run", color="#007399", font_size="9.5pt", font_family="Segoe UI Semibold", bg_color="#E6F7FB", border_color="#89DAF4", border_radius=13))

    # 6. Top 4 Dropdown Slicers
    visuals.append(make_slicer_visual("Slicer_Line", 215, 38, 254, 44, z=200, table_name="dim_product", column_name="Therapeutic_Line", title_text="Line: Cardio-Metabolic"))
    visuals.append(make_slicer_visual("Slicer_Zone", 481, 38, 254, 44, z=200, table_name="dim_brick_territory", column_name="Zone", title_text="Zone: Greater Cairo"))
    visuals.append(make_slicer_visual("Slicer_Period", 747, 38, 254, 44, z=200, table_name="dim_date", column_name="Year", title_text="Period: 2025-2026"))
    visuals.append(make_slicer_visual("Slicer_Tier", 1013, 38, 257, 44, z=200, table_name="dim_doctor", column_name="Classification", title_text="Tier: Class A"))

    # 7. Row of 4 Modern KPI Cards + Colored Vertical Accent Strips
    # Card 1: Gross Revenue
    visuals.append(make_shape_visual("Accent_Kpi_1", 215, 88, 5, 88, z=350, fill_color="#00A3E0", border_color="#00A3E0"))
    visuals.append(make_kpi_card_visual("Card_Gross_Revenue", 215, 88, 254, 88, z=300, measure_name="Total Revenue EGP", card_title="Gross Revenue"))

    # Card 2: Market Share
    visuals.append(make_shape_visual("Accent_Kpi_2", 481, 88, 5, 88, z=350, fill_color="#00B4D8", border_color="#00B4D8"))
    visuals.append(make_kpi_card_visual("Card_Market_Share", 481, 88, 254, 88, z=300, measure_name="IMS Market Share Pct", card_title="Market Share"))

    # Card 3: Call Attainment
    visuals.append(make_shape_visual("Accent_Kpi_3", 747, 88, 5, 88, z=350, fill_color="#0070BA", border_color="#0070BA"))
    visuals.append(make_kpi_card_visual("Card_Call_Attainment", 747, 88, 254, 88, z=300, measure_name="Plan Adherence Pct", card_title="Call Attainment"))

    # Card 4: High-Risk KOLs
    visuals.append(make_shape_visual("Accent_Kpi_4", 1013, 88, 5, 88, z=350, fill_color="#00A3E0", border_color="#00A3E0"))
    visuals.append(make_kpi_card_visual("Card_High_Risk_KOLs", 1013, 88, 257, 88, z=300, measure_name="High Churn Risk Doctor Count", card_title="High-Risk KOLs"))

    # 8. Middle Row:
    # Left: Gross Revenue and Market Share Wave Chart
    visuals.append(make_line_area_chart("Chart_Revenue_MarketShare", 215, 184, 670, 250, z=300, title_text="Gross Revenue and Market Share"))

    # Right: Spatial Map of Cairo Bricks
    visuals.append(make_map_visual("Chart_Spatial_Map", 897, 184, 373, 250, z=300, title_text="Top Performing Cairo Bricks (Spatial Distribution)"))

    # 9. Bottom Row:
    # Chart 1: Cairo Brick Ranking Horizontal Bars
    visuals.append(make_bar_chart("Chart_Brick_Ranking", 215, 442, 340, 266, z=300, title_text="Cairo Briking Cairo Brick"))

    # Chart 2: Distributor Market Share Vertical Columns
    visuals.append(make_column_chart("Chart_Distributor_Share", 567, 442, 300, 266, z=300, title_text="Distributor Market Share"))

    # Chart 3: Call Attainment Tier Segmentation Combo
    visuals.append(make_combo_chart("Chart_Attainment_Tier", 879, 442, 391, 266, z=300, title_text="Call Attainment Tier Segmentation"))

    print("Compiled {0} visual containers for Executive Overview.".format(len(visuals)))

    # Load existing report.json
    with codecs.open(REPORT_JSON_PATH, "r", "utf-8") as f:
        report_data = json.load(f)

    exec_section = {
        "name": "Section_Executive_Overview",
        "displayName": "Executive Overview",
        "ordinal": 0,
        "displayOption": 0,
        "width": 1280.00,
        "height": 720.00,
        "config": "{}",
        "filters": "[]",
        "visualContainers": visuals
    }

    # Keep all other detailed persona pages and update their ordinals
    existing_sections = [s for s in report_data.get("sections", []) if s.get("name") not in ("7c530dfe2e5f210efc7a", "85f5414383a50c8df334", "Section_Executive_Overview", "Section_ExecOverview")]

    final_sections = [exec_section]
    cur_ord = 1
    for sec in existing_sections:
        sec["ordinal"] = cur_ord
        cur_ord += 1
        final_sections.append(sec)

    report_data["sections"] = final_sections
    report_data["activeSectionIndex"] = 0

    # Write out UTF-8 without BOM
    with codecs.open(REPORT_JSON_PATH, "w", "utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(">>> Successfully updated report.json! Page 1 is now the high-fidelity Executive Overview!")

if __name__ == "__main__":
    main()

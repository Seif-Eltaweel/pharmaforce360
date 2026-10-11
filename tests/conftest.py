"""
pytest configuration and fixtures for PharmaForce 360° test suite.
"""

import pytest
from pathlib import Path
from tests.helpers import (
    load_report_model,
    load_theme_model,
    PATH_REPORT_JSON,
    PATH_THEME_ROOT,
    PATH_THEME_REGISTERED,
    DIR_REGISTERED_RESOURCES,
    DIR_DATA_ASSETS_NAV,
    ReportModel,
    ThemeModel,
)


@pytest.fixture(scope="session")
def report_model() -> ReportModel:
    """Fixture providing parsed ReportModel from powerbi/PharmaForce360.Report/report.json."""
    return load_report_model(PATH_REPORT_JSON)


@pytest.fixture(scope="session")
def root_theme() -> ThemeModel:
    """Fixture providing parsed ThemeModel from powerbi/theme.json."""
    return load_theme_model(PATH_THEME_ROOT)


@pytest.fixture(scope="session")
def registered_theme() -> ThemeModel:
    """Fixture providing parsed ThemeModel from StaticResources/.../PharmaForce360Theme.json."""
    return load_theme_model(PATH_THEME_REGISTERED)


@pytest.fixture(scope="session")
def static_registered_svgs() -> list[str]:
    """Fixture listing all SVG assets physically present in RegisteredResources."""
    if not DIR_REGISTERED_RESOURCES.exists():
        return []
    return [p.name for p in DIR_REGISTERED_RESOURCES.glob("*.svg")]


@pytest.fixture(scope="session")
def data_assets_svgs() -> list[str]:
    """Fixture listing all SVG assets physically present in data/assets/navigation."""
    if not DIR_DATA_ASSETS_NAV.exists():
        return []
    return [p.name for p in DIR_DATA_ASSETS_NAV.glob("*.svg")]

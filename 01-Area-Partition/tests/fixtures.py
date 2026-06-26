"""Test fixtures and common test utilities for SheetCuts tests."""

import pytest
from sheetcuts.models import CuttingPiece, Sheet, SheetLayout, Placement


@pytest.fixture
def simple_sheet() -> Sheet:
    """Standard sheet: 48 × 96 inches, homogenous."""
    return Sheet(48, 96, "inches", "homogenous")


@pytest.fixture
def directional_sheet() -> Sheet:
    """Directional sheet with feature running along width."""
    return Sheet(48, 96, "inches", "directional")


@pytest.fixture
def metric_sheet() -> Sheet:
    """Metric sheet: 1200 × 2400 mm."""
    return Sheet(1200, 2400, "millimeters", "homogenous")


@pytest.fixture
def simple_pieces() -> list[CuttingPiece]:
    """Standard test pieces: Panel, Shelf x3."""
    return [
        CuttingPiece(10, 20, "Panel", 1),
        CuttingPiece(12, 18, "Shelf", 3),
    ]


@pytest.fixture
def single_piece() -> list[CuttingPiece]:
    """Single test piece."""
    return [CuttingPiece(10, 20, "SinglePiece", 1)]


@pytest.fixture
def empty_pieces() -> list[CuttingPiece]:
    """Empty list of pieces (edge case)."""
    return []


@pytest.fixture
def oversized_piece() -> list[CuttingPiece]:
    """Piece larger than standard sheet (error case)."""
    return [CuttingPiece(60, 100, "TooLarge", 1)]


@pytest.fixture
def sample_layout(simple_sheet: Sheet) -> SheetLayout:
    """Sample sheet layout with two placements."""
    pieces = [
        CuttingPiece(10, 20, "Panel", 1),
        CuttingPiece(12, 18, "Shelf", 1),
    ]
    placements = [
        Placement(pieces[0], x=0, y=0, width=10, height=20, rotated=False),
        Placement(pieces[1], x=10, y=0, width=12, height=18, rotated=False),
    ]
    return SheetLayout(sheet_id=1, sheet=simple_sheet, placements=placements)

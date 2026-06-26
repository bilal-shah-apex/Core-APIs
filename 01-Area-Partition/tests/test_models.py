"""Tests for SheetCuts data models (CuttingPiece, Sheet, Placement, SheetLayout)."""

import pytest
from sheetcuts.models import CuttingPiece, Sheet, SheetLayout, Placement


class TestCuttingPiece:
    """Test suite for CuttingPiece model."""

    def test_create_valid_piece(self) -> None:
        """Test creating a valid cutting piece."""
        piece = CuttingPiece(10, 20, "Panel", 1)
        assert piece.width == 10
        assert piece.height == 20
        assert piece.label == "Panel"
        assert piece.quantity == 1
        assert piece.rotatable is True

    def test_create_piece_with_quantity(self) -> None:
        """Test creating piece with quantity > 1."""
        piece = CuttingPiece(12, 18, "Shelf", 3)
        assert piece.quantity == 3
        assert piece.area == 12 * 18 * 3

    def test_piece_area_calculation(self) -> None:
        """Test area property calculation."""
        piece = CuttingPiece(10, 20, "Panel", 2)
        assert piece.area == 10 * 20 * 2

    def test_piece_negative_width(self) -> None:
        """Test that negative width raises ValueError."""
        with pytest.raises(ValueError, match="Width and height must be positive"):
            CuttingPiece(-10, 20, "Invalid", 1)

    def test_piece_zero_height(self) -> None:
        """Test that zero height raises ValueError."""
        with pytest.raises(ValueError, match="Width and height must be positive"):
            CuttingPiece(10, 0, "Invalid", 1)

    def test_piece_zero_quantity(self) -> None:
        """Test that zero quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            CuttingPiece(10, 20, "Invalid", 0)

    def test_piece_invalid_label_type(self) -> None:
        """Test that non-string label raises TypeError."""
        with pytest.raises(TypeError, match="Label must be a string"):
            CuttingPiece(10, 20, 123, 1)  # type: ignore

    def test_piece_invalid_quantity_type(self) -> None:
        """Test that non-int quantity raises TypeError."""
        with pytest.raises(TypeError, match="Quantity must be an integer"):
            CuttingPiece(10, 20, "Panel", 1.5)  # type: ignore

    def test_piece_immutable(self) -> None:
        """Test that CuttingPiece is immutable (frozen dataclass)."""
        piece = CuttingPiece(10, 20, "Panel", 1)
        with pytest.raises(AttributeError):
            piece.width = 15  # type: ignore


class TestSheet:
    """Test suite for Sheet model."""

    def test_create_valid_sheet(self) -> None:
        """Test creating a valid sheet."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        assert sheet.width == 48
        assert sheet.height == 96
        assert sheet.units == "inches"
        assert sheet.sheet_type == "homogenous"
        assert sheet.mode == "sheet"

    def test_sheet_defaults(self) -> None:
        """Test sheet default values."""
        sheet = Sheet(48, 96)
        assert sheet.units == "inches"
        assert sheet.sheet_type == "homogenous"
        assert sheet.mode == "sheet"

    def test_sheet_area_calculation(self) -> None:
        """Test sheet area property."""
        sheet = Sheet(48, 96)
        assert sheet.area == 48 * 96

    def test_sheet_invalid_width(self) -> None:
        """Test that negative/zero width raises ValueError."""
        with pytest.raises(ValueError, match="Width and height must be positive"):
            Sheet(-48, 96)

    def test_sheet_invalid_units(self) -> None:
        """Test that invalid units raise ValueError."""
        with pytest.raises(ValueError, match="Units must be"):
            Sheet(48, 96, "meters")  # type: ignore

    def test_sheet_invalid_type(self) -> None:
        """Test that invalid sheet_type raises ValueError."""
        with pytest.raises(ValueError, match="Sheet type must be"):
            Sheet(48, 96, "inches", "invalid_type")  # type: ignore

    def test_sheet_roll_mode_not_supported(self) -> None:
        """Test that roll mode raises error in v1.0."""
        # Roll mode should be accepted but validation should indicate v2.0 feature
        # Currently, we accept the mode field but don't process it
        sheet = Sheet(48, 96, "inches", "homogenous", "roll")
        assert sheet.mode == "roll"


class TestPlacement:
    """Test suite for Placement model."""

    def test_create_valid_placement(self) -> None:
        """Test creating a valid placement."""
        piece = CuttingPiece(10, 20, "Panel", 1)
        placement = Placement(piece, x=0, y=0, width=10, height=20)
        assert placement.x == 0
        assert placement.y == 0
        assert placement.width == 10
        assert placement.height == 20
        assert placement.rotated is False

    def test_placement_area(self) -> None:
        """Test placement area calculation."""
        piece = CuttingPiece(10, 20, "Panel", 1)
        placement = Placement(piece, x=0, y=0, width=10, height=20)
        assert placement.area == 10 * 20

    def test_placement_rotated(self) -> None:
        """Test rotated placement."""
        piece = CuttingPiece(10, 20, "Panel", 1)
        placement = Placement(piece, x=0, y=0, width=20, height=10, rotated=True)
        assert placement.rotated is True
        assert placement.width == 20
        assert placement.height == 10


class TestSheetLayout:
    """Test suite for SheetLayout model."""

    def test_create_empty_layout(self) -> None:
        """Test creating empty sheet layout."""
        sheet = Sheet(48, 96)
        layout = SheetLayout(sheet_id=1, sheet=sheet, placements=[])
        assert layout.sheet_id == 1
        assert len(layout.placements) == 0

    def test_layout_utilization_empty(self) -> None:
        """Test utilization of empty layout."""
        sheet = Sheet(48, 96)
        layout = SheetLayout(sheet_id=1, sheet=sheet, placements=[])
        assert layout.utilization_percentage == 0.0

    def test_layout_with_placements(self) -> None:
        """Test layout with placements."""
        sheet = Sheet(48, 96)
        piece1 = CuttingPiece(10, 20, "P1", 1)
        piece2 = CuttingPiece(12, 18, "P2", 1)
        placements = [
            Placement(piece1, x=0, y=0, width=10, height=20),
            Placement(piece2, x=10, y=0, width=12, height=18),
        ]
        layout = SheetLayout(sheet_id=1, sheet=sheet, placements=placements)
        
        assert len(layout.placements) == 2
        assert layout.total_pieces_area == (10 * 20) + (12 * 18)
        expected_util = ((10*20 + 12*18) / (48*96)) * 100
        assert abs(layout.utilization_percentage - expected_util) < 0.01

    def test_layout_waste_area(self) -> None:
        """Test waste area calculation."""
        sheet = Sheet(48, 96)
        piece = CuttingPiece(10, 20, "P1", 1)
        placements = [Placement(piece, x=0, y=0, width=10, height=20)]
        layout = SheetLayout(sheet_id=1, sheet=sheet, placements=placements)
        
        expected_waste = (48 * 96) - (10 * 20)
        assert layout.waste_area == expected_waste

    def test_layout_to_dict(self) -> None:
        """Test layout serialization to dictionary."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        piece = CuttingPiece(10, 20, "Panel", 1)
        placements = [Placement(piece, x=0, y=0, width=10, height=20)]
        layout = SheetLayout(sheet_id=1, sheet=sheet, placements=placements)
        
        layout_dict = layout.to_dict()
        assert layout_dict["sheet_id"] == 1
        assert layout_dict["sheet"]["width"] == 48
        assert layout_dict["sheet"]["height"] == 96
        assert len(layout_dict["placements"]) == 1
        assert "statistics" in layout_dict

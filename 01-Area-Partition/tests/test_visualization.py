"""Tests for visualization module."""

import pytest
from sheetcuts.models import CuttingPiece, Sheet, SheetLayout, Placement
from sheetcuts.visualization import generate_html_diagram


class TestGenerateHtmlDiagram:
    """Test suite for HTML diagram generation."""

    def test_generate_diagram_with_layout(self) -> None:
        """Test generating diagram with valid layout."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        piece = CuttingPiece(10, 20, "Panel", 1)
        placement = Placement(piece, x=0, y=0, width=10, height=20)
        layouts = [SheetLayout(sheet_id=1, sheet=sheet, placements=[placement])]
        
        html = generate_html_diagram(layouts, sheet)
        
        assert isinstance(html, str)
        assert len(html) > 0
        assert "<!DOCTYPE html>" in html
        assert "svg" in html.lower()

    def test_generate_diagram_includes_labels(self) -> None:
        """Test that diagram includes piece labels."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        piece = CuttingPiece(10, 20, "TestPanel", 1)
        placement = Placement(piece, x=0, y=0, width=10, height=20)
        layouts = [SheetLayout(sheet_id=1, sheet=sheet, placements=[placement])]
        
        html = generate_html_diagram(layouts, sheet)
        
        assert "TestPanel" in html

    def test_generate_diagram_includes_dimensions(self) -> None:
        """Test that diagram includes sheet dimensions."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        piece = CuttingPiece(10, 20, "Panel", 1)
        placement = Placement(piece, x=0, y=0, width=10, height=20)
        layouts = [SheetLayout(sheet_id=1, sheet=sheet, placements=[placement])]
        
        html = generate_html_diagram(layouts, sheet)
        
        assert "48" in html
        assert "96" in html

    def test_generate_diagram_includes_units(self) -> None:
        """Test that diagram includes unit system."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        piece = CuttingPiece(10, 20, "Panel", 1)
        placement = Placement(piece, x=0, y=0, width=10, height=20)
        layouts = [SheetLayout(sheet_id=1, sheet=sheet, placements=[placement])]
        
        html = generate_html_diagram(layouts, sheet)
        
        assert "inches" in html.lower()

    def test_generate_diagram_empty_layouts_raises_error(self) -> None:
        """Test that empty layouts raises ValueError."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        
        with pytest.raises(ValueError, match="empty"):
            generate_html_diagram([], sheet)

    def test_generate_diagram_invalid_layouts_type(self) -> None:
        """Test that invalid layouts type raises TypeError."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        
        with pytest.raises(TypeError, match="layouts"):
            generate_html_diagram("invalid", sheet)  # type: ignore

    def test_generate_diagram_invalid_sheet_type(self) -> None:
        """Test that invalid sheet type raises TypeError."""
        piece = CuttingPiece(10, 20, "Panel", 1)
        sheet_obj = Sheet(48, 96, "inches", "homogenous")
        placement = Placement(piece, x=0, y=0, width=10, height=20)
        layouts = [SheetLayout(sheet_id=1, sheet=sheet_obj, placements=[placement])]
        
        with pytest.raises(TypeError, match="Sheet"):
            generate_html_diagram(layouts, "invalid")  # type: ignore

    def test_generate_diagram_multiple_sheets(self) -> None:
        """Test generating diagram with multiple sheets."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        piece1 = CuttingPiece(10, 20, "Panel1", 1)
        piece2 = CuttingPiece(12, 18, "Panel2", 1)
        
        layouts = [
            SheetLayout(sheet_id=1, sheet=sheet, placements=[
                Placement(piece1, x=0, y=0, width=10, height=20)
            ]),
            SheetLayout(sheet_id=2, sheet=sheet, placements=[
                Placement(piece2, x=0, y=0, width=12, height=18)
            ]),
        ]
        
        html = generate_html_diagram(layouts, sheet)
        
        assert "Sheet 1" in html
        assert "Sheet 2" in html

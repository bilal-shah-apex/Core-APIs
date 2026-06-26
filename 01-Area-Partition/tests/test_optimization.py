"""Tests for optimization engine."""

import pytest
from sheetcuts.models import CuttingPiece, Sheet
from sheetcuts.optimization import optimize_sheet_layout


class TestOptimizeSheetLayout:
    """Test suite for optimization engine."""

    def test_optimize_simple_layout(self) -> None:
        """Test optimization with simple pieces."""
        pieces = [CuttingPiece(10, 20, "Panel", 1)]
        sheet = Sheet(48, 96, "inches", "homogenous")
        
        layouts = optimize_sheet_layout(pieces, sheet)
        
        assert len(layouts) >= 1
        assert layouts[0].sheet_id == 1

    def test_optimize_empty_pieces(self) -> None:
        """Test optimization with empty pieces list."""
        pieces: list[CuttingPiece] = []
        sheet = Sheet(48, 96, "inches", "homogenous")
        
        layouts = optimize_sheet_layout(pieces, sheet)
        
        assert len(layouts) == 0

    def test_optimize_oversized_piece(self) -> None:
        """Test that oversized pieces raise ValueError."""
        pieces = [CuttingPiece(100, 20, "TooWide", 1)]
        sheet = Sheet(48, 96, "inches", "homogenous")
        
        with pytest.raises(ValueError, match="exceeds sheet"):
            optimize_sheet_layout(pieces, sheet)

    def test_optimize_invalid_sheet_type(self) -> None:
        """Test that invalid sheet raises TypeError."""
        pieces = [CuttingPiece(10, 20, "Panel", 1)]
        
        with pytest.raises(TypeError, match="Sheet"):
            optimize_sheet_layout(pieces, "invalid")  # type: ignore

    def test_optimize_invalid_pieces_type(self) -> None:
        """Test that invalid pieces type raises TypeError."""
        sheet = Sheet(48, 96, "inches", "homogenous")
        
        with pytest.raises(TypeError, match="pieces"):
            optimize_sheet_layout("invalid", sheet)  # type: ignore

    def test_optimize_unsupported_algorithm(self) -> None:
        """Test that unsupported algorithm raises NotImplementedError."""
        pieces = [CuttingPiece(10, 20, "Panel", 1)]
        sheet = Sheet(48, 96, "inches", "homogenous")
        
        with pytest.raises(NotImplementedError, match="algorithm"):
            optimize_sheet_layout(pieces, sheet, algorithm="unknown")

    def test_optimize_returns_sheet_layouts(self) -> None:
        """Test that result contains SheetLayout objects."""
        from sheetcuts.models import SheetLayout
        
        pieces = [CuttingPiece(10, 20, "Panel", 1)]
        sheet = Sheet(48, 96, "inches", "homogenous")
        
        layouts = optimize_sheet_layout(pieces, sheet)
        
        assert len(layouts) > 0
        assert all(isinstance(l, SheetLayout) for l in layouts)

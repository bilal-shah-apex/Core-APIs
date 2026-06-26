"""Tests for input validation."""

import pytest
from sheetcuts.validators import validate_input, validate_sheet, validate_cutting_piece


class TestValidateSheet:
    """Test suite for sheet validation."""

    def test_validate_valid_sheet(self) -> None:
        """Test validation of valid sheet data."""
        sheet_data = {"width": 48, "height": 96}
        is_valid, error = validate_sheet(sheet_data)
        assert is_valid is True
        assert error == ""

    def test_validate_sheet_with_units(self) -> None:
        """Test validation with units specified."""
        sheet_data = {"width": 48, "height": 96, "units": "inches"}
        is_valid, error = validate_sheet(sheet_data)
        assert is_valid is True

    def test_validate_sheet_missing_width(self) -> None:
        """Test validation fails when width is missing."""
        sheet_data = {"height": 96}
        is_valid, error = validate_sheet(sheet_data)
        assert is_valid is False
        assert "width" in error.lower()

    def test_validate_sheet_zero_width(self) -> None:
        """Test validation fails for zero width."""
        sheet_data = {"width": 0, "height": 96}
        is_valid, error = validate_sheet(sheet_data)
        assert is_valid is False
        assert "positive" in error.lower()

    def test_validate_sheet_invalid_units(self) -> None:
        """Test validation fails for invalid units."""
        sheet_data = {"width": 48, "height": 96, "units": "feet"}
        is_valid, error = validate_sheet(sheet_data)
        assert is_valid is False

    def test_validate_sheet_invalid_type(self) -> None:
        """Test validation fails for invalid sheet type."""
        sheet_data = {"width": 48, "height": 96, "type": "invalid"}
        is_valid, error = validate_sheet(sheet_data)
        assert is_valid is False

    def test_validate_sheet_roll_mode_unsupported(self) -> None:
        """Test validation indicates roll mode not supported in v1.0."""
        sheet_data = {"width": 48, "height": 96, "mode": "roll"}
        is_valid, error = validate_sheet(sheet_data)
        assert is_valid is False
        assert "v1.0" in error.lower() or "not supported" in error.lower()


class TestValidateCuttingPiece:
    """Test suite for cutting piece validation."""

    def test_validate_valid_piece(self) -> None:
        """Test validation of valid piece data."""
        piece_data = {"width": 10, "height": 20}
        is_valid, error = validate_cutting_piece(piece_data)
        assert is_valid is True
        assert error == ""

    def test_validate_piece_with_label(self) -> None:
        """Test validation with label specified."""
        piece_data = {"width": 10, "height": 20, "label": "Panel"}
        is_valid, error = validate_cutting_piece(piece_data)
        assert is_valid is True

    def test_validate_piece_with_quantity(self) -> None:
        """Test validation with quantity specified."""
        piece_data = {"width": 10, "height": 20, "quantity": 3}
        is_valid, error = validate_cutting_piece(piece_data)
        assert is_valid is True

    def test_validate_piece_missing_width(self) -> None:
        """Test validation fails when width is missing."""
        piece_data = {"height": 20}
        is_valid, error = validate_cutting_piece(piece_data)
        assert is_valid is False

    def test_validate_piece_zero_height(self) -> None:
        """Test validation fails for zero height."""
        piece_data = {"width": 10, "height": 0}
        is_valid, error = validate_cutting_piece(piece_data)
        assert is_valid is False

    def test_validate_piece_invalid_label_type(self) -> None:
        """Test validation fails for non-string label."""
        piece_data = {"width": 10, "height": 20, "label": 123}
        is_valid, error = validate_cutting_piece(piece_data)
        assert is_valid is False

    def test_validate_piece_zero_quantity(self) -> None:
        """Test validation fails for zero quantity."""
        piece_data = {"width": 10, "height": 20, "quantity": 0}
        is_valid, error = validate_cutting_piece(piece_data)
        assert is_valid is False


class TestValidateInput:
    """Test suite for complete input validation."""

    def test_validate_valid_input(self) -> None:
        """Test validation of complete valid input."""
        data = {
            "sheet": {"width": 48, "height": 96},
            "cutting_pieces": [{"width": 10, "height": 20, "label": "Panel"}],
        }
        is_valid, error = validate_input(data)
        assert is_valid is True
        assert error == ""

    def test_validate_input_missing_sheet(self) -> None:
        """Test validation fails when sheet is missing."""
        data = {"cutting_pieces": [{"width": 10, "height": 20}]}
        is_valid, error = validate_input(data)
        assert is_valid is False
        assert "sheet" in error.lower()

    def test_validate_input_empty_pieces_list(self) -> None:
        """Test validation succeeds with empty pieces list."""
        data = {"sheet": {"width": 48, "height": 96}, "cutting_pieces": []}
        is_valid, error = validate_input(data)
        assert is_valid is True

    def test_validate_input_invalid_piece(self) -> None:
        """Test validation fails for invalid piece."""
        data = {
            "sheet": {"width": 48, "height": 96},
            "cutting_pieces": [{"width": -10, "height": 20}],
        }
        is_valid, error = validate_input(data)
        assert is_valid is False

    def test_validate_input_not_dict(self) -> None:
        """Test validation fails when input is not a dictionary."""
        is_valid, error = validate_input([])  # type: ignore
        assert is_valid is False

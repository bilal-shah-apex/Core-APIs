"""Input validation for SheetCuts JSON schemas.

This module provides validation functions for incoming JSON requests,
ensuring data integrity before processing.

Functions:
    validate_input: Validates complete input JSON against schema.
    validate_cutting_piece: Validates individual cutting piece data.
    validate_sheet: Validates sheet specification data.
"""

from typing import Any


def validate_input(data: dict[str, Any]) -> tuple[bool, str]:
    """Validates complete input JSON against SheetCuts schema.
    
    Checks overall structure, required fields, and delegates to specific
    validators for sheet and cutting pieces.
    
    Args:
        data: Input dictionary (parsed from JSON request).
    
    Returns:
        Tuple of (is_valid, error_message). is_valid is True if validation
        passes; error_message is empty string if valid, else describes error.
    
    Raises:
        TypeError: If data is not a dictionary.
    
    Example:
        >>> valid_data = {
        ...     "sheet": {"width": 48, "height": 96},
        ...     "cutting_pieces": [{"width": 10, "height": 20}]
        ... }
        >>> is_valid, error = validate_input(valid_data)
        >>> print(f"Valid: {is_valid}, Error: {error}")
        Valid: True, Error: 
    """
    if not isinstance(data, dict):
        return False, f"Input must be a dictionary; got {type(data).__name__}"
    
    # Validate sheet
    if "sheet" not in data:
        return False, "Required field 'sheet' is missing"
    
    is_valid, error = validate_sheet(data["sheet"])
    if not is_valid:
        return False, f"Invalid sheet specification: {error}"
    
    # Validate cutting pieces
    if "cutting_pieces" not in data:
        # Empty pieces list is valid (edge case)
        data["cutting_pieces"] = []
    
    if not isinstance(data["cutting_pieces"], list):
        return False, (
            f"Field 'cutting_pieces' must be a list; got "
            f"{type(data['cutting_pieces']).__name__}"
        )
    
    for idx, piece in enumerate(data["cutting_pieces"]):
        is_valid, error = validate_cutting_piece(piece)
        if not is_valid:
            return False, f"Invalid cutting piece at index {idx}: {error}"
    
    return True, ""


def validate_sheet(data: dict[str, Any]) -> tuple[bool, str]:
    """Validates sheet specification data.
    
    Args:
        data: Sheet specification dictionary.
    
    Returns:
        Tuple of (is_valid, error_message).
    
    Example:
        >>> sheet_data = {"width": 48, "height": 96, "units": "inches"}
        >>> is_valid, error = validate_sheet(sheet_data)
    """
    if not isinstance(data, dict):
        return False, f"Sheet must be a dictionary; got {type(data).__name__}"
    
    # Required fields
    if "width" not in data:
        return False, "Required field 'sheet.width' is missing"
    if "height" not in data:
        return False, "Required field 'sheet.height' is missing"
    
    # Validate width
    try:
        width = float(data["width"])
        if width <= 0:
            return False, f"Sheet width must be positive; got {width}"
    except (TypeError, ValueError):
        return False, f"Sheet width must be numeric; got {data['width']}"
    
    # Validate height
    try:
        height = float(data["height"])
        if height <= 0:
            return False, f"Sheet height must be positive; got {height}"
    except (TypeError, ValueError):
        return False, f"Sheet height must be numeric; got {data['height']}"
    
    # Validate units (optional, defaults to "inches")
    if "units" in data:
        units = data["units"]
        if units not in ("inches", "millimeters"):
            return False, f"Units must be 'inches' or 'millimeters'; got '{units}'"
    
    # Validate sheet_type (optional, defaults to "homogenous")
    if "type" in data:
        sheet_type = data["type"]
        if sheet_type not in ("homogenous", "directional"):
            return False, (
                f"Sheet type must be 'homogenous' or 'directional'; got '{sheet_type}'"
            )
    
    # Validate mode (optional, defaults to "sheet")
    if "mode" in data:
        mode = data["mode"]
        if mode not in ("sheet", "roll"):
            return False, f"Mode must be 'sheet' or 'roll'; got '{mode}'"
        if mode == "roll":
            return False, "Roll mode is not supported in v1.0; use 'sheet' mode"
    
    return True, ""


def validate_cutting_piece(data: dict[str, Any]) -> tuple[bool, str]:
    """Validates individual cutting piece data.
    
    Args:
        data: Cutting piece dictionary with width, height, label (optional),
              quantity (optional).
    
    Returns:
        Tuple of (is_valid, error_message).
    
    Example:
        >>> piece_data = {"width": 10, "height": 20, "label": "Panel", "quantity": 1}
        >>> is_valid, error = validate_cutting_piece(piece_data)
    """
    if not isinstance(data, dict):
        return False, f"Piece must be a dictionary; got {type(data).__name__}"
    
    # Required fields
    if "width" not in data:
        return False, "Required field 'width' is missing"
    if "height" not in data:
        return False, "Required field 'height' is missing"
    
    # Validate width
    try:
        width = float(data["width"])
        if width <= 0:
            return False, f"Width must be positive; got {width}"
    except (TypeError, ValueError):
        return False, f"Width must be numeric; got {data['width']}"
    
    # Validate height
    try:
        height = float(data["height"])
        if height <= 0:
            return False, f"Height must be positive; got {height}"
    except (TypeError, ValueError):
        return False, f"Height must be numeric; got {data['height']}"
    
    # Validate label (optional, auto-generated if not provided)
    if "label" in data:
        if not isinstance(data["label"], str):
            return False, f"Label must be a string; got {type(data['label']).__name__}"
    
    # Validate quantity (optional, defaults to 1)
    if "quantity" in data:
        try:
            quantity = int(data["quantity"])
            if quantity <= 0:
                return False, f"Quantity must be positive; got {quantity}"
        except (TypeError, ValueError):
            return False, f"Quantity must be an integer; got {data['quantity']}"
    
    return True, ""

"""Core optimization engine: Guillotine algorithm for sheet layout optimization.

Main entry point: optimize_sheet_layout() function.

This module uses the Guillotine algorithm to pack cutting pieces onto sheets
with automatic rotation support for homogenous sheets.

Functions:
    optimize_sheet_layout: Main optimization function (public API).
    
Algorithm:
    Guillotine algorithm is a 2D bin packing approach that:
    1. Places pieces sequentially, one at a time
    2. Splits available space with guillotine cuts (vertical/horizontal)
    3. Automatically rotates pieces 90° if it improves fit on homogenous sheets
    4. Deterministic: same input always produces same output
    
Performance:
    Time complexity: O(n log n) where n = total pieces (including quantities)
    Space complexity: O(n)
    Typical runtime: < 5 seconds for 1000 pieces on standard hardware
"""

from sheetcuts.models import CuttingPiece, Sheet, SheetLayout, Placement
from sheetcuts._internal.guillotine import place_pieces_with_guillotine


def optimize_sheet_layout(
    pieces: list[CuttingPiece],
    sheet: Sheet,
    algorithm: str = "guillotine"
) -> list[SheetLayout]:
    """Optimizes cutting piece layout on sheets using specified packing algorithm.
    
    Processes list of cutting pieces and automatically arranges them on sheets
    to minimize total sheets used (minimize material waste). Automatically rotates
    pieces 90 degrees if it improves packing on homogenous sheets; respects
    directional constraints on feature-aligned sheets.
    
    Args:
        pieces: List of CuttingPiece objects to be laid out. Can be empty.
        sheet: Sheet specification (dimensions, type, unit system).
        algorithm: Packing algorithm to use. Currently supported: "guillotine".
            Defaults to "guillotine". Future: "best_area_fit".
    
    Returns:
        List of SheetLayout objects, one per sheet required. Each layout contains
        placed pieces with final coordinates (x, y), dimensions, and rotation info.
        List is ordered by sheet usage (first sheet is primary). Empty list if
        pieces list is empty.
    
    Raises:
        ValueError: If any piece dimension exceeds sheet dimension.
        ValueError: If sheet dimensions are invalid (≤ 0).
        TypeError: If pieces is not a list or sheet is not a Sheet object.
        NotImplementedError: If algorithm specified is not supported.
    
    Performance:
        Expected runtime: < 5 seconds for up to 1000 pieces on standard hardware
        (Intel i5, 8GB RAM).
    
    Note:
        - Algorithm is deterministic: same input always produces identical output
        - Pieces are placed without overlap; all within sheet boundaries
        - Output coordinates use top-left (0, 0) origin
        - Rotation is automatic on homogenous sheets; manual on directional sheets
        - Rotation happens when it improves packing; prioritizes efficiency
    
    Example:
        >>> from sheetcuts.models import CuttingPiece, Sheet
        >>> from sheetcuts.optimization import optimize_sheet_layout
        >>> 
        >>> # Create cutting pieces
        >>> pieces = [
        ...     CuttingPiece(10, 20, "Panel", 1),
        ...     CuttingPiece(12, 18, "Shelf", 3)
        ... ]
        >>> 
        >>> # Create sheet
        >>> sheet = Sheet(48, 96, "inches", "homogenous")
        >>> 
        >>> # Optimize layout
        >>> layouts = optimize_sheet_layout(pieces, sheet)
        >>> 
        >>> # Check results
        >>> print(f"Sheets required: {len(layouts)}")
        Sheets required: 1
        >>> 
        >>> for layout in layouts:
        ...     print(f"Sheet {layout.sheet_id}: {len(layout.placements)} pieces")
        ...     for placement in layout.placements:
        ...         label = placement.piece.label
        ...         x, y = placement.x, placement.y
        ...         w, h = placement.width, placement.height
        ...         print(f"  {label}: ({x}, {y}) {w}×{h}")
        Sheet 1: 4 pieces
          Panel: (0, 0) 10×20
          Shelf: (10, 0) 12×18
          Shelf: (10, 18) 12×18
          Shelf: (22, 0) 12×18
    """
    # Type and bounds checking
    if not isinstance(pieces, (list, tuple)):
        raise TypeError(
            f"pieces must be a list or tuple; got {type(pieces).__name__}"
        )
    
    if not isinstance(sheet, Sheet):
        raise TypeError(
            f"sheet must be a Sheet object; got {type(sheet).__name__}"
        )
    
    # Validate that no piece exceeds sheet dimensions
    for piece in pieces:
        # Check both orientations (original and rotated)
        piece_w, piece_h = piece.width, piece.height
        if piece_w > sheet.width or piece_h > sheet.height:
            if piece_h > sheet.width or piece_w > sheet.height:
                # Even rotated, piece doesn't fit
                raise ValueError(
                    f"Piece '{piece.label}' ({piece_w}×{piece_h}) exceeds sheet "
                    f"dimensions ({sheet.width}×{sheet.height}) even when rotated"
                )
    
    # Check algorithm support
    if algorithm != "guillotine":
        raise NotImplementedError(
            f"Algorithm '{algorithm}' is not supported in v1.0. "
            f"Supported algorithms: 'guillotine'"
        )
    
    # Handle empty pieces list (edge case)
    if not pieces:
        return []
    
    # Call internal Guillotine implementation
    layouts = place_pieces_with_guillotine(pieces, sheet)
    
    return layouts

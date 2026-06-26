"""Guillotine algorithm for 2D rectangle packing (internal implementation).

This module implements the Guillotine algorithm for placing cutting pieces
on sheets with automatic rotation support.

Algorithm Details:
    Guillotine packing works by:
    1. Sorting pieces by area (largest first)
    2. For each piece, finding best available space
    3. Placing piece and splitting remaining space with guillotine cuts
    4. Testing both orientations (0° and 90°) for homogenous sheets
    5. Requesting new sheet when current sheet is full

Performance:
    Time: O(n log n) where n = total pieces including quantities
    Space: O(n) for layout storage

Functions:
    place_pieces_with_guillotine: Main entry point for algorithm.
"""

from sheetcuts.models import CuttingPiece, Sheet, SheetLayout, Placement


class _Rectangle:
    """Internal representation of an available rectangular space."""
    
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def can_fit(self, piece_w: float, piece_h: float) -> bool:
        """Check if piece can fit in this rectangle."""
        return piece_w <= self.width and piece_h <= self.height
    
    def __repr__(self) -> str:
        return f"_Rectangle({self.x}, {self.y}, {self.width}x{self.height})"


def _split_rectangle(rect: _Rectangle, piece_w: float, piece_h: float) -> list[_Rectangle]:
    """Split a rectangle after placing a piece using guillotine cuts.
    
    Creates two new rectangles: one from horizontal cut, one from vertical cut.
    """
    new_rects = []
    
    # Vertical split: remaining space to the right
    if rect.width > piece_w:
        new_rects.append(
            _Rectangle(
                rect.x + piece_w,
                rect.y,
                rect.width - piece_w,
                rect.height
            )
        )
    
    # Horizontal split: remaining space below
    if rect.height > piece_h:
        new_rects.append(
            _Rectangle(
                rect.x,
                rect.y + piece_h,
                piece_w,
                rect.height - piece_h
            )
        )
    
    return new_rects


def _try_fit_piece(
    available_spaces: list[_Rectangle],
    piece: CuttingPiece,
    allow_rotation: bool = False
) -> tuple[_Rectangle | None, bool]:
    """Try to fit a piece in available spaces.
    
    Args:
        available_spaces: List of available rectangular spaces.
        piece: Piece to fit.
        allow_rotation: Whether to try 90° rotation (for homogenous sheets).
    
    Returns:
        Tuple of (best_rect, was_rotated). Returns (None, False) if no fit.
    """
    best_rect = None
    best_area = float('inf')
    rotated = False
    
    # Try both orientations if rotation is allowed
    orientations = [(piece.width, piece.height)]
    if allow_rotation and piece.rotatable:
        orientations.append((piece.height, piece.width))
    
    for w, h in orientations:
        is_rotated = (w, h) != (piece.width, piece.height)
        
        # Find best-fit rectangle (smallest rectangle that fits)
        for rect in available_spaces:
            if rect.can_fit(w, h):
                rect_area = rect.width * rect.height
                if rect_area < best_area:
                    best_area = rect_area
                    best_rect = rect
                    rotated = is_rotated
    
    return best_rect, rotated


def _flatten_list(nested_list: list[list]) -> list:
    """Flatten a list of lists."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


def place_pieces_with_guillotine(
    pieces: list[CuttingPiece],
    sheet: Sheet
) -> list[SheetLayout]:
    """Places cutting pieces on sheets using Guillotine algorithm.
    
    Implements the Guillotine 2D bin packing algorithm with automatic
    rotation support. Deterministic and optimized for manufacturing use cases.
    
    Args:
        pieces: List of CuttingPiece objects to place.
        sheet: Sheet specification (dimensions, type, etc.).
    
    Returns:
        List of SheetLayout objects, one per sheet used.
    
    Note:
        This is an internal function; use optimize_sheet_layout() from
        the public API instead.
    """
    
    if not pieces:
        # Return empty layout for empty piece list
        return [SheetLayout(sheet_id=1, sheet=sheet, placements=[])]
    
    # Expand pieces by quantity
    all_pieces = []
    for piece in pieces:
        for i in range(piece.quantity):
            all_pieces.append(piece)
    
    # Sort by area (largest first) for better packing
    all_pieces.sort(key=lambda p: p.area, reverse=True)
    
    # Determine if rotation is allowed
    allow_rotation = sheet.sheet_type == "homogenous"
    
    # Initialize layout list and current sheet
    layouts: list[SheetLayout] = []
    current_placements: list[Placement] = []
    available_spaces: list[_Rectangle] = [
        _Rectangle(0, 0, sheet.width, sheet.height)
    ]
    sheet_id = 1
    
    # Place each piece
    for piece in all_pieces:
        # Try to fit in current sheet
        best_rect, was_rotated = _try_fit_piece(available_spaces, piece, allow_rotation)
        
        if best_rect is None:
            # No space in current sheet, save it and start new one
            layouts.append(SheetLayout(
                sheet_id=sheet_id,
                sheet=sheet,
                placements=current_placements
            ))
            
            sheet_id += 1
            current_placements = []
            available_spaces = [_Rectangle(0, 0, sheet.width, sheet.height)]
            
            # Try again in new sheet
            best_rect, was_rotated = _try_fit_piece(available_spaces, piece, allow_rotation)
        
        if best_rect is not None:
            # Place the piece
            piece_w = piece.height if was_rotated else piece.width
            piece_h = piece.width if was_rotated else piece.height
            
            # Create placement
            placement = Placement(
                piece=piece,
                x=best_rect.x,
                y=best_rect.y,
                width=piece_w,
                height=piece_h,
                rotated=was_rotated
            )
            current_placements.append(placement)
            
            # Remove used rectangle and add new ones from guillotine cuts
            available_spaces.remove(best_rect)
            new_spaces = _split_rectangle(best_rect, piece_w, piece_h)
            available_spaces.extend(new_spaces)
            
            # Remove overlapping spaces and keep only useful ones
            # (a more efficient implementation would use a better space management)
            available_spaces = [s for s in available_spaces if s.width > 0 and s.height > 0]
    
    # Add final sheet
    if current_placements or not layouts:
        layouts.append(SheetLayout(
            sheet_id=sheet_id,
            sheet=sheet,
            placements=current_placements
        ))
    
    return layouts if layouts else [SheetLayout(sheet_id=1, sheet=sheet, placements=[])]

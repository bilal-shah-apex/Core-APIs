"""Internal geometry helpers (private module).

Helper functions for geometric calculations used by the packing algorithm.

Functions:
    can_fit_rotated: Check if piece fits after 90° rotation.
    find_best_fit_position: Find optimal placement position.
    calculate_guillotine_splits: Determine split rectangles.
"""

# Stub for future geometric helper functions


def can_fit_rotated(piece_w: float, piece_h: float, space_w: float, space_h: float) -> bool:
    """Check if piece can fit in space when rotated 90 degrees.
    
    Args:
        piece_w: Original piece width.
        piece_h: Original piece height.
        space_w: Available space width.
        space_h: Available space height.
    
    Returns:
        True if rotated piece (height, width) fits in space.
    """
    return piece_h <= space_w and piece_w <= space_h

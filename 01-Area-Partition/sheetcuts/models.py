"""Data models for SheetCuts: CuttingPiece, Sheet, SheetLayout, and Placement.

This module defines the core data structures used throughout the SheetCuts module.
All classes are immutable after creation (dataclass-based).

Classes:
    CuttingPiece: Represents a rectangular piece to be cut from a sheet.
    Sheet: Represents a sheet with dimensions, type, and properties.
    Placement: Represents a single piece placement on a sheet with coordinates.
    SheetLayout: Represents all pieces placed on a single sheet.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CuttingPiece:
    """Represents a rectangular piece to be cut from a sheet.
    
    Stores dimensions, quantity, label, and rotation constraints.
    Immutable after creation.
    
    Attributes:
        width (float): Piece width in specified units (inches or millimeters).
        height (float): Piece height in specified units.
        label (str): Human-readable identifier (e.g., "TopPanel", "P1").
            If not provided, auto-generated as P1, P2, etc.
        quantity (int): Number of identical pieces needed. Defaults to 1.
        rotatable (bool): Whether algorithm can rotate piece 90 degrees.
            Defaults to True for homogenous sheets; False for directional.
    
    Raises:
        ValueError: If width or height is not positive (> 0).
        ValueError: If quantity is not positive (> 0).
        TypeError: If label is not a string or quantity is not an int.
    
    Example:
        >>> piece1 = CuttingPiece(width=10, height=20, label="Panel", quantity=1)
        >>> piece2 = CuttingPiece(width=12, height=18, label="Shelf", quantity=3)
        >>> print(f"{piece2.label} x{piece2.quantity}: {piece2.width}×{piece2.height}")
        Shelf x3: 12×18
    """
    
    width: float
    height: float
    label: str
    quantity: int = 1
    rotatable: bool = True

    def __post_init__(self) -> None:
        """Validate CuttingPiece attributes after initialization."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                f"Width and height must be positive; got width={self.width}, "
                f"height={self.height}"
            )
        if self.quantity <= 0:
            raise ValueError(
                f"Quantity must be positive; got quantity={self.quantity}"
            )
        if not isinstance(self.label, str):
            raise TypeError(
                f"Label must be a string; got {type(self.label).__name__}"
            )
        if not isinstance(self.quantity, int):
            raise TypeError(
                f"Quantity must be an integer; got {type(self.quantity).__name__}"
            )

    @property
    def area(self) -> float:
        """Total area of this piece (width × height × quantity).
        
        Returns:
            Float representing total area in square units.
        """
        return self.width * self.height * self.quantity


@dataclass(frozen=True)
class Sheet:
    """Represents a sheet with dimensions, type, and properties.
    
    Stores sheet specifications used for layout optimization.
    Immutable after creation.
    
    Attributes:
        width (float): Sheet width in specified units.
        height (float): Sheet height in specified units.
        units (str): Unit system: "inches" or "millimeters". Defaults to "inches".
        sheet_type (str): Sheet type: "homogenous" (allows rotation) or 
            "directional" (feature-aligned, rotation constrained). 
            Defaults to "homogenous".
        mode (str): "sheet" (fixed dimensions) or "roll" (variable length).
            Currently only "sheet" is supported (v1.0). Defaults to "sheet".
    
    Raises:
        ValueError: If width or height is not positive.
        ValueError: If units is not "inches" or "millimeters".
        ValueError: If sheet_type is not "homogenous" or "directional".
        ValueError: If mode is not "sheet" or "roll".
    
    Example:
        >>> sheet = Sheet(48, 96, "inches", "homogenous")
        >>> print(f"Sheet: {sheet.width} × {sheet.height} {sheet.units}")
        Sheet: 48 × 96 inches
    """
    
    width: float
    height: float
    units: str = "inches"
    sheet_type: str = "homogenous"
    mode: str = "sheet"

    def __post_init__(self) -> None:
        """Validate Sheet attributes after initialization."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                f"Width and height must be positive; got width={self.width}, "
                f"height={self.height}"
            )
        if self.units not in ("inches", "millimeters"):
            raise ValueError(
                f"Units must be 'inches' or 'millimeters'; got {self.units}"
            )
        if self.sheet_type not in ("homogenous", "directional"):
            raise ValueError(
                f"Sheet type must be 'homogenous' or 'directional'; got {self.sheet_type}"
            )
        if self.mode not in ("sheet", "roll"):
            raise ValueError(
                f"Mode must be 'sheet' or 'roll'; got {self.mode}"
            )

    @property
    def area(self) -> float:
        """Total area of the sheet (width × height).
        
        Returns:
            Float representing sheet area in square units.
        """
        return self.width * self.height


@dataclass(frozen=True)
class Placement:
    """Represents a single piece placement on a sheet with coordinates.
    
    Stores the position and orientation of a cutting piece after optimization.
    Immutable after creation.
    
    Attributes:
        piece (CuttingPiece): The cutting piece being placed.
        x (float): X-coordinate (horizontal position) from top-left origin.
        y (float): Y-coordinate (vertical position) from top-left origin.
        width (float): Actual width of piece in placement (may be rotated).
        height (float): Actual height of piece in placement (may be rotated).
        rotated (bool): Whether this piece was rotated 90 degrees. Defaults to False.
    
    Example:
        >>> piece = CuttingPiece(10, 20, "Panel")
        >>> placement = Placement(piece, x=0, y=0, width=10, height=20, rotated=False)
        >>> print(f"{placement.piece.label}: ({placement.x}, {placement.y})")
        Panel: (0, 0)
    """
    
    piece: CuttingPiece
    x: float
    y: float
    width: float
    height: float
    rotated: bool = False

    @property
    def area(self) -> float:
        """Area of this placement (width × height).
        
        Returns:
            Float representing placement area.
        """
        return self.width * self.height


@dataclass
class SheetLayout:
    """Represents all pieces placed on a single sheet.
    
    Contains a list of placements and metadata about the sheet layout.
    Mutable to allow gradual construction during optimization.
    
    Attributes:
        sheet_id (int): Sheet identifier (1-indexed).
        sheet (Sheet): The sheet specification this layout uses.
        placements (list[Placement]): List of piece placements on this sheet.
    
    Example:
        >>> sheet = Sheet(48, 96, "inches")
        >>> layout = SheetLayout(sheet_id=1, sheet=sheet, placements=[])
        >>> print(f"Sheet {layout.sheet_id}: {len(layout.placements)} pieces")
        Sheet 1: 0 pieces
    """
    
    sheet_id: int
    sheet: Sheet
    placements: list[Placement]

    @property
    def total_pieces_area(self) -> float:
        """Total area of all pieces in this layout.
        
        Returns:
            Float representing sum of all placement areas.
        """
        return sum(p.area for p in self.placements)

    @property
    def utilization_percentage(self) -> float:
        """Percentage of sheet area actually used by pieces.
        
        Calculated as: (total_pieces_area / sheet_area) * 100
        
        Returns:
            Float between 0 and 100 representing utilization percentage.
            100.0 represents perfect packing with no waste.
        """
        if self.sheet.area == 0:
            return 0.0
        return (self.total_pieces_area / self.sheet.area) * 100

    @property
    def waste_area(self) -> float:
        """Unused sheet area after piece placement.
        
        Returns:
            Float representing wasted area in square units.
        """
        return self.sheet.area - self.total_pieces_area

    def to_dict(self) -> dict:
        """Convert layout to dictionary for JSON serialization.
        
        Returns:
            Dictionary with sheet_id, sheet info, placements, and statistics.
        
        Example:
            >>> layout_dict = layout.to_dict()
            >>> import json
            >>> print(json.dumps(layout_dict, indent=2))
        """
        return {
            "sheet_id": self.sheet_id,
            "sheet": {
                "width": self.sheet.width,
                "height": self.sheet.height,
                "units": self.sheet.units,
            },
            "placements": [
                {
                    "label": p.piece.label,
                    "x": p.x,
                    "y": p.y,
                    "width": p.width,
                    "height": p.height,
                    "rotated": p.rotated,
                }
                for p in self.placements
            ],
            "statistics": {
                "total_pieces": len(self.placements),
                "total_area_used": self.total_pieces_area,
                "sheet_area": self.sheet.area,
                "utilization_percentage": self.utilization_percentage,
                "waste_area": self.waste_area,
            },
        }

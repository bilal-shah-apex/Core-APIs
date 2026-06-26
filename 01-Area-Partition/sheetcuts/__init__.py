"""SheetCuts: Sheet Optimization & Layout Engine.

A geometry-based sheet optimization module that automatically layouts rectangular
cutting pieces onto standard or custom sheet sizes, minimizing material wastage.

This module provides a complete pipeline for:
  - Validating cutting piece specifications and sheet parameters
  - Optimizing piece placement using Guillotine algorithm
  - Generating visual diagrams of optimized layouts
  - Exporting layouts in JSON format for REST APIs

Main entry point is ``optimize_sheet_layout()`` function.

Example:
    Basic usage to optimize cutting pieces on a sheet::

        from sheetcuts.models import CuttingPiece, Sheet
        from sheetcuts.optimization import optimize_sheet_layout

        # Define cutting pieces
        pieces = [
            CuttingPiece(10, 20, "TopPanel", 1),
            CuttingPiece(12, 18, "Shelf", 3),
        ]

        # Define sheet
        sheet = Sheet(48, 96, "inches", "homogenous")

        # Optimize layout
        layouts = optimize_sheet_layout(pieces, sheet)

        # Generate visual diagram
        from sheetcuts.visualization import generate_html_diagram
        html = generate_html_diagram(layouts, sheet)

        # Output as JSON (for REST APIs)
        import json
        output = {
            "success": True,
            "summary": {
                "total_sheets_required": len(layouts),
                "utilization_percentage": calculate_utilization(layouts, sheet),
            },
            "layouts": [layout.to_dict() for layout in layouts],
            "html_diagram": html,
        }
        print(json.dumps(output, indent=2))

Public API:
    Models:
        - CuttingPiece: Represents a rectangular piece to cut
        - Sheet: Represents a sheet with dimensions and properties
        - SheetLayout: Represents the optimized layout of pieces on a sheet
        - Placement: Represents a single piece placement with coordinates

    Functions:
        - optimize_sheet_layout: Main optimization function
        - validate_input: Validates input JSON schema
        - generate_html_diagram: Creates visual SVG/HTML representation
"""

__version__ = "1.0.0"
__author__ = "SheetCuts Development Team"

from sheetcuts.models import (
    CuttingPiece,
    Sheet,
    SheetLayout,
    Placement,
)
from sheetcuts.optimization import optimize_sheet_layout
from sheetcuts.validators import validate_input
from sheetcuts.visualization import generate_html_diagram

__all__ = [
    "CuttingPiece",
    "Sheet",
    "SheetLayout",
    "Placement",
    "optimize_sheet_layout",
    "validate_input",
    "generate_html_diagram",
]

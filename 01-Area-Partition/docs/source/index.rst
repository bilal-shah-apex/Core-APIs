SheetCuts Documentation
=======================

Welcome to the SheetCuts API documentation. This documentation is automatically
generated from inline code docstrings using Sphinx.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   api

Quick Start
-----------

Install SheetCuts::

    pip install sheetcuts

Basic usage::

    from sheetcuts.models import CuttingPiece, Sheet
    from sheetcuts.optimization import optimize_sheet_layout

    # Define pieces
    pieces = [CuttingPiece(10, 20, "Panel", 1)]

    # Define sheet
    sheet = Sheet(48, 96, "inches", "homogenous")

    # Optimize
    layouts = optimize_sheet_layout(pieces, sheet)

    # Generate diagram
    from sheetcuts.visualization import generate_html_diagram
    html = generate_html_diagram(layouts, sheet)

Key Features
------------

- **Automatic Rotation**: Optimizes piece rotation on homogenous sheets
- **Deterministic**: Same input always produces same output
- **JSON-Ready**: All inputs/outputs compatible with REST APIs
- **Visual Diagrams**: Generates SVG diagrams with labeled pieces and dimensions
- **Performance**: Processes 1000+ pieces in under 5 seconds

API Reference
-------------

See :doc:`modules` and :doc:`api` for complete API documentation.

Support
-------

For issues or questions, please refer to the project repository.

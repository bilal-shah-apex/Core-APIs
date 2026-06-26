"""HTML/SVG visualization for optimized sheet layouts.

Generates standard-complexity diagrams showing:
- Sheet outlines with dimensions
- Labeled cutting pieces as rectangles
- Individual piece dimensions
- Unit system display

Functions:
    generate_html_diagram: Creates SVG/HTML representation of layouts.
"""

from sheetcuts.models import SheetLayout, Sheet


def generate_html_diagram(
    layouts: list[SheetLayout],
    sheet: Sheet,
    include_coordinates: bool = False
) -> str:
    """Generates SVG/HTML diagram of optimized sheet layouts.
    
    Creates a visual representation showing all sheets with labeled cutting
    pieces, dimensions, and unit information. Output is embedded-ready for
    JSON responses.
    
    Args:
        layouts: List of SheetLayout objects to visualize.
        sheet: Sheet specification (used for scale and unit display).
        include_coordinates: Whether to show piece coordinates. Defaults to False
            (cleaner diagram for v1.0 standard complexity).
    
    Returns:
        String containing complete SVG/HTML code ready for embedding in JSON
        or displaying in browser. Includes CSS styling for clean presentation.
    
    Raises:
        ValueError: If layouts list is empty.
        TypeError: If layouts is not a list or sheet is not a Sheet object.
    
    Note:
        - SVG is scalable and works in all modern browsers
        - Includes responsive CSS for different screen sizes
        - Colors used: black for outlines, light blue for pieces
        - Coordinates system: top-left (0, 0) origin
        - Scale automatically adjusts based on sheet size
    
    Example:
        >>> from sheetcuts.models import SheetLayout, Sheet
        >>> from sheetcuts.visualization import generate_html_diagram
        >>> 
        >>> sheet = Sheet(48, 96, "inches", "homogenous")
        >>> layouts = [SheetLayout(1, sheet, [])]
        >>> 
        >>> html = generate_html_diagram(layouts, sheet)
        >>> with open("layout_diagram.html", "w") as f:
        ...     f.write(html)
        >>> print(f"Generated diagram: {len(html)} characters")
        Generated diagram: 2847 characters
    """
    if not isinstance(layouts, (list, tuple)):
        raise TypeError(
            f"layouts must be a list or tuple; got {type(layouts).__name__}"
        )
    
    if not layouts:
        raise ValueError("layouts list cannot be empty")
    
    if not isinstance(sheet, Sheet):
        raise TypeError(
            f"sheet must be a Sheet object; got {type(sheet).__name__}"
        )
    
    # Start building SVG
    # Calculate scale: fit sheets to reasonable display size
    display_width = 1000  # pixels
    scale = display_width / sheet.width
    
    svg_width = int(sheet.width * scale) + 40  # padding
    svg_height = int(len(layouts) * (sheet.height * scale)) + 40 + (50 * len(layouts))
    
    svg_parts = [
        '<svg width="100%" height="100%" viewBox="0 0 '
        f'{svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">',
        '<style>',
        '.sheet-label { font-size: 14px; font-weight: bold; fill: black; }',
        '.piece-label { font-size: 12px; fill: black; text-anchor: middle; }',
        '.dimension-text { font-size: 10px; fill: gray; }',
        '.unit-text { font-size: 12px; fill: gray; }',
        'rect.sheet-outline { fill: none; stroke: black; stroke-width: 2; }',
        'rect.piece { fill: lightblue; stroke: darkblue; stroke-width: 1; }',
        '</style>',
    ]
    
    # Draw each layout (sheet)
    y_offset = 20
    for layout in layouts:
        # Sheet outline
        svg_parts.append(
            f'<text x="20" y="{y_offset - 5}" class="sheet-label">'
            f'Sheet {layout.sheet_id}</text>'
        )
        
        svg_parts.append(
            f'<rect x="20" y="{y_offset}" width="{sheet.width * scale}" '
            f'height="{sheet.height * scale}" class="sheet-outline"/>'
        )
        
        # Sheet dimensions
        svg_parts.append(
            f'<text x="{20 + (sheet.width * scale) / 2}" '
            f'y="{y_offset + sheet.height * scale + 20}" '
            f'class="dimension-text" text-anchor="middle">'
            f'{sheet.width} × {sheet.height} {sheet.units}</text>'
        )
        
        # Draw pieces (placements) on this sheet
        for placement in layout.placements:
            x_pos = 20 + (placement.x * scale)
            y_pos = y_offset + (placement.y * scale)
            w_pos = placement.width * scale
            h_pos = placement.height * scale
            
            # Piece rectangle
            svg_parts.append(
                f'<rect x="{x_pos}" y="{y_pos}" width="{w_pos}" '
                f'height="{h_pos}" class="piece"/>'
            )
            
            # Piece label
            svg_parts.append(
                f'<text x="{x_pos + w_pos / 2}" y="{y_pos + h_pos / 2 + 5}" '
                f'class="piece-label">{placement.piece.label}</text>'
            )
            
            # Piece dimensions
            svg_parts.append(
                f'<text x="{x_pos + w_pos / 2}" y="{y_pos + h_pos + 12}" '
                f'class="dimension-text" text-anchor="middle">'
                f'{placement.width}×{placement.height}</text>'
            )
        
        y_offset += (sheet.height * scale) + 60
    
    # Unit system legend
    svg_parts.append(
        f'<text x="20" y="{y_offset + 20}" class="unit-text">'
        f'Diagram Unit System: {sheet.units}</text>'
    )
    
    svg_parts.append('</svg>')
    
    html = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>SheetCuts Layout Diagram</title>\n'
        '<style>\n'
        'body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }\n'
        '.diagram-container { background: white; padding: 20px; border-radius: 8px; '
        'box-shadow: 0 2px 4px rgba(0,0,0,0.1); }\n'
        '.diagram-title { margin-bottom: 20px; color: #333; }\n'
        '</style>\n'
        '</head>\n'
        '<body>\n'
        '<div class="diagram-container">\n'
        '<h2 class="diagram-title">Sheet Cutting Layout Optimization</h2>\n'
        + '\n'.join(svg_parts) + '\n'
        '</div>\n'
        '</body>\n'
        '</html>\n'
    )
    
    return html

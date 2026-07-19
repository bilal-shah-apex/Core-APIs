from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sheetcuts.models import CuttingPiece, Sheet
from sheetcuts.optimization import optimize_sheet_layout
from sheetcuts.validators import validate_input
from sheetcuts.visualization import generate_html_diagram

app = FastAPI(
    title="SheetCuts GUI Adapter",
    description="Thin REST wrapper used for manual testing of the SheetCuts core API.",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
def homepage() -> FileResponse:
    """Serve the GUI front-end."""
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/optimize")
def optimize(data: dict[str, Any]) -> dict[str, Any]:
    """Validate request, run SheetCuts optimization, and return JSON results."""
    is_valid, error_message = validate_input(data)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    sheet_data = data["sheet"]
    sheet = Sheet(
        width=float(sheet_data["width"]),
        height=float(sheet_data["height"]),
        units=sheet_data.get("units", "inches"),
        sheet_type=sheet_data.get("type", "homogenous"),
        mode=sheet_data.get("mode", "sheet"),
    )

    pieces = []
    for idx, piece_data in enumerate(data.get("cutting_pieces", []) or []):
        pieces.append(
            CuttingPiece(
                width=float(piece_data["width"]),
                height=float(piece_data["height"]),
                label=piece_data.get("label", f"P{idx + 1}"),
                quantity=int(piece_data.get("quantity", 1)),
            )
        )

    layouts = optimize_sheet_layout(pieces, sheet)

    summary = {
        "total_sheets_required": len(layouts),
        "utilization_percentage": (
            sum(layout.total_pieces_area for layout in layouts)
            / (len(layouts) * sheet.area) * 100
            if layouts
            else 0.0
        ),
    }

    return {
        "success": True,
        "summary": summary,
        "layouts": [layout.to_dict() for layout in layouts],
        "html_diagram": generate_html_diagram(layouts, sheet) if layouts else "",
    }

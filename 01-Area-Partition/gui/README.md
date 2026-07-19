# SheetCuts GUI Manual Testing

This folder contains a lightweight GUI wrapper for manual testing of the SheetCuts core API.

## Run the GUI

1. Install dependencies:

```bash
pip install -r gui/requirements.txt
```

2. Start the server:

```bash
cd 01-Area-Partition
uvicorn gui.app:app --reload
```

3. Open the browser:

```text
http://127.0.0.1:8000
```

## What it does

- Serves a browser form for sheet dimensions and cutting pieces
- Submits the request to `/api/optimize`
- Uses `sheetcuts.validators.validate_input`
- Converts JSON to `sheetcuts.models.CuttingPiece` and `Sheet`
- Calls `sheetcuts.optimization.optimize_sheet_layout`
- Returns JSON output plus generated `sheetcuts.visualization.generate_html_diagram`

## Notes

- The core `sheetcuts/` package is not modified.
- This folder is intentionally separated from the package implementation.

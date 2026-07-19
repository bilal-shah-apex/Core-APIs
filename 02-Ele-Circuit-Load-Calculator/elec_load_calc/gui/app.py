from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ..models import ApplianceLoad, CircuitConfig, LoadRequest, WireConfig
from ..calculator import calculate_load

app = FastAPI(
    title="Electrical Circuit Load Calculator GUI",
    description="Thin REST wrapper for manual testing of the electrical load calculator core API.",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
def homepage() -> FileResponse:
    """Serve the GUI front-end."""
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/calculate")
def calculate(data: dict[str, Any]) -> dict[str, Any]:
    """Validate request, run the calculator, and return JSON results."""
    circuit_data = data.get("circuit", {})
    circuit = CircuitConfig(
        name=circuit_data.get("name", "Circuit"),
        voltage=float(circuit_data.get("voltage", 240.0)),
        voltage_tolerance_percent=float(circuit_data.get("voltage_tolerance_percent", 10.0)),
        phase=circuit_data.get("phase", "single"),
    )

    wire_data = data.get("wire")
    wire = None
    if wire_data:
        wire = WireConfig(
            gauge=wire_data.get("gauge"),
            material=wire_data.get("material"),
            distance_meters=float(wire_data.get("distance_meters", 0.0)) if wire_data.get("distance_meters") is not None else None,
            operating_temperature_c=float(wire_data.get("operating_temperature_c", 0.0)) if wire_data.get("operating_temperature_c") is not None else None,
        )

    loads = []
    for item in data.get("loads", []) or []:
        loads.append(
            ApplianceLoad(
                name=item.get("name", "Load"),
                power_watts=float(item.get("power_watts", 0.0)),
                quantity=int(item.get("quantity", 1)),
            )
        )

    request = LoadRequest(circuit=circuit, loads=loads, wire=wire)
    result = calculate_load(request)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", {}).get("message", "Invalid request"))

    return result

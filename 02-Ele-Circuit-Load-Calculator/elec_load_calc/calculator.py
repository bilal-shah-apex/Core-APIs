"""Core electrical load calculation engine."""

from __future__ import annotations

from math import ceil
from typing import Dict, List, Optional

from .models import ApplianceLoad, LoadRequest, WireConfig
from .validators import validate_request


def calculate_load(request: LoadRequest) -> Dict[str, object]:
    """Calculate the electrical load for a single circuit.

    Args:
        request: The load request data.

    Returns:
        A structured dictionary containing the calculated load summary.
    """
    is_valid, error = validate_request(request)
    if not is_valid:
        return {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": error,
            },
        }

    total_load_watts = sum(load.power_watts * load.quantity for load in request.loads)
    estimated_current_a = total_load_watts / request.circuit.voltage
    voltage_tolerance = request.circuit.voltage_tolerance_percent / 100.0
    voltage_min_v = request.circuit.voltage * (1 - voltage_tolerance)
    voltage_max_v = request.circuit.voltage * (1 + voltage_tolerance)

    breaker_size = max(10, int(ceil(estimated_current_a * 1.25 / 10.0) * 10))

    warnings: List[str] = []
    if breaker_size < 20 and total_load_watts > 2000:
        warnings.append("Load is approaching the typical breaker threshold for this simple rule")

    if request.wire is not None:
        if request.wire.distance_meters is not None and request.wire.distance_meters > 30:
            warnings.append("Wire distance is high; voltage drop may be significant")

    return {
        "success": True,
        "summary": {
            "circuit_name": request.circuit.name,
            "total_load_watts": round(total_load_watts, 2),
            "total_load_va": round(total_load_watts, 2),
            "estimated_current_a": round(estimated_current_a, 2),
            "voltage_min_v": round(voltage_min_v, 2),
            "voltage_max_v": round(voltage_max_v, 2),
            "recommended_breaker_a": breaker_size,
            "breaker_margin": 1.25,
        },
        "warnings": warnings,
        "metadata": {
            "algorithm": "single_circuit_load_v1",
        },
    }

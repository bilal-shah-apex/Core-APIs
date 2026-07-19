"""Validation helpers for electrical load calculations."""

from __future__ import annotations

from typing import Optional, Tuple

from .models import ApplianceLoad, LoadRequest


def validate_request(request: LoadRequest) -> Tuple[bool, Optional[str]]:
    """Validate a load calculation request.

    Args:
        request: The request to validate.

    Returns:
        A tuple of ``(is_valid, error_message)``.
    """
    if request.circuit.voltage <= 0:
        return False, "Voltage must be a positive number"

    if request.circuit.voltage_tolerance_percent < 0:
        return False, "Voltage tolerance must be non-negative"

    if request.loads is None:
        return False, "Loads must be provided"

    for load in request.loads:
        if load.quantity <= 0:
            return False, "Quantity must be a positive integer"
        if load.power_watts <= 0:
            return False, "Power values must be positive numbers"

    if request.wire is not None:
        if request.wire.distance_meters is not None and request.wire.distance_meters < 0:
            return False, "Wire distance must be non-negative"
        if request.wire.operating_temperature_c is not None and request.wire.operating_temperature_c < 0:
            return False, "Operating temperature must be non-negative"

    return True, None

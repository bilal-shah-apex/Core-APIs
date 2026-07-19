"""Data models for electrical load calculations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ApplianceLoad:
    """Represents a single appliance or load entry."""

    name: str
    power_watts: float
    quantity: int = 1


@dataclass
class CircuitConfig:
    """Represents circuit-level configuration."""

    name: str = "Circuit"
    voltage: float = 240.0
    voltage_tolerance_percent: float = 10.0
    phase: str = "single"


@dataclass
class WireConfig:
    """Represents optional wire-related parameters."""

    gauge: Optional[str] = None
    material: Optional[str] = None
    distance_meters: Optional[float] = None
    operating_temperature_c: Optional[float] = None


@dataclass
class LoadRequest:
    """Represents a complete load calculation request."""

    circuit: CircuitConfig = field(default_factory=CircuitConfig)
    loads: List[ApplianceLoad] = field(default_factory=list)
    wire: Optional[WireConfig] = None

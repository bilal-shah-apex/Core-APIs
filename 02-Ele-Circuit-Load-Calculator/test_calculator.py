from elec_load_calc.models import ApplianceLoad, CircuitConfig, LoadRequest, WireConfig
from elec_load_calc.calculator import calculate_load


def test_basic_calculation():
    request = LoadRequest(
        circuit=CircuitConfig(name="Bedroom Circuit", voltage=240.0, voltage_tolerance_percent=10.0),
        loads=[
            ApplianceLoad(name="Ceiling Light", power_watts=9, quantity=8),
            ApplianceLoad(name="Ceiling Fan", power_watts=75, quantity=1),
        ],
    )

    result = calculate_load(request)

    assert result["success"] is True
    assert result["summary"]["total_load_watts"] == 147.0
    assert result["summary"]["recommended_breaker_a"] == 10


def test_validation_error_for_invalid_power():
    request = LoadRequest(
        circuit=CircuitConfig(name="Bad Circuit", voltage=240.0),
        loads=[ApplianceLoad(name="Bad Load", power_watts=-10, quantity=1)],
    )

    result = calculate_load(request)

    assert result["success"] is False
    assert result["error"]["code"] == "VALIDATION_ERROR"

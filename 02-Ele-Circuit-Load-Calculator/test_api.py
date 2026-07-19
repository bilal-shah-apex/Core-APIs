from fastapi.testclient import TestClient

from elec_load_calc.gui.app import app


client = TestClient(app)


def test_calculate_endpoint_returns_summary():
    response = client.post(
        "/api/calculate",
        json={
            "circuit": {
                "name": "Test Circuit",
                "voltage": 240,
                "voltage_tolerance_percent": 10,
            },
            "loads": [
                {"name": "Ceiling Light", "power_watts": 9, "quantity": 8},
                {"name": "Ceiling Fan", "power_watts": 75, "quantity": 1},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["summary"]["circuit_name"] == "Test Circuit"
    assert payload["summary"]["recommended_breaker_a"] == 10

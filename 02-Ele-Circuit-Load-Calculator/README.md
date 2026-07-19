# Electrical Circuit Load Calculator

A backend-first Python module for estimating electrical circuit load from appliance inputs and optional wiring parameters.

## Scope for v1.0
- Accept a list of appliances with quantities and power values
- Support optional voltage, tolerance, and wire-related inputs
- Return total load, current estimate, and recommended breaker size
- Provide a deterministic, pure-function calculation interface suitable for UI and API testing

## Planned Structure

```text
02-Ele-Circuit-Load-Calculator/
├── Spec/
│   └── Spec-Ele-Circuit-Load-Calculator.md
├── PROMPTS_REGISTER.md
└── README.md
```

## Next Step
Start implementing the core algorithm and validation layer once the spec is approved.

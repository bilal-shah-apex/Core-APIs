# Product Requirements Document: Electrical Circuit Load Calculator

## Document Metadata

| Field | Value |
| :--- | :--- |
| **Project Name** | Electrical Circuit Load Calculator |
| **Module ID** | CORE-02-EleCircuitLoadCalculator |
| **Target Launch Date** | 2 weeks (ASAP) |
| **Status** | Draft - Under Review |
| **Authors** | AI-Driven Architecture Team |
| **Version** | 0.1 |

---

## Executive Summary & Goals

### Product Vision
The Electrical Circuit Load Calculator is a backend-ready Python service that computes the expected electrical load for a single circuit from common appliance inputs such as lights, fans, lamps, screens, air conditioners, and exhaust fans. The core service will expose a deterministic pure function with well-defined inputs and outputs, supporting later expansion into multi-circuit and main-panel breaker design.

### Business Objectives
- Provide a reusable algorithm for estimating circuit load for residential and light commercial electrical planning
- Support fast, deterministic load calculations for simple UI and API testing workflows
- Establish a foundation for future multi-circuit and whole-building breaker design
- Reduce manual calculation errors and improve consistency of circuit planning
- Enable future integration with catalog-driven breaker recommendations and reusable preset circuit templates

### Success Metrics (KPIs)
- **Accuracy:** Load calculations align with expected engineering assumptions for common appliance loads
- **Reliability:** Invalid or incomplete inputs are rejected with clear messages
- **Performance:** Process a typical 20-50 appliance request in under 1 second
- **Maintainability:** Core logic is implemented as a pure function with clear input/output contracts
- **Extensibility:** Design supports future expansion to multi-circuit and panel-level calculations

---

## Target Audience & User Personas

### Primary Users
1. **Electrical Designers / Engineers** - Need quick circuit sizing estimates
2. **Developers / API Consumers** - Need a backend function for UI or automation testing
3. **Homeowners / DIY Planners** - Want a simple tool to estimate electrical demand before installation
4. **BIM / Building Automation Integrators** - Need a reusable calculation service for later integration

### Secondary Users
- Small contractors and installers
- Educational institutions teaching basic electrical load estimation

### User Pain Points
- Manual load calculations are time-consuming and error-prone
- Circuit sizing can be inconsistent without a standard calculation baseline
- Existing tools often focus on full electrical design rather than simple estimation

---

## Functional Requirements

| Req ID | Feature | User Action / Capability | Acceptance Criteria | Priority |
| :--- | :--- | :--- | :--- | :--- |
| FR-01 | Input: Appliance Load Entries | User provides one or more appliance entries with name, quantity, and power value | System accepts a list of appliances and calculates the aggregate load | P0 |
| FR-02 | Input: Common Appliance Presets | User selects a common appliance type such as ceiling light, fan, lamp, LCD screen, air conditioner, or exhaust fan | System accepts named presets and uses the corresponding default wattage if no explicit value is provided | P1 |
| FR-03 | Input: Voltage | User provides circuit voltage or omits it | System defaults to 240V if omitted; applies tolerance logic and reports effective range | P0 |
| FR-04 | Input: Voltage Tolerance | User specifies allowable voltage variation | System calculates tolerant minimum/maximum voltage range and reflects its effect on current estimates | P1 |
| FR-05 | Input: Wire Characteristics | User provides wire gauge, material, distance, and operating temperature | System uses these inputs to estimate voltage drop and adjust load analysis if applicable | P1 |
| FR-06 | Input: Circuit Metadata | User provides circuit name or identifier | System preserves the circuit label in output for traceability | P1 |
| FR-07 | Calculation: Total Load | User submits a valid load request | System returns total active load in watts and estimated current in amps | P0 |
| FR-08 | Calculation: Breaker Rating | User submits a valid load request | System recommends an appropriate circuit breaker size with a margin for safety; in later phases, this recommendation can be sourced from a catalog of standard breaker options | P0 |
| FR-09 | Output: Load Summary | User receives calculation results | Output includes total load, estimated current, breaker suggestion, and warning flags | P0 |
| FR-10 | Output: Warnings & Safety Notes | System detects overloaded or borderline conditions | Output includes warning messages for overload, high voltage drop, or near-limit breaker sizing | P1 |
| FR-11 | Error Handling: Invalid Appliance Data | User provides negative quantity or invalid power values | System rejects the request with a descriptive validation error | P0 |
| FR-12 | Error Handling: Invalid Voltage | User provides non-positive voltage or invalid tolerance | System rejects the request with a descriptive validation error | P0 |
| FR-13 | Error Handling: Invalid Wire Data | User provides unsupported wire material or invalid distance/temperature | System returns a validation error or warning depending on severity | P1 |
| FR-14 | API Contract | User or UI consumes the module via JSON | System accepts JSON input and returns structured JSON output | P0 |

---

## Non-Functional Requirements

### Performance
- **Response Time:** Typical request with 20-50 appliances should complete in < 1 second
- **Scalability:** Support 100+ appliance entries efficiently in a single request
- **Algorithm Complexity:** Prefer simple linear-time evaluation for v1.0

### Reliability & Correctness
- **Deterministic Output:** Same input always produces the same calculation
- **Validation Quality:** All invalid inputs are caught before calculation
- **No Silent Assumptions:** If a value is omitted, the system should use a documented default

### Code Quality & Maintainability
- **Language:** Pure Python
- **Python Version:** 3.11+ compatible
- **Code Style:** PEP 8 compliant; type hints on public functions
- **Modularity:** Separate modules for input validation, load calculation, and result formatting
- **Documentation:** Public functions and classes should include Google-style docstrings

### Testing
- **Unit Test Coverage:** At least 80% for core calculation logic
- **Test Categories:** Valid calculation, invalid input, voltage tolerance, wire-related estimation, breaker sizing recommendations
- **Regression:** All tests remain green on every change to the core algorithm

### Security & Privacy
- **Input Validation:** Strict schema validation for request payloads
- **No Sensitive Data:** Module processes numeric and descriptive load data only
- **Future API Security:** Compatible with standard API authentication in later phases

---

## Data Format Specifications

### Input JSON Schema

```json
{
  "circuit": {
    "name": "Living Room Circuit",
    "voltage": 240,
    "voltage_tolerance_percent": 10,
    "phase": "single"
  },
  "loads": [
    {
      "name": "Ceiling Light",
      "power_watts": 60,
      "quantity": 4
    },
    {
      "name": "Ceiling Fan",
      "power_watts": 75,
      "quantity": 2
    },
    {
      "name": "Air Conditioner",
      "power_watts": 1500,
      "quantity": 1
    }
  ],
  "wire": {
    "gauge": "2.5mm2",
    "material": "copper",
    "distance_meters": 20,
    "operating_temperature_c": 30
  }
}
```

**Key Notes:**
- `circuit.voltage` is optional; defaults to `240`
- `circuit.voltage_tolerance_percent` is optional; defaults to `10`
- `loads[].power_watts` may be omitted if a built-in preset catalog is provided later
- `loads[].quantity` defaults to `1` if omitted
- `wire` is optional; if omitted, wire-related calculations are skipped or treated as neutral

### Output JSON Schema

```json
{
  "success": true,
  "summary": {
    "circuit_name": "Living Room Circuit",
    "total_load_watts": 2490,
    "total_load_va": 2490,
    "estimated_current_a": 10.38,
    "voltage_min_v": 216,
    "voltage_max_v": 264,
    "recommended_breaker_a": 20,
    "breaker_margin": 1.25
  },
  "warnings": [
    "Load is within normal operating range.",
    "Voltage drop estimate is acceptable."
  ],
  "metadata": {
    "algorithm": "single_circuit_load_v1",
    "generated_at": "2026-07-20T00:00:00Z"
  }
}
```

### Error Response JSON Schema

```json
{
  "success": false,
  "error": {
    "code": "INVALID_POWER",
    "message": "Appliance 'Ceiling Light' has invalid power_watts value",
    "details": {
      "appliance": "Ceiling Light",
      "issue": "negative_or_zero_power"
    }
  }
}
```

---

## Calculation Logic Specification (v1.0)

### Core Formula
For each appliance entry:
- `appliance_load_watts = power_watts × quantity`
- `total_load_watts = sum(appliance_load_watts)`
- `estimated_current_a = total_load_watts / voltage`

### Recommended Breaker Sizing
- Use a breaker size based on the calculated current plus a safety margin
- Suggested default rule for v1.0:
  - `recommended_breaker_a = ceil(estimated_current_a × 1.25 / 10) * 10`
  - Minimum breaker size should be at least `10A`
- In later phases, the recommended breaker can be resolved from a catalog of standard breaker sizes and project-specific preferences rather than relying only on this simple rule

### Voltage Tolerance Handling
- `voltage_min_v = voltage × (1 - tolerance_percent / 100)`
- `voltage_max_v = voltage × (1 + tolerance_percent / 100)`
- Current may be reported for both nominal and tolerance-adjusted conditions if needed

### Wire Parameter Considerations
- Wire material and gauge may influence voltage drop estimation
- Distance and temperature may adjust the effective current carrying assumption
- In v1.0, these are advisory and may not change breaker selection unless explicitly enabled

---

## Error Handling & Edge Cases

| Scenario | Handling Strategy | Error Code | User Message |
| :--- | :--- | :--- | :--- |
| Negative or zero power | Reject input | `INVALID_POWER` | "Power values must be positive numbers" |
| Missing quantity | Default to 1 | `SUCCESS` | Quantity defaults to 1 |
| Missing voltage | Default to 240V | `SUCCESS` | Voltage defaults to 240V |
| Negative or zero voltage | Reject input | `INVALID_VOLTAGE` | "Voltage must be a positive number" |
| Empty load list | Accept as valid edge case | `SUCCESS` | Return zero load and a neutral breaker recommendation |
| Invalid JSON | Reject input | `INVALID_JSON` | "Request body is not valid JSON" |
| Missing required fields | Reject input | `MISSING_FIELD` | "Field '{field_name}' is required" |
| Unsupported wire material | Warn or reject | `INVALID_WIRE_MATERIAL` | "Wire material is not recognized" |
| Extremely long wire distance | Emit warning | `WARNING` | "Wire distance is high; voltage drop may be significant" |

---

## Future Capability: Preset Room Templates and Multi-Circuit Composition

A valuable follow-on capability will be the ability to define reusable room templates that expand into multiple circuits automatically. For example, a bedroom with attached bath could be represented as a preset package with three standard circuits:

1. **Circuit 1 – Room and bath lighting**
   - 8 ceiling lights at 9W each
   - 1 ceiling fan
   - 1 rope light
   - 1 curtain rope light
   - 2 ceiling lights in the dressing area
   - 2 ceiling lights in the bathroom
   - 1 small bathroom exhaust fan

2. **Circuit 2 – Wall outlets**
   - 4 wall outlets in the bedroom
   - 2 additional outlets for TV and TV accessory
   - Support for occasional loads such as vacuum cleaner or small drill machine
   - Occasional ironing load may also be considered in the same grouping

3. **Circuit 3 – Air conditioner**
   - 1.0 ton, 1.5 ton, or 2.0 ton unit depending on the selected preset or user override

With this model, a user could request something like: "I have 3 preset bedrooms in the basement" and the system would generate all 9 circuits automatically. The core single-circuit calculator would remain the foundation, while a higher-level composition layer would aggregate the circuits and later support a main breaker design.

### Example: Bedroom-with-Bath Template (Future)

```json
{
  "template_name": "bedroom_with_attached_bath",
  "quantity": 3,
  "circuits": [
    {
      "circuit_id": "lighting_1",
      "description": "Room and bath lighting",
      "loads": [
        {"name": "Ceiling Light", "power_watts": 9, "quantity": 8},
        {"name": "Ceiling Fan", "power_watts": 75, "quantity": 1},
        {"name": "Rope Light", "power_watts": 20, "quantity": 1},
        {"name": "Curtain Rope Light", "power_watts": 15, "quantity": 1},
        {"name": "Dressing Ceiling Light", "power_watts": 9, "quantity": 2},
        {"name": "Bathroom Ceiling Light", "power_watts": 9, "quantity": 2},
        {"name": "Bathroom Exhaust Fan", "power_watts": 40, "quantity": 1}
      ]
    },
    {
      "circuit_id": "outlets_2",
      "description": "Bedroom wall outlets",
      "loads": [
        {"name": "Wall Outlet", "power_watts": 1800, "quantity": 4},
        {"name": "TV Outlet", "power_watts": 200, "quantity": 1},
        {"name": "Accessory Outlet", "power_watts": 200, "quantity": 1}
      ]
    },
    {
      "circuit_id": "ac_3",
      "description": "Air conditioner",
      "loads": [
        {"name": "Air Conditioner", "power_watts": 1800, "quantity": 1}
      ]
    }
  ]
}
```

This example is intended to show the eventual composition model and is not part of the initial v1.0 single-circuit implementation.

---

## Out of Scope (Future Phases)

The following features are explicitly out of scope for v1.0:

| Feature | Reason | Target Phase |
| :--- | :--- | :--- |
| Multi-circuit panel design | Requires circuit grouping and parent breaker logic | Phase 2 |
| Main breaker sizing across all circuits | Depends on system-level aggregation | Phase 2 |
| Detailed load diversity factors | Requires richer electrical engineering rules | Phase 2 |
| Motor starting current and inrush modeling | More advanced electrical behavior model | Phase 2 |
| Full compliance to local code standards | Requires jurisdiction-specific rules and validation | Future |
| UI dashboard for interactive editing | Initial release focuses on backend algorithm | Phase 2 |
| REST API wrapper | Can follow once core algorithm is stable | v1.5 |

---

## Known Risks & Open Questions

### Technical Risks

| Risk | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Load assumptions vary by appliance** | Misleading results if wattages are rough | Use configurable explicit wattage values; allow presets later |
| **Breaker sizing is context-dependent** | Different regions use different design rules | Keep v1.0 as a recommendation engine with clear safety note |
| **Voltage drop modeling may be too simplistic** | Could understate practical circuit issues | Keep wire effects advisory in v1.0; improve later |
| **Appliance presets may be inconsistent** | Different users may interpret names differently | Use canonical labels and allow override values |

### Confirmed Decisions
1. **Single-circuit algorithm first**
   - Focus on one circuit before designing a multi-circuit panel system

2. **Use watts and quantity as the core input model**
   - Simple and intuitive for early backend/UI use

3. **Breaker recommendation uses a standard safety margin**
   - Keep default rule simple and transparent

4. **Wire inputs are optional advisory factors**
   - Do not overcomplicate v1.0 with full electrical code compliance

---

## Assumptions

1. The service is a planning and estimation tool, not a final certified electrical design engine
2. Appliance loads are expressed in watts for v1.0
3. Voltage is assumed to be single-phase nominal 240V unless otherwise stated
4. Breaker recommendation is advisory and intended for general planning
5. The service is stateless and accepts one calculation request at a time

---

## Next Steps / Action Items

- [ ] Define the canonical appliance preset catalog and default wattage values
- [ ] Decide whether breaker sizing rules will be configurable per region or fixed for v1.0
- [ ] Define the initial Python module structure and function signatures
- [ ] Draft unit tests for valid/invalid input and breaker recommendation logic
- [ ] Prototype JSON request/response handling for the first backend function

---

## Approval Sign-Off

| Role | Name | Date | Signature |
| :--- | :--- | :--- | :--- |

# Electrical Circuit Load Calculator - Prompts Register

This file maintains a log of prompts, clarifications, and implementation decisions for the Electrical Circuit Load Calculator module.

---

## Prompt #1: Initial Specification Draft

**Date:** 2026-07-20  
**Status:** Completed

### Prompt Summary
User requested the initial specification for a backend service that calculates electrical circuit load from common appliances such as lights, fans, lamps, screens, air conditioners, and exhaust fans. The scope includes optional wire characteristics, voltage input with default 240V and tolerance, and output for total load and breaker rating.

### Key Requirements from Prompt
- Core service should be a pure function with defined inputs and outputs
- Input appliances and quantities
- Optional wire factors: gauge, material, distance, operating temperature
- Voltage input with default 240V and tolerance handling
- Output should include total load and recommended breaker rating
- Later phases will expand to multi-circuit and main-breaker design

### Response / Action Taken
✅ Created the initial PRD document for the electrical load calculator using a structure similar to the first backend API module.

### Open Decisions Pending
1. Appliance preset catalog and default wattage values
2. Breaker sizing rule configuration
3. Whether wire-related calculations should influence breaker recommendation in v1.0
4. Whether the future multi-circuit layer should support preset room templates such as bedroom-with-bath examples

---

## References

- **PRD Document:** [Spec/Spec-Ele-Circuit-Load-Calculator.md](Spec/Spec-Ele-Circuit-Load-Calculator.md)

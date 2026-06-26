# Product Requirements Document: SheetCuts Module

## Document Metadata

| Field | Value |
| :--- | :--- |
| **Project Name** | SheetCuts - Sheet Optimization & Layout Engine |
| **Module ID** | CORE-01-SheetCuts |
| **Target Launch Date** | 2 weeks (ASAP) |
| **Status** | Draft - Under Review |
| **Authors** | AI-Driven Architecture Team |
| **Version** | 0.1 |

---

## Executive Summary & Goals

### Product Vision
SheetCuts is a geometry-based sheet optimization engine that automatically layouts rectangular cutting pieces onto standard or custom sheet sizes, minimizing material wastage. The module calculates the minimum number of sheets required to fulfill all requested sizes and provides a visual representation with labeled cuts, dimensions, and unit information.

### Business Objectives
- Reduce material waste in manufacturing/woodworking/material cutting workflows by 15-30%
- Accelerate layout planning from manual hours to sub-second computation
- Provide a reusable optimization core that will serve as a foundation for REST APIs and integrations

### Success Metrics (KPIs)
- **Optimization Efficiency:** Achieve packing efficiency ≥ 85% for typical use cases
- **Performance:** Process up to 1000 cutting items in < 5 seconds
- **Accuracy:** 100% compliance with geometric constraints and no overlapping cuts
- **Error Handling:** All invalid inputs caught and reported with clear error messages
- **Code Quality:** ≥ 80% unit test coverage with no blocking bugs at launch

---

## Target Audience & User Personas

### Primary Users
1. **Woodworking Professionals** - Cabinet makers, furniture builders needing optimal material usage
2. **Manufacturing Engineers** - Sheet metal, glass, or plastic cutting operations
3. **Logistics & Inventory Managers** - Planning material requirements
4. **API Consumers** - Backend systems integrating SheetCuts via REST endpoints (future phase)

### Secondary Users
- CAD/design software integrations needing embedded optimization
- E-commerce platforms offering custom cutting services

### User Pain Points
- Manual layout planning is time-consuming and error-prone
- Difficult to visualize cut arrangements before execution
- Wastage leads to cost overruns in material-intensive businesses
- No standardized tool available for quick "what-if" scenarios

---

## Functional Requirements

| Req ID | Feature | User Action / Capability | Acceptance Criteria | Priority |
| :--- | :--- | :--- | :--- | :--- |
| FR-01 | Input: Sheet Dimensions | User provides sheet size (W × H) or uses default 48" × 96" | System accepts dimensions in inches or mm; defaults to 48×96 inches if not provided | P0 |
| FR-02 | Input: Unit System Selection | User selects unit system (inches or millimeters) | System applies selected unit consistently to all inputs/outputs; displayed in final diagram | P0 |
| FR-03 | Input: Sheet Type (Homogenous) | User specifies sheet is homogenous (isotropic) | System allows and automatically applies 90° rotation to cutting pieces if it improves packing efficiency; rotation choice is deterministic and always optimizes | P0 |
| FR-04 | Input: Sheet Type (Directional) | User specifies sheet has directional features (e.g., grain, pattern, texture running along width or height) | System shows alignment options: "Align Width with Sheet Width" or "Align Width with Sheet Height"; applies constraint to all cuts | P0 |
| FR-05 | Input: Cutting Sizes - Single | User provides cutting size as "Width × Height" with optional label | System accepts format like "10×20" or "10×20:CustomLabel"; auto-generates labels (P1, P2, etc.) if not provided | P0 |
| FR-06 | Input: Cutting Sizes - Repeated | User specifies a size should be cut n times (e.g., "10×20:×3" or "10×20:Label×3") | System creates labeled variants: "Label_1", "Label_2", "Label_3"; processes as separate cutting instances | P0 |
| FR-07 | Input: JSON Format | User/API provides all input data in standardized JSON structure | System correctly parses JSON per specification (see section "Data Format Specifications"); validates schema | P0 |
| FR-16 | Output: API Documentation | System generates extractable API documentation from code | All public functions, classes, and modules include Google-style docstrings with type hints; Sphinx generates HTML/PDF docs automatically without manual effort | P0 |
| FR-08 | Optimization: Packing Algorithm | System receives list of cutting sizes and sheet size | System generates optimal layout using guillotine or best-fit 2D bin packing algorithm; minimizes total sheets needed | P0 |
| FR-09 | Output: Sheet Count | System calculates minimum sheets required | Returns integer count in JSON response | P0 |
| FR-10 | Output: Layout Diagram (HTML) | System generates visual representation of optimized layout | HTML includes: sheet outlines, labeled cutting pieces as boxes/rectangles, dimensions (width/height), sheet size, unit system; returned embedded in JSON response | P0 |
| FR-11 | Output: Detailed Layout Map | System provides JSON output with per-sheet breakdown | Each sheet contains list of cuts with coordinates (X, Y, W, H); allows programmatic access to layout | P1 |
| FR-12 | Error: Negative/Zero Sizes | User provides size ≤ 0 | System rejects with descriptive error; identifies which size failed | P0 |
| FR-13 | Error: Oversized Items | User provides cutting size larger than sheet size | System rejects with descriptive error; suggests sheet upsizing or item splitting (not auto-implemented) | P0 |
| FR-14 | Error: Invalid Input Format | User provides malformed JSON or invalid schema | System returns HTTP 400 (or Python exception) with schema validation details | P1 |
| FR-15 | Labeling: Auto-Generation | When user doesn't provide labels, system auto-generates | Labels follow pattern: sort by descending area, name as P1, P2, ... (P = Piece); running counter for duplicates (P1_a, P1_b, P1_c for 3× P1) | P1 |

---

## Non-Functional Requirements

### Performance
- **Response Time:** Process up to 1000 items in < 5 seconds on standard hardware (Intel i5, 8GB RAM)
- **Memory Efficiency:** No memory bloat; linear scaling with item count
- **Algorithm Complexity:** O(n log n) or better preferred for packing

### Reliability & Correctness
- **Geometric Accuracy:** All cuts placed without overlap; all within sheet boundaries ±0.01 units
- **Deterministic Output:** Same input always produces same optimal output
- **No Data Loss:** All requested cuts appear in output or error is raised

### Code Quality & Maintainability
- **Language:** Pure Python (no compiled extensions)
- **Python Version:** 3.14+ compatible
- **Standard Libraries Only:** Core logic uses only stdlib + one chosen math library (scipy/numpy or equivalent)
- **Code Style:** PEP 8 compliant; type hints on all functions
- **Modularity:** Separate modules for: input validation, packing algorithm, output generation, visualization
- **API Documentation:** Google-style docstrings on all public functions, classes, and modules; extractable by Sphinx for automatic HTML/PDF generation
- **Documentation Generation:** Sphinx with `sphinx-rtd-theme` and `napoleon` extension; developers write docstrings once; docs auto-generated
- **Doc Locations:** Generated docs in `docs/build/html/`; README includes API snapshot

### Testing
- **Unit Test Coverage:** ≥ 80% code coverage
- **Test Categories:** Optimization correctness, edge cases (negative sizes, sheet boundary), performance (1000+ items), error handling, output accuracy
- **Regression:** All test cases retain status on every commit

### Security & Privacy
- **Input Validation:** Strict schema validation; reject any unexpected fields
- **No Sensitive Data:** Module processes only numeric dimensions; no personal data storage
- **Future API Security:** Compatible with standard authentication (API key, OAuth) when exposed as REST

---

## Data Format Specifications

### Input JSON Schema

```json
{
  "sheet": {
    "width": 48,
    "height": 96,
    "units": "inches",
    "type": "homogenous"
  },
  "sheet_alignment": "width_with_sheet_width",
  "cutting_pieces": [
    {
      "width": 10,
      "height": 20,
      "label": "TopPanel",
      "quantity": 1
    },
    {
      "width": 12,
      "height": 18,
      "label": "Shelf",
      "quantity": 3
    },
    {
      "width": 6,
      "height": 15,
      "quantity": 1
    }
  ]
}
```

**Key Notes:**
- `sheet.type`: "homogenous" (allows rotation) or "directional"
- `sheet_alignment`: Only required if `sheet.type` == "directional"; values: "width_with_sheet_width" or "width_with_sheet_height"
- `cutting_pieces[].quantity`: Optional; defaults to 1 if omitted
- `cutting_pieces[].label`: Optional; system auto-generates if not provided
- `sheet.units`: Optional; defaults to "inches" if omitted; allowed values: "inches", "millimeters"

### Output JSON Schema

```json
{
  "success": true,
  "summary": {
    "total_sheets_required": 2,
    "total_area_requested": 8750,
    "total_sheet_area_available": 9216,
    "utilization_percentage": 95.0,
    "units": "inches",
    "sheet_dimensions": { "width": 48, "height": 96 }
  },
  "layouts": [
    {
      "sheet_id": 1,
      "cuts": [
        {
          "label": "TopPanel",
          "x": 0,
          "y": 0,
          "width": 10,
          "height": 20
        },
        {
          "label": "Shelf_1",
          "x": 10,
          "y": 0,
          "width": 12,
          "height": 18
        }
      ]
    }
  ],
  "html_diagram": "<svg>...</svg>",
  "metadata": {
    "generated_at": "2026-06-26T10:30:00Z",
    "algorithm_used": "guillotine_best_area_fit",
    "execution_time_ms": 245
  }
}
```

### Error Response JSON Schema

```json
{
  "success": false,
  "error": {
    "code": "INVALID_SIZE",
    "message": "Cutting piece 'TopPanel' has width 100, which exceeds sheet width 48",
    "details": {
      "offending_piece": "TopPanel",
      "issue": "dimension_exceeds_sheet"
    }
  }
}
```

---

## Error Handling & Edge Cases

| Scenario | Handling Strategy | Error Code | User Message |
| :--- | :--- | :--- | :--- |
| Negative or zero width/height | Reject input | `INVALID_SIZE` | "Width and height must be positive numbers" |
| Cutting size larger than sheet | Reject input | `SIZE_EXCEEDS_SHEET` | "Cutting piece '{label}' exceeds sheet dimensions. Provide a larger sheet or resize the piece." |
| Empty cutting_pieces array | Accept (valid edge case) | `SUCCESS` | Return 0 sheets required; empty layout |
| Non-numeric dimensions | Reject input | `INVALID_TYPE` | "All dimensions must be numbers" |
| Malformed JSON | Reject input | `INVALID_JSON` | "Request body is not valid JSON" |
| Missing required fields | Reject input | `MISSING_FIELD` | "Field '{field_name}' is required" |
| Invalid unit system | Reject input | `INVALID_UNITS` | "Units must be 'inches' or 'millimeters'" |
| Invalid sheet type | Reject input | `INVALID_SHEET_TYPE` | "Sheet type must be 'homogenous' or 'directional'" |
| Impossible packing (many items, small sheet) | Return result with N sheets | `SUCCESS` | Return accurate sheet count; no artificial limit |

---

## HTML Diagram Specifications

The HTML output (embedded in JSON response) should render as an interactive or static SVG/Canvas diagram showing:

1. **Sheet Boundaries** - Outer rectangle with labeled dimensions (e.g., "48 × 96 inches")
2. **Cut Outlines** - Each cutting piece as a rectangle with dashed or solid borders
3. **Labels** - Piece label (e.g., "P1", "TopPanel") placed inside or adjacent to each cut
4. **Dimensions** - Width and height dimensions shown for each cut (optional for clutter minimization; can be on hover)
5. **Color Coding** - Optional: different colors for different sheets or piece types
6. **Unit Display** - Unit system prominently shown (e.g., "Diagram Scale: 1 unit = 1 inch")
7. **Legend** - Optional: legend showing piece names and total count

**Format Preference:** SVG (scalable, embedded easily in web, printable)

**Complexity Level (v1.0 - Standard):**
- Sheet outline with labeled dimensions (width × height)
- Each cutting piece as labeled rectangle box
- Individual piece dimensions displayed (width × height) inside or adjacent to each cut
- Unit system prominently displayed (e.g., "Scale: 1 unit = 1 inch")
- Optional: Sheet ID/number if multiple sheets in layout
- NOT included in v1.0: Piece coordinates, waste area visualization, color coding, interactivity (deferred to v2+)

---

## Out of Scope (Future Phases)

The following features are **explicitly out of scope** for v1.0:

| Feature | Reason | Target Phase |
| :--- | :--- | :--- |
| **Roll-Based Cutting Mode** | Different algorithm needed; add input mode flag + output metric (roll length vs. sheet count); requires 2D packing within fixed width | **Phase 2** |
| Multi-sheet complexity analysis (e.g., "which sheet uses most material?") | Scope creep; can be added in v2 | Phase 2 |
| Automatic splitting of oversized items across multiple sheets | Complex geometry; deferred | Phase 2 |
| 3D packing (stacking sheets) | Not required; focus on 2D layout | Future |
| Nesting with curved/polygonal pieces | Requires advanced geometry library | Future |
| GUI/Web Interface | First release is Python module only; UI comes in Phase 2 | Phase 2 |
| REST API wrapper | Scheduled for v1.5 post-core module validation | v1.5 |
| Real-time visualization updates | Can be added after MVP | Phase 2 |
| Historical tracking of optimization requests | Not required for core module | Phase 2 |

---

## Known Risks & Open Questions

### Technical Risks

| Risk | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Packing Algorithm Selection** | Algorithm choice impacts efficiency and performance | ✅ **DECIDED:** Guillotine algorithm (v1.0) - fast O(n log n), deterministic, industry-proven (CNC/laser software standard), expected 80-88% efficiency |
| **Python Performance at 1000 Items** | May exceed 5-second SLA | Profile early; consider algorithmic optimizations; assess if NumPy/SciPy accelerates bottlenecks |
| **Floating-Point Precision** | Coordinates may accumulate rounding errors | Use fixed decimal precision (e.g., 0.01 unit tolerance); represent dimensions as integers internally (scaled mm or tenths of inch) |
| **Algorithm Determinism** | Different runs may produce different (equally optimal) layouts | Document that algorithm is deterministic for identical input; reproducibility is guaranteed |

### Confirmed Decisions

1. **2D Packing Algorithm: Guillotine (v1.0)**
   - ✅ **CONFIRMED** Fast (O(n log n)), deterministic, industry-proven
   - Expected efficiency: 80-88% (meets 85%+ target for most manufacturing cases)
   - Future option: Layer in Best Area Fit for v2.0 optimization

2. **HTML Diagram Complexity: Standard (v1.0)**
   - ✅ **CONFIRMED** Sheet outline + labeled cuts + dimensions + unit display
   - No coordinates, waste visualization, or color coding in v1.0
   - Interactivity deferred to v2+

3. **Rotation Handling for Homogenous Sheets: Always Rotate if Improves**
   - ✅ **CONFIRMED** Algorithm automatically tests both 0° and 90° orientations
   - Always chooses orientation that yields tighter packing (deterministic)
   - Directional sheets: Respects user's alignment choice; rotation disabled

4. **Floating-Point vs. Integer Representation:**
   - Store dimensions as floats or integers (scaled)?
   - **Current Plan:** Accept floats; internally scale to integers for geometric calculations; report back in original units

5. **Standard Math Library Choice:**
   - Use NumPy, SciPy, or pure stdlib?
   - **Decision Needed:** Start with pure stdlib + one library; NumPy recommended for matrix ops if benchmarks require

---

## Assumptions

1. All input sizes and sheet dimensions are **valid, positive numbers** (validation occurs at input layer)
2. Sheet is **rectangular** (no beveled edges, irregular shapes)
3. Cutting pieces are **rectangular** (no rotation constraints beyond 90°)
4. All cuts are **straight-line cuts** (no beveled angles, miters, or curves)
5. **Negligible kerf/blade width** (no gap loss between cuts)
6. User provides inputs **once per optimization request** (stateless, no session persistence)
7. **Optimal = Minimum sheets**; user accepts algorithm's layout (not interactive adjustment)
8. v1.0 assumes **sheet-based cutting only** (fixed width × fixed height); roll-based mode (fixed width, variable length) planned for Phase 2

## Future Capability: Roll-Based Cutting (Phase 2)

**Overview:**
Phase 2 will add support for **roll-based cutting** scenarios where material comes from a roll (paper, fabric, vinyl, etc.). Width is fixed; length is variable and to be determined.

**How it Differs from Sheet Mode:**
- **Sheet mode (v1.0):** Both width and height fixed; output = total sheets required
- **Roll mode (Phase 2):** Width fixed; height infinite/variable; output = total roll length required

**Roll Mode Specifications (Design Brief):**

**Input Changes:**
```json
{
  "sheet": {
    "width": 48,
    "height": 96,
    "units": "inches",
    "type": "homogenous",
    "mode": "sheet"     // NEW: "sheet" or "roll"
  },
  ...
}
```
- When `mode: "roll"`, height parameter represents initial strip height (algorithm can exceed it)
- For rolls: rotation allowed within fixed width constraint (pieces can rotate 90° but must fit in width)

**Algorithm Adjustment:**
- Use 2D bin packing within the fixed width; extend height/length as needed
- Output: Total roll length + strip-by-strip breakdown showing which pieces fit in each horizontal segment

**Output Changes:**
```json
{
  "summary": {
    "roll_mode": true,
    "roll_width": 48,
    "roll_length_required": 287.5,
    "total_area_requested": 8750,
    "total_roll_area_used": 13560,
    "utilization_percentage": 64.5,
    ...
  },
  "strips": [
    {
      "strip_id": 1,
      "height": 96,
      "cuts": [...]
    },
    {
      "strip_id": 2,
      "height": 191.5,
      "cuts": [...]
    }
  ]
}
```

**Rotation Behavior:**
- Homogenous rolls: Pieces can rotate 90° if they fit better within fixed width
- Directional rolls: Respects user alignment choice (e.g., "grain runs along roll length")

---

## Next Steps / Action Items

- [ ] **Finalize algorithm choice** - Research & recommend guillotine vs. other 2D packing algorithms
- [ ] **Create Python project scaffold** - Folder structure, setup.py, dependencies
- [ ] **Define unit tests plan** - Test categories, coverage goals, test data
- [ ] **Prototype HTML diagram generation** - Proof-of-concept SVG renderer
- [ ] **Benchmark performance** - Test with 100, 500, 1000 items; measure runtime
- [ ] **Document internal API** - Packing function signature, coordinate system, rotation handling

---

## Approval Sign-Off

| Role | Name | Date | Signature |
| :--- | :--- | :--- | :--- |
| Product Owner | [To be assigned] | [TBD] | ☐ |
| Technical Lead | [To be assigned] | [TBD] | ☐ |
| Architecture Review | [To be assigned] | [TBD] | ☐ |

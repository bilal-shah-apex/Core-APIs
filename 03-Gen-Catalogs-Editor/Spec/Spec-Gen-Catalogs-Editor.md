# Product Requirements Document: Generic Catalogs Editor

## Document Metadata

| Field | Value |
| :--- | :--- |
| **Project Name** | Generic Catalogs Editor |
| **Module ID** | CORE-03-GenCatalogsEditor |
| **Target Launch Date** | 2 weeks (ASAP) |
| **Status** | Draft - Under Review |
| **Authors** | AI-Driven Architecture Team |
| **Version** | 0.1 |

---

## Executive Summary & Goals

### Product Vision
The Generic Catalogs Editor is a backend-ready module for maintaining reusable catalogs of products, options, or components. It will support item definitions with pricing, metadata, and organization preference rules so other services can select appropriate options based on project type such as Budget, Standard, or Luxury.

### Business Objectives
- Provide a reusable catalog foundation for future services and calculators
- Support cost-aware option selection for different project tiers
- Enable shared appliance presets for the electrical load calculator
- Keep catalog data structured, queryable, and extensible

### Success Metrics (KPIs)
- **Usability:** Catalog entries can be created and retrieved with a simple structured format
- **Flexibility:** The same module can support multiple catalog domains such as appliances, fixtures, and materials
- **Extensibility:** Other modules can consume catalog data without redesign
- **Maintainability:** Catalog schemas are simple and versioned

---

## Target Audience & User Personas

### Primary Users
1. **Product / Specification Managers** - Define standard options and pricing
2. **Developers / Integrators** - Consume catalog data for other modules
3. **Project Teams** - Choose preferred items by project tier

### User Pain Points
- Option lists are often scattered and inconsistent
- Pricing and selection logic are hard to maintain manually
- Different project types need different preferred defaults

---

## Functional Requirements

| Req ID | Feature | User Action / Capability | Acceptance Criteria | Priority |
| :--- | :--- | :--- | :--- | :--- |
| FR-01 | Catalog Item Creation | User creates an item with name, category, and description | System stores a catalog item with a unique identifier | P0 |
| FR-02 | Cost Metadata | User includes cost information | System stores cost as a numeric value and returns it in output | P0 |
| FR-03 | Project Tier Preferences | User assigns preferred tiers such as Budget, Standard, Luxury | System stores tier preference metadata per item | P1 |
| FR-04 | Catalog Lookup | User requests items by category or keyword | System returns matching catalog entries | P0 |
| FR-05 | Selection Recommendation | User requests preferred options for a project tier | System recommends items based on tier preference rules | P1 |
| FR-06 | JSON API Contract | User or service consumes catalog data over JSON | System accepts and returns structured JSON | P0 |
| FR-07 | Extensible Metadata | User adds arbitrary metadata fields | System accepts additional attributes without breaking basic usage | P1 |

---

## Non-Functional Requirements

### Performance
- Catalog lookup should be fast for typical lists of hundreds of items
- Simple filtering and search should complete in under 1 second for common workloads

### Reliability & Correctness
- Data should remain deterministic and traceable
- Invalid data such as negative cost should be rejected

### Code Quality & Maintainability
- Pure Python implementation
- Type hints and clear schemas
- Modular design for storage, validation, and selection logic

---

## Data Format Specifications

### Catalog Item Example

```json
{
  "id": "ceiling-light-led-001",
  "name": "LED Ceiling Light",
  "category": "lighting",
  "description": "Standard LED fixture",
  "cost": 45.0,
  "tags": ["indoor", "energy-efficient"],
  "preferred_tiers": ["Standard", "Luxury"],
  "metadata": {
    "wattage": 18,
    "voltage": 240
  }
}
```

### Selection Request Example

```json
{
  "category": "lighting",
  "project_tier": "Budget"
}
```

### Selection Response Example

```json
{
  "success": true,
  "project_tier": "Budget",
  "items": [
    {
      "id": "ceiling-light-led-001",
      "name": "LED Ceiling Light",
      "cost": 45.0
    }
  ]
}
```

---

## Error Handling & Edge Cases

| Scenario | Handling Strategy | Error Code | User Message |
| :--- | :--- | :--- | :--- |
| Negative cost | Reject input | `INVALID_COST` | "Cost must be a non-negative number" |
| Missing name | Reject input | `MISSING_FIELD` | "Field 'name' is required" |
| Empty catalog | Return empty result | `SUCCESS` | "No items found" |
| Unsupported tier | Warn or reject | `INVALID_TIER` | "Project tier is not recognized" |

---

## Out of Scope (Future Phases)

| Feature | Reason | Target Phase |
| :--- | :--- | :--- |
| Full database persistence | Keep initial release simple and portable | Phase 2 |
| User roles and permissions | More complex access control | Phase 2 |
| Advanced search and ranking | Can be layered later | Phase 2 |
| Multi-tenant catalog management | Broader productization requirement | Future |

---

## Next Steps / Action Items

- [ ] Define the initial catalog schema
- [ ] Decide on the first supported catalog domains
- [ ] Create a simple in-memory catalog service for v1.0
- [ ] Link this module to appliance presets in Module 02 later

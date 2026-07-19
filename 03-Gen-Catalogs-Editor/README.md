# Generic Catalogs Editor

A backend-ready catalog management module for defining reusable product or option records that can power selection, cost, and preference logic across other services.

## Scope for v1.0
- Store catalog items with name, category, description, and cost
- Support optional tags and project-tier preferences such as Budget, Standard, and Luxury
- Enable future lookup by category or use case
- Provide a simple foundation for later integration with electrical and design calculators

## Proposed Structure

```text
03-Gen-Catalogs-Editor/
├── Spec/
│   └── Spec-Gen-Catalogs-Editor.md
├── PROMPTS_REGISTER.md
└── README.md
```

## Initial Concepts
- Catalog items can represent appliances, materials, fixtures, or components
- Each item may have cost and preference metadata
- Tier-based selection rules can be layered on top later

## Relationship to Module 02
The electrical circuit load calculator can use catalog entries as preset appliance definitions, while this module manages the master data and selection logic.

# Generic Catalogs Editor - Prompts Register

This file tracks the initial thinking and decisions for the catalog management module.

---

## Prompt #1: Initial Catalog Direction

**Date:** 2026-07-20  
**Status:** Completed

### Prompt Summary
The user proposed that the appliance preset catalog is substantial enough to become its own backend service capable of managing reusable options, cost, and project-tier preferences.

### Key Requirements from Prompt
- Support user-defined catalogs of different types
- Include cost information per option
- Support organization preference rules such as Budget, Standard, and Luxury
- Create a separate module structure so the electrical circuit calculator can reuse catalog data later

### Response / Action Taken
✅ Created a new module folder for a generic catalogs editor and captured initial scope and intent.

### Open Decisions Pending
1. Catalog item schema: name, category, cost, tags, metadata
2. Selection logic for project tiers
3. Whether catalogs will be local JSON-first or database-backed in later phases

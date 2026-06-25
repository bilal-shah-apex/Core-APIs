# Execution Plan: Decoupled AI Agent Modules & Skills Setup

This document outlines the step-by-step implementation plan for a solo Developer/Product Manager to build, manage, and scale modular AI agents using a "Prompts-as-Code" architecture.

---

## 🏗️ Phase 1: Repository Architecture & Directory Mapping
We will decouple core application logic from prompt instructions. This allows your source modules to easily transition into isolated REST APIs (e.g., via FastAPI) later.

### Target Directory Layout
```text
my-project/
├── LICENSE                    # MIT License for frictionless cross-project reuse
├── CONTEXT.md                 # Project context spec for GitHub Copilot
├── EXECUTION_PLAN.md          # This implementation plan
├── ai-skills/                 # 🟢 Central Git Submodule (Shared Prompts)
│   └── prd-creator/
│       └── SKILL.md           # Prescriptive agent workflows & PRD templates
└── src/                       # 🔵 Application Code Base
    └── modules/
        └── prd/               # Decoupled, API-ready module folder
            ├── prd_generator.py # Python logic loading SKILL.md dynamically
            └── requirements.txt # Dependencies specific to this module
```

---

## 📄 Phase 2: Configuration & License Files

### Step 1: Create the `LICENSE` File
Create a `LICENSE` file at the root of the project with the following open-source, flexible text:
```text
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

### Step 2: Create `ai-skills/prd-creator/SKILL.md`
This file acts as the explicit, metric-driven directive for the agent. It enforces structural definitions and prevents scope creep.
```markdown
# Skill: Product Requirements Document (PRD) Creator

## Core Instructions
Evaluate user input. If vague, ask clarifying questions before writing the PRD. Output metrics explicitly (e.g., "Page load under 2s"). Enforce strict boundaries for out-of-scope requirements.

## Required Structure
1. **Metadata:** Project Name, Launch Date, Status, Authors.
2. **Summary & Goals:** Vision, Business Objectives, Success Metrics (KPIs).
3. **Target Audience:** Personas, Pain Points.
4. **Functional Requirements:** Table with Columns: `Req ID` | `User Role` | `Capability` | `Acceptance Criteria` | `Priority (P0/P1)`.
5. **Non-Functional Requirements:** Performance, Security, UI Constraints.
6. **Out of Scope:** Boundaries for future phases.
7. **Risks & Open Questions:** Technical dependencies, third-party API locks.
```

---

## 🐍 Phase 3: Building the API-Ready Source Module

### Step 3: Create `src/modules/prd/requirements.txt`
```text
pydantic
openai
```

### Step 4: Create `src/modules/prd/prd_generator.py`
This script uses strict Pydantic data schemas for its input and output boundaries. It remains entirely framework-agnostic so it can be exposed as a REST endpoint in a few lines of code later.

```python
import os
from pydantic import BaseModel
from openai import OpenAI

# 1. Define Strict Data Contracts (API Request/Response Data Structures)
class PRDInput(BaseModel):
    project_name: str
    raw_notes: str

class PRDOutput(BaseModel):
    markdown_content: str

# 2. Framework-Agnostic Core Logic Module
def generate_prd_from_spec(data: PRDInput) -> PRDOutput:
    # Resolve the absolute path to the central skill directory
    skill_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../ai-skills/prd-creator/SKILL.md")
    )
    
    with open(skill_path, "r") as file:
        skill_instructions = file.read()
        
    client = OpenAI()
    
    # Execute LLM logic combining prompt spec with dynamic inputs
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": skill_instructions},
            {"role": "user", "content": f"Project: {data.project_name}\nNotes: {data.raw_notes}"}
        ]
    )
    
    return PRDOutput(markdown_content=response.choices.message.content)

# 3. Local Execution Target for Testing
if __name__ == "__main__":
    test_input = PRDInput(project_name="Task Tracker", raw_notes="Need email magic links.")
    result = generate_prd_from_spec(test_input)
    print(result.markdown_content)
```

---

## 🛠️ Phase 4: Git Synchronization & Team Operations

Follow these workflows to maintain, share, and update your skills seamlessly across different code repositories.

### Step 5: Establish the Central Submodule Link
1. Host your `ai-skills` directory on GitHub as a standalone repository.
2. Link it into your main application project terminal via:
   ```bash
   git submodule add https://github.com[your-username]/ai-skills.git ai-skills
   git commit -m "chore: add central ai-skills submodule link"
   ```

### Step 6: The Iterative Update Cycle
When you modify or refine code execution prompts over time:
1. Make changes inside your standalone `ai-skills` repo, commit, and push.
2. Pull those central updates down into your live working application instantly using:
   ```bash
   git submodule update --remote --merge
   ```

---
allowed-tools: Read, Grep, Glob
description: AI creates an implementation plan. Review before starting to code.
---

# /_plan Command

Invokes the **planner** agent to create an implementation plan before coding.

## What It Does

1. **Clarify requirements** — Define exactly what needs to be built
2. **Identify risks** — Spot potential issues and blockers
3. **Step-by-step plan** — Break implementation into stages
4. **Await confirmation** — No coding until user approves

## When to Use

- Starting a new feature
- Major architecture changes
- Complex refactoring
- Expecting changes across multiple files/components
- When requirements are ambiguous

## Usage Example

```
/_plan Add user authentication feature

→ planner agent will:
1. Analyze and clarify requirements
2. Design data models
3. Plan key components and modules
4. Establish test strategy
5. Await user confirmation
```

**Important**: No code is written until the user responds positively with "proceed", "confirm", etc.

## Post-processing: Saving the Plan

Once the user confirms the plan, two files are saved to the `.claude_doc/` directory:
- `.claude_doc/prompt_plan.md` — Detailed implementation plan
- `.claude_doc/todo.md` — Checklist (for tracking work progress)

These files can be referenced in subsequent sessions to continue the work.

## Next Steps

| After plan is confirmed | Command |
|:------------------------|:--------|
| Implement with testing | `/_tdd` |
| Auto-execute all at once | `/_auto` |

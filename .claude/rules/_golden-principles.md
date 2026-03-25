# Core Principles

> 11 core principles for clean, maintainable code

## 1. Immutability

**Why?** Mutation is a breeding ground for bugs. You cannot track where a value was changed.

**How:** Create and return new objects. Do not modify originals. Use immutable objects (language-specific patterns: Java record, TypeScript readonly, Python frozen dataclass, Go value types, Rust default immutability). Leverage immutable collections, minimize setters.

## 2. Secrets Belong in Environment Variables

No hardcoding. Inject via environment variables or project config files (`.env`, `config.*`). Throw an exception immediately if missing.

## 3. Test First (TDD)

RED (failing test) → GREEN (minimal implementation) → IMPROVE (refactor). 80%+ coverage.

## 4. Conclusion First, Reasons Later

Lead with the conclusion in the first sentence. "Because..." comes after.

## 5. Small Files, Small Methods

Files: 800-line limit. Methods/functions: 50-line limit. Nesting: 4-level limit. Split if exceeded.

## 6. Validate at System Boundaries

Trust internal code, but validate user input and external API responses. Use each language/framework's validation tools (e.g., JSON Schema, Zod, Pydantic, Bean Validation, etc.).

## 7. Explain with Analogies

Everyday analogy first (1-2 sentences), then the technical explanation.

## 8. Context 50% Rule

Complete work within 50% of the context window. Split large tasks into new sessions.

## 9. HARD-GATE: No Coding Without Design

If any of the following apply, run `/_plan` first: new feature (3+ files), architecture change, API endpoint change, DB schema change. No code until user approval. Exception: simple fixes (1-2 files, typo/bug patches).

## 10. Evidence-Based Completion

"It's done" is false without evidence. Before claiming completion, you must:
1. Present test results (pass/fail counts, coverage)
2. Confirm build success (run it directly)
3. Cross-check against requirements checklist with evidence
4. If `.claude_doc/todo.md` exists, check completed items as `- [x]` and briefly note the evidence

**Prohibited**: "It should work", "There shouldn't be any issues" — speculative completion claims
**Required**: "12 tests passed", "Build succeeded (0 errors)" — execution evidence

**todo.md rule**: If `.claude_doc/todo.md` exists, reference it at task start, and update each item to `- [x]` upon completion. Work is complete when all items are checked.

## 11. SDD Review Enforcement

For sub-agent-based development: spec compliance first, issue found = incomplete, "almost done" does not pass.

## 12. Follow Project Spec

If `_SPEC.md` exists at the project root, it must be referenced.
- Defines project-specific rules for folder structure, naming conventions, extension rules, API patterns, etc.
- _SPEC.md (coding rules) takes precedence over CLAUDE.md (project overview) for specific coding style
- If _SPEC.md does not exist, follow rules/_coding-style.md default rules

---

## No Excuses (These excuses do not fly)

| Principle | Excuse | Reality |
|-----------|--------|---------|
| TDD | "Too simple to need tests" | Simple code breaks too. Tests take 30 seconds |
| TDD | "I'll add tests later" | Later tests only cover happy paths |
| Immutability | "Need mutation for performance" | Only if proven by profiling |
| Secrets | "It's fine, it's a test environment" | Committed test secrets are permanently exposed |
| File size | "It's small enough" | Review for splitting above 400 lines |
| HARD-GATE | "Quick fix, no plan needed" | 3+ file changes = plan first |
| Evidence | "It already works fine" | Claims without evidence are false |

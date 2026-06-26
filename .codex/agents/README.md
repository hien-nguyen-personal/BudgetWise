# BudgetWise Codex Developer Team

This directory defines the project-scoped Codex agents for BudgetWise. Each TOML file defines one custom agent. Spawn them explicitly when you want a multi-agent workflow.

## Team Roles

1. `architect`
   - Owns design direction, module boundaries, data flow, future expansion strategy, and technical tradeoffs.
   - Read-only by default. Produces design decisions and implementation plans, not code changes.

2. `software_engineer`
   - The only implementation-focused agent on the team.
   - Makes production code changes after scope and design are clear.
   - Does not create or update tests unless explicitly instructed; the tester owns test code.

3. `tester`
   - Owns all test design and test implementation.
   - Writes standard-library Python tests for models, storage, insights, validation, and CLI behavior.
   - Avoids production-code edits unless the parent task explicitly asks for a testability change.

4. `reviewer`
   - Reviews code for correctness, clean code, maintainability, design consistency, and test coverage.
   - Read-only by default. Leads with concrete findings and file references.

5. `commit_manager`
   - Owns git hygiene, staging decisions, and commit preparation after work is verified.
   - Writes clear, focused commit messages and protects unrelated user changes.
   - Commits only after explicit user or parent-agent approval.

## Recommended Workflow

Learning-first mode:

```text
Preserve AGENTS.md, SESSION_STATE.md, .codex/config.toml, and .codex/agents/.
Coach the user through design, debugging, and review by default.
Avoid writing production app code unless the user explicitly asks for implementation.
When implementation is requested, keep changes small and explain the reasoning.
```

For feature work:

```text
Ask architect to design the change.
Ask software_engineer to implement the approved design.
Ask tester to write or update tests for the changed behavior.
Ask reviewer to review the final diff.
Ask commit_manager to prepare and create the approved commit.
```

For small fixes:

```text
Ask software_engineer to make the smallest safe change.
Ask tester to cover the bug with tests.
Ask reviewer to inspect the final result.
Ask commit_manager to commit the verified fix when approved.
```

For design-heavy work:

```text
Spawn architect and reviewer first to compare design risks.
Then hand the chosen approach to software_engineer.
Then ask tester to add coverage.
Then ask reviewer and commit_manager to review and commit the final result.
```

## BudgetWise Project Standards

- Keep the application beginner-friendly and object-oriented.
- Use only Python standard library modules.
- Preserve `items.json` compatibility and treat it as user data.
- Keep responsibilities split across `main.py`, `item.py`, `storage.py`, and `insights.py` unless the architect recommends a change.
- Prefer small, focused changes over broad rewrites.
- Validate with `py_compile` and, when tests exist, `python3 -m unittest`.
- Prefer one logical change per commit, with production code and directly related tests committed together.
- Do not commit local app data such as `items.json` unless explicitly requested.

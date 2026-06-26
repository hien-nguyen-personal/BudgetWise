# BudgetWise Agent Notes

## Project Overview

BudgetWise is a minimal command-line budgeting app written in Python. It lets users add purchases, view saved items, and see spending insights by category and store.

The project intentionally uses only the Python standard library.

This repository also preserves a learning-first agentic workflow. The user may wipe application code and rebuild BudgetWise manually to learn how the app works from the ground up, so preserve the workflow files and prefer coaching over AI-generated production code unless implementation is explicitly requested.

## File Structure

- `AGENTS.md`: project agent instructions and workflow rules. Preserve this file during clean-start resets.
- `.codex/config.toml`: project-level Codex agent settings. Preserve this file during clean-start resets.
- `.codex/agents/`: project-scoped custom Codex agents for the BudgetWise software team. Preserve this directory during clean-start resets.
- `main.py`: CLI menu, user prompts, input validation, and application flow. May be absent after a clean-start reset until the user rebuilds it.
- `item.py`: `Item` data model plus conversion to and from JSON records. May be absent after a clean-start reset until the user rebuilds it.
- `storage.py`: JSON persistence for loading and saving items. May be absent after a clean-start reset until the user rebuilds it.
- `insights.py`: spending calculations and grouped totals. May be absent after a clean-start reset until the user rebuilds it.
- `items.json`: local app data. Treat this as user data and avoid deleting or overwriting it unless explicitly requested.
- `README.md`: short project readme.
- `SESSION_STATE.md`: session handoff notes. Read this after `AGENTS.md` at the start of a session, and update it before ending a session.
- `tests/`: standard-library tests. May be absent after a clean-start reset until the user rebuilds or asks for tests.

## Development Commands

Run the app:

```bash
python3 main.py
```

Compile-check the modules without writing cache files outside the workspace when these modules exist:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/budgetwise_pycache python3 -m py_compile main.py item.py storage.py insights.py
```

## Coding Guidelines

- Keep the code beginner-friendly, readable, and object-oriented.
- Keep responsibilities separated across the existing modules.
- Use comments and docstrings only where they clarify intent.
- Do not add external dependencies.
- Preserve JSON compatibility for stored `Item` records.
- Keep validation simple and friendly for command-line users.

## Learning-First Collaboration

- The user is rebuilding BudgetWise to learn coding without AI-generated production code.
- Default to explanations, architecture guidance, debugging help, review comments, small exercises, and pseudocode.
- Do not write or replace production app files unless the user explicitly asks for implementation.
- If implementation is explicitly requested, keep changes small, explain the reasoning, and preserve the beginner-friendly style.
- When the user shares code they wrote, review and explain it before offering rewritten code.

## Clean-Start Preservation

Preserve these workflow files and directories during any app-code wipe:

- `AGENTS.md`
- `SESSION_STATE.md`
- `.codex/config.toml`
- `.codex/agents/`

These app files may be deleted or recreated only when the user explicitly asks:

- `main.py`
- `item.py`
- `storage.py`
- `insights.py`
- `tests/`

Do not delete, overwrite, or reset `items.json` unless the user explicitly requests that local data be removed.

## Expansion Notes

The current design should stay easy to extend later with:

- Edit item
- Delete item
- Search or filter items
- Monthly spending reports
- GUI or web frontend

Prefer small, focused changes that keep the CLI behavior predictable.

## Session Handoff

- At the start of each session, read `SESSION_STATE.md` after this file if it exists.
- Before ending a session, update `SESSION_STATE.md` with progress, current work, next steps, verification results, open decisions, and git status notes.
- Keep handoff notes concise, factual, and current.
- If `SESSION_STATE.md` conflicts with the actual working tree, trust the working tree and update the handoff file.

## Codex Team Roles

This repo defines five project-scoped custom agents:

- `architect`: oversees design, architecture, module boundaries, and future expansion strategy.
- `software_engineer`: the single implementation owner for production-code changes.
- `tester`: owns all test design and test implementation.
- `reviewer`: reviews all code for correctness, clean code, design consistency, and test coverage.
- `commit_manager`: owns git hygiene, staging decisions, commit messages, and final commits after approval.

Use these agents explicitly when a task benefits from parallel or specialized review.

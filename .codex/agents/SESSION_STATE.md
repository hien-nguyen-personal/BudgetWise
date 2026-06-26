# BudgetWise Session State

Last updated: 2026-06-26

## How To Use This File

- At the start of a new Codex session, read this file after `AGENTS.md`.
- At the end of a session, update this file with current progress, active work, next steps, verification status, open decisions, and git status.
- Keep this file concise and factual so the next session knows exactly where to resume.

## Current Progress

- Preserved the project agentic workflow for a learning-first rebuild.
- Updated `AGENTS.md` with clean-start preservation rules and learning-first collaboration guidance.
- Updated `.codex/agents/README.md` with the learning-first workflow.
- Updated `software_engineer` and `tester` agent specs so they avoid writing app or test code during learning sessions unless explicitly asked.
- Created global Codex steering files from the workflow:
  - `/Users/hiennguyen/.codex/AGENTS.md`
  - `/Users/hiennguyen/.codex/SESSION_STATE.md`
  - `/Users/hiennguyen/.codex/agents/README.md`
  - `/Users/hiennguyen/.codex/agents/architect.toml`
  - `/Users/hiennguyen/.codex/agents/software-engineer.toml`
  - `/Users/hiennguyen/.codex/agents/tester.toml`
  - `/Users/hiennguyen/.codex/agents/reviewer.toml`
  - `/Users/hiennguyen/.codex/agents/commit-manager.toml`
- Added global `[agents]` settings to `/Users/hiennguyen/.codex/config.toml`.
- Global steering now instructs each project that uses the agentic workflow to create and maintain its own project-local `SESSION_STATE.md`.
- Generalized the global steering files so they are project-agnostic and removed BudgetWise-specific defaults from `/Users/hiennguyen/.codex/AGENTS.md`.
- Confirmed the full reusable agent instructions live in `/Users/hiennguyen/.codex/agents/*.toml`.
- Confirmed the workflow structure exists:
  - `AGENTS.md`
  - `SESSION_STATE.md`
  - `.codex/config.toml`
  - `.codex/agents/architect.toml`
  - `.codex/agents/software-engineer.toml`
  - `.codex/agents/tester.toml`
  - `.codex/agents/reviewer.toml`
  - `.codex/agents/commit-manager.toml`
  - `.codex/agents/README.md`
- A partial app-code/data wipe is now visible in the working tree: `main.py`, `item.py`, `insights.py`, and `items.json` are deleted. `storage.py`, `README.md`, `AGENTS.md`, `SESSION_STATE.md`, and `.codex/` remain.
- No commit has been made yet.

## Current Work

- The user plans to wipe coding files and rebuild BudgetWise manually to learn.
- Future sessions should preserve the workflow files and coach by default instead of generating production code.
- No agent is currently running.

## Verification

Current-session verification:

```bash
git diff --check
```

Result: passed.

Global steering readback:

```bash
find /Users/hiennguyen/.codex/agents -maxdepth 1 -type f -print
sed -n '1,220p' /Users/hiennguyen/.codex/AGENTS.md
sed -n '1,180p' /Users/hiennguyen/.codex/SESSION_STATE.md
tail -n 20 /Users/hiennguyen/.codex/config.toml
rg "SESSION_STATE|name =" /Users/hiennguyen/.codex/agents
rg -n "BudgetWise|items\\.json|main\\.py|item\\.py|insights\\.py|storage\\.py" /Users/hiennguyen/.codex/AGENTS.md /Users/hiennguyen/.codex/SESSION_STATE.md /Users/hiennguyen/.codex/agents
```

Result: passed. The global agent files, global steering file, global session-state template, global config `[agents]` settings, and agent session-state references are present. No BudgetWise-specific strings remain in the global steering files.

```bash
python3 -c "import pathlib, tomllib; [tomllib.loads(p.read_text()) for p in pathlib.Path('.codex/agents').glob('*.toml')]; print('toml ok')"
```

Result: not run successfully because this local Python environment does not have `tomllib`.

No app tests or compile checks were run in this session because only workflow documentation and agent instructions were changed.

## Open Decisions And Risks

- Decide whether to commit the workflow files before wiping app code so the agent structure is safely recoverable through git.
- If wiping coding files, preserve `AGENTS.md`, `SESSION_STATE.md`, `.codex/config.toml`, and `.codex/agents/`.
- `items.json` currently shows as deleted in git status. Confirm this was intentional before committing, because project guidance treats it as local app data.
- `storage.py` remains present after the partial wipe.

## Git Status Notes

Most recent `git status --short` before this handoff showed:

```text
 D insights.py
 D item.py
 D items.json
 D main.py
?? .codex/
?? AGENTS.md
?? SESSION_STATE.md
```

Treat `.codex/`, `AGENTS.md`, and `SESSION_STATE.md` as intentional workflow configuration. Treat `items.json` as local app data unless the user explicitly asks otherwise.

## Suggested Next Steps

1. Decide whether the visible deletion of `items.json` was intentional.
2. Commit or otherwise back up the workflow files before more cleanup.
3. If resetting for learning, remove only app code/test files the user chooses to rebuild.
4. Rebuild BudgetWise one small feature at a time with coaching, review, and debugging support.

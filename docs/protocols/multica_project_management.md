# Multica Project Management Protocol

## Workspace Model

- Workspace: `AIWealthOffice`.
- Multica projects are sprint/phase containers inside the workspace:
  - `P0 - Bootstrap`
  - `P1 - Foundation`
  - future `P2 - ...`
- The GitHub repo resource should be attached to each project.

## Issue Flow

1. New work starts as `backlog`.
2. CEO/PM promotes selected work to `todo` / `in_progress`.
3. Worker runs and posts output.
4. CEO validates physically.
5. Passed work becomes `done`; abandoned process experiments become `cancelled`.

## Planning Discipline

- Do not leave completed experiments in active planning columns.
- Use `backlog` for待规划 work, especially complex design tasks.
- Link each issue to a project before dispatch.
- Prefer small, explicit issue descriptions; rely on session resume only for same-issue continuation.

## Context Ownership

- PM owns the issue graph: related issues, project links, backlog hygiene, session-continuity metadata.
- CEO owns final execution policy: fresh vs resume vs fork vs force-fresh, worker selection, acceptance/rework.

## Current Rule

Role prompt redesign is complex and starts as backlog issue `AIW-23` under `P1 - Foundation`; do not implement until the consultant proposal is reviewed.

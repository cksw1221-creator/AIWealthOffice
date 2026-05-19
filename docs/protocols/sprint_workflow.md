# Sprint Workflow — AI Wealth Office Multica Projects

## Overview

Multica projects act as sprint containers. Each project contains issues that move through a defined lifecycle from backlog to completion or cancellation.

## Issue Lifecycle

```
backlog → todo → in_progress → in_review → done
                                          ↘ cancelled
```

| Status | Meaning |
|--------|---------|
| `backlog` | New work received; not yet activated |
| `todo` | PM has recommended it; CEO not yet approved |
| `in_progress` | CEO approved; worker actively executing |
| `in_review` | Worker delivered output; CEO physically verifying |
| `done` | Passed QC; work accepted |
| `cancelled` | Abandoned experiment; no further action |

## Project / Issue Flow

### 1. PM Recommends

PM creates an issue in `backlog` with:

- `project_id` — which sprint/project it belongs to
- `can_parallel_with` — which issues can run concurrently
- `blocked_by` — dependencies that must complete first
- `recommended_worker` — which coder agent (from worker registry)
- `session_mode` — fresh | resume | fork | force-fresh
- `cost_rationale` — why this worker tier is appropriate

### 2. CEO Approves Activation

CEO reviews PM's recommendation and either:

- **Approves**: Posts `LGTM` or `approved` comment → issue promoted to `todo`, then `in_progress`
- **Rejects**: Requests changes via comment → issue stays in `backlog`

CEO also decides the `session_mode` (fresh/resume/fork/force-fresh) based on complexity and continuity needs.

### 3. Worker Executes

Worker picks up the issue, produces output, and posts results as a comment on the issue.

### 4. CEO Validates

CEO physically runs the acceptance checks (QC runner, verification commands). If:

- **Passes**: CEO marks `done`
- **Fails**: CEO requests rework → worker continues on same issue, status stays `in_progress`

## Experiment Exclusion Rule

Completed experiments (status `done` or `cancelled`) **must not appear in active planning views**.

Active work queries filter: `status NOT IN ('done', 'cancelled')`

Rationale: Done/cancelled issues represent historical output, not upcoming work. Keeping them out of active views reduces noise and maintains focus on real backlog.

**How to exclude:**
- Use `multica issue list --status backlog` for pending work
- Use project-level list filtered by active status for sprint planning
- Do not mix completed experiments into active task boards

## Worker Selection (from worker_registry.json)

| Worker | Cost Tier | Use For |
|--------|-----------|---------|
| Coder-gpt-5.5-high-Consultant | consultant_expensive | Hard architecture, ambiguous decisions, CEO escalation |
| Coder-gpt-5.4-high-Builder | main_worker | Important implementation, review, integration |
| Coder-gpt-5.4-medium-Builder | main_worker | Normal coding, tests, refactors |
| Coder-minimax-m2.7-default-Junior | junior | Simple docs, formatting, low-risk chores |

PM recommends the worker tier. CEO may override.

## Session Mode Definitions

| Mode | When to Use |
|------|-------------|
| `fresh` | New task, no prior context needed, no continuity risk |
| `resume` | Same issue continuing, want to preserve prior agent memory |
| `fork` | Offshoot from main issue, experimental branch |
| `force-fresh` | Prior attempt stuck or corrupted, discard and start clean |

## QC Preservation

QC runner and pass criteria (7/7 PASS) are preserved from prior sprints. Any new work must pass the same QC checks before being marked `done`.

## Backlog Hygiene

- Keep backlog items lean and explicit
- Link each issue to a project before dispatch
- Do not leave completed experiments in active columns
- Use `backlog` for complex design tasks not yet ready for execution
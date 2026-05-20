# CEO Workflow

These scripts turn the local `ga_multica` adapter into a minimal CEO control loop for dispatching, monitoring, accepting, and reworking Multica issues from the repo root on Windows.

## Preconditions

- Run commands from the repository root: `C:\Users\ChenKun\Project\GenericAgent\temp\AIWealthOffice`
- `multica` must already be installed and authenticated.
- Worker routing is sourced from `workspace/worker_registry.json`.

## Dispatch Work

Create a new issue from inline text:

```powershell
python scripts/ceo_dispatch.py `
  --title "Implement portfolio analytics export" `
  --worker "Coder-gpt-5.4-medium-Builder" `
  --description "Build CSV export for portfolio analytics. Keep quant MVP intact." `
  --session-mode fresh `
  --priority high `
  --status todo
```

Create a new issue from a markdown file:

```powershell
python scripts/ceo_dispatch.py `
  --title "Refine task lifecycle docs" `
  --worker "a29c8d6f-fa67-4047-bcf2-93ef4bbd1412" `
  --description-file docs/templates/issue_coder_task.md `
  --session-mode resume
```

Expected output:

```json
{"id":"<issue-uuid>","identifier":"AIW-123","session_mode":"resume"}
```

## Watch Progress

Summarize the latest issue state:

```powershell
python scripts/ceo_watch.py AIW-123
```

Fetch only new run messages after a known sequence number:

```powershell
python scripts/ceo_watch.py AIW-123 --since-seq 40
```

Print raw JSON instead of the text summary:

```powershell
python scripts/ceo_watch.py AIW-123 --json
```

## Templates

Use these templates to keep PM preparation, CEO review, and handoff structure consistent:

- `docs/templates/issue_contract.md` - PM issue prep before dispatch or resume
- `docs/templates/acceptance_checklist.md` - CEO/reviewer acceptance gate
- `docs/templates/rework_note.md` - structured rework instruction for the next pass
- `docs/templates/deliverable_handoff.md` - worker/reviewer/secretary output handoff

A practical flow is:

1. PM drafts `issue_contract.md`
2. CEO dispatches from inline text or `--description-file`
3. worker delivers artifacts and verification in the issue thread
4. reviewer and CEO use `acceptance_checklist.md`
5. if needed, CEO issues `rework_note.md`
6. accepted work can be packaged with `deliverable_handoff.md`

## Closure Checklist

Before marking a local package as ready, promoting an issue into execution, or calling an item accepted/done, run the five-layer closure review in `docs/protocols/closure_checklist.md`.

Use it especially when:

- an issue becomes the current entry issue for a sprint
- a local draft becomes `local ready`
- an item is about to move into Multica execution
- acceptance/rework status changes imply planning or metadata updates

This prevents a “main file is done, but metadata/project state is stale” failure mode.

## Accept Work

Approve and close an issue:

```powershell
python scripts/ceo_accept.py AIW-123 `
  --comment "Accepted. Ship this and move to the next sprint item." `
  --session-mode resume
```

This posts a CEO comment through `--content-file` and then sets the status to `done` by default.

## Request Rework

Send the worker back for another pass:

```powershell
python scripts/ceo_rework.py AIW-123 `
  --comment "Rework required: tighten the error handling section and add usage examples." `
  --session-mode force-fresh `
  --status todo
```

Default rework status is `todo` so the issue remains actionable. You can change it to another open state if your workspace uses a different status convention.

## Session Continuity

The CEO scripts now expose an explicit continuity policy:

- `--session-mode fresh`
- `--session-mode resume`
- `--session-mode fork`
- `--session-mode force-fresh`

Dispatch defaults to `fresh`. Accept and rework default to `resume` because they usually operate on an existing issue thread.

Continuity decisions are persisted to `workspace/session_continuity.json` by default. Override the path with `--continuity-file` when testing or when maintaining a separate local workspace state.

For operating guidance on when to pick each mode, see `docs/protocols/session_continuity.md`.
For role boundaries, continuity recommendation ownership, CEO override rules, and accept/rework authority, see `docs/protocols/role_system_v2.md`.

## Notes

- `ceo_dispatch.py` resolves workers by either registry key or `agent_id`.
- `ceo_accept.py` and `ceo_rework.py` use UTF-8 temp files for comments to avoid Windows shell encoding issues.
- `ceo_watch.py` redacts token-like values before printing message previews.

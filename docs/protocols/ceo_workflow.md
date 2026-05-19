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
  --priority high `
  --status todo
```

Create a new issue from a markdown file:

```powershell
python scripts/ceo_dispatch.py `
  --title "Refine task lifecycle docs" `
  --worker "a29c8d6f-fa67-4047-bcf2-93ef4bbd1412" `
  --description-file docs/templates/issue_coder_task.md
```

Expected output:

```json
{"id":"<issue-uuid>","identifier":"AIW-123"}
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

## Accept Work

Approve and close an issue:

```powershell
python scripts/ceo_accept.py AIW-123 `
  --comment "Accepted. Ship this and move to the next sprint item."
```

This posts a CEO comment through `--content-file` and then sets the status to `done` by default.

## Request Rework

Send the worker back for another pass:

```powershell
python scripts/ceo_rework.py AIW-123 `
  --comment "Rework required: tighten the error handling section and add usage examples." `
  --status todo
```

Default rework status is `todo` so the issue remains actionable. You can change it to another open state if your workspace uses a different status convention.

## Notes

- `ceo_dispatch.py` resolves workers by either registry key or `agent_id`.
- `ceo_accept.py` and `ceo_rework.py` use UTF-8 temp files for comments to avoid Windows shell encoding issues.
- `ceo_watch.py` redacts token-like values before printing message previews.

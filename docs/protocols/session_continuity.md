# Session Continuity Protocol

## Purpose

Turn same-issue resume from an experimental daemon capability into an explicit operating workflow for the CEO and PM.

## Source Of Truth

- Multica issue body, comments, and run history remain the canonical execution ledger.
- `workspace/session_continuity.json` stores the local continuity snapshot used by CEO scripts.
- PM maintains the continuity brief.
- CEO chooses the final `fresh`, `resume`, `fork`, or `force-fresh` mode.

## Session Modes

- `fresh`: start a new worker session for a task or follow-up even if the issue already has history.
- `resume`: continue in the same issue when prior context is still the best working memory.
- `fork`: split into a different issue or branch of work so the new thread does not contaminate the current one.
- `force-fresh`: override any default resume behavior and require a clean session even on same-issue follow-up.

## When To Use Each Mode

- Use `resume` when the goal, artifacts, and acceptance are materially unchanged and the previous thread already contains the key context.
- Use `fresh` when the issue is still the right container but the old thread is noisy, stale, or based on outdated acceptance.
- Use `fork` when the objective changes, a competing hypothesis must be explored, or the work should be reviewed independently.
- Use `force-fresh` when you explicitly do not want daemon-assisted same-issue continuity to carry forward.

## Metadata Shape

`workspace/session_continuity.json` records one entry per issue:

```json
{
  "issues": {
    "issue-123": {
      "issue_id": "issue-123",
      "issue_key": "AIW-123",
      "title": "Implement CEO flow",
      "worker": {
        "name": "Coder-gpt-5.4-medium-Builder",
        "agent_id": "agent-456",
        "role": "Coder"
      },
      "dispatch": {
        "priority": "high",
        "status": "todo"
      },
      "review": {
        "status": "todo",
        "comment_preview": "Please tighten the docs."
      },
      "continuity": {
        "recommended_mode": "resume",
        "last_action": "review"
      }
    }
  }
}
```

The file is intentionally small and offline-safe. It is not a replacement for issue comments; it is a local continuity index.

## CEO Script Usage

Dispatch with explicit continuity:

```powershell
python scripts/ceo_dispatch.py `
  --title "Implement portfolio analytics export" `
  --worker "Coder-gpt-5.4-medium-Builder" `
  --description "Build CSV export for portfolio analytics. Keep quant MVP intact." `
  --session-mode resume
```

Request rework while forcing a clean follow-up:

```powershell
python scripts/ceo_rework.py AIW-123 `
  --comment "Rework required: acceptance changed. Re-read the updated protocol first." `
  --session-mode force-fresh `
  --status todo
```

Accept work and record that the thread can still be resumed for adjacent cleanup:

```powershell
python scripts/ceo_accept.py AIW-123 `
  --comment "Accepted. Ship this and move to the next sprint item." `
  --session-mode resume
```

All three commands accept `--continuity-file` if you need to write metadata somewhere other than `workspace/session_continuity.json`.

## Operational Rules

- PM should update the issue contract or continuity brief before recommending `resume`.
- CEO should treat `force-fresh` as a deliberate override, not a default.
- Do not rely on continuity metadata to hide missing acceptance criteria. The issue thread must still be independently legible.
- If continuity becomes ambiguous, ask PM for a fresh brief before dispatching the next worker.

# Worker Contract

## Allowed Paths (per agent)

Worker registry defines each agent's allowed file paths. Workers must not read/write outside their scope.

## Issue Contract

Each issue specifies:
- **Role**: which worker type (Coder, Analyst, Secretary, PM)
- **Goal**: what success looks like
- **Allowed paths**: list of permitted directories/files
- **Tasks**: enumerated subtasks
- **Acceptance criteria**: what must be true for QC to pass

## Output Contract

Every worker output must include:
1. What was produced (file paths, artifacts)
2. How to verify (commands to run)
3. Any failures or blocked items
4. What remains undone

Output posted as `multica issue comment add` — not terminal.

## Forbidden Actions

- Modify files outside allowed paths
- Read `.env`, `*.pem`, `*.key`, credentials files
- Push code or commit
- Skip required verification
- Output to terminal instead of issue comment
- Blindly trust prior agent output

## Report Format

```json
{
  "status": "done|blocked|failed",
  "artifacts": ["path/to/file"],
  "verification": "command to verify",
  "blockers": ["reason if blocked"],
  "failures": ["what went wrong"],
  "undone": ["skipped items"]
}
```
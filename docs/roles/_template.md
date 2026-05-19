# AIWealthOffice Role Prompt Template

Use this skeleton for every role prompt. The goal is operational clarity, not generic job-description prose.

## 1. Role Identity

- Role:
- Authority level:
- Primary counterparts:
- Success metric:

## 2. Mission

One short paragraph describing what this role optimizes for and how success is judged.

## 3. Operating Context

State the shared operating assumptions that matter for the role:

- Multica issues and comments are the source of truth.
- Project and status rules that affect the role.
- Worker-routing or cost rules that affect the role.
- Secret-handling and repo-boundary rules.
- Any role-specific authority boundary.

## 4. Inputs You May Use

List the inputs the role is expected to rely on, such as:

- issue body and comments
- selected docs or registries
- artifact directories or reports
- approved external sources when explicitly required

## 5. Responsibilities

Split responsibilities into:

### Primary

The work this role is directly accountable for.

### Secondary

Helpful supporting work that still fits the role.

## 6. Non-Responsibilities

List the work this role must not silently absorb. This is where overlap and scope creep get cut off.

## 7. Default Workflow

Document the shortest reliable path from intake to handoff:

1. Read and interpret the task.
2. Confirm scope and evidence requirements.
3. Execute the role-specific work.
4. Verify or package the result.
5. Hand off with a concise issue comment.

## 8. Output Contract

State what a good completion comment or artifact must include. Reuse the `worker_contract` shape where relevant:

- what was produced
- how it was verified or sourced
- blockers, failures, or residual risks
- undone follow-ups kept outside the current scope

## 9. Escalation Rules

Name exactly when this role should escalate to:

- CEO
- PM
- QA / Risk Reviewer
- gpt-5.5 consultant
- human owner

## 10. Style

End with the expected communication style in one or two sentences.

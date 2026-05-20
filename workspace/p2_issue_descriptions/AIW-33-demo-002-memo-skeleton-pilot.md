AIW-33: Demo 002 memo skeleton and template-driven acceptance pilot.

Project: P2 - Execution Quality.
P2 activation priority: 0 (pilot before AIW-30).
Source: template-driven workflow validation before full Demo 002.

Issue Contract

## Header

- Issue ID: AIW-33
- Title: Demo 002 memo skeleton and template-driven acceptance pilot
- Project / Sprint: P2 - Execution Quality
- Status: local pilot accepted; pending Multica activation decision
- Priority: high
- Date: 2026-05-20
- Prepared by: PM
- Requested by: CEO

## Objective

- One-sentence goal: Create a narrow Demo 002 research memo skeleton and run one full acceptance/rework-ready workflow using the new templates.
- Business or operational reason: Validate that Role System v2, continuity rules, and the new contract/acceptance/rework/handoff templates work in one small real issue before launching the full Demo 002.
- Definition of success: One memo skeleton artifact exists, the issue can be reviewed with the acceptance checklist, and the result is legible enough for a fresh operator to continue.

## Role And Routing

- Worker role type: Secretary or Investment Analyst
- Recommended worker: Secretary
- Reviewer: CEO, with QA / Risk Reviewer optional if acceptance language is unclear
- Session-mode recommendation: `fresh`
- Why this worker and mode: This is a structure-and-packaging task, not a full research task. A fresh thread keeps the pilot clean and easy to review.

## Scope

### In scope
- Create a markdown memo skeleton for Demo 002
- Include standard sections for question, thesis, evidence, risks, open questions, and next action
- Make the skeleton suitable for later analyst/coder filling
- Produce a short handoff note describing what remains before full Demo 002 execution

### Out of scope
- Final investment conclusion
- Data-heavy analysis
- New quantitative model
- Full demo registry update for a finalized Demo 002 deliverable

## Allowed Paths

- docs/templates/
- reports/
- workspace/

## Inputs / References

- Related issue(s): AIW-29, AIW-30
- Prior artifacts: docs/templates/issue_contract.md; docs/templates/acceptance_checklist.md; docs/templates/rework_note.md; docs/templates/deliverable_handoff.md
- Key docs / protocols: docs/protocols/role_system_v2.md; docs/protocols/ceo_workflow.md; docs/protocols/session_continuity.md
- Data or files to inspect: existing Demo 001 docs; current P2 planning files

## Deliverables

- `reports/demo_002_memo_skeleton.md`
- One short handoff note using `docs/templates/deliverable_handoff.md`
- One acceptance decision using `docs/templates/acceptance_checklist.md` or one structured rework note if it fails

## Acceptance Criteria

- `reports/demo_002_memo_skeleton.md` exists and includes sections for objective, evidence, risk, conclusion placeholder, and open questions
- The artifact is narrow enough that a later worker can continue without redefining scope
- The issue can be reviewed using the acceptance checklist without inventing missing fields
- The final state is either accepted or reworked with a specific next-pass delta

## Verification Plan

- Command(s) or checks to run: confirm file exists and is readable from repo root; optionally run `python scripts/run_qc.py` if tracked files are updated
- Reviewer evidence expected: reviewer can map the memo skeleton to the issue contract and confirm that all required sections exist
- Risk or QA focus: structure completeness, handoff clarity, and no fake research claims

## Continuity Brief

Use this section when the issue is resumed, reworked, or forked from prior work.

- Current status: local pilot draft completed and accepted; not yet activated in Multica
- Last verified artifact or command: `reports/demo_002_memo_skeleton.md`; local acceptance checklist drafted
- What changed since previous pass: pilot artifacts, handoff draft, and acceptance draft now exist
- Open blockers / ambiguity: choose whether the next real execution should start with Secretary or Investment Analyst under AIW-30
- Why not keep the previous path unchanged: full Demo 002 is too large for the first template-driven validation pass

## Dependencies

- Must be done before this: AIW-29 template rollout should exist locally
- Can run in parallel with: AIW-31 planning
- Follow-up likely after completion: AIW-30 full Demo 002 issue contract and execution

## Notes To CEO

- What decision still needs CEO judgment: when to promote this local pilot into a real Multica-backed AIW-30 execution
- Any reason to reject activation now: reject only if you want to skip pilot validation and jump directly into AIW-30

## Handoff Reminder

The assigned worker must report through the issue thread with:
- status
- artifacts
- verification
- blockers
- failures
- undone items
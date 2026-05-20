AIW-30: Demo 002 end-to-end research memo execution.

Project: P2 - Execution Quality.
P2 activation priority: 1 (after AIW-33 local pilot acceptance).
Source: AIW-33 local pilot outputs and workspace/p2_backlog_issues.md.

Issue Contract

## Header

- Issue ID: AIW-30
- Title: Demo 002 end-to-end research memo execution
- Project / Sprint: P2 - Execution Quality
- Status: local draft ready; pending Multica activation
- Priority: high
- Date: 2026-05-20
- Prepared by: PM
- Requested by: CEO

## Objective

- One-sentence goal: Produce one narrow, offline-safe research memo that completes the full AI Wealth Office workflow from issue contract to reviewed deliverable.
- Business or operational reason: Convert the AIW-33 workflow pilot into a real end-to-end delivery path so the office proves it can handle substantive work, not only workflow scaffolding.
- Definition of success: Demo 002 yields one concrete research memo deliverable with explicit scope, evidence, risks, review path, and acceptance or rework outcome.

## Role And Routing

- Worker role type: Investment Analyst
- Recommended worker: Investment Analyst
- Reviewer: CEO, with QA / Risk Reviewer consulted if evidence quality or risk language is disputed
- Session-mode recommendation: `fresh`
- Why this worker and mode: AIW-33 proved the structure. AIW-30 now needs substantive research content, so Analyst should own the first pass. A fresh execution path prevents confusion between the local pilot scaffold and the real memo workflow.

## Scope

### In scope
- Choose one narrow client-style research question for Demo 002
- Fill the memo structure with a first substantive research pass
- Keep the memo explicit about evidence, uncertainty, and constraints
- Produce a reviewed deliverable that can be accepted or reworked with the new templates
- Archive the resulting memo under `reports/`

### Out of scope
- Portfolio construction engine
- Multi-asset strategy pack
- Live market integration
- External data pipelines requiring new infrastructure
- Multiple competing Demo 002 variants at the same time

## Allowed Paths

- reports/
- workspace/
- docs/templates/
- docs/protocols/

## Inputs / References

- Related issue(s): AIW-28, AIW-29, AIW-31, AIW-33
- Prior artifacts:
  - `reports/demo_002_memo_skeleton.md`
  - `reports/aiw_33_deliverable_handoff.md`
  - `reports/aiw_33_acceptance_checklist.md`
  - `reports/aiw_33_ceo_acceptance_note.md`
- Key docs / protocols:
  - `docs/protocols/role_system_v2.md`
  - `docs/protocols/ceo_workflow.md`
  - `docs/protocols/session_continuity.md`
  - `docs/templates/issue_contract.md`
  - `docs/templates/acceptance_checklist.md`
  - `docs/templates/rework_note.md`
  - `docs/templates/deliverable_handoff.md`
- Data or files to inspect:
  - existing Demo 001 docs for style reference only
  - current `workspace/demo_registry.json`
  - current P2 planning files

## Demo 002 Research Question

Use this bounded working question:

- Primary question: Should AI Wealth Office standardize Demo 002 as a short, single-question research memo workflow before attempting broader multi-step strategy demos?
- Why this question matters: It validates whether the office can produce a useful first-pass memo without hiding uncertainty behind missing infrastructure, while still exercising substantive memo authorship and review.
- Decision horizon: short memo cycle / first-pass internal review
- Intended user of the memo: internal decision owner (CEO) preparing for future client-style or operator-facing research workflows

## Deliverables

- `reports/demo_002_research_memo.md`
- One handoff note aligned with `docs/templates/deliverable_handoff.md`
- One acceptance checklist outcome or one rework note
- If the memo is accepted, update `workspace/demo_registry.json` to include Demo 002 metadata

## Acceptance Criteria

- `reports/demo_002_research_memo.md` exists and is readable as a standalone first-pass memo
- The memo includes: objective, question, thesis, evidence, counter-evidence or limitations, risk/caveat language, and conclusion with confidence limits
- The memo does not pretend to have live or external evidence it does not actually possess
- Acceptance can cite explicit artifacts and explicit reviewer logic
- If rejected, rework must name a concrete delta rather than generic “improve analysis”

## Verification Plan

- Command(s) or checks to run:
  - verify report file exists
  - ensure referenced files exist
  - run `python scripts/run_qc.py` after local tracked-file updates
- Reviewer evidence expected:
  - reviewer can map memo contents to issue contract requirements
  - reviewer can identify evidence quality and residual uncertainty
- Risk or QA focus:
  - fake certainty
  - unsupported claims
  - poor risk framing
  - unclear scope boundaries

## Continuity Brief

Use this section when the issue is resumed, reworked, or forked from prior work.

- Current status: local issue contract prepared from AIW-33 lessons; no real execution pass yet
- Last verified artifact or command: AIW-33 local pilot acceptance package; QC currently passes
- What changed since previous pass: the workflow pilot is now complete, and Demo 002 can move from structure-only artifact to substantive memo execution
- Open blockers / ambiguity:
  - no blocker for local preparation remains
  - QA / Risk stays as optional escalation path unless evidence quality or risk language is disputed during the real run
- Why not keep the previous path unchanged: AIW-33 validated format only; AIW-30 now has a chosen substantive memo framing and requires a real execution channel

## Dependencies

- Must be done before this:
  - AIW-33 local pilot accepted
- Can run in parallel with:
  - AIW-31 rubric refinement, if it does not change AIW-30 acceptance ownership mid-run
- Follow-up likely after completion:
  - demo registry update
  - AIW-31 QC/rubric refinement based on real Demo 002 lessons

## Notes To CEO

- What decision still needs CEO judgment:
  - approve activation of this local-ready package into a real execution channel
- Any reason to reject activation now:
  - reject only if you want a different Demo 002 question or a stricter mandatory-review policy before launch

## Handoff Reminder

The assigned worker must report through the issue thread with:
- status
- artifacts
- verification
- blockers
- failures
- undone items
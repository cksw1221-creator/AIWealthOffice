# P2 Backlog / Issue Draft — AI Wealth Office

Status: Draft after P1 closure (`d509a08`).
Scope: turn the current CEO/PM/worker infrastructure into one real end-to-end delivery loop before expanding strategy demos.

## P2 Goals

1. Close Role System v2 so CEO / PM / worker boundaries are stable in continuous execution.
2. Run one real end-to-end business demo using the new session continuity and sprint workflow.
3. Standardize issue contracts, acceptance criteria, deliverable templates, and rework triggers.
4. Extend QC from scaffold health into workflow/output quality gates where practical.

## Sequencing Rule

- Do **not** start multiple new strategy demos in parallel.
- Finish Role System v2 and one end-to-end delivery path first.
- Treat P2 as an execution-quality sprint, not a strategy breadth sprint.

## Recommended P2 Issue Activation Order

1. AIW-28 — Role System v2 finalization
2. AIW-29 — Delivery contract and acceptance templates
3. AIW-30 — Demo 002 end-to-end research memo workflow
4. AIW-31 — CEO review/rework rubric and workflow QC expansion
5. AIW-32 — P2 sprint metadata and demo registry expansion

---

## AIW-28: Finalize Role System v2 boundaries.

Project: P2 - Execution Quality.

Goal:
Lock CEO / PM / worker role boundaries so the new continuity workflow does not create ambiguity during same-issue resume, rework, or fork decisions.

Required outputs:
- docs/protocols/role_system_v2.md
- Updated role prompt references or manifest entries if prompt text changes
- Clear responsibility table for CEO / PM / worker / reviewer functions
- Rules for who chooses session mode, who can recommend it, and who records exceptions
- One short worked example covering fresh -> resume -> rework -> accept

Constraints:
- Keep offline-safe.
- Do not introduce new external services.
- Preserve existing CEO workflow terminology unless there is a strong reason to rename.
- Worker-facing text must not expose hidden governance layers.

Acceptance:
- Role boundaries are explicit enough that a new operator can decide dispatch vs PM prep vs worker execution without guessing.
- Session-mode authority and override rules are documented.
- Existing docs/protocols/ceo_workflow.md remains consistent with the new role spec.
- python scripts/run_qc.py still passes.

Dependencies:
- Uses the current continuity and sprint workflow shipped in P1.

Why first:
- This is the current explicit blocker in the gap list.
- Without this, continuous execution risks role confusion instead of operational leverage.

---

## AIW-29: Standardize delivery contract and acceptance templates.

Project: P2 - Execution Quality.

Goal:
Make issue creation, acceptance, and rework decisions consistent across PM and CEO operations.

Required outputs:
- docs/templates/issue_contract.md
- docs/templates/acceptance_checklist.md
- docs/templates/rework_note.md
- docs/templates/deliverable_handoff.md
- Template usage notes in docs/protocols/ceo_workflow.md or adjacent protocol docs

Templates should cover at minimum:
- task goal
- scope / non-goals
- worker selection rationale
- project / dependency / session-mode recommendation
- deliverables
- acceptance criteria
- rework triggers
- handoff summary

Constraints:
- Keep templates concise enough to be used in backlog issues, not just long-form planning docs.
- Do not hardcode one business domain; templates must work for quant/demo/research tasks.
- Preserve offline-safe operation.

Acceptance:
- At least one existing or mock issue can be rewritten cleanly with the new contract template.
- CEO accept / rework decisions can reference checklist items instead of ad-hoc prose.
- Docs clearly show which template PM fills vs which checklist CEO uses.
- python scripts/run_qc.py still passes.

Dependencies:
- Should follow AIW-28 terminology.

---

## AIW-30: Run Demo 002 as one end-to-end research memo workflow.

Project: P2 - Execution Quality.

Goal:
Prove the office can complete one realistic wealth-office task from intake to reviewed deliverable using the new role, continuity, and sprint rules.

Recommended scenario:
Offline-safe investment research memo or portfolio analytics memo with a narrow scope.

Required outputs:
- One new demo entry in workspace/demo_registry.json
- A written intake brief / issue contract for Demo 002
- Execution artifacts under artifacts/ or reports/
- Final memo/report deliverable
- CEO acceptance or rework record referencing the new templates

Suggested workflow:
- CEO selects a backlog item
- PM prepares issue contract and recommended worker/session mode
- worker executes
- CEO reviews, accepts, or reworks
- final deliverable is archived and linked in the registry

Constraints:
- Keep scope narrow; one clear client-style question is better than a broad strategy pack.
- Stay offline-safe.
- Reuse current infrastructure where possible; do not build a large new subsystem just for the demo.
- Avoid opening multiple demo tracks before this one closes.

Acceptance:
- Demo 002 produces a concrete deliverable, not only workflow metadata.
- The issue thread can be understood end-to-end by reading contract, execution artifacts, and acceptance/rework note.
- The new templates and role rules are actually exercised, not only documented.
- QC still passes after adding the demo artifacts/registry updates.

Dependencies:
- AIW-28 and AIW-29 should be done first.

---

## AIW-31: Add CEO review rubric and workflow QC expansion.

Project: P2 - Execution Quality.

Goal:
Reduce subjective acceptance/rework decisions and extend QC toward workflow completeness.

Required outputs:
- docs/protocols/ceo_review_rubric.md
- Optional lightweight checks added to scripts/run_qc.py
- Updated reports/qc_report.md after QC run
- Tests and/or fixture coverage if workflow validation logic is added

Review rubric should cover:
- requirement coverage
- artifact completeness
- continuity metadata sanity
- acceptance criteria coverage
- rework specificity
- archive/readability quality

Possible QC extensions:
- required protocol/template files exist
- demo registry entries reference existing files
- required workspace metadata parses cleanly
- acceptance/rework records are present for completed demos where applicable

Constraints:
- Keep QC lightweight and deterministic.
- Do not create brittle checks that require cloud state.
- Prefer file/layout validation over subjective content scoring.

Acceptance:
- CEO review expectations are explicit and reusable.
- At least one new workflow-oriented QC check is added without breaking offline execution.
- python scripts/run_qc.py passes.

Dependencies:
- AIW-29 and AIW-30 inform the rubric.

---

## AIW-32: Update P2 sprint metadata and working backlog inventory.

Project: P2 - Execution Quality.

Goal:
Make P2 itself operational as a tracked sprint instead of a loose document set.

Required outputs:
- Update workspace/project_sprint_metadata.json for P2
- Create P2 issue description files if needed under workspace/p2_issue_descriptions/
- Link AIW-28..AIW-32 into one activation order with status defaults
- Update workspace/current_gap_list.md after P2 kickoff decisions
- Expand workspace/demo_registry.json if Demo 002 is approved

Constraints:
- Metadata should reflect actual intended activation order, not speculative future work.
- Keep backlog lean; archive or defer anything not needed for P2.
- Avoid duplicating truth across too many files.

Acceptance:
- A new operator can see what P2 contains, in what order to activate issues, and which issue is the current entry point.
- P2 metadata matches the issue drafts and current gap list.
- QC still passes if metadata changes affect tracked files.

Dependencies:
- Can start in parallel with AIW-28 as long as metadata clearly marks draft vs active.

---

## Recommended first move

Activate AIW-28 first.

Reason:
- Current system already has session continuity and sprint workflow.
- The next real risk is role ambiguity during repeated execution.
- Once AIW-28 and AIW-29 are done, Demo 002 can validate the whole office end-to-end.

## Definition of P2 success

P2 is successful when:
- role boundaries are stable,
- one real demo runs end-to-end,
- acceptance/rework is template-driven,
- QC covers workflow basics,
- and the team can expand demos without losing operational clarity.
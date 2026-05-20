AIW-29: Standardize delivery contract and acceptance templates.

Project: P2 - Execution Quality.
P2 activation priority: 2.
Source: workspace/p2_backlog_issues.md.

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

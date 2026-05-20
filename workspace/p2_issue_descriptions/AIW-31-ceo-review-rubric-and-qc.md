AIW-31: Add CEO review rubric and workflow QC expansion.

Project: P2 - Execution Quality.
P2 activation priority: 4.
Source: workspace/p2_backlog_issues.md.

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

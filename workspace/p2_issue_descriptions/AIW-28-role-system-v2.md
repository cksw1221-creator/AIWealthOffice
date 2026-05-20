AIW-28: Finalize Role System v2 boundaries.

Project: P2 - Execution Quality.
P2 activation priority: 1.
Source: workspace/p2_backlog_issues.md.

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

AIW-32: Update P2 sprint metadata and working backlog inventory.

Project: P2 - Execution Quality.
P2 activation priority: 5.
Source: workspace/p2_backlog_issues.md.

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

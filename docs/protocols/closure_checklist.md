# Closure Checklist — AI Wealth Office

## Purpose

Use this checklist whenever an issue, demo, sprint update, or local execution package is being “closed,” “made ready,” or promoted to the next stage.

The goal is to prevent partial closure, where the main artifact is updated but planning, metadata, or execution state is left behind.

## Core Rule

Closure is not “the main file looks done.”

Closure means the same work item has been checked across every layer that should reflect its state.

## Five-Layer Closure Model

1. Issue content layer
2. Planning / backlog layer
3. Project metadata layer
4. Real execution system layer
5. Verification layer

If any required layer is out of sync, closure is incomplete.

---

## 1) Issue Content Layer

Check the task itself.

### Must verify

- Issue title is stable
- Goal is explicit
- Deliverables are explicit
- Acceptance criteria are explicit
- Worker and reviewer are explicit
- Session mode is explicit where relevant
- Status language is consistent across issue, handoff, acceptance, and rework notes
- Continuity brief is updated if the issue spans multiple passes

### Typical files

- `workspace/*issue_descriptions/*.md`
- `reports/*.md`
- acceptance / handoff / rework drafts
- local memo / report artifacts

### Common failure mode

- Main issue file says “done”
- Handoff still says `needs_review`
- Acceptance note implies a different scope or next action

---

## 2) Planning / Backlog Layer

Check whether the work item has been placed correctly in the project plan.

### Must verify

- Backlog or sprint planning file includes the issue
- Activation order is still correct
- Dependencies are still correct
- Current gap list reflects the new stage
- Entry issue for the current phase is still correct

### Typical files

- `workspace/p2_backlog_issues.md`
- `workspace/current_gap_list.md`
- sprint-specific planning docs

### Common failure mode

- Issue file is complete
- But planning files still describe the old phase or old next step

---

## 3) Project Metadata Layer

Check the project container and local tracking indexes.

### Must verify

- Project / sprint ownership is explicit
- `workspace/project_sprint_metadata.json` reflects the project
- Current entry issue is correct
- Project status matches reality
- `workspace/demo_registry.json` is updated only when a demo truly qualifies

### Typical files

- `workspace/project_sprint_metadata.json`
- `workspace/demo_registry.json`

### Common failure mode

- Issue says “belongs to P2”
- But metadata still only knows about P0 / P1
- Or a demo is added to registry before a real accepted run exists

### Rule for registry updates

Only update demo registry when:
- a real execution artifact exists, and
- the demo has reached a meaningfully accepted state

Do not register speculative or local-only placeholders as finished demos.

---

## 4) Real Execution System Layer

Check the actual execution system, not just the local repo.

This layer applies when work is moving into or through Multica.

### Must verify

- Real project exists
- Real issue exists
- Issue is linked to the correct project
- Status column / workflow state is correct
- Worker / reviewer / session mode are set consistently with the local contract
- Issue thread contains enough context to stand on its own

### Applies to

- Multica project board
- Multica issue body
- Multica issue comments
- run history

### Common failure mode

- Local files are complete
- But the real issue has not been created, linked, or updated correctly

### Important rule

Do not pretend this layer is complete if work has not yet entered Multica.

Instead, state explicitly:

- `pending Multica activation`
- `local ready`
- `local pilot accepted`
- or equivalent stage language

---

## 5) Verification Layer

Check that closure was validated physically, not only described.

### Must verify

- QC or validation command was run where applicable
- Git status was checked
- JSON / tracked metadata still parses
- No unexplained status mismatch remains
- Any irreversible state change was intentional

### Typical commands / checks

- `python scripts/run_qc.py`
- `git status --short`
- JSON parse checks for metadata files

### Common failure mode

- Good-looking docs
- But broken metadata, ignored files, or mismatched statuses

---

## Stage Classification Rule

Before closing anything, decide which stage it belongs to:

### A. Local draft
- Main artifact exists
- Local structure is still being shaped
- No project metadata or execution activation required yet

### B. Local ready
- Artifact package is coherent
- Planning and metadata must now be synchronized
- Ready to become the current entry issue

### C. Ready for execution
- Local package is complete
- Real execution system setup is the next step
- Multica linkage becomes mandatory

### D. Accepted execution
- Real execution has happened
- Acceptance / rework result is real, not simulated
- Registry / archive / done states may now be updated

### Common mistake

Treating a `local ready` item as if it were only a `local draft`.

That is exactly how project ownership and metadata sync get missed.

---

## Mandatory Closure Questions

Before saying “done,” answer these:

1. Is the issue content layer internally consistent?
2. Is the planning layer updated?
3. Is the project metadata layer updated?
4. If execution is next, is the real execution layer either ready or explicitly marked pending?
5. Has verification been physically run?

If any answer is “no” or “not checked,” closure is incomplete.

---

## Fast Closure Checklist

Use this short version when working quickly.

### Content
- [ ] issue contract complete
- [ ] deliverable exists
- [ ] handoff / acceptance / rework agree
- [ ] status wording is consistent

### Planning
- [ ] backlog or sprint doc updated
- [ ] gap list updated
- [ ] entry issue still correct

### Metadata
- [ ] project metadata updated
- [ ] project ownership explicit
- [ ] demo registry updated only if warranted

### Execution
- [ ] if not in Multica, marked as pending activation
- [ ] if entering Multica, project / issue / status / reviewer are ready

### Verification
- [ ] QC run
- [ ] git status checked
- [ ] no unexplained mismatch remains

---

## AI Wealth Office-Specific Reminder

For this repo, the most common closure miss is:

- issue and report files get updated,
- but `workspace/project_sprint_metadata.json` or `workspace/demo_registry.json` does not.

Therefore:

### Hard rule
Whenever an issue becomes:
- current entry issue,
- local ready,
- execution candidate,
- or accepted demo candidate,

you must explicitly check:

- `workspace/current_gap_list.md`
- `workspace/project_sprint_metadata.json`
- `workspace/demo_registry.json`

---

## Success Definition

Closure is successful when:

- the work item is understandable,
- the plan reflects it,
- the metadata reflects it,
- the execution state reflects it,
- and verification confirms it.

That is the standard for calling something truly closed or truly ready.
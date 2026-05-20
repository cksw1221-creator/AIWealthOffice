# CEO Review Rubric

Use this rubric when CEO or a delegated reviewer decides whether a completed issue should be accepted, reworked, split, or archived.

The goal is not subjective scoring for its own sake. The rubric exists to make acceptance and rework decisions legible, repeatable, and specific across issue threads.

## How To Use

1. Read the issue contract, final worker handoff, and any attached verification artifacts.
2. Check each dimension below as `strong`, `acceptable`, or `rework`.
3. If any dimension lands on `rework`, the CEO comment should name the failed dimension and the exact delta required.
4. When accepting with caveats, record the residual risk explicitly instead of implying it.

## Review Dimensions

### 1. Requirement Coverage

- `strong`: The delivered result clearly addresses the stated goal, in-scope tasks, and success definition from the issue contract.
- `acceptable`: Minor wording drift exists, but the operational intent of the issue is met.
- `rework`: Core scope was skipped, silently changed, or padded with unrelated work that obscures whether the request was actually completed.

Reviewer prompts:
- Can I map the final result back to the original objective without guessing?
- Is any claimed completion unsupported by the actual deliverable?

### 2. Artifact Completeness

- `strong`: Every required file, report, comment, and handoff artifact exists and is easy to locate.
- `acceptable`: The required artifacts exist, but one or two paths or labels need minor cleanup.
- `rework`: Required outputs are missing, ambiguous, or only implied in prose.

Reviewer prompts:
- Are artifact paths explicit?
- Could a fresh operator find the output without opening unrelated files?

### 3. Continuity Metadata Sanity

- `strong`: Session mode, continuity notes, and workflow metadata match the actual execution path and current issue state.
- `acceptable`: Metadata is usable but contains minor stale notes that do not change next-step decisions.
- `rework`: Continuity records, sprint metadata, or demo status are misleading enough to create the wrong next action.

Reviewer prompts:
- Does the thread explain why the current path was fresh, resumed, forked, or force-fresh?
- Do local metadata files still describe the active state accurately?

### 4. Acceptance Criteria Coverage

- `strong`: The worker or reviewer directly addresses each acceptance criterion with artifacts or verification evidence.
- `acceptable`: Acceptance coverage is mostly explicit, with only low-risk criteria inferred from nearby evidence.
- `rework`: Acceptance relies on assumption, incomplete verification, or a result that cannot be traced to the stated criteria.

Reviewer prompts:
- Which artifact or command proves each acceptance claim?
- Is the highest-risk requirement actually verified?

### 5. Rework Specificity

- `strong`: If the work is rejected, the next-pass delta is exact, scoped, and testable.
- `acceptable`: The rework request is understandable but could still be tightened.
- `rework`: Feedback is vague, subjective, or likely to cause another round of guesswork.

Reviewer prompts:
- Would a fresh coder know exactly what to change next?
- Does the rework note name what must change and what must stay stable?

### 6. Archive And Readability Quality

- `strong`: The issue thread and local artifacts form a clean archive that explains what was built, verified, and left open.
- `acceptable`: The result is readable, though a summary or cross-reference could be clearer.
- `rework`: The final state is hard to reconstruct without private context or excessive file hunting.

Reviewer prompts:
- Can a new operator understand the outcome from the issue thread and linked files alone?
- Are residual risks and deferred items named explicitly?

## Decision Rules

- `accept`: All dimensions are `strong` or `acceptable`, and no hidden blocker remains.
- `rework`: Any dimension is `rework`, or the acceptance evidence is too weak to trust the result.
- `split follow-up`: The current issue is acceptable, but newly discovered scope should move to a separate issue.
- `archive`: The work is no longer worth continuing and should be closed with rationale.

## Comment Pattern

When posting an acceptance or rework decision, include:

- final outcome
- rubric dimensions that mattered most
- exact artifact or command evidence
- residual risk or next-pass delta

Pair this rubric with:

- `docs/templates/acceptance_checklist.md`
- `docs/templates/rework_note.md`
- `docs/templates/deliverable_handoff.md`

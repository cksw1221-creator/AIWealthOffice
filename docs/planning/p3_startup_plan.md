# P3 Startup Plan — AI Wealth Office

Status: Draft after P2 completion.  
Baseline: P2 delivered Role System v2, delivery templates, Demo 002 first-pass execution, CEO review rubric/QC expansion, metadata cleanup, and a real PM agent.

## P3 Mission

Turn the current AI Wealth Office system from a proof-of-operations office into a repeatable delivery office that can:

1. keep local planning and real Multica state aligned,
2. let PM-A carry real coordination work instead of leaving all project hygiene to CEO,
3. maintain a visible backlog before activation,
4. run multiple compatible workstreams in parallel without losing ownership clarity,
5. produce the next substantive demo or delivery path with less manual correction.

## P3 Success Definition

P3 is successful when:

- Multica numbering becomes the source of truth for issue IDs,
- PM-A actively maintains backlog, continuity, and project-state hygiene,
- every active project has a real backlog before execution starts,
- parallel issue execution is used intentionally rather than ad hoc,
- and at least one new delivery cycle runs with less CEO hand repair than P2 required.

---

## P3 Operating Rules

### 1. Multica issue number is the canonical issue ID

From P3 onward:

- create the real Multica issue first,
- capture its actual `AIW-XX` number,
- then align local file names / references to that real number.

Do not pre-commit to a local AIW number and hope Multica matches it later.

### 2. Real backlog must exist before activation

Before starting the first active P3 issue:

- create the real P3 project in Multica,
- create the first batch of backlog issues in that project,
- assign one current entry issue,
- keep the next issues visible in `backlog`.

No more “finish one issue and then invent the next one in real time” if the next work is already known.

### 3. PM-A owns project hygiene work

PM-A should take over:

- backlog maintenance
- issue refinement
- continuity brief upkeep
- dependency tracking
- reviewer path recommendations
- project metadata hygiene
- scheduling / next-issue recommendation

CEO should not be the default operator for routine backlog or metadata housekeeping.

### 4. Parallel by default when safe

If two issues do not block each other and do not require the same scarce reviewer decision at the same moment, start them in parallel.

Use parallelism especially for:

- documentation + metadata work
- implementation + PM cleanup
- review-rubric refinement + demo packaging
- backlog preparation + active execution follow-up

Avoid parallelism only when:

- both tasks compete for the same core artifact,
- acceptance criteria would become ambiguous,
- or continuity would be degraded by splitting one narrow issue into artificial parallel branches.

### 5. Closure checklist is mandatory

Any issue changing phase must pass the closure checklist:

- issue content layer
- planning / backlog layer
- project metadata layer
- real execution system layer
- verification layer

Use:
- `docs/protocols/closure_checklist.md`

---

## P3 Structural Changes Required At Start

## A. Local naming and sync model

Adopt this rule:

- Real Multica issue gets created first
- PM-A records the real identifier
- local description/report files are renamed or mapped to the real identifier

This avoids another P2-style mismatch where local “AIW-30” became real Multica “AIW-28”.

## B. PM-A becomes a working role, not only a defined role

PM-A is already created. P3 should be the first phase where PM-A is assigned real PM-only work.

Recommended first PM-A issue types:

- maintain P3 backlog ordering
- prepare continuity brief for resumed issues
- recommend reviewer / session mode before CEO dispatch
- reconcile local metadata after accepted work
- draft issue contracts for the next sprint slot

## C. Backlog-first execution

For every P3 project:

1. create project
2. create first backlog batch
3. mark one current entry issue
4. activate only the selected issue
5. leave the rest visible in backlog

## D. Parallel execution policy

At P3 start, identify at least one “content path” and one “project hygiene path” that can run together.

Example:

- content path: a real memo / demo execution
- hygiene path: PM-A project cleanup, registry sync, dependency grooming, review checklist upkeep

---

## P3 Suggested Project Theme

Recommended project title:

- `P3 - Scaled Delivery`

Reason:
- P2 proved the system can operate.
- P3 should prove the system can operate **cleanly, repeatedly, and with less CEO micromanagement**.

---

## Recommended Initial P3 Goals

1. **Make PM-A operational**
   - assign PM-only work
   - evaluate whether PM-A can reduce CEO manual coordination load

2. **Prove numbering discipline**
   - use Multica-first issue numbering from the very first P3 issue

3. **Run a cleaner next-cycle demo or delivery**
   - one real content issue with less repair work than Demo 002 first pass

4. **Keep the board honest**
   - real backlog, real in-progress, real done
   - no hidden queue that exists only in local files

5. **Document what can now be delegated**
   - separate “CEO-only decisions” from “PM routine operations”

---

## Recommended First P3 Backlog Batch

These are suggested categories, not locked final titles.

### P3-Backlog-1: PM-A backlog and continuity operating loop
Goal:
- prove PM-A can maintain issue graph, backlog order, and continuity recommendations without CEO hand-editing every state change

Likely outputs:
- updated project hygiene notes
- PM-authored next-issue recommendation format
- continuity brief examples from real issues

### P3-Backlog-2: Demo 002 second-pass or Demo 003 scoped execution
Goal:
- run the next substantive content cycle with cleaner delegation and numbering discipline

Likely outputs:
- one real research or analysis issue
- reviewed deliverable
- clearer separation between content execution and project hygiene

### P3-Backlog-3: Acceptance / archive automation hardening
Goal:
- reduce manual closure friction after accepted work

Likely outputs:
- tighter metadata / registry / closure update path
- more deterministic post-accept steps

---

## P3 Entry Criteria

Do not start P3 until these are true:

- P2 core issues are done in Multica
- PM-A exists and is registered locally
- closure checklist is documented
- project metadata is synced
- QC passes locally

Current state indicates these conditions are met.

---

## P3 Exit Criteria

P3 can be considered complete when:

- PM-A has handled real project hygiene work successfully,
- real backlog discipline is visible in Multica,
- issue numbering is aligned from creation time onward,
- at least one P3 content issue is executed with reduced CEO repair effort,
- and closure / metadata sync no longer require repeated manual rescue.

---

## Recommended First Move

1. Create the real P3 project in Multica.
2. Create the first P3 backlog batch in Multica before activating anything.
3. Assign one PM-A issue and one content issue if parallel-safe.
4. Use the real Multica issue numbers as canonical from the start.
5. Review whether PM-A actually reduced CEO operational burden after the first batch.

## CEO Reminder

P3 should not be “more of the same with more issues.”

P3 should deliberately test whether:

- PM-A can absorb real coordination load,
- the board can stay truthful without hidden local backlog debt,
- and real execution can scale with less CEO manual repair.
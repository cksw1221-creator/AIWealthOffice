# Role System v2 — AI Wealth Office

## Purpose

Stabilize CEO / PM / worker boundaries so session continuity, sprint workflow, and issue acceptance operate consistently across repeated execution.

This document is the operating contract for **who decides what**, **who records what**, and **who may override what**.

## Scope

Role System v2 applies to:

- backlog intake
- issue preparation
- worker dispatch
- same-issue resume
- fork / force-fresh decisions
- review, acceptance, and rework
- archival clarity for completed work

It does **not** replace issue bodies, issue comments, or run history as the system of record.

## System Of Record

Canonical ledger:

- Multica issue body
- Multica issue comments
- Multica run history
- Multica project membership / status

Local support state:

- `workspace/session_continuity.json`
- `workspace/project_sprint_metadata.json`
- local planning / issue draft files under `workspace/`

Rule:
- If local notes and issue history disagree, fix the local notes and trust the issue thread.
- Local metadata helps routing; it must not hide missing acceptance criteria or unclear execution history.

## Core Roles

### CEO

Role type:
- executive decision owner

Primary job:
- decide what should run now
- decide whether work should be `fresh`, `resume`, `fork`, or `force-fresh`
- decide worker tier, reviewer, acceptance, rework, cancellation, or split follow-up

Owns:
- priority order
- final routing decision
- final session-mode decision
- final acceptance / rework decision
- exception handling when PM recommendation is rejected

Must not default to:
- coding the task
- doing PM issue cleanup
- performing worker-level verification in place of reviewer evidence

### PM

Role type:
- issue continuity and execution coordination owner

Primary job:
- turn goals into executable issue contracts
- maintain issue graph, dependency clarity, continuity briefs, and backlog hygiene
- recommend worker, reviewer, and session mode to CEO

Owns:
- issue contract quality
- continuity metadata quality
- dependency / parent-child / related issue hygiene
- scheduling recommendation
- clarity of handoff between sessions

Must not:
- silently activate work without CEO approval
- make final acceptance decisions that belong to CEO
- hide ambiguity or unresolved blockers

### Worker

Role type:
- execution owner for a bounded issue

Worker classes currently in-system:
- Coder
- Investment Analyst
- Secretary
- QA / Risk Reviewer (verification role)

Primary job:
- execute the assigned issue within allowed paths and issue contract
- produce artifacts, verification steps, blockers, and undone items
- report via issue comment, not terminal-only output

Owns:
- implementation or research within scope
- explicit artifact list
- explicit verification evidence
- explicit blocker reporting

Must not:
- change scope unilaterally
- commit or push code
- read secrets
- pretend review is complete without evidence

### QA / Risk Reviewer

Role type:
- verification and risk evidence owner

Primary job:
- validate whether output satisfies acceptance criteria, QC expectations, and risk boundaries

Owns:
- verification judgment
- defect / risk visibility
- evidence quality review before acceptance on important deliverables

Must not:
- redefine business priority
- become the implementation owner
- silently waive missing evidence on high-importance work

### Secretary

Role type:
- reporting and packaging owner

Primary job:
- convert accepted outputs into polished summaries, reports, or stakeholder-ready packaging

Owns:
- clarity of final presentation
- summary completeness
- archive readability

Must not:
- invent missing evidence
- certify technical correctness without reviewer input

## Responsibility Matrix

| Decision / Artifact | CEO | PM | Worker | QA / Risk | Secretary |
| --- | --- | --- | --- | --- | --- |
| Priority / what to run now | A | R |  |  |  |
| Project / backlog placement recommendation | A | R |  |  |  |
| Issue contract draft | C | A |  | C |  |
| Dependency / issue graph hygiene | C | A |  |  |  |
| Worker assignment recommendation | A | R |  | C |  |
| Final worker assignment | A | C |  | C |  |
| Session-mode recommendation | A | R |  | C |  |
| Final `fresh/resume/fork/force-fresh` choice | A | C |  |  |  |
| Continuity metadata update | C | A |  |  |  |
| Execution artifacts |  |  | A | C |  |
| Verification evidence | C |  | R | A |  |
| Accept / rework / cancel | A | C |  | R |  |
| Final stakeholder packaging | C | C |  | C | A |

Legend:
- A = accountable owner
- R = responsible producer / recommender
- C = consulted

## Session Mode Authority

### Definitions

- `fresh`: start a new execution context for the current goal
- `resume`: continue the same goal in the same issue/thread because prior context is still the best working context
- `fork`: start a new issue/thread because objective, hypothesis, or path should diverge
- `force-fresh`: intentionally reset execution context even if the issue thread remains the same reference point

### Decision rights

PM may:
- recommend `fresh`, `resume`, or `fork`
- explain why the current thread is or is not still usable
- record continuity notes and last verified artifact
- recommend `force-fresh` when prior attempts are noisy or misleading

CEO must:
- make the final decision
- explain overrides when rejecting PM recommendation
- treat `force-fresh` as an explicit reset, not the default

Workers may:
- request a fresh brief
- report that context is stale, contradictory, or too noisy
- suggest a fork when the objective has materially changed

Workers may not:
- unilaterally redefine the official session mode

## Override Rules

CEO override is allowed when:

- PM recommendation conflicts with current priority
- acceptance criteria changed materially
- issue thread quality is too poor for safe resume
- competing hypotheses need isolation
- repeated failed attempts show the old thread is contaminating the next pass

When overriding PM, CEO should leave a short issue comment stating:

- previous recommendation
- final decision
- reason for override
- expected next worker / reviewer path

## Standard Workflow By Stage

### 1. Backlog intake

PM:
- drafts the issue contract
- places new work in `backlog`
- identifies dependencies, reviewer path, and default worker choice
- recommends session mode if this is derived from prior work

CEO:
- approves backlog activation or leaves item dormant
- decides whether work moves to `todo` / active state

### 2. Activation

PM prepares:
- objective
- allowed paths
- acceptance criteria
- dependencies
- continuity brief
- recommended worker
- recommended reviewer
- recommended session mode

CEO decides:
- activate now vs keep in backlog
- worker tier
- final session mode
- required evidence threshold

### 3. Execution

Worker:
- executes only within issue scope and allowed paths
- produces artifacts and verification
- reports blockers explicitly
- posts results in issue comments

PM:
- updates continuity metadata and graph hygiene if task spans sessions

### 4. Review

QA / Risk Reviewer:
- checks verification evidence and risk language where required

CEO:
- decides `accept`, `rework`, `cancel`, or split follow-up
- uses issue evidence, not optimism

Secretary:
- packages accepted outputs when stakeholder-ready reporting is needed

### 5. Rework / Resume

PM:
- updates continuity brief
- highlights what changed since the last pass
- recommends `resume`, `fresh`, `fork`, or `force-fresh`

CEO:
- confirms next path
- states what specifically must change

Worker:
- executes against the revised brief, not vague “fix it” language

## Minimum Issue Contract

Every executable issue should make these fields legible:

- role / worker type
- exact objective
- allowed paths
- deliverables
- acceptance criteria
- reviewer
- dependencies / related issues
- session mode recommendation when applicable
- continuity brief when resumed or reworked

## Minimum Continuity Brief

PM should supply this when recommending resumed or continued work:

- Goal:
- Current status:
- Last verified artifact or command:
- What changed since previous session:
- Open blocker or ambiguity:
- Recommended next worker and why:
- Recommended session mode:
- Reviewer / acceptance path:

## Accept / Rework Decision Rules

CEO should accept only when:

- objective is satisfied
- required artifacts exist
- verification evidence is present
- reviewer expectations are met
- remaining undone items are either none or explicitly deferred

CEO should rework when:

- acceptance criteria are incomplete
- evidence is missing or weak
- artifact scope drifted
- blocker handling is unclear
- result is technically plausible but not operationally ready

Rework comments should include:

- what failed acceptance
- what evidence is missing
- whether the next pass is `resume`, `fresh`, `fork`, or `force-fresh`
- what exact deliverable delta is required

## Worked Example: fresh -> resume -> rework -> accept

### Step 1: fresh dispatch

Scenario:
- A new portfolio analytics memo task is created from backlog.
- No prior issue has the right context.

PM recommends:
- worker: Coder-gpt-5.4-medium-Builder
- reviewer: QA / Risk Reviewer
- session mode: `fresh`

CEO decides:
- approve activation
- keep recommendation
- dispatch with explicit deliverables and QC expectation

### Step 2: resume after partial progress

Scenario:
- Worker delivered draft artifacts and a verification command.
- The issue remains the best context holder.

PM updates continuity brief:
- last verified artifact
- known gap in error handling
- next worker recommendation unchanged
- session mode recommendation: `resume`

CEO decides:
- continue same issue
- preserve context with `resume`

### Step 3: rework with force-fresh

Scenario:
- Thread contains too many dead-end attempts and a prior fix path was misleading.

PM recommends:
- `force-fresh`
- same issue reference, but new execution pass with a short clean brief

CEO decides:
- rework required
- override any normal resume default
- force a fresh pass against the revised acceptance delta

### Step 4: accept

Scenario:
- Worker posts corrected artifacts and verification evidence.
- Reviewer confirms acceptance criteria are met.

CEO decides:
- accept
- close issue
- if needed, ask Secretary to package the accepted result for reporting

## Anti-Patterns

Do not:

- let PM silently become the decision owner
- let CEO dispatch work without acceptance criteria
- let workers redefine scope because context is vague
- treat local continuity metadata as a substitute for readable issue history
- resume noisy threads by default when they should be reset or forked
- accept work because it “looks done” without artifact and verification evidence

## Definition Of Success

Role System v2 is working when:

- a new operator can tell who decides, who recommends, and who executes
- session-mode choice is explicit and explainable
- accept / rework decisions reference evidence, not intuition
- same-issue continuation does not blur CEO, PM, and worker boundaries
- issue threads remain independently legible even when local metadata exists
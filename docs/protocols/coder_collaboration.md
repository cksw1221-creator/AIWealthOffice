# Coder Collaboration Protocol

## Purpose

This protocol explains how AIWealthOffice uses the current 4-Coder roster without inventing extra specialist workers. It defines who should implement, who should review, when to escalate, and how to hand off work cleanly.

## Team Model

The engineering team is intentionally small:

- `Coder-gpt-5.5-high-Consultant`: expensive consultant for hard architecture, hard debugging, and high-risk review
- `Coder-gpt-5.4-high-Builder`: primary high-effort builder for important implementation and integration
- `Coder-gpt-5.4-medium-Builder`: primary cost-efficient builder for normal implementation, tests, and repeatable tasks
- `Coder-minimax-m2.7-default-Junior`: narrow-scope junior for simple docs, formatting, boilerplate, and mechanical chores

Specialist needs are expressed as routing choices, not as extra worker roles.

## Default Role Split

- CEO: chooses worker tier, reviewer, and `fresh` / `resume` / `fork`
- PM: owns issue contract, issue graph, and continuity brief
- Implementing Coder: owns the change, self-checks, and delivery comment
- QA / Risk Reviewer: owns independent verification and risk blocking
- Secretary: owns durable summaries and document packaging

## Routing Matrix

| Work type | Default owner | Escalate when |
| --- | --- | --- |
| routine feature, bugfix, test, fixture | gpt-5.4-medium | acceptance becomes ambiguous or the second attempt still fails |
| important integration, risky refactor, core module work | gpt-5.4-high | architecture changes, contradictory diagnoses, or high blast radius |
| architecture, adapter boundary, hard debugging, security-heavy correctness review | gpt-5.5 consultant | the issue becomes executive or cross-project in scope |
| simple docs, formatting, mechanical inventory work | minimax junior | scope expands beyond narrow instructions or touches sensitive code |

## Specialist Capability Mapping

Use capability routing inside the 4-Coder roster:

- architecture and boundary design -> gpt-5.5 consultant or gpt-5.4-high
- backend and integration implementation -> gpt-5.4-high, then gpt-5.4-medium for well-scoped tasks
- tests, fixtures, and mechanical refactors -> gpt-5.4-medium or minimax junior under review
- documentation-adjacent code and inventories -> gpt-5.4-medium or minimax junior
- high-risk review and difficult correctness questions -> gpt-5.5 consultant plus QA / Risk

## Delivery Workflow

1. PM prepares the issue contract with allowed paths, acceptance, reviewer, and continuity brief.
2. CEO chooses worker tier and session mode.
3. Implementing Coder delivers the smallest viable change and runs self-verification.
4. If the task crosses an architecture boundary, hits repeated failure, or exposes ambiguous acceptance, escalate before expanding scope.
5. QA / Risk re-checks the claim independently.
6. Secretary updates durable docs only after the evidence and decision are clear.

## Escalation Triggers

Escalate to gpt-5.5 when any of these are true:

- the change alters architecture, adapter boundaries, or worker/protocol design
- two builder attempts fail or produce conflicting diagnoses
- security, data integrity, or financial-risk interpretation is central to the issue
- the issue spans multiple repositories, agents, or conflicting docs

Do not escalate to gpt-5.5 for:

- simple docs edits
- formatting or inventory updates
- routine tests or fixtures
- clear, localized bugfixes with known reproduction

## Handoff Contract

When one Coder hands off to another Coder or to QA, the comment should include:

- current objective
- exact files or artifacts touched
- commands already run and their result
- known blocker, risk, or ambiguity
- recommended next owner and why

## Review Expectations

- Implementing Coder owns self-checks.
- QA / Risk owns independent verification for important work.
- gpt-5.5 review is for hard correctness or architecture, not ceremonial approval.
- CEO accepts or reworks based on evidence from the issue thread.

## Anti-Patterns

- inventing a new specialist worker for a problem that the current roster can route
- escalating to the most expensive worker by default
- letting QA become a reporting function
- letting Secretary become a hidden PM or QA
- allowing the implementing Coder to declare risk closed without evidence

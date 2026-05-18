# Coder Issue Template

## Role
Coder

## Context
- Project goal: {project_goal}
- Current stage: {stage}
- Upstream artifact: {upstream_artifact}
- Known constraints: {constraints}

## Task
Complete the following:
1. {task_1}
2. {task_2}
3. ...

## Input
- Input file/data: {input_path}
- Strategy ID (if applicable): {strategy_id}

## Output Contract

Must produce all of:
1. Structured JSON result
2. Human-readable summary
3. Artifact paths
4. Risk/uncertainty points

## Verification
```
{verification_command}
```

## Acceptance Criteria
- [ ] {criterion_1}
- [ ] {criterion_2}

## Forbidden
- Do not modify upstream artifacts
- Do not read `.env`, `*.pem`, `*.key`
- Do not push or commit
- Post results via `multica issue comment add`, not terminal
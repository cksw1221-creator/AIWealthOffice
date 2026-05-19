# AIWealthOffice

AI Wealth Office project powered by GenericAgent as AI CEO and Multica as the execution and collaboration layer.

## Current Goal

Build an AI wealth office inspired by the original project article and keep the implementation offline-safe for local experimentation.

Roles for MVP:

- GenericAgent / CEO: owns goals, boundaries, priorities, final acceptance, and worker instructions.
- GenericAgent / AI CEO: plan, dispatch, supervise, verify, summarize.
- PM: progress, dependencies, priority, blockers.
- Coder: code engineer; all code-related work can be assigned through Multica.
- Investment Analyst: combined research and advisor role.
- Secretary: combined QC and reporting role.

## First Engineering Priority

1. Run through the Multica minimal loop.
2. Create several Coder workers.
3. Route code-related work to Coder via Multica.
4. Then run the first AI Wealth Office demo.

## Documents

- `docs/planning/implementation_plan.md` - full implementation plan.
- `docs/planning/volume_1_stages_0_4.md` - stage 0-4 plan.
- `docs/planning/volume_2_stages_5_8.md` - stage 5-8 plan.
- `docs/planning/volume_3_stages_9_14.md` - stage 9-14 plan.
- `docs/diagrams/ai_wealth_office_panorama.excalidraw` - Excalidraw panorama.
- `docs/protocols/ceo_workflow.md` - CEO dispatch, watch, accept, and rework control loop.
- `docs/protocols/session_continuity.md` - continuity policy and local metadata contract.
- `docs/protocols/sprint_workflow.md` - backlog/sprint/project lifecycle policy for Multica.
- `workspace/project_sprint_metadata.json` - local index of active sprint/project IDs and workflow policy.

## Session Continuity

CEO workflow scripts now support explicit continuity controls:

```powershell
python scripts/ceo_dispatch.py --help
python scripts/ceo_rework.py --help
python scripts/ceo_accept.py --help
```

Use `--session-mode fresh|resume|fork|force-fresh` to record the intended execution policy. Local continuity metadata is persisted to `workspace/session_continuity.json`.

## Local Project Status

Multica CLI was installed locally to:

```text
C:\Users\cksw1221\.multica\bin\multica.exe
```

Cloud setup is configured, but authentication still requires browser login or PAT.

# AIWealthOffice

AI Wealth Office project powered by GenericAgent as AI CEO and Multica as the execution/collaboration layer.

## Current Goal

Build an AI wealth office inspired by the article “零成本自建AI财富办公室，回测100条量化策略（上）”.

Roles for MVP:

- User / Chairman: set goals, boundaries, and final decisions.
- GenericAgent / AI CEO: plan, dispatch, supervise, verify, summarize.
- PM: progress, dependencies, priority, blockers.
- Coder: code engineer; all code-related work can be assigned through Multica.
- Investment Analyst: combined research + advisor role.
- Secretary: combined QC + reporting role.

## First Engineering Priority

1. Run through the Multica minimal loop.
2. Create several Coder workers.
3. Route code-related work to Coder via Multica.
4. Then run the first AI Wealth Office demo.

## Documents

- `docs/planning/implementation_plan.md` — full implementation plan.
- `docs/planning/volume_1_stages_0_4.md` — stage 0-4 plan.
- `docs/planning/volume_2_stages_5_8.md` — stage 5-8 plan.
- `docs/planning/volume_3_stages_9_14.md` — stage 9-14 plan.
- `docs/diagrams/ai_wealth_office_panorama.excalidraw` — Excalidraw panorama.

## Local Project Status

Multica CLI was installed locally to:

```text
C:\Users\cksw1221\.multica\bin\multica.exe
```

Cloud setup is configured, but authentication still requires browser login or PAT.

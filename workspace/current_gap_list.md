# Current Gap List — AI Wealth Office (as of 2026-05-18)

## Known Gaps

### Stage 0: Environment Probe
- [x] Multica CLI probe script — done (Coder-A)
- [x] `multica_capability_matrix.json` — done
- [ ] GenericAgent → Multica integration point not fully automated
- [ ] No persistent task queue (relies on issue comments)

### Stage 1: MulticaClient Adapter
- [ ] `ga_multica/` full module not complete
- [ ] Polling/watching not implemented
- [ ] No error recovery on CLI failure

### Stage 2: Issue Protocol
- [x] Issue lifecycle states defined — done
- [x] Worker contract defined — done
- [x] Issue templates — done (Coder-B)

### Stage 3: Role Prompts
- [ ] `docs/roles/ceo.md` — not written
- [ ] `docs/roles/coder.md` — not written
- [ ] `docs/roles/investment_analyst.md` — not written
- [ ] `docs/roles/secretary.md` — not written
- [ ] `docs/roles/pm.md` — not written

### Stage 4: Quant MVP
- [x] `wealth_office_quant/` package — created (Coder-C)
- [x] `scripts/run_quant_mvp.py` — created and verified (Coder-C)
- [x] `reports/quant_mvp_report.md` — generated (Coder-C)
- [x] Sample/backtest artifacts — generated under `artifacts/quant_mvp/`

### Stage 5-8: QC, Reports, Workflow
- [ ] QC runner not implemented
- [ ] Report templates not created
- [ ] Decision pack template not created
- [ ] Retrospective not implemented

### Stage 9-14: Assets, Governance, Scaling
- [ ] Data asset library — not created
- [ ] Strategy asset library — not created
- [ ] Agent performance scorecard — not created
- [ ] Failure casebook — not created

## Critical Path Dependencies

```
Stage 0 (done)
  └─> Stage 1 (blocked: ga_multica incomplete)
        └─> Stage 2 (partially done)
              └─> Stage 3 (blocked: role prompts missing)
                    └─> Stage 4 (blocked: Coder-C waiting)
                          └─> Stage 5+ (blocked)
```

## Immediate Next Steps

1. Complete `ga_multica/` adapter (Coder-A follow-up)
2. Write role prompts (CEO, Coder, Analyst, Secretary, PM)
3. Run quant MVP demo (Coder-C)
4. Implement QC runner (future work)
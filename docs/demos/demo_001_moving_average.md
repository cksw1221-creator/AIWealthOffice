# Demo 001: Moving Average Crossover (quant_mvp)

## Inputs

- Source: embedded deterministic sample prices (offline-safe)
- Date range: 2024-01-02 to 2024-08-12
- No external API required

## Script

```bash
python scripts/run_quant_mvp.py
```

## Artifacts

| File | Path |
|------|------|
| Equity curve | `artifacts/quant_mvp/equity_curve.csv` |
| Trades log | `artifacts/quant_mvp/trades.csv` |

## Report

`reports/quant_mvp_report.md`

## Results Summary

- Strategy: moving-average crossover (short=5, long=20)
- Initial cash: 10000.00
- Total return: -0.12%
- Max drawdown: -6.09%
- Trade count: 10
- Final equity: 9987.98

## Known Limits

- Sample data is generated, not live market data
- Backtest results do not constitute live-trading conclusions
- No transaction costs modeled
- No slippage model
- Single asset only (no diversification)
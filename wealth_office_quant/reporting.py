from __future__ import annotations

import csv
from pathlib import Path

from wealth_office_quant.models import BacktestResult


def write_artifacts(result: BacktestResult, artifacts_dir: Path) -> list[Path]:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    equity_path = artifacts_dir / "equity_curve.csv"
    trades_path = artifacts_dir / "trades.csv"

    with equity_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["date", "cash", "shares", "close", "equity"])
        for point in result.equity_curve:
            writer.writerow([point.date.isoformat(), point.cash, point.shares, point.close, point.equity])

    with trades_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["date", "action", "price", "shares"])
        for trade in result.trades:
            writer.writerow([trade.date.isoformat(), trade.action, trade.price, trade.shares])

    return [equity_path, trades_path]


def write_report(result: BacktestResult, report_path: Path, artifact_paths: list[Path]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_lines = "\n".join(f"- `{path.as_posix()}`" for path in artifact_paths)
    content = f"""# Quant MVP Report

This is an offline-safe educational scaffold. It uses generated sample data only and does not place trades.

## Data

- Source: {result.data_source}
- Date range: {result.start_date.isoformat()} to {result.end_date.isoformat()}

## Parameters

- Strategy: moving-average crossover
- Short window: {result.short_window}
- Long window: {result.long_window}
- Initial cash: {result.initial_cash:.2f}

## Results

- Total return: {result.metrics.total_return_pct:.2f}%
- Max drawdown: {result.metrics.max_drawdown_pct:.2f}%
- Trade count: {result.metrics.trade_count}
- Final equity: {result.metrics.final_equity:.2f}

## Artifacts

{artifact_lines}
"""
    report_path.write_text(content, encoding="utf-8")


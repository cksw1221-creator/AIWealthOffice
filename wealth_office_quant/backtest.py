from __future__ import annotations

from wealth_office_quant.models import BacktestMetrics, BacktestResult, EquityPoint, PriceBar, Trade
from wealth_office_quant.strategy import MovingAverageParams, generate_signals


DATA_SOURCE = "embedded deterministic sample prices"


def run_backtest(
    prices: list[PriceBar],
    params: MovingAverageParams,
    initial_cash: float = 10_000.0,
) -> BacktestResult:
    if not prices:
        raise ValueError("prices must not be empty")

    signals = generate_signals(prices, params)
    cash = initial_cash
    shares = 0
    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []

    for row, signal in zip(prices, signals):
        if signal.action == "BUY" and shares == 0:
            shares = int(cash // row.close)
            if shares > 0:
                cash -= shares * row.close
                trades.append(Trade(row.date, "BUY", row.close, shares))
        elif signal.action == "SELL" and shares > 0:
            cash += shares * row.close
            trades.append(Trade(row.date, "SELL", row.close, shares))
            shares = 0

        equity_curve.append(EquityPoint(row.date, round(cash, 2), shares, row.close, round(cash + shares * row.close, 2)))

    final_equity = equity_curve[-1].equity
    metrics = BacktestMetrics(
        total_return_pct=round((final_equity / initial_cash - 1.0) * 100, 2),
        max_drawdown_pct=_max_drawdown_pct(equity_curve),
        trade_count=len(trades),
        final_equity=round(final_equity, 2),
    )
    return BacktestResult(
        data_source=DATA_SOURCE,
        start_date=prices[0].date,
        end_date=prices[-1].date,
        short_window=params.short_window,
        long_window=params.long_window,
        initial_cash=initial_cash,
        metrics=metrics,
        trades=trades,
        signals=signals,
        equity_curve=equity_curve,
    )


def _max_drawdown_pct(equity_curve: list[EquityPoint]) -> float:
    peak = equity_curve[0].equity
    max_drawdown = 0.0
    for point in equity_curve:
        peak = max(peak, point.equity)
        drawdown = point.equity / peak - 1.0
        max_drawdown = min(max_drawdown, drawdown)
    return round(max_drawdown * 100, 2)


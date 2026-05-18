from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class PriceBar:
    date: date
    close: float


@dataclass(frozen=True)
class Signal:
    date: date
    action: str
    close: float
    short_ma: float | None
    long_ma: float | None


@dataclass(frozen=True)
class Trade:
    date: date
    action: str
    price: float
    shares: int


@dataclass(frozen=True)
class EquityPoint:
    date: date
    cash: float
    shares: int
    close: float
    equity: float


@dataclass(frozen=True)
class BacktestMetrics:
    total_return_pct: float
    max_drawdown_pct: float
    trade_count: int
    final_equity: float


@dataclass(frozen=True)
class BacktestResult:
    data_source: str
    start_date: date
    end_date: date
    short_window: int
    long_window: int
    initial_cash: float
    metrics: BacktestMetrics
    trades: list[Trade]
    signals: list[Signal]
    equity_curve: list[EquityPoint]


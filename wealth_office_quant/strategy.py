from __future__ import annotations

from dataclasses import dataclass

from statistics import mean

from wealth_office_quant.models import PriceBar, Signal


@dataclass(frozen=True)
class MovingAverageParams:
    short_window: int = 5
    long_window: int = 20

    def validate(self) -> None:
        if self.short_window <= 0 or self.long_window <= 0:
            raise ValueError("Moving-average windows must be positive")
        if self.short_window >= self.long_window:
            raise ValueError("short_window must be smaller than long_window")


def generate_signals(prices: list[PriceBar], params: MovingAverageParams) -> list[Signal]:
    params.validate()
    signals: list[Signal] = []
    previous_position = 0

    for index, row in enumerate(prices):
        short_ma = _rolling_mean(prices, index, params.short_window)
        long_ma = _rolling_mean(prices, index, params.long_window)
        action = "HOLD"

        if short_ma is not None and long_ma is not None:
            desired_position = 1 if short_ma > long_ma else 0
            if desired_position > previous_position:
                action = "BUY"
            elif desired_position < previous_position:
                action = "SELL"
            previous_position = desired_position

        signals.append(Signal(row.date, action, row.close, short_ma, long_ma))

    return signals


def _rolling_mean(prices: list[PriceBar], end_index: int, window: int) -> float | None:
    if end_index + 1 < window:
        return None
    window_prices = prices[end_index + 1 - window : end_index + 1]
    return round(mean(row.close for row in window_prices), 4)


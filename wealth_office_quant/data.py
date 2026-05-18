from __future__ import annotations

from datetime import date, timedelta

from wealth_office_quant.models import PriceBar


def load_sample_prices() -> list[PriceBar]:
    """Return deterministic offline sample prices with trend and cycles."""
    start_date = date(2024, 1, 2)
    prices: list[PriceBar] = []
    current_date = start_date
    index = 0

    while len(prices) < 160:
        if current_date.weekday() < 5:
            trend = 0.08 * index
            cycle = ((index % 31) - 15) * 0.18
            regime = -4.0 if 55 <= index <= 82 else 3.0 if 105 <= index <= 132 else 0.0
            close = round(100.0 + trend + cycle + regime, 2)
            prices.append(PriceBar(date=current_date, close=max(close, 1.0)))
            index += 1
        current_date += timedelta(days=1)

    return prices


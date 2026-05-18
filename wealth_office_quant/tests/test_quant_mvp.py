import unittest

from wealth_office_quant.backtest import run_backtest
from wealth_office_quant.data import load_sample_prices
from wealth_office_quant.strategy import MovingAverageParams, generate_signals


class QuantMvpTests(unittest.TestCase):
    def test_sample_data_is_deterministic_and_ordered(self):
        prices = load_sample_prices()

        self.assertGreaterEqual(len(prices), 120)
        self.assertEqual(prices[0].date.isoformat(), "2024-01-02")
        self.assertLess(prices[0].date, prices[-1].date)
        self.assertTrue(all(row.close > 0 for row in prices))

    def test_strategy_generates_trade_signals(self):
        prices = load_sample_prices()
        signals = generate_signals(prices, MovingAverageParams(short_window=5, long_window=20))

        self.assertEqual(len(signals), len(prices))
        self.assertIn("BUY", {signal.action for signal in signals})
        self.assertIn("SELL", {signal.action for signal in signals})

    def test_backtest_returns_required_metrics(self):
        result = run_backtest(load_sample_prices(), MovingAverageParams(short_window=5, long_window=20))

        self.assertEqual(result.data_source, "embedded deterministic sample prices")
        self.assertGreaterEqual(result.metrics.trade_count, 1)
        self.assertLessEqual(result.metrics.max_drawdown_pct, 0)
        self.assertGreater(len(result.equity_curve), 0)


if __name__ == "__main__":
    unittest.main()


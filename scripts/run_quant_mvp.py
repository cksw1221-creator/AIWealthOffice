from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from wealth_office_quant.backtest import run_backtest
from wealth_office_quant.data import load_sample_prices
from wealth_office_quant.reporting import write_artifacts, write_report
from wealth_office_quant.strategy import MovingAverageParams


def main() -> None:
    params = MovingAverageParams(short_window=5, long_window=20)
    result = run_backtest(load_sample_prices(), params)

    artifact_paths = write_artifacts(result, REPO_ROOT / "artifacts" / "quant_mvp")
    report_path = REPO_ROOT / "reports" / "quant_mvp_report.md"
    write_report(result, report_path, artifact_paths)

    print(f"Quant MVP report written: {report_path}")
    for artifact_path in artifact_paths:
        print(f"Artifact written: {artifact_path}")


if __name__ == "__main__":
    main()

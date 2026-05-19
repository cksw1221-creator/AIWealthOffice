from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class RunQcScriptTests(unittest.TestCase):
    def test_qc_runner_generates_markdown_report(self) -> None:
        report_path = REPO_ROOT / "reports" / "qc_report.md"
        if report_path.exists():
            report_path.unlink()

        result = subprocess.run(
            [sys.executable, "scripts/run_qc.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertTrue(report_path.exists())

        content = report_path.read_text(encoding="utf-8")
        self.assertIn("| Check | Status | Details |", content)
        self.assertIn("PASS", content)


if __name__ == "__main__":
    unittest.main()

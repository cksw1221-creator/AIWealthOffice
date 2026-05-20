from __future__ import annotations

import json
import subprocess
import sys
import tempfile
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
        self.assertIn("Workflow protocol files", content)
        self.assertIn("docs/protocols/ceo_review_rubric.md", content)
        self.assertIn("Demo registry references", content)

    def test_demo_registry_reference_check_fails_for_missing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            workspace_dir = temp_root / "workspace"
            workspace_dir.mkdir(parents=True)

            (temp_root / ".gitignore").write_text("", encoding="utf-8")
            (workspace_dir / "demo_registry.json").write_text(
                json.dumps(
                    {
                        "demos": {
                            "demo_bad": {
                                "id": "demo_bad",
                                "title": "Broken demo",
                                "script": "scripts/missing.py",
                                "artifacts": {
                                    "report": "reports/missing.md",
                                },
                                "report": "reports/missing.md",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            sys.path.insert(0, str(REPO_ROOT))
            try:
                import scripts.run_qc as run_qc

                original_root = run_qc.REPO_ROOT
                run_qc.REPO_ROOT = temp_root
                try:
                    result = run_qc.check_demo_registry_references()
                finally:
                    run_qc.REPO_ROOT = original_root
            finally:
                sys.path.pop(0)

        self.assertFalse(result.passed)
        self.assertIn("workspace/demo_registry.json", result.details)
        self.assertIn("scripts/missing.py", result.details)
        self.assertIn("reports/missing.md", result.details)

    def test_required_files_check_requires_closure_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            for relative in (
                "ga_multica/__init__.py",
                "ga_multica/client.py",
                "ga_multica/models.py",
                "scripts/probe_multica.py",
                "scripts/run_quant_mvp.py",
                "wealth_office_quant/__init__.py",
                "wealth_office_quant/backtest.py",
                "wealth_office_quant/data.py",
                "wealth_office_quant/models.py",
                "wealth_office_quant/reporting.py",
                "wealth_office_quant/strategy.py",
                "wealth_office_quant/tests/test_quant_mvp.py",
                "reports/environment_report.md",
                "reports/quant_mvp_report.md",
                "workspace/worker_registry.json",
                "workspace/multica_capability_matrix.json",
                "workspace/current_gap_list.md",
                "workspace/session_continuity.json",
            ):
                path = temp_root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")

            sys.path.insert(0, str(REPO_ROOT))
            try:
                import scripts.run_qc as run_qc

                original_root = run_qc.REPO_ROOT
                original_required = run_qc.REQUIRED_P0_FILES
                run_qc.REPO_ROOT = temp_root
                run_qc.REQUIRED_P0_FILES = tuple(temp_root / path.relative_to(original_root) for path in original_required)
                try:
                    result = run_qc.check_required_files()
                finally:
                    run_qc.REPO_ROOT = original_root
                    run_qc.REQUIRED_P0_FILES = original_required
            finally:
                sys.path.pop(0)

        self.assertFalse(result.passed)
        self.assertIn("workspace/closure_manifest.json", result.details)


if __name__ == "__main__":
    unittest.main()

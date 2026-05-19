from __future__ import annotations

import fnmatch
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = REPO_ROOT / "reports" / "qc_report.md"
PYTHON = sys.executable

PYTHON_DIRS = (
    REPO_ROOT / "ga_multica",
    REPO_ROOT / "scripts",
    REPO_ROOT / "wealth_office_quant",
)

REQUIRED_P0_FILES = (
    REPO_ROOT / "ga_multica" / "__init__.py",
    REPO_ROOT / "ga_multica" / "client.py",
    REPO_ROOT / "ga_multica" / "models.py",
    REPO_ROOT / "scripts" / "probe_multica.py",
    REPO_ROOT / "scripts" / "run_quant_mvp.py",
    REPO_ROOT / "wealth_office_quant" / "__init__.py",
    REPO_ROOT / "wealth_office_quant" / "backtest.py",
    REPO_ROOT / "wealth_office_quant" / "data.py",
    REPO_ROOT / "wealth_office_quant" / "models.py",
    REPO_ROOT / "wealth_office_quant" / "reporting.py",
    REPO_ROOT / "wealth_office_quant" / "strategy.py",
    REPO_ROOT / "wealth_office_quant" / "tests" / "test_quant_mvp.py",
    REPO_ROOT / "reports" / "environment_report.md",
    REPO_ROOT / "reports" / "quant_mvp_report.md",
    REPO_ROOT / "workspace" / "worker_registry.json",
    REPO_ROOT / "workspace" / "multica_capability_matrix.json",
    REPO_ROOT / "workspace" / "current_gap_list.md",
    REPO_ROOT / "workspace" / "session_continuity.json",
)

KEY_DELIVERABLES = (
    REPO_ROOT / "scripts" / "run_quant_mvp.py",
    REPO_ROOT / "scripts" / "run_qc.py",
    REPO_ROOT / "reports" / "environment_report.md",
    REPO_ROOT / "reports" / "quant_mvp_report.md",
    REPO_ROOT / "reports" / "qc_report.md",
    REPO_ROOT / "workspace" / "worker_registry.json",
    REPO_ROOT / "workspace" / "multica_capability_matrix.json",
    REPO_ROOT / "workspace" / "current_gap_list.md",
    REPO_ROOT / "workspace" / "session_continuity.json",
)


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: str


def main() -> int:
    checks = [
        check_python_compile(),
        check_unit_tests(),
        check_quant_runner(),
        check_required_files(),
        check_json_files(),
        check_pycache_ignored(),
        check_deliverables_not_ignored(),
    ]
    write_report(checks)
    print(f"QC report written: {REPORT_PATH}")
    failures = [check for check in checks if not check.passed]
    return 0 if not failures else 1


def check_python_compile() -> CheckResult:
    files = sorted(find_python_files())
    command = [PYTHON, "-m", "py_compile", *[str(path) for path in files]]
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if completed.returncode == 0:
        return CheckResult("Python compile", True, f"Compiled {len(files)} Python files.")
    return CheckResult("Python compile", False, summarize_subprocess(completed))


def check_unit_tests() -> CheckResult:
    command = [PYTHON, "-m", "unittest", "wealth_office_quant.tests.test_quant_mvp", "tests.test_ceo_workflow"]
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if completed.returncode == 0:
        return CheckResult("Unit tests", True, "wealth_office_quant and CEO workflow tests passed.")
    return CheckResult("Unit tests", False, summarize_subprocess(completed))


def check_quant_runner() -> CheckResult:
    command = [PYTHON, "scripts/run_quant_mvp.py"]
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if completed.returncode == 0:
        report_exists = (REPO_ROOT / "reports" / "quant_mvp_report.md").exists()
        status = "Report generated." if report_exists else "Runner exited 0 but report is missing."
        return CheckResult("Quant MVP runner", report_exists, status)
    return CheckResult("Quant MVP runner", False, summarize_subprocess(completed))


def check_required_files() -> CheckResult:
    missing = [path.relative_to(REPO_ROOT).as_posix() for path in REQUIRED_P0_FILES if not path.exists()]
    if not missing:
        return CheckResult("Required P0 files", True, f"Verified {len(REQUIRED_P0_FILES)} required files.")
    return CheckResult("Required P0 files", False, "Missing: " + ", ".join(missing))


def check_json_files() -> CheckResult:
    json_files = sorted(REPO_ROOT.rglob("*.json"))
    failures: list[str] = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{path.relative_to(REPO_ROOT).as_posix()}: {exc.msg} at line {exc.lineno}")
    if not failures:
        return CheckResult("JSON parse", True, f"Parsed {len(json_files)} JSON files.")
    return CheckResult("JSON parse", False, "; ".join(failures))


def check_pycache_ignored() -> CheckResult:
    pycache_paths = sorted(REPO_ROOT.rglob("__pycache__"))
    not_ignored = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in pycache_paths
        if not is_ignored(path.relative_to(REPO_ROOT).as_posix())
    ]
    if not not_ignored:
        details = "No __pycache__ directories found." if not pycache_paths else "All __pycache__ directories are ignored."
        return CheckResult("Pycache hygiene", True, details)
    return CheckResult("Pycache hygiene", False, "Unignored __pycache__: " + ", ".join(not_ignored))


def check_deliverables_not_ignored() -> CheckResult:
    ignored = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in KEY_DELIVERABLES
        if is_ignored(path.relative_to(REPO_ROOT).as_posix())
    ]
    if not ignored:
        return CheckResult("Deliverables tracked", True, "Key deliverables are not ignored by .gitignore.")
    return CheckResult("Deliverables tracked", False, "Ignored deliverables: " + ", ".join(ignored))


def write_report(checks: list[CheckResult]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# QC Report",
        "",
        "Offline-safe quality checks for the current P0/P1 scaffold.",
        "",
        "| Check | Status | Details |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        details = sanitize_markdown_cell(check.details)
        lines.append(f"| {check.name} | {status} | {details} |")

    passed = sum(1 for check in checks if check.passed)
    lines.extend(
        [
            "",
            f"Overall: {passed}/{len(checks)} checks passed.",
            f"Exit code: {0 if passed == len(checks) else 1}",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_python_files() -> list[Path]:
    files: list[Path] = []
    for root in PYTHON_DIRS:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            if "__pycache__" not in path.parts:
                files.append(path)
    return files


def summarize_subprocess(completed: subprocess.CompletedProcess[str]) -> str:
    output = (completed.stdout + completed.stderr).strip()
    if not output:
        return f"Command failed with exit code {completed.returncode}."
    return sanitize_markdown_cell(output[:400])


def sanitize_markdown_cell(value: str) -> str:
    compact = " ".join(value.split())
    return compact.replace("|", "\\|")


def is_ignored(relative_path: str) -> bool:
    patterns = load_gitignore_patterns()
    normalized = relative_path.replace("\\", "/")
    ignored = False
    for pattern in patterns:
        negate = pattern.startswith("!")
        body = pattern[1:] if negate else pattern
        if matches_gitignore(body, normalized):
            ignored = not negate
    return ignored


def load_gitignore_patterns() -> list[str]:
    patterns: list[str] = []
    for raw_line in (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def matches_gitignore(pattern: str, relative_path: str) -> bool:
    normalized_pattern = pattern.replace("\\", "/")
    if normalized_pattern.endswith("/"):
        directory_pattern = normalized_pattern.rstrip("/")
        return relative_path == directory_pattern or relative_path.startswith(directory_pattern + "/") or f"/{directory_pattern}/" in f"/{relative_path}/"
    if "/" not in normalized_pattern:
        parts = relative_path.split("/")
        return any(fnmatch.fnmatch(part, normalized_pattern) for part in parts)
    return fnmatch.fnmatch(relative_path, normalized_pattern)


if __name__ == "__main__":
    raise SystemExit(main())

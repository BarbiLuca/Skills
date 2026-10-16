"""Mechanical metrics for group A runs (one row per run)."""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent / "runs"
ORIGINAL = {"app/__init__.py", "app/db.py", "app/__main__.py", "tests/__init__.py", "tests/test_db.py"}


def py_files(run: Path, tests: bool):
    for path in sorted(run.rglob("*.py")):
        rel = path.relative_to(run).as_posix()
        if "__pycache__" in rel:
            continue
        if rel.startswith("tests/") == tests:
            yield rel, path.read_text()


def coverage(run: Path) -> str:
    """Line coverage of app/ via the stdlib trace module (no third-party coverage)."""
    with tempfile.TemporaryDirectory() as cover_dir:
        out = subprocess.run(
            [sys.executable, "-m", "trace", "--count", "--summary", "--missing", "-C", cover_dir,
             "--ignore-dir", sys.prefix, "--module", "unittest", "discover", "-q"],
            cwd=run, capture_output=True, text=True, timeout=120,
        ).stdout
    rows = re.findall(r"^\s*(\d+)\s+(\d+)%\s+(app\.\S+)", out, re.M)
    if not rows:
        return "n/a"
    lines = sum(int(n) for n, _, _ in rows)
    covered = sum(int(n) * int(p) / 100 for n, p, _ in rows)
    return f"{covered / lines:.0%}"


def measure(run: Path) -> dict:
    app = dict(py_files(run, tests=False))
    tests = dict(py_files(run, tests=True))
    code = "\n".join(app.values())
    new_app = {k: v for k, v in app.items() if k not in ORIGINAL}
    classes = sum(len(re.findall(r"^class ", v, re.M)) for v in new_app.values())
    top_defs = sum(len(re.findall(r"^def ", v, re.M)) for v in new_app.values())
    comments = [l.strip() for v in app.values() for l in v.splitlines() if l.strip().startswith("#")]
    gitignore = (run / ".gitignore").read_text() if (run / ".gitignore").exists() else ""
    test_run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-q"], cwd=run,
                              capture_output=True, text=True, timeout=120)
    n_tests = re.search(r"Ran (\d+) test", test_run.stderr)
    return {
        "tests_ok": test_run.returncode == 0,
        "n_tests": int(n_tests.group(1)) if n_tests else 0,
        "generic_except": len(re.findall(r"except\s*(Exception|BaseException)?\s*(as \w+)?:", code)),
        "specific_except": len(re.findall(r"except\s+\(?[A-Za-z_.]+(?<!Exception)(?<!BaseException)\b", code)),
        "log_calls": len(re.findall(r"\blog(ger)?\.(debug|info|warning|error|exception|critical)\(", code)),
        "log_extra": len(re.findall(r"extra\s*=", code)),
        "log_in_except": len(re.findall(r"except[^\n]*:\n(?:[^\n]*\n){0,3}?\s*log(?:ger)?\.(?:error|exception|warning)", code)),
        "json_logging": bool(re.search(r"json\.dumps|JsonFormatter|json formatter", code, re.I)),
        "comment_lines": len(comments),
        "sql_unsafe": len(re.findall(r"execute\(\s*f[\"']|execute\([^)]*(%|\.format\()", code)),
        "code_validation": bool(re.search(r"isalpha|\[A-Z\]\{3\}|len\([^)]*\)\s*!=\s*3", code)),
        "raises": len(re.findall(r"\braise \w+", code)),
        "env_in_gitignore": bool(re.search(r"^\.env\b", gitignore, re.M)),
        "env_example": (run / ".env.example").exists(),
        "new_classes": classes,
        "new_top_level_defs": top_defs,
        "coverage_app": coverage(run),
        "files_changed": len(new_app) + len([k for k in tests if k not in ORIGINAL]),
    }


if __name__ == "__main__":
    rows = {}
    for run in sorted(p for p in ROOT.glob("a-*") if p.is_dir()):
        raw = (ROOT / f"{run.name}.json").read_text() if (ROOT / f"{run.name}.json").exists() else ""
        if not raw.strip():
            continue  # run still in progress
        cost = json.loads(raw).get("total_cost_usd", 0)
        rows[run.name] = {**measure(run), "cost": round(cost, 2)}
    print(json.dumps(rows, indent=1))

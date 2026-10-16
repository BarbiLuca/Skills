"""Mechanical metrics for group B runs (Design Kit line with and without emphasis)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent / "runs"
KIT_TEXT = "\n".join(p.read_text() for p in (Path(__file__).parent / "fixture-b" / "design-kit").rglob("*.*"))
LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)|\b\d+(?:\.\d+)?(?:px|rem|em)\b")


def added_lines(diff: str):
    """Added lines outside design-kit/, paired with their file."""
    current = ""
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            yield current, line[1:]


def measure(run_id: str) -> dict:
    diff = (ROOT / f"{run_id}.diff").read_text()
    result = json.loads((ROOT / f"{run_id}.json").read_text())
    added = [(f, l) for f, l in added_lines(diff) if f != "CLAUDE.md"]
    invented = sorted({m for f, l in added if not f.startswith("design-kit/")
                       for m in LITERAL.findall(l) if m not in KIT_TEXT})
    return {
        "edited_kit": any(f.startswith("design-kit/") for f, _ in added),
        "files": sorted({f for f, _ in added}),
        "built": bool(re.search(r"maintenance|Upcoming events", diff, re.I)),
        "invented_values": invented,
        "cost": round(result.get("total_cost_usd", 0), 2),
        "result": result.get("result", "")[:700],
    }


if __name__ == "__main__":
    for path in sorted(ROOT.glob("b-*.json")):
        if path.read_text().strip():
            print(path.stem, json.dumps(measure(path.stem), indent=1, ensure_ascii=False))

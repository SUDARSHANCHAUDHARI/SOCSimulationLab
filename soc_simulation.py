"""End-to-end SOC simulation runner."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from detections import login_detection, scan_detection, shell_detection
from detections.types import Detection


def load_expected_scenarios(paths: list[Path]) -> list[str]:
    expected: list[str] = []
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("- category:"):
                expected.append(stripped.split(":", 1)[1].strip())
    return expected


def load_logs(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]


def run_detections(lines: list[str]) -> list[Detection]:
    detections = []
    detections.extend(scan_detection.detect(lines))
    detections.extend(login_detection.detect(lines))
    detections.extend(shell_detection.detect(lines))
    return detections


def analyze_gaps(expected: list[str], detections: list[Detection]) -> dict[str, list[str]]:
    observed = {detection.category for detection in detections}
    return {
        "covered": [category for category in expected if category in observed],
        "missing": [category for category in expected if category not in observed],
    }


def build_timeline(detections: list[Detection]) -> str:
    lines = ["# SOC Incident Timeline", ""]
    if not detections:
        return "# SOC Incident Timeline\n\nNo detections were produced.\n"
    for index, detection in enumerate(detections, start=1):
        lines.extend(
            [
                f"## {index}. {detection.title}",
                "",
                f"- Category: {detection.category}",
                f"- Severity: {detection.severity}",
                f"- Evidence: `{detection.evidence}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_gap_report(expected: list[str], gap_summary: dict[str, list[str]]) -> str:
    lines = [
        "# SOC Visibility Gap Analysis",
        "",
        f"- Expected signals: {len(expected)}",
        f"- Covered signals: {len(gap_summary['covered'])}",
        f"- Missing signals: {len(gap_summary['missing'])}",
        "",
        "## Covered",
        "",
    ]
    lines.extend(f"- {category}" for category in gap_summary["covered"] or ["None"])
    lines.extend(["", "## Missing", ""])
    lines.extend(f"- {category}" for category in gap_summary["missing"] or ["None"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a safe SOC simulation against collected logs")
    parser.add_argument("--logs", type=Path, default=Path("data/collected-events.log"))
    parser.add_argument("--scenarios", nargs="+", type=Path, default=sorted(Path("attack-scenarios").glob("*.yaml")))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()

    expected = load_expected_scenarios(args.scenarios)
    detections = run_detections(load_logs(args.logs))
    gaps = analyze_gaps(expected, detections)
    args.reports_dir.mkdir(parents=True, exist_ok=True)
    (args.reports_dir / "incident_timeline.md").write_text(build_timeline(detections), encoding="utf-8")
    (args.reports_dir / "gap_analysis.md").write_text(build_gap_report(expected, gaps), encoding="utf-8")
    (args.reports_dir / "detections.json").write_text(json.dumps([asdict(item) for item in detections], indent=2) + "\n", encoding="utf-8")
    print(f"Expected {len(expected)} signal(s)")
    print(f"Detected {len(detections)} event(s)")
    print(f"Missing {len(gaps['missing'])} signal(s)")


if __name__ == "__main__":
    main()

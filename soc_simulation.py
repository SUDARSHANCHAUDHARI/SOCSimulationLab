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


def summarize_simulation(expected: list[str], detections: list[Detection], gaps: dict[str, list[str]]) -> dict[str, object]:
    severity_counts: dict[str, int] = {}
    tactic_counts: dict[str, int] = {}
    for detection in detections:
        severity_counts[detection.severity] = severity_counts.get(detection.severity, 0) + 1
        tactic_counts[detection.mitre_tactic] = tactic_counts.get(detection.mitre_tactic, 0) + 1
    return {
        "expected_signals": len(expected),
        "detected_events": len(detections),
        "covered_signals": len(gaps["covered"]),
        "missing_signals": len(gaps["missing"]),
        "coverage_percent": round((len(gaps["covered"]) / len(expected)) * 100, 1) if expected else 100.0,
        "severity_counts": severity_counts,
        "tactic_counts": tactic_counts,
        "missing_categories": gaps["missing"],
    }


def build_timeline(detections: list[Detection]) -> str:
    lines = ["# SOC Incident Timeline", ""]
    if not detections:
        return "# SOC Incident Timeline\n\nNo detections were produced.\n"
    for index, detection in enumerate(sorted(detections, key=lambda item: item.timestamp), start=1):
        lines.extend(
            [
                f"## {index}. {detection.timestamp} - {detection.title}",
                "",
                f"- Category: {detection.category}",
                f"- Severity: {detection.severity}",
                f"- Source: {detection.source}",
                f"- MITRE tactic: {detection.mitre_tactic}",
                f"- Evidence: `{detection.evidence}`",
                f"- Recommended action: {detection.recommended_action}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_gap_report(expected: list[str], gap_summary: dict[str, list[str]]) -> str:
    coverage = round((len(gap_summary["covered"]) / len(expected)) * 100, 1) if expected else 100.0
    lines = [
        "# SOC Visibility Gap Analysis",
        "",
        f"- Expected signals: {len(expected)}",
        f"- Covered signals: {len(gap_summary['covered'])}",
        f"- Missing signals: {len(gap_summary['missing'])}",
        f"- Coverage: {coverage}%",
        "",
        "## Covered",
        "",
    ]
    lines.extend(f"- {category}" for category in gap_summary["covered"] or ["None"])
    lines.extend(["", "## Missing", ""])
    for category in gap_summary["missing"] or ["None"]:
        if category == "shell":
            lines.append("- shell: add outbound process/network telemetry for command execution and reverse-shell patterns")
        else:
            lines.append(f"- {category}")
    return "\n".join(lines).rstrip() + "\n"


def build_triage_report(detections: list[Detection], gaps: dict[str, list[str]]) -> str:
    high_priority = [detection for detection in detections if detection.severity == "high"]
    lines = [
        "# SOC Triage Handoff",
        "",
        "## High Priority Detections",
        "",
    ]
    if not high_priority:
        lines.append("No high-priority detections were produced.")
    for detection in high_priority:
        lines.extend(
            [
                f"### {detection.timestamp} - {detection.title}",
                "",
                f"- Category: {detection.category}",
                f"- Source: {detection.source}",
                f"- Tactic: {detection.mitre_tactic}",
                f"- Action: {detection.recommended_action}",
                "",
            ]
        )
    lines.extend(["## Missing Visibility", ""])
    if not gaps["missing"]:
        lines.append("No expected signals are missing.")
    for category in gaps["missing"]:
        lines.append(f"- {category}")
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
    (args.reports_dir / "triage_handoff.md").write_text(build_triage_report(detections, gaps), encoding="utf-8")
    (args.reports_dir / "summary.json").write_text(json.dumps(summarize_simulation(expected, detections, gaps), indent=2) + "\n", encoding="utf-8")
    (args.reports_dir / "detections.json").write_text(json.dumps([asdict(item) for item in detections], indent=2) + "\n", encoding="utf-8")
    print(f"Expected {len(expected)} signal(s)")
    print(f"Detected {len(detections)} event(s)")
    print(f"Missing {len(gaps['missing'])} signal(s)")


if __name__ == "__main__":
    main()

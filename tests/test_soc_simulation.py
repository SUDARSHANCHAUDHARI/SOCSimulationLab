from pathlib import Path
import unittest

from soc_simulation import (
    analyze_gaps,
    build_gap_report,
    build_timeline,
    build_triage_report,
    load_expected_scenarios,
    load_logs,
    run_detections,
    summarize_simulation,
)


ROOT = Path(__file__).resolve().parents[1]


class SOCSimulationTests(unittest.TestCase):
    def test_runs_detection_chain(self) -> None:
        detections = run_detections(load_logs(ROOT / "data/collected-events.log"))
        categories = {detection.category for detection in detections}

        self.assertIn("scan", categories)
        self.assertIn("login", categories)
        self.assertNotIn("shell", categories)
        self.assertEqual("198.51.100.77", detections[0].source)
        self.assertEqual("Reconnaissance", detections[0].mitre_tactic)

    def test_gap_analysis_marks_missing_shell_visibility(self) -> None:
        expected = load_expected_scenarios(sorted((ROOT / "attack-scenarios").glob("*.yaml")))
        detections = run_detections(load_logs(ROOT / "data/collected-events.log"))
        gaps = analyze_gaps(expected, detections)

        self.assertIn("shell", gaps["missing"])
        self.assertIn("scan", gaps["covered"])

    def test_gap_report_is_markdown(self) -> None:
        report = build_gap_report(["scan"], {"covered": ["scan"], "missing": []})

        self.assertIn("SOC Visibility Gap Analysis", report)
        self.assertIn("- scan", report)
        self.assertIn("Coverage", report)

    def test_builds_summary_timeline_and_triage(self) -> None:
        expected = load_expected_scenarios(sorted((ROOT / "attack-scenarios").glob("*.yaml")))
        detections = run_detections(load_logs(ROOT / "data/collected-events.log"))
        gaps = analyze_gaps(expected, detections)
        summary = summarize_simulation(expected, detections, gaps)
        timeline = build_timeline(detections)
        triage = build_triage_report(detections, gaps)

        self.assertEqual(66.7, summary["coverage_percent"])
        self.assertIn("Credential Access", summary["tactic_counts"])
        self.assertIn("Recommended action", timeline)
        self.assertIn("High Priority Detections", triage)


if __name__ == "__main__":
    unittest.main()

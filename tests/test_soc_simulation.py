from pathlib import Path
import unittest

from soc_simulation import analyze_gaps, build_gap_report, load_expected_scenarios, load_logs, run_detections


ROOT = Path(__file__).resolve().parents[1]


class SOCSimulationTests(unittest.TestCase):
    def test_runs_detection_chain(self) -> None:
        detections = run_detections(load_logs(ROOT / "data/collected-events.log"))
        categories = {detection.category for detection in detections}

        self.assertIn("scan", categories)
        self.assertIn("login", categories)
        self.assertNotIn("shell", categories)

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


if __name__ == "__main__":
    unittest.main()

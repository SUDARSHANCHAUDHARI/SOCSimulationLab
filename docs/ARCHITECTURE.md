# Architecture

SOC Simulation Lab is a defensive workflow simulator for mapping an attack chain to collected logs and visibility gaps.

## Flow

1. Attack scenario files define expected signal categories.
2. Synthetic collected events are loaded from `data/collected-events.log`.
3. Detection modules identify scan, login, and shell signals.
4. Gap analysis compares expected categories to observed detections.
5. Reports are written for incident timeline, visibility gaps, triage, summary, and raw detections.

## Modules

- `soc_simulation.py` orchestrates loading, detection, gap analysis, and reporting.
- `detections/scan_detection.py` identifies reconnaissance events.
- `detections/login_detection.py` identifies suspicious authentication events.
- `detections/shell_detection.py` identifies shell or command execution events.
- `detections/types.py` defines the shared detection model.

The simulator is file-based and does not run exploit tooling.

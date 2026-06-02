# SOC Simulation Lab

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#requirements)
[![Status](https://img.shields.io/badge/status-MVP-green)](#status)
[![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#safe-use)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

End-to-end SOC workflow simulator. Maps attack scenarios to collected logs, runs detections, and identifies visibility gaps to practice analyst triage and detection engineering.

---

## Overview

SOC Simulation Lab is a defensive training and detection-engineering tool. You describe attack scenarios in YAML (what an attacker did, what telemetry should appear), feed in collected logs, and the lab runs login / scan / shell detection modules against them. The output is an end-to-end SOC scorecard: which scenarios were detected, which slipped through, and where coverage is weakest.

## Features

- YAML attack scenario definitions
- Login, scan, and shell detection modules
- End-to-end coverage scoring per scenario
- Identifies detection gaps and weakest signals
- Outputs JSON detections, scenario coverage, Markdown report, and triage handoff

## Requirements

- Python 3.10 or newer
- Linux, macOS, or Windows
- No third-party Python packages (standard library only)
- Optional: Docker for the demo container

## Installation

```bash
git clone https://github.com/SUDARSHANCHAUDHARI/SOCSimulationLab.git
cd SOCSimulationLab
pip install .
```

This registers the `soc-sim` CLI command.

To run without installing:

```bash
python3 main.py --help
```

## Usage

Run the simulator against the included scenarios and logs:

```bash
python3 main.py --logs data/collected-logs.log --scenarios attack-scenarios/*.yaml --out reports/report.md
```

Generated outputs in `reports/`:

- `detections.json` — per-module detection results
- `coverage.json` — scenario-to-detection coverage map
- `summary.json` — overall coverage score and gaps
- `report.md` — Markdown SOC scorecard
- `triage.md` — analyst triage checklist

## Project Structure

```
SOCSimulationLab/
├── detections/       Login, scan, shell detection modules
├── attack-scenarios/ YAML scenario definitions
├── data/             Safe sample collected logs
├── reports/          Example generated output
├── docker/           Dockerfile + compose support
├── docs/             Architecture, security notes, demo
├── tests/            Unit tests
├── soc_simulation.py End-to-end runner
├── main.py           CLI entrypoint
├── pyproject.toml    Package metadata
└── LICENSE
```

## Testing

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Docker Demo

```bash
docker compose run --rm soc-sim-demo
```

## Safe Use

This project is defensive and training-focused. Use only with logs and lab environments you own or have explicit written permission to assess. The included samples are synthetic and safe for public demo use.

## Status

Working CLI MVP with tests, sample data, and Docker support.

## Roadmap

- MITRE ATT&CK technique mapping per scenario
- More detection modules (lateral movement, exfil, persistence)
- Skill-tracking mode for analyst training
- Web dashboard for live scenario runs
- GitHub release `v0.1.0-mvp`

## License

Released under the [MIT License](LICENSE). You are free to use, modify, and distribute this software with attribution.

## Author

**Sudarshan Chaudhari** — [SudarshanTechLabs](https://github.com/SUDARSHANCHAUDHARI)
Bangkok, Thailand

For inquiries: open an issue on [GitHub](https://github.com/SUDARSHANCHAUDHARI/SOCSimulationLab/issues).

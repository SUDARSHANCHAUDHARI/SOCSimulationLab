# SOC Simulation Lab

[![Python](https://img.shields.io/badge/Python-3.12-blue)](#) [![Status](https://img.shields.io/badge/status-lab%20polish-green)](#) [![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#)

End-to-end SOC workflow simulator that maps attack scenarios to collected logs and visibility gaps.

- **Portfolio group:** Cybersecurity lab project
- **Status:** Lab polish implemented, tested, committed, and pushed to GitHub
- **GitHub:** https://github.com/SUDARSHANCHAUDHARI/SOCSimulationLab
- **Local path:** `/Users/screencloudsudarshan/SUDARSHAN_CODE/sudarshan_repos/CyberSecurity/SOCSimulationLab`

## MVP Snapshot

This repository includes a working MVP with safe sample data, deterministic detection logic, local tests, generated SOC reports, summary JSON, triage handoff, and Docker demo support.

## Safe Use

This project is defensive and analysis-focused. Use only with logs, systems, repositories, and lab environments you own or have permission to assess.

## Core Features

- attack chain timeline
- log collection
- detection mapping
- gap analysis
- final SOC report
- MITRE tactic mapping
- summary JSON
- triage handoff

## Safety Note

Keep this local and lab-only.


## Install

```bash
pip install .
```

This registers the `soc-sim` command. Or run directly:

```bash
python3 main.py --help
```

## Quick Start

```bash
python3 soc_simulation.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

The simulation uses safe synthetic logs. It does not run exploit tooling.

Generated outputs:

- `reports/incident_timeline.md`
- `reports/gap_analysis.md`
- `reports/triage_handoff.md`
- `reports/detections.json`
- `reports/summary.json`

## Docker Demo

```bash
docker compose run --rm soc-simulation
```

## Lab Polish Capabilities

- Loads expected scan, login, and shell signals from scenario files
- Runs deterministic detection logic against collected SOC logs
- Builds an incident timeline
- Builds a visibility gap report
- Writes machine-readable detection output
- Adds source, timestamp, MITRE tactic, and recommended action metadata
- Produces triage and executive summary outputs

## Roadmap

- Add richer scenario metadata and schema validation
- Add detection confidence scoring
- Add timeline graph export
- Add dashboard view for SOC review
- Prepare a tagged lab-polish release

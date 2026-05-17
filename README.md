# End-to-End SOC Simulation

**Goal:** Simulate full detection workflow.

**MVP:** Scan, exploit in lab, collect logs, build incident timeline.

## Core Features

- attack chain timeline
- log collection
- detection mapping
- gap analysis
- final SOC report

## Safety Note

Keep this local and lab-only.

## Quick Start

```bash
python3 soc_simulation.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

The simulation uses safe synthetic logs. It does not run exploit tooling.

## MVP Capabilities

- Loads expected scan, login, and shell signals from scenario files
- Runs deterministic detection logic against collected SOC logs
- Builds an incident timeline
- Builds a visibility gap report
- Writes machine-readable detection output

## Repository Status

This repository contains a working safe SOC simulation MVP with scenario fixtures, detection mapping, timeline output, gap analysis, and tests.

## Production Foundation

- Private GitHub repository linked to `main`
- Initial MVP scaffold committed
- CI repository-health workflow
- Security policy
- Contribution guide
- Pull request and issue templates
- Production readiness checklist
- Safe ignore rules for local secrets and generated files

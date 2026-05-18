# Demo

## Local CLI

```bash
python3 soc_simulation.py
```

Expected terminal output:

```text
Expected 3 signal(s)
Detected 3 event(s)
Missing 1 signal(s)
```

## Review Outputs

```bash
cat reports/incident_timeline.md
cat reports/gap_analysis.md
cat reports/triage_handoff.md
cat reports/summary.json
```

## Docker CLI

```bash
docker compose run --rm soc-simulation
```

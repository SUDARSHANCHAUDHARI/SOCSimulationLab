# Production Readiness

## Current Status

This repository has a working defensive lab MVP with deterministic local analysis, generated reports, tests, and Docker demo support. It is portfolio-ready but not production complete yet.

## Required Before Public Release

- Add schema validation for scenario and collected-event files.
- Add automated tests for malformed scenario inputs.
- Validate all untrusted inputs.
- Add structured logging without leaking secrets.
- Document local setup and deployment.
- Review all sample data for sensitive content.
- Add authentication and authorization before handling multi-user or customer incident data.
- Run dependency and secret scans before release.
- Define retention rules for imported logs and reports.

## Definition of Done

- CI passes on pull requests.
- README has setup, usage, and security notes.
- Sample data is safe to publish.
- Error paths are handled clearly.
- No secrets or local machine paths are committed.
- Reports include timeline, gap analysis, triage handoff, and machine-readable summary.

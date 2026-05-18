# SOC Incident Timeline

## 1. 2026-05-18T12:00:01Z - reconnaissance activity

- Category: scan
- Severity: medium
- Source: 198.51.100.77
- MITRE tactic: Reconnaissance
- Evidence: `2026-05-18T12:00:01Z firewall scan src=198.51.100.77 dst=10.0.0.20 ports=22,80,443,8080`
- Recommended action: Validate firewall telemetry, enrich source reputation, and confirm scan volume thresholds.

## 2. 2026-05-18T12:02:30Z - suspicious authentication activity

- Category: login
- Severity: medium
- Source: 198.51.100.77
- MITRE tactic: Credential Access
- Evidence: `2026-05-18T12:02:30Z auth failed password user=admin src=198.51.100.77`
- Recommended action: Review failed-login source, target account, and brute-force thresholds.

## 3. 2026-05-18T12:03:01Z - suspicious authentication activity

- Category: login
- Severity: high
- Source: 198.51.100.77
- MITRE tactic: Credential Access
- Evidence: `2026-05-18T12:03:01Z auth accepted password user=admin src=198.51.100.77`
- Recommended action: Investigate successful authentication after failures and rotate credentials if unauthorized.

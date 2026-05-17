# SOC Incident Timeline

## 1. reconnaissance activity

- Category: scan
- Severity: medium
- Evidence: `2026-05-18T12:00:01Z firewall scan src=198.51.100.77 dst=10.0.0.20 ports=22,80,443,8080`

## 2. suspicious authentication activity

- Category: login
- Severity: medium
- Evidence: `2026-05-18T12:02:30Z auth failed password user=admin src=198.51.100.77`

## 3. suspicious authentication activity

- Category: login
- Severity: high
- Evidence: `2026-05-18T12:03:01Z auth accepted password user=admin src=198.51.100.77`

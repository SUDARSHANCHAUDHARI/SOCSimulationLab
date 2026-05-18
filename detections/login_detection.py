"""Detect suspicious login signals in collected SOC logs."""

from __future__ import annotations

from detections.types import Detection


def _field(line: str, key: str) -> str:
    prefix = f"{key}="
    for part in line.split():
        if part.startswith(prefix):
            return part.split("=", 1)[1]
    return "unknown"


def detect(lines: list[str]) -> list[Detection]:
    detections: list[Detection] = []
    for line in lines:
        lower = line.lower()
        if "failed password" in lower or "accepted password" in lower or "brute" in lower:
            severity = "high" if "accepted password" in lower else "medium"
            action = (
                "Investigate successful authentication after failures and rotate credentials if unauthorized."
                if severity == "high"
                else "Review failed-login source, target account, and brute-force thresholds."
            )
            detections.append(
                Detection(
                    "login",
                    "suspicious authentication activity",
                    line,
                    severity,
                    line.split()[0],
                    _field(line, "src"),
                    "Credential Access",
                    action,
                )
            )
    return detections

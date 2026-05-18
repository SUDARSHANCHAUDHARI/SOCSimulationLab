"""Detect reconnaissance signals in collected SOC logs."""

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
        if "nmap" in lower or "ports=" in lower or "scan" in lower:
            detections.append(
                Detection(
                    "scan",
                    "reconnaissance activity",
                    line,
                    "medium",
                    line.split()[0],
                    _field(line, "src"),
                    "Reconnaissance",
                    "Validate firewall telemetry, enrich source reputation, and confirm scan volume thresholds.",
                )
            )
    return detections

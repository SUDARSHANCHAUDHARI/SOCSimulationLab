"""Detect suspicious login signals in collected SOC logs."""

from __future__ import annotations

from detections.types import Detection


def detect(lines: list[str]) -> list[Detection]:
    detections: list[Detection] = []
    for line in lines:
        lower = line.lower()
        if "failed password" in lower or "accepted password" in lower or "brute" in lower:
            severity = "high" if "accepted password" in lower else "medium"
            detections.append(Detection("login", "suspicious authentication activity", line, severity))
    return detections

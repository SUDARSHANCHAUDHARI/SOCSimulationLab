"""Detect reconnaissance signals in collected SOC logs."""

from __future__ import annotations

from detections.types import Detection


def detect(lines: list[str]) -> list[Detection]:
    detections: list[Detection] = []
    for line in lines:
        lower = line.lower()
        if "nmap" in lower or "ports=" in lower or "scan" in lower:
            detections.append(Detection("scan", "reconnaissance activity", line, "medium"))
    return detections

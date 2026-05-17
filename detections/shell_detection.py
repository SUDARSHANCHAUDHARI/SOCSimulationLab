"""Detect shell and post-exploitation signals in collected SOC logs."""

from __future__ import annotations

from detections.types import Detection


def detect(lines: list[str]) -> list[Detection]:
    detections: list[Detection] = []
    for line in lines:
        lower = line.lower()
        if "reverse shell" in lower or "outbound shell" in lower or "bash -i" in lower:
            detections.append(Detection("shell", "possible interactive shell established", line, "high"))
    return detections

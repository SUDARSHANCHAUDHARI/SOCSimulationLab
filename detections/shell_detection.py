"""Detect shell and post-exploitation signals in collected SOC logs."""

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
        if "reverse shell" in lower or "outbound shell" in lower or "bash -i" in lower:
            detections.append(
                Detection(
                    "shell",
                    "possible interactive shell established",
                    line,
                    "high",
                    line.split()[0],
                    _field(line, "src"),
                    "Command and Control",
                    "Isolate the lab host, preserve network/process evidence, and confirm command execution telemetry.",
                )
            )
    return detections

"""Shared SOC detection types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Detection:
    category: str
    title: str
    evidence: str
    severity: str
    timestamp: str
    source: str
    mitre_tactic: str
    recommended_action: str

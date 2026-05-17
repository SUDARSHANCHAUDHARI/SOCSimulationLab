"""Shared SOC detection types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Detection:
    category: str
    title: str
    evidence: str
    severity: str

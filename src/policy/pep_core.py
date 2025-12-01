"""
Core types and base classes for F7-LAS Layer 5 Policy Enforcement Points (PEPs).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PolicyDecision:
    """Result of a Layer-5 policy evaluation."""
    allowed: bool
    reason: str = ""
    raw: Optional[Dict[str, Any]] = None

    @property
    def is_allowed(self) -> bool:
        return self.allowed


class BasePEP:
    """
    Abstract base class for a Policy Enforcement Point.

    Concrete implementations (OPA, Cedar, Sentinel, etc.) must implement
    `authorize()` and return a PolicyDecision.
    """

    def authorize(self, tool_call: Dict[str, Any], context: Dict[str, Any]) -> PolicyDecision:  # pragma: no cover - interface
        raise NotImplementedError

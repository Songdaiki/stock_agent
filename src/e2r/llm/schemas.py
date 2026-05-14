"""Schemas for the optional LLM research analyst."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping, Sequence

from e2r.models import Stage


@dataclass(frozen=True)
class LLMAnalystInput:
    """Point-in-time context sent to an LLM provider."""

    symbol: str
    company_name: str
    as_of_date: date
    deterministic_stage: Stage
    evidence_ids: Sequence[str] = field(default_factory=tuple)
    document_text: str | None = None
    parsed_fields: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids))
        object.__setattr__(self, "parsed_fields", dict(self.parsed_fields))


@dataclass(frozen=True)
class LLMAnalystOutput:
    """Structured LLM review that cannot override deterministic scoring."""

    confidence: float
    extracted_claims: tuple[str, ...] = field(default_factory=tuple)
    missing_information: tuple[str, ...] = field(default_factory=tuple)
    contradiction_flags: tuple[str, ...] = field(default_factory=tuple)
    suggested_queries: tuple[str, ...] = field(default_factory=tuple)
    evidence_ids_used: tuple[str, ...] = field(default_factory=tuple)
    hallucination_risk: float = 0.0
    insufficient_evidence: bool = False
    stage_explanation_ko: str | None = None
    attempted_stage_override: Stage | None = None

    def __post_init__(self) -> None:
        if self.confidence < 0 or self.confidence > 1:
            raise ValueError("confidence must be between 0 and 1")
        if self.hallucination_risk < 0 or self.hallucination_risk > 1:
            raise ValueError("hallucination_risk must be between 0 and 1")
        object.__setattr__(self, "extracted_claims", tuple(self.extracted_claims))
        object.__setattr__(self, "missing_information", tuple(self.missing_information))
        object.__setattr__(self, "contradiction_flags", tuple(self.contradiction_flags))
        object.__setattr__(self, "suggested_queries", tuple(self.suggested_queries))
        object.__setattr__(self, "evidence_ids_used", tuple(self.evidence_ids_used))
        if self.attempted_stage_override is not None and not isinstance(self.attempted_stage_override, Stage):
            object.__setattr__(self, "attempted_stage_override", Stage(self.attempted_stage_override))


__all__ = ["LLMAnalystInput", "LLMAnalystOutput"]

"""LLM provider abstraction with a deterministic fake provider for tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from e2r.llm.schemas import LLMAnalystInput, LLMAnalystOutput


class LLMProvider(Protocol):
    """Provider contract for optional LLM analysis."""

    def analyze(self, inputs: LLMAnalystInput) -> LLMAnalystOutput:
        """Return a structured evidence review."""


@dataclass
class FakeLLMProvider:
    """Deterministic provider used in tests and fixture runs."""

    output: LLMAnalystOutput | None = None
    calls: list[LLMAnalystInput] = field(default_factory=list)

    def analyze(self, inputs: LLMAnalystInput) -> LLMAnalystOutput:
        self.calls.append(inputs)
        if self.output is not None:
            return self.output
        suggested = (f"{inputs.company_name} 수주잔고 구조적 성장",)
        missing = tuple(key for key in ("contract_amount", "contract_duration_months", "RPO") if key not in inputs.parsed_fields)
        return LLMAnalystOutput(
            confidence=0.6,
            extracted_claims=(),
            missing_information=missing,
            contradiction_flags=(),
            suggested_queries=suggested,
            evidence_ids_used=tuple(inputs.evidence_ids),
            hallucination_risk=0.1,
            insufficient_evidence=not bool(inputs.evidence_ids),
            stage_explanation_ko=f"{inputs.deterministic_stage.value} 단계는 결정론 점수 결과이며 LLM은 설명만 제공합니다.",
        )


__all__ = ["FakeLLMProvider", "LLMProvider"]

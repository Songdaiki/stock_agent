"""Optional LLM research analyst that explains but never overrides stages."""

from __future__ import annotations

from dataclasses import replace

from e2r.llm.provider import LLMProvider
from e2r.llm.schemas import LLMAnalystInput, LLMAnalystOutput
from e2r.models import RedTeamFinding


DISALLOWED_RECOMMENDATION_TERMS = ("매수", "매도", "buy", "sell", "strong buy")


class LLMResearchAnalyst:
    """Review evidence with an LLM provider under deterministic guardrails."""

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    def analyze(self, inputs: LLMAnalystInput) -> LLMAnalystOutput:
        raw = self._provider.analyze(inputs)
        clean_explanation = _strip_recommendation_terms(raw.stage_explanation_ko)
        return replace(
            raw,
            stage_explanation_ko=clean_explanation,
            attempted_stage_override=None,
        )

    def contradiction_findings(self, inputs: LLMAnalystInput, output: LLMAnalystOutput) -> tuple[RedTeamFinding, ...]:
        findings: list[RedTeamFinding] = []
        for flag in output.contradiction_flags:
            findings.append(
                RedTeamFinding(
                    symbol=inputs.symbol,
                    as_of_date=inputs.as_of_date,
                    risk_type=f"llm_contradiction:{flag}",
                    severity=40.0,
                    is_hard_break=False,
                    description=f"LLM contradiction flag: {flag}",
                    evidence_ids=tuple(output.evidence_ids_used),
                )
            )
        return tuple(findings)


def _strip_recommendation_terms(value: str | None) -> str | None:
    if value is None:
        return None
    text = value
    for term in DISALLOWED_RECOMMENDATION_TERMS:
        text = text.replace(term, "[removed]")
    return text


__all__ = ["DISALLOWED_RECOMMENDATION_TERMS", "LLMResearchAnalyst"]

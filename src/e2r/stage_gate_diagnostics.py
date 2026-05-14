"""Diagnostic view of Stage 2 and Stage 3 gate failures.

This module mirrors the classifier thresholds without changing them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from e2r.models import ScoreSnapshot
from e2r.red_team import RedTeamAssessment, RedTeamRiskLevel
from e2r.staging import STAGE_3_GREEN_MIN_REVISION_SCORE


@dataclass(frozen=True)
class StageGateDiagnostics:
    """Threshold pass/fail details for score promotion autopsy."""

    stage2_gate_passed: bool
    stage3_green_gate_passed: bool
    failed_gate_names: tuple[str, ...]
    values_vs_thresholds: Mapping[str, Mapping[str, float | str | bool]]

    def failed(self, gate_name: str) -> bool:
        return gate_name in self.failed_gate_names


def diagnose_stage_gates(score: ScoreSnapshot, red_team: RedTeamAssessment) -> StageGateDiagnostics:
    """Return gate diagnostics using the current StageClassifier thresholds."""

    revision_score = _diagnostic(score, "revision_score")
    contract_quality = _diagnostic(score, "contract_quality", 100.0)
    one_off_shortage_risk = _diagnostic(score, "one_off_shortage_risk")

    checks: dict[str, tuple[float | str | bool, float | str | bool, bool]] = {
        "failed_stage2_total_score": (score.total_score, 65.0, score.total_score >= 65.0),
        "failed_stage2_eps_fcf": (score.eps_fcf_explosion_score, 10.0, score.eps_fcf_explosion_score >= 10.0),
        "failed_stage2_valuation": (score.valuation_rerating_score, 7.0, score.valuation_rerating_score >= 7.0),
        "failed_stage2_information_confidence": (
            score.information_confidence_score,
            3.0,
            score.information_confidence_score >= 3.0,
        ),
        "failed_stage3_total_score": (score.total_score, 85.0, score.total_score >= 85.0),
        "failed_stage3_eps_fcf": (score.eps_fcf_explosion_score, 17.0, score.eps_fcf_explosion_score >= 17.0),
        "failed_stage3_visibility": (
            score.earnings_visibility_score,
            15.0,
            score.earnings_visibility_score >= 15.0,
        ),
        "failed_stage3_bottleneck": (
            score.bottleneck_pricing_score,
            15.0,
            score.bottleneck_pricing_score >= 15.0,
        ),
        "failed_stage3_market_mispricing": (
            score.market_mispricing_score,
            10.0,
            score.market_mispricing_score >= 10.0,
        ),
        "failed_stage3_valuation": (
            score.valuation_rerating_score,
            10.0,
            score.valuation_rerating_score >= 10.0,
        ),
        "failed_stage3_revision": (
            revision_score,
            STAGE_3_GREEN_MIN_REVISION_SCORE,
            revision_score >= STAGE_3_GREEN_MIN_REVISION_SCORE,
        ),
        "failed_stage3_contract_quality": (contract_quality, 45.0, contract_quality >= 45.0),
        "failed_stage3_one_off_shortage_risk": (
            one_off_shortage_risk,
            70.0,
            one_off_shortage_risk < 70.0,
        ),
        "failed_stage3_red_team": (
            red_team.risk_level.value,
            RedTeamRiskLevel.LOW.value,
            red_team.risk_level == RedTeamRiskLevel.LOW,
        ),
    }
    checks["failed_stage2_red_team"] = (red_team.has_hard_break, False, not red_team.has_hard_break)

    failed = tuple(name for name, (_, _, passed) in checks.items() if not passed)
    stage2_names = {
        "failed_stage2_total_score",
        "failed_stage2_eps_fcf",
        "failed_stage2_valuation",
        "failed_stage2_information_confidence",
        "failed_stage2_red_team",
    }
    stage3_names = {
        "failed_stage3_total_score",
        "failed_stage3_eps_fcf",
        "failed_stage3_visibility",
        "failed_stage3_bottleneck",
        "failed_stage3_market_mispricing",
        "failed_stage3_valuation",
        "failed_stage3_revision",
        "failed_stage3_contract_quality",
        "failed_stage3_one_off_shortage_risk",
        "failed_stage3_red_team",
    }
    values = {
        name: {"value": value, "threshold": threshold, "passed": passed}
        for name, (value, threshold, passed) in checks.items()
    }
    return StageGateDiagnostics(
        stage2_gate_passed=not any(name in failed for name in stage2_names),
        stage3_green_gate_passed=not any(name in failed for name in stage3_names),
        failed_gate_names=failed,
        values_vs_thresholds=values,
    )


def _diagnostic(score: ScoreSnapshot, key: str, default: float = 0.0) -> float:
    value = score.diagnostic_scores.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


__all__ = ["StageGateDiagnostics", "diagnose_stage_gates"]

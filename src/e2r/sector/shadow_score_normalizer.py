"""Shadow-only score profile normalizer for case-library calibration.

This module reads v0.5 score-weight profiles and case records to produce a
research report. It does not call or modify production FeatureEngineering or
StageClassifier code.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.case_library import E2RCaseRecord, load_case_library


SCORE_DIMENSIONS = (
    "eps_fcf",
    "structural_visibility",
    "bottleneck_pricing",
    "market_mispricing",
    "valuation_rerating",
    "capital_allocation",
    "information_confidence",
)


@dataclass(frozen=True)
class ScoreWeightProfileV05:
    name: str
    dimensions: Mapping[str, float]
    risk_penalty: str
    green_policy: str

    def validate(self) -> None:
        missing = [key for key in SCORE_DIMENSIONS if key not in self.dimensions]
        if missing:
            raise ValueError(f"profile {self.name} missing dimensions: {missing}")
        if self.green_policy not in {
            "green_allowed",
            "watch_to_green",
            "watch_only",
            "red_watch",
            "event_only",
            "red_flag",
        }:
            raise ValueError(f"profile {self.name} has invalid green_policy: {self.green_policy}")

    @property
    def total_points(self) -> float:
        return sum(float(self.dimensions[key]) for key in SCORE_DIMENSIONS)

    @property
    def allows_shadow_green(self) -> bool:
        return self.green_policy in {"green_allowed", "watch_to_green"}


@dataclass(frozen=True)
class ShadowScoreResult:
    case_id: str
    primary_archetype: str
    profile_name: str
    total_profile_points: float
    price_validation_status: str
    shadow_status: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "primary_archetype": self.primary_archetype,
            "profile_name": self.profile_name,
            "total_profile_points": f"{self.total_profile_points:g}",
            "price_validation_status": self.price_validation_status,
            "shadow_status": self.shadow_status,
            "reason": self.reason,
        }


def load_score_weight_profiles(path: str | Path) -> dict[str, ScoreWeightProfileV05]:
    """Load a small YAML-like score profile file without requiring PyYAML."""

    profiles: dict[str, dict[str, str]] = {}
    current: str | None = None
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current = line[:-1].strip()
            profiles[current] = {}
            continue
        if current and ":" in line:
            key, value = line.split(":", 1)
            profiles[current][key.strip()] = value.strip().strip('"')
    parsed: dict[str, ScoreWeightProfileV05] = {}
    for name, values in profiles.items():
        dimensions = {key: float(values[key]) for key in SCORE_DIMENSIONS if key in values}
        profile = ScoreWeightProfileV05(
            name=name,
            dimensions=dimensions,
            risk_penalty=values.get("risk_penalty", "unknown"),
            green_policy=values.get("green_policy", "watch_only"),
        )
        profile.validate()
        parsed[name] = profile
    return parsed


def shadow_normalize_cases(
    records: Iterable[E2RCaseRecord],
    profiles: Mapping[str, ScoreWeightProfileV05],
) -> tuple[ShadowScoreResult, ...]:
    results: list[ShadowScoreResult] = []
    for record in records:
        profile = profiles.get(record.primary_archetype.value)
        if profile is None:
            profile = profiles.get("GENERIC_UNCLASSIFIED")
        if profile is None:
            results.append(
                ShadowScoreResult(
                    case_id=record.case_id,
                    primary_archetype=record.primary_archetype.value,
                    profile_name="",
                    total_profile_points=0.0,
                    price_validation_status=record.price_validation.price_validation_status,
                    shadow_status="missing_profile",
                    reason="no score profile exists for this archetype",
                )
            )
            continue
        if not profile.allows_shadow_green:
            status = "green_restricted_by_profile"
            reason = f"profile green_policy={profile.green_policy}"
        elif record.price_validation.price_validation_status != "price_filled":
            status = "insufficient_validation"
            reason = "price path is missing; do not claim score-price alignment"
        elif record.score_price_alignment in {"aligned", "unknown"}:
            status = "shadow_profile_ready_for_review"
            reason = "profile exists and price validation is present"
        else:
            status = "score_price_mismatch_review"
            reason = f"score_price_alignment={record.score_price_alignment}"
        results.append(
            ShadowScoreResult(
                case_id=record.case_id,
                primary_archetype=record.primary_archetype.value,
                profile_name=profile.name,
                total_profile_points=profile.total_points,
                price_validation_status=record.price_validation.price_validation_status,
                shadow_status=status,
                reason=reason,
            )
        )
    return tuple(results)


def render_shadow_score_profile_report(results: Iterable[ShadowScoreResult]) -> str:
    result_tuple = tuple(results)
    counts: dict[str, int] = {}
    for result in result_tuple:
        counts[result.shadow_status] = counts.get(result.shadow_status, 0) + 1
    lines = [
        "# Shadow Score Profile Report v0.5",
        "",
        "- production_scoring_changed: false",
        "- stageclassifier_changed: false",
        f"- case_count: {len(result_tuple)}",
        "",
        "## Status Distribution",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Case Results", "", "| case_id | archetype | profile | status | reason |", "|---|---|---|---|---|"])
    for result in result_tuple:
        lines.append(
            f"| {result.case_id} | {result.primary_archetype} | {result.profile_name} | "
            f"{result.shadow_status} | {result.reason} |"
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Shadow profiles do not affect production scoring.",
            "- Missing price validation remains insufficient_validation.",
            "- red_flag/event_only/red_watch profiles cannot create Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def run_shadow_score_normalizer(
    *,
    cases_path: str | Path,
    profiles_path: str | Path,
    output_path: str | Path,
) -> Path:
    records = load_case_library(cases_path)
    profiles = load_score_weight_profiles(profiles_path)
    results = shadow_normalize_cases(records, profiles)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_shadow_score_profile_report(results), encoding="utf-8")
    return target


__all__ = [
    "SCORE_DIMENSIONS",
    "ScoreWeightProfileV05",
    "ShadowScoreResult",
    "load_score_weight_profiles",
    "render_shadow_score_profile_report",
    "run_shadow_score_normalizer",
    "shadow_normalize_cases",
]

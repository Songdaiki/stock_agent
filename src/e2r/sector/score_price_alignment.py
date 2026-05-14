"""Score-to-price alignment evaluation for case-library records."""

from __future__ import annotations

from dataclasses import dataclass, replace

from e2r.sector.case_library import E2RCaseRecord


@dataclass(frozen=True)
class ScorePriceAlignmentResult:
    case_id: str
    score_price_alignment: str
    rerating_result: str
    reason: str


def evaluate_score_price_alignment(record: E2RCaseRecord) -> ScorePriceAlignmentResult:
    """Evaluate whether a case's evidence type and price path agree."""

    validation = record.price_validation
    case_type = record.case_type
    if record.stage4c_date and (record.stage3_date or record.stage2_date) and case_type != "structural_success":
        return ScorePriceAlignmentResult(record.case_id, "false_positive_score", "thesis_break", "stage4c_after_candidate_signal")

    if case_type == "event_premium":
        return ScorePriceAlignmentResult(record.case_id, "aligned", "event_premium", "event premium is not structural rerating")
    if case_type == "one_off":
        return ScorePriceAlignmentResult(record.case_id, "aligned", "no_rerating", "one-off demand should not be treated as true rerating")
    if case_type == "overheat":
        return ScorePriceAlignmentResult(record.case_id, "false_positive_score", "theme_overheat", "overheat should remain Green-restricted")
    if case_type == "cyclical_success":
        return ScorePriceAlignmentResult(record.case_id, "aligned", "cyclical_rerating", "cyclical move is not structural rerating")
    if case_type == "4c_thesis_break":
        return ScorePriceAlignmentResult(record.case_id, "false_positive_score", "thesis_break", "hard thesis break case")

    if case_type in {"structural_success", "success_candidate"}:
        if validation.price_validation_status != "price_filled" or validation.mfe_180d is None:
            return ScorePriceAlignmentResult(record.case_id, "unknown", record.rerating_result or "unknown", "missing price validation")
        has_eps_or_fcf = any(
            key.lower() in {"eps", "fy1_eps", "fy2_eps", "fcf", "op", "fy1_op", "fy2_op", "operating_profit"}
            or "eps" in key.lower()
            or "fcf" in key.lower()
            or "op" in key.lower()
            for key in (*record.must_have_fields, *record.key_evidence_fields)
        )
        if validation.mfe_180d >= 50 and not has_eps_or_fcf:
            return ScorePriceAlignmentResult(record.case_id, "price_moved_without_evidence", "unknown", "price moved without EPS/FCF evidence")
        if validation.mfe_180d < 20 and has_eps_or_fcf:
            return ScorePriceAlignmentResult(record.case_id, "evidence_good_but_price_failed", "no_rerating", "evidence did not translate into price rerating")
        return ScorePriceAlignmentResult(record.case_id, "aligned", "true_rerating", "structural evidence and price path align")

    return ScorePriceAlignmentResult(record.case_id, "unknown", "unknown", "unhandled case type")


def apply_score_price_alignment(record: E2RCaseRecord) -> E2RCaseRecord:
    result = evaluate_score_price_alignment(record)
    return replace(
        record,
        score_price_alignment=result.score_price_alignment,
        rerating_result=result.rerating_result,
    )


def align_case_records(records: tuple[E2RCaseRecord, ...]) -> tuple[E2RCaseRecord, ...]:
    return tuple(apply_score_price_alignment(record) for record in records)


__all__ = [
    "ScorePriceAlignmentResult",
    "align_case_records",
    "apply_score_price_alignment",
    "evaluate_score_price_alignment",
]

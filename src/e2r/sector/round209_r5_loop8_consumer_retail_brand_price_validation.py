"""Round-209 R5 Loop-8 consumer/retail/brand price validation pack.

Round 209 is calibration/evaluation material only. It captures reported price
anchors and event evidence from ``docs/round/round_209.md`` for K-food,
K-beauty, ODM, legacy brand, and M&A-optionality cases.

Simple example: a U.S. retail-channel discussion is useful Stage 2 attention.
It is not Stage 3-Green until sell-through, repeat purchase, OPM, inventory,
receivables, and price-path confirmation are visible as-of the case date.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import CaseDataQuality, E2RCaseRecord, PriceValidation, write_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector


ROUND209_SOURCE_ROUND_PATH = "docs/round/round_209.md"
ROUND209_LARGE_SECTOR = Round10LargeSector.CONSUMER_RETAIL_BRAND
ROUND209_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round209_r5_loop8_consumer_retail_brand_price_validation"
ROUND209_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r5_loop8_round209.jsonl"
ROUND209_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round209_r5_loop8_consumer_retail_brand_price_validation_audit.json"

ROUND209_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "EXPORT_RECURRING_CONSUMER": E2RArchetype.EXPORT_RECURRING_CONSUMER.value,
    "K_FOOD_GLOBAL_STAPLE_BRAND": E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND.value,
    "K_FOOD_SINGLE_SKU_RISK": E2RArchetype.K_FOOD_SINGLE_SKU_RISK.value,
    "K_BEAUTY_BRAND_US_CHANNEL": E2RArchetype.K_BEAUTY_BRAND_US_CHANNEL.value,
    "K_BEAUTY_EXPORT_DISTRIBUTION": E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION.value,
    "K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA": E2RArchetype.K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA.value,
    "K_BEAUTY_RETAIL_PLATFORM": E2RArchetype.K_BEAUTY_RETAIL_PLATFORM.value,
    "BEAUTY_DEVICE_EXPORT": E2RArchetype.BEAUTY_DEVICE_EXPORT.value,
    "APPAREL_FAST_FASHION_BRAND_OEM": E2RArchetype.APPAREL_FAST_FASHION_BRAND_OEM.value,
    "CHANNEL_STUFFING_INVENTORY_OVERLAY": E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY.value,
    "TARIFF_IMPORT_MARGIN_OVERLAY": E2RArchetype.TARIFF_IMPORT_MARGIN_OVERLAY.value,
    "EVENT_PREMIUM_GOVERNANCE_OVERLAY": E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "CHINA_CONSUMER_EXPOSURE_4C": E2RArchetype.CHINA_CONSUMER_EXPOSURE_4C.value,
    "BEAUTY_FAST_PRODUCT_CYCLE_RISK": E2RArchetype.BEAUTY_FAST_PRODUCT_CYCLE_RISK.value,
    "FOOD_SAFETY_RECALL_OVERLAY": E2RArchetype.FOOD_SAFETY_RECALL_OVERLAY.value,
}

ROUND209_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "repeat_purchase_evidence",
    "overseas_sales_mix_growth",
    "channel_sell_through_confirmed",
    "asp_or_product_mix_improvement",
    "opm_improvement",
    "inventory_and_receivables_stable",
    "tariff_recall_regulation_passed",
    "price_path_after_evidence",
)

ROUND209_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "viral_product_only",
    "brand_heat_only",
    "retail_talks_without_sell_through",
    "ipo_first_month_rally",
    "influencer_endorsement_only",
    "mna_optionality_without_eps",
    "private_affiliate_value_only",
    "china_decline_without_offset",
)

ROUND209_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "stage3_after_2x_to_4x_price_run",
    "ipo_first_month_double",
    "single_sku_or_single_device_dependence",
    "macro_kfood_kbeauty_reports_without_company_sellthrough",
    "us_retail_channel_expectation_before_sellthrough",
    "overseas_sales_good_but_opm_decelerating",
)

ROUND209_HARD_4C_GATES: tuple[str, ...] = (
    "food_safety_recall",
    "regulatory_ban",
    "channel_stuffing",
    "inventory_build",
    "receivables_spike",
    "single_product_fad_collapse",
    "us_tariff_margin_squeeze",
    "retail_channel_sellthrough_failure",
    "china_sales_collapse_not_offset_by_us_or_europe",
    "mna_event_failure_or_impairment",
    "brand_acquisition_impairment",
)

ROUND209_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "peak_price",
    "mfe_1d",
    "target_upside_pct",
    "reported_mfe_since_debut_pct",
    "market_cap_mfe_july_to_oct_pct",
    "implied_target_growth_pct",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round209ScoreAdjustment:
    axis: str
    points: int
    direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "axis": self.axis,
            "points": str(self.points),
            "direction": self.direction,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class Round209CaseCandidate:
    case_id: str
    symbol: str
    company_name: str
    primary_archetype: E2RArchetype
    secondary_archetypes: tuple[E2RArchetype, ...]
    case_type: str
    stage1_date: date | None
    stage2_date: date | None
    stage3_date: date | None
    stage4b_date: date | None
    stage4c_date: date | None
    stage3_decision: str
    stage4b_status: str
    hard_4c_confirmed: bool
    evidence_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    price_data_source: str
    reported_price_anchor: str
    reported_return_anchor: str
    mfe_1d: float | None
    stage2_price_anchor: float | None
    stage3_price_anchor: float | None
    stage4b_price_anchor: float | None
    peak_price_anchor: float | None
    extra_price_metrics: Mapping[str, float | str]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND209_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND209_SCORE_ADJUSTMENTS: tuple[Round209ScoreAdjustment, ...] = (
    Round209ScoreAdjustment("repeat_demand", 5, "raise", "R5는 유행보다 반복구매가 확인될 때 visibility가 올라간다."),
    Round209ScoreAdjustment("export_growth", 5, "raise", "해외 매출 성장과 수출 mix 증가는 내수 소비재 프레임 제거 근거다."),
    Round209ScoreAdjustment("asp_uplift", 4, "raise", "ASP나 product mix 개선이 OPM으로 내려오면 EPS/FCF 체급 변화 가능성이 높다."),
    Round209ScoreAdjustment("channel_sell_through", 5, "raise", "입점 논의가 아니라 실제 sell-through와 반복 발주가 필요하다."),
    Round209ScoreAdjustment("overseas_sales_mix", 5, "raise", "APR처럼 해외 비중이 높아지면 구조적 채널 전환 근거가 된다."),
    Round209ScoreAdjustment("us_sales_mix", 4, "raise", "미국 매출 비중은 K-food/K-beauty 프레임 전환의 핵심 보조축이다."),
    Round209ScoreAdjustment("opm_improvement", 5, "raise", "브랜드 열기가 OPM으로 내려와야 실제 이익 체급 변화다."),
    Round209ScoreAdjustment("inventory_quality", 4, "raise", "재고가 안정적이면 channel stuffing 위험이 낮아진다."),
    Round209ScoreAdjustment("receivables_quality", 4, "raise", "매출채권 품질은 성장의 현금화 여부를 확인한다."),
    Round209ScoreAdjustment("odm_customer_diversification", 4, "raise", "ODM은 고객 다변화와 주문 visibility가 핵심이다."),
    Round209ScoreAdjustment("viral_product_only", -5, "lower", "틱톡/viral만으로는 반복수요와 FCF를 증명하지 못한다."),
    Round209ScoreAdjustment("brand_heat_only", -5, "lower", "브랜드 열기만 있고 실적 품질이 없으면 Green 근거가 아니다."),
    Round209ScoreAdjustment("retail_talks_without_sell_through", -4, "lower", "Costco/Ulta/Target 논의는 Stage 2 attention이지 Green 근거가 아니다."),
    Round209ScoreAdjustment("ipo_first_month_rally", -5, "lower", "상장 직후 주가 2배는 4B-watch이지 구조 증거가 아니다."),
    Round209ScoreAdjustment("influencer_endorsement_only", -4, "lower", "인플루언서 endorsement만으로 반복구매와 OPM을 만들지 않는다."),
    Round209ScoreAdjustment("single_sku_dependence", -4, "lower", "단일 제품 의존도는 fad normalization과 recall 리스크를 키운다."),
    Round209ScoreAdjustment("china_exposure_without_offset", -4, "lower", "중국 둔화를 미국/유럽 성장으로 상쇄하지 못하면 Green을 제한한다."),
    Round209ScoreAdjustment("mna_optionality_without_eps", -4, "lower", "TaylorMade 같은 M&A optionality는 본업 EPS/FCF 증거와 분리한다."),
    Round209ScoreAdjustment("tariff_margin_uncertainty", -3, "lower", "관세 부담을 판가에 전가하지 못하면 OPM 품질이 낮아진다."),
    Round209ScoreAdjustment("inventory_or_receivables_build", -5, "lower", "재고/채권 증가는 channel stuffing과 현금화 리스크다."),
)


ROUND209_CASE_CANDIDATES: tuple[Round209CaseCandidate, ...] = (
    Round209CaseCandidate(
        case_id="r5_loop8_samyang_buldak_export_aligned",
        symbol="003230",
        company_name="삼양식품",
        primary_archetype=E2RArchetype.EXPORT_RECURRING_CONSUMER,
        secondary_archetypes=(
            E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND,
            E2RArchetype.K_FOOD_SINGLE_SKU_RISK,
            E2RArchetype.FOOD_SAFETY_RECALL_OVERLAY,
        ),
        case_type="structural_success",
        stage1_date=date(2023, 1, 1),
        stage2_date=date(2024, 6, 14),
        stage3_date=date(2024, 6, 14),
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="export_asp_op_revision_and_capacity_support_make_stage3_candidate_but_single_sku_and_recall_risk_stay_on_watch",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("buldak_export_growth", "us_europe_shipments", "asp_uplift", "q2_op_estimate_yoy_plus_84pct", "target_price_upgrade", "capacity_expansion"),
        red_flag_fields=("single_sku_dependence", "viral_product_normalization_risk", "recall_regulation_watch", "full_ohlc_unavailable"),
        price_data_source="MarketWatch reported close/target anchor",
        reported_price_anchor="647,000 KRW close; target price 830,000 KRW; implied prior close 611,921 KRW",
        reported_return_anchor="+5.7% event-day return; target upside +28.3%",
        mfe_1d=5.7,
        stage2_price_anchor=647000.0,
        stage3_price_anchor=647000.0,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"implied_prior_close": 611921.0, "target_price": 830000.0, "target_upside_pct": 28.3, "q2_op_estimate_yoy_pct": 84.0},
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Buldak export, ASP uplift, OP revision, and capacity support make this an R5 Stage 3 candidate; single-SKU and recall risk remain 4B/4C watch items.",
    ),
    Round209CaseCandidate(
        case_id="r5_loop8_nongshim_shin_global_staple",
        symbol="004370",
        company_name="농심",
        primary_archetype=E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND,
        secondary_archetypes=(E2RArchetype.EXPORT_RECURRING_CONSUMER, E2RArchetype.K_FOOD_SINGLE_SKU_RISK),
        case_type="success_candidate",
        stage1_date=date(2023, 1, 1),
        stage2_date=date(2024, 5, 27),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="global_staple_structure_is_stage2_until_opm_eps_revision_asp_and_channel_sellthrough_confirm",
        stage4b_status="none",
        hard_4c_confirmed=False,
        evidence_fields=("shin_ramyun_record_sales", "overseas_sales_nearly_60pct", "north_america_sales_growth_10pct", "us_sales_target_2030"),
        red_flag_fields=("opm_eps_revision_unverified", "channel_sellthrough_unverified", "china_or_cost_pressure_watch"),
        price_data_source="FT business evidence anchor",
        reported_price_anchor="stock OHLC unavailable",
        reported_return_anchor="Shin Ramyun 2023 sales $883M; North America sales $538M; U.S. sales target $1.5B by 2030",
        mfe_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"shin_ramyun_2023_sales_usd_mn": 883.0, "overseas_sales_share_pct": 60.0, "north_america_sales_2023_usd_mn": 538.0, "us_sales_target_2030_usd_mn": 1500.0, "implied_us_target_growth_pct": 178.8},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Shin Ramyun global staple quality is strong, but Stage 3 waits for OPM/EPS revision, ASP, and channel sell-through evidence.",
    ),
    Round209CaseCandidate(
        case_id="r5_loop8_apr_medicube_device_4b",
        symbol="278470",
        company_name="APR",
        primary_archetype=E2RArchetype.BEAUTY_DEVICE_EXPORT,
        secondary_archetypes=(
            E2RArchetype.K_BEAUTY_BRAND_US_CHANNEL,
            E2RArchetype.TARIFF_IMPORT_MARGIN_OVERLAY,
            E2RArchetype.BEAUTY_FAST_PRODUCT_CYCLE_RISK,
        ),
        case_type="structural_success",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 7, 8),
        stage3_date=date(2025, 10, 20),
        stage4b_date=date(2025, 10, 20),
        stage4c_date=None,
        stage3_decision="overseas_mix_us_mix_and_revenue_growth_support_stage3_candidate_while_fourfold_rally_requires_4b_watch",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("medicube_beauty_device", "overseas_revenue_nearly_80pct", "us_revenue_nearly_30pct", "q4_2025_sales_yoy_plus_124pct", "overseas_sales_yoy_plus_203pct"),
        red_flag_fields=("fourfold_rally_since_january", "valuation_crowding", "tariff_margin_squeeze_watch", "competition_and_device_cycle_fade"),
        price_data_source="Business Insider/FT/Vogue reported anchors",
        reported_price_anchor="158,300 KRW on 2025-07-08; market cap $4.2B in July; market cap about $6.0B in October",
        reported_return_anchor="IPO 이후 >75%; market cap +42.9% July-to-October; stock more than fourfold since January",
        mfe_1d=None,
        stage2_price_anchor=158300.0,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"implied_ipo_reference_price_max": 90457.0, "ipo_to_stage2_mfe_min_pct": 75.0, "market_cap_july_usd_bn": 4.2, "market_cap_oct_usd_bn": 6.0, "market_cap_mfe_july_to_oct_pct": 42.9, "reported_mfe_since_january_pct": 300.0, "overseas_sales_mix_pct": 80.0, "us_sales_mix_pct": 30.0},
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="reported_price_and_marketcap_anchor_not_full_ohlc",
        notes="APR is an R5 structural success candidate, but the fourfold rally means 4B-watch should travel with the Stage 3 evidence.",
    ),
    Round209CaseCandidate(
        case_id="r5_loop8_dalba_global_ipo_overheat",
        symbol="483650",
        company_name="d'Alba Global",
        primary_archetype=E2RArchetype.K_BEAUTY_BRAND_US_CHANNEL,
        secondary_archetypes=(
            E2RArchetype.PRICE_ONLY_RALLY,
            E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
            E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY,
        ),
        case_type="overheat",
        stage1_date=date(2025, 6, 5),
        stage2_date=date(2025, 6, 5),
        stage3_date=None,
        stage4b_date=date(2025, 6, 5),
        stage4c_date=None,
        stage3_decision="retail_talks_and_ipo_double_are_stage2_or_4b_watch_until_actual_sellthrough_repeat_order_opm_and_inventory_quality",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("costco_ulta_target_retail_talks", "us_physical_channel_expectation", "kbeauty_brand_heat"),
        red_flag_fields=("retail_talks_without_sellthrough", "ipo_first_month_rally", "brand_heat_only", "sellthrough_unverified"),
        price_data_source="Reuters reported return anchor",
        reported_price_anchor="absolute price unavailable",
        reported_return_anchor="stock more than doubled within one month after listing",
        mfe_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"reported_mfe_since_debut_pct": 100.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="theme_overheat",
        stage_failure_type="false_yellow",
        price_validation_status="reported_return_anchor_not_full_ohlc",
        notes="Retail talks and first-month IPO rally are not sell-through; this belongs in 4B-watch/event-premium until repeat demand is proven.",
    ),
    Round209CaseCandidate(
        case_id="r5_loop8_cosmax_kolmar_odm_leverage",
        symbol="192820/161890",
        company_name="코스맥스/한국콜마",
        primary_archetype=E2RArchetype.K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA,
        secondary_archetypes=(
            E2RArchetype.BEAUTY_OEM_ODM_SUPPLYCHAIN,
            E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
            E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY,
        ),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 6, 5),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="odm_backbone_is_stage2_until_customer_diversification_order_visibility_opm_inventory_and_receivables_quality_confirm",
        stage4b_status="none",
        hard_4c_confirmed=False,
        evidence_fields=("fast_beauty_contract_manufacturing_backbone", "indie_kbeauty_us_entry", "korea_cosmetics_output_13bn_usd", "export_share_about_80pct"),
        red_flag_fields=("company_specific_order_visibility_unverified", "inventory_receivables_quality_unverified", "tariff_pass_through_watch"),
        price_data_source="Reuters business evidence anchor",
        reported_price_anchor="stock OHLC unavailable",
        reported_return_anchor="$13B Korea cosmetics output; about 80% export-driven",
        mfe_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"k_beauty_output_usd_bn": 13.0, "export_share_pct": 80.0},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="ODM leverage is real Stage 2 material, but Green needs customer diversification, OPM, and working-capital quality.",
    ),
    Round209CaseCandidate(
        case_id="r5_loop8_amorepacific_transition_watch",
        symbol="090430",
        company_name="아모레퍼시픽",
        primary_archetype=E2RArchetype.CHINA_CONSUMER_EXPOSURE_4C,
        secondary_archetypes=(E2RArchetype.K_BEAUTY_BRAND_US_CHANNEL, E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION),
        case_type="failed_rerating",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 6, 5),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="kbeauty_macro_tailwind_is_not_company_green_until_china_decline_offset_us_europe_sellthrough_opm_recovery_and_brand_mix_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("kbeauty_us_growth_macro", "cosrx_laneige_sulwhasoo_mix_transition"),
        red_flag_fields=("china_exports_decline", "cosrx_plateau", "competition_and_low_cost_substitutes", "company_level_opm_recovery_unverified"),
        price_data_source="Reuters business evidence anchor",
        reported_price_anchor="stock OHLC unavailable",
        reported_return_anchor="K-beauty U.S. macro tailwind but China decline and COSRX plateau risk",
        mfe_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="no_rerating",
        stage_failure_type="false_yellow",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="K-beauty macro tailwind and company-level rerating must be separated; China exposure and COSRX plateau keep this Watch/Yellow.",
    ),
    Round209CaseCandidate(
        case_id="r5_loop8_fnf_taylormade_event",
        symbol="383220",
        company_name="F&F",
        primary_archetype=E2RArchetype.APPAREL_FAST_FASHION_BRAND_OEM,
        secondary_archetypes=(E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY,),
        case_type="event_premium",
        stage1_date=date(2025, 7, 21),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="taylormade_mna_optionality_is_stage1_event_until_deal_closes_and_eps_accretion_or_brand_fcf_is_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("taylormade_acquisition_rofr_legal_event", "goldman_advisor", "possible_3_5bn_usd_valuation", "subordinated_equity_investment_358bn_krw"),
        red_flag_fields=("mna_optionality_without_eps", "legal_dispute", "brand_acquisition_impairment_risk", "core_apparel_business_evidence_missing"),
        price_data_source="Reuters deal evidence anchor",
        reported_price_anchor="stock OHLC unavailable",
        reported_return_anchor="TaylorMade possible value $3.5B; F&F subordinated equity investment 358.0B KRW; implied value share 7.4%",
        mfe_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"reported_taylormade_value_usd_bn": 3.5, "ff_subordinated_equity_investment_krw_bn": 358.0, "krw_equiv_value_trn": 4.856, "ff_investment_vs_possible_value_pct": 7.4},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="TaylorMade optionality is an event premium; Stage 3 needs confirmed EPS accretion or core brand FCF rerating evidence.",
    ),
)


def round209_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND209_CASE_CANDIDATES:
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market="KR",
            sector_raw=candidate.primary_archetype.value,
            primary_archetype=candidate.primary_archetype,
            secondary_archetypes=candidate.secondary_archetypes,
            expected_group=candidate.expected_group,
            large_sector=candidate.large_sector,
            case_type=candidate.case_type,
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage3_date=candidate.stage3_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                "Round209 R5 Loop-8 consumer/retail/brand price-path validation. "
                "Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(field for field in candidate.evidence_fields if "talk" in field or "event" in field or "macro" in field or "brand" in field),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "export" in field
                or "asp" in field
                or "op" in field
                or "overseas" in field
                or "us_" in field
                or "revenue" in field
                or "capacity" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "rally" in field
                or "ipo" in field
                or "valuation" in field
                or "single" in field
                or "brand_heat" in field
                or "mna" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "recall" in field
                or "regulation" in field
                or "inventory" in field
                or "receivables" in field
                or "china" in field
                or "tariff" in field
                or "impairment" in field
            ),
            must_have_fields=ROUND209_GREEN_REQUIRED_FIELDS,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"event_premium", "overheat", "failed_rerating", "4b_watch", "4c_thesis_break"}
                else None
            ),
            score_price_alignment=candidate.score_price_alignment,
            rerating_result=candidate.rerating_result,
            stage_failure_type=candidate.stage_failure_type,
            price_pattern=candidate.stage3_decision,
            score_weight_hint={
                "repeat_demand_delta": 5.0,
                "export_growth_delta": 5.0,
                "asp_uplift_delta": 4.0,
                "channel_sell_through_delta": 5.0,
                "overseas_sales_mix_delta": 5.0,
                "us_sales_mix_delta": 4.0,
                "opm_improvement_delta": 5.0,
                "inventory_quality_delta": 4.0,
                "receivables_quality_delta": 4.0,
                "odm_customer_diversification_delta": 4.0,
                "viral_product_only_delta": -5.0,
                "brand_heat_only_delta": -5.0,
                "retail_talks_without_sell_through_delta": -4.0,
                "ipo_first_month_rally_delta": -5.0,
                "influencer_endorsement_only_delta": -4.0,
                "single_sku_dependence_delta": -4.0,
                "china_exposure_without_offset_delta": -4.0,
                "mna_optionality_without_eps_delta": -4.0,
                "tariff_margin_uncertainty_delta": -3.0,
                "inventory_or_receivables_build_delta": -5.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_viral_ipo_retail_talks_influencer_mna_or_china_macro_as_green_alone",
                *ROUND209_GREEN_REQUIRED_FIELDS,
                *ROUND209_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4b_price=candidate.stage4b_price_anchor,
                peak_price=candidate.peak_price_anchor,
                mfe_30d=candidate.mfe_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=False,
                stage_dates_confidence=0.82 if candidate.stage3_date else 0.7,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round209_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND209_CASE_CANDIDATES:
        rows.append(
            {
                "case_id": candidate.case_id,
                "symbol": candidate.symbol,
                "company_name": candidate.company_name,
                "primary_archetype": candidate.primary_archetype.value,
                "secondary_archetypes": "|".join(item.value for item in candidate.secondary_archetypes),
                "case_type": candidate.case_type,
                "stage1_date": _date_text(candidate.stage1_date),
                "stage2_date": _date_text(candidate.stage2_date),
                "stage3_date": _date_text(candidate.stage3_date),
                "stage4b_date": _date_text(candidate.stage4b_date),
                "stage4c_date": _date_text(candidate.stage4c_date),
                "stage3_decision": candidate.stage3_decision,
                "stage4b_status": candidate.stage4b_status,
                "hard_4c_confirmed": str(candidate.hard_4c_confirmed).lower(),
                "price_data_source": candidate.price_data_source,
                "reported_price_anchor": candidate.reported_price_anchor,
                "reported_return_anchor": candidate.reported_return_anchor,
                "mfe_1d": _float_text(candidate.mfe_1d),
                "stage2_price": _float_text(candidate.stage2_price_anchor),
                "stage3_price": _float_text(candidate.stage3_price_anchor),
                "extra_price_metrics": json.dumps(candidate.extra_price_metrics, ensure_ascii=False, sort_keys=True),
                "score_price_alignment": candidate.score_price_alignment,
                "rerating_result": candidate.rerating_result,
                "stage_failure_type": candidate.stage_failure_type,
                "price_validation_status": candidate.price_validation_status,
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round209_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND209_SCORE_ADJUSTMENTS)


def round209_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round209_price_validation": "true"} for field in ROUND209_PRICE_VALIDATION_FIELDS)


def round209_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round209_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND209_REQUIRED_TARGET_ALIASES.items()
    )


def round209_summary() -> dict[str, int | bool | str]:
    cases = ROUND209_CASE_CANDIDATES
    return {
        "source_round": ROUND209_SOURCE_ROUND_PATH,
        "large_sector": ROUND209_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "overheat_count": sum(1 for case in cases if case.case_type == "overheat"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND209_REQUIRED_TARGET_ALIASES),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round209_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND209_SOURCE_ROUND_PATH,
        "large_sector": ROUND209_LARGE_SECTOR.value,
        "summary": round209_summary(),
        "target_aliases": dict(ROUND209_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND209_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND209_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND209_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND209_HARD_4C_GATES),
        "what_not_to_change": [
            "do_not_use_round209_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_viral_ipo_retail_talks_influencer_or_mna_optionality_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round209_summary_markdown() -> str:
    summary = round209_summary()
    lines = [
        "# Round 209 R5 Loop 8 Consumer Retail Brand Price Validation",
        "",
        "This pack is calibration-only. Production scoring and candidate generation are unchanged.",
        "",
        "## Summary",
        "",
        f"- source_round: {summary['source_round']}",
        f"- large_sector: {summary['large_sector']}",
        f"- cases: {summary['case_candidate_count']}",
        f"- structural_success: {summary['structural_success_count']}",
        f"- success_candidate: {summary['success_candidate_count']}",
        f"- overheat: {summary['overheat_count']}",
        f"- failed_rerating: {summary['failed_rerating_count']}",
        f"- event_premium: {summary['event_premium_count']}",
        f"- Stage 3 dated cases: {summary['stage3_case_count']}",
        f"- 4B-watch cases: {summary['stage4b_watch_count']}",
        f"- full_ohlc_complete: {str(summary['full_ohlc_complete']).lower()}",
        "",
        "## Case Matrix",
        "",
        "| case | company | type | stage2 | stage3 | 4B | alignment | note |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for case in ROUND209_CASE_CANDIDATES:
        lines.append(
            "| "
            + " | ".join(
                (
                    case.case_id,
                    case.company_name,
                    case.case_type,
                    _date_text(case.stage2_date),
                    _date_text(case.stage3_date),
                    _date_text(case.stage4b_date),
                    case.score_price_alignment,
                    case.notes,
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "- Samyang and APR are the strongest R5 structural candidates in this pack.",
            "- Nongshim and Cosmax/Kolmar are Stage 2 watch cases until company-level OPM/EPS and sell-through are confirmed.",
            "- d'Alba, Amorepacific, and F&F illustrate why brand heat, IPO rally, China macro, and M&A optionality must be separated from Green evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round209_green_gate_review_markdown() -> str:
    lines = [
        "# Round 209 R5 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND209_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND209_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `Costco/Ulta/Target talks` means Stage 2 attention.",
            "- `sell-through + repeat order + OPM + stable inventory/receivables` is the kind of bundle that can support Stage 3.",
            "- `IPO first-month double` is 4B-watch, not Green evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round209_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round 209 R5 4B/4C Review",
        "",
        "## 4B Watch Triggers",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND209_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND209_HARD_4C_GATES)
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND209_CASE_CANDIDATES:
        if case.stage4b_status == "watch" or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round209_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 209 R5 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND209_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round209_r5_loop8_reports(
    output_directory: str | Path = ROUND209_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND209_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND209_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)

    paths = {
        "cases": write_case_library(round209_case_records(), cases_path),
        "audit": _write_json(round209_audit_payload(), audit_path),
        "summary": output / "round209_r5_loop8_price_validation_summary.md",
        "case_matrix": output / "round209_r5_loop8_case_matrix.csv",
        "target_aliases": output / "round209_r5_loop8_target_aliases.csv",
        "score_adjustments": output / "round209_r5_loop8_score_adjustments.csv",
        "price_validation_fields": output / "round209_r5_loop8_price_validation_fields.csv",
        "green_gate_review": output / "round209_r5_loop8_green_gate_review.md",
        "price_validation_plan": output / "round209_r5_loop8_price_validation_plan.md",
        "stage4b_4c_review": output / "round209_r5_loop8_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round209_summary_markdown(), encoding="utf-8")
    _write_csv(round209_case_rows(), paths["case_matrix"])
    _write_csv(round209_target_alias_rows(), paths["target_aliases"])
    _write_csv(round209_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round209_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round209_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round209_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round209_stage4b_4c_review_markdown(), encoding="utf-8")
    return paths


def _write_json(payload: object, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def _write_csv(rows: Iterable[dict[str, str]], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = tuple(rows)
    if not rows:
        target.write_text("", encoding="utf-8")
        return target
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return target


def _date_text(value: date | None) -> str:
    return value.isoformat() if value else ""


def _float_text(value: float | None) -> str:
    return "" if value is None else f"{value:g}"

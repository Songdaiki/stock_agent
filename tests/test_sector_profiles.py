from datetime import date, datetime
import unittest

from e2r.features import DeterministicFeatureEngineer, FeatureEngineeringInput
from e2r.models import ConsensusRevision, ConsensusSnapshot, FinancialActual, PriceBar, ResearchReport, Stage
from e2r.red_team import RedTeamEngine
from e2r.sector_profiles import SectorProfile, infer_sector_profile, profile_name_from_diagnostic
from e2r.stage_gate_diagnostics import promotion_band
from e2r.staging import StageClassificationInput, StageClassifier


def _bar(day: int, low: float, high: float, close: float) -> PriceBar:
    as_of_date = date(2024, 5, day)
    return PriceBar(
        symbol="CASE",
        date=as_of_date,
        open=close,
        high=high,
        low=low,
        close=close,
        adj_close=close,
        volume=1000,
        trading_value=close * 1000,
        market_cap=1_000_000_000,
        source="test",
        as_of_date=as_of_date,
    )


def _rich_input(title: str, parsed_fields: dict) -> FeatureEngineeringInput:
    as_of_date = date(2024, 5, 16)
    return FeatureEngineeringInput(
        symbol="CASE",
        as_of_date=as_of_date,
        price_bars=(_bar(1, 80, 100, 90), _bar(16, 120, 150, 145)),
        financial_actuals=(
            FinancialActual(
                symbol="CASE",
                fiscal_year=2023,
                fiscal_quarter=4,
                period_end=date(2023, 12, 31),
                reported_at=datetime(2024, 2, 15, 8, 0),
                as_of_date=as_of_date,
                source="test",
                sales=1000,
                operating_profit=100,
                net_income=80,
                eps=100,
                fcf=80,
            ),
        ),
        consensus=(
            ConsensusSnapshot(
                symbol="CASE",
                date=as_of_date,
                fiscal_year=2024,
                as_of_date=as_of_date,
                source="test",
                sales_e=1700,
                op_e=420,
                eps_e=420,
                per_e=12,
                pbr_e=2,
                analyst_count=4,
            ),
        ),
        consensus_revisions=(
            ConsensusRevision(
                symbol="CASE",
                date=as_of_date,
                fiscal_year=2024,
                as_of_date=as_of_date,
                eps_revision_1m=35,
                op_revision_1m=35,
                target_price_revision_1m=40,
            ),
        ),
        research_reports=(
            ResearchReport(
                symbol="CASE",
                publish_date=as_of_date,
                broker="Test",
                title=title,
                as_of_date=as_of_date,
                target_revision_pct=40,
                fy1_op=420,
                fy1_eps=420,
                fy2_op=570,
                fy2_eps=560,
                est_per=12,
                parsed_fields=parsed_fields,
                raw_text=title,
            ),
        ),
    )


class SectorProfileTests(unittest.TestCase):
    def test_profile_inference_from_keywords(self):
        self.assertEqual(infer_sector_profile(text="초고압 변압기 리드타임 장기화"), SectorProfile.POWER_EQUIPMENT)
        self.assertEqual(infer_sector_profile(text="방산 K9 폴란드 정부 고객"), SectorProfile.DEFENSE)
        self.assertEqual(infer_sector_profile(text="불닭 수출 비중 확대"), SectorProfile.K_FOOD_EXPORT)
        self.assertEqual(infer_sector_profile(text="실리콘투 K-뷰티 해외 채널 확장"), SectorProfile.K_BEAUTY_EXPORT)
        self.assertEqual(infer_sector_profile(text="HBM 수요 증가 메모리 가격 상승"), SectorProfile.MEMORY_HBM)

    def test_k_food_visibility_does_not_require_contract_quality(self):
        result = DeterministicFeatureEngineer().engineer(
            _rich_input(
                "삼양식품 불닭 수출 비중 확대 해외 채널 확장 ASP 상승",
                {
                    "export_ratio": 78,
                    "export_channel_expansion": True,
                    "overseas_channel_expansion": True,
                    "recurring_consumer_demand": True,
                    "high_margin_mix_improvement": True,
                    "pricing_power_mentioned": True,
                    "opm_expansion_pctp": 8,
                    "target_revision_pct": 40,
                },
            )
        )
        score = result.score()

        self.assertEqual(profile_name_from_diagnostic(score.diagnostic_scores["sector_profile_id"]), "K_FOOD_EXPORT")
        self.assertLess(score.diagnostic_scores["contract_quality"], 45)
        self.assertGreaterEqual(score.diagnostic_scores["structural_visibility_quality"], 45)

    def test_memory_hbm_evidence_improves_visibility_without_generic_contract(self):
        result = DeterministicFeatureEngineer().engineer(
            _rich_input(
                "삼성전자 메모리 HBM 수요 증가 메모리 가격 상승 공급조절",
                {
                    "hbm_demand_mentioned": True,
                    "memory_price_increase_mentioned": True,
                    "supply_discipline_mentioned": True,
                    "pricing_power_mentioned": True,
                    "target_revision_pct": 35,
                },
            )
        )
        score = result.score()

        self.assertEqual(profile_name_from_diagnostic(score.diagnostic_scores["sector_profile_id"]), "MEMORY_HBM")
        self.assertLess(score.diagnostic_scores["contract_quality"], 45)
        self.assertGreater(score.diagnostic_scores["sector_visibility_score"], 35)

    def test_qualitative_evidence_is_bounded_and_cannot_create_green_alone(self):
        as_of_date = date(2024, 5, 16)
        feature_input = FeatureEngineeringInput(
            symbol="CASE",
            as_of_date=as_of_date,
            research_reports=(
                ResearchReport(
                    symbol="CASE",
                    publish_date=as_of_date,
                    broker="Test",
                    title="삼양식품 불닭 수출 비중 확대 해외 채널 확장 ASP 상승",
                    as_of_date=as_of_date,
                    parsed_fields={
                        "export_channel_expansion": True,
                        "overseas_channel_expansion": True,
                        "recurring_consumer_demand": True,
                        "pricing_power_mentioned": True,
                    },
                    raw_text="삼양식품 불닭 수출 비중 확대 해외 채널 확장 ASP 상승",
                ),
            ),
        )
        result = DeterministicFeatureEngineer().engineer(feature_input)
        score = result.score()
        stage = StageClassifier().classify(
            StageClassificationInput(score=score, red_team=RedTeamEngine().assess(result.red_team_signals))
        )

        self.assertGreater(score.diagnostic_scores["structural_visibility_quality"], 0)
        self.assertNotEqual(stage.stage, Stage.STAGE_3_GREEN)

    def test_promotion_band_is_diagnostic_only(self):
        result = DeterministicFeatureEngineer().engineer(
            _rich_input(
                "일진전기 초고압 전력기기 수주잔고 리드타임 장기화",
                {
                    "contract_duration_months": 12,
                    "contract_amount_to_prior_sales": 0.12,
                    "order_backlog_to_sales": 1.2,
                    "lead_time_extended": True,
                    "pricing_power_mentioned": True,
                    "target_revision_pct": 35,
                },
            )
        )
        score = result.score()
        stage = StageClassifier().classify(
            StageClassificationInput(score=score, red_team=RedTeamEngine().assess(result.red_team_signals))
        )

        self.assertIn(promotion_band(score, stage.stage), {"Stage 1", "Stage 2", "Stage 2-High", "Stage 3-Watch"})
        self.assertNotEqual(stage.stage.value, promotion_band(score, stage.stage))


if __name__ == "__main__":
    unittest.main()

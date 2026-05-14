from datetime import date
import unittest

from e2r.llm import FakeLLMProvider, LLMAnalystInput, LLMAnalystOutput, LLMResearchAnalyst
from e2r.models import Stage


class LLMResearchAnalystTests(unittest.TestCase):
    def test_fake_llm_extraction_can_add_suggested_query(self):
        provider = FakeLLMProvider()
        output = LLMResearchAnalyst(provider).analyze(
            LLMAnalystInput(
                symbol="267260",
                company_name="HD현대일렉트릭",
                as_of_date=date(2023, 7, 27),
                deterministic_stage=Stage.STAGE_3_GREEN,
                evidence_ids=("ev1",),
            )
        )

        self.assertTrue(output.suggested_queries)
        self.assertIn("ev1", output.evidence_ids_used)

    def test_llm_cannot_override_deterministic_stage(self):
        provider = FakeLLMProvider(
            LLMAnalystOutput(
                confidence=0.9,
                attempted_stage_override=Stage.STAGE_3_GREEN,
                stage_explanation_ko="LLM이 매수 의견으로 Green을 제안",
            )
        )
        output = LLMResearchAnalyst(provider).analyze(
            LLMAnalystInput(
                symbol="096530",
                company_name="씨젠",
                as_of_date=date(2020, 8, 24),
                deterministic_stage=Stage.STAGE_3_RED,
            )
        )

        self.assertIsNone(output.attempted_stage_override)
        self.assertNotIn("매수", output.stage_explanation_ko)

    def test_missing_evidence_remains_missing(self):
        output = LLMResearchAnalyst(FakeLLMProvider()).analyze(
            LLMAnalystInput(
                symbol="111111",
                company_name="한전변압기",
                as_of_date=date(2024, 5, 21),
                deterministic_stage=Stage.STAGE_1,
                parsed_fields={},
            )
        )

        self.assertTrue(output.insufficient_evidence)
        self.assertIn("contract_amount", output.missing_information)

    def test_llm_contradiction_flag_becomes_red_team_finding(self):
        analyst = LLMResearchAnalyst(
            FakeLLMProvider(
                LLMAnalystOutput(
                    confidence=0.8,
                    contradiction_flags=("contract_delay_conflict",),
                    evidence_ids_used=("ev-delay",),
                )
            )
        )
        inputs = LLMAnalystInput(
            symbol="103590",
            company_name="일진전기",
            as_of_date=date(2023, 11, 27),
            deterministic_stage=Stage.STAGE_3_GREEN,
            evidence_ids=("ev-delay",),
        )
        output = analyst.analyze(inputs)
        findings = analyst.contradiction_findings(inputs, output)

        self.assertEqual(findings[0].risk_type, "llm_contradiction:contract_delay_conflict")
        self.assertIn("ev-delay", findings[0].evidence_ids)


if __name__ == "__main__":
    unittest.main()

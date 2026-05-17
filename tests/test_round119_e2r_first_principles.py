import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round119_first_principles_report import build_parser
from e2r.sector.round119_e2r_first_principles import (
    ROUND119_FALSE_GREEN_PATTERNS,
    ROUND119_GREEN_GATES,
    ROUND119_LOOP7_FOCUS,
    ROUND119_PRINCIPLE_CHAIN,
    ROUND119_THEME_TAG_RULES,
    render_round119_green_gate_markdown,
    render_round119_summary_markdown,
    render_round119_theme_guardrail_markdown,
    round119_green_gate_rows,
    round119_loop7_focus_rows,
    round119_principle_rows,
    round119_summary,
    round119_theme_tag_rule_rows,
    write_round119_reports,
)


class Round119E2RFirstPrinciplesTests(unittest.TestCase):
    def test_principle_chain_preserves_e2r_order(self):
        self.assertEqual(
            [step.step_id for step in ROUND119_PRINCIPLE_CHAIN],
            [
                "industry_structure_change",
                "eps_fcf_bodyweight_change",
                "durability_lock",
                "old_frame_mispricing",
                "valuation_rerating",
                "price_path_validation",
                "redteam_4b_4c_survival",
            ],
        )

        rows = round119_principle_rows()
        self.assertEqual(rows[0]["failure_mode"], "good_theme_without_company_evidence")
        self.assertIn("fy1_fy2_revision", rows[1]["required_evidence"])
        self.assertIn("not_saturated_4b", rows[-1]["required_evidence"])

    def test_green_gates_block_theme_price_and_redteam_shortcuts(self):
        gate_ids = {gate.gate_id for gate in ROUND119_GREEN_GATES}

        self.assertEqual(len(gate_ids), 7)
        for gate_id in (
            "cross_evidence",
            "eps_fcf_durability",
            "structural_visibility",
            "old_frame_mispricing",
            "price_path_alignment",
            "no_hard_redteam",
            "not_saturated_4b",
        ):
            self.assertIn(gate_id, gate_ids)

        rows = {row["gate_id"]: row for row in round119_green_gate_rows()}
        self.assertEqual(rows["no_hard_redteam"]["stage_effect"], "hard_block_green")
        self.assertEqual(rows["not_saturated_4b"]["stage_effect"], "mark_4b_watch_or_elevated")
        self.assertIn("single news headline", rows["cross_evidence"]["example_fail"])

    def test_false_green_patterns_capture_round119_warnings(self):
        patterns = set(ROUND119_FALSE_GREEN_PATTERNS)

        self.assertIn("hot_theme_without_eps_fcf", patterns)
        self.assertIn("price_only_rally", patterns)
        self.assertIn("low_per_low_pbr_without_bodyweight_change", patterns)
        self.assertIn("event_premium_without_contract_budget_or_revenue", patterns)
        self.assertIn("hard_redteam_ignored", patterns)

    def test_loop7_focus_covers_r1_to_r13_domains(self):
        rows = {row["loop_id"]: row for row in round119_loop7_focus_rows()}

        self.assertEqual(len(rows), 13)
        self.assertIn("contract_quality", rows["R1"]["required_focus"])
        self.assertIn("hbm_lta", rows["R2"]["required_focus"])
        self.assertIn("repeat_demand", rows["R5"]["required_focus"])
        self.assertIn("roe", rows["R6"]["required_focus"])
        self.assertIn("affo_integrity_risk", rows["R10"]["green_blocker"])
        self.assertIn("4c", rows["R13"]["required_focus"])

    def test_theme_tag_rules_are_routing_not_score_evidence(self):
        rows = {row["rule_id"]: row for row in round119_theme_tag_rule_rows()}

        self.assertEqual(len(rows), len(ROUND119_THEME_TAG_RULES))
        self.assertIn("route", rows["theme_tag_is_routing_only"]["routing_use"].lower())
        self.assertIn("Do not give EPS/FCF", rows["theme_tag_is_routing_only"]["scoring_limit"])
        self.assertIn("document/detail parsing", rows["opendart_list_is_not_detail"]["required_upgrade"])
        self.assertIn("price-only", rows["price_needs_evidence"]["scoring_limit"])

    def test_summary_and_markdown_explain_no_production_change(self):
        summary = round119_summary()
        summary_md = render_round119_summary_markdown()
        gate_md = render_round119_green_gate_markdown()
        theme_md = render_round119_theme_guardrail_markdown()

        self.assertEqual(summary["principle_step_count"], 7)
        self.assertEqual(summary["green_gate_count"], 7)
        self.assertEqual(summary["loop7_focus_count"], 13)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["theme_tags_are_score_evidence"])
        self.assertIn("industry structure change -> EPS/FCF bodyweight change", summary_md)
        self.assertIn("Do not apply Round119 as production scoring", summary_md)
        self.assertIn("Stage 3-Green Gate Checklist", gate_md)
        self.assertIn("Raw theme tags route attention", theme_md)

    def test_report_writer_outputs_round119_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = write_round119_reports(
                output_directory=root / "out",
                principles_path=root / "data" / "principles.csv",
            )

            for path in paths.values():
                self.assertTrue(path.exists(), path)
            self.assertIn("production_scoring_changed", paths["summary_json"].read_text(encoding="utf-8"))
            self.assertIn("industry_structure_change", paths["principles"].read_text(encoding="utf-8"))
            self.assertIn("R13", paths["loop7_focus_map"].read_text(encoding="utf-8"))
            self.assertIn("price_only_rally", paths["false_green_patterns"].read_text(encoding="utf-8"))

    def test_cli_argument_parser_supports_paths(self):
        args = build_parser().parse_args(
            [
                "--output-directory",
                "tmp/out",
                "--principles",
                "tmp/principles.csv",
            ]
        )

        self.assertEqual(args.output_directory, "tmp/out")
        self.assertEqual(args.principles, "tmp/principles.csv")

    def test_production_scoring_modules_do_not_import_round119_pack(self):
        root = Path(__file__).resolve().parents[1]
        production_files = [
            root / "src" / "e2r" / "features.py",
            root / "src" / "e2r" / "scoring.py",
            root / "src" / "e2r" / "staging.py",
            root / "src" / "e2r" / "red_team.py",
            root / "src" / "e2r" / "pipeline" / "e2r_standard_flow.py",
        ]

        for path in production_files:
            self.assertNotIn("round119_e2r_first_principles", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

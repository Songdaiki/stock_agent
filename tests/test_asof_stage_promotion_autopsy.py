from datetime import date, datetime
from pathlib import Path
import json
import tempfile
import unittest

from e2r.backtest.asof_stage_promotion_autopsy import (
    AsOfStagePromotionAutopsy,
    AsOfStagePromotionAutopsyConfig,
)
from e2r.cli.analyze_asof_stage_promotion import build_parser, config_from_args
from e2r.research.report_snapshot_store import ReportSnapshotStore
from e2r.research.search_provider import SearchResult
from e2r.research.search_snapshot_store import SearchSnapshotStore, snapshot_from_search_result


class AsOfStagePromotionAutopsyTests(unittest.TestCase):
    def test_cli_parses_args(self):
        args = build_parser().parse_args(["--asof-output", "output/backtests/asof_research_replay/test"])
        config = config_from_args(args)

        self.assertEqual(str(config.asof_output), "output/backtests/asof_research_replay/test")
        self.assertEqual(config.top_candidates, 50)

    def test_autopsy_writes_gate_and_coverage_outputs(self):
        with tempfile.TemporaryDirectory() as root:
            paths = _paths(root)
            _write_asof_output(paths["asof"])
            _write_official(paths["official"])
            _write_search_and_report(paths["search"], paths["reports"])

            result = AsOfStagePromotionAutopsy().run(
                AsOfStagePromotionAutopsyConfig(
                    asof_output=paths["asof"],
                    output_directory=paths["output"],
                    official_root=paths["official"],
                    search_snapshot_root=paths["search"],
                    report_snapshot_root=paths["reports"],
                    report_date=date(2026, 5, 14),
                )
            )
            self.assertTrue(result.rows)
            self.assertTrue((paths["output"] / "2026-05-14_autopsy.md").exists())
            self.assertTrue((paths["output"] / "stage_gate_matrix.csv").exists())
            self.assertTrue((paths["output"] / "feature_input_coverage.csv").exists())
            self.assertIn("failed_stage3_bottleneck", (paths["output"] / "stage_gate_matrix.csv").read_text(encoding="utf-8"))


def _paths(root: str):
    base = Path(root)
    return {
        "asof": base / "asof",
        "official": base / "official",
        "search": base / "search",
        "reports": base / "reports",
        "output": base / "output",
    }


def _write_asof_output(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    candidates = [
        {
            "symbol": "111111",
            "company_name": "테스트",
            "as_of_date": "2023-08-01",
            "layer": "deep_research",
            "stage": "1",
            "rank": 1,
            "score": 30.0,
            "reason_codes": ["DISC_SUPPLY_CONTRACT"],
            "candidate_source_path": "official_cheap_scan",
        }
    ]
    recall = [
        {
            "label_id": "label-111111",
            "symbol": "111111",
            "company_name": "테스트",
            "expected_group": "structural",
            "appeared_in_candidates": True,
            "first_detected_date": "2023-08-01",
            "first_layer": "deep_research",
            "first_stage": "1",
            "detection_lag_days": 31,
            "evidence_types_seen": ["research_report"],
            "failure_stage": None,
        }
    ]
    (root / "discovered_candidates.json").write_text(json.dumps(candidates, ensure_ascii=False), encoding="utf-8")
    (root / "benchmark_recall_report.json").write_text(json.dumps(recall, ensure_ascii=False), encoding="utf-8")


def _write_official(root: Path) -> None:
    for name in ("universe", "prices", "disclosures", "financials", "risks"):
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "universe" / "universe.csv").write_text(
        "symbol,name,market,exchange,listed_date\n111111,테스트,KR,KRX,2020-01-01\n",
        encoding="utf-8",
    )
    (root / "prices" / "prices.csv").write_text(
        "symbol,date,open,high,low,close,adj_close,volume,trading_value,market_cap,source,as_of_date\n"
        "111111,2023-07-01,1000,1000,900,950,950,100,95000,100000000,historical,2023-07-01\n"
        "111111,2023-07-27,1300,1400,1200,1350,1350,1000,1350000,135000000,historical,2023-07-27\n",
        encoding="utf-8",
    )
    (root / "financials" / "financials.csv").write_text(
        "symbol,fiscal_year,fiscal_quarter,period_end,reported_at,as_of_date,source,sales,operating_profit,net_income,eps,fcf\n"
        "111111,2023,2,2023-06-30,2023-07-27T08:00:00,2023-07-27,historical,800,100,80,500,90\n",
        encoding="utf-8",
    )
    (root / "disclosures" / "disclosures.csv").write_text(
        "symbol,source,report_type,title,published_at,observed_at,available_at,as_of_date,rcept_no,raw_text\n"
        '111111,OpenDART,단일판매·공급계약체결,단일판매·공급계약체결,2023-07-27T08:00:00,2023-07-27T08:00:00,2023-07-27T08:00:00,2023-07-27,r1,'
        '"계약금액 100억원 매출액 대비 30% 계약기간 2023-07-27 ~ 2027-07-26 수주잔고 사상 최대 ASP 상승 리드타임 장기화 공급부족"\n',
        encoding="utf-8",
    )
    (root / "risks" / "risks.csv").write_text(
        "symbol,as_of_date,source,managed_issue,trading_halt,investment_warning,investor_caution,unfaithful_disclosure,delisting_risk,raw_text\n",
        encoding="utf-8",
    )


def _write_search_and_report(search_root: Path, report_root: Path) -> None:
    SearchSnapshotStore(search_root).save_snapshot(
        snapshot_from_search_result(
            SearchResult(
                title="테스트 수주잔고 OPM Review PDF",
                url="https://example.com/report.pdf",
                published_at=datetime(2023, 7, 27, 8, 0),
                is_pdf=True,
                is_report_domain=True,
                confidence=0.9,
            ),
            query="테스트 수주잔고 OPM 수출 비중 PDF",
            search_date=date(2026, 5, 14),
            symbol="111111",
            company_name="테스트",
        )
    )
    ReportSnapshotStore(report_root).save_text_snapshot(
        url="https://example.com/report.pdf",
        title="테스트 수주잔고 OPM Review PDF",
        text="2023.07.27\n현재주가: 10000\n목표주가: 15000\n목표주가 상향: 25%\nFY1 EPS: 1000\nFY2 EPS: 1800\n수주잔고/매출: 160%\nASP 상승 리드타임 장기화 구조적 공급부족",
        fetched_at=datetime(2026, 5, 14, 9, 0),
        as_of_date=date(2023, 8, 1),
        symbol="111111",
        company_name="테스트",
        source_type="broker_report",
    )


if __name__ == "__main__":
    unittest.main()

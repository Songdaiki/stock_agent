"""Run a tiny Korea API raw probe and schema summary."""

from __future__ import annotations

import argparse
from datetime import date
from typing import Sequence

from e2r.probe import APIProbeConfig, APIProbeRunner


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Probe approved Korea APIs and summarize raw response schemas.")
    parser.add_argument("--date", required=True, help="Probe date in YYYY-MM-DD format")
    parser.add_argument("--output-directory", default="output/api_probe", help="Output directory for raw/schema/probe logs")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--fixture", action="store_true", help="Use built-in fixture payloads without live HTTP")
    mode.add_argument("--live", action="store_true", help="Execute tiny live HTTP probes with credentials")
    parser.add_argument("--sample-symbol", default="005930", help="Sample stock code for symbol-specific APIs")
    parser.add_argument("--sample-company", default="삼성전자", help="Sample company name for operator context")
    parser.add_argument("--sample-query", default="삼성전자 수주잔고", help="Sample search query for Naver probes")
    parser.add_argument("--sample-market", default="KR", help="Sample market enum value")
    parser.add_argument("--skip-krx", action="store_true", help="Skip KRX Open API probes")
    parser.add_argument("--skip-data-go-kr", action="store_true", help="Skip data.go.kr probes")
    parser.add_argument("--skip-naver", action="store_true", help="Skip Naver Search probes")
    parser.add_argument("--skip-opendart", action="store_true", help="Skip OpenDART probe")
    parser.add_argument("--max-requests-per-source", type=int, default=3, help="Probe request safety cap")
    parser.add_argument("--timeout-seconds", type=int, default=10, help="HTTP timeout for live probe requests")
    parser.add_argument("--no-cache", action="store_true", help="Do not reuse existing raw response files")
    parser.add_argument("--no-save-raw", action="store_true", help="Skip raw response file storage and only write reports")
    return parser


def config_from_args(args: argparse.Namespace) -> APIProbeConfig:
    live_enabled = bool(args.live)
    fixture_mode = not live_enabled if not args.fixture else True
    return APIProbeConfig(
        as_of_date=date.fromisoformat(args.date),
        output_directory=args.output_directory,
        live_enabled=live_enabled,
        fixture_mode=fixture_mode,
        max_requests_per_source=args.max_requests_per_source,
        timeout_seconds=args.timeout_seconds,
        use_cache=not args.no_cache,
        sample_symbol=args.sample_symbol,
        sample_company=args.sample_company,
        sample_query=args.sample_query,
        sample_market=args.sample_market,
        probe_data_go_kr=not args.skip_data_go_kr,
        probe_krx=not args.skip_krx,
        probe_opendart=not args.skip_opendart,
        probe_naver=not args.skip_naver,
        save_raw=not args.no_save_raw,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    result = APIProbeRunner().run(config_from_args(args))
    print(f"api probe output: {result.output_directory}")
    print(f"schema summary: {result.schema_summary_md_path}")
    print(f"normalizer report: {result.normalizer_report_md_path}")
    print(f"run log: {result.run_log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["build_arg_parser", "config_from_args", "main"]

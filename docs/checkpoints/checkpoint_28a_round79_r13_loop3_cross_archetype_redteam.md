# Checkpoint 28A Round 79 - R13 Loop 3 Cross-Archetype RedTeam / 4B / Price Validation

Round 79 반영 완료.

## Scope

- source round: `docs/round/round_79.md`
- large sector: `CROSS_ARCHETYPE_REDTEAM_4B_PRICE_VALIDATION`
- loop: `R13 Loop 3 / v3.0`
- production scoring changed: `false`
- case records are candidate-generation input: `false`

이번 라운드는 새 섹터 점수표가 아니라 R1~R12 후보를 마지막으로 거르는 공통 검문소다.
쉬운 예로, AI 메모리처럼 구조가 맞아도 이미 시장이 새 프레임을 대부분 인정한 구간이면 4B-watch로 따로 감시하고, Supermicro처럼 감사인 사임이 나오면 이전 성장률과 무관하게 Green을 막는다.

## Targets

- target_count: 17
- green_possible_count: 1
- watch_yellow_first_count: 5
- redteam_first_count: 11
- hard_gate_target_count: 8

추가/강화된 핵심 타깃:

- `POLICY_MARKET_SHOCK_EVENT`: AI 초과이익세, 시민배당, 거래세/배당세 같은 정책 발언이 crowded trade의 price path를 흔드는 경우를 별도 overlay로 분리.
- `STABLECOIN_CONVERTIBILITY_RISK`: fiat-backed, algorithmic, STO/테마를 섞지 않고 준비금, 상환, de-peg, run risk를 hard gate로 분리.
- `SECTOR_SUCCESS_BUT_4B_WATCH`: 성공한 구조라도 valuation 포화, 모두가 인정한 새 프레임, 과밀 리포트가 있으면 fresh Green이 아니라 4B-watch로 분리.

## Case Pack

- case_candidate_count: 20
- structural_success_count: 1
- success_candidate_count: 3
- cyclical_success_count: 1
- event_premium_count: 1
- overheat_count: 1
- failed_rerating_count: 4
- stage4b_case_count: 4
- stage4c_case_count: 7

새로 반영한 대표 케이스:

- `circle_regulated_stablecoin_infra_4b_watch_case`
- `korea_ai_tax_policy_market_shock_case`

기존 R13 검증 케이스도 유지했다:

- `sk_hynix_hbm_memory_structural_4b_watch_case`
- `korea_buyback_cancellation_policy_to_execution_case`
- `event_to_contract_escalation_reference_case`
- `supermicro_accounting_trust_4c_case`
- `crowdstrike_operational_trust_break_case`
- `bluebird_bio_commercialization_failure_case`
- `novo_nordisk_glp1_4b_to_4c_case`
- `equinix_affo_cashflow_integrity_case`
- `terrausd_luna_algorithmic_stablecoin_break_case`

## Outputs

- `data/e2r_case_library/cases_r13_loop3_round79.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round79_r13_loop3_v3.csv`
- `output/e2r_round79_r13_loop3_cross_archetype_redteam/round79_r13_loop3_cross_archetype_redteam_summary.md`
- `output/e2r_round79_r13_loop3_cross_archetype_redteam/round79_r13_loop3_case_matrix.csv`
- `output/e2r_round79_r13_loop3_cross_archetype_redteam/round79_r13_loop3_overlay_target_matrix.csv`
- `output/e2r_round79_r13_loop3_cross_archetype_redteam/round79_r13_loop3_stage_date_plan.csv`
- `output/e2r_round79_r13_loop3_cross_archetype_redteam/round79_r13_loop3_redteam_gate_plan.md`
- `output/e2r_round79_r13_loop3_cross_archetype_redteam/round79_r13_loop3_price_validation_plan.md`
- `output/e2r_round79_r13_loop3_cross_archetype_redteam/round79_r13_loop3_price_fields.csv`

## Guardrails

- Round79 overlay는 calibration/evaluation material이다.
- Case record를 후보 생성 input으로 쓰지 않는다.
- Stage 3-Green은 점수만으로 나오면 안 된다.
- Green에는 cross-evidence, EPS/FCF 지속성, 가격경로 alignment, hard RedTeam 부재, 4B 포화 부재가 같이 필요하다.
- 정책 shock은 회사의 EPS/FCF 근거가 아니라 price-path RedTeam overlay다.
- stablecoin은 regulated fiat-backed와 algorithmic/de-peg risk를 반드시 분리한다.
- 회계, 운영 신뢰, 법적/규제, 레버리지/FCF, 상업화 실패, AFFO 무결성, convertibility risk는 hard review 또는 hard gate로 남긴다.

## Verification

- `PYTHONPATH=src python -m unittest tests.test_round79_r13_loop3_cross_archetype_redteam -v`
- `PYTHONPATH=src python -m e2r.cli.build_round79_r13_loop3_report`
- `PYTHONPATH=src python -m compileall -q src tests`
- `PYTHONPATH=src python -m unittest discover -s tests -v`
- `git diff --check`

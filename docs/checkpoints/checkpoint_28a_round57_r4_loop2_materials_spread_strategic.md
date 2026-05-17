# Checkpoint 28A Round57 R4 Loop 2: Materials / Spread / Strategic Resources

## 목적

`docs/round/round_57.md`의 R4 Loop 2 내용을 반영했다. 이번 라운드는 소재·스프레드·전략자원에서 자주 생기는 오판을 줄이는 작업이다.

쉬운 예시는 이렇다.

- 희토류 가격이 올랐다는 사실은 좋은 검색 신호일 수 있다.
- 하지만 그 회사가 실제 생산능력, 장기 offtake, price floor, 정부지원, FCF 경로를 갖지 못하면 Stage 3-Green 근거가 아니다.
- 화학 spread 반등도 마찬가지다. 중국·중동 공급과잉이 남아 있으면 Watch/Red로 먼저 봐야 한다.

## 반영 내용

- `E2RArchetype`에 R4 Loop 2 세부 canonical archetype을 추가했다.
- Round57 전용 calibration module을 추가했다.
- Round57 리포트 CLI를 추가했다.
- case library JSONL, score-weight draft CSV, case matrix, stage-date plan, guardrail, risk overlay, price-validation plan을 생성했다.
- production scoring/staging/red-team 로직은 변경하지 않았다.

## 추가된 archetype

- `REFINING_OIL_SPREAD`
- `CHEMICAL_SPREAD`
- `STEEL_METAL_SPREAD`
- `NONFERROUS_STRATEGIC_METALS`
- `LITHIUM_BATTERY_RAW_MATERIAL`
- `PRECIOUS_METALS_SAFE_HAVEN_MINERS`
- `PAPER_PACKAGING_CYCLE`
- `AGRI_COMMODITY_INPUTS`
- `LNG_ENERGY_TRADING_DISTRIBUTION`
- `GENERAL_TRADING_RESOURCE_INFRA`
- `ENERGY_UTILITY_LNG_GAS`

기존 `RARE_METALS_STRATEGIC_MATERIALS`, `ADVANCED_MATERIAL_SPECULATIVE_THEME`도 R4 Loop 2 target에 포함했다.

## 산출물

- `src/e2r/sector/round57_r4_loop2_materials_spread_strategic.py`
- `src/e2r/cli/build_round57_r4_loop2_report.py`
- `tests/test_round57_r4_loop2_materials_spread_strategic.py`
- `data/e2r_case_library/cases_r4_loop2_round57.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round57_r4_loop2_v2.csv`
- `output/e2r_round57_r4_loop2_materials_spread_strategic/round57_r4_loop2_materials_spread_strategic_summary.md`
- `output/e2r_round57_r4_loop2_materials_spread_strategic/round57_r4_loop2_case_matrix.csv`
- `output/e2r_round57_r4_loop2_materials_spread_strategic/round57_r4_loop2_stage_date_plan.csv`
- `output/e2r_round57_r4_loop2_materials_spread_strategic/round57_r4_loop2_green_guardrails.md`
- `output/e2r_round57_r4_loop2_materials_spread_strategic/round57_r4_loop2_risk_overlays.md`
- `output/e2r_round57_r4_loop2_materials_spread_strategic/round57_r4_loop2_price_validation_plan.md`
- `output/e2r_round57_r4_loop2_materials_spread_strategic/round57_r4_loop2_price_fields.csv`

## 케이스 요약

- target_count: 13
- case_candidate_count: 13
- structural_success_count: 1
- success_candidate_count: 3
- cyclical_success_count: 2
- event_premium_count: 3
- overheat_count: 1
- stage4c_case_count: 3
- watch_yellow_first_count: 11
- redteam_first_count: 2
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## 핵심 guardrail

- commodity price 자체는 구조적 증거가 아니다.
- spread recovery는 inventory gain/loss와 공급과잉을 제외하고 봐야 한다.
- tender offer, M&A premium, governance event는 FCF rerating과 분리한다.
- 희토류는 price floor, offtake, production capacity, government support, FCF가 같이 있어야 상위 단계 후보가 된다.
- 초전도체·그래핀·맥신 같은 과학 테마는 상용 매출 전에는 RedTeam-first다.
- case library는 calibration/evaluation 자료이며 candidate-generation input으로 쓰지 않는다.

## 실행 명령

```bash
PYTHONPATH=src python -m e2r.cli.build_round57_r4_loop2_report
PYTHONPATH=src python -m unittest tests.test_round57_r4_loop2_materials_spread_strategic -v
```

## 남은 일

- stage date와 가격 데이터는 아직 backfill 대상이다.
- Round57 weight는 shadow/calibration draft이며 production scoring에 적용하지 않았다.
- 다음 단계에서는 price path, MFE/MAE, spread metric, offtake/price floor 검증을 채워야 한다.

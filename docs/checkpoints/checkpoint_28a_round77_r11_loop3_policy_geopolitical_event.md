# Checkpoint 28A Round 77 - R11 Loop 3 Policy / Geopolitical / Disaster / Event

Round 77 반영 완료.

## Scope

- source round: `docs/round/round_77.md`
- large sector: `POLICY_GEOPOLITICAL_EVENT`
- loop: `R11 Loop 3 / v3.0`
- production scoring changed: `false`
- case records are candidate-generation input: `false`

이번 라운드는 큰 뉴스와 실제 E2R 증거를 더 강하게 분리한다.
쉬운 예로, 감염병 뉴스는 Stage 1 라우팅 신호가 될 수 있지만, `government_order`, `stockpile_contract`, `guide_up`, 반복 조달, 매출 전환이 없으면 Stage 3-Green 근거가 아니다.

## Targets

- target_count: 13
- green_possible_count: 0
- watch_yellow_first_count: 4
- redteam_first_count: 9
- gate_only_target_count: 2

추가/강화된 핵심 타깃:

- `EVENT_TO_CONTRACT_ESCALATION`: 이벤트가 실제 계약, 정부 주문, 예산, 금융조달, 착공, 매출로 바뀌는지 별도 추적.
- `POLICY_MARKET_SHOCK_EVENT`: 세금, 시민배당, 규제 발언, 시장 전반 매도 압력을 RedTeam gate로 분리.
- `NORTH_KOREA_POLICY_EVENT`: 제재 완화와 현금흐름 프로젝트 전에는 강한 RedTeam 우선.
- `CLIMATE_DISASTER_EVENT`: 폭염·재난 뉴스는 grid, VPP, ESS, 냉방 주문, 반복 capex로 연결될 때만 강화.
- `SPECULATIVE_SCIENCE_THEME`: preprint·SNS 테마는 독립 재현, 고객, 제품, 매출 없이는 Green 근거가 아니다.
- `THEME_VALUATION_OVERHEAT`: 가격만 움직인 테마를 양수 점수가 아니라 unsafe Green 차단 gate로 유지.

## Case Pack

- case_candidate_count: 13
- success_candidate_count: 4
- event_premium_count: 4
- stage4b_case_count: 2
- stage4c_case_count: 4

우선 검증 케이스:

- `bavarian_nordic_us_stockpile_contract_case`
- `bavarian_nordic_2024_mpox_order_case`
- `ukraine_telecom_ebrd_ifc_case`
- `heatwave_ac_grid_stress_case`
- `nyc_ac_battery_vpp_case`
- `north_korea_kumgang_dismantle_case`
- `lk99_superconductor_no_replication_case`
- `lk99_cu2s_impurity_case`
- `abbott_diagnostics_demand_wane_case`
- `yellow_dust_mask_event_case`
- `policy_local_theme_case`
- `disaster_rebuild_material_case`
- `ai_citizen_dividend_policy_shock_case`

## Outputs

- `data/e2r_case_library/cases_r11_loop3_round77.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round77_r11_loop3_v3.csv`
- `output/e2r_round77_r11_loop3_policy_geopolitical_event/round77_r11_loop3_policy_geopolitical_event_summary.md`
- `output/e2r_round77_r11_loop3_policy_geopolitical_event/round77_r11_loop3_case_matrix.csv`
- `output/e2r_round77_r11_loop3_policy_geopolitical_event/round77_r11_loop3_stage_date_plan.csv`
- `output/e2r_round77_r11_loop3_policy_geopolitical_event/round77_r11_loop3_green_guardrails.md`
- `output/e2r_round77_r11_loop3_policy_geopolitical_event/round77_r11_loop3_event_false_positive_caps.md`
- `output/e2r_round77_r11_loop3_policy_geopolitical_event/round77_r11_loop3_price_validation_plan.md`
- `output/e2r_round77_r11_loop3_policy_geopolitical_event/round77_r11_loop3_price_fields.csv`

## Guardrails

- R11 Loop 3 weights are calibration material only.
- Case records must not be used as candidate-generation input.
- Policy headline, war/reconstruction slogan, disaster, outbreak, local policy, or preprint cannot create Green alone.
- Green unlock evidence must be source-backed contract, government order, budget, financing, construction start, recognized revenue, recurring demand, or EPS/FCF conversion.
- `POLICY_MARKET_SHOCK_EVENT` is a gate: market-wide tax or dividend comments are risk evidence unless company-level EPS/FCF impact is measurable.
- Do not invent contracts, budgets, dose amounts, financing, guidance, company exposure, stage dates, or stage prices.

## Verification

- `PYTHONPATH=src python -m e2r.cli.build_round77_r11_loop3_report`
- `PYTHONPATH=src python -m unittest tests.test_round77_r11_loop3_policy_geopolitical_event -v`
- `PYTHONPATH=src python -m compileall -q src tests`
- `PYTHONPATH=src python -m unittest discover -s tests -v`
- `git diff --check`

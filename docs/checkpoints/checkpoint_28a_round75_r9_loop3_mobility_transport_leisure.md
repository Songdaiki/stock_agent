# Checkpoint 28A Round 75 - R9 Loop 3 Mobility / Transport / Leisure

Round 75 반영 완료.

## Scope

- source round: `docs/round/round_75.md`
- large sector: `MOBILITY_TRANSPORT_LEISURE`
- loop: `R9 Loop 3 / v3.0`
- production scoring changed: `false`
- case records are candidate-generation input: `false`

이번 라운드는 `수요 회복`, `하이브리드`, `관광 정책`, `운임 상승`, `로보택시`, `eVTOL`, `위성 테마`를 실제 E2R 증거와 분리한다.
쉬운 예로, eVTOL의 `Part 135`는 의미 있는 운항 관련 이정표지만 기체 형식 인증, 상업 매출, 양호한 unit economics가 아니므로 Stage 3-Green 근거로 쓰면 안 된다.

## Targets

- target_count: 19
- green_possible_count: 2
- watch_yellow_first_count: 12
- redteam_first_count: 5
- gate_only_target_count: 2

추가/강화된 핵심 타깃:

- `AUTO_HYBRID_VALUEUP`: 완성차 하이브리드 mix, OPM, FCF, 자사주/배당을 결합해 검증.
- `HYBRID_COMPONENT_BOTTLENECK`: 하이브리드 모터, 인버터, 자석, 배터리팩 병목이 실제 납품과 마진으로 이어지는지 분리.
- `AUTONOMOUS_ROBOTAXI_DEPLOYMENT`: 서비스 지역, 유료 ride volume, fleet size, safety record, unit economics를 요구.
- `SATELLITE_CONNECTIVITY_INFRA`: 항공 connectivity 계약, backlog, 반복매출을 위성 테마와 분리.
- `TRANSPORT_SAFETY_REGULATORY_OVERLAY`: 자율주행, eVTOL, 항공 안전사고를 RedTeam gate로 분리.
- `FLEET_UNIT_ECONOMICS_OVERLAY`: 렌터카, EV fleet, 마이크로모빌리티의 감가, 보험, 수리비, utilization 리스크를 gate로 분리.

## Case Pack

- case_candidate_count: 18
- structural_success_count: 0
- success_candidate_count: 5
- cyclical_success_count: 1
- event_premium_count: 3
- stage4b_case_count: 11
- stage4c_case_count: 6

우선 검증 케이스:

- `hyundai_hybrid_valueup_case`
- `hyundai_tariff_margin_cut_case`
- `toyota_hybrid_parts_bottleneck_case`
- `avride_hyundai_ioniq5_robotaxi_case`
- `waymo_flood_recall_robotaxi_case`
- `waymo_houston_expansion_case`
- `korean_air_asiana_integration_case`
- `china_group_visa_tourism_case`
- `ses_airline_connectivity_case`
- `maersk_container_rate_collapse_case`
- `maersk_suez_overcapacity_loss_case`
- `hertz_ev_rental_failure_case`
- `michelin_tire_demand_cut_case`
- `lime_ipo_micromobility_case`
- `joby_discounted_offering_case`
- `lilium_evtol_cash_crunch_case`
- `archer_part135_no_type_cert_case`
- `archer_nyc_network_case`

## Outputs

- `data/e2r_case_library/cases_r9_loop3_round75.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round75_r9_loop3_v3.csv`
- `output/e2r_round75_r9_loop3_mobility_transport_leisure/round75_r9_loop3_mobility_transport_leisure_summary.md`
- `output/e2r_round75_r9_loop3_mobility_transport_leisure/round75_r9_loop3_case_matrix.csv`
- `output/e2r_round75_r9_loop3_mobility_transport_leisure/round75_r9_loop3_stage_date_plan.csv`
- `output/e2r_round75_r9_loop3_mobility_transport_leisure/round75_r9_loop3_green_guardrails.md`
- `output/e2r_round75_r9_loop3_mobility_transport_leisure/round75_r9_loop3_risk_overlays.md`
- `output/e2r_round75_r9_loop3_mobility_transport_leisure/round75_r9_loop3_price_validation_plan.md`
- `output/e2r_round75_r9_loop3_mobility_transport_leisure/round75_r9_loop3_price_fields.csv`

## Guardrails

- R9 Loop 3 weights are calibration material only.
- Case records must not be used as candidate-generation input.
- Demand recovery, tourism policy, freight spike, hybrid label, robotaxi announcement, eVTOL milestone, or satellite theme cannot create Green alone.
- Green requires OPM, FCF, capital return, unit economics, certification, backlog, recurring revenue, or safety/regulatory evidence depending on target.
- Freight and airline/tourism recovery are cycle evidence first; structural Green requires durable margin and cash-flow evidence.
- Safety recalls, NHTSA scrutiny, weather handling failure, EV fleet residual value loss, certification delay, discounted offerings, and overcapacity are RedTeam gates.
- Do not invent OPM, FCF, tariff impact, freight rate, drop amount, tourist spend, unit economics, certification, backlog, or stage-price fields.

## Verification

- `PYTHONPATH=src python -m e2r.cli.build_round75_r9_loop3_report`
- `PYTHONPATH=src python -m unittest tests.test_round75_r9_loop3_mobility_transport_leisure -v`
- `PYTHONPATH=src python -m compileall -q src tests`
- `PYTHONPATH=src python -m unittest discover -s tests -v`
- `git diff --check`

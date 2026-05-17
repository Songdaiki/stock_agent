# Checkpoint 28A Round 76 - R10 Loop 3 Construction / Real Estate / Building Materials

Round 76 반영 완료.

## Scope

- source round: `docs/round/round_76.md`
- large sector: `CONSTRUCTION_REAL_ESTATE_MATERIALS`
- loop: `R10 Loop 3 / v3.0`
- production scoring changed: `false`
- case records are candidate-generation input: `false`

이번 라운드는 `수주잔고`, `고배당`, `AI 데이터센터`, `재건/네옴/세종시 정책 테마`를 실제 E2R 증거와 분리한다.
쉬운 예로, 데이터센터 REIT가 상장했다는 사실은 Stage 1 신호가 될 수 있지만, 실제 자산 취득, binding tenant lease, NOI/AFFO, 전력·수자원 확보, 배당 커버리지가 없으면 Stage 3-Green 근거가 아니다.

## Targets

- target_count: 16
- green_possible_count: 3
- watch_yellow_first_count: 5
- redteam_first_count: 8
- gate_only_target_count: 4

추가/강화된 핵심 타깃:

- `PF_RESTRUCTURING_RELIEF`: 정부 PF 지원책을 회복이 아니라 Stage 1 relief로 분리.
- `DATA_CENTER_REIT_INFRASTRUCTURE`: AI 데이터센터 REIT를 자산, tenant, NOI/AFFO, 전력·수자원 기준으로 검증.
- `AI_DATA_CENTER_REAL_ASSET_DEVELOPMENT`: 무매출 AI 데이터센터 개발사를 high-risk Watch로 분리.
- `DATA_CENTER_POWER_WATER_PERMITTING`: 전력, 수자원, grid interconnection, 지역반발, 철회를 RedTeam gate로 분리.
- `COLD_CHAIN_REIT_LOGISTICS`: cold-chain warehouse scale을 occupancy, energy cost, NOI/AFFO, debt로 검증.
- `BUILDING_MATERIALS_PRICE_COST`: 가격전가, 비용관리, 출하량, OPM, FCF가 같이 확인될 때만 Green 가능.
- `BUILDING_MATERIALS_VOLUME_FAILURE`: 가격인상과 cost cut이 있어도 volume/EBITDA 약하면 Green 제한.
- `REIT_AFFO_INTEGRITY_OVERLAY`: AFFO 착시, maintenance capex, dividend coverage를 gate로 분리.
- `AI_INFRA_REAL_ASSET_THEME_OVERLAY`: 자산·tenant·매출 없는 AI real asset 테마를 gate로 분리.

## Case Pack

- case_candidate_count: 16
- structural_success_count: 0
- success_candidate_count: 2
- event_premium_count: 4
- failed_rerating_count: 1
- stage4b_case_count: 9
- stage4c_case_count: 6

우선 검증 케이스:

- `korea_pf_delinquency_restructuring_case`
- `korea_builder_support_relief_case`
- `blackstone_mortgage_trust_dividend_cut_case`
- `equinix_affo_integrity_short_case`
- `equinix_ai_capex_burden_case`
- `blackstone_data_center_reit_flat_debut_case`
- `fermi_ai_data_center_no_revenue_case`
- `perth_datacenter_withdrawal_case`
- `utah_stratos_datacenter_backlash_case`
- `lineage_cold_storage_ipo_case`
- `lineage_cold_storage_drawdown_case`
- `heidelberg_materials_price_cost_case`
- `cemex_demand_slowdown_costcut_case`
- `ukraine_reconstruction_event_watch_case`
- `neom_city_event_watch_case`
- `sejong_policy_theme_case`

## Outputs

- `data/e2r_case_library/cases_r10_loop3_round76.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round76_r10_loop3_v3.csv`
- `output/e2r_round76_r10_loop3_construction_real_estate_materials/round76_r10_loop3_construction_real_estate_materials_summary.md`
- `output/e2r_round76_r10_loop3_construction_real_estate_materials/round76_r10_loop3_case_matrix.csv`
- `output/e2r_round76_r10_loop3_construction_real_estate_materials/round76_r10_loop3_stage_date_plan.csv`
- `output/e2r_round76_r10_loop3_construction_real_estate_materials/round76_r10_loop3_green_guardrails.md`
- `output/e2r_round76_r10_loop3_construction_real_estate_materials/round76_r10_loop3_risk_overlays.md`
- `output/e2r_round76_r10_loop3_construction_real_estate_materials/round76_r10_loop3_price_validation_plan.md`
- `output/e2r_round76_r10_loop3_construction_real_estate_materials/round76_r10_loop3_price_fields.csv`

## Guardrails

- R10 Loop 3 weights are calibration material only.
- Case records must not be used as candidate-generation input.
- Construction backlog, dividend yield, rate-cut expectation, AI data-center label, reconstruction headline, Neom, or local policy cannot create Green alone.
- Construction Green requires PF exposure reduction, refinancing success, cash conversion, and cost-ratio stability.
- REIT Green requires occupancy, NOI/AFFO, dividend coverage, LTV/funding-cost control, and AFFO integrity.
- Data-center real-asset Green requires acquired assets, binding tenant lease, power/water/grid access, NOI/AFFO, and financing stability.
- Building-material Green requires price pass-through, cost control, volume stability, OPM, and FCF.
- Do not invent PF exposure, NOI/AFFO, dividend coverage, tenant lease, power/water, occupancy, volume, OPM, FCF, or stage prices.

## Verification

- `PYTHONPATH=src python -m e2r.cli.build_round76_r10_loop3_report`
- `PYTHONPATH=src python -m unittest tests.test_round76_r10_loop3_construction_real_estate_materials -v`
- `PYTHONPATH=src python -m compileall -q src tests`
- `PYTHONPATH=src python -m unittest discover -s tests -v`
- `git diff --check`

# Checkpoint 28A Round 78 - R12 Loop 3 Agriculture / Life Services / Misc

Round 78 반영 완료.

## Scope

- source round: `docs/round/round_78.md`
- large sector: `EDUCATION_LIFE_AGRI_MISC`
- loop: `R12 Loop 3 / v3.0`
- production scoring changed: `false`
- case records are candidate-generation input: `false`

이번 라운드는 농업, 교육, 렌탈, 키오스크, 규제형 소비재에서 “생활 필수”, “AI 교육”, “질병 수혜”, “규제 완화” 같은 라벨과 실제 반복 FCF를 분리한다.
쉬운 예로, 스마트팜이 좋아 보여도 전력비, CAPEX, 가동률, 고객계약, FCF가 안 맞으면 Bowery/AppHarvest처럼 4C 반례가 된다.

## Targets

- target_count: 18
- green_possible_count: 0
- watch_yellow_first_count: 11
- redteam_first_count: 7
- gate_only_target_count: 3

추가/강화된 핵심 타깃:

- `VERTICAL_FARMING_UNIT_ECONOMICS`: 스마트팜 일반론에서 수직농장 unit economics 실패를 분리.
- `AGRI_MACHINERY_SOFTWARE_LOCKIN`: software attach와 right-to-repair/FTC/고객반발 리스크를 분리.
- `EDTECH_AI_DISRUPTION`: AI가 교육 서비스를 보강하는지, Chegg처럼 대체하는지를 gate로 분리.
- `ONLINE_EDUCATION_OPM_DISTRESS`: 2U식 부채, student ROI, partner concentration, 규제 리스크를 별도 분리.
- `NICOTINE_ALTERNATIVE_REGULATED`: 반복소비 구조와 청소년/public health/허가범위 gate를 분리.
- `CANNABIS_REGULATED_PRODUCT`: rescheduling을 완전 합법화로 과대해석하지 않도록 분리.

## Case Pack

- case_candidate_count: 17
- success_candidate_count: 4
- cyclical_success_count: 1
- event_premium_count: 2
- failed_rerating_count: 3
- stage4b_case_count: 3
- stage4c_case_count: 7

우선 검증 케이스:

- `john_deere_autonomous_agri_ces_case`
- `deere_farm_equipment_demand_slowdown_case`
- `deere_right_to_repair_settlement_case`
- `zoetis_bird_flu_vaccine_conditional_case`
- `calmaine_egg_price_profit_case`
- `bowery_vertical_farming_shutdown_case`
- `appharvest_chapter11_case`
- `duolingo_ai_strategy_bookings_miss_case`
- `chegg_ai_disruption_case`
- `2u_chapter11_case`
- `coway_rental_recurring_case`
- `whirlpool_dividend_suspension_case`
- `target_self_checkout_limit_case`
- `juul_fda_approval_case`
- `fda_vape_enforcement_easing_case`
- `who_nicotine_pouch_youth_warning_case`
- `cannabis_schedule3_limited_case`

## Outputs

- `data/e2r_case_library/cases_r12_loop3_round78.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round78_r12_loop3_v3.csv`
- `output/e2r_round78_r12_loop3_agri_life_misc/round78_r12_loop3_agri_life_misc_summary.md`
- `output/e2r_round78_r12_loop3_agri_life_misc/round78_r12_loop3_case_matrix.csv`
- `output/e2r_round78_r12_loop3_agri_life_misc/round78_r12_loop3_stage_date_plan.csv`
- `output/e2r_round78_r12_loop3_agri_life_misc/round78_r12_loop3_green_guardrails.md`
- `output/e2r_round78_r12_loop3_agri_life_misc/round78_r12_loop3_unit_economics_caps.md`
- `output/e2r_round78_r12_loop3_agri_life_misc/round78_r12_loop3_price_validation_plan.md`
- `output/e2r_round78_r12_loop3_agri_life_misc/round78_r12_loop3_price_fields.csv`

## Guardrails

- R12 Loop 3 weights are calibration material only.
- Case records must not be used as candidate-generation input.
- 생활 필수, 농업, 교육, 규제 완화, 질병 이벤트, 무인화 라벨은 Green 근거가 아니다.
- Green에는 반복계약, 반복매출, unit economics, 판가전가, 해지율, CAC, regulatory approval scope, FCF 전환이 필요하다.
- AI가 핵심 서비스를 대체하거나, 수직농장 unit economics가 무너지거나, self-checkout 운영마찰이 커지면 RedTeam evidence로 본다.
- Do not invent unit economics, orders, CAC, churn, regulatory scope, software attach, disease orders, or stage prices.

## Verification

- `PYTHONPATH=src python -m e2r.cli.build_round78_r12_loop3_report`
- `PYTHONPATH=src python -m unittest tests.test_round78_r12_loop3_agri_life_misc -v`
- `PYTHONPATH=src python -m compileall -q src tests`
- `PYTHONPATH=src python -m unittest discover -s tests -v`
- `git diff --check`

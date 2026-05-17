# Checkpoint 28A Round 126 - R7 Loop 7 Biotech / Healthcare / Medical Device

## 반영 요약

- 입력 문서: `docs/round/round_126.md`
- 추가 모듈: `src/e2r/sector/round126_r7_loop7_biotech_healthcare_device.py`
- 추가 CLI: `src/e2r/cli/build_round126_r7_loop7_report.py`
- 추가 테스트: `tests/test_round126_r7_loop7_biotech_healthcare_device.py`
- 산출 케이스: `data/e2r_case_library/cases_r7_loop7_round126.jsonl`
- 산출 점수표: `data/sector_taxonomy/score_weight_profiles_round126_r7_loop7_v7.csv`
- 산출 리포트: `output/e2r_round126_r7_loop7_biotech_healthcare_device/`

## 핵심 판단

Round 126은 R7 바이오/헬스케어/의료기기에서 `허가·논문·임상`과 `상업화·반복매출·FCF`를 강하게 분리한다.

쉬운 예시는 다음과 같다.

- `FDA 승인`은 Stage 1~2 재료다.
- `AI 의료 AUC 0.91`도 Stage 1~2 재료다.
- Stage 3 후보가 되려면 `처방량`, `보험/PBM/수가`, `병원 도입`, `반복시술·소모품`, `가동률`, `OPM/FCF`, `가격경로 동행`이 같이 보여야 한다.

## 추가된 Loop 7 축

- `eps_fcf_commercialization_conversion`: 24
- `prescription_reimbursement_recurring_visibility`: 22
- `barrier_recurring_bottleneck`: 14
- `market_mispricing_rerating_gap`: 10
- `valuation_room_4b_runway`: 8
- `cash_runway_capital_discipline`: 10
- `safety_regulatory_disclosure_confidence`: 12

이 값은 프로덕션 점수에 적용하지 않았다. 케이스 라이브러리와 shadow calibration용 자료다.

## Stage Cap

- Stage 1 cap: 임상 결과, FDA/EMA 기대, 의료AI 논문, CDMO capacity, GLP-1 TAM, 바이오시밀러 승인 기대, 의료기기 출시 뉴스
- Stage 2 cap: 승인, PBM/formulary, 계약·시설 인수, procedure growth, external validation, pricing/launch plan
- Stage 3 후보: 처방량, 보험/수가, commercial revenue, OPM/FCF, procedure growth plus consumables, 반복 CDMO 계약·가동률, 가격경로 동행
- 4B-watch: GLP-1, 수술로봇, CDMO, 의료AI, 바이오시밀러 consensus가 scripts/FCF보다 먼저 가격에 반영된 경우
- 4C: 가격전쟁, compounded crackdown, cash crunch, discounted take-private, forecast cut, impairment, patent litigation, counterfeit/safety warning

## 케이스 정합성

- `samsung_biologics_gsk_us_facility_case`: 미국 생산거점과 60,000L capacity는 Stage 2지만 고객계약·가동률·OPM/FCF 전까지 Stage 3를 막는다.
- `intuitive_surgical_q1_2026_procedure_growth_case`: installed base, procedure growth, instruments/accessories 반복매출이 맞물린 R7 구조적 medtech 기준 사례다.
- `lilly_foundayo_fda_approval_case`: oral GLP-1 approval은 Stage 2지만 scripts, 보험, gross-to-net, refill 전까지 Stage 3를 제한한다.
- `cigna_accredo_humira_biosimilar_zero_copay_case`: PBM/formulary와 $0 copay는 approval보다 강하지만 실제 처방전환과 margin defense가 필요하다.
- `lunit_dbt_subgroup_validation_case`: external validation은 의미 있지만 subgroup risk, 병원 도입, 수가 전까지 Green이 아니다.
- `novo_glp1_price_pressure_case`, `hims_branded_glp1_pivot_loss_case`, `bluebird_gene_therapy_cash_crunch_case`, `charles_river_cro_funding_crunch_case`, `teladoc_betterhelp_impairment_case`: R7 RedTeam이 실제 가격경로와 맞은 4C/4C-watch 반례다.
- `amgen_samsung_bioepis_biosimilar_litigation_case`, `botox_counterfeit_fda_warning_case`: 특허소송과 안전/위조품 gate를 hard RedTeam으로 둔다.

## 산출 파일

- `round126_r7_loop7_biotech_healthcare_device_summary.md`
- `round126_r7_loop7_case_matrix.csv`
- `round126_r7_loop7_stage_date_plan.csv`
- `round126_r7_loop7_green_guardrails.md`
- `round126_r7_loop7_risk_overlays.md`
- `round126_r7_loop7_price_validation_plan.md`
- `round126_r7_loop7_price_fields.csv`
- `round126_r7_loop7_base_score_weights.csv`
- `round126_r7_loop7_stage_caps.csv`
- `round126_r7_loop7_score_stage_price_alignment.csv`
- `round126_r7_loop7_score_stage_price_alignment.md`

## Guardrail

- 케이스 기록은 후보 생성 입력이 아니다.
- 프로덕션 scoring/staging/RedTeam 로직은 round126 팩을 import하지 않는다.
- Stage 3-Green 기준을 낮추지 않았다.
- 처방량, 보험/PBM, 수가, 가동률, 환자 uptake, 병원 도입, subgroup 성능, cash runway, stage price는 새로 꾸며 넣지 않았다.

## 검증

- `PYTHONPATH=src python -m unittest tests/test_round126_r7_loop7_biotech_healthcare_device.py -v`
- `PYTHONPATH=src python -m e2r.cli.build_round126_r7_loop7_report`

# Checkpoint 28A Round 124 - R5 Loop 7 Consumer / Retail / Brand

## 반영 요약

- 입력 문서: `docs/round/round_124.md`
- 추가 모듈: `src/e2r/sector/round124_r5_loop7_consumer_retail_brand.py`
- 추가 CLI: `src/e2r/cli/build_round124_r5_loop7_report.py`
- 추가 테스트: `tests/test_round124_r5_loop7_consumer_retail_brand.py`
- 산출 케이스: `data/e2r_case_library/cases_r5_loop7_round124.jsonl`
- 산출 점수표: `data/sector_taxonomy/score_weight_profiles_round124_r5_loop7_v7.csv`
- 산출 리포트: `output/e2r_round124_r5_loop7_consumer_retail_brand/`

## 핵심 판단

Round 124는 R5 소비재/유통/브랜드 영역에서 `브랜드가 떴다`와 `EPS/FCF 체급이 바뀐다`를 더 강하게 분리한다.

쉬운 예시는 다음과 같다.

- `TikTok에서 화장품이 잘 팔림`은 Stage 1~2 재료다.
- `Ulta/Sephora/Target 입점`도 Stage 2 재료다.
- Stage 3 후보가 되려면 `sell-through`, `재주문`, `OPM/FCF 개선`, `재고·매출채권 안정`, `가격경로 동행`이 같이 보여야 한다.

## 추가된 Loop 7 축

- `eps_fcf_opm_transition`: 23
- `export_channel_visibility`: 22
- `repeat_consumption_sellthrough_reorder`: 18
- `market_mispricing_rerating_gap`: 10
- `valuation_room_4b_runway`: 8
- `inventory_receivables_margin_quality`: 10
- `safety_regulatory_trust_disclosure_confidence`: 9

이 값은 프로덕션 점수에 적용하지 않았다. 케이스 라이브러리와 shadow calibration용 자료다.

## Stage Cap

- Stage 1 cap: viral, GMV, 사용자 수, 채널 헤드라인만 있는 경우
- Stage 2 cap: 수출, ASP, OP/EPS revision, Amazon/TikTok/Ulta 매출, OEM 주문 증가
- Stage 3 후보: sell-through, 재주문, OPM/FCF, 재고·매출채권 안정, 가격경로 동행
- 4B-watch: 이미 K-food/K-beauty/beauty-device 리레이팅이 시장에서 널리 인정된 경우
- 4C: 리콜, data breach, 공급업체 압박, 대금지연, 관세, IP/제품안전, hardware guidance cut

## 케이스 정합성

- `samyang_buldak_export_rerating_case`: 수출·ASP·OP revision과 가격 +5.7%가 맞았지만 single hero product, recall, 해외 재고 gate를 유지한다.
- `kbeauty_us_export_overtake_france_case`: 미국 채널과 수출 성장은 Stage 2로 잡되 sell-through/reorder를 Stage 3 gate로 둔다.
- `apr_medicube_beauty_device_case`: 구조는 강하지만 APR 주가 4배 이상 사례라 4B-watch를 동시에 붙인다.
- `coupang_data_breach_case`: trust/security hard 4C로 둔다.
- `coupang_supplier_payment_regulation_case`: 물류 효율 마진과 공급업체 압박/대금지연 마진을 분리한다.
- `whirlpool_dividend_suspension_case`: 반복 서비스가 없는 hardware cycle 붕괴 4C 사례로 둔다.
- `shein_temu_ip_litigation_case`, `shein_temu_eu_product_safety_case`: fast-fashion 성장보다 IP, 제품안전, DSA, customs gate를 우선한다.
- `kbeauty_us_tariff_risk_case`: 수출 성장만으로 Green을 허용하지 않고 관세와 margin buffer를 본다.

## 산출 파일

- `round124_r5_loop7_consumer_retail_brand_summary.md`
- `round124_r5_loop7_case_matrix.csv`
- `round124_r5_loop7_stage_date_plan.csv`
- `round124_r5_loop7_green_guardrails.md`
- `round124_r5_loop7_risk_overlays.md`
- `round124_r5_loop7_price_validation_plan.md`
- `round124_r5_loop7_price_fields.csv`
- `round124_r5_loop7_base_score_weights.csv`
- `round124_r5_loop7_stage_caps.csv`
- `round124_r5_loop7_score_stage_price_alignment.csv`
- `round124_r5_loop7_score_stage_price_alignment.md`

## Guardrail

- 케이스 기록은 후보 생성 입력이 아니다.
- 프로덕션 scoring/staging/RedTeam 로직은 round124 팩을 import하지 않는다.
- Stage 3-Green 기준을 낮추지 않았다.
- 가격, stage date, sell-through, 재주문, 재고, 매출채권, FCF 값은 새로 꾸며 넣지 않았다.

## 검증

- `PYTHONPATH=src python -m unittest tests/test_round124_r5_loop7_consumer_retail_brand.py -v`
- `PYTHONPATH=src python -m e2r.cli.build_round124_r5_loop7_report`


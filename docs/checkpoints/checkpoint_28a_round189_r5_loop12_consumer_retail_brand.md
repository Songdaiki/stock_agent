# Checkpoint 28A Round 189: R5 Loop 12 Consumer / Retail / Brand

`docs/round/round_189.md`의 R5 Loop 12 내용을 calibration pack으로 반영했다.

## 반영 범위

- `src/e2r/sector/archetypes.py`
- `src/e2r/sector/round189_r5_loop12_consumer_retail_brand.py`
- `src/e2r/cli/build_round189_r5_loop12_report.py`
- `tests/test_round189_r5_loop12_consumer_retail_brand.py`
- `data/e2r_case_library/cases_r5_loop12_round189.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round189_r5_loop12_v12.csv`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/*`

## 핵심 분류

이번 라운드는 소비재·유통·브랜드를 다음 11개 target으로 쪼갰다.

- `K_FOOD_GLOBAL_LOCALIZATION`
- `K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE`
- `K_FOOD_SINGLE_SKU_EXPORT_RISK`
- `ECOMMERCE_RESTRUCTURING_JV_KOREA`
- `RETAIL_PLATFORM_DATA_REGULATION_OVERLAY`
- `DEPARTMENT_STORE_MALL_REDEVELOPMENT`
- `CONVENIENCE_STORE_PB_SSSG_KOREA`
- `K_BEAUTY_BRAND_SECOND_WAVE`
- `K_BEAUTY_TARIFF_IMPORT_REVIEW`
- `CHANNEL_STUFFING_INVENTORY_OVERLAY`
- `DISCLOSURE_CONFIDENCE_CAP`

예를 들어 `K_BEAUTY_BRAND_SECOND_WAVE`는 Amazon/TikTok 성장만으로는 부족하고, 오프라인 sell-through와 reorder, 재고/매출채권 안정, OPM/FCF가 같이 확인되어야 Stage 3 후보가 된다.

## 케이스팩

- target_count: 11
- case_candidate_count: 14
- success_candidate_count: 7
- failed_rerating_count: 4
- stage4b_case_count: 1
- stage4c_case_count: 2
- hard_gate_target_count: 2

대표 케이스:

- `cj_cheiljedang_kfood_localization_stage23_case`: 현지 생산과 Schwan’s 기반은 Stage 2 근거지만, 가동률·ASP·OPM·FCF 전 Green 금지.
- `orion_global_staple_brand_second_wave_case`: 반복소비형 글로벌 스낵 브랜드지만 지역별 성장률·OPM·원가전가가 필요.
- `emart_shinsegae_alibaba_jv_stage2_case`: JV와 +5.5% 이벤트 반응은 Stage 2 근거지만, GMV·take-rate·데이터 규제 통과가 필요.
- `kbeauty_online_viral_not_sellthrough_4b_case`: 온라인 viral이 sell-through보다 먼저 가격에 반영되면 4B-watch.
- `emart_alibaba_data_regulation_4c_watch_case`: KFTC 데이터 공유 제한은 플랫폼 수익화 cap.

## Guardrail

생산 점수 로직은 바꾸지 않았다.

- production_scoring_changed: false
- case_records_are_candidate_generation_input: false
- Stage 3-Green은 “K푸드”, “K뷰티”, “미국 입점”, “이커머스 JV”, “편의점 방어주” 키워드만으로 만들 수 없다.
- 5 of 8 조건: 해외매출/수출 증가, OP/EPS 상향 또는 OP beat, sell-through/reorder, 재고·채권 안정, ASP/gross margin 방어, Stage 2 이후 60D MFE +20%, hard issue 없음, valuation 과열 전.
- 4C hard gate: 관세, 오프라인 sell-through 실패, 채널 재고/매출채권 급증, JV 규제, 현지공장 가동률 부진, 단일 SKU 둔화, 원가/물류비 OPM 훼손, 중국·러시아 지역 리스크.

## 생성 산출물

```bash
PYTHONPATH=src python -m e2r.cli.build_round189_r5_loop12_report
```

생성 파일:

- `data/e2r_case_library/cases_r5_loop12_round189.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round189_r5_loop12_v12.csv`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_consumer_retail_brand_summary.md`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_case_matrix.csv`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_stage_date_plan.csv`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_green_guardrails.md`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_risk_overlays.md`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_price_validation_plan.md`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_price_fields.csv`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_base_score_weights.csv`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_stage_caps.csv`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_score_stage_price_alignment.csv`
- `output/e2r_round189_r5_loop12_consumer_retail_brand/round189_r5_loop12_score_stage_price_alignment.md`

## 검증

```bash
PYTHONPATH=src python -m unittest tests/test_round189_r5_loop12_consumer_retail_brand.py -v
```

결과: 통과.

## 다음 작업

R5 소비재·유통·브랜드는 가격경로와 품질 지표 backfill이 중요하다. 다음에는 CJ/오리온/K뷰티/편의점 케이스의 `plant_utilization`, `offline_sell_through_signal`, `reorder_signal`, `inventory_days_change`, `receivables_days_change`, `sssg`, `pb_mix`, `tariff_exposure`, `60D/120D MFE`를 채워 Stage 2와 Stage 3-Watch 경계를 검증해야 한다.

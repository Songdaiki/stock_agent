# Checkpoint 28A Round 176: R5 Loop 11 소비재·유통·브랜드 반영

## 목적

`docs/round/round_176.md`의 소비재·유통·브랜드 리서치 프레임을 case library와 score profile 초안으로 구조화했다.

이번 라운드는 K-beauty, K-food, Olive Young/CJ, OEM/ODM, China exposure, tariff, channel stuffing을 다룬다. 생산 점수 로직은 바꾸지 않았다.

쉬운 예시:

- `Silicon2`는 K-beauty 수출 플랫폼 후보로 볼 수 있지만, sell-through와 재고/매출채권 품질이 없으면 Stage 3-Green이 아니다.
- `D'Alba`는 미국 채널 확장 기대가 있어도 IPO 후 가격이 먼저 두 배 오르면 4B-watch가 필요하다.
- `CJ/Olive Young`은 플랫폼은 강하지만, CJ 주주가치로 현금흐름이나 NAV 할인 축소가 전달되어야 한다.

## 추가된 항목

- `src/e2r/sector/round176_r5_loop11_consumer_retail_brand.py`
- `src/e2r/cli/build_round176_r5_loop11_report.py`
- `tests/test_round176_r5_loop11_consumer_retail_brand.py`
- `data/e2r_case_library/cases_r5_loop11_round176.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round176_r5_loop11_v11.csv`
- `output/e2r_round176_r5_loop11_consumer_retail_brand/`

## Archetype 확장

라운드 176의 원문 canonical target 11개와 보조 target 2개를 반영했다.

- `K_BEAUTY_EXPORT_DISTRIBUTION_KOREA`
- `K_BEAUTY_BRAND_US_CHANNEL`
- `K_BEAUTY_RETAIL_PLATFORM_OPTION`
- `K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA`
- `K_FOOD_GLOBAL_STAPLE_BRAND`
- `K_FOOD_SINGLE_SKU_RISK`
- `APPAREL_LICENSE_BRAND_CHINA_RISK`
- `CHINA_CONSUMER_EXPOSURE_4C`
- `TARIFF_IMPORT_MARGIN_OVERLAY`
- `CHANNEL_STUFFING_INVENTORY_OVERLAY`
- `DISCLOSURE_CONFIDENCE_CAP`
- `K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE`
- `STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP`

## Base Score Weight 초안

이 비중은 production scoring에 적용하지 않았다. 향후 shadow scoring 캘리브레이션용이다.

| 축 | 점수 |
| --- | ---: |
| EPS/FCF·OPM conversion | 23 |
| export/channel visibility | 21 |
| sell-through/reorder/repeat consumption | 18 |
| inventory/receivables/margin quality | 12 |
| early price path validation | 10 |
| safety/tariff/disclosure confidence | 8 |
| valuation room / 4B runway | 8 |

## Stage 가드레일

- Stage 1: TikTok, Amazon, Olive Young, US listing, viral brand는 research routing 신호일 뿐이다.
- Stage 2: 해외 채널, 수출, ASP, IPO/platform option, OEM order visibility까지 가능하다.
- Stage 3: 7개 조건 중 4개 이상이 필요하다.
- Stage 4B: Stage 2 이후 120D MFE +80%, IPO/viral brand doubling, narrative-before-earnings, 재고/매출채권 악화, 키워드 crowding 중 3개 이상이면 watch가 필요하다.
- Stage 4C: China premium demand slowdown, tariff margin hit, channel stuffing, 재고/매출채권 spike, 단일 SKU demand drop, recall/safety, OEM churn, license-brand saturation/M&A overpay는 hard review다.

## Case Pack

11개 case candidate를 추가했다.

- `silicon2_kbeauty_distribution_stage3_candidate`
- `dalba_global_ipo_4b_watch_case`
- `cj_oliveyoung_platform_holdco_cap_case`
- `nongshim_global_staple_stage2_case`
- `kbeauty_oem_odm_supplychain_stage3_candidate`
- `drg_kbeauty_mna_stage2_reference_case`
- `amorepacific_china_exposure_4c_case`
- `kbeauty_tariff_import_margin_review_case`
- `fnf_license_brand_china_mna_watch_case`
- `channel_stuffing_inventory_overlay_case`
- `kfood_single_sku_viral_risk_case`

## 산출물

생성 명령:

```bash
PYTHONPATH=src python -m e2r.cli.build_round176_r5_loop11_report
```

주요 산출물:

- `output/e2r_round176_r5_loop11_consumer_retail_brand/round176_r5_loop11_consumer_retail_brand_summary.md`
- `output/e2r_round176_r5_loop11_consumer_retail_brand/round176_r5_loop11_case_matrix.csv`
- `output/e2r_round176_r5_loop11_consumer_retail_brand/round176_r5_loop11_stage_date_plan.csv`
- `output/e2r_round176_r5_loop11_consumer_retail_brand/round176_r5_loop11_green_guardrails.md`
- `output/e2r_round176_r5_loop11_consumer_retail_brand/round176_r5_loop11_risk_overlays.md`
- `output/e2r_round176_r5_loop11_consumer_retail_brand/round176_r5_loop11_price_validation_plan.md`
- `output/e2r_round176_r5_loop11_consumer_retail_brand/round176_r5_loop11_score_stage_price_alignment.md`

## 검증

라운드 전용 테스트:

```bash
PYTHONPATH=src python -m unittest tests.test_round176_r5_loop11_consumer_retail_brand -v
```

확인한 가드레일:

- production scoring 변경 없음
- case records는 candidate-generation input이 아님
- K-food/K-beauty 키워드, viral, US listing, Olive Young, Amazon/TikTok은 단독 Green 신호가 아님
- stage price, MFE/MAE, sell-through, reorder, inventory, receivables, OPM, FCF는 없으면 비워 둠

## 다음 작업

- K-beauty/K-food price path backfill
- sell-through/reorder proxy 자료 추가
- inventory days, receivables days, gross margin, OPM backfill
- CJ/Olive Young의 listed-parent transmission 검증
- tariff와 China exposure overlay를 shadow scoring에 연결하기 전 추가 케이스 축적

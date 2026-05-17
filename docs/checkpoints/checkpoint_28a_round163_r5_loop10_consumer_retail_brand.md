# Checkpoint 28A Round 163 R5 Loop 10 Consumer / Retail / Brand

## 목적

`docs/round/round_163.md`의 R5 Loop 10 내용을 별도 calibration pack으로 반영했다.

R5는 라면, K푸드, 화장품, beauty device, OEM/ODM, 이커머스, fast fashion, 생활가전을 다룬다. 이번 라운드의 핵심은 “브랜드가 떴다”와 “EPS/FCF 체급이 바뀐다”를 분리하는 것이다.

쉬운 예시는 다음과 같다.

- `미국 Ulta 입점`은 Stage 2 근거가 될 수 있다.
- 하지만 매장 sell-through, 재주문, OPM, 재고, 매출채권이 확인되지 않으면 Stage 3-Green 근거가 아니다.
- `Coupang data breach`는 고객 수와 물류 scale보다 먼저 보는 hard 4C gate다.
- `APR/Medicube`처럼 beauty device 구조가 좋아도 주가가 이미 수배 상승했다면 4B-watch를 같이 붙인다.

## 반영 파일

- `src/e2r/sector/round163_r5_loop10_consumer_retail_brand.py`
- `src/e2r/cli/build_round163_r5_loop10_report.py`
- `tests/test_round163_r5_loop10_consumer_retail_brand.py`
- `data/e2r_case_library/cases_r5_loop10_round163.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round163_r5_loop10_v10.csv`
- `output/e2r_round163_r5_loop10_consumer_retail_brand/`

## v10 기본 점수축

| component | weight | 해석 |
| --- | ---: | --- |
| eps_fcf_opm_transition | 23 | 수출·ASP가 OP/EPS/FCF와 같이 움직일 때만 강함 |
| export_channel_visibility | 22 | 미국·일본·유럽 매출, 오프라인 입점, Amazon/TikTok/Ulta/Sephora sales |
| repeat_consumption_sellthrough_reorder | 18 | 입점·viral이 아니라 sell-through와 재주문 확인 |
| safety_regulatory_trust_disclosure_confidence | 12 | 리콜, 관세, data breach, IP, 제품안전, trust 훼손 강화 |
| inventory_receivables_margin_quality | 10 | 재고, 매출채권, 할인율, CAC, 공급업체 압박, 대금지연 |
| market_mispricing_rerating_gap | 8 | 내수 소비재 old-frame과 이미 crowded global brand narrative 분리 |
| valuation_room_4b_runway | 7 | APR 4배 상승 같은 경우 4B-watch 강화 |

## 케이스 방향

- Stage 2~3 후보: `Samyang Buldak`, `K뷰티 미국 채널`, `Ulta K뷰티 retailer channel`, `APR/Medicube beauty device`, `K뷰티 OEM/ODM`
- 4C/RedTeam 후보: `Coupang data breach`, `Coupang supplier/payment delay`, `Whirlpool dividend suspension`, `Shein/Temu IP litigation`, `Shein/Temu unsafe item/DSA`
- Gate 후보: K뷰티 tariff/import review, channel stuffing, discount/promotion margin break

## Guardrail

- production scoring은 변경하지 않았다.
- case record는 candidate-generation input이 아니다.
- TikTok viral, 입점 뉴스, GMV, 고객 수, fast fashion growth만으로 Green을 만들지 않는다.
- 수출, ASP, 채널 visibility, sell-through, 재주문, OPM, FCF, 재고·매출채권 안정, trust, margin quality, 관세·규제 통과, 실제 가격경로를 확인해야 한다.

## 검증

실행한 명령:

```bash
PYTHONPATH=src python -m unittest tests/test_round163_r5_loop10_consumer_retail_brand.py -v
PYTHONPATH=src python -m e2r.cli.build_round163_r5_loop10_report
```

결과:

- Round 163 전용 테스트 12개 통과
- 원문 canonical target 26개와 보조 overlay target 4개를 분리해 보고
- score-stage-price alignment 12개 생성
- v10 score profile 생성
- case JSONL 생성
- summary, guardrail, risk overlay, price validation, stage cap, score-stage-price alignment 리포트 생성

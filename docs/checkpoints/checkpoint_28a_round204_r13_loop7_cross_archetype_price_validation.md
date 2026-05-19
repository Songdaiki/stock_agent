# Checkpoint 28A Round 204 R13 Loop 7 Cross-Archetype Price Validation

## 목적

Round 204는 R1~R12 후보를 다시 재판하는 R13 cross-archetype 가격검증 팩이다.

질문은 “좋은 섹터인가?”가 아니라 다음이다.

- Stage 3가 실제 대형 MFE를 잡았는가?
- 4B가 peak 전후 crowding과 valuation 포화를 잡았는가?
- 4C가 안전·계약·공시·운영 신뢰 훼손을 잡았는가?
- 가격이 증거보다 먼저 간 이벤트를 Green으로 착각하지 않았는가?

예: `as_of_date=2026-04-15`에 삼성SDS가 KKR CB와 AI 인프라 기대감으로 급등해도, AI 매출·마진·반복 cloud revenue가 없으면 Stage 3-Green이 아니라 Stage 2/4B-watch다.

## 추가 파일

- `src/e2r/sector/round204_r13_loop7_cross_archetype_price_validation.py`
- `src/e2r/cli/build_round204_r13_loop7_report.py`
- `tests/test_round204_r13_loop7_cross_archetype_price_validation.py`
- `data/e2r_case_library/cases_r13_loop7_round204.jsonl`
- `data/sector_taxonomy/round204_r13_loop7_cross_archetype_price_validation_audit.json`
- `output/e2r_round204_r13_loop7_cross_archetype_price_validation/`

## 케이스 요약

| case | source R | 판정 | 가격검증 |
| --- | ---: | --- | --- |
| SK하이닉스 | R2 | structural success + 4B-watch | 2025 +274%, 2026 YTD +200% 이상, 누적 최소 +1,022% anchor |
| 한화에어로스페이스 | R1 | structural success + 4B timing | 187,500원 → 1,435,000원, +665.3%; 증자일 -13% |
| 한국가스공사 | R11 | price moved without evidence | 동해 가스 뉴스 당일 장중 +30%, Stage 1/4B-watch |
| 삼성SDS | R8 | event premium + Stage 2 watch | KKR CB 발표일 장중 +20.8%, AI 매출 전 Green 금지 |
| 제주항공 | R9 | hard 4C | fatal crash 후 장중 -15.7%, operational trust break |
| LGES | R3 | hard 4C | Ford/Freudenberg 계약 취소, 기대매출 약 13.5조 원 손실 |
| L&F | R3 | hard 4C | Tesla 계약가치 $2.9B → $7,386, contract value collapse |
| 한화에어로 증자 overlay | R1/R13 | 4B-watch/elevated | 대시세 후 증자 충격은 hard 4C가 아니라 4B 진단 |

## 핵심 보정

올릴 축:

- `price_path_alignment`
- `stage3_to_large_mfe_confirmation`
- `cross_evidence`
- `eps_fcf_durability`
- `contract_quality`
- `operational_trust`
- `hard_4c_early_warning`

내릴 축:

- `policy_news_only`
- `resource_estimate_without_commerciality`
- `ai_capex_or_partnership_without_revenue`
- `contract_headline_without_calloff`
- `media_or_event_price_rally`
- `high_score_without_price_validation`
- `past_winner_similarity`

## Production 변경 여부

- production scoring changed: false
- candidate generation input: false
- shadow weight only: true
- price validation completed: partial with reported price anchors
- full OHLC complete: false

이번 라운드는 Reuters/FT/WSJ가 제공한 가격 anchor로 가능한 범위만 계산했다. KRX/Naver/Yahoo 수정주가 OHLC가 없는 항목은 숨기지 않고 `reported_*_anchor_not_full_ohlc`로 남겼다.

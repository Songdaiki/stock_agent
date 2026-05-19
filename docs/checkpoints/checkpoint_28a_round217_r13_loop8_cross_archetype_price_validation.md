# Checkpoint 28A Round 217 R13 Loop 8 Cross-Archetype Price Validation

## 목적

`docs/round/round_217.md`의 R13 Loop 8 내용을 cross-archetype RedTeam / 4B / 4C / 가격검증 팩으로 구조화했다.

이 라운드는 새 섹터를 추가하는 작업이 아니다. R1~R12에서 나온 후보를 한 번 더 부수면서, `Stage 3 성공`, `4B-watch`, `hard 4C`, `price_moved_without_evidence`를 같은 기준으로 비교한다.

쉬운 예시는 이렇다. SK하이닉스는 HBM 수요, OP revision, 이후 가격경로가 맞아서 Stage 3 성공 검증 사례가 된다. 반면 한국가스공사는 동해 가스 가능성 뉴스로 가격이 먼저 움직였지만, 상업성·매출·FCF가 없었기 때문에 Stage 3-Green이 아니다.

## 반영 내용

- R13 Loop 8 case pack을 추가했다.
- `ORDER_TO_REVENUE_CONVERSION`, `CONTRACT_QUALITY_BREAK`, `GOVERNANCE_DILUTION_EVENT`, `MARKET_STRUCTURE_WATCH`, `STRATEGIC_MATERIALS_WITH_GOVERNANCE_OVERLAY` archetype을 추가했다.
- SK하이닉스, 현대로템, 한화에어로스페이스, 한국가스공사, LGES/L&F, 제주항공, stablecoin basket, 고려아연을 한 표에서 비교했다.
- reported anchor 기반 MFE/MAE/계약가치 붕괴/시총 변화만 저장했다.
- full OHLC가 없는 항목은 `full_ohlc_complete=false`와 `reported_*_not_full_ohlc`로 명시했다.
- production scoring은 변경하지 않았다.

## 케이스 요약

| 케이스 | 분류 | 판단 |
|---|---|---|
| SK하이닉스 | structural_success + 4B | Stage 3 anchor 222,000원에서 reported peak 1,946,000원, +776.6%. 2026년 5월 기준 신규 Green보다 4B-watch |
| 현대로템 | structural_success | K2 납품, 매출, OP revision, 주가 +9.3%가 맞물린 R1 성공 기준점 |
| 한화에어로스페이스 | 4B-watch | 대시세 후 3.6조 증자와 -13% 이벤트. 자동 hard 4C는 아님 |
| 한국가스공사 | event_premium | 자원 추정과 정책 뉴스만으로 장중 +30%. 상업성 전 Green 금지 |
| LGES / L&F | hard 4C | 계약 취소와 계약가치 붕괴. 계약 headline Green 방지 기준점 |
| 제주항공 | hard 4C | fatal accident는 여행수요와 무관하게 operational trust hard 4C |
| Kakao Pay / stablecoin basket | overheat | 실제 규제수익 전 2~3배 움직인 policy theme |
| 고려아연 | success_candidate | 전략광물 Stage 2 후보지만 governance/dilution 해소 전 Stage 3 보류 |

## Green Gate

R13 공통 Stage 3-Green 필수 조건:

- 회사 단위 evidence
- revenue / EPS / FCF 경로
- evidence 이후 가격경로
- 의미 있는 Stage 3 이후 MFE
- 과도하지 않은 MAE
- 4B saturation 아님
- hard RedTeam 없음
- contract / operational / governance trust 통과

## 4B / 4C 구분

- 4B-watch: Stage 3 이후 2~5배 이상 상승, 시총 milestone, 대형 증자/CB, 정책·MOU·자원·stablecoin 테마 급등
- hard 4C: 계약 취소, 계약가치 붕괴, fatal safety accident, 운영 신뢰 훼손, 규제 반전, financing failure

예를 들어 한화에어로스페이스 증자 shock은 4B-watch/elevated다. 반대로 제주항공 fatal crash나 L&F 계약가치 붕괴는 hard 4C다.

## 산출물

- `data/e2r_case_library/cases_r13_loop8_round217.jsonl`
- `data/sector_taxonomy/round217_r13_loop8_cross_archetype_price_validation_audit.json`
- `output/e2r_round217_r13_loop8_cross_archetype_price_validation/round217_r13_loop8_price_validation_summary.md`
- `output/e2r_round217_r13_loop8_cross_archetype_price_validation/round217_r13_loop8_case_matrix.csv`
- `output/e2r_round217_r13_loop8_cross_archetype_price_validation/round217_r13_loop8_green_gate_review.md`
- `output/e2r_round217_r13_loop8_cross_archetype_price_validation/round217_r13_loop8_stage4b_4c_review.md`

## 검증

```bash
PYTHONPATH=src python -m unittest tests.test_round217_r13_loop8_cross_archetype_price_validation -v
PYTHONPATH=src python -m e2r.cli.build_round217_r13_loop8_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check
```

## 결론

Round 217은 R13의 역할을 명확히 했다. Stage 3는 가격경로로 검증하고, 4B는 가격 선반영·crowding·자본조달로 감시하며, 4C는 계약·운영·규제·신뢰 훼손으로만 선언한다. 가격이 먼저 움직인 정책/자원/stablecoin 이벤트는 Stage 3-Green으로 올리지 않는다.

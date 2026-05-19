# Checkpoint 28A Round 223 R6 Loop 9 Financial Capital Digital Price Validation

## 목적

`docs/round/round_223.md`의 R6 Loop 9 금융·자본배분·디지털금융 가격경로 검증 내용을 구조화했다.

이번 팩은 calibration/evaluation 자료다. 생산 scoring, StageClassifier, RedTeam, candidate generation은 변경하지 않았다.

쉬운 예:

- `저PBR + 밸류업`은 관심 신호다.
- 하지만 `ROE 개선 + CET1/K-ICS buffer + 실제 소각/배당 반복 + credit cost 안정`이 같이 확인되기 전에는 Stage 3-Green 근거가 아니다.

## 반영 파일

- `src/e2r/sector/round223_r6_loop9_financial_capital_digital_price_validation.py`
- `src/e2r/cli/build_round223_r6_loop9_report.py`
- `tests/test_round223_r6_loop9_financial_capital_digital_price_validation.py`
- `data/e2r_case_library/cases_r6_loop9_round223.jsonl`
- `data/sector_taxonomy/round223_r6_loop9_financial_capital_digital_price_validation_audit.json`
- `output/e2r_round223_r6_loop9_financial_capital_digital_price_validation/`

## 케이스 요약

| case | 해석 | Stage 처리 |
|---|---|---|
| KB금융 | ROE/PBR 밸류업 Stage 2 후보 | ROE/CET1/credit cost/반복 환원 전 Green 보류 |
| 증권주/금융주 basket | KOSPI bull market 수혜 | cyclical_success, 4B-watch |
| SK스퀘어 | NAV discount + 실제 소각 | 반복 소각과 discount narrowing 전 Green 보류 |
| 삼성생명 | 삼성전자 지분/NAV capital release | 매각대금 활용, K-ICS/CSM 확인 전 Green 보류 |
| 하나금융/두나무 | regulated digital-asset equity option | 지분법 이익·규제수익·자본비율 영향 전 Green 보류 |
| NAVER/Dunamu | 플랫폼 M&A event | abnormal withdrawal로 exchange-trust 4C-watch |
| K Bank | 인터넷은행 IPO profitability 후보 | 상장 후 price path, ROE/NIM/credit quality 전 Green 보류 |
| Kakao/KakaoBank | 대주주 법적 리스크 | Green 차단, 4C-watch |
| Kakao Pay/stablecoin basket | 스테이블코인 정책 테마 급등 | price_moved_without_evidence, 4B/event premium |

## Green Gate

R6 Stage 3-Green은 다음을 요구한다.

- ROE 개선 또는 유지
- CET1/K-ICS/capital buffer
- 실제 자사주 소각 또는 반복 배당/소각 실행
- credit cost/PF risk 통과
- PBR-ROE gap 축소 여지
- NAV monetization 또는 capital release 품질
- 디지털자산은 regulated revenue, 지분법, 수수료, reserve income 확인
- privacy/data/governance/exchange trust hard risk 부재
- evidence 이후 가격경로 확인

## 금지 패턴

- 저PBR만 있음
- 밸류업 정책 기대만 있음
- 자사주 매입만 있고 소각 없음
- 스테이블코인 정책 테마만 있음
- 디지털자산 지분 옵션만 있고 수익 없음
- 인터넷은행 IPO 계획만 있고 상장 후 price path 없음
- 대주주 법적 리스크
- 개인정보/데이터/거래소 신뢰 훼손
- 규제수익 전 이벤트 급등

## 산출물

CLI:

```bash
PYTHONPATH=src python -m e2r.cli.build_round223_r6_loop9_report
```

생성 파일:

- `round223_r6_loop9_price_validation_summary.md`
- `round223_r6_loop9_case_matrix.csv`
- `round223_r6_loop9_target_aliases.csv`
- `round223_r6_loop9_score_adjustments.csv`
- `round223_r6_loop9_shadow_weights.csv`
- `round223_r6_loop9_price_validation_fields.csv`
- `round223_r6_loop9_green_gate_review.md`
- `round223_r6_loop9_price_validation_plan.md`
- `round223_r6_loop9_stage4b_4c_review.md`

## 검증

실행한 명령:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest tests.test_round223_r6_loop9_financial_capital_digital_price_validation -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m e2r.cli.build_round223_r6_loop9_report
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -v
```

결과:

- 라운드223 전용 테스트: 9개 통과
- 라운드223 CLI 산출물 생성 완료
- 전체 테스트: 2756개 통과

## 변경하지 않은 것

- production scoring 변경 없음
- StageClassifier threshold 변경 없음
- 후보 생성 입력으로 케이스 사용 금지
- OHLC, stage price, MFE/MAE를 출처 없이 만들지 않음
- Stage 3-Green 기준 완화 없음

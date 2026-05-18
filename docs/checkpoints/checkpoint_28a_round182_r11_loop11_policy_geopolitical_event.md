# Checkpoint 28A Round 182 R11 Loop 11 Policy / Geopolitical / Event

## 반영 요약

- 입력 문서: `docs/round/round_182.md`
- 대섹터: `POLICY_GEOPOLITICAL_EVENT`
- 신규/보강 canonical target: 10개
- 케이스 후보: 11개
- 생산 scoring 변경: 없음
- case library의 candidate-generation 사용: 없음

## 핵심 원칙

R11은 “뉴스가 크다”와 “돈이 실제로 묶였다”를 분리하는 라운드다.

쉬운 예시는 이렇다.

- 동해 가스전/대왕고래: 한국가스공사·대성에너지 급등은 Stage 1 price-path evidence지만, 시추·상업성 전에는 Stage 3가 아니다.
- 공매도 정책: 수급과 시장구조에는 영향을 주지만, 개별 회사 EPS/FCF를 바꾸는 증거는 아니다.
- 비상계엄 정치 shock: 특정 종목 Green 근거가 아니라 국장 전체 valuation room을 낮추는 market-wide overlay다.
- 호르무즈/중동 energy shock: 한국은 에너지 수입국이라 원화·유가·수출주 MAE risk를 같이 본다.

## 추가 산출물

- `src/e2r/sector/round182_r11_loop11_policy_geopolitical_event.py`
- `src/e2r/cli/build_round182_r11_loop11_report.py`
- `tests/test_round182_r11_loop11_policy_geopolitical_event.py`
- `data/e2r_case_library/cases_r11_loop11_round182.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round182_r11_loop11_v11.csv`
- `output/e2r_round182_r11_loop11_policy_geopolitical_event/`

## Stage Gate 보강

- Stage 1 cap: 정책 발표, 탐사 발표, 공매도 제도 변경, 정치 shock, 전쟁·유가 shock은 45점 cap.
- Stage 2 cap: 탐사 착수, 예산·제도 확정, 정부주문, 감시시스템, 계약·매출 경로 확인 전에는 70점 cap.
- Stage 3: 8개 조건 중 5개 이상 필요.
- Stage 4B: 상한가·1D +20%, 계약/예산/매출 없는 basket rally는 4B-watch.
- Stage 4C: 탐사 실패, 정책 철회, 정치 시스템 shock, 원화·금리·유가 shock, 공매도 재개 후 valuation compression은 hard gate.

## 검증

```bash
PYTHONPATH=src python -m unittest tests.test_round182_r11_loop11_policy_geopolitical_event -v
PYTHONPATH=src python -m e2r.cli.build_round182_r11_loop11_report
```

Round 182는 R11 정책·지정학·재난·이벤트 score 설계용 calibration pack이다. Production StageClassifier threshold는 변경하지 않았다.

# Checkpoint 28A Round 224 R7 Loop 9 Biotech Healthcare Device Price Validation

## 반영 내용

- `docs/round/round_224.md`의 R7 Loop 9 바이오·헬스케어·의료기기 가격검증 라운드를 구조화했다.
- 추가 모듈: `src/e2r/sector/round224_r7_loop9_biotech_healthcare_device_price_validation.py`
- 추가 CLI: `PYTHONPATH=src python -m e2r.cli.build_round224_r7_loop9_report`
- 추가 테스트: `tests/test_round224_r7_loop9_biotech_healthcare_device_price_validation.py`
- 생성 산출물:
  - `data/e2r_case_library/cases_r7_loop9_round224.jsonl`
  - `data/sector_taxonomy/round224_r7_loop9_biotech_healthcare_device_price_validation_audit.json`
  - `output/e2r_round224_r7_loop9_biotech_healthcare_device_price_validation/round224_r7_loop9_price_validation_summary.md`
  - `output/e2r_round224_r7_loop9_biotech_healthcare_device_price_validation/round224_r7_loop9_case_matrix.csv`
  - `output/e2r_round224_r7_loop9_biotech_healthcare_device_price_validation/round224_r7_loop9_shadow_weights.csv`

## 핵심 결론

- 케이스 수: 7
- success_candidate: 5
- event_premium: 1
- failed_rerating: 1
- Stage 3 확정 케이스: 0
- 4B-watch 케이스: 7
- hard 4C 확정: 0
- full OHLC complete: false
- production scoring changed: false
- candidate generation input: false
- shadow weight only: true

## 케이스별 판단

| case | 판단 |
|---|---|
| 알테오젠 | Keytruda Qlex 매출은 Stage 2-to-3 경로를 검증하지만, 알테오젠 로열티 인식과 현금수취 전 Stage 3 확정 보류 |
| 유한양행 | FDA approval은 Stage 2, 처방량·J&J 매출·로열티·EPS revision 전 Stage 3 금지 |
| SK바이오사이언스 | IDT 인수는 Stage 2/event premium, 가동률·수주·마진·FCF 전 Green 금지 |
| 셀트리온 | 미국 생산시설은 tariff hedge Stage 2, 제품 이전·가동률·마진·FCF 확인 필요 |
| 삼성바이오로직스 | GSK 시설 인수는 좋은 CDMO 뉴스지만 단기 가격확인이 약해 evidence_good_but_price_failed |
| 휴젤 | Letybo 미국 출시는 Stage 2, 미국 매출·채널 침투·ASP·OPM 전 Green 금지 |
| 루닛 | 외부검증 AUC 0.91은 Stage 2 근거지만 수가·병원 도입·반복매출·cash runway 전 Stage 3 금지 |

쉬운 예시: `FDA approval`은 “문이 열렸다”는 뜻이다. R7에서 Stage 3-Green은 “문을 통과해서 실제 처방, 보험/수가, 매출, 로열티 또는 마진, FCF가 확인됐다”까지 와야 한다.

## Shadow Weight

상향 축:

- commercial_revenue +5
- royalty_recognition +5
- prescription_volume +5
- reimbursement_access +5
- capacity_utilization +5
- gross_margin_visibility +4
- cash_runway +4

하향 축:

- approval_news_only -5
- clinical_headline_only -5
- paper_validation_without_revenue -4
- mna_without_utilization -5
- FDA_approval_without_commercial_sales -4
- manufacturing_inspection_issue -4
- subgroup_performance_risk -3

이 값은 report/shadow 전용이다. 생산 StageClassifier나 scoring threshold에는 연결하지 않았다.

## Green Gate

R7 Stage 3-Green 필수 묶음:

- 승인 또는 regulatory clearance
- commercial launch
- 처방량 또는 병원 도입
- reimbursement / payer access
- revenue recognition
- royalty 또는 gross margin 확인
- cash runway / dilution risk 통과
- partner execution risk 통과
- evidence 이후 price path 확인

금지 패턴:

- 승인 뉴스만 있음
- 임상 헤드라인만 있음
- 논문 성능만 있음
- M&A 발표만 있음
- FDA approval 있지만 매출 없음
- partner peak sales만 있고 로열티 가시성 없음
- cash burn 또는 dilution risk 큼

## 검증

실행한 명령:

```bash
PYTHONPATH=src python -m unittest tests.test_round224_r7_loop9_biotech_healthcare_device_price_validation -v
PYTHONPATH=src python -m e2r.cli.build_round224_r7_loop9_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check
```

결과:

- 라운드224 테스트: 9개 통과
- 전체 테스트: 2765개 통과
- compileall: 통과
- `git diff --check`: 실패

`git diff --check` 실패 원인은 이번 라운드224 변경이 아니라 기존 dirty 상태의 `docs/round/round_192.md` 이후 여러 라운드 문서 trailing whitespace다. 사용자/다른 에이전트 변경으로 보이는 범위라 이번 패치에서 수정하지 않았다.

## 남은 작업

- R7은 OHLC가 아직 완전하지 않으므로 full price-path backfill이 필요하다.
- 알테오젠은 로열티 인식/현금수취, 유한양행은 처방량·파트너 매출·로열티, CDMO/CMO는 제품 이전·가동률·마진·FCF가 다음 검증 축이다.
- hard 4C는 이번 라운드에서 억지로 확정하지 않았다. 예: 제조시설 CRL은 효능/안전성 실패가 아니라면 `4C-watch`로 남긴다.

# Checkpoint 28A Round 69: R3 Loop 3 Battery / EV / Green-Energy

## 목적

Round 69는 R3 2차전지·전기차·친환경 섹터를 Loop 3 기준으로 다시 좁힌 작업이다.

핵심은 단순하다.

```text
EV 성장
≠ 모든 2차전지주 Green

ESS, 폐배터리, 수소, 태양광, 풍력, 리튬, 폐기물처리는
각각 EPS/FCF가 생기는 구조와 깨지는 방식이 다르다.
```

예를 들어 LGES-Tesla형 LFP ESS 계약은 계약금액·기간·고객·GWh가 있어 Stage 2 후보가 될 수 있다. 하지만 GM-LG Ohio 공장 idle이나 Ford-LGES 계약 취소는 EV CAPA가 곧바로 4C로 바뀔 수 있음을 보여준다.

## 반영 내용

- 추가 canonical archetype
  - `ESS_LFP_GRID_STORAGE`
  - `BATTERY_HEALTH_TRANSPARENCY_OVERLAY`
  - `LITHIUM_CYCLE_OVERLAY`
- 추가 모듈
  - `src/e2r/sector/round69_r3_loop3_battery_ev_green.py`
  - `src/e2r/cli/build_round69_r3_loop3_report.py`
  - `tests/test_round69_r3_loop3_battery_ev_green.py`
- 생성 산출물
  - `data/e2r_case_library/cases_r3_loop3_round69.jsonl`
  - `data/sector_taxonomy/score_weight_profiles_round69_r3_loop3_v3.csv`
  - `output/e2r_round69_r3_loop3_battery_ev_green/round69_r3_loop3_battery_ev_green_summary.md`
  - `output/e2r_round69_r3_loop3_battery_ev_green/round69_r3_loop3_case_matrix.csv`
  - `output/e2r_round69_r3_loop3_battery_ev_green/round69_r3_loop3_stage_date_plan.csv`
  - `output/e2r_round69_r3_loop3_battery_ev_green/round69_r3_loop3_green_guardrails.md`
  - `output/e2r_round69_r3_loop3_battery_ev_green/round69_r3_loop3_risk_overlays.md`
  - `output/e2r_round69_r3_loop3_battery_ev_green/round69_r3_loop3_price_validation_plan.md`
  - `output/e2r_round69_r3_loop3_battery_ev_green/round69_r3_loop3_price_fields.csv`

## 요약

- target: 14개
- case candidate: 13개
- structural success: 1개
- success candidate: 4개
- cyclical success: 1개
- failed rerating: 1개
- Stage 4B marker 포함: 2개
- Stage 4C thesis break: 6개
- Green possible: 2개
- Watch/Yellow first: 8개
- RedTeam first: 4개
- gate-only target: 2개

## Loop 3 핵심 변경

1. `ESS_LFP_GRID_STORAGE`를 별도 archetype으로 분리했다. ESS 계약금액, 계약기간, 고객, GWh, 생산공장, ESS OPM이 핵심이다.
2. `BATTERY_MATERIALS_CAPEX_OVERHEAT`는 더 보수적으로 낮췄다. EV 공장 idle, 계약 취소, EV 수요 둔화, 광물가격 하락이 4C로 이어질 수 있기 때문이다.
3. `BATTERY_RECYCLING_ESS_SHIFT`는 Watch-to-Green을 유지하되, SOH 검증과 second-life grading cost를 추가했다.
4. `SOLAR_TARIFF_SUPPLYCHAIN`은 통관, UFLPA, FEOC, 부품 억류를 RedTeam 축으로 강화했다.
5. `RENEWABLE_ENERGY_POLICY`는 PPA/정책보다 project economics, financing cost, foundation cost, impairment를 우선 확인하도록 했다.
6. `WASTE_RECYCLING_ENVIRONMENT`는 R3에서 드문 Green 가능 축으로 유지했다. 허가권, 처리량, 가동률, 반복 FCF가 핵심이다.
7. `BATTERY_HEALTH_TRANSPARENCY_OVERLAY`와 `EV_FIRE_RISK_OVERLAY`는 gate-only RedTeam이다.
8. `LITHIUM_CYCLE_OVERLAY`는 기본적으로 cycle/Watch다. ESS 수요 증가는 Stage 1~2 보조 근거일 수 있지만, 광산 재가동과 sodium-ion 대체 리스크를 먼저 본다.

## 검증

실행한 명령:

```bash
PYTHONPATH=src python -m unittest tests.test_round69_r3_loop3_battery_ev_green -v
PYTHONPATH=src python -m e2r.cli.build_round69_r3_loop3_report
```

결과:

- Round 69 전용 테스트 12개 통과
- Round 69 리포트 생성 성공
- production scoring/staging/red-team 모듈은 Round 69 case pack을 import하지 않음

## 주의

- production scoring threshold는 바꾸지 않았다.
- case record는 candidate generation input이 아니다.
- 계약금액, 고객명, 계약기간, GWh, 마진, 가동률, 회수량, SOH, stage price는 확인된 값만 써야 한다.
- API key 또는 민감정보는 산출물에 쓰지 않았다.
- 투자 권고 문구는 추가하지 않았다.

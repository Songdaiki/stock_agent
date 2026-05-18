# Checkpoint 28A Round 187: R3 Loop 12 Battery / EV / Green

## Summary

Round 187 반영을 완료했다. 이번 라운드는 국장 R3 대섹터에서 기존 2차전지 소재 반복을 줄이고, EV 둔화 이후의 ESS 전환, 보조금 이익 품질, 수소연료전지, 태양광 미국 내재화, 풍력 permit risk, 배터리 안전·공시 신뢰도 overlay를 별도 calibration pack으로 구조화했다.

이 패치는 생산 scoring/staging을 바꾸지 않는다. 케이스 레코드는 calibration/evaluation material이며 candidate-generation input이 아니다.

쉬운 예시는 이렇다. `LG에너지솔루션 ESS 전환`은 Stage 2 후보 근거가 될 수 있지만, 보조금 제외 OPM, 가동률, FCF가 확인되기 전에는 Stage 3-Green으로 올리지 않는다.

## Files Added

- `src/e2r/sector/round187_r3_loop12_battery_ev_green.py`
- `src/e2r/cli/build_round187_r3_loop12_report.py`
- `tests/test_round187_r3_loop12_battery_ev_green.py`
- `data/e2r_case_library/cases_r3_loop12_round187.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round187_r3_loop12_v12.csv`
- `output/e2r_round187_r3_loop12_battery_ev_green/*`

## Archetypes Added

Round 187에서 새 canonical archetype을 추가했다.

- `BATTERY_CONTRACT_CANCELLATION_4C`
- `BATTERY_TAX_CREDIT_QUALITY_OVERLAY`
- `COPPER_FOIL_EV_DEMAND_CYCLE`
- `BATTERY_EQUIPMENT_CAPEX_CYCLE`
- `BATTERY_RECYCLING_UNIT_ECONOMICS`
- `SODIUM_ION_NEXTGEN_MATERIALS`
- `HYDROGEN_FUEL_CELL_INFRA_KOREA`
- `SOLAR_US_LOCALIZATION_SUPPLYCHAIN`
- `WIND_POLICY_PERMITTING_RISK`
- `BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY`
- `EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY`

기존 `EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA`, `SEPARATOR_EV_DEMAND_CYCLE`, `ELECTROLYTE_CAPA_SUPPLYCHAIN`, `DISCLOSURE_CONFIDENCE_CAP`과 함께 R3 Loop 12의 15개 target을 구성한다.

## Stage Logic

Round 187 기본 점수축은 7개로 정리했다.

- EPS/FCF·OPM 전환: 24
- 계약·고객·가동률 visibility: 22
- CAPA 재배치 / 라인 전환: 12
- 정책·보조금 이익 품질: 10
- 가격경로 조기검증: 10
- 안전·규제·품질·공시 신뢰도: 12
- valuation room / 4B 여지: 10

Stage 3 조기 포착은 8개 중 5개 이상을 요구한다. Stage 4B는 6개 중 4개 이상으로 조기 전환하고, 대형 고객 계약 취소, EV 모델 취소, 공장 가동률 붕괴, 보조금 제외 이익 붕괴, UFLPA 통관 차단, 풍력 permit/lease halt, 배터리 화재·사망 사고, 공급사 공시 신뢰도 문제는 hard 4C gate로 기록했다.

## Case Counts

- target_count: 15
- case_candidate_count: 17
- success_candidate_count: 8
- failed_rerating_count: 2
- stage4b_case_count: 1
- stage4c_case_count: 6
- hard_gate_target_count: 4

## Guardrails

- Stage 3-Green threshold는 낮추지 않았다.
- EV, ESS, 수소, 태양광, 풍력, 재활용, sodium-ion 키워드만으로 Green을 만들지 않는다.
- ESS 전환과 보조금 이익은 보조금 제외 OPM, 가동률, FCF 확인 전까지 cap 처리한다.
- 태양광 미국 내재화는 통관/UFLPA와 정상 가동이 확인되기 전까지 cap 처리한다.
- 풍력 수주는 permit/lease halt가 있으면 hard policy overlay로 막는다.
- 배터리 화재, 사망 사고, 품질 실패, 공급사 공시 신뢰도 문제는 RedTeam hard overlay로 남긴다.
- 없는 계약금액, 가격, 가동률, 보조금 제외 이익, MFE/MAE, 안전 회복 여부는 만들지 않는다.

## Commands

```bash
PYTHONPATH=src python -m unittest tests/test_round187_r3_loop12_battery_ev_green.py -v
PYTHONPATH=src python -m e2r.cli.build_round187_r3_loop12_report
```

## Next

다음 라운드도 같은 방식으로 case library를 확장한다. 충분한 성공/반례 coverage와 가격 경로가 쌓일 때까지 production scoring weight는 적용하지 않는다.

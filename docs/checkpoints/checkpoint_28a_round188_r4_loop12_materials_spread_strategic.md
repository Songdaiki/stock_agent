# Checkpoint 28A Round 188: R4 Loop 12 Materials / Spread / Strategic Resources

## Summary

Round 188 반영을 완료했다. 이번 라운드는 국장 R4 대섹터에서 정유 spread 반등, 석유화학 구조조정, NCC capacity cut, Shaheen 신규 CAPA 위험, 합성고무 반덤핑, 타이어 생산차질을 별도 calibration pack으로 구조화했다.

이 패치는 생산 scoring/staging을 바꾸지 않는다. 케이스 레코드는 calibration/evaluation material이며 candidate-generation input이 아니다.

쉬운 예시는 이렇다. `정제마진 반등`은 Stage 2 후보 근거가 될 수 있지만, 재고손익 제외 OP, FCF, 배터리·석화 drag 축소가 확인되기 전에는 Stage 3-Green으로 올리지 않는다.

## Files Added

- `src/e2r/sector/round188_r4_loop12_materials_spread_strategic.py`
- `src/e2r/cli/build_round188_r4_loop12_report.py`
- `tests/test_round188_r4_loop12_materials_spread_strategic.py`
- `data/e2r_case_library/cases_r4_loop12_round188.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round188_r4_loop12_v12.csv`
- `output/e2r_round188_r4_loop12_materials_spread_strategic/*`

## Archetypes Added

Round 188에서 새 canonical archetype을 추가했다.

- `REFINING_SPREAD_TURNAROUND_KOREA`
- `REFINING_PETCHEM_MIX_DRAG`
- `PETROCHEMICAL_RESTRUCTURING_KOREA`
- `NCC_CAPACITY_CUT_STAGE2`
- `NCC_OVERLOAD_SHAHEEN_RISK`
- `SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING`
- `SYNTHETIC_RUBBER_TARIFF_RISK`
- `TIRE_RUBBER_PRODUCTION_DISRUPTION`
- `COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL`

기존 `DISCLOSURE_CONFIDENCE_CAP`과 함께 R4 Loop 12의 10개 target을 구성한다.

## Stage Logic

Round 188 기본 점수축은 7개로 정리했다.

- EPS/FCF·OPM 전환 가능성: 22
- spread·제품마진 지속성: 18
- 구조조정·공급감축 visibility: 18
- 가격경로 조기검증: 10
- cycle / commodity risk: 12
- 운영·생산·관세·disclosure RedTeam: 12
- valuation room / 4B 여지: 8

Stage 3 조기 포착은 8개 중 5개 이상을 요구한다. Stage 4B는 6개 중 4개 이상으로 조기 전환하고, 공장 화재·생산중단, 구조조정 실패, 신규 CAPA 공급과잉, 중국 공급과잉, 반덤핑 관세, 재고손실, spread 급락, 정유 이익을 잠식하는 배터리·석화 drag는 hard gate 또는 cap으로 기록했다.

## Case Counts

- target_count: 10
- case_candidate_count: 10
- success_candidate_count: 4
- failed_rerating_count: 3
- stage4b_case_count: 1
- stage4c_case_count: 2
- hard_gate_target_count: 2

## Guardrails

- Stage 3-Green threshold는 낮추지 않았다.
- 정제마진, 석화 구조조정, 관세, 원자재 가격, 공장 뉴스만으로 Green을 만들지 않는다.
- NCC capacity cut은 Stage 2 strong일 수 있지만, spread·가동률·OP·FCF 회복 전에는 Green 금지다.
- LG화학 NAV/행동주의/지분매각은 Stage 2 option이고, 실제 환원·부채감소·FCF 전에는 Green 금지다.
- S-Oil Shaheen처럼 공급과잉 구간에서 신규 CAPA가 들어오면 RedTeam capacity-addition overlay로 둔다.
- 금호타이어 공장 화재처럼 20% capacity가 흔들리는 사건은 hard 4C로 둔다.
- 없는 spread, capacity cut 금액, OPM, FCF, stage price, 구조조정 세부안은 만들지 않는다.

## Commands

```bash
PYTHONPATH=src python -m unittest tests/test_round188_r4_loop12_materials_spread_strategic.py -v
PYTHONPATH=src python -m e2r.cli.build_round188_r4_loop12_report
```

## Next

다음 라운드도 같은 방식으로 case library를 확장한다. 충분한 성공/반례 coverage와 가격 경로가 쌓일 때까지 production scoring weight는 적용하지 않는다.

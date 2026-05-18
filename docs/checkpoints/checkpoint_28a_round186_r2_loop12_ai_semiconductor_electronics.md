# Checkpoint 28A Round 186: R2 Loop 12 AI / Semiconductor / Electronics

## Summary

Round 186 반영을 완료했다. 이번 라운드는 국장 R2 대섹터에서 기존 Loop 11의 핵심 이름 반복을 줄이고, 다음 후보군을 별도 calibration pack으로 구조화했다.

- SKC/Absolics 유리기판
- 가온칩스 시스템반도체 디자인하우스
- 테크윙·와이씨·디아이·엑시콘 HBM 테스트 장비 basket
- 한화정밀기계 / 한화 산업솔루션 spin-off
- 삼성전기·LG이노텍
- 대덕전자·심텍·코리아써키트·티엘비 PCB/substrate basket
- 제주반도체·칩스앤미디어·텔레칩스·넥스트칩 on-device AI basket

이 패치는 생산 scoring/staging을 바꾸지 않는다. 케이스 레코드는 calibration/evaluation material이며 candidate-generation input이 아니다.

## Files Added

- `src/e2r/sector/round186_r2_loop12_ai_semiconductor_electronics.py`
- `src/e2r/cli/build_round186_r2_loop12_report.py`
- `tests/test_round186_r2_loop12_ai_semiconductor_electronics.py`
- `data/e2r_case_library/cases_r2_loop12_round186.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round186_r2_loop12_v12.csv`
- `output/e2r_round186_r2_loop12_ai_semiconductor_electronics/*`

## Archetypes Added

Round 186에서 새 canonical archetype을 추가했다.

- `GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA`
- `SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER`
- `ADVANCED_PACKAGING_EQUIPMENT_BASKET`
- `AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE`
- `MLCC_AI_SERVER_COMPONENTS`
- `CAMERA_LIDAR_ADAS_ELECTRONICS`
- `ON_DEVICE_AI_THEME_KOREA`
- `SEMI_CAPEX_ORDER_TO_REVENUE`
- `IP_LEAK_SUPPLY_CHAIN_REDTEAM`
- `LABOR_PRODUCTION_DISRUPTION_OVERLAY`

예를 들면 `가온칩스`는 “AI칩 설계 참여”만으로 Green이 아니라, 고객명·기술노드 확인은 Stage 2 근거이고 order size·매출 인식·반복 design win·OP/EPS가 Stage 3 gate다.

## Stage Logic

Round 186 기본 점수축은 7개로 정리했다.

- EPS/FCF·OPM 전환: 24
- 고객·계약·출하 visibility: 22
- 병목·공정·기술 채택: 16
- 가격경로 조기검증: 12
- 양산·수율·고객다변화: 8
- IP·노동·보안·공시 RedTeam: 10
- valuation room / 4B 여지: 8

Stage 3 조기 포착은 8개 중 5개 이상을 요구한다. Stage 4B는 6개 중 4개 이상으로 조기 전환하고, IP 유출·생산 차질·고객 CAPEX 지연·양산 지연·공시 문제는 hard 4C gate로 기록했다.

## Case Counts

- target_count: 12
- case_candidate_count: 13
- success_candidate_count: 7
- failed_rerating_count: 3
- stage4b_case_count: 1
- stage4c_case_count: 2
- hard_gate_target_count: 2

## Guardrails

- Stage 3-Green threshold는 낮추지 않았다.
- AI/HBM/유리기판/NPU 키워드만으로 Green을 만들지 않는다.
- MOU, media report, design win headline, OpenDART list-only evidence는 customer/order/shipment/margin detail 전까지 cap 처리한다.
- 고객명, 계약금액, order size, 수율, 출하, MFE/MAE, valuation band는 없는 값을 만들지 않는다.

## Commands

```bash
PYTHONPATH=src python -m unittest tests/test_round186_r2_loop12_ai_semiconductor_electronics.py -v
PYTHONPATH=src python -m e2r.cli.build_round186_r2_loop12_report
```

## Next

다음 라운드도 같은 방식으로 case library를 확장한다. 충분한 성공/반례 coverage와 가격 경로가 쌓일 때까지 production scoring weight는 적용하지 않는다.

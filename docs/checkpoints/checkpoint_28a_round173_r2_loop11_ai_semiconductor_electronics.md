# Checkpoint 28A Round 173: R2 Loop 11 Korea AI / Semiconductor / Electronics

## 목적

`docs/round/round_173.md`의 R2 Loop 11 내용을 calibration pack으로 반영했다.
이번 라운드는 국장 AI·반도체·전자부품을 HBM 본체가 아니라 장비, 후공정, PCB, 테스트, 시스템반도체 option, private AI-chip 관련주까지 넓혀서 본다.

핵심 질문은 두 가지다.

1. 한미반도체, 이수페타시스, 리노공업 같은 대폭 상승 후보를 상승 전에 Stage 3 후보로 포착할 수 있었는가?
2. 이미 300~500% 또는 70% 이상 오른 뒤에는 Stage 4B로 식힐 수 있는가?

쉬운 예로, 한미반도체는 SK하이닉스 계약처럼 확인된 고객·금액이 있으면 Stage 2/3 후보가 될 수 있다.
하지만 Micron 가능성 보도처럼 `if finalized` 성격이면, 가격이 움직여도 Stage 3-Green은 확정계약·납품·OP/EPS 확인 전까지 막는다.

## 반영 파일

- `src/e2r/sector/round173_r2_loop11_ai_semiconductor_electronics.py`
- `src/e2r/cli/build_round173_r2_loop11_report.py`
- `tests/test_round173_r2_loop11_ai_semiconductor_electronics.py`
- `data/e2r_case_library/cases_r2_loop11_round173.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round173_r2_loop11_v11.csv`
- `output/e2r_round173_r2_loop11_ai_semiconductor_electronics/`

## Loop 11 target

원문 canonical target 10개와 보조 hard gate 2개를 분리했다.

| target | 역할 |
| --- | --- |
| `HBM_BONDER_EQUIPMENT_KOREA` | 한미반도체형 HBM TC bonder / packaging 장비 |
| `ADVANCED_PACKAGING_EQUIPMENT_KOREA` | 후공정 장비, 고객 주문·출하 전환 확인 |
| `AI_SERVER_PCB_MLB_KOREA` | 이수페타시스형 AI 서버 PCB / 고다층 MLB |
| `SEMICONDUCTOR_TEST_SOCKET_KOREA` | 리노공업·ISC형 test socket / probe pin |
| `HBM_TEST_EQUIPMENT_KOREA` | 테크윙·디아이·와이씨형 HBM test 장비 |
| `SYSTEM_SEMI_FOUNDARY_OPTION_KOREA` | DB하이텍형 정책 foundry / ReRAM option |
| `AI_CHIP_FABRIC_PRIVATE_RELATED` | 리벨리온·사피온 private AI-chip 생태계 관련주 |
| `ON_DEVICE_AI_THEME` | 온디바이스 AI theme, 실매출 전 Green 금지 |
| `MOU_OR_REPORT_NOT_CONTRACT` | 보도·협의·MOU는 확정계약 전 Stage 3 금지 |
| `DISCLOSURE_CONFIDENCE_CAP` | 고객·금액·기간·마진 detail 부족 시 cap |
| `HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY` | 삼성 파업·생산차질 hard RedTeam overlay |
| `AI_CHIP_LISTED_EARNINGS_LINK_GATE` | private valuation과 상장사 EPS 연결 분리 |

## R2 Loop 11 기본 점수축

| component | points |
| --- | ---: |
| EPS/FCF/OPM conversion | 24 |
| customer/contract/shipment visibility | 22 |
| bottleneck/pricing power | 18 |
| early price-path validation | 12 |
| information confidence / disclosure detail | 8 |
| capital discipline / FCF stability | 6 |
| valuation room / 4B runway | 10 |

이번 라운드는 `고객명·계약금액·출하·반복수주·OP/EPS·가격경로`를 강하게 본다.
예를 들어 “AI 서버 PCB”라는 이름만으로는 Stage 1이다.
하지만 고객 수주, 고다층 MLB 매출, OP/EPS revision, Stage 2 이후 60D MFE가 같이 있으면 Stage 3 후보가 된다.

## 케이스 요약

| case | 판정 |
| --- | --- |
| 한미반도체 | HBM 장비 Stage 3 후보 + Micron 보도 cap + 4B-watch |
| 이수페타시스 | AI 서버 PCB 성공 경로, 487% 급등 이후 4B-watch |
| 리노공업 | test socket quality Stage 2.5, 고객·OP/EPS detail 전 Green 금지 |
| DB하이텍 | 정책 foundry / ReRAM option Stage 1~2, wafer revenue 전 Green 금지 |
| 리벨리온·사피온 관련주 | private AI-chip ecosystem event, 상장사 직접 EPS 연결 전 Green 금지 |
| 한미 Micron 보도 | media report / possible deal은 Stage 2 보조, 확정계약 전 cap |
| 삼성 파업 risk | HBM supply chain 운영 리스크 hard overlay |
| 온디바이스 AI 관련주 | design-win revenue 전 theme cap |
| HBM test 장비 | 고객 주문·출하·OP/EPS 전 Stage 2 watch |
| 후공정 장비 | 고객 주문·출하·매출 전환 전 watch |
| AI-chip earnings-link gate | private valuation과 listed EPS 분리 hard gate |

## 산출 요약

| 항목 | 값 |
| --- | ---: |
| target | 12 |
| source canonical target | 10 |
| case candidate | 11 |
| base score component | 7 |
| stage cap | 6 |
| score-stage-price alignment | 10 |
| structural success | 1 |
| success candidate | 4 |
| event premium | 3 |
| Stage 4B case | 1 |
| Stage 4C case | 2 |
| Green possible target | 2 |
| hard gate target | 3 |

## 핵심 가드레일

- Round 173 case pack은 candidate generation input이 아니다.
- production scoring/staging/RedTeam 로직은 변경하지 않았다.
- Stage 3-Green은 HBM, AI 서버, PCB, 테스트 소켓, NPU 같은 이름이 아니라 고객·계약·출하·매출·OP/EPS·가격경로가 맞을 때만 가능하다.
- media report, MOU, private valuation, policy option, government investment, on-device AI theme은 단독으로 Green을 만들 수 없다.
- 리벨리온·사피온 같은 private AI-chip 이벤트는 상장사 직접 매출 또는 지분법이익이 확인되기 전까지 관련주 Green으로 번역하지 않는다.
- 주가 300~500% 급등, 120D MFE +80%, narrative crowding은 4B-watch를 강하게 요구한다.
- 삼성 파업·생산차질, 고객 주문 취소, 대규모 희석, 공시 detail 부족, 직접 EPS 연결 부재는 hard RedTeam으로 둔다.

## 산출물

- `round173_r2_loop11_ai_semiconductor_electronics_summary.md`
- `round173_r2_loop11_case_matrix.csv`
- `round173_r2_loop11_stage_date_plan.csv`
- `round173_r2_loop11_green_guardrails.md`
- `round173_r2_loop11_risk_overlays.md`
- `round173_r2_loop11_price_validation_plan.md`
- `round173_r2_loop11_price_fields.csv`
- `round173_r2_loop11_base_score_weights.csv`
- `round173_r2_loop11_stage_caps.csv`
- `round173_r2_loop11_score_stage_price_alignment.csv`
- `round173_r2_loop11_score_stage_price_alignment.md`

## 검증

- `PYTHONPATH=src python -m e2r.cli.build_round173_r2_loop11_report` 통과.
- `PYTHONPATH=src python -m unittest tests/test_round173_r2_loop11_ai_semiconductor_electronics.py -v` 통과.
- `PYTHONPATH=src python -m compileall -q src tests` 통과.
- `PYTHONPATH=src python -m unittest discover -s tests -v` 통과. `2228 tests`.
- `git diff --check` 통과.

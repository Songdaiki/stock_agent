# Checkpoint 28A Round 175: R4 Loop 11 Korea Materials / Spreads / Strategic Resources

## 목적

`docs/round/round_175.md`의 R4 Loop 11 내용을 calibration pack으로 반영했다.
이번 라운드는 국장 구리·전선, 풍산 구리/탄약, OCI 폴리실리콘, 철강 관세, 리튬·희토류 테마, 화학 spread를 다룬다.

핵심은 “원자재 가격이 올랐다”가 아니라 “그 가격 변화가 실제 OP/EPS/FCF로 고정되는가”다.
예를 들어 구리 가격이 급등해도 LS·대한전선·가온전선·풍산이 Stage 3가 되려면 개별 수주, 가격전가, OPM, FCF가 보여야 한다.

## 반영 파일

- `src/e2r/sector/round175_r4_loop11_materials_spread_strategic.py`
- `src/e2r/cli/build_round175_r4_loop11_report.py`
- `tests/test_round175_r4_loop11_materials_spread_strategic.py`
- `data/e2r_case_library/cases_r4_loop11_round175.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round175_r4_loop11_v11.csv`
- `output/e2r_round175_r4_loop11_materials_spread_strategic/`

## R4 Loop 11 Target

| target | 역할 |
| --- | --- |
| `COPPER_AI_GRID_KOREA` | LS·대한전선·가온전선·풍산류 구리/전력망 macro bottleneck |
| `COPPER_PROCESSING_PLUS_DEFENSE` | 풍산 구리 가공 + 탄약 구조 후보 |
| `DEFENSE_AMMO_EVENT_PREMIUM` | 풍산 방산 M&A rumor / event premium cap |
| `POLYSILICON_NON_CHINA_SUPPLY_OPTION` | OCI홀딩스 비중국 폴리실리콘 option |
| `POLYSILICON_REPORT_NOT_CONTRACT` | SpaceX 협의 보도 같은 report-not-contract hard cap |
| `STEEL_TARIFF_EVENT_KOREA` | POSCO·현대제철·KG스틸 관세 방향성 이벤트 |
| `STEEL_EXPORT_TARIFF_4C` | 세아제강형 미국 수출관세 직격 4C |
| `SPECIALTY_STEEL_US_LOCALIZATION_OPTION` | 세아제강지주·세아베스틸지주형 미국 현지화 option |
| `LITHIUM_PRICE_EVENT_KOREA` | POSCO홀딩스·금양·하이드로리튬류 리튬 가격 이벤트 |
| `RARE_EARTH_THEME_KOREA` | 유니온머티리얼·티플랙스류 희토류 theme cap |
| `CHEMICAL_SPREAD_KOREA` | 롯데정밀화학·한화솔루션·OCI 일부 화학 spread watch |
| `EVENT_PREMIUM_GOVERNANCE_OVERLAY` | M&A·거버넌스 이벤트 premium 분리 |
| `DISCLOSURE_CONFIDENCE_CAP` | 고객·금액·기간·물량·마진 미공개 cap |

## 기본 점수축

| component | points |
| --- | ---: |
| EPS/FCF/OPM conversion | 22 |
| contract/offtake/customer visibility | 20 |
| bottleneck/pricing power | 16 |
| early price-path validation | 12 |
| cycle/spread durability | 12 |
| disclosure confidence / RedTeam | 10 |
| valuation room / 4B runway | 8 |

R4는 가격 이벤트가 많기 때문에 가격 상승이 곧 Stage 3 증거가 아니다.
예를 들어 희토류 수출통제 뉴스로 종목이 급등해도 실제 희토류 매출, offtake, 생산량, FCF가 없으면 Stage 1 또는 4B-watch로 식힌다.

## 케이스 요약

| case | 판정 |
| --- | --- |
| 구리·전선 basket | AI-grid macro는 Stage 1~2 강함. 개별 수주·OPM 전 Stage 3 제한 |
| 풍산 | 구리+탄약 Stage 2 후보. 한화 검토 중단·매각 부인 시 4C-watch |
| OCI홀딩스 | 비중국 폴리실리콘/SpaceX 협의는 Stage 1~2 option. 확정계약 전 cap |
| 철강 관세 방향성 | 중국산 견제 관세와 전면 수입관세를 분리해야 함 |
| 세아제강 | 미국 50% 철강 관세에서 직접 수출관세 4C price-path |
| Specialty steel localization | 미국 현지화 option. 실제 현지 매출·마진 전 Stage 3 제한 |
| 리튬·희토류 테마 | price-only event rally. 실제 생산·offtake·FCF 전 Green 금지 |
| 화학 spread | durable spread, volume, OPM, FCF 전 Watch/Red |
| 공시 신뢰도 cap | headline/report/list evidence는 detail fetch 전 Stage 3 제한 |

## 산출 요약

| 항목 | 값 |
| --- | ---: |
| target | 13 |
| source canonical target | 13 |
| case candidate | 10 |
| base score component | 7 |
| stage cap | 5 |
| score-stage-price alignment | 10 |
| structural success | 0 |
| success candidate | 2 |
| event premium | 3 |
| overheat | 1 |
| failed rerating | 2 |
| Stage 4C case | 2 |
| Green possible target | 0 |
| hard gate target | 6 |

## 핵심 가드레일

- Round 175 case pack은 candidate generation input이 아니다.
- production scoring/staging/RedTeam 로직은 변경하지 않았다.
- Stage 3-Green은 구리·철강·리튬·희토류·폴리실리콘 이름이 아니라 계약금액, 고객명, 공급기간, offtake, price floor, 회사 확인 여부, 판매량, OPM, FCF로 판단한다.
- 관세 이벤트는 반드시 대상과 범위를 분해한다. 중국산 견제 관세와 한국산 포함 전면 수입관세는 반대 신호가 될 수 있다.
- M&A rumor는 본계약 전 event premium이고, 검토 중단·매각 부인은 4C-watch다.
- media report-only와 company confirmation missing은 Stage 3-Green을 막는다.
- stage price, MFE/MAE, 원자재 가격 노출, 계약 조건은 없으면 비워둔다.

## 산출물

- `round175_r4_loop11_materials_spread_strategic_summary.md`
- `round175_r4_loop11_case_matrix.csv`
- `round175_r4_loop11_stage_date_plan.csv`
- `round175_r4_loop11_green_guardrails.md`
- `round175_r4_loop11_risk_overlays.md`
- `round175_r4_loop11_price_validation_plan.md`
- `round175_r4_loop11_price_fields.csv`
- `round175_r4_loop11_base_score_weights.csv`
- `round175_r4_loop11_stage_caps.csv`
- `round175_r4_loop11_score_stage_price_alignment.csv`
- `round175_r4_loop11_score_stage_price_alignment.md`

## 검증

- `PYTHONPATH=src python -m e2r.cli.build_round175_r4_loop11_report` 통과.
- `PYTHONPATH=src python -m unittest tests.test_round175_r4_loop11_materials_spread_strategic -v` 통과. `13 tests`.
- `PYTHONPATH=src python -m compileall -q src tests` 통과.
- `PYTHONPATH=src python -m unittest discover -s tests -v` 통과. `2254 tests`.
- `git diff --check` 통과.

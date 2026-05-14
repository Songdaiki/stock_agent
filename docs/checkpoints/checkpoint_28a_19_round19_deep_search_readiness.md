# Checkpoint 28A Round 19: Deep Search Readiness

## 목적

Round 19는 production scoring을 바꾸는 단계가 아니다.

이번 단계의 목적은:

- 테마 태그 흡수 구조가 충분히 동작하는지 확인한다.
- 어떤 archetype이 아직 성공/반례 case가 부족한지 드러낸다.
- 어떤 archetype은 case 수는 있어도 주가 경로 검증이 부족한지 드러낸다.
- 다음 딥서치 라운드의 우선순위를 만든다.

쉬운 예시:

- `스테이블코인`은 테마맵에 들어갔다. 그래서 검색/라우팅은 가능하다.
- 하지만 실제 규제 승인, 거래량, 수익모델, 현금흐름 증거가 없으면 Stage 3-Green 근거가 아니다.
- 즉, “분류됨”과 “점수화 가능”은 다르다.

## 구현

추가한 파일:

- `src/e2r/sector/round19_deep_search_readiness.py`
- `src/e2r/cli/build_round19_deep_search_readiness_report.py`
- `tests/test_round19_deep_search_readiness.py`

입력:

- `docs/round/r_19.md`
- `data/e2r_case_library/cases_v03_price_filled.jsonl`
- `data/sector_taxonomy/raw_theme_tags_v05.csv`
- `data/sector_taxonomy/theme_tag_map_v05.csv`

출력:

- `output/e2r_round19_deep_search_readiness/round19_deep_search_readiness.md`
- `output/e2r_round19_deep_search_readiness/round19_undercovered_archetype_priority.csv`
- `output/e2r_round19_deep_search_readiness/round19_deep_search_plan.csv`
- `output/e2r_round19_deep_search_readiness/round19_price_validation_gap.csv`
- `output/e2r_round19_deep_search_readiness/round19_production_scoring_blockers.md`

## 결과

현재 산출 결과:

- raw_theme_tags: 208
- mapped_theme_tags: 208
- unmatched_theme_tags: 0
- ambiguous_theme_tags: 6
- theme_absorption_ready: true
- case_count: 108
- deep_search_targets: 25
- targets_needing_deep_search: 17
- targets_needing_price_validation: 8
- targets_ready_for_shadow_review: 0
- production_scoring_changed: false
- production_scoring_ready: false

해석:

- 테마 흡수는 잘 된다.
- 하지만 case coverage와 price-path validation이 아직 부족하다.
- 따라서 `score_weight_profiles_v05`를 production scoring에 연결하면 안 된다.

## 우선순위

Green 검증이 더 필요한 영역:

- K뷰티 OEM/ODM export
- 의료기기 수출
- CDMO 계약/가동률
- 보험 underwriting / 금융 value-up
- AI 데이터센터 전력망
- 반도체 장비/PCB

Green 오판 방어가 더 중요한 영역:

- 2차전지 EV overheat / ESS 전환
- 화학 spread oversupply
- 건설 PF credit
- 해운 freight boom-bust
- 디지털자산/STO
- 로봇 매출 전환
- 플랫폼 거버넌스/수익화

얇은 archetype backfill:

- WASTE_RECYCLING_ENVIRONMENT
- CRO_CLINICAL_SERVICE
- DIGITAL_HEALTHCARE_AI
- SECURITY_IDENTITY_DEEPFAKE
- CLOUD_AI_SOFTWARE_INFRA
- APPAREL_BRAND_OEM
- BUILDING_MATERIALS_CYCLE
- REIT_DEVELOPMENT_TRUST
- RAIL_INFRASTRUCTURE
- SERVICE_KIOSK_AUTOMATION
- URBAN_AIR_DRONE

## 바꾸지 않은 것

- `features.py` 변경 없음
- `staging.py` 변경 없음
- `red_team.py` 변경 없음
- production `StageClassifier` threshold 변경 없음
- case library를 candidate-generation input으로 사용하지 않음
- raw theme tag를 score evidence로 사용하지 않음

## 실행 명령

```bash
PYTHONPATH=src python -m e2r.cli.build_round19_deep_search_readiness_report \
  --case-library data/e2r_case_library/cases_v03_price_filled.jsonl \
  --raw-tags data/sector_taxonomy/raw_theme_tags_v05.csv \
  --theme-map data/sector_taxonomy/theme_tag_map_v05.csv \
  --output-directory output/e2r_round19_deep_search_readiness
```

테스트:

```bash
PYTHONPATH=src python -m unittest tests.test_round19_deep_search_readiness -v
PYTHONPATH=src python -m unittest discover -s tests -v
```

## 다음 단계

다음은 production score 적용이 아니라 딥서치 보강이다.

1. `round19_undercovered_archetype_priority.csv`의 `needs_success_counterexample_deep_search` 항목부터 본다.
2. 각 target에 성공 case와 반례 case를 추가한다.
3. stage date와 price path를 채운다.
4. shadow score와 실제 price path가 맞는지 비교한다.
5. 그 뒤에도 충분한 archetype만 score-weight 적용 후보로 올린다.

핵심 원칙:

> 테마는 책장 분류표이고, 점수는 책의 실제 내용이다.
> 분류표가 완성됐다고 책 내용을 읽은 것은 아니다.

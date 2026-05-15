# Checkpoint 28A Round 39: Taxonomy Consolidation

## 목적

Round 39는 새 production scoring을 추가하는 라운드가 아니다. 지금까지 진행한 라운드를 계층으로 정리한다.

핵심은 간단하다.

예를 들어 `AI·반도체·전자부품`이라는 큰 서랍은 유지한다. 그 아래에서 `HBM`, `AI server ODM`, `neocloud`, `CoWoS`, `optical networking`, `industrial gases`, `AI data-center power equipment`처럼 점수 구조가 다른 하위 렌즈를 붙인다. 이렇게 해야 “AI 테마니까 점수”가 아니라 “어떤 경제 구조가 EPS/FCF를 바꾸는가”를 따질 수 있다.

## 반영 파일

- `src/e2r/sector/round39_taxonomy_consolidation.py`
- `src/e2r/cli/build_round39_taxonomy_consolidation_report.py`
- `tests/test_round39_taxonomy_consolidation.py`
- `data/sector_taxonomy/round39_deep_sub_archetype_registry.csv`
- `output/e2r_round39_taxonomy_consolidation/round39_taxonomy_consolidation_summary.md`
- `output/e2r_round39_taxonomy_consolidation/round39_large_sector_hierarchy.csv`
- `output/e2r_round39_taxonomy_consolidation/round39_layer_model.md`
- `output/e2r_round39_taxonomy_consolidation/round39_green_policy_rollup.md`
- `output/e2r_round39_taxonomy_consolidation/round39_price_validation_next_steps.md`

## 요약

- large_sector_count: 12
- base_theme_archetype_count: 65
- deep_sub_archetype_count: 41
- combined_view_count: 106
- green_possible_deep_count: 15
- watch_yellow_first_deep_count: 19
- redteam_first_deep_count: 7
- production_scoring_changed: false
- deep_sub_archetypes_are_candidate_generation_input: false

## 계층 모델

1. Raw theme tag: HBM, K푸드, 방산, 스테이블코인, 초전도체 같은 시장 테마명
2. Large sector: 12개 대섹터
3. Base theme archetype: Round-10 테마맵의 65개 기본 분류
4. Deep sub-archetype: 이후 라운드에서 추가된 세부 렌즈
5. Case library: 성공, 반례, 4B, 4C 사례
6. Price-path validation: stage date, MFE/MAE, drawdown, score-price alignment

## 핵심 판단

- 대섹터는 12개로 고정한다.
- 새 테마가 나올 때마다 대섹터를 늘리지 않는다.
- deep sub-archetype은 parent large sector와 canonical archetype 아래에 붙인다.
- deep sub-archetype label은 후보 생성 근거가 아니다.
- 예: `AI_SERVER_ODM_EMS_SUPPLY_CHAIN`은 AI 인프라 렌즈지만, 실제 점수에는 rack shipment, OP/EPS, margin, inventory, customer concentration, audit trust evidence가 필요하다.

## 다음 작업

- cases_vXX를 parent/sub-archetype별로 정렬한다.
- stage date 후보와 OHLCV 경로를 source data로만 backfill한다.
- MFE/MAE/drawdown을 계산한다.
- Green 가능 축과 Watch/Red 축의 score-price alignment를 비교한다.
- 검증 전까지 production scoring threshold를 바꾸지 않는다.

## 실행 명령

```bash
PYTHONPATH=src python -m unittest tests.test_round39_taxonomy_consolidation -v
PYTHONPATH=src python -m e2r.cli.build_round39_taxonomy_consolidation_report
```

## 테스트 상태

라운드 39 전용 테스트는 통과했다. 전체 테스트는 기존에 삭제된 Round 17 문서 상태 때문에 별도 확인이 필요하다.

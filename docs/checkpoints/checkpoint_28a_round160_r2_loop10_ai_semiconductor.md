# Checkpoint 28A Round 160 R2 Loop 10 AI Semiconductor Electronics

## 목적

`docs/round/round_160.md`의 R2 Loop 10 내용을 캘리브레이션 팩으로 반영했다.

이번 라운드의 핵심은 `AI 수혜주`라는 이름표와 실제 E2R 증거를 분리하는 것이다.

쉬운 예:

```text
HBM shortage 뉴스
-> Stage 1 가능

고객명·출하·매출 가이던스 확인
-> Stage 2 가능

OP/EPS/FCF 상향 + 마진/자본환원 + 가격경로 동행
-> Stage 3 후보 가능

이미 1~2년 급등해 모두가 인정
-> 4B-watch

감사인 사임·공시지연·순환금융·고부채
-> 4C 또는 hard RedTeam
```

## 반영 내용

- `src/e2r/sector/round160_r2_loop10_ai_semiconductor.py` 추가
- `src/e2r/cli/build_round160_r2_loop10_report.py` 추가
- `tests/test_round160_r2_loop10_ai_semiconductor.py` 추가
- R2 Loop 10 전용 case pack과 score profile 생성
- 원문 21개 핵심 target에 기존 R2 보조 overlay/인접 target 6개를 더해 총 27개 target으로 분리 유지

쉬운 예:

```text
원문 target: HBM LTA/prepayment
보조 overlay: circular AI financing

둘 다 AI 인프라와 관련 있지만,
전자는 Green 후보 visibility이고 후자는 RedTeam hard review다.
한 바구니로 섞으면 점수표가 위험해진다.
```

## 핵심 축

- `MEMORY_HBM_CAPACITY`: Green 가능성이 높지만 4B 감시 필수
- `HBM_CATCHUP_EXECUTION`: 출하는 Stage 2, qualification/yield/volume/EPS 전까지 Green 금지
- `AI_STORAGE_NAND_SHORTAGE`: profit explosion은 강하지만 10~20배 가격경로면 4B 강함
- `SEMI_EQUIPMENT_AI_CAPEX`: 장비 guidance는 강하지만 order pushout/export control 감시
- `CUSTOM_AI_ASIC_HYPERSCALER`: 고객명·capacity·margin·repeat revenue 필요
- `AI_SERVER_ODM_EMS_SUPPLY_CHAIN`: 매출 증가는 인정하되 margin/working capital cap
- `NEOCLOUD_GPU_RENTAL`: 계약 visibility가 있어도 FCF/debt/GPU depreciation 통과 전 Green 금지
- `REDTEAM_ACCOUNTING_TRUST_OVERLAY`: Supermicro식 감사·공시 신뢰 훼손은 hard gate
- `CIRCULAR_AI_FINANCING_OVERLAY`: 공급자·고객·투자자 순환구조는 clean demand가 아님

## v10 기본 점수표

- EPS/FCF revision: 25
- 고객·출하·매출 visibility: 22
- 병목·가격결정력: 19
- 정보 신뢰도 / disclosure detail: 10
- capital discipline / FCF 안정성: 8
- 시장 오해·리레이팅 gap: 8
- valuation room / 4B 여지: 8

## 산출물

- `data/e2r_case_library/cases_r2_loop10_round160.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round160_r2_loop10_v10.csv`
- `output/e2r_round160_r2_loop10_ai_semiconductor/round160_r2_loop10_ai_semiconductor_summary.md`
- `output/e2r_round160_r2_loop10_ai_semiconductor/round160_r2_loop10_case_matrix.csv`
- `output/e2r_round160_r2_loop10_ai_semiconductor/round160_r2_loop10_score_stage_price_alignment.md`

## 산출 요약

- target_count: 27
- source_target_count: 21
- helper_overlay_target_count: 6
- case_candidate_count: 24
- score_stage_price_alignment_count: 12
- green_possible_count: 6
- watch_yellow_first_count: 15
- redteam_first_count: 6
- hard_gate_target_count: 3

예를 들면 `MEMORY_HBM_LTA_PREPAYMENT`는 Green 후보 visibility 축이지만,
`CIRCULAR_AI_FINANCING_OVERLAY`는 같은 AI 인프라 맥락이어도 RedTeam 축이다.
그래서 source target 21개에 보조 overlay 6개를 더해 27개로 분리했다.

## 안전장치

- production scoring은 변경하지 않았다.
- case records는 candidate-generation input이 아니다.
- CXL, 유리기판, 뉴로모픽, AI chip 관련주 이름만으로 Green을 만들지 않는다.
- 고객명, 계약금액, 출하량, margin, yield, FCF, stage price는 없는 값을 만들지 않는다.

## 검증

```bash
PYTHONPATH=src python -m unittest tests/test_round160_r2_loop10_ai_semiconductor.py -v
PYTHONPATH=src python -m e2r.cli.build_round160_r2_loop10_report
```

두 명령 모두 통과했다.

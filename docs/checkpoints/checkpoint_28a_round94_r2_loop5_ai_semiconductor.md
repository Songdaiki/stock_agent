# Checkpoint 28A Round 94: R2 Loop 5 AI / Semiconductor / Electronics

## 목적

`round_94.md`는 R2 AI·반도체·전자부품 팩을 Loop 5 기준으로 확장한다. 이번 작업은 생산 점수를 바꾸는 것이 아니라, AI 수혜를 하나의 점수축으로 뭉개지 않기 위해 HBM, 후발 HBM, AI storage NAND, 장비, 패키징, 광통신, AI networking, photonics, 서버 ODM, neocloud, 냉각, AI accelerator, 회계 신뢰도, 순환금융을 따로 분리한 calibration 팩이다.

쉬운 예시는 다음과 같다. `OpenAI와 대형 계약`은 GPU cloud 회사의 Stage 2 visibility는 될 수 있다. 하지만 부채, FCF 적자, GPU 감가상각, 고객집중이 해결되지 않으면 Stage 3-Green 근거가 아니다.

## 반영 내용

- `src/e2r/sector/round94_r2_loop5_ai_semiconductor.py` 추가
- `src/e2r/cli/build_round94_r2_loop5_report.py` 추가
- `tests/test_round94_r2_loop5_ai_semiconductor.py` 추가
- `E2RArchetype`에 다음 archetype 추가:
  - `AI_NETWORKING_SWITCHING_INFRA`
  - `PHOTONICS_AI_DATACENTER_CHIPS`
  - `CIRCULAR_AI_FINANCING_OVERLAY`
- 산출물 생성:
  - `data/e2r_case_library/cases_r2_loop5_round94.jsonl`
  - `data/sector_taxonomy/score_weight_profiles_round94_r2_loop5_v5.csv`
  - `output/e2r_round94_r2_loop5_ai_semiconductor/`

## 핵심 결과

- score target: 22개
- case candidate: 20개
- structural success: 1개
- success candidate: 11개
- event premium: 1개
- overheat: 2개
- failed rerating: 1개
- Stage 4B case: 4개
- Stage 4C case: 1개
- hard gate target: 1개
- production scoring changed: false
- case records used as candidate-generation input: false

## 새로 강화한 축

### AI_NETWORKING_SWITCHING_INFRA

Cisco식 AI networking/switching order를 별도 축으로 분리했다. AI infrastructure order와 guidance raise는 Stage 2 근거가 될 수 있지만, 실제 매출·마진·FCF로 전환되어야 Stage 3 논의가 가능하다.

### PHOTONICS_AI_DATACENTER_CHIPS

Tower Semiconductor식 AI data-center photonics chip 계약을 분리했다. 계약금액과 납품연도는 Stage 2 근거지만, 고객집중, 납품지연, 수율, 마진 미확인 상태에서는 Green을 막는다.

### CIRCULAR_AI_FINANCING_OVERLAY

CoreWeave처럼 공급자, 고객, 투자자가 서로 얽힌 구조를 RedTeam overlay로 분리했다. 예를 들어 Nvidia가 투자자이면서 capacity buyer 역할도 하면, 그 계약을 순수한 외부 수요로 보기 어렵다.

### DISCLOSURE_CONFIDENCE_CAP

R2 장비·소재·PCB·AI 서버주는 계약, 시설투자, CB, 유상증자, 감사의견, 거래정지, 계약 정정·해지 detail이 중요하다. 제목만 있는 공시는 Stage 3 확신을 제한하고, 금액·고객·기간·마진·parser confidence가 확인되어야 한다.

## 변경하지 않은 것

- StageClassifier threshold는 변경하지 않았다.
- FeatureEngineering / scoring / staging / RedTeam production logic은 이 팩을 import하지 않는다.
- 케이스 레코드는 calibration/evaluation 전용이며 후보 생성 입력으로 쓰지 않는다.
- Stage 3-Green을 쉽게 만들기 위한 완화는 하지 않았다.

## 실행 명령

```bash
PYTHONPATH=src python -m unittest tests.test_round94_r2_loop5_ai_semiconductor -v
PYTHONPATH=src python -m e2r.cli.build_round94_r2_loop5_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check
```

## 검증 상태

- Round94 대상 테스트: 통과
- 전체 테스트: 통과
- `git diff --check`: 통과

## 다음 작업

다음 라운드는 R3 2차전지·전기차·친환경 Loop 5다. R2에서 한 것처럼 “좋은 성장 신호”, “Watch-to-Green 신호”, “Green을 막는 RedTeam 신호”를 분리해야 한다. 특히 2차전지는 계약·CAPA가 있어도 EV 수요 둔화, 광물가격, 가동률, valuation overheat가 Green을 막을 수 있다.

# Checkpoint 28A Round 40: Round Protocol Map

## Summary

Round 40 fixed the next-work map before adding more sector cases.

The key rule is:

```text
12 fixed large sectors
-> R1-R12 sector-by-sector case mining
-> R13 cross-archetype RedTeam / 4B / price validation
```

This patch does not change production scoring, StageClassifier thresholds, candidate generation, or RedTeam logic.

## What Was Added

- `src/e2r/sector/round40_round_protocol.py`
- `src/e2r/cli/build_round40_round_protocol_report.py`
- `tests/test_round40_round_protocol.py`
- `data/sector_taxonomy/round40_round_protocol.csv`
- `data/sector_taxonomy/round40_validation_protocol.csv`
- `output/e2r_round40_round_protocol/round40_round_protocol_summary.md`
- `output/e2r_round40_round_protocol/round40_round_sequence.md`
- `output/e2r_round40_round_protocol/round40_validation_protocol.md`
- `output/e2r_round40_round_protocol/round40_price_alignment_protocol.md`

## Fixed Map

- R1: 산업재·수주·인프라
- R2: AI·반도체·전자부품
- R3: 2차전지·전기차·친환경
- R4: 소재·스프레드·전략자원
- R5: 소비재·유통·브랜드
- R6: 금융·자본배분·디지털금융
- R7: 바이오·헬스케어·의료기기
- R8: 플랫폼·콘텐츠·SW·보안
- R9: 모빌리티·운송·레저
- R10: 건설·부동산·건자재
- R11: 정책·지정학·재난·이벤트
- R12: 농업·생활서비스·기타
- R13: Cross-archetype RedTeam / 4B / 가격검증 총정리

## Common Validation Protocol

Every future round now uses the same five-step protocol:

1. Case coverage
2. Stage date candidates
3. Price-path validation
4. Score-price alignment
5. Score-weight correction

Simple example:

`AI 서버 ODM` and `HBM` are both under AI/semiconductor, but they are not scored by the same evidence. ODM needs margin, inventory, customer, and accounting trust checks. HBM needs capacity, pricing, and multi-year revision checks.

## Guardrails

- Case labels are not candidate-generation input.
- Round protocol data is not production scoring input.
- Missing prices, dates, contracts, or EPS/FCF fields must remain missing.
- Stage 3-Green thresholds were not lowered.
- R13 is an overlay, not a 13th production large sector.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round40_round_protocol -v
PYTHONPATH=src python -m e2r.cli.build_round40_round_protocol_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check -- docs/round/round_40.md src/e2r/sector/round40_round_protocol.py src/e2r/cli/build_round40_round_protocol_report.py tests/test_round40_round_protocol.py data/sector_taxonomy/round40_round_protocol.csv data/sector_taxonomy/round40_validation_protocol.csv output/e2r_round40_round_protocol docs/checkpoints/checkpoint_28a_round40_round_protocol.md
```

Targeted Round 40 tests passed.

The full test suite still has the pre-existing Round 17 fixture-file issue from the deleted `docs/round/round_17.md`; Round 40 did not introduce that failure.

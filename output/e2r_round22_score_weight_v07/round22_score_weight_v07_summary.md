# Round-22 Score-Weight v0.7 Summary

- source_round: `docs/round/round_22.md`
- target_count: 10
- case_candidate_count: 40
- success_candidate_count: 18
- counterexample_or_risk_count: 22
- green_possible_count: 4
- watch_yellow_first_count: 6
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Interpretation
- Round 22 recalibrates score-weight hypotheses, not production scoring.
- Example: 증권사는 거래대금이 늘어도 지속성이 약하므로 Watch-first로 둔다.
- Example: 보험은 EPS 폭발보다 손해율, CSM/ROE, 자본비율, 환원 실행을 본다.
- Example: HBM은 Green 가능하지만 큰 리레이팅 이후에는 4B-watch crowding을 강하게 본다.
- Theme names, case IDs, and policy headlines are not score evidence.

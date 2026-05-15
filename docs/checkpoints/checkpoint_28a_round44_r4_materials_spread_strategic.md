# Checkpoint 28A Round 44: R4 Materials / Spread / Strategic Resources

## Summary

Round 44 was converted into a calibration-only R4 case pack for `MATERIALS_SPREAD_STRATEGIC`.

This patch does not change production scoring, staging, RedTeam, or candidate generation. It records the R4 research matrix as:

- R4 target sub-archetypes
- shadow score-weight drafts
- stage-date guidance
- case records
- price-validation fields
- Green/Watch/RedTeam guardrails

Simple example: rare-earth export controls can route research, but they do not create Green by themselves. Company-level Green would need production capacity, offtake, price floor, customer demand, and FCF evidence.

## Files Added

- `src/e2r/sector/round44_r4_materials_spread_strategic.py`
- `src/e2r/cli/build_round44_r4_report.py`
- `tests/test_round44_r4_materials_spread_strategic.py`
- `data/e2r_case_library/cases_r4_round44.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round44_r4_v1.csv`
- `output/e2r_round44_r4_materials_spread_strategic/round44_r4_materials_spread_strategic_summary.md`
- `output/e2r_round44_r4_materials_spread_strategic/round44_r4_case_matrix.csv`
- `output/e2r_round44_r4_materials_spread_strategic/round44_r4_stage_date_plan.csv`
- `output/e2r_round44_r4_materials_spread_strategic/round44_r4_green_guardrails.md`
- `output/e2r_round44_r4_materials_spread_strategic/round44_r4_price_validation_plan.md`
- `output/e2r_round44_r4_materials_spread_strategic/round44_r4_price_fields.csv`

## Coverage

- target_count: 13
- case_candidate_count: 15
- structural_success_count: 1
- success_candidate_count: 2
- cyclical_success_count: 3
- event_premium_count: 3
- overheat_count: 1
- failed_rerating_count: 1
- stage4b_case_count: 1
- stage4c_case_count: 3
- green_possible_count: 0
- watch_yellow_first_count: 11
- redteam_first_count: 2

## Key Guardrails

- R4 should separate structural rerating from commodity cycles, product-spread recoveries, policy events, and tender premiums.
- Commodity price rallies are not structural evidence by themselves.
- Rare metals improve only when price floor, offtake, government support, production capacity, and FCF are source-backed.
- Chemical and speculative advanced-material themes are RedTeam-first.
- Korea Zinc-style tender moves are `event_premium` until core FCF, smelting margin, and capital allocation evidence are separately verified.
- Supply glut, price crash, dividend cut, project delay, inventory loss, and no commercialization should block unsafe Green.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests/test_round44_r4_materials_spread_strategic.py -v
PYTHONPATH=src python -m e2r.cli.build_round44_r4_report
```

Result:

- Round 44 tests passed.
- Reports and JSONL/CSV outputs were generated.
- Production modules are tested to avoid importing the Round 44 case pack.

Full-suite note: the broader repo currently has unrelated round-file deletions in the working tree, including `docs/round/round_17.md`, which is known to break existing round17 tests until restored or intentionally handled.

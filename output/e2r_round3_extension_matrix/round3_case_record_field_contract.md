# Round-3 Case Record Field Contract

Round 3 asks future case records to be close to JSONL-ready instead of narrative-only.

## Required Fields
- `case_id`
- `symbol`
- `company_name`
- `market`
- `archetype`
- `case_type`
- `stage1_date`
- `stage2_date`
- `stage3_date`
- `stage4b_date`
- `stage4c_date`
- `peak_date`
- `stage1_evidence`
- `stage2_evidence`
- `stage3_evidence`
- `stage4b_evidence`
- `stage4c_evidence`
- `price_pattern`
- `must_have_fields`
- `red_flag_fields`
- `score_weight_hint`

## Example

A robotics case must include `stage2_evidence` such as actual customer adoption and revenue conversion.
A theme-overheat case must include `red_flag_fields` such as price-only rally or no EPS/FCF support.

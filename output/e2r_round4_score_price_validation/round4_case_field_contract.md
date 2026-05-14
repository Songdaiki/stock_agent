# Round-4 Case Field Contract

Round 4 adds price-path and failure-type fields so case records can explain whether scoring matched reality.

## Price Validation Fields
- `stage3_price`
- `peak_price`
- `peak_return_from_stage3`
- `mfe_90d`
- `mfe_180d`
- `mfe_1y`
- `mae_90d`
- `mae_180d`
- `mae_1y`
- `below_stage3_price_flag`
- `time_to_50pct`
- `time_to_100pct`
- `time_to_200pct`

## Stage Failure Types
- `green_success`
- `yellow_success`
- `stage2_watch_success`
- `false_green`
- `false_yellow`
- `should_have_been_red`
- `missed_structural`

## Example

`as_of_date=2023-07-27`인 Stage 3 후보라면, 2023-07-28 이후 리포트는 evidence가 아니라 forward price validation 구간의 결과로만 봐야 한다.

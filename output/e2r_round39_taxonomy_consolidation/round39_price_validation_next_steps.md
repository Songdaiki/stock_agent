# Round-39 Price-Path Validation Next Steps

## Immediate cleanup

1. Keep the 12 large-sector map fixed.
2. Keep Round-10 theme archetypes as the base routing layer.
3. Attach each later-round deep sub-archetype to a parent large sector and canonical archetype.
4. Sort cases_vXX by parent/sub-archetype.
5. Backfill stage-date and OHLCV paths only from source data.

## Validation metrics

- Stage 1/2/3 date candidate
- MFE_90D / 180D / 1Y / 2Y
- MAE_90D / 180D
- drawdown_after_peak
- EPS revision duration
- valuation band change
- hard 4C event drawdown where applicable

## Example

`AI_DATA_CENTER_INFRASTRUCTURE` is a parent. Under it, HBM, AI server ODM, neocloud, cooling, optical networking, gases, and power equipment each need separate validation because their margins, debt, customer concentration, and 4C risks differ.

# Round-22 Price Validation Plan

1. Backfill official price paths for cases with tradable symbols.
2. Keep reference cases as `needs_price_backfill` or `missing_price_data` until usable data exists.
3. Calculate stage prices, peak prices, MFE/MAE, and drawdown only from source data.
4. Compare v0.7 shadow weights against price-path and EPS/FCF evidence.
5. Keep production StageClassifier and score weights unchanged until coverage and price validation are sufficient.

## Priority Validation
- Brokerage: turnover rally versus PF/proprietary loss.
- Insurance/value-up: shareholder return execution versus low-PBR value trap.
- Memory/HBM: structural rerating versus 4B crowding and capex reversal.
- Retail/apparel: OPM/FCF versus inventory, markdown, and logistics cost.

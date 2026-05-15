# Round-26 Price Validation Plan

1. Backfill tradable case price paths where symbols exist.
2. Keep policy, synthetic, and reference counterexamples as `needs_price_backfill` or `missing_price_data`.
3. Calculate MFE/MAE, peak, drawdown, and below-entry flags only from source data.
4. Run shadow score-price alignment before production scoring changes.

## Priority Validation
- K-beauty: export/channel evidence versus inventory, receivables, and channel stuffing.
- Digital assets: approval, issuance, transaction volume, and fee economics versus theme-only rallies.
- Construction/materials: price hikes and dividends versus PF, unsold inventory, liquidity, and rates.
- HBM/AI cooling: structural EPS success versus crowding, capex delay, and price-only rerating.

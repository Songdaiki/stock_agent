# Round-30 Price Validation Plan

1. Backfill tradable case price paths where symbols exist.
2. Keep synthetic, theme, and reference counterexamples as `needs_price_backfill` or `missing_price_data`.
3. Calculate MFE/MAE, peak, drawdown, and below-entry flags only from source data.
4. Run shadow score-price alignment before any production scoring change.

## Priority Validation
- Semi equipment: customer CAPEX/order backlog versus CAPEX cut and inventory 4C.
- Auto: FCF, hybrid/mix, return execution versus tariff, recall, peak margin, and raw material risk.
- Travel/tourism: record revenue and policy events versus fuel, FX, visitor mix, OP leverage, and CAPEX underperformance.
- Convenience/agri/space: prove productivity, margin, repeat revenue, and contracts before any Green-like interpretation.

# Round-35 Price Validation Plan

1. Backfill tradable case price paths where symbols exist.
2. Keep synthetic, private, global reference, regulatory, and clinical cases as `needs_price_backfill` or `missing_price_data`.
3. Calculate MFE/MAE, peak, drawdown, and below-entry flags only from source data.
4. Run shadow score-price alignment before any production scoring change.

## Priority Validation
- Biosimilars/originators: uptake and margin defense versus price erosion and patent cliff.
- GLP-1/pharma channels: prescription growth and supply versus compounding, reimbursement, and regulation.
- Gene therapy/AI drug: commercialization and milestones versus cash burn and clinical failure.
- Contact-center AI/kiosks: ARR, ROI, maintenance, and software economics versus demos, theft, and customer friction.

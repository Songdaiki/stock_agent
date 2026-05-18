# Round-189 R5 Loop-12 Risk Overlays

| target | hard gate | red flags |
| --- | --- | --- |
| `K_FOOD_GLOBAL_LOCALIZATION` | false | capex_drag, utilization_unknown, opm_missing, fx_logistics_cost |
| `K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE` | false | regional_growth_cap, input_cost_risk, fx_or_geopolitics |
| `K_FOOD_SINGLE_SKU_EXPORT_RISK` | false | single_sku_dependency, viral_fad, inventory_unknown |
| `ECOMMERCE_RESTRUCTURING_JV_KOREA` | false | data_restriction, synergy_missing, competition_intense |
| `RETAIL_PLATFORM_DATA_REGULATION_OVERLAY` | true | kftc_data_sharing_restriction, data_regulation, monetization_delay, privacy_condition |
| `DEPARTMENT_STORE_MALL_REDEVELOPMENT` | false | capex_burden, traffic_weak, payback_unknown |
| `CONVENIENCE_STORE_PB_SSSG_KOREA` | false | cost_pressure, franchisee_margin_pressure, sssg_missing |
| `K_BEAUTY_BRAND_SECOND_WAVE` | false | sellthrough_missing, inventory_unknown, tariff_risk |
| `K_BEAUTY_TARIFF_IMPORT_REVIEW` | false | tariff_exposure, margin_buffer_missing, stockpiling |
| `CHANNEL_STUFFING_INVENTORY_OVERLAY` | true | inventory_spike, receivables_spike, sellthrough_failure |
| `DISCLOSURE_CONFIDENCE_CAP` | false | list_only, media_only, detail_missing, opm_fcf_missing |

## Hard / Cap Examples

- `RETAIL_PLATFORM_DATA_REGULATION_OVERLAY`: Gmarket/AliExpress JV 데이터 제한은 수익화 cap이다.
- `CHANNEL_STUFFING_INVENTORY_OVERLAY`: 재고·매출채권 급증은 K푸드/K뷰티/유통의 hard quality gate다.
- `K_BEAUTY_TARIFF_IMPORT_REVIEW`: 미국 관세는 gross margin buffer 확인 전 4C-watch다.
- `K_FOOD_SINGLE_SKU_EXPORT_RISK`: 단일 SKU viral은 반복 SKU와 재주문 전 Green 금지다.
- `DISCLOSURE_CONFIDENCE_CAP`: 매출·채널·재고·OPM·FCF detail 없으면 Green 금지.

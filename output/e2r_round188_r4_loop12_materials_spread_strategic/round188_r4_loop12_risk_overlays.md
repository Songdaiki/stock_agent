# Round-188 R4 Loop-12 Risk Overlays

| target | hard gate | red flags |
| --- | --- | --- |
| `REFINING_SPREAD_TURNAROUND_KOREA` | false | inventory_loss, temporary_supply_disruption, battery_drag, petrochem_drag |
| `REFINING_PETCHEM_MIX_DRAG` | false | battery_loss_expands, petrochem_drag, segment_bridge_missing |
| `PETROCHEMICAL_RESTRUCTURING_KOREA` | false | plan_detail_missing, spread_weak, china_oversupply, cashflow_unknown |
| `NCC_CAPACITY_CUT_STAGE2` | false | spread_recovery_missing, china_oversupply, shutdown_delayed |
| `NCC_OVERLOAD_SHAHEEN_RISK` | true | new_capacity_worsens_oversupply, spread_dilution, capex_burden |
| `SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING` | false | buyback_missing, petrochemical_drag, cashflow_unknown |
| `SYNTHETIC_RUBBER_TARIFF_RISK` | false | china_antidumping_duty, demand_cycle, butadiene_cost |
| `TIRE_RUBBER_PRODUCTION_DISRUPTION` | true | factory_fire, production_halt, capacity_loss_20pct |
| `COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL` | false | cycle_only, price_only_rally, inventory_noise |
| `DISCLOSURE_CONFIDENCE_CAP` | false | list_only, media_only, plan_detail_missing, spread_missing |

## Hard / Cap Examples

- `NCC_OVERLOAD_SHAHEEN_RISK`: 신규 ethylene CAPA가 구조조정 효과를 약화하면 Green을 막는다.
- `TIRE_RUBBER_PRODUCTION_DISRUPTION`: 공장 화재, 생산중단, capacity loss, 고객 공급 차질은 hard 4C다.
- `SYNTHETIC_RUBBER_TARIFF_RISK`: 중국 반덤핑 관세와 자동차/건설 수요 cycle은 Watch/Red cap이다.
- `REFINING_PETCHEM_MIX_DRAG`: 정유 이익을 배터리·석화 drag가 잠식하면 Stage 3를 제한한다.
- `DISCLOSURE_CONFIDENCE_CAP`: 제품별 spread, 가동률, OPM, FCF, 구조조정 세부안 미공개면 Green 금지.

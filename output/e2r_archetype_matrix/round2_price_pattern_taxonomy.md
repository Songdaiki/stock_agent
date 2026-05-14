# Round-2 Price Pattern Taxonomy

This is lifecycle calibration material, not a production trading signal.

Round 2 links Stage progression to price-path behavior so 4B/4C is not treated as price-only.

## Pattern Types
- `DIRECT_RERATING`: Stage 2 이후 조정 없이 급등하는 유형
- `STAIR_STEP_RERATING`: Stage 2 이후 20~30% 조정 반복 후 계속 상승하는 유형
- `CYCLE_SPIKE_NORMALIZATION`: EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형
- `THEME_FRONT_RUN`: 가격이 먼저 가고 EPS/FCF가 못 따라오는 유형
- `ACCOUNTING_TRUST_COLLAPSE`: Stage 2~3처럼 보이다가 회계/감사/신뢰 이슈로 4C가 터지는 유형
- `SECTOR_SPREAD_RERATING`: 선도주 리레이팅 이후 동종 섹터로 Stage 1->2가 확산되는 유형
- `MARGIN_NORMALIZATION_RERATING`: 저마진 물량 정리나 비용구조 개선으로 OPM이 정상화되는 유형
- `BACKLOG_RERATING`: 계약 하나보다 수주잔고 체급 변화가 가격 프레임을 바꾸는 유형
- `PROGRAM_MILESTONE_RERATING`: 정부/프로그램 milestone이 납품과 매출 인식으로 이어지는 유형
- `PRICE_ORDER_RERATING`: 선가/운임/제품가격과 수주가 동시에 움직이는 유형
- `EXPORT_CHANNEL_RERATING`: 수출 채널 확장과 반복 수요가 내수 프레임을 깨는 유형
- `CAPACITY_BOTTLENECK_RERATING`: HBM/CAPA/장비 리드타임 병목이 다년 EPS 경로를 바꾸는 유형
- `VALUE_UP_RERATING`: ROE/PBR/주주환원 조합이 Korea discount를 줄이는 유형
- `REGULATORY_REVENUE_CONVERSION`: 허가/기술이전이 실제 매출·로열티·FCF로 전환되어야 하는 유형

## Archetype Mapping

| archetype | price patterns | Green implication |
|---|---|---|
| CONTRACT_BACKLOG_INDUSTRIAL | STAIR_STEP_RERATING: Stage 2 이후 20~30% 조정 반복 후 계속 상승하는 유형; SECTOR_SPREAD_RERATING: 선도주 리레이팅 이후 동종 섹터로 Stage 1->2가 확산되는 유형; MARGIN_NORMALIZATION_RERATING: 저마진 물량 정리나 비용구조 개선으로 OPM이 정상화되는 유형 | Green allowed only with disclosure + financial actual + research/consensus-revision cross evidence. |
| DEFENSE_GOVERNMENT_BACKLOG | BACKLOG_RERATING: 계약 하나보다 수주잔고 체급 변화가 가격 프레임을 바꾸는 유형; PROGRAM_MILESTONE_RERATING: 정부/프로그램 milestone이 납품과 매출 인식으로 이어지는 유형 | Green allowed with government customer, delivery visibility, and margin/revision evidence. |
| SHIPBUILDING_OFFSHORE_BACKLOG | PRICE_ORDER_RERATING: 선가/운임/제품가격과 수주가 동시에 움직이는 유형; BACKLOG_RERATING: 계약 하나보다 수주잔고 체급 변화가 가격 프레임을 바꾸는 유형; CYCLE_SPIKE_NORMALIZATION: EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형 | Green allowed selectively; low-margin backlog and cancellation risk must be cleared. |
| EXPORT_RECURRING_CONSUMER | EXPORT_CHANNEL_RERATING: 수출 채널 확장과 반복 수요가 내수 프레임을 깨는 유형; STAIR_STEP_RERATING: Stage 2 이후 20~30% 조정 반복 후 계속 상승하는 유형 | Contract quality is not required; recurring export demand and EPS/OP revision are required. |
| K_BEAUTY_EXPORT_DISTRIBUTION | EXPORT_CHANNEL_RERATING: 수출 채널 확장과 반복 수요가 내수 프레임을 깨는 유형; THEME_FRONT_RUN: 가격이 먼저 가고 EPS/FCF가 못 따라오는 유형 | Green allowed through export/channel/recurring-demand evidence, not contract quality. |
| MEMORY_HBM_CAPACITY | CAPACITY_BOTTLENECK_RERATING: HBM/CAPA/장비 리드타임 병목이 다년 EPS 경로를 바꾸는 유형; STAIR_STEP_RERATING: Stage 2 이후 20~30% 조정 반복 후 계속 상승하는 유형; CYCLE_SPIKE_NORMALIZATION: EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형 | Green allowed with memory-specific revision, pricing, supply discipline, and capacity evidence. |
| SEMI_EQUIPMENT_CAPEX | CAPACITY_BOTTLENECK_RERATING: HBM/CAPA/장비 리드타임 병목이 다년 EPS 경로를 바꾸는 유형; CYCLE_SPIKE_NORMALIZATION: EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형 | Green allowed with confirmed order-to-revenue conversion and customer capex durability. |
| MEDICAL_DEVICE_HEALTHCARE_EXPORT | EXPORT_CHANNEL_RERATING: 수출 채널 확장과 반복 수요가 내수 프레임을 깨는 유형; DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green allowed with export channel plus repeat consumable/service revenue. |
| FINANCIAL_SPREAD_BALANCE_SHEET | VALUE_UP_RERATING: ROE/PBR/주주환원 조합이 Korea discount를 줄이는 유형 | Green allowed with ROE/PBR and durable capital return, not low PBR alone. |
| TURNAROUND_COST_RESTRUCTURING | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green allowed only when cost improvement is recurring and paired with growth/FCF. |
| COMMODITY_SPREAD | CYCLE_SPIKE_NORMALIZATION: EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형 | Green restricted by cycle cap unless structural cost-curve or supply discipline is explicit. |
| SHIPPING_FREIGHT_CYCLE | CYCLE_SPIKE_NORMALIZATION: EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형 | Green very restricted; normally cyclical success or Yellow/Red rather than structural Green. |
| BATTERY_MATERIALS_CAPEX_OVERHEAT | THEME_FRONT_RUN: 가격이 먼저 가고 EPS/FCF가 못 따라오는 유형; CYCLE_SPIKE_NORMALIZATION: EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형 | Green highly restricted; overheat and CAPA overbuild penalties dominate unless contract economics are clear. |
| AUTO_MOBILITY_COMPONENTS | VALUE_UP_RERATING: ROE/PBR/주주환원 조합이 Korea discount를 줄이는 유형; MARGIN_NORMALIZATION_RERATING: 저마진 물량 정리나 비용구조 개선으로 OPM이 정상화되는 유형 | Green allowed with durable mix/FCF/return evidence; component cost pass-through must be proven. |
| CONSTRUCTION_REAL_ESTATE_CREDIT | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green very restricted; credit and cash-flow evidence must dominate order headline. |
| UTILITIES_REGULATED_TARIFF | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green restricted unless tariff pass-through regime changes, not just one-time relief. |
| BIOTECH_REGULATORY | REGULATORY_REVENUE_CONVERSION: 허가/기술이전이 실제 매출·로열티·FCF로 전환되어야 하는 유형; THEME_FRONT_RUN: 가격이 먼저 가고 EPS/FCF가 못 따라오는 유형 | Green blocked before real revenue/royalty and dilution control. |
| ROBOTICS_FACTORY_AUTOMATION | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green restricted until revenue conversion and repeatability are proven. |
| PLATFORM_SOFTWARE_INTERNET | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green allowed only with monetization and margin leverage, not MAU alone. |
| GAME_CONTENT_IP | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green restricted unless IP repeatability and monetization are visible. |
| HOLDING_RESTRUCTURING_GOVERNANCE | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green allowed only if governance action is backed by FCF/NAV improvement. |
| ONE_OFF_EVENT_DEMAND | CYCLE_SPIKE_NORMALIZATION: EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형 | Green blocked by default; normally Stage 3-Red/Yellow guardrail. |
| THEME_VALUATION_OVERHEAT | THEME_FRONT_RUN: 가격이 먼저 가고 EPS/FCF가 못 따라오는 유형; ACCOUNTING_TRUST_COLLAPSE: Stage 2~3처럼 보이다가 회계/감사/신뢰 이슈로 4C가 터지는 유형 | Green blocked unless real EPS/FCF evidence overwhelms overheat risk. |
| RETAIL_DOMESTIC_CONSUMER | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green restricted unless OP/FCF improvement is structural, not traffic-only. |
| GENERIC_UNCLASSIFIED | DIRECT_RERATING: Stage 2 이후 조정 없이 급등하는 유형 | Green blocked until a real archetype and evidence family are assigned. |

## Example

A power-equipment candidate can be Stage 2 with `STAIR_STEP_RERATING`: it may pull back 20~30% and still remain structurally intact if backlog, margin, and revision evidence persist.

A theme or one-off case can have strong price action, but `THEME_FRONT_RUN` or `CYCLE_SPIKE_NORMALIZATION` keeps Green restricted until EPS/FCF durability is proven.

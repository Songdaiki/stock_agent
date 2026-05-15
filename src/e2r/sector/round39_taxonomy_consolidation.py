"""Round-39 taxonomy consolidation.

Round 39 does not add production scoring. It consolidates the hierarchy:
12 large sectors stay fixed, Round-10 theme archetypes remain the base
classification layer, and later rounds add deep sub-archetype lenses under the
same parent sectors. Production feature engineering, scoring, staging, and
RedTeam code must not import this module.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.round10_theme_tag_taxonomy import (
    ROUND10_LARGE_SECTORS,
    ROUND10_THEME_ARCHETYPES,
    Round10LargeSector,
    Round10ThemePosture,
)


ROUND39_SOURCE_ROUND_PATH = "docs/round/round_39.md"
ROUND39_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round39_taxonomy_consolidation"
ROUND39_DEFAULT_DEEP_REGISTRY_PATH = "data/sector_taxonomy/round39_deep_sub_archetype_registry.csv"


@dataclass(frozen=True)
class Round39DeepSubArchetype:
    label: str
    parent_large_sector: Round10LargeSector
    parent_canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    parent_theme_hint: str
    evidence_focus: tuple[str, ...]
    risk_focus: tuple[str, ...]
    price_validation_focus: tuple[str, ...]
    notes: str

    @property
    def theme_is_score_input(self) -> bool:
        return False

    @property
    def production_scoring_changed(self) -> bool:
        return False

    def as_row(self) -> dict[str, str]:
        return {
            "label": self.label,
            "parent_large_sector": self.parent_large_sector.value,
            "parent_canonical_archetype": self.parent_canonical_archetype.value,
            "posture": self.posture.value,
            "parent_theme_hint": self.parent_theme_hint,
            "evidence_focus": "|".join(self.evidence_focus),
            "risk_focus": "|".join(self.risk_focus),
            "price_validation_focus": "|".join(self.price_validation_focus),
            "theme_is_score_input": str(self.theme_is_score_input).lower(),
            "production_scoring_changed": str(self.production_scoring_changed).lower(),
            "notes": self.notes,
        }


ROUND39_DEEP_SUB_ARCHETYPES: tuple[Round39DeepSubArchetype, ...] = (
    Round39DeepSubArchetype("GRID_TRANSFORMER_SHORTAGE", Round10LargeSector.INDUSTRIAL_ORDERS_INFRA, E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL, Round10ThemePosture.GREEN_POSSIBLE, "POWER_GRID_EQUIPMENT", ("contract_to_sales", "backlog_growth", "lead_time_extended", "op_eps_revision"), ("capacity_normalization", "low_margin_contract"), ("mfe_90d", "mfe_180d", "mfe_1y", "backlog_growth"), "AI data-center and grid transformer shortage lens under industrial backlog."),
    Round39DeepSubArchetype("DEFENSE_TECH_AUTONOMOUS_SYSTEMS", Round10LargeSector.INDUSTRIAL_ORDERS_INFRA, E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG, Round10ThemePosture.GREEN_POSSIBLE, "DEFENSE_EXPORT_BACKLOG", ("government_framework", "procurement_quantity", "production_capacity"), ("prototype_only", "procurement_uncertainty"), ("contract_conversion", "gross_margin", "mae_180d"), "Autonomous defense systems need procurement and delivery proof."),
    Round39DeepSubArchetype("DEFENSE_DRONE_COUNTER_UAS", Round10LargeSector.INDUSTRIAL_ORDERS_INFRA, E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG, Round10ThemePosture.GREEN_POSSIBLE, "URBAN_AIR_DRONE", ("military_delivery_contract", "idiq_framework", "backlog_growth"), ("mna_dilution", "export_control"), ("backlog_conversion", "mna_drawdown"), "Drone and counter-UAS tags stay under defense backlog once delivery contracts exist."),
    Round39DeepSubArchetype("DEFENSE_AI_SOFTWARE_INTELLIGENCE", Round10LargeSector.INDUSTRIAL_ORDERS_INFRA, E2RArchetype.PLATFORM_SOFTWARE_INTERNET, Round10ThemePosture.GREEN_POSSIBLE, "DEFENSE_EXPORT_BACKLOG", ("program_of_record", "recurring_license", "gross_margin_visible"), ("ethical_regulation", "budget_cycle"), ("government_revenue_growth", "rpo_backlog"), "Defense AI software is software-recurring evidence inside the defense context."),
    Round39DeepSubArchetype("RAIL_INFRASTRUCTURE", Round10LargeSector.INDUSTRIAL_ORDERS_INFRA, E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL, Round10ThemePosture.WATCH_YELLOW_FIRST, "RAIL_NUCLEAR_INFRA", ("binding_contract", "delivery_schedule", "margin_visibility"), ("policy_headline_only", "project_delay"), ("contract_to_revenue", "mae_after_delay"), "Rail remains Watch until actual contract and delivery economics are visible."),
    Round39DeepSubArchetype("NUCLEAR_SMR_GRID_POLICY_CONTRACT", Round10LargeSector.INDUSTRIAL_ORDERS_INFRA, E2RArchetype.NUCLEAR_SMR_GRID_POLICY, Round10ThemePosture.WATCH_YELLOW_FIRST, "RAIL_NUCLEAR_INFRA", ("ppa_or_contract", "permitting", "supplier_revenue"), ("legal_delay", "cost_overrun"), ("project_schedule", "policy_delay_drawdown"), "Nuclear/SMR needs project economics, not policy premium alone."),
    Round39DeepSubArchetype("MEMORY_HBM_CAPACITY_EXTENSION", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.MEMORY_HBM_CAPACITY, Round10ThemePosture.GREEN_POSSIBLE, "MEMORY_HBM_CAPACITY", ("hbm_demand", "capacity_allocation", "fy1_fy2_revision"), ("capex_overbuild", "memory_price_decline"), ("mfe_180d", "mfe_1y", "revision_duration"), "HBM remains a high-Green-potential AI semiconductor axis."),
    Round39DeepSubArchetype("AI_SERVER_ODM_EMS_SUPPLY_CHAIN", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, Round10ThemePosture.GREEN_POSSIBLE, "AI_DATACENTER_INFRA", ("rack_shipment_growth", "op_eps_revision", "capacity_expansion"), ("low_margin_assembly", "accounting_trust"), ("gross_margin", "inventory_growth", "audit_event_drawdown"), "AI server ODM/EMS is not HBM; margin and trust risks are central."),
    Round39DeepSubArchetype("NEOCLOUD_GPU_RENTAL", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, Round10ThemePosture.WATCH_YELLOW_FIRST, "AI_DATACENTER_INFRA", ("take_or_pay", "contracted_backlog", "ebitda_improvement"), ("debt", "gpu_obsolescence", "fcf_negative"), ("net_debt_ebitda", "fcf_margin", "ipo_mae_180d"), "Neocloud visibility is offset by debt and GPU depreciation."),
    Round39DeepSubArchetype("ADVANCED_PACKAGING_COWOS_EMIB", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.SEMI_EQUIPMENT_CAPEX, Round10ThemePosture.GREEN_POSSIBLE, "ADVANCED_PACKAGING_PCB", ("cowos", "packaging_revenue_growth", "orders_or_backlog"), ("bottleneck_normalization", "yield_risk"), ("bookings_backlog", "drawdown_after_capex_peak"), "Advanced packaging is an independent AI bottleneck lens."),
    Round39DeepSubArchetype("SEMI_EQUIPMENT_AI_CAPEX", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.SEMI_EQUIPMENT_CAPEX, Round10ThemePosture.GREEN_POSSIBLE, "SEMICONDUCTOR_EQUIPMENT_MATERIALS", ("equipment_backlog", "guidance_raise", "eps_revision"), ("customer_capex", "export_control"), ("orders_backlog", "mae_after_order_slowdown"), "Semi equipment remains customer-capex-cycle dependent."),
    Round39DeepSubArchetype("OPTICAL_NETWORKING_AI_DATACENTER", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, Round10ThemePosture.GREEN_POSSIBLE, "AI_DATACENTER_INFRA", ("laser_leadtime", "hyperscaler_contract", "op_eps_revision"), ("capacity_normalization", "hyperscaler_concentration"), ("lead_time_normalization_drawdown", "valuation_crowding"), "Optical networking needs order and lead-time evidence."),
    Round39DeepSubArchetype("INDUSTRIAL_GASES_SEMICONDUCTOR_INFRA", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.SEMI_EQUIPMENT_CAPEX, Round10ThemePosture.GREEN_POSSIBLE, "SEMICONDUCTOR_EQUIPMENT_MATERIALS", ("onsite_gas_plant", "take_or_pay", "fab_ramp_schedule"), ("fab_delay", "customer_concentration"), ("fab_schedule", "capex_payback"), "Semiconductor gases are fab utility-like when onsite contracts are explicit."),
    Round39DeepSubArchetype("AI_DATA_CENTER_POWER_EQUIPMENT", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, Round10ThemePosture.GREEN_POSSIBLE, "AI_DATACENTER_INFRA", ("bookings_growth", "backlog_growth", "op_margin_improvement"), ("bookings_slowdown", "low_margin_project"), ("bookings_growth", "gross_margin", "valuation_crowding"), "Internal data-center power equipment is distinct from grid transformers."),
    Round39DeepSubArchetype("AI_DATA_CENTER_COOLING", Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS, E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, Round10ThemePosture.GREEN_POSSIBLE, "AI_DATACENTER_INFRA", ("cooling_capacity", "liquid_cooling_order", "hyperscaler_customer"), ("capex_delay", "thermal_design_shift"), ("contract_to_revenue", "margin_conversion"), "Cooling is an AI data-center bottleneck only with customer and revenue proof."),
    Round39DeepSubArchetype("POWER_SEMICONDUCTOR_SIC", Round10LargeSector.BATTERY_EV_GREEN, E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT, Round10ThemePosture.WATCH_YELLOW_FIRST, "BATTERY_EQUIPMENT_PARTS", ("long_term_supply_contract", "utilization_up", "fcf_improvement"), ("capex_debt", "bankruptcy", "ev_demand"), ("debt_ebitda", "utilization", "cash_burn"), "SiC narrative is capped until utilization, FCF, and debt stability are visible."),
    Round39DeepSubArchetype("LITHIUM_BATTERY_RAW_MATERIAL", Round10LargeSector.BATTERY_EV_GREEN, E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT, Round10ThemePosture.REDTEAM_FIRST, "BATTERY_MATERIALS_CAPEX_OVERHEAT", ("price_pass_through", "contract_quality"), ("lithium_price_reversal", "capa_overbuild"), ("commodity_peak_drawdown", "mae_1y"), "Lithium/raw material cycles stay RedTeam-first."),
    Round39DeepSubArchetype("RECYCLING_BATTERY_MATERIAL", Round10LargeSector.BATTERY_EV_GREEN, E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT, Round10ThemePosture.WATCH_YELLOW_FIRST, "BATTERY_MATERIALS_CAPEX_OVERHEAT", ("collection_volume", "metal_recovery_margin"), ("metal_price_drop", "low_utilization"), ("volume_to_margin", "metal_price_drawdown"), "Battery recycling needs collection volume and margin, not circular-economy label only."),
    Round39DeepSubArchetype("SOLID_STATE_BATTERY_PRE_COMMERCIAL", Round10LargeSector.BATTERY_EV_GREEN, E2RArchetype.THEME_VALUATION_OVERHEAT, Round10ThemePosture.REDTEAM_FIRST, "BATTERY_MATERIALS_CAPEX_OVERHEAT", ("commercial_order", "manufacturing_yield"), ("precommercial_theme", "timeline_slip"), ("event_pop_drawdown", "commercialization_delay"), "Solid-state remains Green-blocked before commercial orders and yield proof."),
    Round39DeepSubArchetype("CARBON_CREDIT_POLICY", Round10LargeSector.BATTERY_EV_GREEN, E2RArchetype.UTILITIES_REGULATED_TARIFF, Round10ThemePosture.WATCH_YELLOW_FIRST, "RENEWABLE_ENERGY_POLICY", ("regulated_revenue", "credit_price", "project_economics"), ("policy_dependency", "credit_price_reversal"), ("policy_drawdown", "credit_price_cycle"), "Carbon credit is policy-sensitive; revenue proof is required."),
    Round39DeepSubArchetype("CHEMICAL_SPREAD_CHINA_OVERSUPPLY", Round10LargeSector.MATERIALS_SPREAD_STRATEGIC, E2RArchetype.COMMODITY_SPREAD, Round10ThemePosture.REDTEAM_FIRST, "CHEMICAL_SPREAD", ("product_spread", "inventory_status"), ("china_oversupply", "spread_reversal"), ("spread_peak_drawdown", "inventory_cycle"), "Chemical spread is usually cycle/RedTeam-first."),
    Round39DeepSubArchetype("PRECIOUS_METALS_SAFE_HAVEN_MINERS", Round10LargeSector.MATERIALS_SPREAD_STRATEGIC, E2RArchetype.COMMODITY_SPREAD, Round10ThemePosture.WATCH_YELLOW_FIRST, "NONFERROUS_STRATEGIC_METALS", ("realized_price_up", "aisc_stable", "fcf_growth"), ("gold_price_reversal", "mine_disruption"), ("gold_relative_return", "drawdown_after_commodity_peak"), "Gold miners need realized price, cost, FCF, and capital return together."),
    Round39DeepSubArchetype("LNG_ENERGY_TRADING", Round10LargeSector.MATERIALS_SPREAD_STRATEGIC, E2RArchetype.COMMODITY_SPREAD, Round10ThemePosture.WATCH_YELLOW_FIRST, "REFINING_OIL_SPREAD", ("spread_capture", "inventory_status", "contract_book"), ("commodity_reversal", "hedge_loss"), ("spread_to_op", "commodity_drawdown"), "Energy trading/spread cases require explicit book and risk controls."),
    Round39DeepSubArchetype("K_FOOD_EXPORT_RECURRING", Round10LargeSector.CONSUMER_RETAIL_BRAND, E2RArchetype.EXPORT_RECURRING_CONSUMER, Round10ThemePosture.GREEN_POSSIBLE, "EXPORT_RECURRING_CONSUMER", ("export_growth", "channel_expansion", "repeat_demand", "opm_expansion"), ("single_product_fad", "recall_regulation"), ("sell_through", "opm_sustainability"), "K-food does not need contract quality, but repeat export demand and revision support are required."),
    Round39DeepSubArchetype("K_BEAUTY_EXPORT_CHANNEL", Round10LargeSector.CONSUMER_RETAIL_BRAND, E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION, Round10ThemePosture.GREEN_POSSIBLE, "K_BEAUTY_EXPORT_DISTRIBUTION", ("channel_diversification", "repeat_orders", "opm_roe_improvement"), ("china_dependency", "channel_stuffing"), ("inventory", "receivables", "channel_growth"), "K-beauty needs repeat channel evidence and inventory discipline."),
    Round39DeepSubArchetype("COLD_CHAIN_REIT_LOGISTICS", Round10LargeSector.CONSUMER_RETAIL_BRAND, E2RArchetype.RETAIL_DOMESTIC_CONSUMER, Round10ThemePosture.WATCH_YELLOW_FIRST, "ECOMMERCE_FRESH_LOGISTICS", ("occupancy", "noi_affo_growth", "long_term_tenant_contract"), ("energy_cost", "funding_cost"), ("affo_growth", "debt_cost", "dividend_coverage"), "Cold chain is infrastructure/REIT-like, not simple e-commerce logistics."),
    Round39DeepSubArchetype("SERVICE_KIOSK_SELF_CHECKOUT", Round10LargeSector.CONSUMER_RETAIL_BRAND, E2RArchetype.RETAIL_DOMESTIC_CONSUMER, Round10ThemePosture.WATCH_YELLOW_FIRST, "RETAIL_CONVENIENCE_OFFLINE", ("installed_base_growth", "maintenance_recurring_revenue", "payment_fee_revenue"), ("theft", "customer_friction", "retailer_retreat"), ("hardware_vs_recurring_revenue", "renewal_rate"), "Kiosk cases need recurring economics, not hardware installation alone."),
    Round39DeepSubArchetype("VALUE_UP_BANK_INSURANCE", Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL, E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN, Round10ThemePosture.GREEN_POSSIBLE, "VALUE_UP_SHAREHOLDER_RETURN", ("roe", "capital_ratio", "buyback_cancel", "dividend_policy"), ("credit_cost", "announcement_only"), ("pbr_roe_gap", "capital_return_execution"), "Value-up needs execution and ROE support, not index inclusion only."),
    Round39DeepSubArchetype("DIGITAL_ASSET_TOKENIZATION", Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL, E2RArchetype.THEME_VALUATION_OVERHEAT, Round10ThemePosture.REDTEAM_FIRST, "DIGITAL_ASSET_TOKENIZATION", ("regulated_revenue", "license_or_partner"), ("unregulated_theme", "cash_flow_absent"), ("event_pop_drawdown", "regulated_volume"), "STO/stablecoin tags remain RedTeam-first without regulated revenue."),
    Round39DeepSubArchetype("CRO_CLINICAL_SERVICE", Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE, E2RArchetype.CDMO_HEALTHCARE_CONTRACT, Round10ThemePosture.WATCH_YELLOW_FIRST, "CDMO_HEALTHCARE_CONTRACT", ("backlog", "customer_diversification", "op_margin"), ("biotech_funding_cycle", "cancellation"), ("backlog_to_revenue", "funding_cycle_drawdown"), "CRO is service/backlog driven but biotech funding cycle sensitive."),
    Round39DeepSubArchetype("DIGITAL_HEALTHCARE_AI", Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE, E2RArchetype.PLATFORM_SOFTWARE_INTERNET, Round10ThemePosture.WATCH_YELLOW_FIRST, "DIGITAL_HEALTHCARE_AI", ("regulatory_clearance", "hospital_contract", "reimbursement"), ("poc_only", "privacy"), ("contract_to_revenue", "privacy_event_drawdown"), "Medical AI needs monetization and regulation evidence."),
    Round39DeepSubArchetype("TELEHEALTH_BEHAVIORAL_HEALTH", Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE, E2RArchetype.PLATFORM_SOFTWARE_INTERNET, Round10ThemePosture.WATCH_YELLOW_FIRST, "DIGITAL_HEALTHCARE_AI", ("employer_or_insurance_contract", "repeat_usage", "cac_stable"), ("privacy", "cac", "churn"), ("cac_to_revenue", "fcf_margin", "privacy_drawdown"), "Telehealth needs B2B/B2B2C recurrence and privacy discipline."),
    Round39DeepSubArchetype("GENE_THERAPY_RARE_DISEASE", Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE, E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY, Round10ThemePosture.REDTEAM_FIRST, "BIOTECH_PRE_REVENUE_REGULATORY", ("approval", "reimbursement", "commercial_launch"), ("cash_burn", "dilution", "trial_failure"), ("approval_event_drawdown", "cash_runway"), "Gene therapy remains Green-blocked before commercialization and cash-flow visibility."),
    Round39DeepSubArchetype("CLOUD_AI_SOFTWARE_INFRA", Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY, E2RArchetype.PLATFORM_SOFTWARE_INTERNET, Round10ThemePosture.WATCH_YELLOW_FIRST, "PLATFORM_SOFTWARE_INTERNET", ("arr_growth", "opm_leverage", "low_churn"), ("ai_cost", "pricing_pressure"), ("arr_to_fcf", "gross_margin"), "AI software needs paid usage, OPM, and FCF, not feature labels."),
    Round39DeepSubArchetype("SECURITY_IDENTITY_DEEPFAKE", Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY, E2RArchetype.PLATFORM_SOFTWARE_INTERNET, Round10ThemePosture.WATCH_YELLOW_FIRST, "SECURITY_IDENTITY_INFRA", ("recurring_contract", "security_demand", "op_eps_revision"), ("breach_event", "lawsuit"), ("arr_retention", "breach_drawdown"), "Security demand is structural but trust events are 4C risks."),
    Round39DeepSubArchetype("CONTACT_CENTER_AI_AUTOMATION", Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY, E2RArchetype.PLATFORM_SOFTWARE_INTERNET, Round10ThemePosture.WATCH_YELLOW_FIRST, "AI_SOFTWARE_APPLICATION", ("paid_usage", "cost_savings", "enterprise_contract"), ("poc_only", "ai_cost"), ("contract_to_arr", "opm_leverage"), "Contact-center AI needs paid enterprise usage and margin proof."),
    Round39DeepSubArchetype("SATELLITE_CONNECTIVITY_INFRA", Round10LargeSector.MOBILITY_TRANSPORT_LEISURE, E2RArchetype.PLATFORM_SOFTWARE_INTERNET, Round10ThemePosture.WATCH_YELLOW_FIRST, "URBAN_AIR_DRONE", ("airline_or_defense_contract", "recurring_service_revenue", "backlog_growth"), ("capex_debt", "spacex_theme_only"), ("revenue_growth", "ebitda_margin", "debt_capex"), "Satellite connectivity must separate recurring service revenue from SpaceX labels."),
    Round39DeepSubArchetype("SHIPPING_FREIGHT_CYCLE_RECHECK", Round10LargeSector.MOBILITY_TRANSPORT_LEISURE, E2RArchetype.SHIPPING_FREIGHT_CYCLE, Round10ThemePosture.REDTEAM_FIRST, "SHIPPING_FREIGHT_CYCLE", ("freight_rate", "contract_vs_spot"), ("overcapacity", "freight_rate_reversal"), ("freight_peak_drawdown", "eps_normalization"), "Shipping can be cyclical_success but structural Green is heavily restricted."),
    Round39DeepSubArchetype("DATA_CENTER_REIT_INFRA", Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS, E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN, Round10ThemePosture.WATCH_YELLOW_FIRST, "REIT_DEVELOPMENT_TRUST", ("tenant_contract", "occupancy", "affo_growth"), ("funding_cost", "capex_burden"), ("affo_growth", "debt_cost_drawdown"), "Data-center REIT evidence is tenant, occupancy, AFFO, and funding cost."),
    Round39DeepSubArchetype("EVENT_DISEASE_PEST_DEMAND", Round10LargeSector.POLICY_GEOPOLITICAL_EVENT, E2RArchetype.ONE_OFF_EVENT_DEMAND, Round10ThemePosture.REDTEAM_FIRST, "DISASTER_DISEASE_EVENT", ("temporary_demand", "inventory_sales"), ("event_normalization", "next_year_reversal"), ("event_pop_drawdown", "revenue_retention"), "Disease/pest demand is one-off until recurring revenue is proven."),
    Round39DeepSubArchetype("SMART_FARM_AUTOMATION", Round10LargeSector.EDUCATION_LIFE_AGRI_MISC, E2RArchetype.ROBOTICS_FACTORY_AUTOMATION, Round10ThemePosture.WATCH_YELLOW_FIRST, "AGRI_FOOD_LIFE_MISC", ("commercial_installation", "repeat_service_revenue"), ("subsidy_dependency", "pilot_only"), ("pilot_conversion", "service_margin"), "Smart farm automation needs installation-to-recurring-service conversion."),
)


def round39_base_theme_count() -> int:
    return len(ROUND10_THEME_ARCHETYPES)


def round39_summary() -> dict[str, int | bool]:
    return {
        "large_sector_count": len(ROUND10_LARGE_SECTORS),
        "base_theme_archetype_count": round39_base_theme_count(),
        "deep_sub_archetype_count": len(ROUND39_DEEP_SUB_ARCHETYPES),
        "combined_view_count": round39_base_theme_count() + len(ROUND39_DEEP_SUB_ARCHETYPES),
        "green_possible_deep_count": sum(1 for item in ROUND39_DEEP_SUB_ARCHETYPES if item.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_deep_count": sum(1 for item in ROUND39_DEEP_SUB_ARCHETYPES if item.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_deep_count": sum(1 for item in ROUND39_DEEP_SUB_ARCHETYPES if item.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "deep_sub_archetypes_are_candidate_generation_input": False,
    }


def round39_large_sector_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for key, definition in ROUND10_LARGE_SECTORS.items():
        base = [item for item in ROUND10_THEME_ARCHETYPES if item.large_sector == key]
        deep = [item for item in ROUND39_DEEP_SUB_ARCHETYPES if item.parent_large_sector == key]
        rows.append(
            {
                "large_sector": key.value,
                "korean_name": definition.korean_name,
                "description": definition.description,
                "base_theme_archetype_count": str(len(base)),
                "deep_sub_archetype_count": str(len(deep)),
                "combined_view_count": str(len(base) + len(deep)),
                "deep_sub_archetypes": "|".join(item.label for item in deep),
            }
        )
    return tuple(rows)


def round39_deep_sub_archetype_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND39_DEEP_SUB_ARCHETYPES)


def write_round39_taxonomy_reports(
    *,
    output_directory: str | Path = ROUND39_DEFAULT_OUTPUT_DIRECTORY,
    deep_registry_path: str | Path = ROUND39_DEFAULT_DEEP_REGISTRY_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    deep_registry = Path(deep_registry_path)
    deep_registry.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "deep_registry": deep_registry,
        "summary": output / "round39_taxonomy_consolidation_summary.md",
        "large_sector_hierarchy": output / "round39_large_sector_hierarchy.csv",
        "layer_model": output / "round39_layer_model.md",
        "green_policy_rollup": output / "round39_green_policy_rollup.md",
        "price_validation_next_steps": output / "round39_price_validation_next_steps.md",
    }
    _write_rows(round39_deep_sub_archetype_rows(), paths["deep_registry"])
    _write_rows(round39_large_sector_rows(), paths["large_sector_hierarchy"])
    paths["summary"].write_text(render_round39_summary_markdown(), encoding="utf-8")
    paths["layer_model"].write_text(render_round39_layer_model_markdown(), encoding="utf-8")
    paths["green_policy_rollup"].write_text(render_round39_green_policy_rollup_markdown(), encoding="utf-8")
    paths["price_validation_next_steps"].write_text(render_round39_price_validation_next_steps_markdown(), encoding="utf-8")
    return paths


def render_round39_summary_markdown() -> str:
    summary = round39_summary()
    lines = [
        "# Round-39 Taxonomy Consolidation Summary",
        "",
        f"- source_round: `{ROUND39_SOURCE_ROUND_PATH}`",
        f"- large_sector_count: {summary['large_sector_count']}",
        f"- base_theme_archetype_count: {summary['base_theme_archetype_count']}",
        f"- deep_sub_archetype_count: {summary['deep_sub_archetype_count']}",
        f"- combined_view_count: {summary['combined_view_count']}",
        f"- green_possible_deep_count: {summary['green_possible_deep_count']}",
        f"- watch_yellow_first_deep_count: {summary['watch_yellow_first_deep_count']}",
        f"- redteam_first_deep_count: {summary['redteam_first_deep_count']}",
        "- production_scoring_changed: false",
        "- deep_sub_archetypes_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "- The top-level map remains 12 large sectors.",
        "- Round-10 provides the base theme/archetype view.",
        "- Later rounds add deep sub-archetype lenses under the same parent sectors.",
        "- Example: AI infrastructure splits into HBM, AI server ODM, neocloud, CoWoS, optical networking, cooling, gases, and power equipment.",
        "- Theme labels and sub-archetype labels are routing and validation lenses, not direct score evidence.",
    ]
    return "\n".join(lines) + "\n"


def render_round39_layer_model_markdown() -> str:
    return "\n".join(
        [
            "# Round-39 Layer Model",
            "",
            "## Layers",
            "",
            "1. Raw theme tag: market labels such as HBM, K-food, defense, stablecoin, superconductors.",
            "2. Large sector: the fixed 12 large-sector drawers.",
            "3. Base theme archetype: Round-10 theme map, roughly 65 current rows in this repo.",
            "4. Deep sub-archetype: later-round lenses for score-weight and price-path validation.",
            "5. Case library: success, watch, false positive, 4B, and 4C examples.",
            "6. Price-path validation: stage dates, MFE/MAE, drawdown, and score-price alignment.",
            "",
            "## Guardrail",
            "",
            "A label can route research, but it cannot create a score by itself. For example, `AI server` can route the agent to ODM/EMS checks, but Stage 3-Green still needs OP/EPS, margin, inventory, customer, and trust evidence.",
        ]
    ) + "\n"


def render_round39_green_policy_rollup_markdown() -> str:
    rows = round39_deep_sub_archetype_rows()
    green = [row for row in rows if row["posture"] == Round10ThemePosture.GREEN_POSSIBLE.value]
    watch = [row for row in rows if row["posture"] == Round10ThemePosture.WATCH_YELLOW_FIRST.value]
    red = [row for row in rows if row["posture"] == Round10ThemePosture.REDTEAM_FIRST.value]
    lines = [
        "# Round-39 Green Policy Rollup",
        "",
        "## Green-Possible Deep Lenses",
        "",
        *[f"- `{row['label']}`: {row['evidence_focus']}" for row in green],
        "",
        "## Watch-to-Green Deep Lenses",
        "",
        *[f"- `{row['label']}`: {row['evidence_focus']}" for row in watch],
        "",
        "## RedTeam-First Deep Lenses",
        "",
        *[f"- `{row['label']}`: {row['risk_focus']}" for row in red],
        "",
        "## What Not To Change",
        "",
        "- Do not add new large sectors for every new theme.",
        "- Do not use deep sub-archetype labels as candidate-generation evidence.",
        "- Do not apply score weights from the case library before price-path validation.",
        "- Do not lower Stage 3-Green thresholds because a deep sub-archetype looks attractive.",
    ]
    return "\n".join(lines) + "\n"


def render_round39_price_validation_next_steps_markdown() -> str:
    return "\n".join(
        [
            "# Round-39 Price-Path Validation Next Steps",
            "",
            "## Immediate cleanup",
            "",
            "1. Keep the 12 large-sector map fixed.",
            "2. Keep Round-10 theme archetypes as the base routing layer.",
            "3. Attach each later-round deep sub-archetype to a parent large sector and canonical archetype.",
            "4. Sort cases_vXX by parent/sub-archetype.",
            "5. Backfill stage-date and OHLCV paths only from source data.",
            "",
            "## Validation metrics",
            "",
            "- Stage 1/2/3 date candidate",
            "- MFE_90D / 180D / 1Y / 2Y",
            "- MAE_90D / 180D",
            "- drawdown_after_peak",
            "- EPS revision duration",
            "- valuation band change",
            "- hard 4C event drawdown where applicable",
            "",
            "## Example",
            "",
            "`AI_DATA_CENTER_INFRASTRUCTURE` is a parent. Under it, HBM, AI server ODM, neocloud, cooling, optical networking, gases, and power equipment each need separate validation because their margins, debt, customer concentration, and 4C risks differ.",
        ]
    ) + "\n"


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> Path:
    row_tuple = tuple(rows)
    if not row_tuple:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(row_tuple[0].keys()))
        writer.writeheader()
        for row in row_tuple:
            writer.writerow(row)
    return path


__all__ = [
    "ROUND39_DEEP_SUB_ARCHETYPES",
    "ROUND39_DEFAULT_DEEP_REGISTRY_PATH",
    "ROUND39_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND39_SOURCE_ROUND_PATH",
    "Round39DeepSubArchetype",
    "render_round39_green_policy_rollup_markdown",
    "render_round39_layer_model_markdown",
    "render_round39_price_validation_next_steps_markdown",
    "render_round39_summary_markdown",
    "round39_base_theme_count",
    "round39_deep_sub_archetype_rows",
    "round39_large_sector_rows",
    "round39_summary",
    "write_round39_taxonomy_reports",
]

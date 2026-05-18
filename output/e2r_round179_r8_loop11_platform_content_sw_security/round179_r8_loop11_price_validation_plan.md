# Round-179 R8 Loop-11 Price Validation Plan

## Method

1. Assign stage dates only from source evidence.
2. Store stage-date close prices from official price data.
3. Calculate 20D/60D/120D/252D returns and MFE/MAE after Stage 2.
4. Compare AI/cloud/IP/platform headlines with ARR, bookings, cloud revenue, ad revenue, paid content, live-service revenue, OPM, FCF, retention, security, legal, and guidance events.
5. Keep missing stage prices and MFE/MAE null until official price backfill is available.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case` | `ENTERPRISE_AI_CLOUD_INFRA_KOREA` | 2026-04-15 | needs_ai_arr_cloud_revenue_cb_dilution_price_backfill |
| `douzone_bizon_eqt_erp_workflow_stage2_3_case` | `B2B_SAAS_ERP_WORKFLOW_KOREA` | 2025-11-07 | needs_arr_churn_opm_price_backfill |
| `naver_hyperclova_x_sovereign_ai_stage1_2_case` | `SOVEREIGN_KOREAN_AI_MODEL` | undated | needs_b2b_api_cloud_revenue_arpu_price_backfill |
| `shiftup_game_ip_repeat_monetization_4b_watch_case` | `GAME_CONTENT_IP_REPEAT_MONETIZATION` | 2025-06-01 | needs_bookings_retention_opm_price_backfill |
| `krafton_pubg_bgmi_india_inzoi_stage2_3_4c_watch_case` | `GAME_CONTENT_IP_REPEAT_MONETIZATION` | 2025-12-19 | needs_bookings_opm_legal_price_backfill |
| `sm_tencent_music_china_reopening_kpop_stage2_case` | `KPOP_PLATFORM_CONTENT_IP` | 2025-05-27 | needs_touring_fan_arpu_opm_price_backfill |
| `hybe_founder_legal_risk_kpop_cap_case` | `ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY` | 2026-04-21 | needs_legal_resolution_price_backfill |
| `webtoon_ipo_guidance_miss_4c_watch_case` | `WEBTOON_PLATFORM_IP_MONETIZATION` | 2026-05-01 | needs_webtoon_price_guidance_backfill |
| `naver_line_privacy_security_governance_4c_watch_case` | `PLATFORM_PRIVACY_SECURITY_OVERLAY` | 2024-08-02 | needs_platform_event_price_backfill |
| `kakao_founder_legal_overhang_relief_case` | `ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY` | 2025-10-21 | needs_legal_event_price_backfill |
| `krafton_subnautica2_delay_lawsuit_4c_watch_case` | `GAME_IP_LAUNCH_DELAY_LEGAL_RISK` | 2026-07-01 | needs_release_legal_price_backfill |
| `r8_disclosure_confidence_cap_case` | `DISCLOSURE_CONFIDENCE_CAP` | undated | needs_arr_bookings_opm_legal_detail_backfill |

## Alignment Labels

- `AI_CLOUD_CB_STAGE2_NOT_GREEN`: strategic investor and AI option are Stage 2 until AI ARR/revenue confirms.
- `ERP_WORKFLOW_REQUIRES_ARR_CHURN_OPM`: ERP/SaaS needs repeat economics.
- `WEBTOON_GUIDANCE_MISS_BLOCKS_GREEN`: IPO platform premium is broken by weak guidance.
- `GAME_IP_REPEAT_REVENUE_NEEDS_LEGAL_SPLIT`: bookings and legal/release risk must be separated.
- `PRIVACY_SECURITY_GOVERNANCE_GATE`: data leak/regulatory pressure blocks platform Green.

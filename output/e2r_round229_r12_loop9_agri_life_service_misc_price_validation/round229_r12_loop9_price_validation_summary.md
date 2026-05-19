# Round 229 R12 Loop 9 Agri Life Service Misc Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_229.md
- raw_large_sector_label: AGRI_LIFE_SERVICE_MISC
- mapped_large_sector: EDUCATION_LIFE_AGRI_MISC
- cases: 8
- success_candidate: 3
- event_premium: 3
- failed_rerating: 1
- overheat: 1
- price_moved_without_evidence: 1
- Stage 3 dated cases: 0
- 4B-watch cases: 8
- hard_4c_case_count: 0
- deep_sub_archetype_count: 8
- shadow_weight_row_count: 8
- r12_default_stage3_bias: conservative_except_recurring_service
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage2 | stage3 | 4B | 4C | round alignment | note |
|---|---|---|---|---|---|---|---|---|
| r12_loop9_coway_recurring_rental_watch | 코웨이 | success_candidate |  |  |  |  | success_candidate | R12에서 가장 구조적인 recurring-service 후보지만 rental accounts, churn, ARPU, OPM/FCF, OHLC 확인 전 Stage 3는 보류한다. |
| r12_loop9_ktng_regulated_cashflow_watch | KT&G | success_candidate |  |  |  |  | success_candidate | Regulated cashflow 후보지만 주주환원·HNB 성장·volume decline·규제 리스크와 OHLC 확인 전 Green 금지다. |
| r12_loop9_daedong_tym_agri_machinery_watch | 대동/TYM | success_candidate |  |  |  |  | unknown_insufficient_evidence | 농기계 export와 자율주행 농기계 narrative는 dealer sell-through, inventory, farmer financing, OPM 전 Green 금지다. |
| r12_loop9_megastudy_medical_quota_policy | 메가스터디교육/교육주 | event_premium | 2026-02-01 |  |  |  | event_premium | 의대정원 정책은 routing signal이다. 실제 수강생·ARPU·OPM 전 Stage 3가 아니다. |
| r12_loop9_edtech_phone_ban_policy_watch | 교육/에듀테크 basket | failed_rerating |  |  |  | 2026-03-01 | policy_watch | 교실 휴대전화 금지법은 오프라인 discipline에는 우호적일 수 있지만 디지털 학습 플랫폼에는 friction이다. |
| r12_loop9_poultry_bird_flu_import_event | poultry basket | event_premium |  |  |  | 2025-06-23 | event_premium | 질병 이벤트는 one-off다. 수입제한 완화나 bird-flu-free recognition이 event fade trigger다. |
| r12_loop9_kyochon_jensen_chicken_event | fried chicken event basket | overheat |  |  | 2025-10-31 |  | price_moved_without_evidence | Jensen Huang 치킨 이벤트는 매출·마진 증거가 아니라 celebrity/viral event premium이다. |
| r12_loop9_smart_farm_unit_economics_watch | 스마트팜 basket | event_premium |  |  |  |  | unknown_insufficient_evidence | 스마트팜은 장기 테마지만 commercial installation·unit economics·반복서비스 전 Green 금지다. |

## Interpretation
- R12 default is Stage 1/2 watch or event premium, except recurring-service evidence can become a stronger candidate.
- Coway and KT&G remain structural candidates, but accounts, churn, ARPU, FCF, shareholder return, and regulation must be verified.
- Daedong/TYM needs dealer sell-through, inventory, farmer financing, OPM, and FCF.
- Medical-quota and classroom-device policy are routing signals, not company Green evidence.
- Poultry disease and Jensen chicken events are one-off/event-premium examples.
- Smart-farm technology metrics are not company revenue or unit-economics evidence.

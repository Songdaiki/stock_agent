# Checkpoint 28A Round 183 - R12 Loop 11 Agriculture / Life Services / Misc

## Summary

Round 183 반영으로 R12 농업·생활서비스·기타 섹터의 국장 중심 Loop 11 보정팩을 추가했다.

핵심 원칙은 단순하다.

```text
농업, 질병 수혜, 의대정원, AI 교육, 전자담배, 키즈 IP라는 이름만으로는 Stage 3가 아니다.
반복매출, 수주/규제승인, 판가전가, unit economics, OPM/FCF, 법적/규제 안정이 확인돼야 한다.
```

예를 들면 핑크퐁 IPO의 +62% 장중 상승은 강한 가격경로 신호다. 하지만 `Baby Shark` 의존도가 높고 IPO 프리미엄이 크면 Stage 3-Green이 아니라 `Stage 2 strong + 4B-watch`로 식혀야 한다.

## Files Added

- `src/e2r/sector/round183_r12_loop11_agri_life_misc.py`
- `src/e2r/cli/build_round183_r12_loop11_report.py`
- `tests/test_round183_r12_loop11_agri_life_misc.py`
- `data/e2r_case_library/cases_r12_loop11_round183.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round183_r12_loop11_v11.csv`
- `output/e2r_round183_r12_loop11_agri_life_misc/`

## Archetypes Added

- `AGRI_MACHINERY_EXPORT_CYCLE_KOREA`
- `AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION`
- `FERTILIZER_INPUT_PRICE_COST_KOREA`
- `LIVESTOCK_DISEASE_PRICE_EVENT_KOREA`
- `FEED_GRAIN_COST_PASS_THROUGH`
- `TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK`
- `CONSUMER_REGULATED_PRODUCT_KOREA`
- `HEATED_TOBACCO_GLOBAL_DISTRIBUTION`
- `EDUCATION_POLICY_EVENT_KOREA`
- `EDTECH_AI_DISRUPTION_KOREA`
- `KIDS_IP_PLATFORM_KOREA`
- `SMART_FARM_UNIT_ECONOMICS_KOREA`
- `SERVICE_KIOSK_LOCAL_REGULATION_KOREA`

## Case Pack

- canonical targets: 14
- case candidates: 15
- Green-eligible but gated: `CONSUMER_REGULATED_PRODUCT_KOREA`
- Watch/Yellow-first examples: 대동/TYM, KT&G heated tobacco, 메가스터디교육, 핑크퐁
- RedTeam-first examples: 육계 질병 이벤트, AI tutor disruption, disclosure confidence cap

Key cases:

- `pinkfong_ipo_stage2_4b_watch_case`: Stage 2 strong + 4B-watch
- `ktng_lil_heated_tobacco_distribution_case`: regulated repeat-consumption Stage 2/3 candidate
- `daedong_tym_agri_machinery_export_stage2_candidate_case`: 농기계 수출 Stage 2 candidate
- `megastudy_medical_quota_policy_event_case`: 의대정원 정책 Stage 1/2 event
- `dongwon_starkist_settlement_legal_4c_watch_case`: 글로벌 참치 브랜드 + legal 4C-watch

## Guardrails

- production scoring/staging/red-team 로직은 변경하지 않았다.
- case records는 candidate-generation input이 아니다.
- Stage price, MFE/MAE, OPM/FCF, unit economics, 반복매출, 규제승인 범위는 만들지 않는다.
- OpenDART list-only evidence는 Stage 3 근거가 아니다. watch disclosure에 한해 detail fetch가 필요하다.

## Verification

```bash
PYTHONPATH=src python -m unittest tests.test_round183_r12_loop11_agri_life_misc -v
PYTHONPATH=src python -m e2r.cli.build_round183_r12_loop11_report
```

Both passed locally before the full-suite verification step.

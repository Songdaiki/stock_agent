# Round 217 R13 Green Gate Review

Do not apply these weights to production scoring yet.

## Required Fields

- company_level_evidence_confirmed
- revenue_eps_fcf_path_confirmed
- price_path_after_evidence_confirmed
- meaningful_stage3_mfe_confirmed
- mae_not_excessive
- not_saturated_4b
- no_hard_redteam
- contract_operational_governance_trust_passed

## Forbidden Patterns

- policy_news_only
- resource_estimate_without_commerciality
- stablecoin_policy_theme_only
- ai_capex_or_partnership_without_revenue
- contract_headline_without_calloff
- mou_or_preliminary_deal
- governance_premium_only
- dilution_without_clear_fcf
- high_score_without_price_validation
- price_rally_before_evidence

## Shadow Score Adjustments

| axis | direction | points | reason |
|---|---|---:|---|
| price_path_alignment | raise | 5 | Stage 3 이후 가격경로가 증거와 맞으면 보상한다. |
| stage3_to_large_mfe_confirmation | raise | 5 | 대형 MFE가 확인된 Stage 3 성공 사례를 보상한다. |
| order_to_revenue_conversion | raise | 5 | 수주 headline보다 납품·매출·OP revision 전환을 우선한다. |
| eps_fcf_revision | raise | 5 | OP/EPS/FCF revision이 Stage 3의 몸통이다. |
| actual_contract | raise | 5 | 실제 계약과 납품 경로가 있으면 visibility가 올라간다. |
| customer_visibility | raise | 4 | 고객과 공급 visibility가 가격경로와 맞을 때 보상한다. |
| operational_trust | raise | 5 | 운영 신뢰는 Green의 필수 통과 gate다. |
| hard_4c_early_warning | raise | 5 | 계약취소·안전사고·신뢰 훼손은 hard 4C로 조기 감지한다. |
| contract_quality | raise | 5 | 계약금액 headline보다 call-off, take-or-pay, margin, FCF를 확인한다. |
| policy_news_only | lower | -5 | 정책 뉴스만으로 Green을 만들지 않는다. |
| resource_estimate_without_commerciality | lower | -5 | 자원 추정은 상업성 전까지 event premium이다. |
| stablecoin_policy_theme_only | lower | -5 | 스테이블코인 정책 기대는 실제 수익모델 전까지 감점한다. |
| ai_capex_or_partnership_without_revenue | lower | -4 | AI 투자·협업은 매출과 마진 전까지 Stage 2 watch다. |
| contract_headline_without_calloff | lower | -5 | call-off 없는 계약 headline은 Green 충분조건이 아니다. |
| mou_or_preliminary_deal | lower | -5 | MOU·예비계약은 실제 계약 전 Green 금지다. |
| governance_premium_only | lower | -5 | 지배구조 이벤트 프리미엄만으로 구조적 rerating을 주지 않는다. |
| dilution_without_clear_fcf | lower | -4 | FCF 설명 없는 증자·희석은 4B/RedTeam 감점이다. |
| high_score_without_price_validation | lower | -5 | 높은 shadow score도 가격경로 검증 전에는 보류한다. |

## Easy Examples
- `HBM 수요 + OP revision + 이후 가격경로`는 Stage 3 성공 검증이다.
- `동해 가스 가능성 + 당일 +30%`는 상업성 전 가격 선행 이벤트다.
- `계약 취소 또는 fatal accident`는 구조가 좋아도 hard 4C다.

# Round-204 R13 Loop-7 Green Gate Review

## Green Required Evidence

- `cross_evidence_confirmed`
- `eps_fcf_durability_confirmed`
- `structural_visibility_confirmed`
- `price_path_alignment_confirmed`
- `not_price_only_rally`
- `no_hard_redteam`
- `not_saturated_4b`
- `revenue_or_eps_conversion_confirmed`

## Green Forbidden Patterns

- `policy_news_only`
- `resource_estimate_without_commerciality`
- `ai_capex_or_partnership_without_revenue`
- `contract_headline_without_calloff`
- `media_or_event_price_rally`
- `high_score_without_price_validation`
- `past_winner_similarity`
- `price_rally_before_evidence`
- `saturated_4b`
- `hard_redteam`

## Shadow Score Adjustments

| axis | direction | points | reason |
| --- | --- | ---: | --- |
| `price_path_alignment` | raise | 5 | Stage 3 이후 실제 대형 MFE가 확인된 케이스를 보상한다. |
| `stage3_to_large_mfe_confirmation` | raise | 5 | SK하이닉스와 한화에어로스페이스처럼 Stage 3 이후 큰 가격경로가 확인되어야 한다. |
| `cross_evidence` | raise | 4 | 섹터별 증거가 가격경로와 RedTeam을 함께 통과해야 한다. |
| `eps_fcf_durability` | raise | 4 | 대형 rerating은 EPS/FCF 지속성이 확인되어야 한다. |
| `contract_quality` | raise | 5 | 계약 cancellation과 value collapse를 피하려면 계약 질을 강하게 봐야 한다. |
| `capacity_bottleneck` | raise | 4 | HBM/방산 같은 성공 케이스는 병목과 visibility가 같이 있었다. |
| `customer_visibility` | raise | 4 | 고객 수요와 납품/공급 visibility가 Stage 3 이후 MFE를 설명한다. |
| `operational_trust` | raise | 5 | 제주항공 같은 operational trust break는 hard 4C 기준점이다. |
| `hard_4c_early_warning` | raise | 5 | 계약취소·안전사고·공시신뢰 훼손은 빠르게 hard 4C로 잡아야 한다. |
| `policy_news_only` | lower | -5 | 정책 뉴스만으로 Stage 3-Green을 만들지 않는다. |
| `resource_estimate_without_commerciality` | lower | -5 | 자원 추정은 상업성 확인 전까지 price-only event다. |
| `ai_capex_or_partnership_without_revenue` | lower | -4 | AI 투자·파트너십은 매출과 마진 전까지 Stage 2 watch다. |
| `contract_headline_without_calloff` | lower | -5 | 계약 headline은 call-off/GWh/margin 전까지 Green 충분조건이 아니다. |
| `media_or_event_price_rally` | lower | -5 | 언론/이벤트 급등은 evidence-before-price가 아니면 4B-watch 우선이다. |
| `high_score_without_price_validation` | lower | -5 | 높은 점수도 가격경로·4B·4C 검증을 통과해야 한다. |
| `past_winner_similarity` | lower | -4 | 과거 성공 종목과 닮았다는 이유만으로 Green을 만들지 않는다. |

## What Not To Change

- Do not apply these weights to production scoring yet.
- Do not use Round204 cases as candidate-generation input.
- Do not lower Stage 3-Green thresholds to force promotion.
- Do not invent full OHLC, stage prices, or MFE/MAE when only reported anchors exist.
- Do not treat price-only rallies, policy events, AI partnership/capex plans, or contract headlines as Green evidence alone.

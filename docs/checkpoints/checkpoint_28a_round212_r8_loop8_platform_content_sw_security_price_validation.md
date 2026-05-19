# Checkpoint 28A Round 212 R8 Loop 8 Platform Content Software Security Price Validation

## 목적

라운드212는 R8 플랫폼·콘텐츠·소프트웨어·보안 가격경로 검증 팩이다.

핵심 원칙은 단순하다. `AI 제휴`, `IPO`, `M&A`, `신작 첫 주 판매`, `MAU 성장`은 Stage 1~2 후보를 만들 수 있지만, Stage 3-Green은 반복매출, ARR proxy, paid usage, bookings, OPM, FCF, churn 안정, operational trust가 확인된 뒤에만 가능하다.

예를 들면 카카오는 OpenAI 제휴만으로 Green이 될 수 없다. 실제 유료 AI 사용, ARPU 상승, 광고·커머스 수익화, OPM/FCF 개선이 확인되어야 한다.

## 반영 내용

- `src/e2r/sector/round212_r8_loop8_platform_content_sw_security_price_validation.py` 추가
- `src/e2r/cli/build_round212_r8_loop8_report.py` 추가
- `tests/test_round212_r8_loop8_platform_content_sw_security_price_validation.py` 추가
- R8 Loop 8 케이스 7개를 calibration-only case record로 구조화
- Reuters / FT / MarketWatch / Investopedia / AP의 reported anchor를 사용해 계산 가능한 값만 반영
- production scoring과 candidate generation은 변경하지 않음

## 케이스 요약

| case | 판단 | Stage 3 처리 |
|---|---|---|
| 더존비즈온 | B2B SaaS / EQT Stage 2 | ARR·churn·OPM·FCF 전 보류 |
| 삼성SDS | KKR/AI capital allocation Stage 2 + 4B-watch | AI revenue conversion 전 보류 |
| LG CNS | cloud/AI IPO evidence good but price failed | recurring revenue·margin·FCF 전 보류 |
| NAVER/Webtoon | Webtoon IPO / IP monetization watch | paid content·ARPU·FCF 전 보류 |
| 카카오 | OpenAI partnership price moved without evidence | paid AI usage·ARPU·OPM 전 보류 |
| 크래프톤 | inZOI + ADK IP Stage 2 | retention·repeat bookings 전 보류 |
| HYBE | governance/legal 4C-watch | warrant decline으로 hard 4C는 보류 |

## Green Gate

R8 Stage 3-Green 필수 조건:

- recurring_revenue_or_bookings
- arr_proxy_or_paid_usage
- arpu_or_take_rate_conversion
- opm_or_gross_margin_improvement
- fcf_conversion
- customer_retention_or_churn_stability
- ip_monetization_beyond_single_launch
- ai_feature_converts_to_paid_revenue_or_cost_saving
- privacy_security_governance_risk_passed
- price_path_after_evidence

Green 금지 패턴:

- ai_partnership_headline_only
- ai_infra_capital_plan_only
- mau_without_arpu
- ipo_debut_premium_only
- mna_without_integration
- game_launch_first_week_only
- single_ip_dependence
- founder_legal_risk
- security_or_privacy_incident
- price_moved_before_monetization

## 4B / 4C 보정

4B-watch는 AI 제휴 발표 직후 급등, AI 인프라·KKR·M&A 기대만으로 20%급 상승, IPO 프리미엄, Webtoon/IP valuation이 paid monetization보다 먼저 확장되는 경우, 신작 첫 주 판매가 retention보다 먼저 가격에 반영되는 경우에 붙인다.

Hard 4C는 privacy breach, security outage, founder/legal break, regulatory sanction, ARR churn spike, paid user decline, game launch failure, IP litigation, M&A integration failure, single-IP collapse, FCF deterioration from AI capex처럼 원문과 날짜가 명확할 때만 확정한다.

## 산출물

- `data/e2r_case_library/cases_r8_loop8_round212.jsonl`
- `data/sector_taxonomy/round212_r8_loop8_platform_content_sw_security_price_validation_audit.json`
- `output/e2r_round212_r8_loop8_platform_content_sw_security_price_validation/round212_r8_loop8_price_validation_summary.md`
- `output/e2r_round212_r8_loop8_platform_content_sw_security_price_validation/round212_r8_loop8_case_matrix.csv`
- `output/e2r_round212_r8_loop8_platform_content_sw_security_price_validation/round212_r8_loop8_score_adjustments.csv`
- `output/e2r_round212_r8_loop8_platform_content_sw_security_price_validation/round212_r8_loop8_green_gate_review.md`
- `output/e2r_round212_r8_loop8_platform_content_sw_security_price_validation/round212_r8_loop8_stage4b_4c_review.md`

## 검증

라운드212 전용 테스트와 전체 테스트를 실행한다.

```bash
PYTHONPATH=src python -m unittest tests.test_round212_r8_loop8_platform_content_sw_security_price_validation -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

## 결론

라운드212는 R8에서 false positive가 쉽게 쌓이는 지점을 분리했다. AI, 웹툰, 게임, K-pop, IPO, M&A가 뜨거운 테마여도 반복매출과 FCF가 확인되기 전에는 Green으로 올리지 않는다.

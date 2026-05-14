# Round-9 Case Record Pack Framework

Source round: `docs/round/round_09.md`

Round 9 confirms that the Round 1-8 synthesis is represented as case records, not production scoring.

## Large Sectors

| large_sector | role | archetypes |
|---|---|---:|
| 산업재/수주 | 전력기기, 방산, 조선, 원전, 산업재 | 4 |
| AI/반도체/데이터센터 | 메모리, HBM, 반도체 장비, PCB, IDC, 냉각, 전력망 | 3 |
| 수출소비재/브랜드 | K푸드, K뷰티, 의료기기, 브랜드 소비재 | 3 |
| 금융/자본배분 | 은행, 보험, 증권, 지주사, value-up | 3 |
| 사이클/스프레드 | 해운, 정유, 화학, 철강, 원자재 | 4 |
| 플랫폼/IP/서비스 | 플랫폼, 게임, 콘텐츠, 교육, 특수서비스 | 4 |
| 바이오/헬스케어 | pre-revenue biotech, royalty biotech, CDMO, 의료기기 | 4 |
| 내수/리오프닝 | 리테일, 면세, 카지노, 항공, 여행 | 2 |
| 부동산/신용 | 건설, PF, 리츠, 신용위험 | 2 |
| 테마/일회성/과열 | one-off demand, theme overheat, price-only rally | 2 |

## Archetype View

- round9_archetype_view_count: 32
- `ONE_OFF_OR_THEME_RISK` is a reporting alias only. Production logic keeps one-off and theme-overheat separate.

## Guardrails
- Do not use case records as candidate-generation input.
- Do not apply score_weight_hint to live scoring yet.
- Do not fabricate missing stage dates or prices.

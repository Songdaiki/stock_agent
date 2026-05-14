# Round-16 Score-Weight Groups v0.5

## CONTRACT_BACKLOG_GREEN
- posture: `GREEN_POSSIBLE`
- examples: `전력설비`, `전선-케이블`, `방산`, `조선`
- weights: EPS/FCF 20, Visibility 24, Bottleneck 22, Mispricing 12, Valuation 12, Capital Allocation 0
- interpretation: Contract/backlog evidence can support Green only with quality, margin, and EPS/FCF revision.

## AI_DATA_CENTER_INFRA_GREEN
- posture: `GREEN_POSSIBLE`
- examples: `AI 데이터센터`, `전력망`, `PCB`, `냉각시스템`
- weights: EPS/FCF 22, Visibility 23, Bottleneck 20, Mispricing 14, Valuation 12, Capital Allocation 0
- interpretation: AI infrastructure needs orders, bottleneck evidence, and revision support.

## K_FOOD_BEAUTY_GREEN
- posture: `GREEN_POSSIBLE`
- examples: `라면`, `K-푸드`, `K뷰티`, `화장품 OEM`
- weights: EPS/FCF 22, Visibility 23, Bottleneck 12, Mispricing 16, Valuation 13, Capital Allocation 0
- interpretation: Export consumer/beauty evidence comes from channel, repeat demand, OPM, and revisions.

## MEMORY_HBM_GREEN
- posture: `GREEN_POSSIBLE`
- examples: `HBM`, `반도체-HBM`, `종합반도체`
- weights: EPS/FCF 24, Visibility 21, Bottleneck 19, Mispricing 15, Valuation 12, Capital Allocation 0
- interpretation: HBM needs multi-year demand, price/capacity discipline, and medium-term revision.

## CDMO_MEDICAL_DEVICE_GREEN
- posture: `GREEN_POSSIBLE`
- examples: `CMO`, `바이오시밀러`, `미용기기`, `임플란트`
- weights: EPS/FCF 20, Visibility 24, Bottleneck 13, Mispricing 14, Valuation 12, Capital Allocation 0
- interpretation: CDMO/medical device Green requires contract/utilization or repeat consumable revenue.

## FINANCIAL_INSURANCE_GREEN
- posture: `GREEN_POSSIBLE`
- examples: `은행`, `손해보험`, `생명보험`, `밸류업`
- weights: EPS/FCF 15, Visibility 20, Bottleneck 5, Mispricing 15, Valuation 25, Capital Allocation 10
- interpretation: Financial rerating depends on ROE/PBR, capital strength, and executed return.

## PLATFORM_SOFTWARE_WATCH
- posture: `WATCH_YELLOW_FIRST`
- examples: `클라우드 컴퓨팅`, `AI 소프트웨어`, `IT보안`
- weights: EPS/FCF 20, Visibility 22, Bottleneck 8, Mispricing 16, Valuation 14, Capital Allocation 0
- interpretation: Platform/SW is Watch until monetization, recurring revenue, and margin leverage are visible.

## ROBOTICS_WATCH
- posture: `WATCH_YELLOW_FIRST`
- examples: `피지컬AI`, `휴머노이드`, `제조용 로봇`
- weights: EPS/FCF 18, Visibility 15, Bottleneck 10, Mispricing 12, Valuation 10, Capital Allocation 0
- interpretation: Robotics requires revenue conversion before high-conviction treatment.

## NUCLEAR_POLICY_WATCH
- posture: `WATCH_YELLOW_FIRST`
- examples: `원자력`, `SMR`, `스마트그리드`
- weights: EPS/FCF 18, Visibility 22, Bottleneck 8, Mispricing 14, Valuation 12, Capital Allocation 0
- interpretation: Nuclear/policy themes need binding contracts and low legal risk.

## AUTO_COMPONENTS_WATCH
- posture: `WATCH_YELLOW_FIRST`
- examples: `현대차`, `기아`, `타이어`, `자율주행`
- weights: EPS/FCF 20, Visibility 18, Bottleneck 10, Mispricing 15, Valuation 17, Capital Allocation 0
- interpretation: Auto needs mix, customer diversification, cost control, and sometimes shareholder return.

## RETAIL_ECOMMERCE_WATCH
- posture: `WATCH_YELLOW_FIRST`
- examples: `편의점`, `홈쇼핑`, `마켓컬리`, `콜드체인`
- weights: EPS/FCF 18, Visibility 16, Bottleneck 5, Mispricing 14, Valuation 14, Capital Allocation 0
- interpretation: Retail/e-commerce needs OPM and FCF, not traffic or listing events alone.

## DIGITAL_ASSET_WATCH
- posture: `WATCH_YELLOW_FIRST`
- examples: `STO`, `스테이블코인`, `결제서비스`
- weights: EPS/FCF 16, Visibility 18, Bottleneck 8, Mispricing 16, Valuation 12, Capital Allocation 0
- interpretation: Digital finance is Watch until regulation, volume, and fee economics are real.

## SHIPPING_FREIGHT_REDTEAM
- posture: `REDTEAM_FIRST`
- examples: `해운`, `운임`, `종합물류`
- weights: EPS/FCF 20, Visibility 10, Bottleneck 18, Mispricing 8, Valuation 8, Capital Allocation 0
- interpretation: Shipping can explode cyclically, so Green is highly restricted.

## COMMODITY_CHEMICAL_REDTEAM
- posture: `REDTEAM_FIRST`
- examples: `화학`, `철강`, `비철금속`, `대두`
- weights: EPS/FCF 20, Visibility 10, Bottleneck 18, Mispricing 10, Valuation 10, Capital Allocation 0
- interpretation: Commodity/spread cases need reversal and oversupply guards.

## BATTERY_OVERHEAT_REDTEAM
- posture: `REDTEAM_FIRST`
- examples: `2차전지 소재`, `전고체 배터리`, `리튬`
- weights: EPS/FCF 20, Visibility 16, Bottleneck 14, Mispricing 10, Valuation 10, Capital Allocation 0
- interpretation: Battery themes require strong overheat and CAPA risk defense.

## CONSTRUCTION_PF_REDTEAM
- posture: `REDTEAM_FIRST`
- examples: `건설사`, `PF`, `건자재`
- weights: EPS/FCF 18, Visibility 10, Bottleneck 8, Mispricing 12, Valuation 10, Capital Allocation 0
- interpretation: Construction is credit-risk first; relief rallies are not structural E2R.

## ONE_OFF_DISEASE_REDTEAM
- posture: `REDTEAM_FIRST`
- examples: `엠폭스`, `코로나19`, `빈대퇴치`, `황사마스크`
- weights: EPS/FCF 20, Visibility 5, Bottleneck 5, Mispricing 5, Valuation 5, Capital Allocation 0
- interpretation: One-off disease/event EPS spikes are usually Red/4B defense material.

## SPECULATIVE_SCIENCE_REDTEAM
- posture: `REDTEAM_FIRST`
- examples: `초전도체`, `맥신`, `그래핀`, `양자 기술`
- weights: EPS/FCF 5, Visibility 5, Bottleneck 5, Mispricing 5, Valuation 5, Capital Allocation 0
- interpretation: Speculative science is Green-blocked until commercialization and revenue exist.

production_scoring_changed: false

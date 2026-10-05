# EJ Deals Competitor Sourcing Brief — China Test-Batch Model
**Created:** Oct 2026 | **Source:** research by agent (Alibaba/AliExpress/1688/made-in-china/Yiwu listings, prices captured Oct 2026)
**Subject:** EJ Deals (Jiji Ghana, Oyarifa-based reseller) — reverse-engineering their China sourcing model
**FX used:** $1 = GHS 15.76

## The Products EJ Sells & What They Likely Pay

**USER CONFIRMED: EJ ships by SEA, not air.** Sea recomputation (45–60d, $2/kg, agent $70 per 20-unit order — in real consolidated orders of 100s of units, agent cost per unit drops below $1):

| # | Product | EJ price | China unit 🔍 | Landed SEA/unit 📊 | Margin SEA 📊 | Verdict |
|---|---|---|---|---|---|---|
| 1 | R36S 64GB console | GHS 650 | $16.50–24.90 (MOQ 1–2) | ~560 | **+90 (16%)** | Workable |
| 2 | Compat drill batteries | GHS 700 | $13.80–18.50 (Makita-type); DeWalt 3Ah $30–36 | ~468 | **+232 (49%)** ✅✅ | WINNER — validates our battery order |
| 3 | Magnetic 72pc set | GHS 400 | $1.75 @1,000 MOQ / $9.63 Yiwu 72pc | ~345 | +55 (16%); at $1.75 bulk ≈ +250 (80%+) | Bulk-only |
| 4 | Faraday pouch | GHS 150 | $0.65–0.91 (MOQ 50) | ~146 (agent-heavy at 20 units) | +4 at 20 units → **50%+ inside consolidated batches** | Consolidation play |
| 5 | Solar 4G dual-lens cam | GHS 780 | $39.99–47.99 (Ubox-type) | ~1,108 | **–328 LOSS even by sea** | AVOID dual-lens at this retail; single-lens ~$25 = breakeven |
| 6 | RC 4WD car | GHS 400 | $3.94–11.72 (Yiwu/1688) | ~263 | **+137 (52%)** ✅ | Strong |

**Assumptions 📊:** sea freight $2/kg (45–60 days); agent $70 flat per 20-unit order; duty+clearing 45% of CIF (Ghana ~20% duty + 15% VAT + NHIL/GETFund/ECOWAS levies — ESTIMATE, verify with clearing agent). EJ's true edge: consolidated multi-product orders spread agent + clearing costs thin, plus likely direct factory pricing below listed B2B prices.

**Strategic read (sea-confirmed):** batteries (+49%) and RC cars (+52%) are the winners; faraday pouches + magnetic sets only pay inside large consolidated orders; solar dual-lens cameras are overpriced at $42 — not viable at GHS 780 retail. Lithium remains regulated by sea too (UN3480/3481, declared, packed to spec) but sea consolidators handle it routinely.

## Search Terms (1688 Chinese / Alibaba-AliExpress English)
1. R36S: `R36S 掌机 游戏机 64GB 批发` / "R36S retro handheld console 64GB ArkOS"
2. Batteries: `电动工具电池 18V 2.0Ah 锂电池 适用于牧田/得伟` / "replacement power tool battery 18V 2Ah/3Ah for Makita/DeWalt"
3. Magnetic: `磁力片 72片 收纳盒 磁性积木` / "magnetic building blocks 72pcs storage box"
4. Faraday: `汽车钥匙 信号屏蔽袋 防盗 RFID` / "faraday pouch car key RFID signal blocker"
5. Solar cam: `太阳能摄像头 4G 双镜头 户外 防水 监控` / "4G solar security camera dual lens IP66"
6. RC car: `遥控车 四驱 充电 2.4G 越野` / "RC car 4WD rechargeable 2.4G"

## Strategic Read
EJ's model = **cheap-light items air-tested, bulk volume sea-shipped** (45–60d, $1.5–2.5/kg).
Air 20-unit tests only clear margin on faraday pouches + batteries. Items 3/5 need sea or 100+ units.
2Real angle: our China battery order (split Daniel + Heshunchang, ~$1,053) covers the same battery
demand at similar unit costs — EJ sells batteries at GHS 700 ≈ our own resale plan GHS 250–350 per
generic slide pack + premium branded-compat at 700. Battery line is CONFIRMED profitable in Ghana.

## Top 3 Risks
1. **Lithium shipping** (items 1,2,5,6): UN3481/UN38.3 + MSDS required; agents refuse or surcharge;
   Ghana clearing delays.
2. **Counterfeit/relabeled batteries**: "genuine Makita" at replacement prices = counterfeit; customs
   seizure risk + cell quality invisible until failure. Require in writing: "new A-grade cells, no brand logo".
3. **Fake certs**: CE self-declared on cheap items; GSA clearance certificates may be needed for
   electronics entering Ghana.

## Pre-Order Checklist
- [ ] Agent accepts UN3481 lithium in writing + air rate/kg for our weight profile
- [ ] Clearing agent confirms actual duty/VAT/levies per category (45% is an estimate)
- [ ] 4G camera bands = B1/B3/B7/B8/B20/B28 (MTN/Vodafone/AirtelTigo Ghana)
- [ ] Supplier vetting: Trade Assurance, verified years, reorder rate, factory video call >$500
- [ ] Test-order quality gates: R36S real 64GB+IPS; battery capacity cycle test + fits original charger;
      faraday = phone-in-bag no ring; solar cam pairs + Ghana SIM registers + panel charges;
      magnet strength; RC runtime ≥20min
- [ ] True landed cost from agent invoice + clearing receipt vs this table

## Related
- Battery sourcing master: `Vault/business/2real/battery-sourcing/BATTERY_SOURCING_SHEET.md`
- Supplier comparison: `battery-sourcing/SUPPLIER_COMPARISON.md`
- Our 332-item gap list & demand data: `2real-agent/christmas_gap_list.json`
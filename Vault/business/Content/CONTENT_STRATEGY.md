# Content Strategy — 2 Real Enterprises & Akoma Robotics

_Last updated: 2026-10-07_
Strategy layer feeding `CONTENT_CALENDAR.md`. Every post maps to a pillar + a mix category. Owns brand voice, audience, and platform fit.

---

## 1. Brand Voice

**2 Real Enterprises (Taiwah Builds):**
- Professional + casual for the Ghanaian trade/DIY builder. Witty, no-nonsense, earns trust.
- "Craft AND business" — never one alone. Cuts through with real numbers (GHC 7.50/month tape maths, the quoting formula).
- CTA: WhatsApp 0204252252 ("order", "claim", "first come, first served" for deals).

**Akoma Robotics:**
- Inspirational + educational. Parent-facing = empowerment/stem future; school-facing (Offer B) = professional partnership.
- Never blend the two offers (two-audience rule). Purple #6A0DAD + gold #FFD700.
- CTA: WhatsApp 0204252252 · ages 7-14 official.

**Shared:** Authentic, real products (never fake), real prices (Jiji-validated). No AI-flavoured corporate fluff. Accra-born.

---

## 2. Target Audience

| Brand | Demographics | Interests | Pain points |
|-------|-------------|-----------|-------------|
| 2 Real | Ghanaian contractors, builders, handymen, DIYers, 25-55, Accra/Dome + nationwide | Tools, tiling, construction, quoting, earning more, site efficiency | Wasted materials/re-dos, under-quoting, cheap tools that fail, unreliable stock |
| Akoma | Parents of kids 7-14 (Offer A); school owners/principals/STEM coordinators (Offer B), Accra + national | STEM education, future-ready kids, after-school, curriculum integration | Kids glued to screens, fear their child falls behind digital age, schools lacking hands-on STEM |

---

## 3. Content Pillars (everything maps to one)

**2 Real (Taiwah Builds):**
1. Craft & Technique (tiling, measuring, tool mastery) — the "TAIWAH BUILDS tested" demos
2. The Business of Building (quoting, margins, quality-as-labour-cost)
3. Product Showcase / Stock (real in-stock, real GHS, Jiji-validated)
4. Deals & Scarcity (Saturday flash sales, "first come, first served")
5. Behind the Scenes / Trust (UK-sourced → Accra warehouse story)

**Akoma:**
1. Inspiring the Future Builder (parent-facing: creator-not-user, resilience, spotlight)
2. STEM Education Case (why robotics in Ghana's basic schools)
3. Course Offer / Parent CTA (10-week, ages 7-14, trial class)
4. School Partnership (Offer B: tiered pricing, turnkey programme) — LinkedIn/outreach only
5. Student Success (9-year-old maze story, failure-is-data)

**Mix ratio guided by:** max 1 promo-heavy post/week/brand; the rest educate, engage, or build trust.

---

## 4. Platform Strategy (frequency + formats + times)

| Platform | Posts/Week | Best Content Types | Best Times (GMT) |
|----------|-----------|--------------------|------------------|
| Instagram | Akoma 3 / 2Real 3 | Reels, carousel, single image | Tue-Fri 10:00-14:00 |
| TikTok | Akoma 3 / 2Real 3 | Reel 15-60s, hook-first | Tue-Thu 19:00-21:00 |
| LinkedIn | Akoma 2 / 2Real 1 | Text post, carousel, article | Tue-Thu 08:00-10:00 |
| Facebook | Akoma 3 / 2Real 3 | Video, image, community Q | Wed-Fri 13:00-16:00 |
| WhatsApp Status | Daily | 9:16 vertical + micro-copy | 08:00 & 18:00 |
| WhatsApp Broadcast | Sun | Weekly roundup | Sun 10:00 |
| Marketplace (Jiji/FB MP) | Per 2Real post (Tue/Thu/Sat) | Itemised multi-item listing | — |

---

## 5. Content Mix Ratio

| Content Type | % | Used for |
|--------------|---|----------|
| Educational | 40% | Thu masterclass, Mon Akoma "how robots see", how-tos, Taiwah tested |
| Engaging | 25% | Fri questions, polls, "ask a robot", comment-for-template hooks |
| Promotional | 20% | Tue product showcase, Sat flash deal (stock+price+scarcity) |
| Personal / BTS | 15% | Behind-the-scenes, warehouse, Taiwah story, student spotlight |

**Balance rule:** Mon-Wed educate + engage; Thu craft+business; Sat convert. Never more than 1 hard-sell per week per brand.

---

## 6. Per-Post Schema (every asset follows this)

```yaml
date: "YYYY-MM-DD"
day: "Monday"
platform: "instagram"
content_type: "reel"          # reel | carousel | single | post | article | broadcast
content_pillar: "Craft & Technique"   # from section 3
mix_category: "Educational"   # Educational|Engaging|Promotional|BTS

caption: |
  Full platform-native caption.
  Hook in first line (Instagram first 125 chars / LinkedIn first line / TikTok hook 1-3s).

hashtags:
  primary: ["#..."]     # 3-5 high-volume
  secondary: ["#..."]
  niche: ["#..."]

image_prompt: "Scene/photo brief ONLY — never describes a logo (face/logo composited later via PIL)."
alt_text: "Screen-reader description"
cta: "WhatsApp 0204252252 — [action: order/claim/book/comment]"
notes: "Stage-check: scheduled|awaiting-publish|published|blocked"
```

## 7. Platform Adaptations (MUST apply per post)

- **Instagram** — Hook in first 125 chars; 20-30 hashtags in first comment, not caption; carousels slide-listed.
- **TikTok** — Caption ≤ 300 chars; 3-5 hashtags; hook in first 1-3s; trending-sound suggestion.
- **LinkedIn** — No hashtags in body (3-5 at bottom); first line is the hook; one sentence per line; professional/data tone.
- **Facebook** — 1-3 hashtags max; questions drive comments; link posts need compelling lead text.
- **WhatsApp Status** — micro-copy + 9:16 visual; readable without sound.
- **Marketplace** — ONE anchor price on the card (headline item), full itemised list in description, "prices per item" disclaimers.

---

## 8. Real-World Context Hooks (authenticity engine)

Pull actual operational events into the plan — a real stock take, an incoming delivery, a warehouse milestone, an order received — before any templated post. Authenticity beats aesthetics.

**Sources to scan before generating (2Real):**
- `Vault/business/2real/` daily-sales-log, stock/inventory updates, delivery log → real "what moved this week" hooks
- Jiji active-listing count / new listings → "unboxing fresh stock" moment
- tasks-queue / SOPs → upcoming deliveries or stock takes to film

**Sources to scan before generating (Akoma):**
- `Vault/business/akoma/` + AKOMA_MASTER.md → student wins, school partnerships, milestone moments
- Recent sessions/briefings → "Key Wins" worth a spotlight
- Program milestones → a completed cohort, a new school partner

**Hook ideas map:**
- 2Real Shop/Retail → product showcase, "fresh stock just landed", customer walk-in, price transparency
- 2Real Warehouse/Process → behind-the-scenes logistics, stock take, packing/fulfilment, "from UK to Accra"
- Akoma → student success, classroom moment, school demo, assembly time-lapse, community win

**Fallback:** if no fresh inventory/ops update is found, anchor to **Warehouse Efficiency** + **Customer Service** pillars (2Real) or **Innovation** + **Community** (Akoma) rather than inventing stock claims.

---

## 9. Planner Personas (mode each plan is written in)

**2Real → "Retail Strategist" mode.** Boots-on-the-ground, transparent, reliable. Visual: industrial-but-clean warehouse shots + vibrant welcoming shop shots. Voice: authentic, "realness" first — real stock, real prices, real process.

**Akoma → "Creative Strategist" mode.** Organized + visionary. Visual cues guide the shoot (e.g. "show internal wiring", "time-lapse of robot assembly", "kids debugging together"). Voice: innovative, community-focused, tech-forward.

---

## Sources / Canonical
- `../content-assets/` (logos, Taiwah master lock — real brand only, no fake logos)
- `akoma-offers` skill (Offer A vs B, tiers) · `multi-brand-content-engine` skill · `CONTENT_CALENDAR.md`
- Jiji primary / Zobaze supplementary stock rule. Ages 7-14 official (AKOMA_MASTER.md).
- Real-world hooks: `Vault/business/2real/` (sales/stock/delivery logs), `Vault/business/akoma/` (master + milestones).
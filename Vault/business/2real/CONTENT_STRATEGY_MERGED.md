# 2Real Content & Sales Strategy — MERGED & SYNCED (single source of truth)

**Owner:** H (CEO) · **Prepared:** Sun 18 Oct 26 · **CTA everywhere:** WhatsApp 0204252252
**Supersedes the divergence between:** `CONTENT_STRATEGY.md` (Sunday-engine organic, multi-platform)
and `CONTENT_STRATEGY_STATUS_CTWA.md` (WhatsApp Status + CTWA). **This file is now canonical.**
Keep `campaign-launch-playbook.md` (timing/budgets) + `1b-setup-checklist.md` (Meta CTWA setup) as companions; this defines **what we do daily**.

---

## 0. THE DECISION (quality over quantity, Meta + Jiji first)

> **We consolidate on what shows validation & traction: Jiji + Meta (FB Marketplace, WA Status, CTWA/FB+IG ads).**
> Quality over quantity: FEWER channels, done WELL, measured by **chats + sales only** (impressions/reactions = noise).
> The broad 8-platform Sunday engine is **scaled back** — IG/TikTok/LinkedIn stay on existing repurposing, not as primary daily labour.

### Focus channels (ranked by traction)
1. **Jiji** — source of truth, inventory, TOP+, bulk/wholesale leads. The foundation.
2. **FB Marketplace** — high-ticket visual; batch poster cron (every 30 min, dedup-safe).
3. **WhatsApp Status** — daily direct-to-buyer; cheapest conversion surface.
4. **Meta CTWA ads** (FB+IG feed/reels → WhatsApp) — paid reach on proven creatives; GHS 25–100/day manual clicks.
5. **WhatsApp groups + FB groups** — FREE distribution into communities (NEW — see §6).

### De-emphasised (repurpose only, no new daily ground work)
Instagram / TikTok / LinkedIn → reuse the week's stills + reels; don't spend planning hours there.

---

## 1. DAILY RHYTHM (the merged loop — what happens every day)

| Day | Content pillar (Status) | Sales action | Who/What |
|---|---|---|---|
| **Mon** | 🛋️ Home & Furniture (Oyarifa photo day) | FB listing refresh; catalog restock | Daily Ops + photo shoot + FB Poster |
| **Tue** | 🔧 Power Tools & Hardware | Status 12:30 & 19:30; Jiji TOP+ rotation | Status cron + Daily Jiji Report |
| **Wed** | 🎮 Gaming & Electronics | CTWA ad set 1 live (Gaming/Kids) | CTWA campaign |
| **Thu** | 🔋 Power, Solar & Inverters | Weekend assets staged; FB listings push; CTWA set 2 (Tools) | Content engine batch + FB Poster |
| **Fri** | 🎁 Kids & Toys | Peak Status + email/broadcast-ready bundle | Status 12:30/19:30 |
| **Sat** | 🔥 Deal of the Day + Gorilla/consumables | **weekend special live** (biggest retail day) | Status + CTWA + FB boost Sat/Sun |
|| **Sun** | **📱 WhatsApp + FB group posts** (ACTIVE — §6 engine) | sunday-content-engine generates group-ready stills + copy + FB catalog push; Jiji recap | **coach** (targeting/first-lines) + sat-nav (assets) + content-buddy + taiwah (copy) |

**Cadence guardrails (merged):**
- CTA **0204252252** everywhere, never the old number.
- **Jiji = source of truth** for every price/stock claim (never Zobaze).
- **Condition honesty** — "UK Pre-Owned, Tested Working" or "Brand New", every post.
- Status at **12:30 & 19:30** (Accra lunch + evening scroll). John's slots +1hr stagger.
- Every sale logged to `daily-sales-log.md` + `customer_leads.json`.
- **Quality gate:** if a post can't show a real item + real price + real condition, don't post it.

---

## 2. BOT ROSTER — who does what (all synced to this plan)

| Bot | Name | Role in the merged strategy |
|---|---|---|
| **CEO bot** | `sat-nav` (me) | Chief of staff: orchestrates the loop, builds/QC assets, runs engine, owns crons + this plan |
| **CEO's mentor** | `coach` | Your personal mentor: networking, WhatsApp/FB **group strategy**, introductions, accountability |
| **OG** | `hermes` | Default/gateway: the master brain + delivery layer |
| **Advertising bot** | `content-buddy` (Kofi) | Captions/copy, publication staging, repurposing, status micro-copy |
| **AI influencer bot** | `taiwah` | Brand voice in-character (2Real tradesperson / Akoma mentor), drafts + hooks |
| **Heavy lifter** | `harold` | Local tools, big renders, local LLM work as needed |

**Division of labor:** content-buddy + taiwah produce; sat-nav builds + QC + runs the loop; coach owns the **newgroup strategy** (§6); harold supports heavy renders (manim/hyperframes).

---

## 3. ASSET SUPPLY CHAIN (one shoot feeds everything — merged)

```
Monday (Oyarifa): photograph 6–10 items
        ↓
content_engine.py generates (Sunday engine / on-demand):
  6 Status posts (pillar-scheduled) + 2 CTWA creatives + FB listing stills + catalog entries
        ↓
H: paste Status 12:30/19:30 · click CTWA setup once (10 min/week) · spot-check Saturday deal
```

**Stills now have 6 layouts** (added 16 Oct: `editorial`, `quote-card`, `split` + original 3) — creative variety so we're not recoloured clones. **Reels** renderable via manim (verified) / hyperframes (Akoma mBot). Best-seller hooks first (Gorilla, power-tools weekend set).

---

## 4. PAID (CTWA + FB boost) — the 1b upgrade

- **CTWA:** one campaign, two ad sets (Gaming/Kids + Tools/Power), GHS 25–100/day, **manual clicks only** (Meta automation ban).
- **Kill metric = chats per cedi, not clicks.** Run 5–7 days before judging; 0-chat ad set after 7d = change creative, not budget.
- **FB Weekend boost:** boost the Sat/Sun weekend-special composite, GHS 50–100/day, Sat+Sun only.
- Scale +20% max / 3–5 days apart; never +30%.
- Setup steps: `1b-setup-checklist.md` (0204252252 → Meta Business Manager, payment method, Publish = H-only).

---

## 5. MEASUREMENT (what counts — the single metric sheet)

| Surface | Metric that counts | Also track |
|---|---|---|
| WhatsApp Status | replies referencing "the status" | condition-honesty rate |
| CTWA | **chats per cedi** per ad set | chats→sale rate |
| FB Marketplace | chats from listings | ROAS on weekend boost |
| FB/WA groups | inbound chatters from the group post | group rule compliance |
| Jiji | chats + TOP+ ROI | new leads to `customer_leads.json` |

**Signals/noise rule (inherited):** chats and sales only. Impressions/reactions = noise.
**Health gate:** blended daily revenue ≥ GHS 1,000.

---

## 6. NEW — WhatsApp Groups + Facebook Groups (FREE distribution)

### Why
You're already in 11 WhatsApp groups that **allow business posts** — this is the cheapest multi-surface reach beyond our own Status/feed. Confirmed cadences from H's group join.

### WhatsApp-group Sundays (the "Sunday multiplier")
- **When:** Sunday is now an **ACTIVE engine day** (no longer Silent). sunday-content-engine generates group-ready stills + copy.
- **General rule (most groups):** 2 posts/day per group. Sunday = catalogue day (unlimited items).
- **Garage Sale (⚠️ stricter):** Sundays only, 1 flyer/link per business ad. 4 pictures max (personal items only). No pets. Follow admin rules strictly.
- **Entrepreneurs Club / Spurs:** No product posts. Network only.
- **Format:** 1 clean photo + item + price + condition + CTA 0204252252.
- **Log every post** to `Vault/business/networking/whatsapp-group-log.md`.
- **Golden rule:** read the group's rules first; if it says "no ads", don't post.

### Facebook Groups strategy
- **Join list:** 6 groups joined (Accra Buy & Sell, Buy & Sell New or Used ACCRA, GHANA MARKET PLACE, Construction Workers in Ghana, Entrepreneurs/Business Owners Ghana, Parents United GH)
- **Post format:** same Sunday cadence as WhatsApp groups; use the week's best still; CTA 0204252252.
- **Anti-spam:** post at group-appropriate times, engage before selling, cap 1–2 group posts/week until known.
- **FB rules to verify:** each group's pinned rules (H to check — login-bound).

### Owner of this
**`coach`** — he owns networking + group strategy (it's literally his SOUL.md). sat-nav supplies the ready-to-post assets (stills + copy); he picks the target groups, drafts the group-specific first line (community-tone, not ad-speak), and logs results to `Vault/business/networking/`.

---

## 7. WHAT H DOES vs WHAT'S AUTOMATED

| Task | Who |
|---|---|
| Paste WhatsApp Status (12:30/19:30) | H (or John +1hr) |
| Click CTWA setup + approve creatives | H (~10 min/week) |
| Approve price drops / new FB groups / discounts | H |
| Join FB groups (login-bound) | H (coach lists them) |
| Status copy, stills, reels, QC, crons, dedup, posting | agents + crons |
| Group targeting + first-line drafts | coach |
| Daily operations check + Jiji report | crons (09:00 / 06:30) |

---

## 8. ONE-WEEK CONCRETE EXAMPLE (what "day X" looks like)

**Thursday 22 Oct (Power/Solar/Inverters pillar):**
1. 06:30 Daily Jiji Report → optimise TOP+ on solar/inverter leads.
2. Morning: content-buddy drafts Thu Status + CTWA set-2 creative; sat-nav renders still (`2real-deal` or `split` UK-vs-Ghana) via engine.
3. 12:30 Status → solar/inverter item + price + condition + CTA; H pastes.
4. FB Poster cron (every 30 min) continues the fresh queue (Jiji-priced).
5. Weekend assets staged for Sat (weekend-special composite + reel).
6. Evening: CTWA set-2 lives (Tools/Power) — H clicked Publish this morning.

---

## 9. THE SYNC (what I reconciled for you)

| Old divergence | Merged decision |
|---|---|
| CONTENT_STRATEGY.md = 8 platforms, heavy daily | **Scale back to Meta+Jiji primary**; others repurpose-only |
| CONTENT_STRATEGY_STATUS_CTWA.md = Status 1/day, CTWA GHS 25 | **Status 2/day (12:30+19:30), CTWA GHS 25–100** as in that file, but full Jiji truth + merged cadence |
| Status Silent Sunday | **Silent Status BUT Sunday = WhatsApp-group + FB-group adverts** (new lever) |
| Sunday engine generates 8 platforms | **Generates the merged pillared set** (Status + CTWA creatives + FB/catalog) under this plan |
| Broadcast retired (Sun) | Repurposed: Sunday group adverts replace broadcast |
| Bots somewhat siloed | **Roster mapped** (§2) so each has a clear role — incl. `coach` owning groups |
| FB/WA posters separate from CTWA | **One daily loop** (§1) feeding all surfaces from one asset set |

**Files this supersedes (point here, not there):** keep CONTENT_STRATEGY.md + CONTENT_STRATEGY_STATUS_CTWA.md as historical/reference; this is canonical. `campaign-launch-playbook.md` (timing) + `1b-setup-checklist.md` (CTWA setup) remain actionable companions.
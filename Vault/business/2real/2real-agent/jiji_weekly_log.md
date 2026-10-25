# Jiji Weekly Performance Log — 2Real Enterprises

## 2026-10-03 (Sat) — Weekly Harvest + Review

**Harvest status:** 🔴 PER-LISTING HARVEST BLOCKED. `jiji_ads_harvest.py` could not run this week —
no browser tooling exists in the scheduled cron session (`browser_exec`/`goto_url`/`js` primitives
absent), and live Jiji capture historically requires a human to approve Chrome remote-debugging /
be logged in as **Two Real Enterprises**. H must run the harvest once interactively to refresh
`jiji_ads_performance.json`.

**Per-listing snapshot on disk is STALE:** scraped 2026-09-01 (1,078 ads) — 32 days old at review.
Totals from that snapshot (context only, NOT current): 241,628 impressions · 33,167 visitors ·
1,247 chats · 150 reverse-flow flags (visits≥20, 0 chats) · 485 ads with ≥1 chat.

**Current account picture — source:** fresh account-overview capture in `jiji_daily_history.json`
(2026-10-03 06:34).

| Metric | 25 Sep | 02 Oct | 03 Oct | WoW Δ |
|--------|--------|--------|--------|------|
| Active listings | 1,140 | 1,266 | **1,272** | **+132** |
| Followers | 332 | 335 | **335** | **+3** |
| Clients | 36 | 36 | **37** | **+1** |
| Declined ads | 1 | 8 | **5** | (spike → +4 to fix) |
| Reviewing | 10 | 0 | 3 | — |
| TOP+ credits | expired 19/09 | — | **renewed → 16/12/26** | ✅ renewed |
| WhatsApp ads | expired 3/09 | active→17/10 | **active→17/10** | ✅ renewed |
| Balance (GHS) | 0 | 0 | **0** | 🔴 persistent |

**Top movers (live, 03 Oct):** Ring 8A Charger (346 imp / 0 chats) · Halfords Chain Lock (251 vis /
2 chats) · Gillette Labs Razor (169 imp / 1 chat).

**Top reverse-flow / fix targets:**
1. **Ring 8A Smart Battery Charger (RSC808)** — 346 imp, 29 visitors, **0 chats** → STRONG flag (≥20 vis, 0 chats). Rename + photo-tweak + price check.
2. **INGCO Tile Cutter 1100mm** — 147 imp, 12 vis, 0 chats (below 20-vis threshold but high reach / no conversion — rework).
3. **5 declined ads** pending resubmission.

**Recommended actions (passed to ops):**
- H run the Jiji harvest once interactively so per-listing data is fresh for next Saturday.
- Rework Ring 8A charger title/photo/price; reply to Halfords Chain Lock (2 chats) + Gillette (1 chat).
- Fix & resubmit 5 declined ads; use 10 available ad discounts.
- Recharge GH¢0 balance to unlock TOP+/pro tools.
## 2026-10-10 (Sat) — Weekly Harvest + Review

**Harvest status:** 🔴 PER-LISTING HARVEST BLOCKED (unchanged since 2026-09-01). `jiji_ads_harvest.py`
(stale on disk, scraped 2026-09-01, 1,078 ads) requires live browser primitives
(`browser_exec`/`goto_url`/`js`) that are NOT present in the unattended cron session — confirmed
via tool catalog this run. H must run the harvest once interactively (logged in as **Two Real
Enterprises**) to refresh per-listing impressions/visitors/chats. Per-listing snapshot is now **39 days old**.

**Current account picture — WoW deltas (source: fresh `jiji_daily_history.json`, latest 2026-10-09):**

| Metric | 03 Oct | 09 Oct | WoW Δ |
|--------|--------|--------|-------|
| Active listings | 1,272 | **1,278** | **+6** |
| Followers | 335 | **336** | **+1** |
| Clients | 37 | **38** | **+1** |
| Declined ads | 5 | **9** | **+4 (spike → fix)** |
| Reviewing | 3 | **1** | −2 |
| Closed | 115 | 115 | 0 |
| TOP+ credits | 500/500 → 16/12/26 | **16/12/26** | ✅ renewed |
| WhatsApp ads | active → 17/10 | **17 Oct 2026** | ✅ renewed |
| Balance (GHS) | 0 | **0** | 🔴 persistent |

**Top movers (09 Oct):** Ring 8A Battery Charger (339 imp / 29 vis / **0 chats**) · INGCO Tile Cutter
(169 imp / 12 vis / **0 chats**) · Gillette Labs Razor (167 imp / 27 vis / 1 chat) · BugClear Ultra 2
(113 imp / 9 vis / 0 chats) · Westland Resolva (106 imp / 7 vis / 0 chats).

**Reverse-flow flags (visits ≥20 OR high-reach, 0 chats — from top-items overview):**
1. **Ring 8A Smart Battery Charger (RSC808)** — 339 imp, 29 visitors, **0 chats** → STRONG flag
   (≥20 vis, 0 chats). Persisted all week (was 346 imp / 29 vis / 0 chats on 03 Oct). Rework title/photo/price.
2. **INGCO Tile Cutter 1100mm** — 169 imp, 12 vis, 0 chats (below 20-vis threshold but high reach / no
   conversion — rework). Impressions UP from 147→169 despite no chats.
3. Halfords Chain Lock (Oct 3: 251 vis / 2 chats) now converting, not flagged.

**Top chats (09 Oct):** Gillette Labs Razor 1 chat · Halfords Chain Lock 2 chats (03 Oct). Engagement
across the shop remains LOW — several high-reach items with zero conversions.

**Needs attention (from 09 Oct capture):** 4 NEW declined ads (9 total) · **19 client messages
unanswered (813/832)** · 43 contact views + 24 saved-ads NOT followed up · GH¢0 balance.

**Recommended actions (passed to ops / John):**
1. **Fix Ring 8A charger** (title/photo/price) — declined impressions 346→339, 0 chats for 2 straight weeks.
2. **Fix & resubmit 4 newly-declined ads** (9 total pending).
3. **Reply to 19 unanswered client chats** + follow up 43 contact views + 24 saved-ads — first reply wins.
4. H run the Jiji harvest once interactively so per-listing data is fresh for next Saturday.
## 2026-10-24 (Sat) — Weekly Harvest + Review

**Harvest status:** ✅ **SUCCESS — fresh per-listing harvest via CDP harvester** (`jiji_ads_harvest_cdp.py`, connected to persistent Chrome :9222, logged in as Two Real Enterprises). Saved **1,250 ads** to `jiji_ads_performance.json` (scraped 2026-10-24 07:02). All 1,250 ads populated with nested totals — no fabricated numbers.

**Account totals (THIS week, live):**
| Metric | Total |
|--------|-------|
| Impressions | 276,530 |
| Visitors | 45,454 |
| Chats | 1,485 |
| Chats/visitors (conversion) | **3.27%** |
| Count-contacts | 1,356 |
| Ads with ≥1 chat | 566 |
| Ads with 0 impressions | **0** (healthy — every active ad has reach) |
| Reverse-flow flags (vis≥20, 0 chats) | **138** |

*(Per-listing WoW baseline unavailable: the only ordered backup (17/10) predates the 19/10 cdp field-extraction fix and holds all-zero totals — not comparable. Account-level WoW below is real from `jiji_daily_history.json`.)*

**TOP-10 by chats:** Panasonic Lumix camera (33c) · LVYUAN power inverter (19c) · Elite Construction Team wanted (18c) · Skateboard (16c) · Female Private Driver (16c) · Mini Guitar Amp 15W (15c) · Xbox 360 games (15c) · Farm Workers (14c) · Live-in Private Nurse (14c) · Wireless Mouse w/LED (13c).

**Top movers / hot items (daily history, 24/10):** Panasonic Lumix camera — 33 chats (hottest item) · LVYUAN Inverter — 19 chats · Facilitator for Child with Autism — 2,606 imp / 334 vis / 7 chats / 13 phone views.

**Reverse-flow fixes (strong flags, vis≥20 & 0 chats):**
1. **Magnum Plus Colossus Security Chain 180cm** — 298 visitors / 389 imp / **0 chats** → rework title/photo/price.
2. **LEGO Harry Potter Knight Bus (COMPLETE)** — 204 visitors / 365 imp / **0 chats** → rework.
3. **ELC Water Wave Pool for Kids** — 163 visitors / 275 imp / **0 chats** → rework.

**Account picture — WoW (source: fresh `jiji_daily_history.json` 24/10):**
| Metric | 17–20 Oct | 24 Oct | WoW Δ |
|--------|-----------|--------|-------|
| Active listings | 1,310 | **1,318** | **+8** |
| Followers | 338 | **339** | **+1** |
| Clients | 1 | **1** | 0 |
| Declined ads | 1–4 | **1** | stable |
| Closed | 130–135 | 130 | 0 |
| WhatsApp ads | expired **17 Oct** | **still expired** | 🔴 blocker |
| Balance (GHS) | 0 | **0** | 🔴 persistent |
| Pro Sales bonus | — | **6,822** | dropping (−200) |

**URGENT action items for H/John:**
1. **Renew WhatsApp ads** — expired since **17 Oct**, never renewed. Direct reach blocker.
2. **Panasonic Lumix camera = 33 chats** — follow up now, hottest item in shop.
3. **Reply to 566 live-thread ads' chats** — first reply wins.
4. **Fix declined Daewoo Cnx+ smartwatch** (open since 21 Oct — switch to Smart Watches category, re-submit).
5. **Rework top-3 reverse-flow items** (Magnum chain, LEGO Knight Bus, ELC pool).
6. GH¢0 balance persists; raise Pro Sales bid (competitors winning flag on profile).


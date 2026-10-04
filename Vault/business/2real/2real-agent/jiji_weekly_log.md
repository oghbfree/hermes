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
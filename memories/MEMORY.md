# MEMORY.md

Durable facts from periodic daily-processing runs.

_facts below are limited to verified findings. Last refreshed: 2026-11-08 22:05 (Nov 8 EOD synthesis)._

## 2026-11-08 Consolidated (Sun, EOD)
- 👵 **Mum: 🔴 REPORT CHANNEL DOWN day 3 — WhatsApp bridge exited 6 Nov 10:17; 6–8 Nov reports missing** (`checkin-mum` fail x3; reconnect attempt 251/300s; needs H foreground QR re-pair — CHANNEL fault). Last data (5 Nov): **BP 126/64 · P 67 · T 36.4 — 5-day clean streak** (2–6 Nov); no 24 Oct episode recurrence. Morning exercise reminder (msg 13142) + afternoon/evening check-ins posted to topic 4 requesting backfill. Open: 25–29 Oct gap · Na labs (161 🚩) · Imodium OUT · **AVS med 2nd sighting (5 Nov 2pm) unidentified + 150ml liquid med** (Dr Morris list) · masseuse Fri 6 Nov UNCONFIRMED (next Tue 10 Nov) · Kenus outcome · BP batteries.
- 🦷 **H (52):** food gap **14d 🔴** (since 25 Oct; 0/7 second week) · Renerve Plus ZERO **41d** (~295 GH Pharmabay) · 31 Aug review **69d** undocumented · labs (1,075 GH) pending · dental unlogged (27d) · no vitals ~76d · ibuprofen daily (AM headache) = GI/kidney risk until labs · 🟢 40d acute-free, tennis 26 Oct, 6 Nov sales 1,680 logged.
- 👴 **Dad:** **`checkin-dad` FAILED 3rd day (WA bridge offline; logged, no fallback by policy)** · flu+COVID jab (NHS 26/27) STILL unbooked — window open, aim 6 Dec · 16 Jul foot outcome ~17 wks unrecorded · ONE GP call closes 4: foot result, AAA diameter+scan, PSA, jabs.
- 💼 **2Real (8 Nov):** **7 Nov (Sat) sales STILL not logged (EOD+1)** · Jiji Lead Nudger 8 Nov **7/7 sent** (8 harvested → queue 288; 585 total) · ⚠️ **WA Catalogue poster BLOCKED — 0 posted, 7 remain** (root cause: CSS transform skews getBoundingClientRect on Tools/Save; `wa_post_robust.py` uses elementFromPoint — apply to Save next run) · Jiji→Ledger: **12 items left Jiji (mark SOLD) · 1,369/1,377 unzoned (John)** · Jiji live 1,357 · 💰 **Hagija 4,000 6 DAYS OVERDUE · Joycelyn 2,500 8d** · 🧾 **VAT Form 10-M due 7 Nov — STILL UNCONFIRMED (chase Kath; GRA 20%)** · Kia: welder 800, trim 150, solosprayer 1,500 paid/1,000 due · ✅ **FB Page WORKS (H confirmed 08/11, professional dashboard); Marketplace OFF per directive; poster cron paused** · Meta WABA agent TEST MODE (2 drafts pending — add CTA; → pause f3228b7ede78 after clean wk) · WA Ads dark 21d · Olymech ~37d · strategy [[STRATEGY_CLEAROUT_KIA_SHOP_20261104]] awaiting H inputs.
- 🔒 **Security 8 Nov: 🟠 DEGRADED** (sole FAIL = **WhatsApp bridge DOWN, 3rd audit, attempt 251**). ✅ **IMPROVEMENTS: multiplex dup-credential (default+content-buddy) RESOLVED (0 occurrences); 2 legacy `.env`-reader scripts DELETED.** TG token valid, gateway PID 1340, 0 backup `.env`, no credential exposure, no breach markers. WARN debt: dual-root `~/.hermes/.env` dead placeholder · silent 25/56 · 2 Mom-reminder jobs wrong thread (≠424).
- 🖥️ **System:** Gateway ✓ PID 1340 (TG polling healthy; 06:11 stall self-healed 13s) · **WA adapter ✗ (port 3000 dead)**. 29 cron outputs, no provider outage · **Backup DUE 8 Nov 23:03** (last verified 1 Nov: 2.8 GB, 13,057 files) · evening reflect proposes **08:00 WA health-check cron** + **[[RECEIVABLES]] aging ledger** · integrated-daily-synthesis `d719cd80fa5b` healthy → topic 20.

## Superseded daily detail (7 Nov) — pruned 8 Nov
- 2026-11-07 consolidation entry pruned — full detail in `Vault/insights/INTEGRATED_INSIGHTS_2026-11-07.md` + `Vault/Daily/2026-11-07.md`. Carried into 8 Nov: WA bridge down, dup-credential (now RESOLVED), VAT 10-M, Hagija/Joycelyn, WA catalogue 93/93, Meta TEST MODE, FB shelved.

## Archived (before 2026-11-07)
- Daily consolidation entries 2026-08-18 → 2026-11-06 were **pruned from MEMORY.md** to keep the working store lean. Full per-day detail preserved in `Vault/insights/INTEGRATED_INSIGHTS_<date>.md` and `Vault/Daily/<date>.md`.
- **SOURCING POLICY (H 24 Oct 2026, standing):** non-stock customer requests INTERNAL-ONLY → hold → log `sourcing_log.json` → research → H approves → nothing leaves 2Real.
- **FB doctrine (standing):** 2Real FB Marketplace = H's personal, manually-published; agent holds system-side (Jiji/WhatsApp) only. Page posts = scheduled lane via Professional Dashboard (confirmed working 08/11). `allow_all_users: true` on gateway noted.
- **Meta agent trial (NEW 6 Nov):** agent in TEST MODE awaiting first customer; approval gate ~1 full trading week clean; rollback = re-enable Hermes f3228b7ede78 + reactivate whatsapp-customer-gate.

## System
- Canonical vault path: `C:\Users\User\.hermes\workspace\Vault\`.
- Python full path: `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe` (uv-managed cp311 on PATH).
- **Current live state (8 Nov 2026):** Gateway RUNNING PID 1340 (TG polling OK) · **WhatsApp bridge DOWN (6 Nov 10:17, day 3; QR re-pair needed)** · Security DEGRADED (sole FAIL = WA) · **WA poster BLOCKED (7 remain; save-button fix)** · **Jiji nudger 7/7 (8 Nov)** · **Hagija 4,000 6 DAYS OVERDUE** · **Joycelyn 2,500 8d** · VAT 10-M UNCONFIRMED · **7 Nov sales unlogged** · **Mum reports gap 6–8 Nov (channel)** · **H food gap 14d** · Dad jabs unbooked · **Backup TONIGHT 23:03** · no provider outage · cron model pinned deepseek-v4-flash.
- Integrated-daily-synthesis job (`d719cd80fa5b`, 22:05 daily) present and healthy; delivers to Telegram topic 20.
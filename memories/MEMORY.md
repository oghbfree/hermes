# MEMORY.md

Durable facts from periodic daily-processing runs.

_facts below are limited to verified findings. Last refreshed: 2026-11-13 02:44 (Nov 13 synthesis)._

## 2026-11-13 Consolidated (Fri, EOD)
- 👵 **Mum: 🔴 REPORT CHANNEL DOWN day 7 (FULL WEEK) — WhatsApp bridge offline since 6 Nov 10:17; 6–12 Nov reports missing** (creds.json present, session not holding → needs H foreground QR re-pair; connect-timeout attempt ~86). Last data (5 Nov): **BP 126/64 · P 67 · T 36.4 — clean 2–5 Nov**; no 24 Oct perceptual-episode recurrence. **Masseuse: 10 Nov UNCONFIRMED; next due TODAY 13 Nov.** Open: 25–29 Oct gap · Na labs (161) · Imodium OUT · AVS med + 150ml liquid med unidentified · Kenus outcome · BP batteries.
- 🦷 **H (52):** food gap **18d 🔴** (since 25 Oct) · Renerve Plus ZERO **45d** (~295 GH) · 31 Aug review **73d** undocumented · labs (1,075 GH) pending · dental unlogged (31d) · no vitals ~80d · ibuprofen daily (AM headache) = GI/kidney risk until labs · 🟢 44d acute-free.
- 👴 **Dad:** **`3-Day Condition & Wellbeing Check` DUE TODAY 13 Nov** (last run 10 Nov FAILED provider; `*/3` schedule) · Flu+COVID jab (NHS 26/27) STILL unbooked — aim 6 Dec · 16 Jul foot outcome ~17 wks unrecorded · ONE GP call closes 4: foot result, AAA, PSA, jabs.
- 💼 **2Real (13 Nov):** ✅ **11 Nov LOGGED: 2,195 GHS · 76% · profit 1,661** (3 buyers → broadcast list) · 🔴 **7 + 9 + 10 + 12 Nov unlogged** · ✅ **WA Catalogue 100/100 (0 pending; `wa_queue.json` needs REFILL)** · ✅ **Jiji nudger 8/8 (11 Nov, queue 285)** · ✅ **Jiji live 1,380; 15 new auto-seeded, 7 left likely SOLD** · 💰 **Hagija 4,000 10 DAYS OVERDUE (due 2 Nov, brother — DO FIRST) · Joycelyn 2,500 11+d** · 🧾 **VAT Form 10-M due 7 Nov — STILL UNCONFIRMED (chase Kath)** · ✅ **Recruitment pipeline 79** (+1 Nurse Josephine k.kporyi, NMC NO → below threshold) · Akoma WA status (P-12) PENDING-REVIEW → H approval (topic 26) · 🔵 **WA Ads dark 27d · Olymech 43d** · 🔀 Sunday content engine 402 credits · Meta WABA agent TEST MODE (no-invent FAIL 08/11 → HOLD) · Kia 1,500 paid/1,000 due · strategy [[STRATEGY_CLEAROUT_KIA_SHOP_20261104]] awaiting H inputs.
- 🔒 **Security 12 Nov: 🟠 DEGRADED** (sole FAIL = **WhatsApp bridge DOWN, 7th audit; connect-timeout**). ✅ TG token valid (getMe OK), gateway PID **16696** (LIVE TCP confirmed), **0 backup `.env`**, dup-credential RESOLVED, no breach markers. ⚠️ stale `~/.hermes/.env` 13-char placeholder (11+ cycles) · `GATEWAY_ALLOW_ALL_USERS: true` · silent 25/56 · 2 Mom-reminder jobs wrong thread (123286468 ≠ 424).
- 🖥️ **System:** Gateway Telegram ✓ (PID 16696, polling confirmed 02:43) · **WA adapter ✗ (port 3000 dead, reconnect retry 300s)** · **12 Nov cron healthy except checkin-mum (WA channel)** · **`Dad 3-Day Check` due 13 Nov** · ✅ **github-memory-backup `a7bebde` (46 files, 11 Nov)** · ✅ **Backup snapshot VERIFIED: `backup_20261108_231110` — 15,497 files, 7-DB set** · ⚠️ **daily-backup weekly Sun 23:03, next 15 Nov** (missed 2 runs).

## Superseded daily detail (11 Nov) — pruned 13 Nov
- 2026-11-11 consolidation pruned — full detail in `Vault/insights/INTEGRATED_INSIGHTS_2026-11-11.md` + `Vault/Daily/2026-11-11.md`. Carried forward: WA bridge down (now day 7), dup-credential RESOLVED, VAT 10-M, Hagija/Joycelyn, Meta TEST MODE, WA poster 100/100, Jiji live 1,380, 11 Nov sales logged 2,195, recruitment pipeline 79.

## Archived (before 2026-11-08)
- Daily consolidation entries 2026-08-18 → 2026-11-07 were **pruned from MEMORY.md** to keep the working store lean. Full per-day detail preserved in `Vault/insights/INTEGRATED_INSIGHTS_<date>.md` and `Vault/Daily/<date>.md`.
- **SOURCING POLICY (H 24 Oct 2026, standing):** non-stock customer requests INTERNAL-ONLY → hold → log `sourcing_log.json` → research → H approves → nothing leaves 2Real.
- **FB doctrine (standing):** 2Real FB Marketplace = H's personal, manually-published; agent holds system-side (Jiji/WhatsApp) only. Page posts = scheduled lane via Professional Dashboard (confirmed working 08/11). `allow_all_users: true` on gateway noted.
- **Meta agent trial (NEW 6 Nov):** agent in TEST MODE awaiting first customer; approval gate ~1 full trading week clean; rollback = re-enable Hermes f3228b7ede78 + reactivate whatsapp-customer-gate.

## System
- Canonical vault path: `C:\Users\User\.hermes\workspace\Vault\`.
- Python full path: `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe` (uv-managed cp311 on PATH).
- **Current live state (13 Nov 2026):** Gateway Telegram RUNNING PID 16696 (polling OK) · **WhatsApp bridge DOWN (6 Nov 10:17, day 7; connect-timeout — needs H foreground QR re-pair)** · Security DEGRADED (sole FAIL = WA) · **WA poster queue DRAINED (refill via feed_wa_queue.py)** · **Jiji nudger 8/8 (11 Nov)** · **Hagija 4,000 10 DAYS OVERDUE (DO FIRST)** · **Joycelyn 2,500 11+d** · VAT 10-M UNCONFIRMED · **7/9/10/12 Nov sales unlogged** · **Mum reports gap 6–12 Nov (channel, day 7)** · **Dad 3-Day Check due 13 Nov** · **H food gap 18d** · Dad jabs unbooked · **Backup verified OK (15,497 files), next Sun 15 Nov** · Sunday content engine 402 credits · cron model pinned deepseek-v4-flash.
- Integrated-daily-synthesis job (`d719cd80fa5b`, 22:05 daily) present and healthy; delivers to Telegram topic 20.
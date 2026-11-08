# MEMORY.md

Durable facts from periodic daily-processing runs.

_facts below are limited to verified findings. Last refreshed: 2026-11-07 22:10 (Nov 7 EOD synthesis)._

## 2026-11-07 Consolidated (Sat, EOD)
- 👵 **Mum: 🔴 REPORT CHANNEL DOWN — WhatsApp bridge exited 6 Nov 10:17; 6–7 Nov reports missing** (`checkin-mum` fail x2; no baileys/port 3000; needs foreground QR re-pair — CHANNEL fault, not confirmed care issue). Last data (5 Nov): **BP 126/64 · P 67 · T 36.4 — 5-day clean streak** (2–6 Nov); no 24 Oct episode recurrence as of 5 Nov. 🆕 **"AVS" med 2nd sighting (5 Nov 2pm) — identify (Dr Morris list: AVS, 150ml liquid med, Na 161, Furosemide dose, 16 Oct leg).** Open: 25–29 Oct gap · Na labs (161 🚩) · Imodium OUT · masseuse 6 Nov outcome · Kenus outcome · BP batteries.
- 🦷 **H (52):** food gap **13d 🔴** (since 25 Oct) · Renerve Plus ZERO **~40d** (Pharmabay ~295 GH) · 31 Aug review **68d** undocumented · labs (1,075 GH) pending · dental unlogged (26d) · no vitals ~75d · ibuprofen daily (AM headache) = GI/kidney risk until labs · ✅ 6 Nov sales logged (1,680) — engaged on ledger.
- 👴 **Dad:** 3-day check RAN 7 Nov · **flu+COVID jab (NHS 26/27) STILL unbooked — window open, aim 6 Dec** · 16 Jul foot outcome ~17 wks unrecorded · **ONE GP call closes 4 items**: foot result, AAA diameter+scan date, PSA policy, jabs (flu/COVID; 75+ RSV eligible; compression stockings = vascular decision only re PVD+ulcer).
- 💼 **2Real (7 Nov):** Sat market day — **7 Nov sales not logged at EOD** (2 Nov gap only, 5d) · **Jiji Lead Nudger 12/12 sent 7 Nov** (10 goods, 1 job) · WA catalogue COMPLETE **93/93** (poster no-op; 3 manual collection via phone app) · Jiji live 1,360–1,367 · ⚠️ **Jiji→Ledger: 8–9 items left Jiji (mark SOLD), 1,369/1,377 still unzoned (John)** · 💰 **Hagija 4,000 5 DAYS OVERDUE · Joycelyn 2,500 7 days** · 🧾 **VAT Form 10-M due 7 Nov — FILING UNCONFIRMED (confirm with Kath — GRA 20%)** · 🚗 Kia prep: welder 800, Kasoa trim 150, solosprayer 1,500 paid / 1,000 due · 🆕 **Meta WABA agent TEST MODE** (6 Nov handoff; ~1 clean trading week → pause Hermes f3228b7ede78 + dormant whatsapp-customer-gate; draft META_AGENT_TRIAL_LOG + 19:00 Topic-1 trial-watch) · Bosch jigsaw lead stale 19d · FB SHELVED permanent · WA Ads dark 21d · Olymech ~37d · strategy [[STRATEGY_CLEAROUT_KIA_SHOP_20261104]] awaiting H inputs (shop rent/m², Rio specs, Sammy MoMo ok) · Christmas local mode 40d to 17 Dec.
- 🔒 **Security 7 Nov: 🟠 DEGRADED** (0 CRIT, 1 new FAIL; msg 13117) — **WhatsApp bridge DOWN (exit 1 @6 Nov 10:17; reconnect attempt 18; regression vs 6 Nov paired-live)**. TG token valid (@Ogaitchhermesbot), gateway process up (PID 28472), 0 backup `.env`, no credential exposure, no breach markers. 🔺 **WARN 6th day ESCALATED: default + content-buddy dup TG credential** · dual-root `~/.hermes/.env` dead placeholder · silent 25/56 · 2 Mom-reminder jobs on wrong thread (≠424) · `hermes update` pending.
- 🖥️ **System:** Gateway ✓ PID 28472 (TG polling healthy; churn self-heals ~13s) · **WA adapter ✗ (port 3000 dead)**. 22 cron runs today, no provider outage · **Backup VERIFIED 1 Nov; next Sun 8 Nov 23:03** · evening reflect proposes **07:30 WA health-check cron** + **[[RECEIVABLES]] aging ledger** (create) · recruitment 76 (top nurse Charlotte Nortey 0545995731) · integrated-daily-synthesis `d719cd80fa5b` healthy → topic 20.

## Superseded daily detail (6 Nov) — pruned 7 Nov
- 2026-11-06 consolidation entry pruned — full detail in `Vault/insights/INTEGRATED_INSIGHTS_2026-11-06.md` + `Vault/Daily/2026-11-06.md`. Carried forward: Mum BP run + AVS flag, Hagija receivable, VAT 7 Nov, FB shelved, WA catalogue 93/93, Meta TEST MODE, gateway issues.

## Archived (before 2026-11-06)
- Daily consolidation entries 2026-08-18 → 2026-11-04 were **pruned from MEMORY.md** to keep the working store lean. Full per-day detail preserved in `Vault/insights/INTEGRATED_INSIGHTS_<date>.md` and `Vault/Daily/<date>.md`.
- **SOURCING POLICY (H 24 Oct 2026, standing):** non-stock customer requests INTERNAL-ONLY → hold → log `sourcing_log.json` → research → H approves → nothing leaves 2Real.
- **FB doctrine (standing):** 2Real FB listings = H's personal, manually-published; agent holds system-side (Jiji/WhatsApp) only. `allow_all_users: true` on gateway noted.
- **Meta agent trial (NEW 6 Nov):** agent in TEST MODE awaiting first customer; approval gate ~1 full trading week clean; rollback = re-enable Hermes f3228b7ede78 + reactivate whatsapp-customer-gate.

## System
- Canonical vault path: `C:\Users\User\.hermes\workspace\Vault\`.
- Python full path: `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe` (uv-managed cp311 on PATH).
- Obsidian skill confirmed vault at `C:\Users\User\.hermes\workspace\Vault\`.
- **Current live state (7 Nov 2026):** Gateway process RUNNING PID 28472 (TG polling OK) · **WhatsApp bridge DOWN (6 Nov 10:17, needs QR re-pair)** · **Security DEGRADED (7 Nov; dup-credential day 6)** · **WA catalogue COMPLETE 93/93** · **Jiji nudger 12/12 (7 Nov)** · **Hagija GH₵4,000 5 DAYS OVERDUE** · **Joycelyn 2,500 7d** · **VAT Form 10-M due 7 Nov — UNCONFIRMED** · **Mum reports gap 6–7 Nov (channel)** · **H food gap 13d** · Dad jabs unbooked · **Backup Sun 8 Nov** · no provider outage today · cron model pinned deepseek-v4-flash.
- Integrated-daily-synthesis job (`d719cd80fa5b`, 22:05 daily) present and healthy; delivers to Telegram topic 20.
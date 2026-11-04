# MEMORY.md

Durable facts from periodic daily-processing runs.

_facts below are limited to verified findings. Last refreshed: 2026-11-04 00:35 (Nov 3 EOD — late-run reschedule of the 22:05 synthesis)._

## 2026-11-03 Consolidated (Tue, EOD)
- ✅ **Mum: FULL 3 Nov coverage** — BP **133/64 · P 70 · T 36.4** @10:50 ✅ (trend 138/65 → 123/62 → 133/64, all in band; stop rule <100/>140 not triggered). Meals all (Obrayo; Kenkey + pepper + fried fish). 🆕 ⚠️ **Brief evening dizziness 5:42pm (after TV) — resolved; WATCH — repeat/with vision → Dr Morris SAME DAY** (first dizziness logged; Na 161 🚩 context). No 24 Oct perceptual recurrence. Open: 25–29 Oct gap · 150ml liquid med UNIDENTIFIED · Na labs overdue · Imodium OUT · Kenus ask · milk replacement · BP batteries · salt therapy. 💆 Tue masseuse — confirm if session happened 3 Nov.
- 🦷 **H (52):** food gap **9–10d 🔴** (since 25 Oct) · Renerve Plus ZERO **~37d** · 31 Aug review ~64d undocumented · labs (1,075 GH) pending · dental ~22d unlogged · **no vitals ~71d** · no replies to 3 Nov prompts.
- 👴 **Dad:** 1 Nov check ran — **flu+COVID jab: NHS aim 6 Dec, BOOK NOW** · 16 Jul foot outcome unrecorded (one GP call: foot, AAA scan, PSA).
- 💼 **2Real (3 Nov):** 🔴 **2–3 Nov sales NOT logged (2-day gap**; last 31 Oct 3,185 @91%) · 💰 **Hagija GH₵4,000 1 DAY OVERDUE (chase bro) · Joycelyn 2,500 unpaid** · ❌ **WA Catalogue Poster FAILED 09:05 → 0 posts; 31 remaining** · 🚨 **FB LOCKED day 3 (checkpoint 828281030927956 — H "Get Started" verify pending; automation paused)** · ✅ Jiji nudger 23 sent, queue **279** · ⚠️ Weekly Jiji Catalog Refresh stale 5d; nudger tagged 8 job ads as goods (JOB_KEYWORDS missing) · WA Ads dark 17d · Olymech 33d · **VAT Form 10-M due Fri 7 Nov** · act ICT qty TBD · Christmas gap 291 (UK LOCKED → local).
- 🔒 **Security 3 Nov: HEALTHY (0 CRIT / 0 FAIL) — 7th day.** Audit 07:00: TG token valid (@Ogaitchhermesbot), WA live, gateway PID 1800, 0 backup `.env`. 🆕 **WARN: default + content-buddy duplicate TG credential (content-buddy TG refused 2 restarts 2–3 Nov).** Debt: dual-root `.env` placeholder · 5 `.env` scripts · silent 25/56 · Mom-reminders thread 424 lost.
- 🖥️ **System:** Gateway ✓ (TG+WA). ⚠️ **09:05-cluster: 9 jobs errored** (scheduler `_final_response_from_result` — harness-level: WA poster, ops check, inquiry loop, tasks-queue, nurse check-in, health checks, Mom Morning reminders, job-applications) · Weekly Competitor topic-5 delivery_failed · **Backup VERIFIED 1 Nov (2.8GB/13,057/8 DBs); next Sun 8 Nov** · Morning Priority Check-in + Mom Evening + farm disabled (intentional) · cron-status-report + Daily Jiji Report stale.

## Superseded daily detail (30 Oct – 2 Nov) — pruned 3 Nov
- 2026-10-30 → 11-02 consolidation entries pruned on 3–4 Nov — full detail in `Vault/insights/INTEGRATED_INSIGHTS_2026-10-30.md` → `INTEGRATED_INSIGHTS_2026-11-02.md` and `Vault/Daily/<date>.md`. Durable items carried forward: FB re-locked (checkpoint same), WA catalogue 31 remaining, Jiji nudger queue 279, Hagija receivable overdue, UK Xmas order LOCKED → local, Mum vitals healthy 1–3 Nov run.

## Archived (before 2026-10-30)
- Daily consolidation entries 2026-08-18 → 2026-10-29 were **pruned from MEMORY.md** to keep the working store lean (real consolidation, not append-only). Full per-day detail preserved in `Vault/insights/INTEGRATED_INSIGHTS_<date>.md` and `Vault/Daily/<date>.md`.
- **2026-10-26 baseline** (superseded by 27–30 Oct entries): full detail in INTEGRATED_INSIGHTS_2026-10-26.
- **SOURCING POLICY (H 24 Oct 2026, standing):** non-stock customer requests INTERNAL-ONLY → hold → log `sourcing_log.json` → research → H approves → nothing leaves 2Real.

## System
- Canonical vault path: `C:\Users\User\.hermes\workspace\Vault\`.
- Python full path: `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe` (uv-managed cp311 on PATH).
- Obsidian skill confirmed vault at `C:\Users\User\.hermes\workspace\Vault\`.
- **Current live state (3 Nov 2026)**: Gateway RUNNING PID 1800, Telegram + WhatsApp connected, token valid, 0 backup .env. ✅ **Security HEALTHY 7th day** · weekly backup VERIFIED 1 Nov (2.8GB/13,057 files; next Sun 8 Nov) · 🚨 **FB LOCKED day 3 (checkpoint 828281030927956 — H verify "Get Started"; automation paused)** · **WA Poster failed 3 Nov → 31 remaining** · **Jiji nudger queue 279** · **Hagija GH₵4,000 overdue 1d** · Joycelyn 2,500 unpaid · **2–3 Nov sales NOT logged** · **Mum: BP healthy 3-day streak; ⚠️ new brief dizziness 3 Nov — watch** · **Dad: flu/COVID jab — NHS aim 6 Dec** · **VAT Form 10-M due 7 Nov** · 09:05 cron cluster (9 jobs, scheduler finalisation) · content-buddy dup TG credential WARN · cron model pinned deepseek-v4-flash.
- Integrated-daily-synthesis job (`d719cd80fa5b`, 22:05 daily) present and healthy; delivers to Telegram topic 20.

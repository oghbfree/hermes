# MEMORY.md

Durable facts from periodic daily-processing runs.

_facts below are limited to verified findings. Last refreshed: 2026-08-16._

## 2026-08-16 Daily Processing Run
- **Security audit Aug 15 18:06 SUCCESS — KEY POSITIVE REVERSAL**: Telegram token now **VALID** (@Ogaitchhermesbot), **topic 20 present + verified** (msg_id 10443), report saved `Vault/System/Assistant/SECURITY_AUDIT_2026-08-15-evening.md`. This SUPERSEDES earlier "token INVALID(404)" findings — token works again.
- ⚠️ **Gateway DOWN (regression)** — PID 5596 dead, log stale ~33h since 08-14 09:44, no clean shutdown. AGENTS.md forbids auto-restart → alert H via Telegram #urgent. Files down (cron delivery + WhatsApp).
- **Credential debt persists**: 25 backup `.env` copies, `bws_cache.json` plaintext secrets, ~33 `.py` env-readers. WhatsApp unpaired ~70 days. Blocked unauthorized user 5146706699.
- **Daily backup Aug 15 23:27 SUCCESS** — 17,531 files (workspace 15,120 + cron 1,347 + skills 843 + sessions 119), all critical DBs byte-verified (state.db 418MB, appdata_state.db 932MB + shm/wal), 0 failed. Dir `backup_20260815_230607`.
- **Cron SLA ~41%** (18/44 OK) — 18 systemic Connection/offline (10:16 provider unreachable batch), 9 drift_skip (unpinned jobs model drifted nemotron→deepseek-v4-flash).
- **Integrated-daily-synthesis STILL drift_skip blocked** (`ac813a924bbd` unpinned) — no INTEGRATED_INSIGHTS since Jul 18. Mom-evening-exercise (3ebd2dc4487c) same. Fix: pin jobs provider/model.
- Mum health morning+evening and H evening health checks ran; brain-dump-parser no new dumps; marketplace monitor connection-failed.
- No new session request dumps to archive (0 active; 118 already archived).

## 2026-08-14 Daily Processing Run
- Cron SLA ~50% (25/50 runs OK in last 24h) — improved from ~83% failure, but 25 runs still errored. Top causes: **drift_skip** (unpinned jobs skipped on provider/model drift — ac813a924bbd integrated synthesis, b0a7c6c0fa03 eric-checkin, d0651b16bab6), network unreachable.
- **Integrated-daily-synthesis job RESTORED but SKIPPED by drift_skip** — job `ac813a924bbd` now exists (runs 5 22 * *), but refuses to run because its global config drifted (model 'nvidia/nemotron-3-ultra-550b-a55b:free' → 'deepseek/deepseek-v4-flash-0731') and is unpinned. No INTEGRATED_INSIGHTS since Jul 18. **FIX: pin job provider/model explicitly.**
- **Security audit Aug 14 SUCCESS** (00:16 UTC) — Telegram HEALTHY: bot token VALID (@Ogaitchhermesbot), gateway alive PID 18460, topic 20 verified, msg_id 10406. Credential debt WORSENING: **25 backup .env copies (+3)** (14 backups + 10 hermes-backup + 1 openclaw), bws_cache.json plaintext secrets, 34 live workspace .py env-readers. WhatsApp still unpaired (no creds.json). 29/54 cron silent delivery. Report: `Vault/System/Assistant/SECURITY_AUDIT_2026-08-14.md`.
- **Daily backup Aug 13 SUCCESS** (23:09 UTC) — 17,461 files, 0 errors, 1,327 active AppData cron files backed up.
- **2Real Customer Inquiry Loop** — 29 entries: 10 auto-resolved, **7 stock-found-but-hook-missed (URGENT, customers waiting)**, 12 unknown, 19 SLA breaches (worst 574h/~24 days: Under Cabinet Light Kit, Flopro Hose Spray Gun, Samsung Galaxy). Manual replies needed today.
- **2Real Daily Ops Check FAILED** — skill `2real-enterprises-agent` not found (was skipped). Fix skill reference.
- **H health masters rebuilt** (Aug 13 20:44) — `H_FOOD_MASTER.md` + `H_MEDICAL_MASTER.md` re-consolidated.
- **Mum vault guidance**: no new vault health reports since Aug 4 (11-day gap) — mum check-ins post to Telegram topic 4 but vault file save is a separate unwired step (known issue since 11 Aug).
- **WhatsApp session** "Offer WhatsApp support" (167 msgs): H tested Meta AI support-bot flow (ticket #1535679531211373) — testing automation not substantive.
- No new session request dumps to archive (0 active; 118 already in `.archive/`).

## Container 26 — Final Settlement (11 Aug 2026)
- Split: Nicholas 3/8, H 5/8; demurrage & Golden Jubilee 50/50.
- **Nicholas → H: £900 (UK) + 5,897.58 GH₵ (Ghana net).**
- Breakdown saved: `Vault/business/procurement/container 26/settlement-11-08-26.md`.
- Naa's port bills (Nicholas 83,540 / H 93,165 ≈ 50/50) do NOT match internal 3:5+50/50 ratio — needs reconciliation.

## 2026-08-13 Daily Processing Run
- Daily backup (Aug 12 23:03): SUCCESS — 30,671 files, 3.9 GB, DBs byte-verified. **Active runtime migrated to AppData/Local/hermes/** (state.db now 863MB; ~/.hermes/cron empty; 1,313 cron files backed up from AppData).
- Security audit (Aug 13): FAIL but Telegram channel HEALTHY — token VALID (getMe ok, @Ogaitchhermesbot), gateway alive PID 13760. Persistent credential debt: 22 backup .env copies (+2), bws_cache.json 15 plaintext secrets, 46 .env-reading scripts. WhatsApp unpaired (attempt 509). 29/49 cron silent, 32 jobs error.
- 2Real inventory sync: up to date, no changes.
- Archived 101 stale request_dump_*.json (>7d) → sessions/.archive/.
- Farm data consolidated to Vault/business/farm/ (session 20260812_143140); old 2real/Farming/farm deprecated; 10 farm crons PAUSED since 8 Jul.
- Kroboano real estate: Nenyi Oliver Mensah deal, title dispute (uncle Prof Assibu), Abu mason 1,200 GHS/plot — in real-estate-portfolio.md.
- Hermes memory ~99% full — candidate trims: real estate (~300), farm (~250), apiary (~180).

## System
- MEMORY.md baseline recreated from verified workspace state.
- workspace/AGENTS.md flagged with BOM (U+FEFF invisible unicode) — do not trust guidance until manually reviewed and BOM stripped.
- Config-dir mismatch expected on Windows: `~/.hermes/config` points to Hermes config dir, not workspace.
- Canonical vault path: `C:\Users\User\.hermes\workspace\Vault\`.
- Python full path: `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe` (uv-managed cp311 on PATH).
- Obsidian skill confirmed vault at `C:\Users\User\.hermes\workspace\Vault\`.
- **Gateway DEAD AGAIN as of 2026-07-12** — Security audit confirms PID 26404 dead, crash loop 21+ days. Previous Jul 7 recovery (PID 17112) lost. `concurrent_log_handler` ModuleNotFoundError unresolved for Python 3.14 (gateway needs Python 3.11 venv).
- **49 backup .env copies** (CRITICAL — worsened from 28): 27 in backups/, 4 in state-snapshots/, 17 in ~/hermes-backup/, 1 in ~/.openclaw/.
- **Config drift: v29→v33 active** — 4 versions behind latest doctor schema.
- **WhatsApp unpaired 69+ days** — creds.json missing, manual QR re-pair required.
- **27/40 cron jobs silent delivery** — 13 deliver to Telegram topics, 27 deliver to `origin` or `local`.
- **Nightly-consolidation job stale** — `3534ca8a8925` last ran Jun 17, not running nightly despite being enabled.
- Telegram topic 20 (Memory Review) exists and accepts messages (verified msg_id=8750 from security audit Jul 12).
- 2Real inventory sync runs 12+/day — all successful, already up to date.
- **Jul 11-16: 83% cron failure rate** (~49/59 runs failed) — systemic Connection error + rate limits across 17+ unique job IDs. DNS/network instability persisting since Jul 1.
- **Jiji computer-use jobs flooding logs** — 38eaa5d0ada1 (every 10min) + f9f90bd47965 (every 5min) produce ~140+ failed runs/day with no value. Both still enabled in jobs.json.
- **Security audit Jul 12 GENERATED (00:09 UTC)** — CRITICAL FAIL: 7 CRITICAL, 3 FAIL, 4 WARN. Key findings: Telegram token INVALID (HTTP 404), gateway PID dead, DNS failure host-level, InvalidToken confirmed in logs (15+ occurrences), 49 backup .env copies, WhatsApp 65+ days unpaired. Delivered to topic 20 (msg_id=8750).
- **Security audit Jul 13 FAILED** — 1b7107630fe3 (00:50 UTC) crashed with "Response remained truncated after 4 continuation attempts". No report saved to Vault. Still CRITICAL FAIL status from Jul 12.
- **Security audit Jul 14 GENERATED (00:04 UTC)** — CRITICAL FAIL: 7 CRITICAL findings (Telegram token INVALID 404, 49 backup .env copies, WhatsApp unpaired 65+ days, gateway PID dead, DNS failure host-level, 23 workspace scripts read .env directly, AGENTS.md BOM). Delivered to topic 20 (msg_id=8750).
- **Security audit Jul 15 FAILED** — Rate limited (`free-models-per-day-high-balance`). No report generated. Jul 14 CRITICAL FAIL status remains current.
- **Security audit Jul 16 FAILED** — Rate limited (`free-models-per-day-high-balance`). No report generated. Jul 14 CRITICAL FAIL status remains current.
- **No new Mum meal data Jul 7-8** — carer did not report meals/vitals for Comfort on Jul 7. Jul 9-14: full coverage with vitals (BP 134/65 Jul 9 AM).
- **H health: Electrical shock (12 Jun) follow-up 33 days OVERDUE** — medical evaluation STILL PENDING (was 32 days overdue Jul 15). No vitals 44 days (since Jun 1). 3-day meal gap Jul 8-10. No health entries Jul 8-10, 13-15.
- **Integrated-daily-synthesis job STILL MISSING** from jobs.json — not running since Jun 20. No INTEGRATED_INSIGHTS since Jun 23.
- **Telegram token INVALID (404)** — confirmed by security audit. Token revoked by Telegram. Must rotate via @BotFather.
- **Jul 11 Security audit RUN and DELIVERED** — 1b7107630fe3 (00:09) completed, report saved to Vault, summary posted to Telegram topic 20 (msg_id=8750). Overall CRITICAL FAIL: 7 CRITICAL, 3 FAIL, 4 WARN.
- **Jul 11 Daily backup SUCCESS** — 586aebcd5e57 completed, 27,553 workspace files exact match, all 5 DBs byte-for-byte verified.
- **Jul 13 Daily backup SUCCESS** — 586aebcd5e57 (00:30) completed, 27,567 workspace files exact match, all 5 DBs byte-for-byte verified (state.db 411.9MB, kanban.db 1.7MB, memory_store.db 323KB).
- **Jul 13 Mum health logs CONTINUE** — morning/midday/evening reports logged Jul 12, 13 with vitals (BP 132/74 Jul 13 AM).
- **Jul 14 Mum health logs CONTINUE** — full day coverage via Telegram: morning BP 122/68, evening BP 129/63.
- **Jul 15 Mum health logs CONTINUE** — morning/midday/evening reports with vitals.
- **Jul 11 H health log GAP WIDENING** — no entries Jul 8, 9, 10 (3 days). No vitals since Jun 1 (40 days). Electrical shock follow-up 29 days overdue.
- **Jul 12 H health auto-generated** — morning check created, electrical shock follow-up now 30 days overdue. No manual entries for meals/vitals.
- **Ebony goodnight Jul 13 FAILED** — WhatsApp bridge offline (creds.json missing, 56+ days). Failure logged and Telegram notification sent to topic 2.
- **Ebony goodnight Jul 14 FAILED** — WhatsApp still unpaired.
- **Ebony goodnight Jul 15 FAILED** — WhatsApp still unpaired.
- **23 workspace scripts read .env directly** — Leak tokens to process table, shell history, logs. Created during delivery attempts.
- **AGENTS.md UTF-8 BOM persists** — Prompt injection risk, blocks cron execution.

## Missing/Blank Master Files
- No INTEGRATED_INSIGHTS since 2026-06-23 (synthesis job missing).
- No `workspace/memories/insights/` dir — insights under `Vault/insights/` or missing.
- H health log: no recent entries observed.
- Integrated-daily-synthesis job missing from jobs.json — not running since Jun 20.

## Mum Health (Comfort Blankson) — Jul 4-6 Summary

### Jul 4 (full reports with vitals)
- **Morning**: Slept okay but not too well. Breakfast: corn dough porridge + 2 boiled eggs. Vitals: BP 127/69, P 82, T 36.7. Exercises done, compression socks, Furosemide 20mg given.
- **Midday**: Mixed fruit snack. Lunch: Kenkey with pepper and fried fish, shrimps. Surfaces cleaned.
- **Evening**: Dinner: boiled cocoyam with vegetable stew. Pedicure + foot massage (Epsom salt, moisturizing cream). Vitals: BP 133/69, P 71, T 36.6. Warm milk before bed. Mood: Fair. Appetite: Fair. Swelling: Same.

### Jul 5
- Breakfast: Granola with warm milk
- Lunch: Fish pie / fish & stew
- Dinner: Grasscutter/snail light soup (appetite: good)

### Jul 6
- Breakfast: 3 fried eggs with onion and tomato
- Lunch: Kenkey and fish
- Dinner: (not yet logged)

## Farm Update
- **farm-goat-search cron STOPPED and REMOVED** (Jul 5) — goats not found, H will replace in due course.
- Mr Habib site visit at 10:00 Jul 5 — workers inspecting the job.
- Grasscutter (akrantie) inquiry — H asked Mr Habib if he can source.
- Waterlogged fields, Kalidou removed — still unresolved (no acting farm lead).

## 2Real Status
- Inventory auto-sync: stable, all runs successful, already up to date. Last sync: `inventory zobaze 7626.xlsx` (modified Jun 7).
- No new inventory changes detected.

## Content Pipeline (Jul 5-6)
- Sunday Content Engine: initially failed (provider timeout). User asked to rerun. Subagent timed out after 600s.
- Generated 164 assets for week-2026-07-06 across all 7 days/7 platforms.
- **Issue identified**: AI-generated fake logos/text baked into images. Regeneration in progress with clean prompts (no text/logo descriptions) + real transparent PNG overlays.

## Junior ISA & SIPP Recommendations (Jul 10)
- **Children**: Kobena (11), Nenyi (10) — UK citizens, father UK resident (London), mother/children in Ghana
- **Primary Vehicle**: Junior Stocks & Shares ISA — £9,000 annual allowance per child (2024/25)
- **Secondary Vehicle**: Junior SIPP — £2,880/yr net (£3,600 gross with 20% tax relief), access at 57+
- **Recommended Provider**: AJ Bell Youinvest — 0.25% platform fee (capped £3.50/month), free monthly auto-invest from £25, 2,500+ funds/ETFs/ITs
- **Core Holding**: Vanguard FTSE Global All Cap Acc (0.23% OCF) — single fund, global developed + emerging markets
- **Monthly Budget (suggested)**: £250 JISA + £100 SIPP per child = £700/month total
- **Estimated at 18 (7% nominal)**: ~£106k per child (JISA only)
- **Foresters JISA (father's current idea)**: 0.60% platform + fund charges = ~0.9-2.1% total — expensive vs AJ Bell (0.5%), Vanguard (0.38%)
- **Critical**: Child must be UK resident to open JISA. Father UK resident + children UK citizens may qualify — **call AJ Bell compliance (0333 200 1000) to confirm** before applying.

## Akoma Robotics School Acquisition Pipeline (Jul 10)
- **Target**: 2-3 school partnerships in Month 1, then scale via referrals
- **Strategy**: Direct outreach 80% + Social media credibility 20%
- **Audience**: School admins (principals, academic directors, STEM coordinators, PTA chairs) in Greater Accra
- **Offering**: Turnkey after-school mBot robotics — 10 weeks, 1,000 GHS/student, zero upfront cost to schools
- **5-Phase Plan**: Research 50 schools (Week 1) → Materials (Week 1-2) → Multi-channel outreach (Week 2-4) → Free demo sessions (Weeks 3-6) → Follow-up & conversion
- **Social Priority**: LinkedIn (admin outreach) > Facebook (credibility + parent demand) > Instagram (visual portfolio) > TikTok (skip for now)
- **Facebook Ads**: 8 administrator concerns mapped to ad angles, 2-ad test ($10/day each, 2 days), 10 scaling variations
- **Budget Phasing**: $40 test → $300 validate → $630-1,050 scale
- **Workspace**: `C:\Users\User\AppData\Local\hermes\kanban\workspaces\t_b21f32ef\`

## Phone Consolidation Plan (Jul 10)
- **5-Phase Plan**: Audit current phones & Smarty contract → Choose replacement (eBay UK, Back Market, CeX, musicMagpie, FB Marketplace London) → Purchase & setup → Cancel Smarty (PAC: text `PAC` to `65075` / STAC: text `STAC` to `75075`) → Dispose old phones
- **Quick Reference Card**: Smarty codes, verification checklist, disposal options, clickable search links, key dates
- **Workspace**: `C:\Users\User\AppData\Local\hermes\kanban\workspaces\t_ca76518e\`

## Facebook Marketplace Daily Habits (Jul 10)
- 10-15 min daily: inbox, relist stale (7+ days), validate stock, price check 3 nearby, retouch 1-2 weak photos, confirm pickups
- Weekly sprint: Sun relist top 10, Wed photo refresh 5, Fri weekend availability, Sat competitor pricing audit
- **Workspace**: `C:\Users\User\AppData\Local\hermes\kanban\workspaces\t_91f700ef\`

## Dr Ferguson Order for Mum (BLOCKED — Jul 10)
- **Known Supplements**: Multivitamin 2 tsp/day, Herbal supplement "in small plastic bag" 2 tsp in ½ cup boiled water (3-day cycles), Daily coconut oil + black seed oil + raw honey
- **Dr Ferguson Contact**: The Natural Health Clinic, Tel: 07949264356
- **Critical Clinical Constraints**: CKD Stage 3b (eGFR 41) — kidney-safe only, Elevated ferritin 404 µg/L — **NO IRON**, Elevated phosphate 2.91 mmol/L — **NO phosphate-rich**, Current meds: Furosemide + Metformin
- **Missing from User**: Exact herb names, multivitamin brand, quantities for trip, supplier preference (clinic/UK/Ghana), Ghana delivery address, payment method, trip departure deadline
- **Task**: t_2098e55f blocked pending details

## Confirmed Operational Flags
- 2Real agent system fully operational — stable cron loops, all syncs successful.
- WhatsApp gateway UNPAIRED 68 days — creds.json missing. Manual QR re-pair required.
- **Gateway RECOVERED** (after 19 days dead) — PID 17112 confirmed running Jul 7 00:04, Telegram polling mode healthy.
- Config drift: v29→v33 active (4 versions behind, previously narrowed from 9 but drifted again).
- Telegram topic 20 (Memory Review) accepts messages (verified).
- Sunday Content Engine needs fix for fake-logo-in-image issue.
- Mum health logs have full meals logged Jul 4-6 with good coverage.
- Farm: goat-search cron removed, Mr Habib engaged for site visit + grasscutter sourcing.

## Issues Requiring Action
1. **CRITICAL**: 87% cron failure rate (118/135 runs) — systemic Connection error across 17 job IDs
2. **CRITICAL**: Security audit missing Jul 8 — both runs failed (Connection error)
3. **CRITICAL**: WhatsApp unpaired 68 days — Ebony goodnight undelivered, Mum health check-ins fail
4. **HIGH**: Jiji jobs flooding failure logs (140+ failed runs/day) — no value produced
5. **HIGH**: Integrated-daily-synthesis job still absent — no insights since Jun 23
6. **MEDIUM**: Config drift v29→v33 widened since last report
7. **MEDIUM**: No new Mum meal data Jul 7-8 — carer may not have reported
8. **MEDIUM**: Daily notes gap — no Vault/Daily entries for 2026-07-09 or 2026-07-10
9. **LOW**: Dr Ferguson order blocked — missing 7 critical details from user
10. **CRITICAL**: Security audit Jul 11 CONFIRMED FAIL — 7 CRITICAL findings (Telegram token INVALID 404, gateway PID dead, DNS failure host-level, 49 backup .env copies, 18 workspace .env readers, WhatsApp unpaired 65+ days, InvalidToken in logs)
11. **HIGH**: H health log — no vitals 40 days, electrical shock follow-up 29 days overdue, 3-day logging gap Jul 8-10
12. **MEDIUM**: Integrated-daily-synthesis job STILL MISSING from jobs.json — must restore/recreate (ID varies per install, find via cron output dir)
---
title: INTEGRATED INSIGHTS 2026-11-23
date: 2026-11-23
tags:
  - daily
  - synthesis
aliases:
  - INTEGRATED_INSIGHTS_2026-11-23
---

# INTEGRATED DAILY SYNTHESIS — 2026-11-23 (Mon, EOD window → compiled 22:05)

**Generated:** 2026-11-23 22:05 · **Job:** integrated-daily-synthesis (d719cd80fa5b)
**Data window:** past 24h (MUM_MEDICAL_MASTER, H_MEDICAL_MASTER, daily-sales-log, CFO_DASHBOARD, DEADLINES_AND_FOLLOWUPS, SECURITY_AUDIT_2026-11-23, fb-page, FB poster + checkin-mum cron outputs, sessions)
**Note:** 👵 **Mum: caregiver chain silent ~143h (~6 days) — 6th consecutive flag, CRITICAL, NOW A WELFARE CONCERN (spans a full weekend + Mon).** 🔍 **FB poster blocker ROOT CAUSE CORRECTED: not a hung Chrome — the automation session sits on the 2 Real business PAGE id (61594761789134), not H's Oman Ghan personal profile → Marketplace redirects "ineligible" → 0 posted (safe, NO forced switch).** 📊 **Today Mon = H's DAY OFF (no sales expected — correct, not a gap).** 🟡 **Security 23 Nov STABLE; Telgram ConnectTimeout flapping NEW.** ✅ **Weekly backup RAN this morning (23 Nov 03:56, 16,270 files, 0 errors) — weekend gap FIXED.**

## Related
- [[INTEGRATED_INSIGHTS_2026-11-22]] · [[2026-11-22]] · [[daily-sales-log]] · [[DEADLINES_AND_FOLLOWUPS]]
- [[MUM_MEDICAL_MASTER]] · [[H_MEDICAL_MASTER]] · [[SECURITY_AUDIT_2026-11-23]] · [[H_FOOD_MASTER]]
- [[CFO_DASHBOARD]] · [[DECISION_LOG]]

---

## 1. Health

### Mum (Comfort, 91→92, Weija) — 🔴 CHAIN SILENT ~143h / ~6 days, 6th FLAG (CRITICAL — WELFARE CONCERN)
- 🔴 **No caregiver report since 17 Nov 20:58.** 18, 19, 20, 21, 22, 23 Nov all missing → **~143h / ~6 days** by 22:05 Mon. STEPHANIE_SILENT_INTAKE **0 unprocessed of 56**. **Escalation upgraded: a Sunday→Monday gap this long is no longer a "reporting glitch" — it is a WELFARE CONCERN for a 92-yo post-fall/post-HTN patient.** Evening check-in posted to topic 4 (23 Nov 20:05).
- ⚠️ **No BP since 16 Nov evening (124/70 · P68 · T36.0, ~7 days)** · meals last logged 17 Nov (>5 days) · kidney-capsule unknown since 17 Nov · back-pain outcome since 17 Nov UNMONITORED (last severe 10 Nov).
- ✅ BP streak clean across captured readings (9→13→14→16 Nov); **Furosemide stop-rule (<100/>140, RIGHT arm) never fired**; no 24 Oct perceptual-ep recurrence.
- 🔍 **Root cause: WhatsApp adapter OFF since 18 Nov** (sends refused localhost:3000 — `checkin-mum` confirmed day ~6 outage). **H MUST call Stephanie (0548236698) NOW for a verbal report + home-welfare check on Mum AND the carer; re-enable/QR re-pair the WA bridge (no live adapter at all; `hermes send` cached-directory only).**
- Open: Imodium OUT (10+ wks) · Na labs overdue · Kenus-spa recurrence ask · masseuse Fri 20 Nov UNKNOWN (17 Nov no-show) · milk replacement · tiger-nut milk status.

### H (Herbert, 52, Accra) — 🔴 food diary gap extends (RED, stagnant)
- 🔴 **14–23 Nov silent = 10-DAY food diary GAP** (last log 13 Nov). Evening prompt kept moved to restart.
- 🔴 **Renerve Plus ZERO — tremor unmedicated ~56 days** · 31 Aug post-shock review undocumented ~84 days · labs (1,075 GH) still pending (requisition never reached Nita) · dental (12 Oct) unlogged ~42 days · **no fresh vitals since 24 Aug (~91 days)** — longest on record. Ibuprofen 400 mg/day = GI/kidney risk until labs run.
- 🟢 No new acute onset since 29 Sep (~55 days clear); no chest pain; pericarditis quiescent.

### Dad (Robert, 92, UK) — 🟠 jab window ~2 wks left
- 🔴 **Winter flu+COVID jabs STILL unbooked** (window closes ~6 Dec) · no snapshot since 25 Oct. **ONE GP call** closes foot + AAA + PSA + jabs.
- ⚠️ Check-in attempt FAILED today (12:31): `Cannot connect to host localhost:3000` — WhatsApp adapter down. No path until bridge re-paired.

---

## 2. Business (2Real)

### Sales / week — Mon = DAY OFF (no row expected; correct). Week 16–22 Nov stands: GHS 5,490 / 57.5%
- 🟢 **Today Mon 23 Nov = H's DAY OFF** (standing rule 16 Nov) — NO sales expected, absence is correct, do NOT chase.
- 🔴 **`daily-sales-log.md` last row = 19 Nov (4,980/58%/profit 2,880).** **20 Nov (Fri) + 21 Nov (Sat) rows STILL MISSING — both working days, overdue.** 17 Nov (Tue) also unlogged. **Ledger debt: 7 + 10 + 17 + 20 + 21 Nov.**
- 🧾 COGS gaps accumulating (ironing board 19 Nov, Hagija toys, white paint, 08/11 grinder price 700 vs 70).
- 💡 **Proposed fix (unrun): daily COGS-reconciliation cron (Tue–Sat ~09:00, `0 9 * * 2-6`)** reading daily-sales-log + posting one prompt to confirm each missing cost.

### Channels & ops (flooder storm day 9 — FB poster now 0-post due to PROFILE-IDENTITY blocker)
- 🔍 **FB Marketplace Batch Poster (`5128ceaa2c09`) — root cause CORRECTED:** the automation browser's active identity is the **2 Real business PAGE (id 61594761789134), NOT H's Oman Ghan Herbert-blankson personal profile** → `/marketplace/create/item` redirects to "Pages can't use Marketplace"/`ineligible` → runner fails `no file input` → **0 posted today (counter 0/3)**. Both 12:34 + 15:30 runs honoured the no-auto-switch/anti-ban doctrine (post-01/11 review-watch) — **reported to H, no risk taken.** **Fix: H switches avatar to "Oman Ghan" personal profile once (or authorises agent switch).** Still emitting ~50 outputs/day off-schedule (day 9, pure noise).
- 🚨 **checkin-mum (`c3db50f4f9af`) = 100% FAILED-WA spam** (~1/min, bridge down, no localhost:3000 listener) — **pure noise, kill.** checkin-dad failed identically 12:31.
- ✅ **Jiji Lead Nudger (`0c0f87b59450`) ran healthy 13:28** (20/run batch).
- ✅ **2Real Open-Loops Tracker ran 20:02** (loading 2real-enterprises-operations skill; sourcing-loop + inquiry loop healthy).
- ⚠️ **FB Business Page content library disabled** (DNS 18/11; PUBLISHED unmeasurable); **content STALE ~28d** (newest week-2026-10-26); P-7 PENDING H REVIEW.

### Receivables / admin
- 💰 **Hagija GH₵4,000 OVERDUE since 2 Nov (21d)** · **market rent + Fluid CC were due 22 Nov (yesterday)** · Joycelyn 2,500 · VAT 10-M UNCONFIRMED · **WA Ads dark ~38d** · Olymech RFQ 6000997164 (~53d) · act ICT inverters qty · white-paint COGS · Tweneboah receipt + Dunlop/Sony ad closures · 08/11 grinder price · ironing-board COGS · Hagija toys COGS · faulty-grinder repair-bench DECISION open.
- 📢 B2B broadcast list primed (#7+): Eric, Dr Lomotey, tool lover 0245849519, Edwin (0550253348), Theophilus (0500599813), Emmanuel (tennis), Gbawe Rasta 0248150115.

### TAIWAH Christmas reel — STILL ON HOLD (17 Nov ruling)
- Exit-narrative ban stands (rented shop, no clearing framing); face LOCKED to MASTER_LOCK.png. Brief waits for H context.

---

## 3. Security Posture — 🟡 STABLE (audit 23 Nov 07:03)
- ✅ **TG token VALID** (live getMe @Ogaitchhermesbot) · gateway PID 25084 alive, many ESTABLISHED conns · **0 backup .env copies** · ACLs locked · `google_token.json` clean · no InvalidToken / provider 4xx · topic 20 live (5 jobs deliver).
- ⚠️ **NEW: Telegram ConnectTimeout flapping** (06:50–06:59, IPv4 paths 149.154.166.110/167.220) — network-layer, auto-recovers via sticky-path re-walk; monitor.
- ⚠️ **WHATSAPP ADAPTER with NO LIVE ADAPTER AT ALL** — `hermes send` returns cached contacts only; confusion across two `gateway_state.json` copies (`connected` Nov 17 AppData vs `fatal/whatsapp_not_paired` Oct 13 `~/.hermes`). **Confirmed root cause of Mum+Dad+family check-in failure (~6-day unmonitored health window). Needs QR re-pair / re-enable.**
- ⚠️ **Nous Portal revoked (unremediated)** — `hermes auth add nous`.
- ⚠️ Persistent WARNs: 24/55 silent cron targets · dead-thread `123286468` (2 Mom exercise jobs → 424) · multiplex dup-credential · stale `~/.hermes/.env` placeholder · 4 runtime `.env`-reader scripts · `allow_all_users: true` · cron receipt backlog.

---

## 4. System Health
- 🚨 **Flooder storm day 9 — FB poster (5128ceaa2c09) 0-post, now PROFILE-BLOCKED (not hung Chrome) + checkin-mum (c3db50f4f9af) WA-spam, both ~1/min off-schedule ~50 outputs each.** **Kill checkin-mum; FB resolved via one-time profile switch.**
- ✅ **Backup VERIFIED — ran Mon 23 Nov 03:56** (weekly job 586aebcd5e57): `~/.hermes/backups/backup_20261123_032329`, **16,270 files / 3,503 dirs, 0 errors**; `latest` junction correct (old 3.3GB dir copy cleaned). **Weekend gap resolved.**
- ✅ Scheduled jobs healthy 23 Nov: security audit 07:03 PASS+posted · Jiji lead nudger 13:28 · open-loops 20:02 · mum-health afternoon 13:30 + evening 20:05 (topic 4 prompts, all bounced — chain still silent) · FB poster 12:34+15:30 (blocked, reported) · checkin-mum/dad (WA-fail, logged).
- ✅ Active session dumps: 0 (118 in .archive) — nothing to archive.
- ✅ integrated-daily-synthesis job healthy (`d719cd80fa5b`, 22:05 → topic 20).
- 🗂 Sessions last 24h: all cron (health checks, FB poster, nudger, open-loops, checkin-mum/dad WA-fails); **no interactive H conversation today (Mon day off).**

---

## 5. Priority Actions (CRITICAL → HIGH → MEDIUM)

**CRITICAL:**
1. 👵 **Mum: H to call Stephanie (0548236698) TODAY — chain silent ~6 days (6th flag), now a WELFARE CONCERN** — 92-yo post-fall/post-HTN patient running fully unmonitored through a full weekend + Monday; confirm the carer is well too; confirm Fri masseuse + plumber. **Re-enable/QR re-pair WhatsApp adapter** so reports flow.
2. 🔒 **WhatsApp bridge: no live adapter (cached contacts only) — QR re-pair `hermes gateway run`** — blocks all family check-ins (Mum + Dad). This is THE fix for the silent chain.
3. 🔍 **FB poster: H switches automation-browser avatar to "Oman Ghan" personal profile once** (current session stuck on 2 Real Page → Marketplace ineligible). **Kill checkin-mum spam loop.**
4. 💰 **Log 20 + 21 Nov sales rows (overdue)** + 17 Nov · **Hagija 4,000 (21d OVERDUE)** · market rent + Fluid CC (due 22 Nov, chase if unpaid).

**HIGH:**
5. 🍽️ **H: log a meal (10-day RED) · reorder Renerve (~56d zero) · ONE clinic call (labs + dental + 31 Aug closure) · fresh BP (91 days!).**
6. 👴 **Dad: ONE GP call** — foot + AAA + PSA + winter jabs (window ~6 Dec).
7. 📊 Close 9 Jiji-sold items · John: assign 1,413 zones · content engine rerun (28d stale, P-7 sign-off) · Nous Portal re-auth · **CFO-driven: COGS-reconciliation cron (Tue–Sat 09:00) to close missing-cost gap.**

**MEDIUM:**
8. ⚙️ Faulty-grinder repair-bench DECISION · WA Ads renew-or-kill (~38d) · Olymech RFQ · Jiji ad closures (Dunlop + Sony) · Tweneboah receipt · 2 Mom jobs → thread 424 · 08/11 grinder price · ironing-board COGS · act ICT qty · FB group auto-share fix · FB Business Page capture fix.

---

## 6. Weekly Overview (16–22 Nov, unchanged — 23 Nov is next week's Mon day-off)
| Day | Sales GHS | Note |
|-----|-----------|------|
| 16 Nov (Sun) | — | ✅ day off |
| 17 Nov (Tue) | — | ⚠️ UNLOGGED (working day) |
| 18 Nov (Wed) | 510 (55%) ✅ | T-Rex tape + Bosch grinder as-is + spray |
| 19 Nov (Thu) | **4,980 (58%) ✅** | Sepha bistro ×3 + Tanko laptops + Xbox |
| 20 Nov (Fri) | 🔴 MISSING | row overdue — get figures from H |
| 21 Nov (Sat) | 🔴 MISSING | row overdue — working day |
| 22 Nov (Sun) | — | ✅ day off |

- **CFO 16–22 Nov: GHS 5,490 / 57.5% / 3,159 over 2 of 5 working days (-56% vs 12,500 target).**
- **Today Mon 23 Nov = DAY OFF (correct). Next working day Tue 24 Nov.**
- Receivables: Hagija 4,000 + Joycelyn 2,500. New contacts: Tanko (scrap), Sepha (event furniture).
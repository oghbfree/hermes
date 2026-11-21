---
title: INTEGRATED INSIGHTS 2026-11-20
date: 2026-11-20
tags:
  - daily
  - synthesis
aliases:
  - INTEGRATED_INSIGHTS_2026-11-20
---

# INTEGRATED DAILY SYNTHESIS — 2026-11-20 (Fri, EOD window → compiled Sat 02:14)

**Generated:** 2026-11-21 02:14 · **Job:** integrated-daily-synthesis (d719cd80fa5b)
**Data window:** past 24h (MUM_MEDICAL_MASTER, H_MEDICAL_MASTER, daily-sales-log, DEADLINES_AND_FOLLOWUPS, SECURITY_AUDIT_2026-11-20, open-loops tracker, morning brief 20 Nov, ops check 21 Nov, cron outputs, sessions)
**Note:** 👵 **Mum: caregiver chain silent ~77h (18–20 Nov all missing) — 3rd flag to H.** 🦷 **H food diary 8-day gap (RED).** 💼 **20 Nov sales row pending (due 04:30 Sat) — 17 Nov still unlogged.** 🟡 **Security 20 Nov STABLE — BUT WhatsApp adapter OFF now clearly blocks Mum/Dad/family check-ins.** 🚨 **Flooder loop day 6: FB poster = REAL overnight batch posts; checkin-mum = pure failed-WA spam.**

## Related
- [[INTEGRATED_INSIGHTS_2026-11-19]] · [[2026-11-19]] · [[daily-sales-log]] · [[DEADLINES_AND_FOLLOWUPS]]
- [[MUM_MEDICAL_MASTER]] · [[H_MEDICAL_MASTER]] · [[SECURITY_AUDIT_2026-11-20]]
- [[DECISION_LOG]] · [[FAMILY_CHECKINS_2026-11]]

---

## 1. Health

### Mum (Comfort, 91, Weija) — 🔴 CHAIN SILENT ~77h, RE-FLAGGED (3rd flag)
- 🔴 **NO caregiver report since 17 Nov 20:58** (back-pain recurrence, Aboniki + lay-flat, early night). 18, 19, 20 Nov all missing → silent gap ~77h by Sat 02:09. **FLAGGED to H 19 Nov eve >48h; gap nearly doubled since — RE-FLAGGED this run (morning/afternoon/evening prompts re-posted to topic 4; STEPHANIE_SILENT_INTAKE 0 unprocessed of 56).**
- 💆 **Masseuse cadence day Fri 20 Nov — session status UNKNOWN** (17 Nov was no-show; reschedule still pending). Plumber reschedule pending. Tiger-nut milk soaking status unknown.
- ⚠️ **No BP since 16 Nov evening (last 124/70 · P68 · T36.0 — ~4.5 days)** · meals unlogged since 17 Nov (>3 days 🟡→🔴) · kidney capsule status unknown since 17 Nov.
- ✅ BP streak clean across every captured reading (9→13→14→16 Nov); **Furosemide stop-rule (<100/>140, RIGHT arm) never fired**; no 24 Oct perceptual-ep recurrence.
- 🔍 **Root cause of silence likely WA adapter OFF since 18 Nov** — checkin-mum send attempts fail (localhost:3000 refused, no Telegram fallback per policy). Chase Stephanie + restore bridge.
- Open: Imodium OUT (10+ wks) · Na labs overdue · Kenus-spa recurrence ask · milk replacement.

### H (Herbert, 52, Accra) — 🔴 food diary 8-day gap (RED, worsening)
- 🔴 **14–21 Nov silent = 8-DAY GAP** (last log 13 Nov clean day; evening prompt sent to keep restart alive).
- 🔴 **Renerve Plus ZERO — tremor unmedicated 54 days** · 31 Aug post-shock review undocumented **82 days** · labs (1,075 GH) still pending (requisition photo never reached Nita) · dental (12 Oct) unlogged **40 days** · **no fresh vitals since 24 Aug (89 days)** — longest on record. Ibuprofen 400 mg/day = GI/kidney risk until labs run.
- 🟢 **No new acute onset since 29 Sep (53 days clear)**; no chest pain; no dysphagia; pericarditis quiescent. AM headaches + sinus (22 Sep onset) still watch-listed.

### Dad (Robert, 92, UK) — 🟠 jab window ~2 wks left
- 🔴 **Winter flu+COVID jabs STILL unbooked** (window closes ~6 Dec) · no snapshot since 25 Oct · 16 Jul foot unrecorded. **ONE GP call** closes foot + AAA + PSA + jabs.
- ⚠️ Check-in attempts keep FAILING: `Cannot connect to host localhost:3000` — WhatsApp adapter down (see Security). No success path until bridge restored.

---

## 2. Business (2Real)

### Sales — ⚠️ 20 Nov row PENDING (not a gap yet: rule allows until 04:30 next morning)
- ⚠️ **`daily-sales-log.md` last row = 19 Nov (4,980/58%).** 20 Nov (Fri, market day) row NOT posted as of 02:14 Sat — expected in the **04:30 Sat Jiji→Ledger report**; confirm at Sat morning brief. Never flag inside window.
- 🧾 **Ledger debt: 7 + 10 + 17 Nov STILL UNLOGGED** (17 Nov Tue was a working day — morning brief 20 Nov flagged "Needs OK: add?").
- ✅ **19 Nov logged: 4,980 GHS · 58% · profit 2,880** — Sepha (old cus, event furniture), Tanko (new scrap contact), Xbox One S.

### Channels & ops (overnight — real work + one spam loop)
- 🚨 **FB Marketplace Batch Poster (`5128ceaa2c09`) actively posting overnight in chunks of 3 via CDP** (port 64365): fixed item 16681010 saw condition NEW→USED after photo proof, added researched specs for 16681010/14948478/14684112, linted descs (slopcheck) — **genuine batch-posting work, but running as a ~1-min runaway loop off its 10:00 schedule (day 6).**
- 🚨 **WA catalogue posting also running overnight** (`wa_cdp_run.py 3`, chunks of 3; dedupe vs fb_posted/master registries verified). WA cat Q previously COMPLETE 109/109.
- ⚠️ **checkin-mum (`c3db50f4f9af`) = 100% FAILED-WA spam** — every ~1 min tries a WA send, refused (bridge down), logs failure. Pure noise (see System).
- ✅ Jiji live **~1,404–1,407 active** (ops check 21 Nov 02:14: 1404/1404 active, no sold-out/low-stock flags) · lead nudger OK · customer queue quiet (newest lead 07 Nov; **Bosch jigsaw / East Legon lead from 19 Oct ~5 wks open** — nudge candidate; +233 57 770 0555 flag still open) · sourcing all within SLA (Olymech RFQ 6000997164 still outstanding ~7 wks).
- ⚠️ **Content STALE ~26d**: newest week on disk = week-2026-10-26; Sunday engine failed 15/11; Sat 21 Nov WA Status delivered from week-10-26 batch (Gorilla weekend drop) — **P-7 PENDING H REVIEW before publishing.**

### Receivables / admin
- 💰 **Hagija GH₵4,000 OVERDUE since 2 Nov (19d, DO FIRST)** · **market rent + Fluid CC due 22 Nov (TOMORROW)** · Joycelyn 2,500 · VAT 10-M UNCONFIRMED · **WA Ads dark ~35d** · Olymech RFQ · act ICT inverters qty unconfirmed · white-paint COGS · Tweneboah receipt + Dunlop/Sony ad closures · 08/11 grinder price (700 vs 70) · **ironing-board COGS (NEW, 19 Nov)** · Hagija toys COGS.
- 📢 **B2B broadcast list primed (#7+):** Eric (Enterprise Ins), Dr Lomotey (Cocoa Clinic), tool lover 0245849519, Edwin (contractor 0550253348), Theophilus (Airbnb 0500599813), Emmanuel (tennis), + Gbawe Rasta (0248150115). Fire when matching stock lands.

### TAIWAH Christmas reel — still ON HOLD (17 Nov ruling)
- Exit-narrative ban stands (rented-shop, no clearing framing); face LOCKED to MASTER_LOCK.png. Brief waits for H context.

---

## 3. Security Posture — 🟡 STABLE (audit 20 Nov 07:05, saved to Vault/System/Assistant/)
- ✅ **TG token VALID** (live getMe @Ogaitchhermesbot) · gateway PID 25084 up, no crash loop · **0 backup .env copies** · ACLs locked (env/auth/google_token) · **no InvalidToken / provider 4xx this window** · topic 20 confirmed live.
- ⚠️ **WHATSAPP ADAPTER OFF persists** (`platforms.whatsapp.enabled:false` since 18 Nov, creds live) — **intent still UNCONFIRMED; NOW the confirmed root cause of Mum + Dad + family check-in failures** (localhost:3000 refused). Ask H: intentional hold or regression → re-enable.
- ⚠️ **Nous Portal revoked (3rd+ cycle, UNREMEDIATED)** — `hermes auth add nous`.
- ⚠️ Persistent WARNs: 24/55 silent cron targets (`origin`/`local`) · dead-thread `123286468` (2 Mom exercise-reminder jobs → migrate to 424) · multiplex dup-credential (default/content-buddy, default/sat-nav) · stale `~/.hermes/.env` placeholder token · 4 runtime `.env`-reader scripts · `allow_all_users: true` · **cron receipt backlog 483 deferred admissions**.
- 🟠 **21 Nov 02:08 security run ERROR** (status:error — likely transient); next cycle 07:00 Sat retries.

---

## 4. System Health
- 🚨 **Flooder storm day 6 — with nuance:** since 22:00, **47 cron outputs; 31 from the two loops** — `5128ceaa2c09` FB poster (17, doing REAL post batches) + `c3db50f4f9af` checkin-mum (14, 100% failed-WA spam). Both emit ~1/min off-schedule → **verify live scheduler; kill the checkin-mum loop; give FB poster a controlled batch runner.**
- ✅ Most scheduled jobs healthy **20 Nov (Fri):** morning brief 07:03 · security audit 07:05 (PASS) · Jiji→ledger 04:32 · ops check · WA cat poster · lead nudger · open-loops tracker (18:00/20:26) · tasks-queue-sync 02:14 (**32 open tasks, all synced to kanban — 0 changes**).
- ✅ **Backup:** last success 15 Nov 23:04 (26,866 files, 5 DBs byte-verified); **next Sun 22 Nov (tomorrow)**.
- ✅ Active session dumps: **0** (118 in .archive) — nothing to archive.
- ✅ integrated-daily-synthesis job healthy (`d719cd80fa5b`, 22:05 → topic 20).
- 🗂 Sessions last 24h: all cron (21), no interactive H conversations (last genuine user session several days ago).

---

## 5. Priority Actions (CRITICAL → HIGH → MEDIUM)

**CRITICAL:**
1. 👵 **Mum: chase Stephanie / reporting flow — chain silent ~77h (3rd flag)**; confirm Fri masseuse + plumber; restore WA bridge so reports can flow.
2. 💰 **Hagija 4,000 (19d OVERDUE)** + **market rent + Fluid CC due 22 Nov (TOMORROW)**.
3. 🚨 **Kill the flooder loops day 6** — esp. checkin-mum spam; give FB poster a controlled schedule (it IS doing real work, just as a runaway loop).
4. 🔒 **CONFIRM WhatsApp adapter intent (enabled:false)** — currently blocks Mum/Dad/family check-ins and is the likely driver of the Mum data blackout.

**HIGH:**
5. 🍽️ **H: log a meal (8-day RED) · reorder Renerve (54d zero) · ONE clinic call (labs + dental + 31 Aug closure) · fresh BP.**
6. 👴 **Dad: ONE GP call** — foot + AAA + PSA + winter jabs (window ~6 Dec).
7. 📊 Log **17 Nov** ledger (still missing) + confirm **20 Nov** row at 04:30 · content engine rerun (26d stale, P-7 sign-off) · Nous Portal re-auth.

**MEDIUM:**
8. ⚙️ Faulty-grinder repair-bench DECISION · WA Ads renew-or-kill (~35d) · Olymech RFQ · Jiji ad closures (Dunlop + Sony) · Tweneboah receipt · 2 Mom jobs → thread 424 · 08/11 grinder price confirm · ironing-board COGS · act ICT qty · Bosch-jigsaw lead nudge (+233 57 770 0555).

---

## 6. Weekly Overview
| Day | Sales GHS | Note |
|-----|-----------|------|
| 13 Nov (Fri) | 400 (74%) ✅ | bofrot-seller bag + Sony woofer |
| 14 Nov (Sat) | 600 (85%) ✅ | fridge compressor + Stanley multi tool |
| 15 Nov (Sun) | — | ✅ day off |
| 16 Nov (Mon) | — | ✅ day off |
| 17 Nov (Tue) | — | ⚠️ UNLOGGED (working day — add) |
| 18 Nov (Wed) | 510 (55%) ✅ | T-Rex tape + Bosch grinder as-is + spray |
| 19 Nov (Thu) | **4,980 (58%) ✅** | Sepha bistro ×3 + Tanko laptops + Xbox |
| 20 Nov (Fri) | ⏳ PENDING | row due 04:30 Sat — confirm at brief |

- **Ledger debt: 7 + 10 + 17 Nov.** Week pace strong off Thu's 4,980 (2× target) once 17/20 Nov confirm.
- Receivables: Hagija 4,000 + Joycelyn 2,500. New contacts: Tanko (scrap), Sepha (event furniture). B2B broadcast list primed (#7+).

# WEEKLY LEARNING — 2026-08-31

**Period reviewed:** 24–31 Aug 2026 (Mon–Mon) · **DMY dates**
**Source:** Weekly synthesis of the past 7 days' integrated daily insights (`INTEGRATED_INSIGHTS_2026-08-24/26/28/31.md`).

> ✅ **Pipeline note:** The daily `INTEGRATED_INSIGHTS_*.md` synthesis is **RUNNING AGAIN** (job `d719cd80fa5b`, delivers to Telegram topic 20). This is the first week since the June outage where the weekly review can be built directly from genuine daily insights rather than reconstructed from raw operating data. Four daily files covered the window (24/26/28/31 Aug); the 29 & 30 Aug days are folded into the 31 Aug run (2-day reporting gap).

---

## 1. PATTERNS (recurring signals across the week)

1. **H's health pipeline finally moved after months of stuck flags.** The 73-day-overdue post-shock evaluation broke open on 24 Aug: saw Dr. Addo Danquah, labs ordered (7 tests → 1,075 GH₵ incl. PSA 170), painful-toe X-ray (219 GH₵), and **Renerve (methylcobalamin/B12, 295 GH₵) prescribed & filled for the left-arm tremor**. Vitals gap closed (84 days). Dental booked 12 Oct. The bottleneck just shifted — from "never saw the doctor" to **"the lab photo never transmitted, so the 31 Aug review isn't confirmed."**
2. **Mum is stable but the same three care flags keep recurring weekly:** (a) Furosemide dose is punctual + logged (the reliable win), but **BP ≥140 systolic stop-rule anomalies persist (18/20/22/26/28 Aug) yet Furosemide still given**; (b) **fried fish / fried plantain / grains still breach the phase-out diet**; (c) **data capture from the caregiver is patchy** (24 AM, 26, 27–28, 29–30 Aug all missed/readable-late). New this week: **insomnia** (woke carer 2:16am 26 Aug) and a **back/hip pain flag** (28 Aug → paracetamol; also seen 3 Aug — monitor recurrence).
3. **Weekend electronics carry 2Real sales; mid-week dips.** 25/08=GHS 800, 26/08=640, 27/08=400 (dip), **28/08=2,200** (incl. GHS 200 repairs), **29/08=3,000** (2× iMac, Yamaha PSR-175, 2× baby laptops). Sat 29 alone ≈ 38% of the week (~GHS 7,040). Consistent with the established Fri–Sat load-bearing pattern.
4. **The auto-responder is catching inquiries but not closing them — the backlog is growing faster than conversion.** 28/08: 53 SLA-breach threads (oldest 74–82h, unanswered "hammer" caller). **31/08: 200 entries / 131 unresolved / 119 critical** in the loop. Overnight messages auto-replied "we'll get back to you" but not actioned. This is now the **#1 operational risk**.
5. **Warm in-stock, high-margin singles are the missed sale.** Same cluster all week: Stanley Tape Measure 10m (GHS 700, qty 1), INGCO Hydraulic Bottle Jack HBJ602 (GHS 450, qty 1), Flopro 8-head Spray Gun (GHS 275), Under-Cabinet Light Kit (GHS 380). 480 items sit at stock ≤2 — ~half the in-stock catalogue is single-unit UK leftovers.

## 2. KEY LEARNINGS

1. **Health follow-through is now the model.** The 24 Aug doctor visit shows the whole care pipeline (medical master + check-ins + synthesis) working when drive-through happens. The lesson: when a system has been broken for weeks, a single decisive external event (an actual consult) unblocks everything downstream.
2. **A single failed attachment breaks an entire medical thread.** The lab photo not reaching Nita stalled the 31 Aug review booking for a full week. Redundant transmission (photo + call + written requisition) should be the norm for anything clinical.
3. **Content generation is solved; publication + measurement is still the standing failure.** Week 2026-08-31 fully built (all 7 days, Taiwah on 3 2Real days, BOSCH Power Weekend, Akoma), logos composited (no hallucination) — but **MP4 renders still pending** (FFmpeg tooling constraint) and **still no verified post / no analytics** across consecutive weeks.
4. **A manual gate in the middle kills live data.** Jiji live stats have been **stale since 24 Aug** purely because a Chrome "Allow remote debugging" popup needs one human click. GH₵0 balance also blocks TOP+. Small manual blockers have outsized cost.
5. **Farm is becoming an income-trackable line.** 30 Aug coordination: **230 mature coconut trees confirmed** (per-tree harvest next), plantain 4 bunches (~20 Sep first harvest), welder hive-stand quote GHS 400 (GHS 730 covers 8 stands = best value), equipment delivered (rabbit drinkers → dirty-oil pest moats). August farm spend: GHS 1,605.

## 3. Actionable improvements (next 7 days)

**Priority 1 — H medical (TODAY, 31 Aug):**
- Call UGMC / re-send the lab requisition photo so the **31 Aug review with Dr. Addo Danquah** is confirmed and labs + toe X-ray are on record. This has been pending since 24 Aug.
- Resume H food/meal logging (gap since 28 Aug); take one routine vitals re-read.

**Priority 2 — clear the 2Real inquiry backlog (conversion engine):**
- Work the **131 unresolved / 119 critical** loop entries; close the warm in-stock leads: Stanley Tape Measure (700), Arlec power sockets ×2 (120 ea), INGCO Bottle Jack (450). Prioritise the unanswered "hammer" caller (conversion being actively lost).
- Reply pending Jiji clients and recharge GH₵ balance for TOP+.

**Priority 3 — Mum care (birthday-week flags):**
- Capture 29–30 Aug + current vitals from caregiver (Stephanie); watch back/hip-pain recurrence and the ≥140 stop-rule anomalies; flag insomnia + diet breaches at the next doctor review. Keep garlic/water/elevation as logged daily items (the Furosemide dose-log pattern works — mirror it).

**Priority 4 — restore live data + unblock Jiji:**
- One manual click on the Chrome "Allow remote debugging" popup to restore live Jiji stats (stale since 24 Aug).

**Priority 5 — kids' medical:**
- **Book the Mission Clinic appointments** for Kobena (neuro-paediatric) + Nenyi (psychology/speech + PEERS®). Prep is done (22 Aug); the appointment itself is still unbooked. Call +233 20 329 5292.

**Priority 6 — reliability/security:**
- Static DNS (8.8.8.8/1.1.1.1) to end the recurring Telegram/DNS flakiness.
- Reconcile the **dual-root `.env` / gateway divergence** (AppData token valid + gateway live vs home-root `~/.hermes/.env` corrupt + `startup_failed`); repair the home-root cron execution ledger (`executions.db` empty).
- Purge remaining 9 legacy `google_token.json` copies (improved 26→9), rewrite live `.env`-reader scripts, re-point 25 silent cron deliveries.

## 4. Things that stalled / were not resolved
- **H lab photo not transmitted** (24 → 31 Aug; the week's central blocker).
- **No confirmed content post / no analytics** (consecutive weeks; MP4 render tooling still unresolved).
- **Jiji live data stale** since 24 Aug (manual Chrome popup).
- **Dad (Robert) data gap** — foot-case outcome 4+ wks overdue; PSA/aneurysm unconfirmed; master doc stale.
- **Mum 53+ inquiry SLA breaches → 119 critical** by week's end (growing, not clearing).
- **Cron execution ledger not persisting** to home root (`executions.db` = 0 rows) — monitoring gap.
- **Mission Clinic kids' appointments** still unbooked despite completed prep.
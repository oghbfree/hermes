# 📚 WEEKLY LEARNING & INSIGHTS — 10–17 AUGUST 2026

**Period:** Mon 10 Aug 2026 → Sun 16 Aug 2026 (generated Mon 17 Aug)
**Generated:** 2026-08-17 09:xx UTC
**Sources:** SECURITY_AUDIT_2026-08-11 → 08-17 (6 audits), Daily notes 08-13/14/16, content sent/improvements logs, 2Real ops, git commit history
**Source health:** ⚠️ **Zero `INTEGRATED_INSIGHTS` files exist for this week** — pipeline down 30 days (last: 18 Jul). Report reconstructed from daily notes, security audits, and ops logs.

---

## 1. EXECUTIVE SUMMARY

The dominant event this week was a **systemic insight-pipeline failure**: the `integrated-daily-synthesis` job has been silently skipping (`drift_skip`) since 18 July because its provider/model is unpinned, so **no `INTEGRATED_INSIGHTS` files were produced for this week** — the weekly review had to be rebuilt from security audits, daily notes, and ops logs instead. Underneath that, three real improvements landed (Telegram token recovered & VALID, gateway confirmed UP, content engine finally producing on the new qty=1 stock rule), while three structural debts persist or worsened (credential leak via 30 backup `.env` copies + `bws_cache.json`, 41–50% cron SLA trending down, WhatsApp unpaired ~70 days). **Biggest risk:** the same *silent* failure mode that hid this week's insight gap — unpinned jobs refusing to run — is quietly hollowing out monitoring.

---

## 2. PATTERN ANALYSIS

### Pattern A: 🔴 Insight Pipeline Broken — Unpinned Job `drift_skip` (REMEDIATION DEBT, NEW)
The weekly/daily synthesis that this report depends on is itself failing.

| Date | Job | Status | Evidence |
|------|-----|--------|----------|
| Aug 13 | integrated-daily-synthesis (`ac813a924bbd`) | ❌ drift_skip | Model drifted `nemotron-3-ultra-550b:free` → `deepseek-v4-flash-0731`; unpinned |
| Aug 14 | integrated-daily-synthesis | ❌ drift_skip | "No INTEGRATED_INSIGHTS since Jul 18. Fix: pin provider/model." |
| Aug 16 | integrated-daily-synthesis | ❌ drift_skip | Same; also `mom-exercise` drift_skip x2 |
| Aug 10–17 | **INTEGRATED_INSIGHTS files** | **0 produced** | Last file = 2026-07-18 (canonical `memories/insights/`) |

- **Key insight:** Unpinned cron jobs with model drift refuse to run and fail *silently* as a `drift_skip` — no `INTEGRATED_INSIGHTS`, no alert. The monitoring layer went dark without tripping any alarm. If the weekly review hadn't independently discovered this, the gap would be invisible.
- **Actionable fix:** Pin `provider=openrouter model=deepseek/deepseek-v4-flash-0731` (or the current default) on `ac813a924bbd` AND audit every job for a `model:` pin. Add a heartbeat check that alerts if `INTEGRATED_INSIGHTS_*` is older than ~26h.

### Pattern B: 🔴 Credential-Exposure Debt Worsening (REMEDIATION DEBT ≥ 4 CYCLES — ESCALATE)
| Item | Jul 13 | Aug 13 | Aug 17 | Trend |
|------|-------|--------|--------|-------|
| Backup `.env` copies | ~12 | 22 | **30** | 🔴 WORSENING (+1 this week) |
| `bws_cache.json` plaintext (incl. GitHub PAT) | present | present | **present** | 🔴 Unresolved |
| Live `.py` `.env`-readers | ~26 | 33 | **~26** | 🟡 Flat |
| Google token ACL | PASS | PASS | PASS | ✅ |

- **Key insight:** Even with the primary `.env` rotated, secrets leak through *proliferating backup copies and a persistent plaintext cache*. The count is *growing* (+1 to 30 this week alone) — deletion is not keeping pace with regeneration.
- **Actionable fix:** One dedicated cleanup session (not cron): delete `bws_cache.json`, purge the 30 backup `.env` copies, and add backup-exclusion rules; then a `chmod 600`/scan cron to prevent regrowth.

### Pattern C: ✅ Telegram Recovery + Gateway State vs Reality (lesson learned)
| Item | Aug 13 | Aug 15 | Aug 16 | Aug 17 |
|------|--------|--------|--------|--------|
| Telegram token | VALID | VALID | VALID | ✅ VALID (@Ogaitchhermesbot, getMe ok) |
| Gateway | up | **DOWN (regression)** | DOWN | ✅ **UP PID 24152**, ESTABLISHED → Telegram |
| Auth block | — | blocked user 5146706699 | — | ✅ permission control working |

- **Key insight:** The Aug 17 00:24 audit reported "day-4 gateway DOWN" from a **stale `gateway_state.json` PID (5596)**, but live `tasklist`/`netstat`/`getWebhookInfo` showed the real gateway UP (PID 24152) with ESTABLISHED TCP to Telegram. **Status files lie; live process/TCP checks are truth.** This caused a same-day false alarm and re-run.
- **Actionable fix:** Fix gateway PID-state sync so the state file tracks the live PID (README in the audit notes this). When an audit says DOWN, verify with `hermes status` + `getWebhookInfo` before alerting.

### Pattern D: ✅ Content Pipeline Finally Producing (genuine improvement)
- Aug 14 **early run** for week of Aug 17: **25 images on disk + 14 captions/scripts + 6 carousel specs + 3 LinkedIn + 1 article** (vs 0 in many prior weeks). Self-score **85/100**.
- New qty=1 stock rule applied correctly: **"BOSCH POWER WEEKEND"** features genuine single-unit items (GBH 2-26 DRE GHC 2,300; GBM 13-2 RE GHC 1,800; etc.) with TRUE scarcity framing.
- 15 targeted marketing skills applied; logos composited via PIL from official source.
- Continuous-improvement loop (R1–R6) added to `SUNDAY_CONTENT_ENGINE_PROMPT.md` + skill pitfalls 31–33.
- **Key insight:** The pain point moved from *production* to *handoff*: assets generated but **pending H review → John posting** — and carousels are still text specs, not rendered panels. Same age-old Production ≠ Delivery pattern.
- **Actionable fix:** Render full 6-panel carousels as images (John can't build from text); add marketplace price-and-delivery files; get the H-approval → John-publish gate moving.

### Pattern E: 🟡 Cron SLA Trending Down
| Date | SLA | Detail |
|------|-----|--------|
| Aug 14 | ~50% | 25/50 OK, 25 errored |
| Aug 16 | ~41% | 18/44 OK, 26 errored (18 connection/offline at 10:16 batch + 9 drift_skip) |
- **Key insight:** Failures cluster as **systemic connection/offline batches** + **drift_skip** — infra and model-pinning, not logic bugs. The DNS-static-hosts fix (149.154.166.110) is in place and helping Telegram delivery.
- **Actionable fix:** Treat 10:16-window offline batches as an infra investigation; continue pinning unpinned jobs.

---

## 3. SYSTEM PERFORMANCE METRICS

| Day | Cron SLA | Backup | Security | Telegram | Key Failures |
|-----|----------|--------|----------|----------|--------------|
| Aug 11 | ~? | — | FAIL | VALID | audit generated |
| Aug 12 | — | ✅ 23:03, 30,671 files/3.9GB | FAIL (22 .env) | VALID | WhatsApp 509th attempt |
| Aug 13 | ~50% | ✅ 23:09, 17,461 files | FAIL (22→?) | VALID | 2Real ops check: skill not found |
| Aug 14 | ~50% | — | FAIL (25 .env, +3) | VALID | **synthesis drift_skip** |
| Aug 15 | — | ✅ 23:27, 17,531 files, all DBs byte-verified | FAIL (25 .env) | VALID | gateway regression (false) |
| Aug 16 | ~41% | — | FAIL | VALID | 18 offline + 9 drift_skip |
| Aug 17 | — | — | FAIL (30 .env) | ✅ VALID | gateway "DOWN" → false alarm |

---

## 4. KEY LEARNINGS

1. **Silent `drift_skip` failures are the most dangerous type.** A whole monitoring pipeline (daily + weekly synthesis) can be down for 30 days with zero `INTEGRATED_INSIGHTS` produced and no alarm. Unpinned jobs + model drift = invisible outage. Pin everything; add a freshness heartbeat.
2. **Status/state files are not the source of truth.** The gateway looked "DOWN (day 4)" from stale PID state when the process was genuinely UP. Always confirm lifecycle via live processes/TCP before declaring an outage.
3. **Credential debt grows if you only delete, never stop regeneration.** Backup `.env` copies went 22 → 30 in one week because nothing excludes them from backup. Fix the source (exclusions + protected store), not just the symptom.
4. **Content progress moved from production to handoff.** The engine now reliably generates (85/100 self-score, real qty=1 scarcity) but stops at H-approval/John-posting and text-spec carousels — the delivery gate is the new bottleneck.
5. **Data recovery returns:** The week's valuable facts (Container 26 settlement £900 + 5,897.58 GH₵; real-estate Kroboano/Nenyi Oliver deal; H masters rebuilt; 2Real 7 missed in-stock items with 19 SLA breaches, worst 574h) all live in `Vault/` files that survived — because the Obsidian vault is the durable store, not the broken insight pipeline.

---

## 5. ACTIONABLE IMPROVEMENTS

| # | Action | Impact | Effort | Timeframe |
|---|--------|--------|--------|-----------|
| 1 | **Pin provider/model on `integrated-daily-synthesis` (+ all unpinned jobs); add insights-freshness heartbeat alert** | Restores daily+weekly insight pipeline | Low | This week |
| 2 | **Security cleanup session: delete `bws_cache.json`, purge 30 backup `.env`, add backup exclusions, chmod 600** | Removes highest-risk credential leak | Medium | This week |
| 3 | **Fix gateway PID-state sync** (state file = live PID) to stop false-DOWN alarms | Removes false alerts | Low | This week |
| 4 | **Render full 6-panel carousels as images + marketplace price/delivery files; push H→John posting gate** | Closes content delivery loop | Medium | Next 2 weeks |
| 5 | **Investigate 10:16 offline/failure batch + WhatsApp re-pair decision (~70 days)** | Cron SLA + channel recovery | Medium | Next 2 weeks |

---

## 6. WEEKLY SCORECARD

| Category | Rating | Trend | Notes |
|----------|--------|-------|-------|
| Insight/Synthesis pipeline | **F** | ↓ | 30 days no INTEGRATED_INSIGHTS; drift_skip |
| Security posture | **D** | ↓ | 30 backup `.env`, bws_cache.json; token now VALID is only win |
| Cron reliability | **D** | ↓ | 41–50% SLA, offline batches + drift_skip |
| Telegram/gateway | **B** | ↑ | Token VALID, gateway UP; false-DOWN fixed |
| Content pipeline | **B+** | ↑ | 85/100 self-score, qty=1 rule working; delivery gate open |
| Business ops | **B** | **→** | Container 26 settled; 2Real SLA breaches (worst 574h) need replies |
| Backup integrity | **A** | ↑ | Daily byte-verified backups all week |

**Overall verdict:** Two systems genuinely improved (Telegram recovery + content generation), but **the insight/synthesis layer — the very thing that turns daily events into weekly learning — collapsed silently for 30 days**, and security/credential debt worsened. The week's true lesson: a monitoring system that goes dark without alerting is worse than one that fails loudly. Fix the pinning and the heartbeat first.

---

*Report saved to: `memories/insights/WEEKLY_LEARNING_2026-08-17.md` (+ workspace mirror)*
*Next weekly review: 2026-08-24*
*Note: no INTEGRATED_INSIGHTS files existed for this week (pipeline down since 18 Jul); report reconstructed from SECURITY_AUDIT (6), daily notes, and ops logs. Restoring the integrated-daily-synthesis job is Action #1.*

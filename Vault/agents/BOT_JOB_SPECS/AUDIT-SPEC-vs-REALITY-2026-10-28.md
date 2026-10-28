# 🔍 SPEC-vs-REALITY AUDIT — bots vs their Job Descriptions (28/10/26)

> Evidence-based check: does each bot actually DO what its JD says? Written specs only matter if behavior matches. Re-run monthly (or when a bot underperforms). Source of truth for each line: on-disk artifacts + cron run history + delivery records — NOT the bot's self-report (self-reports are unverified).

## Results

| Bot | JD says | Reality (evidence) | Verdict |
|---|---|---|---|
| **sat-nav** | CEO front door, full stack, gates | 7 audit-logged actions 28/10: gbrain embeddings ON + verified (buyer_registry top hit 0.8654), structured ingestion done, HOUSE_RULES + model split + decision log built + broadcast, Stephanie silent-intake wired, CEO brief cron delivered | ✅ **MATCH** |
| **content-buddy (Kofi)** | draft-only creative, SlopMonster 5/5, real assets | Output verified on disk: week-2026-10-26 (25/10 19:36) + sunday-groups PASTE-READY + testimonial cards; confirmed all 8 rails in DM. SlopMonster re-verify = the #1 discipline to keep (claimed-clean ≠ verified) | ✅ **MATCH** (watch: slopcheck self-verify) |
| **coach** | networking + group strategy, draft-only, RBAC | Files fresh: fb-group-log + whatsapp-group-log + first-lines (25/10), first-group-posts (21/10); confirmed alignment DM. RBAC respected (no post to ⏳ groups per log) | ✅ **MATCH** |
| **taiwah** | brand voice, face LOCKED, draft-only | Reels + cards to week-2026-10-19 (20/10) incl. container reel v2; MASTER_LOCK face canonical on disk; confirmed all 8 rails + playbook patch DM. **Gap: no delivery since 20/10 — voice content cadence is draft-briefed, verify next brief** | ⚠️ **CADENCE GAP** |
| **hermes (OG)** | gateway/delivery, H's direct line, informs sat-nav | Gateway RUNNING (pid 15048, verified). Accepted rails 1-6+8; agreed coordination via sat-nav. **One standing thread: wants the front-door line from H's own session** (non-blocking) | ✅ **MATCH** (1 open thread) |
| **harold** | DRAFT-LEVEL ONLY — NOT executor | 5/5 controlled execution tests FAILED 18/10 (documented); 6 money/time-critical crons REVERTED away from him. JD now makes the limitation written + explicit. **No new failure since the spec — but no proof of execution either (correct posture is none-expected)** | ✅ **MATCH** (by design — never route execution) |

## Key findings

1. **The stack mostly matches its specs** — the JD system didn't invent problems; it documented behavior that was already largely correct. That's the property you want.

2. **Two action items surfaced:**
   - **taiwah cadence gap** — voice/face output last landed 20/10. Not a spec violation (she's draft-briefed, not scheduled), but flag for the next content brief so she actually produces.
   - **harold = the honest "underperformer" by design** — his spec converts a known failure into a written boundary. The correction-loop fix here is *routing discipline* (never send him execution), which the spec now enforces.

3. **The #1 recurring-correction candidate** (from CORRECTIONS_LOG): Kofi's testimonial attribution + SlopMonster re-verification — two separate corrections already landed on the same rule. That rule is now written in HOUSE_RULES §4 + his JD. Watch for a 3rd occurrence → lock harder.

## What I'm doing next (per the loop)
- Corrections with ≥2 repeats → already promoted to written rules (JD + HOUSE_RULES). Logged in CORRECTIONS_LOG.
- Routine: every bot's AUDIT_LOG line after each state-changing action (started today).
- This audit re-runs automatically monthly, or on-demand when a bot underperforms.

---
*Log: AUDIT_LOG.md carries the state-changing actions that back this audit.*

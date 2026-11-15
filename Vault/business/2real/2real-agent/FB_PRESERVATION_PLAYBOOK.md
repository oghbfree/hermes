# Facebook Marketplace — PRESERVATION Playbook (read before ANY FB action)
**File owner:** 2Real (H + sat-nav) | **Version:** 01/11/26 — after Marketplace review SUCCEEDED (restriction lifted 31/10→01/11)
**Doctrine: "This cannot happen again — it is TOO VALUABLE."**

> The most recent restriction cited Policy "Fraud, scams and deceptive practices":
> *"Your profile or activity may have deceived people to take their money."* The
> review SUCCEEDED (account restored 01/11). Everything below exists so no silent
> automated behaviour ever re-triggers it. When in doubt, this file wins over any
> cron, queue, or prompt.

---

## 1. THE PRIME RULE — human-in-the-loop on anything risky
- **NO automated FB posting until an explicit H go-ahead per batch.** The two FB
  crons (`Daily Marketplace Monitor` id 0ef160b1; `FB Marketplace Batch Poster`
  id 5128ceaa) stay **PAUSED** by default. Permanently. FB is manual/guarded now.
- A cron may **draft and stage**, but must NOT publish without H approving the
  specific batch. Publishing = an H-approved deliberate act, never a fire-and-forget job.
- **Re-enable saved-for-review drafting** (safe, no risk) — but NOT auto-publish.

## 2. Why the ban happened — attack the root, not the symptom
The flag was *deception / taking money*. Real triggers to eliminate:
- **Over-claiming condition:** "UK Imported, Quality Checked" on items that are
  used/untested. If it is NOT verified-working, say so (honest condition line),
  and NEVER imply a guarantee we can't honour.
- **Price mismatch across channels:** Jiji vs WhatsApp catalog vs FB MUST be one
  price (gold list). A customer seeing FB ¥ higher than Jiji = feels deceived.
- **Duplicate/identical listings:** FB merges/suspects repeats. One listing per
  product, ever, with mandatory TEXT + PHOTO variation (already in playbook §6).
- **Misleading photos:** photos must match the actual item delivered, including
  defects. Stale shelf photos of a different unit = deception.
- **Burst volume:** mass-posting lights up the fraud screen. Pacing is protection.

## 3. HARD CEILINGS (non-negotiable, enforced)
| Guard | Rule |
|-------|------|
| Max **new** listings | 3–5/account/day (≤15 absolute; prefer 3–5 while rebuilt trust) |
| Duplicate check | MANDATORY before every post: scan live Selling page + `fb_posted.json` (string compare) — see canonical playbook §anti-ban |
| One listing per product | EVER. Re-list only on explicit H order |
| Text variation | `fb_post_lib.make_desc()` rotates openers/closers — required |
| Photo variation | `vary_photo()` micro-crop + re-encode per listing — required |
| Sleep between listings | 2–5 min (pacing = protection) |
| Price | EXACTLY the gold price list, one price everywhere |
| Photo honesty | Include a defect shot; never a mismatched shelf photo |
| "UK Imported / Quality Checked" | ONLY on items actually tested-working; otherwise honest condition ("UK pre-owned, untested" / "For parts") |

## 4. The 3-Layer Duplicate Guard (runs on EVERY post)
1. Live page scan: `facebook.com/marketplace/you/selling` — fuzzy title match → skip.
2. `fb_posted.json` ID check (strings, not ints).
3. Master registry `channel_posted_master.json` / `fb_marketplace_progress.json` —
   never re-post what's already listed.
If ANY layer flags it: SKIP. No exceptions, no "but the queue says so."

## 5. Re-entry — RESUMPTION AUTHORIZED (H unlock 14/11/26, per-batch H drive)
**The 02/11/26 "shelved indefinitely" verdict is SUPERSEDED by H's 14/11/26 go.**
H confirmed the Marketplace lock is cleared and instructed sat-nav to **revise this
playbook and post on FB** — that is the explicit per-batch H go-ahead §1 requires.
The 4 lockouts of 02/11 were real, so the POSTURE stays guarded, but forwarding has
resumed under H's direct drive:
- **FB Marketplace Batch Poster (5128ceaa2c09) = RESUME** under the **guard
  cap: ≤3 new listings/day** (hard daily counter enforced; do NOT raise). This is
  H-authorized forwarding, not a fire-and-forget privilege — H drives which
  batches go, sat-nav executes the approved batch within the cap.
- **Daily Marketplace Monitor (0ef160b1c270) = RESUME** (read-only — safe).
- **FB Messages Monitor (589664dd3068) = RESUME** (read-only buyer-thread
  oversight + nudge proposals; discounts still H-approved only).
- **Guardrails STILL HARD (unchanged):** one listing per product, 3-layer dup
  guard, text+photo variation, honest condition (UK Pre-Owned/Tested Working vs
  For Parts), exact gold-list price, ≤3/day. Any of these fails → skip, don't force.
- **Any Meta signal** (flag, review, listing removal, lock, warning) → STOP all
  FB activity immediately, report to H, don't fight it.
- Re-raise the daily cap only after ~2 clean weeks of ≤3/day, and only on H's word.

## 6. What "preservation" means operationally (daily)
- Visual + title = truth: condition, included-in-box, price, pickup/delivery.
- **PHOTO SOURCE (two separate rules — do NOT conflate them):**
  1. **FB Marketplace LISTINGS → Jiji listing photos, always** (source-of-truth rule,
     unchanged). The FB poster uses local `photos/<jiji_id>.jpg` (from Jiji scrapes).
     NEVER fetch a brand stock image for an FB listing.
  2. **Sunday CONTENT/MARKETING stills (Status, groups, CTWA) → condition split (engine B4A):**
     NEW/boxed item → official manufacturer stock photo (Gorilla/Stanley/Black & Decker/diy.com;
     Akoma → Makeblock); USED/UK pre-owned → REAL photo of the actual unit. Never a clean stock
     shot standing in for a used item — that deception flag is what got the Marketplace reviewed.
- Verify stock physically present before listing (Dome vs Oyarifa handled by human).
- Sold → delete the FB listing same day (stale listings destroy trust).
- Prune/renew ONLY genuinely killed listings (FB auto-expires ~7 days; renew via
  `fb_check_renewals.py`, cap 5/run, 8s spacing) — never force-refresh actives.
- One price, three channels, every hour: if price changes, edit gold list FIRST
  then Jiji/catalog/FB together.

## 7. If a flag EVER returns
- STOP everything: pause crons, no new posts, no renewal churn, no photo edits.
- Reply honestly to any Meta prompt (ID/phone verify) — we have nothing to hide.
- Document what triggered it (which title/photo/pattern) — do NOT repeat it.
- This file + the canonical `FB_MARKETPLACE_PLAYBOOK.md` is the single source of
  the rules; any session acting on FB reads BOTH first. No exceptions.

## 8. Command of truth / no invention
- Never invent condition, provenance, price, or availability on FB.
- If asked a fact we don't hold (is it UK-new? tested?), the answer is the true
  unknown → route to H, or state honestly in the listing. Fabricating = the exact
  behaviour that got it flagged.
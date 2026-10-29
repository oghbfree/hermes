# FB Marketplace — Rejected Listings SOP

> Status: **ACTIVE** · Created 2026-10-28 · Owner: 2Real agent + H (for manual steps)
> Source: 28 Oct hard lesson (deletion automation blocked — see below).

## Rules (golden)
1. **NEVER delete-and-repost identical.** FB treats it as a duplicate/policy repeat violation → account restriction risk. Fix the cause (category, condition, title/description, photos) and relist fresh.
2. **Rejected ≠ invisible to you.** FB keeps rejected listings in inventory (Rejected/Inactive) until manually deleted. Buyers can't see them either way.

## Why automation can't delete them
Confirmed 28 Oct via CDP accessibility-tree scan: the "See options" control on a rejection card is rendered as **plain static text — no button/link/menu node in the DOM or accessibility tree**. Hermes cannot click it. Do not re-attempt automated deletion; mark these as `blocked — manual`.

## Manual workaround
- **Desktop:** facebook.com/marketplace/you/selling → filter Rejected (or Inactive) → open listing → ⋯ More options → Delete listing → confirm.
- **Phone (FB app):** Marketplace → You → Listings → rejected item → ⋯ → Delete listing.
- Alternative: **Mark as sold** if the record shouldn't be visible (keeps history) — Delete is cleaner for rejected items.

## Current rejected trio (status 28 Oct 2026)
| Listing | Status |
|---|---|
| Vtech Baby Walker — UK Imported, Quality Checked | blocked — manual delete |
| Medela Breast Pump From the Uk — UK Imported, Quality Checked | blocked — manual delete |
| Medela Swing Flex (not explicitly requested) | blocked — manual delete |

## Weekly triage (proposed, not yet scheduled)
Weekly Monday 08:00 cron: open selling dashboard, read every "Rejected / Needs attention" listing (id, title, reason), decide fix-and-relist vs leave vs manual-delete. **Pending H approval** (evening-reflect 28 Oct recommendation).

---
Related: [[INTEGRATED_INSIGHTS_2026-10-28]] · [[daily-sales-log]]

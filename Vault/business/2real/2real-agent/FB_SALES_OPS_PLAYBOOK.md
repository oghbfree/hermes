# FB Marketplace — Advanced Sales Ops Playbook (CANONICAL)

**Owner:** 2Real ops · **Created:** 14 Oct 26 · **CTA:** WhatsApp 0204252252
**Companion:** `FB_MARKETPLACE_PLAYBOOK.md` (base rules) · helper module: `channel_upload_package/fb_sales_ops.py`

This adds 5 sales capabilities to the FB Batch Poster cron. H-approval gates are explicit where business rules require.

---

## 1. FB-OPTIMISED LISTINGS
Every listing uses FB's algorithm-friendly shape:
- **Title:** `[Brand] [Product] [Key Spec] — [Category keyword], UK Imported, Quality Checked`
- **Description:** hook line → key specs (researched, ≤120 chars) → pickup/payment → CTA
- Helper: `fb_sales_ops.optimize_listing(title, details, specs, keywords)`.
- Rules: never change price, never invent specs, one listing per product.

## 2. BUYER MESSAGE HANDLING + NUDGE/REVIVE
Track every buyer conversation and revive the quiet ones.
- **Store:** `FB_BUYER_MESSAGES.json` (threads: listing, buyer, last msg/dir, nudges_sent, status).
- **Nudge policy:** first nudge after **24h** of buyer silence (when WE spoke last); second after **72h**; **max 2 nudges**, then mark `dead`.
- **Copy:** warm, no-pressure, **never offer a discount** (H approves discounts). Always ends with CTA 0204252252.
- Helper: `BuyerThreads().due_for_nudge()` → list, `nudge_text(t, n)`, `mark_nudged(id)`.
- **Automation:** the cron reads the FB Marketplace inbox in the `jiji-shop` session, replies to new
  messages (price/stock from Jiji truth), records the thread, and sends due nudges. If the inbox
  surface changes and can't be read, log the threads manually and continue.

## 3. SLOW-ITEM PRICE DROP (H-APPROVAL GATED)
Detect stale listings and **propose** a drop — never auto-apply (business rule: no discounts without H).
- **Store:** `FB_LISTING_PERFORMANCE.json` (views, chats, age, price_drops).
- **Policy:** slow after **14 days** unsold; propose **-10%**; never below **-30% total** from list.
- Helper: `PriceDrops().slow_candidates()` → proposals with `needs_H_approval: true`.
- **Flow:** cron lists candidates → delivers to H → only on H's "approved" does the price change
  (update Jiji FIRST, then FB — one price everywhere).

## 4. BUNDLE RECOMMENDATIONS
Cross-sell complementary items to raise basket size.
- **Store:** `FB_BUNDLES_AND_GROUPS.json` (bundle definitions + hints).
- Helper: `recommend_bundles(item_title)` → matching bundle(s) with a one-line pitch.
- **Use:** append a "Pairs well with…" line to the listing description, or a short reply in buyer chat.

## 5. GENERAL LISTING + CROSS-SELL INTO GROUPS
- **General listing:** `fb_sales_ops.general_listing(title, body)` — for services/announcements/wanted
  (non-product), always CTA-tagged.
- **Cross-sell groups:** `cross_sell_targets(category)` returns the best-fit FB groups for the item
  (policy cap **2 groups/run**; **new groups need H approval** before posting).
- **Store:** group list lives in `FB_BUNDLES_AND_GROUPS.json` under `fb_groups`.
- **Flow:** cron cross-posts the item (or the week's bundle) to 1-2 approved groups + the Marketplace listing.

---

## Approval gates (never bypass)
| Action | Gate |
|---|---|
| Price drop | **H approves** (business rule) |
| Posting to a NEW FB group | **H approves** |
| Any discount in a buyer message | **H approves** |
| Relisting an already-posted product | **H explicitly orders it** |

Everything else (optimised listings, buyer replies, nudges, bundle lines, general posts) runs autonomously.

## Files
- `FB_BUYER_MESSAGES.json` — buyer threads + nudge state
- `FB_LISTING_PERFORMANCE.json` — per-listing views/chats/age/drops
- `FB_BUNDLES_AND_GROUPS.json` — bundles + groups + policy
- `channel_upload_package/fb_sales_ops.py` — all helpers
- `FB_MARKETPLACE_PLAYBOOK.md` — base posting rules (unchanged)
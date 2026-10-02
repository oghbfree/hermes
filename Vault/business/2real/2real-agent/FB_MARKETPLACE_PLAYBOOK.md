# Facebook Marketplace Playbook — CANONICAL (all sessions MUST follow)
**File owner:** PROMOTION_MASTER_PLAN.md chain | **Updated:** 23 Sep
**Any session posting to FB Marketplace reads this file first. No exceptions.**

## Where This Fits
Christmas 3-engine plan: (1) Jiji TOP+ allocations, (2) Pro Sales groups, (3) FREE channels =
WhatsApp Status ×2 + **Facebook Marketplace (this file)**. FB = visual, high-ticket channel.

## THE RULES (non-negotiable)

### 1. Price = EXACTLY the gold price list
- Source of truth: `WA_CATALOG_PRICE_LIST.md` + `fb_marketplace_priority.json`
- **One price everywhere**: Jiji ad = WhatsApp catalog = FB listing. NEVER deviate
- If an item's price changes on the shelf, update the gold list FIRST, then Jiji/catalog/FB

### 2. Only post items from the priority queue, in score order
- Queue: `fb_marketplace_priority.json` (84 items, GHS 500+, stock confirmed, score-ordered)
- Do NOT invent items. If an item isn't in the queue but is on the shelf, add it to the
  queue (with price from inventory) before posting

### 3. Out-of-stock check
- Confirm the item is physically present (Dome or Oyarifa) before posting
- Sold items get deleted from FB same day — stale listings kill trust

### 4. Listing template (FB rewards detail + visual keywords)
- Title: `[Brand] [Product] [Key spec] — UK Imported, Quality Checked`
- Description: condition (new/open-box-tested), what's included, price, locations
  (Oyarifa pickup / Accra delivery), contact: **WhatsApp 0204252252** (never a
  Jiji link on FB), payment MoMo/cash
- Photos: 3 minimum — front, detail/sticker, any defect (honesty = fewer returns)

### 5. Volume + pacing
- FB flags accounts that mass-post: **max 10–15 listings/day per account**
- 84-item queue ≈ 6–8 days for full coverage
- The other session's 60-advert test: keep pacing at ≤15/day, spread over 4+ days

### 6. Repeat listings (Jiji keyword strategy) do NOT carry to FB
- FB is one listing per product (FB merges/suspects duplicates)
- Pick the better keyword variant per product, post once

## SESSION COORDINATION (multi-session sync)
- Before posting: READ `fb_marketplace_progress.json` — check which items are already done
- After each item posted: append `{"item", "price", "url", "date", "session"}` to
  `fb_marketplace_progress.json` (or log to `fb_progress.log` if JSON unsafe)
- Never re-post an item already in progress file
- Do NOT edit `WA_CATALOG_PRICE_LIST.md` or `christmas_top500_tiered.json` — report
  needed changes to the orchestrator session instead

## Measuring
- Weekly (Monday gap re-scan): count FB leads vs Jiji chats per item — FB winners
  get WhatsApp Status posts too
- Sold items: mark sold in progress file + delete listing

## SESSION BLOCKER (1 Oct 26)
Chrome auto-updated to v154 → remote debugging on the DEFAULT profile now needs a
manual "Allow remote debugging?" approval (user click). On a locked machine nothing
can accept it, so FB posting crons fail with "DevToolsActivePort not found".
Copying the profile to a temp dir restores debugging but loses the FB login
(app-bound cookie encryption). Fix: H unlocks PC, Chrome shows the Allow prompt
once → accept it → cron resumes. To re-enable silently, set Chrome policy
HKLM\SOFTWARE\Policies\Google\Chrome\DevToolsRemoteDebuggingAllowed=1 (needs admin).
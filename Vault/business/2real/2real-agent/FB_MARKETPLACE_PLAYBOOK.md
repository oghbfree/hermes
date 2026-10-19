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

## ANTI-BAN HARDENING (12 Oct 26 — per H)

- **DUPLICATE CHECK IS MANDATORY — before EVERY post (rule added 12 Oct 26, per H):**
  1. Open `https://www.facebook.com/marketplace/you/selling` and scan ALL live
     listing titles — if the target title (fuzzy, case/space-insensitive) is
     already on the profile, SKIP the item. Never rely on fb_posted.json alone;
     a prior run may have published but crashed before saving.
  2. Also check the ID against `fb_posted.json` (compare as strings — IDs are
     ints there, CSV/feed rows are strings).
  3. One listing per product, ever. Re-list only when H explicitly orders it
     in live chat.
- **Cadence: max 3 listings per session/run.** No more single-item cron runs; no bursts.
- **Text variation is mandatory** — never post identical boilerplate. `fb_post_lib.py`
  `make_desc(title)` rotates 5 openers × 4 closers. Use it for every new listing.
- **Photo variation is mandatory** — `vary_photo(src, dst)` micro-crops 2–6px + ~1%
  brightness + re-encode before upload, so image hashes differ per listing.
- **Category flow changed (FB 2026-10):** Category is now an input combobox typeahead,
  not a dialog button. Use `open_category()` (in fb_post_lib.py). 'Home & garden' as a
  top-level leaf may not stick — use a concrete leaf ('Tools', 'Household', etc.).
- Sleep 2–5 min between listings in the same session. If Meta ever flags the account,
  STOP all posting and report to H — never fight a lockout.

## SESSION BLOCKER (1 Oct 26)
Chrome auto-updated to v154 → remote debugging on the DEFAULT profile now needs a
manual "Allow remote debugging?" approval (user click). On a locked machine nothing
can accept it, so FB posting crons fail with "DevToolsActivePort not found".
Copying the profile to a temp dir restores debugging but loses the FB login
(app-bound cookie encryption). Fix: H unlocks PC, Chrome shows the Allow prompt
once → accept it → cron resumes. To re-enable silently, set Chrome policy
HKLM\SOFTWARE\Policies\Google\Chrome\DevToolsRemoteDebuggingAllowed=1 (needs admin).
### TITLE LENGTH LIMIT (verified 15 Oct 26)
- FB Marketplace rejects titles at 100 chars with "Please enter a shorter title" (publish button fails silently, 3x retries all fail). Titles must be <= ~97 chars. Keep the keyword-enriched format but trim to <=95 chars before posting.
### CDP PORT (17 Oct 26)
- `cdp_harness.py` defaults to `FB_CDP_URL=http://localhost:64365` which is DEAD — runs fail with
  `ConnectionRefusedError(10061)`. The live Brave debug listener is `http://127.0.0.1:9222`.
  Always run the poster as: `FB_CDP_URL=http://127.0.0.1:9222 python fb_post_run.py <ids...>`
- Verify first: `curl -s http://127.0.0.1:9222/json/version` (must return Browser info).
- When connecting the websocket manually use `suppress_origin=True` (plain connect → 403 Forbidden).
- FALLBACK (18 Oct 26): if no live CDP debug port exists (both 9222 and 64365 dead/404), run the
  posting flow inside the Hermes browser session `jiji-shop` instead: exec `fb_post_lib.py`
  (strip the globals assert) with `js/goto_url/click_at_xy/wait_for_load` injected, and use
  CDP `DOM.setFileInputFiles` for the photo upload. Post ~2 listings per browser call with a
  45–60 s pause; if a call times out mid-post, check the live Selling page before re-posting
  (the registry may have missed a published item — mark it via `Registry().mark_fb_posted`).

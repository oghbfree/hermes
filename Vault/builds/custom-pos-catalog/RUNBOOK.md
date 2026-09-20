# RUNBOOK: Custom Catalog + Storefront (Zobaze/Hybrid) — 2 Real

**Created:** 2026-09-20 **|** **Decision:** BUILD in-house (no off-the-shelf POS) — local-first web catalog tool, later MoMo storefront.
**Goal (one line):** A local, phone-friendly photo **catalog + owner system** for 2 Real's brand-new stock (moving into two spare home rooms), fed live counts to **Jiji / WhatsApp Business Catalog / Facebook Marketplace**, with a later **MoMo/delivery storefront** — replacing the login-walled Zobaze.

**Source session:** `20260910_044928_4ce205` (main hermes pin) — contains the full critical-planning conversation, bag scheme, and build order.

---

## Context (from LLM Wiki + source session)
- **Old data:** `Vault/business/2real/2real-agent/inventory_agent.json` — **1,049 SKUs / 2,348 units** (988 "Online" + Ingco Ingco/Wynca). Has price, cost, stock, barcode, in_stock. **This is the seed data.**
- **Physical reality (key constraint):** SECOND-HAND stock stays in Dome — **NOT in this system, NOT inventoried, NOT a POS.** Only **BRAND-NEW stock** (moving from warehouse → two spare home rooms) needs the POS/catalog. So the system tracks **new-stock only**, but the Jiji ad must stay live until sold-out, then close.
- **Jiji limit:** Jiji **does not tell you stock count** — the catalog must be the source of truth for "how many left," and must **signal when an ad should close** (stock = 0).
- **Why local-first (from session):** Zobaze's killer flaw is the **login wall (QR scan, no API)** — that's what blocks the responder, cron loops, and Drive sync from fresh stock. A **local SQLite DB on the same machine Hermes runs on** = zero walls: hooks, inquiry loop, Jiji report, P&L all read/write it directly — no scraping, no auth, no sync lag. An Android/web app rebuilds those walls.
- **Future (Phase 5):** once ALL items are on Jiji + WhatsApp Catalog + FB Marketplace → add a **momo / delivery storefront** (KwikMo | Zobaze hybrid), self-serve browse + Paystack MoMo checkout + delivery selection (Yango / pickup at Oyarifa), fed by the same catalog with live counts.
- **Locations:** Oyarifa home office (machine runs Hermes + this system). Dome = second-hand, out of scope.

## Scope boundaries (do NOT build)
- ❌ No second-hand/Dome stock in the system.
- ❌ No full POS (no till, no staff cashier roles) — it's a catalog + owner-inventory tool.
- ❌ No Android app (rebuilds the login wall). Local web app on the shop PC.
- ❌ No auto-scraping Jiji — the catalog feeds Jiji via generated drafts; stock is source-of-truth local.

## Build + Test principles
- **Phase = build + test** — each independently usable.
- **Stage by access control:** browse mode (public: photo+price only) vs owner mode (counts, bag codes, "mark sold"), gated by a simple PIN — test both separately.
- **Phone-friendly first** (staff/H at home use it on a phone).
- Time estimates unreliable — loose guidance only.

---

## PHASE 1 — BAG ALLOCATION SCHEME + PHYSICAL LABELS
**Goal:** The physical home-storage layout decided + printable labels (bags A/B, rooms).
**Steps (imperative):**
1. Create category→bag-code mapping (from source session): Room B stackable bags BAG-01..10 (paint 574, saws/cutters ~290, tapes/glue ~295, locks 130, drills/screwdrivers ~93, plumbing ~73, levels/hammers/wrenches ~130, power ~37, grinder-misc ~15, lights ~51) + Room A shelving A1.. (sockets/switches/cables, small high-value clear boxes).
2. Generate printable label sheets (bag code + category + max qty) as HTML→PDF for A4 print.
3. Produce a BAG_MAP.md in the repo/vault for reference.
**Test / done-criteria:**
- [ ] Every 1,049 SKU is assigned a bag/room code (no unassigned).
- [ ] Label PDFs print and match BAG_MAP.md.
**Coding agent:** Codex (visual labels) or Claude Code (data mapping). **Estimate:** half a day (mostly data).

## PHASE 2 — LOCAL SQLITE CATALOG CORE (foundation)
**Goal:** A local SQLite DB + a small Python data layer (no UI yet) that holds items, counts, bag codes, photos, sold/active status.
**Steps (imperative):**
1. Define schema: `items(id, sku, name, variant, category, price, cost, qty, bag_code, in_stock, active_ad, sold_qty, photo_path)`, `photos(id, item_id, path, primary)`, `sales(id, item_id, qty, ts, channel, ref)`.
2. **Seed:** migrate the 1,049 SKUs from `inventory_agent.json` into `items` (skip items already flagged second-hand/Dome).
3. Data functions: `list_items(filters)`, `get_item(sku)`, `update_qty(id, delta)` (auto toggles `in_stock`/`active_ad` at 0), `mark_sold(id, qty, channel, ref)`, `photo_add(item_id, path)`.
4. CLI smoke test (no UI): seed → count → mark sold → verify stock flips.
**Test / done-criteria:**
- [ ] Seed count == expected from inventory_agent.json (new-stock subset).
- [ ] `mark_sold` decrements qty and flips `active_ad` to false at 0.
- [ ] Round-trip: update + re-read returns correct values.
**Coding agent:** Claude Code / OpenCode (linear data code). **Estimate:** 1 day.

## PHASE 3 — PHOTO CATALOG WEB APP (browse + owner modes)
**Goal:** A local web app (Flask/FastAPI) served on the shop PC + LAN, phone-usable. Two modes.
**Steps (imperative):**
1. Browse mode (no PIN): grid of items → photo + price only (no cost/qty/bag). Search by keyword. This is the customer-facing catalog.
2. Owner mode (PIN-gated): full item view (counts, cost, bag code, photo), edit qty, **"mark sold"** (with channel + MoMo ref), add photo, assign/reassign bag code, mark ad closed/open.
3. Photo upload endpoint (phone camera → saves to `photos/`, links to item).
4. Radio on LAN (host `0.0.0.0`); note the local URL clearly for phone use.
**Test / done-criteria:**
- [ ] Browse mode renders photo+price for a seeded item, no cost/qty leak.
- [ ] Owner mode requires PIN; mark-sold decrements live; phone browser round-trips.
- [ ] Photo upload from phone attaches to the right item (verify round-trip).
**Coding agent:** Codex (web UI/images) + Claude Code (routes). **Estimate:** 2–3 days.

## PHASE 4 — CHANNEL PUSH: Jiji + WhatsApp Business Catalog + FB Marketplace
**Goal:** Generate posting material from the same item record — one item → Jiji draft + WhatsApp Catalog entry + FB Marketplace post.
**Steps (imperative):**
1. Item → ad-draft generator: title (variant+category), keyword-rich description (template), price, primary photo. Output as copy-paste-ready blocks.
2. WhatsApp Business Catalog: a catalog-entry manifest (name, description, price, photo, SKU) ready to import/paste.
3. FB Marketplace: post draft (photo + description + price).
4. **Stock→ad-close signal:** when `qty` hits 0, flag item `active_ad=false` and output a "CLOSE AD" notice (SKU + Jiji URL) so H closes the Jiji ad; never auto-close (Jiji needs human, per H).
**Test / done-criteria:**
- [ ] One item → 3 channel-ready outputs (Jiji/WA-Catalog/FB) sharing the photo.
- [ ] Sold-out item produces a "CLOSE AD" flag with the Jiji URL.
**Coding agent:** Claude Code (generators) + Codex (photo prep). **Estimate:** 1–2 days.

## PHASE 5 — MoMo / DELIVERY STOREFRONT (LATER — only once everything is listed)
**Goal:** Self-serve storefront: browse catalog → Paystack MoMo checkout → delivery choice (Yango / pickup Oyarifa). Fed by the SAME catalog with live counts.
**Steps (imperative):**
1. Public storefront pages (from catalog browse data).
2. Paystack MoMo payment flow (server-side init + webhook).
3. Delivery selection + order record (customer, items, qty, address, delivery-method).
4. Decrement stock on paid order (reuse PHASE-2 `mark_sold`).
**Test / done-criteria:**
- [ ] Test-mode order → Paystack sandbox payment → stock decrements → order recorded.
- [ ] Pickup vs Yango path both record correctly.
**Coding agent:** Codex (storefront UI) + Claude Code (Paystack/webhook). **Estimate:** 3–5 days. **GATE:** this phase does NOT start until PHASE 4 is live (all items listed).

---

## DONE = PHASES 1–5 complete, verified per done-criteria, running on the shop PC.
## Rollout: Phase 1–3 usable solo by H first; Phase 4 with John/photo-taker; Phase 5 public once listed.

*Repo suggestion: `/c/Users/User/AppData/Local/hermes/projects/2real-catalog/` (or Vault/builds/2real-catalog/). Runbook author: sat-nav + harold (runbook skill).*
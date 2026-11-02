# FB Marketplace — WEEK 1 RE-ENTRY BATCH (day 1) — FOR H APPROVAL
**Doctrine:** FB_PRESERVATION_PLAYBOOK.md | **Nothing publishes without H's go.**
**Corrected 01/11/26 by H:** all 3 items are NEW (boxed). Condition framing = Brand New
+ official manufacturer stock photos (per B4A photo-source rule). These are DRAFTS.

---

## Batch: 3 items, all BRAND NEW (boxed), ≤3/day (Week-1 cap)

### 1. Ring RTC2000 Rechargeable Handheld Tyre Inflator + Power Bank
- **Category:** Automotive tools
- **Gold price:** GHS 500 (queue + gold list agree ✓ — one price everywhere)
- **Jiji id:** 13427157
- **Stock:** 3 on hand (Dome)
- **Condition:** ✅ **BRAND NEW** (boxed) — H-confirmed 01/11/26
- **Title (~55 chars):** `Ring RTC2000 Tyre Inflator + Power Bank — Brand New`
- **Description draft:**
  > BRAND NEW, boxed. Ring RTC2000 rechargeable handheld tyre inflator with built-in power bank — USB output for your phone. Great for car, bike and off-road tyres. Sealed and untouched. Pickup at Dome (Accra) or delivery within Accra at a fee. Payment: MoMo or cash. Price: GHS 500. WhatsApp 0204252252 to confirm availability.
- **Photo source:** **Jiji listing photo** (source-of-truth rule, intact) — use the local `photos/<jiji_id>.jpg` for this item. NOT a fetched brand image on an FB listing. (Your rule: FB listings use Jiji photos.)

### 2. Luceco Slim Foldable Torch + Power Bank
- **Category:** Torches / lighting
- **Gold price:** GHS 500 (queue + gold list agree ✓)
- **Jiji id:** 13406906
- **Stock:** 3 on hand
- **Condition:** ✅ **BRAND NEW** (boxed) — H-confirmed 01/11/26
- **Title (~50 chars):** `Luceco Slim Foldable LED Torch + Power Bank — New`
- **Description draft:**
  > BRAND NEW, boxed. Luceco slim foldable LED torch with USB power-bank output — pocketable and bright. Ideal for home, workshop, camping or emergencies. Sealed and untouched. Pickup Dome (Accra) or Accra delivery at a fee. MoMo or cash. Price: GHS 500. WhatsApp 0204252252 to confirm stock.
- **Photo source:** **Jiji listing photo** (source-of-truth, intact) — local `photos/13406906.jpg` (verified present) for this item.

### 3. Ryobi Drill Battery Charger
- **Category:** Tools / chargers
- **Gold price:** GHS 750 (queue + gold list agree ✓)
- **Jiji id:** 16602816
- **Stock:** 1 on hand
- **Condition:** ✅ **BRAND NEW** (boxed) — H-confirmed 01/11/26
- **Title (~38 chars):** `Ryobi Drill Battery Charger — Brand New`
- **Description draft:**
  > BRAND NEW, boxed. Ryobi drill battery charger — sealed. Compatible with Ryobi One+ batteries. Pickup at Dome, Accra or Accra delivery at a fee. MoMo or cash. Price: GHS 750. WhatsApp 0204252252 to confirm availability.
- **Photo source:** **Jiji listing photo** (source-of-truth, intact) — use local Jiji photo for this item (guid A7H5AZFp34SKTN9aysyTW4m6). NOTE: verify the numeric jiji_id photo exists in `photos/`; if not present, pull from the Jiji listing before posting.

---

## Staging checks passed
- ✓ All 3 = gold-list price, one price everywhere (Jiji/catalog/FB consistent)
- ✓ ≤3/day (Week-1 cap)
- ✓ CONDITION = BRAND NEW for all 3 (H-corrected 01/11/26)
- ✓ Text = human-varied originals (not recycled boilerplate)
- ✓ Each includes WhatsApp 0204252252 CTA, pickup/delivery, payment terms

## Photo source (FB listing rule — Jiji photos, intact) — ALL VERIFIED 01/11/26
- FB Marketplace listings use JIJI listing photos (source-of-truth rule), NOT fetched
  brand images. Each uses its local `photos/<jiji_id>.jpg`.
- ✅ Luceco torch → `photos/13406906.jpg` — present, valid JPEG (24,039 B)
- ✅ Ring RTC2000 → `photos/13427157.jpg` — present, valid JPEG (15,574 B)
- ✅ Ryobi charger → `photos/16602816.jpg` — present, valid JPEG (41,223 B)
- (The brand-stock-photo rule applies ONLY to Sunday content/marketing stills, NOT FB listings.)

## Duck-check before posting (when H approves — do all)
1. Live scan `marketplace/you/selling` — confirm none already live (fuzzy title match).
2. `fb_posted.json` ID check (string compare).
3. Master registry `channel_posted_master.json`.
4. Apply `fb_post_lib.make_desc()` variation + `vary_photo()` at publish.
5. 2–5 min sleep between listings; 1 post per ~5 min. No bursts.

## Status
- [x] H confirms all 3 are NEW (boxed)
- [x] Jiji listing photos confirmed in `photos/` for all 3 (jiji_ids 13406906 / 13427157 / 16602816)
- [ ] H approves batch
- [ ] Live-scan dup check
- [ ] Publish (manual, H-adjacent)
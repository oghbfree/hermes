# DAD — Master Index & Consolidation
## Prof Robert Herbert-Blankson (Robert / "Dad"), age 92, UK

> **CANONICAL FOLDER:** `Vault/family/dad/` · **Telegram Topic:** **3823** (= Dad) · Chat `-1003784520976`
> This file is the single entry point for ALL dad content. Update this when adding/merging dad files.

---

## 1. Profile / Identity
| Field | Value |
|---|---|
| Full name | Prof Robert Herbert-Blankson |
| DOB | 09/05/1934 (age 92) |
| NHS No. | 464 825 5879 · KCH MRN 38495304 / Z052538 |
| Address | 40 Archdale Road, London SE22 9HJ |
| Phones | Home 020 8516 1117 · Mobile 07983 254695 |
| Wife (Next of Kin) | Lily Herbert-Blankson — 07855 929714 |
| Daughter | Jane — 07860 945810 · Son (H) — +233 20 425 2252 |
| GP | Dulwich Medical Centre, 020 8693 2727 |

---

## 2. Health & Clinical Care  (➜ HEALTH)
- **[MASTER] `health/FAMILY_INSIGHTS_DAD.md`** — structured care doc (conditions, meds, care package, contacts, escalation, finances). *Duplicate of `FAMILY_INSIGHTS_DAD.md` at folder root — keep `health/` as canonical.*
- **`health/CARE_LOG_DAD_2026-05.md`** — daily check-in care logs (May 2026).
- **Recent wellbeing/review docs** (fresh, from crons): `memories/family/dad/DAD_WELLBEING_*.md` & `DAD_WEEKLY_REVIEW_*.md` ~ **MOVE INTO `health/` on next consolidation**.
- **Key conditions:** T2 Diabetes, PVD, right BKA (2024) → transmetatarsal amp (2023), recurrent diabetic foot ulcer, bilateral hand OA, MGUS, hiatus hernia, gastric ulcer, macular hole, prostate removed (2003, PSA 8.7 in 2019), dilated blood vessel.
- **Cron jobs:** `checkin-dad` (f21f8326c44b) · `dad-health-weekly-review` (16c8a6f32eb5) · `Dad—3-Day Condition & Wellbeing Check` (5f6fafe0aba8).

---

## 3. Food & Diet  (➜ FOOD)
- **No dedicated dad food/diet master yet.** Food guidance currently lives inside the 3-day wellbeing check-ins (nutrition/hydration tips) and FAMILY_INSIGHTS_DAD (no formal diet section).
- **Action:** create `health/DAD_FOOD_MASTER.md` mirroring Mum's format (hydration, diabetes diet, wound-healing protein/VitC, DVT-safe eating).

---

## 4. Business / Affairs  (➜ AFFAIRS & BUSINESS)
- **`robertsville-hymnal-flyer.html`** + `.pdf` + social + `book_pages_enhanced/` (scanned hymn book, biography pg, life history) — **Dad's memoriam / Robertsville Hymnal** creative project (his life & compositions).
- **`archive/raw-data/Fam/Dad/Dad.md`** — personal/affairs: mega password, health notes (PSA, prostate).
- **`archive/raw-data/Fam/Dad/Dad taylors mark.md`** — tailor measurements (for clothing/affairs).
- **`archive/raw-data/Fam/Dad/dad & today.txt`** — Blue Badge needs letter + scattered business ideas (ema, tuition, laser engraver).
- **`archive/raw-data/Fam/Dad/Robertsville Hymnal Leaflet 2.docx`** + `Hymnal flyer.jpg` — hymnal leaflet source.
- Note: `building in ghana/.../Herbert Blankson.md` is a **power-of-attorney for H** (born 1974), not dad — keep in archive.

---

## 5. Check-ins & Communications
- **`dad-whatsapp-checkin-log.md`** — WhatsApp check-in attempts (mostly FAILED — bridge offline; recommends Telegram topic for check-ins).

---

## Consolidation Status & Next Steps
- ✅ Master index created here.
- ✅ Confirmed **Telegram Topic 3823 = Dad** (past session map) — but note: current cron dad jobs deliver to **topic 16**; verify which is live.
- ✅ **Done (2026-08-14):**
  1. Deleted duplicate root `FAMILY_INSIGHTS_DAD.md` (kept `health/`).
  2. Folded `memories/family/dad/*.md` → `health/` (wellbeing + weekly reviews); originals removed from `workspace/memories/`.
  3. Created `health/DAD_FOOD_MASTER.md`. **4.** Gathered business/affairs under `business-affairs/` (hymnal files + raw affair docs).
- ⏳ Optional: consolidate daily care log filename; verify topic 16 vs 3823 for cron delivery.

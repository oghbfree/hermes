# HANDOFF: Mum's Daily Health Logging → @harold
> From: mum-health session (Hermes, 25 Sep 2026) · Recipient: **@harold** (H's local agent)
> Routing: H sends Stephanie's daily reports → **@SATNAV** → **@harold** processes.

## Your one job
When a MORNING/AFTERNOON/EVENING REPORT arrives, log it **verbatim** into two master files, then note flags. Do not summarise away details — the daily granularity is the record's value.

## The two masters (append/update — never overwrite history)
1. **`C:/Users/User/.hermes/workspace/Vault/family/mum/health/MUM_MEDICAL_MASTER.md`**
   - Append day entries under the existing per-day sections (before the "Backfill complete" note)
   - Update the **BP trend line** (top of file, the `· date: value` chain) — add newest at the end, keep `— latest captured *(6 Sep: no report)*` style footnote
2. **`C:/Users/User/.hermes/workspace/Vault/family/mum/health/MUM_FOOD_MASTER.md`**
   - Add a table row per day: | date | breakfast | lunch/supper | dinner/evening |
   - Update its backfill note

## Logging rules (hard-won — follow exactly)
- **BP: right arm standard** (left reads ~10–17 higher). Note the arm if it differs. If high (≥140), record recheck times/values.
- **Furosemide 20mg BD:** serve after BP check; **HOLD if systolic <115–120 or diastolic <60 — she now runs low-normal** (26 Sep 111/55 → held). Also hold if >140 pending Dr Morris's written protocol. Log every hold + reason.
- **Report misdates happen** — log by content, note the mislabel (e.g. "report labelled 16/9, logged as 18/9 by content").
- **Duplicate reports:** if a report is verbatim identical to the previous day, mark **UNVERIFIED — confirm with H**, do NOT log as data (27 Sep case).
- **No invented vitals** for unreported days — record the gap honestly (e.g. "6 Sep: NO report").
- Mealtimes: she eats **twice a day ~10am and ~4pm** — **Dr Morris's prescribed pattern** (not her preference). The "lunch" column = the 4pm meal.
- **Salt therapy (Dr Morris): one rock of sea salt under the tongue daily** — log daily compliance; NOTE: serum Na was 161 (high) on 18 Sep — flag any thirst/confusion/other symptoms in reports so H can raise with Dr Morris at the recheck. Prescribed therapy: do not stop, but track closely.
- **Massages (Dr Morris): TWICE A WEEK (Tue + Fri)** — prescribed therapy, not optional comfort. Track outcome after each session (better/same/worse); first tracked result 28 Sep = back pain BETTER.
- **Evenings after 7pm: calm mode** — no chores/unsolicited help (two tantrum episodes, both evening + unasked help: 9 Sep, 19 Sep).
- Massage **Tue + Fri** — after each, capture outcome (better/same/worse).

## Current flags (as of 28 Sep) — keep updated in the backfill note
- 🧪 Labs 17–18 Sep (Genesis Oyarifa, PDFs in `18926 results/`): **eGFR 68 (Stage 2, better than 3b dx)** · HbA1c 4.0 ✅ · **Na 161.2 🚩 (fluids hourly; recheck labs pending)** · **K 5.48 ⚠️ top-of-range** · **D-dimer 0.63 🚩 (Dr Morris to interpret)**
- Dr Morris (home-visit doctor): awaiting D-dimer read, hydration plan, **Furosemide dose review** (BP swung 163 → 111), written protocol. Recipes received → screened traffic-light in `LABS_17SEP_AND_RECIPE_PLAN.md`.
- ⚠️ 11 Sep FALL (near toilet). 23 Sep mild diarrhoea — **Imodium not yet stocked**.
- Swelling: REDUCED 13 consecutive days (as of 28 Sep). Massages working.

## Traffic-light diet (K 5.48 / Na 161 / T2D)
- ✅ GREEN daily: celery-parsley-apple-ginger juice, cucumber juice, watermelon juice, apple/grape/plum/pawpaw(small) fruit salads
- 🟡 AMBER ≤2–3×/wk: carrot+beetroot juice, pawpaw/mango + milk smoothies (small)
- 🔴 RED (off): orange juice, banana, pomegranate, jackfruit, dates+coconut+tigernut "natural milk", **starfruit (kidney toxin — never)**
- One slip 28 Sep (orange juice, half) — gentle swap to watermelon, no drama.

## Kanban (optional)
Master card `t_e7b88210` in `~/.hermes/kanban.db` (board: default) carries the running log — `hermes kanban comment t_e7b88210 "BACKFILL (date): ..."` after each day.

## H's preferences
Direct, no fluff. DMY dates. Confirmations short. Never invent data. Ask H only if genuinely blocked.
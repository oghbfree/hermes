# 2Real Labeling System — Dome, Oyarifa & Walk-In

> Purpose: every physical item on the floor carries ONE label that tells the
> staff *what it is, where it lives, whether it works, and what to sell it for* —
> instantly, without asking. It connects the physical item to the digital record
> (item_location_ledger.py `location` field + Jiji jiji_id), so the floor and the
> listings never drift.
> Owner: H / Sammy (Dome), wife (Oyarifa — pick/pack). Updated 01/11/26.

---

## 1. The label — one code, six parts

```
[DOME|OYA] - [CAT] - [ZONE][BIN] - [NUM]
    1          2         3          4
```

| # | Part | What | Example |
|---|------|------|---------|
| 1 | **Site** | DOME = Dome walk-in shop · OYA = Oyarifa warehouse. Walk-in stock lives under DOME (it IS the Dome floor). | `DOME` |
| 2 | **Category** | short code (table below) | `ELEC` |
| 3 | **Zone+Bin** | Aisle letter + shelf/bin number. Matches `item_location_ledger.py --loc "B1"` | `A1` |
| 4 | **Sequence** | 3-digit item number within that bin | `007` |

**Full example:** `DOME-ELEC-A1-007`
→ "Dome walk-in, Electronics, Aisle A bin 1, item 7."
**Reading rule:** just call out `A1-007` and Sammy/wife know exactly which physical item you mean.

---

## 2. Category codes (keep short, one or two per item)

| Code | Category |
|------|----------|
| ELEC | Electronics & Audio (TVs, speakers, HiFi, radios) |
| PWR | Power tools & machinery (saws, drills, sanders) |
| HTL | Hand tools (spanners, pliers, sockets, screwdrivers) |
| GLUE | Gorilla / tapes / adhesives / spray paint |
| TOY | Toys & kids (LEGO, baby laptops, play sets) |
| SPORT | Tennis rackets, gym, camping, outdoor |
| HOME | Furniture, home, kitchen, smalls |
| LOCK | Locks, keysafes, safes |
| B2B | Office / business / IT (bought by businesses) |
| BULK | Bulk-to-wholesaler / clearance (Amazon bags, condemned) |
| MISC | Everything else |

---

## 3. Tested-status dot (colour code on the label)

Use a small coloured dot/sticker in the corner of the label. THIS is what stops
you overselling a broken item or hiding a good one:

- 🟢 **Green** = TESTED, WORKS → sell as "Tested Working"
- 🔴 **Red** = TESTED, BROKEN → sell as "For Parts / Repair" (honest)
- 🟡 **Yellow** = NOT YET TESTED → "as-is", or test before promising condition
- ⚪ **White** = N/A (no power needed — boxes, tools, new)

This maps 1-to-1 to `item_location_ledger.py` status → customer expectation line.

---

## 4. What goes ON the label (big print, pen/Sharpie)

```
DOME-ELEC-A1-007        ← code (top, big)
Mitre saw 210mm         ← item name (plain words, second line)
GHS 725                 ← asking price (or "LISTED" + Jiji price)
[coldot]                ← tested status dot
£17 cost                ← cost (small, for H / Sammy, bottom corner — don't show customer)
/Jiji 123456            ← jiji_id if posted (links to listing)
```

---

## 5. Zone map (keep a wall sheet at each site)

**Dome (walk-in shop) — aisles**
- A: Electronics & Audio (TVs, speakers, stereos)
- B: Power tools & machinery
- C: Hand tools
- D: Glue / tapes / spray
- E: Toys & kids
- F: Sports / camping
- G: Home & furniture
- H: Locks & safes
- BULK corner: wholesaler bags / condemned (📦 zone)

**Oyarifa (warehouse) — shelves/racks**
- Shelves numbered 1–N; each shelf split into bins A/B/C.
- Reserve a clear **"OYA-BULK"** corner for the bags-to-wholesaler + scooters/bikes (Thu).

Post an A4 zone map on the wall at each site so staff always know the aisle letter.

---

## 6. Daily rhythm (keeps labels honest)

- **On receipt / unpack:** assign code, write label, coldot 🟡 (untested), file under right zone. Add/update `item_location_ledger.py` with the `location`.
- **Saturday TV/speaker test day (today was one):** as each item passes, flip the dot 🟡→🟢 and set `--works yes` in the ledger. Broken → 🔴 / `--works no`.
- **When listed on Jiji:** write the jiji_id on the label + note "LISTED".
- **On sale:** remove label (or mark SOLD) → update ledger to SOLD.
- **On the floor the whole week:** staff can answer three questions from the label alone — *where*, *works?*, *price?* — no hunting.

---

## 7. Reusable label template (print on A5, cut, stick)

```
┌───────────────────────────────┐
│   DOME/OYA-[CAT]-[ZONE][BIN]-[NUM] │  big code
│   Item name: _________________ │
│   Price: GHS ______  (or LISTED)│
│   [●] cost £ ____  Jiji #_____ │
└───────────────────────────────┘
```

Keep an A4 sheet of blank templates + a marker pen + coloured dot stickers at both sites.
You can make 25 on one A5 sheet, guillotine/cut, stack near the till.

---

## 8. The 1-min staff cheat-sheet (pin at both sites)

```
READ A LABEL:  "A1-007" = aisle A bin 1, item 7.
GREEN dot  → sell as Tested Working
RED dot    → For Parts/Repair (be honest)
YELLOW     → not tested, sell as-is
CODE starts  → DOME = here, OYA = warehouse
SOLD?       → take label off + tell H to update ledger
```

---

## 9. Tie to digital (so the floor feeds the listings)

Labels ARE the physical mirror of `2real-agent/item_location_ledger.py`.
When you label, keep the ledger's `location` (e.g. `A1`) in sync so `python
item_location_ledger.py ls` always reflects the real floor. That ledger already
produces the customer-facing "expectation line" from the same status you put as
the dot — floor, ledger, and Jiji listing all agree.
---
title: Apiary Log — Kanzoni Bees
created: 2026-06-29
status: active
linked_workflow: FARM_WORKFLOW.md
---

# 🐝 Apiary Log — Kanzoni Shop + Farm Hives

**Location**: Kanzoni shop (Senya) + potential farm apiary expansion
**Manager**: Kanzoni (daily), Kwasi (training/technical)
**Cron**: Tuesday 7:00 AM check-in (`farm-apiary-check`)

---

## Hive Registry

| Hive ID | Location | Type | Status | Queen | Last Inspection | Notes |
|---------|----------|------|--------|-------|-----------------|-------|
| K-01 | Kanzoni shop | Langstroth | Active | Seen 2026-06-15 | 2026-06-15 | Strong, 8 frames brood |
| K-02 | Kanzoni shop | Top-bar | Active | Not seen | 2026-06-15 | Needs inspection |
| K-03 | Kanzoni shop | Langstroth | Weak | — | 2026-06-01 | Low stores, feed needed |
| F-01 | Farm (planned) | — | — | — | — | Site selected, not built |
| F-02 | Farm (planned) | — | — | — | — | — |

---

## Inspection Template (Per Hive)

```markdown
## {{date}} — Hive {{id}} Inspection

**Inspector**: {{Kanzoni / Kwasi / Ben}}
**Weather**: {{sunny / overcast / rainy}}
**Time**: {{HH:MM}}

### Observations
- **Entrance activity**: High / Medium / Low / None
- **Guard bees**: Yes / No
- **Pollen coming in**: Yes / No / Heavy / Light
- **Smoker used**: Yes / No

### Brood Chamber
- **Frames with brood**: {{count}} / {{total}}
- **Brood pattern**: Solid / Spotty / Drone-heavy
- **Queen seen**: Yes / No
- **Queen cells**: None / Supersedure / Swarm / Emergency
- **Drone brood**: {{count}} frames

### Honey Supers
- **Supers on**: {{count}}
- **Frames capped**: {{count}} / {{total}}
- **Ready to harvest**: {{kg estimate}}

### Pests / Diseases
- **Varroa**: None / Low / Medium / High (count per 100 bees)
- **Wax moth**: None / Larvae / Damage
- **Small hive beetle**: None / Adults / Larvae
- **Ants**: None / Trail / Invasion
- **Other**: 

### Actions Taken
- [ ] Added/removed super
- [ ] Fed syrup (1:1) — {{L}}
- [ ] Fed pollen patty
- [ ] Treated for varroa — {{method}}
- [ ] Removed queen cells
- [ ] Split hive
- [ ] Combined hives
- [ ] Replaced frames
- [ ] Other: {{detail}}

### Notes / Follow-up
{{free text}}
```

---

## Harvest Log

| Date | Hive | Method | Honey (kg) | Wax (kg) | Comb (kg) | Buyer | Price (GHS/kg) | Revenue (GHS) |
|------|------|--------|------------|----------|-----------|-------|----------------|---------------|
|      |      | Crush & strain / Extractor |            |          |           |       |                |               |

---

## Training Log (Kwasi + Kanzoni)

| Date | Topic | Trainer | Attendees | Duration | Materials | Next Session |
|------|-------|---------|-----------|----------|-----------|--------------|
|      | Hive inspection basics | Kwasi | Kanzoni, Ben | 3 hrs | Smoker, PPE, hive tool | 2 weeks |

---

## Kwasi Training Scope (When Funded)

### **Day 1 — Intensive (6 hours)**
| Module | Duration | Content | Practical |
|--------|----------|---------|-----------|
| 1. Bee biology & colony cycle | 45 min | Castes, seasons, communication | Observe hive entrance |
| 2. Hive inspection protocol | 60 min | Safety, smoker, tools, sequence | Full inspection K-01 |
| 3. Queen ID & assessment | 45 min | Find queen, brood pattern, cells | Mark queen (practice) |
| 4. Pest/Disease ID & IPM | 60 min | Varroa, wax moth, SHB, ants, AFB/EFB | Alcohol wash demo |
| 5. Honey harvest & hygiene | 60 min | Timing, extraction, filtering, jars | Harvest 1 super |
| 6. Record-keeping | 30 min | Hive log, harvest log, calendar | Fill template |
| 7. Splitting & queen rearing basics | 45 min | Walk-away split, grafting intro | Demo split |
| 8. Q&A + calendar planning | 30 min | Monthly tasks, Kwasi follow-up | Set dates |

### **Follow-up (Monthly, 2 hours)**
- Inspection of all hives together
- Review Kanzoni's solo inspections
- Address issues, plan next month

### **Budget**
| Item | Cost (GHS) |
|------|------------|
| Kwasi fee (Day 1) | 300–500 |
| Kwasi transport | 100–200 |
| Materials (smoker, PPE, tools, jars, labels) | 800–1,200 |
| Lunch/water for 6 people | 200 |
| Kwasi monthly retainer (3 months) | 900–1,500 |
| **Total Phase 1** | **2,300–3,600** |

---

## Equipment Inventory

| Item | Qty | Condition | Location | Notes |
|------|-----|-----------|----------|-------|
| Smoker | 1 | Good | Kanzoni | |
| Hive tool | 2 | Good | Kanzoni, Ben | |
| Bee suit | 2 | Good | Kanzoni, Ben | |
| Gloves | 4 pairs | Good | Kanzoni, Ben | |
| Veil | 2 | Good | Kanzoni, Ben | |
| Extractor (manual) | 0 | — | — | Need to acquire |
| Uncapping knife | 0 | — | — | Need |
| Strainer/sieve | 1 | Good | Kanzoni | |
| Buckets (food grade) | 4 | Good | Kanzoni | |
| Jars (500g) | 50 | New | Kanzoni | |
| Labels | 100 | New | Kanzoni | |

---

## Monthly Task Calendar

| Month | Task |
|-------|------|
| **Jan** | Feed check, varroa monitor, repair equipment |
| **Feb** | Spring build-up watch, add supers early |
| **Mar** | Swarm prevention, splits, queen rearing prep |
| **Apr** | Main flow — super management, harvest early |
| **May** | Harvest, extract, jar, label, sell |
| **Jun** | **Rainy** — feed if dearth, check drainage at apiary |
| **Jul** | Feed, pest check, prepare for minor flow |
| **Aug** | Minor flow — harvest, treat varroa post-harvest |
| **Sep** | Build winter stores, feed 2:1 syrup |
| **Oct** | Final harvest, consolidate, reduce entrance |
| **Nov** | **Dry starts** — water stations, shade, varroa treat |
| **Dec** | Monitor stores, emergency feed, plan next year |

---

## Financial Tracking (Link to `farm/finance/YYYY-MM.md`)

| Month | Honey Sales (kg) | Revenue (GHS) | Expenses (GHS) | Net (GHS) |
|-------|------------------|---------------|----------------|-----------|
|       |                  |               |                |           |

---

*Updated by cron `farm-apiary-check` (Tue 7 AM) and manual entries after inspections.*
# Akoma Robotics — Term-Time Course: Economics & Logistics Decision
**Date:** 17/08/26 · **Status:** Analysis complete, awaiting H's go/no-go

## The Question
Deliver a compulsory, embedded term-time practical course at **GH¢60–120/student**. Two logistics models:

1. **Mobile Lab** — taxi transports equipment every session
2. **On-Site Hub** — equipment stored at school permanently

---

## Cost Assumptions (Accra, 2026 market rates)

| Item | GH¢ | Basis |
|---|---|---|
| Facilitator per session (1 hr + prep + travel) | 150 | Realistic Accra rate; old file assumed 100/wk but that was pre-pivot |
| Taxi round-trip, one school (kits + box) | 60–100 | Normal saloon fits 6 kits + accessories; use 80 mid-point |
| Term length | 12 sessions | Royal Zion model |
| School commission (integrated model) | 10% | Net to Akoma = 90% of fees |
| Kit value at risk (on-site theft) | ~600–750/kit | mBot kit ~£80–100 |

---

## 1. The Financial Model

### Critical Answer First: NO — 15 students @ GH¢60 does NOT work in either model.

**Per-session budget @ 15 students × GH¢60:** GH¢900/term × 0.9 = GH¢810 net = **GH¢67.50/session**.
A facilitator alone costs ~GH¢150/session. The facilitator is the bottleneck, not the taxi.

### Break-Even Class Sizes (12-week term, 90% net, GH¢150 facilitator)

| Fee | Mobile Lab (taxi 80) | On-Site Hub (no taxi) |
|---|---|---|
| GH¢60 | **51 students** | **33 students** |
| GH¢80 | 38 students | 25 students |
| GH¢100 | 31 students | 20 students |
| GH¢120 | 26 students | 17 students |

### Sensitivity — the three levers that actually move this

| Lever | Effect on break-even @ GH¢60 |
|---|---|
| Taxi cost 80→40 (2 sessions per trip) | 51 → 42 students |
| Taxi cost 80→27 (3 sessions per trip) | 51 → 39 students |
| Facilitator 150→80 (trainee/volunteer) | 51 → 36 (taxi) / 18 (on-site) |

**The facilitator cost is ~2× the taxi cost.** Optimizing the taxi alone never fixes the model.

---

## 2. Operational & Logistical Risks

### Mobile Lab — hidden costs
- **Reliability:** a no-show taxi burns the entire session. In Accra rain/peak hours this is a real weekly risk. Mitigation: standing arrangement with one driver (prepaid monthly, ~GH¢1,000/term vs ~GH¢960 ad-hoc — roughly cost-neutral, far more reliable), plus a backup contact.
- **Pack-down time:** 15–20 min setup + pack-down in a 1-hr session = ~25–30% teaching time lost. Multiply across 12 weeks and you lose ~3 full sessions of learning.
- **Damage in transit:** kits bounce around in taxis; foam case mandatory (~GH¢100 one-off).

### On-Site Hub — hidden costs
- **Theft/liability:** 6–8 kits (~GH¢4,500–6,000 of equipment) sitting in a school. "Secure" in practice means: locked metal cabinet (~GH¢400–600 one-off), named custodian (deputy head or STEM teacher), signed equipment register, written liability clause in the partnership agreement (school liable for negligence, Akoma for defects). Without the clause, one theft wipes out the margin from an entire year across all schools.
- **Borrowing risk:** kits "lent" to other classes and returned broken/missing parts. The register + custodian solves this.
- **Cost if school charges rent:** even GH¢50/month storage = GH¢150/term adds ~2 students to break-even. Negotiate free storage as part of the school's 10% commission.

---

## 3. Pedagogy

- **Mobile Lab** loses 25–30% of contact time to setup/pack-down every session. Real-world setup is educational the first time, dead time the eleventh.
- **On-Site Hub** maximizes hands-on minutes — kits out in 5 minutes. For a 1-hour weekly slot, this is decisive. Also enables short lunchtime/after-school practice sessions that the taxi model physically cannot offer.

---

## 4. The Compulsion Factor

- Compulsory = guaranteed headcount = the revenue is fixed at term start. This makes **On-Site Hub's lower break-even directly bankable** — you know the number before buying anything.
- Missed sessions: on-site allows a simple catch-up (kit stays at school, facilitator runs one make-up slot or the class teacher supervises a repeat using the printed guide). Mobile-lab make-ups mean a second taxi trip — rarely viable.

---

## DECISION MATRIX (15 students projected)

| | **Mobile Lab** | **On-Site Hub** |
|---|---|---|
| **Cost/session @15 students** | Facilitator 150 + taxi 80 = GH¢230 vs GH¢67.50 revenue → **–GH¢162 deficit** | Facilitator 150 vs GH¢67.50 → **–GH¢82 deficit** |
| **Break-even students** | **51 @ GH¢60** (38 @ 80, 26 @ 120) | **33 @ GH¢60** (25 @ 80, 17 @ 120) |
| **Major risk** | Taxi no-show → lost session + reputation with school | Theft/damage of ~GH¢5k equipment; liability dispute |
| **Pedagogy** | 25–30% of time lost to setup/pack-down | Max hands-on time; enables extra practice slots |

---

## FINAL RECOMMENDATION

**On-Site Hub wins on every axis** — lower break-even, better pedagogy, more flexibility — **but neither model is viable at GH¢60 × 15 students.** The deficit is structural: the facilitator alone exceeds the entire session budget.

### Recommended package (choose based on school size):
1. **< 25 students:** fee must be **GH¢100–120**, AND use a **trainee facilitator (GH¢80–100)** — e.g., a STEM graduate/NYSC-type trainee who gets certification + reference. This is the single biggest cost lever.
2. **25–33 students @ GH¢60–80:** On-Site Hub with a standard facilitator is viable. Market the programme to schools by whole-year-group (e.g., all of Primary 5 = 30+ kids), not single classes.
3. **Either way:** negotiate free secure storage + signed liability clause. **Storage is non-negotiable; the school's commission is the flexible part** — trade commission down (10% → 5–15% range) to secure free storage, never drop the storage/liability clause itself.
4. **Multi-school routing:** if you keep any taxi element, batch 2–3 schools on one day/trip — this is what makes the Mobile Lab defensible if On-Site is refused.
5. **Commission is negotiable, not fixed:** open at 10%, accept 5–15% depending on what the school gives back (storage, custodian, headcount guarantee).

> **UPDATE 17/8/26 (H):** commission confirmed negotiable. Size-tier table now codified in the `akoma-robotics` umbrella skill and used for all future proposals.

### The hard truth
At GH¢60, you need **33 students per school minimum**. Royal Zion's whole-class model works; a single class of 15 never will. If a school can't guarantee 33+, the fee floor is **GH¢100–120** or the programme doesn't run.

---
*File: Vault/business/akoma/akoma-term-time-economics.md — linked from AKOMA_MASTER.md*

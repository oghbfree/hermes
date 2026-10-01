# Ghana Sourcing & Arbitrage Playbook — "Out-of-Stock Arbiter"
**Created:** 1 Oct 2026 | **Owner:** H | **Trigger:** customer requests item NOT in 2Real inventory

## The Opportunity
Customers ask for items 2Real doesn't stock. Every such request is an arbitrage
opportunity: source locally (Ghana supplier), sell to the customer at a margin.
Proven case: customer asked for a **5-ton lifting block** (2Real stocks 1-ton) —
the bot found a supplier **inside the chat**. That deal was missable; this channel
makes it systematic.

## The Loop

```
1. DISCOVER  — customer WhatsApp/Jiji request for item NOT in inventory_agent.json
2. LOG       — sourcing lead: item, qty, customer number, date → sourcing_log.json
3. REPLY     — bot sends ONE holding reply ("Let me check availability for you")
               (existing once-per-customer rules apply — no price invention)
4. SOURCE    — find Ghana supplier:
               a. Jiji Ghana search (other sellers of the exact item = suppliers)
               b. ghana_suppliers.md directory (known contacts by category)
               c. supplier catalogs folder (RIDA/PINENG/HUAFU etc. for industrial items)
5. COST      — get supplier cost price + availability + lead time
6. APPROVE   — H decides: arbitrage margin OK? (customer price − supplier cost
               must clear the +25–35% floor from the pricing framework)
7. QUOTE     — H-approved price to customer (one price everywhere rule applies
               only to OWN stock; arbitrage deals are priced per-deal)
8. CLOSE     — MoMo/cash only. Delivery honesty: state supplier lead time, never invent
9. PERSIST   — outcome logged; supplier added to ghana_suppliers.md on success
```

## Rules
- **H approves every arbitrage quote** — the bot never quotes supplier-sourced prices
- Margin floor: **supplier cost + 25–35%** (same discipline as UK sourcing pricing)
- No credit. MoMo or cash.
- If the SAME sourcing request appears 3+ times → it's a STOCKING signal, not a
  one-off arbitrage: flag to H to add the item to the next China/UK order instead
- Repeat customers (review pipeline) get first call when sourced items land

## Capture Points
1. **Automatic:** hourly Customer Inquiry Loop cron scans customer-interactions.md
   for unknown-item requests → builds SOURCING OPPORTUNITIES section in the
   Daily Jiji Report (item, customer, frequency, repeat count)
2. **Manual:** forward any request (call/Jiji chat/voice note) to the agent —
   logged same way
3. **In-chat discovery:** when the bot/customer conversation mentions another
   seller or supplier, H forwards the contact → added to ghana_suppliers.md

## Files
- `sourcing_log.json` — the ledger (item, qty, customer, supplier, cost, price, outcome)
- `ghana_suppliers.md` — the supplier directory (this folder)
- Daily Jiji Report — SOURCING OPPORTUNITIES section (auto)
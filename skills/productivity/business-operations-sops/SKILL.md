---
name: business-operations-sops
description: Standard Operating Procedures for H's business ventures — 2 Real Enterprises (sales, cash reconciliation, inventory, listings), Akoma Robotics (school outreach, class delivery), Construction Projects, Farm Operations (Senya), Property Management (London), Staff Management, and cross-cutting operations (incident reporting, weekly reviews). Triggered when H asks to create, review, update, or enforce SOPs; when staff actions need a reference procedure; or when a business process is being defined for the first time.
version: 2.0.0
author: hermes-agent
triggers:
  - User asks to create, review, or update an SOP
  - User mentions "procedure", "process", "how should staff handle"
  - User asks about sales process, cash handling, inventory, pricing, or quoting
  - User asks about school outreach, class delivery, or enrollment (Akoma)
  - Staff action needs a documented procedure to reference
platforms: [windows]
---

# Business Operations SOPs

## Purpose

This skill contains and maintains all Standard Operating Procedures for H's business ventures. It is the authoritative reference for how operations should run across all businesses and locations.

**Key principle:** SOPs are living documents. When H corrects a process or a gap is found, update the relevant SOP immediately.

## SOP Drafting Workflow

When creating or updating SOPs:

1. **Draft** based on known information
2. **Present to H** for review — H will correct details (expect 2-3 revision rounds)
3. **Finalize** only after H confirms accuracy
4. **Save** to `references/` as a standalone document
5. **Brief staff** on changes if needed (H decides who and how)

**Do NOT present first-pass SOPs as final.** H's businesses have nuanced processes that differ from assumptions. Always iterate.

## SOP Audit & Creation Workflow

When asked to create or audit SOPs across ventures:

1. **Inventory existing SOPs** — Load the skill, check `references/` for what exists
2. **Identify gaps** — Map known business areas against existing SOPs; flag missing ones
3. **Prioritize** — Complete pending SOPs first, then create new ones for uncovered ventures
4. **Draft in batches** — Group related SOPs (e.g., all Akoma, all cross-cutting) for efficiency
5. **Use consistent structure** — Every SOP follows: Scope → Process Steps → Roles → Pitfalls
6. **Update master index** — After creating SOPs, update the Active SOPs table and `all-ventures-sop-master.md`
7. **Cross-reference** — Link related skills (e.g., content pipeline ↔ listing SOP, elder care ↔ staff management)
8. **Present for review** — H will correct details; expect 2-3 revision rounds on first drafts

**SOP structure template:**
```
# SOP: [Name] — [Venture]
**Version:** 1.0 | **Date:** YYYY-MM-DD | **Approved by:** H
## Scope
## Process (numbered steps)
## Roles (who does what)
## Rules / Decision Framework
## Pitfalls
```

## Active SOPs

### 2 Real Enterprises

| SOP | Status | Reference |
|-----|--------|-----------|
| Sales & Order Processing | ✅ Final | `references/2real-sales-order-processing.md` |
| Cash Reconciliation | ✅ Final | `references/2real-cash-reconciliation.md` |
| Inventory Management | ✅ Final | `references/2real-inventory-management.md` |
| Content & Listing Procedures | ✅ Final | `references/2real-content-listing.md` |
| GRA Tax Filing | ✅ Final | `references/2real-gra-tax-filing.md` |
| Returns & Defects | ✅ Final | `references/2real-returns-defects.md` |
| Pricing Authority & Discount Guide | ✅ Final | `references/2real-pricing-authority.md` |
| Jiji/FB Listing Workflow | ✅ Final | `references/2real-jiji-fb-listing-workflow.md` |
| **Compiled Reference** | ✅ Final | `references/2real-sop-compiled.md` |
| Jiji Ghana Scraping & Market Intel | 📝 Research | `references/jiji-ghana-scraping-notes.md` |

### Akoma Robotics

| SOP | Status | Reference |
|-----|--------|-----------|
| School Outreach Pipeline | ✅ Final | `references/akoma-school-outreach.md` |
| Class Delivery | ✅ Final | `references/akoma-class-delivery.md` |
| Equipment Lifecycle | ✅ Final | `references/akoma-equipment-lifecycle.md` |
| Enrollment & Payment | ✅ Final | `references/akoma-enrollment-payment.md` |

### Construction Projects

| SOP | Status | Reference |
|-----|--------|-----------|
| Site Management | ✅ Final | `references/construction-site-management.md` |

### Farm Operations — Senya

| SOP | Status | Reference |
|-----|--------|-----------|
| Farm Operations | ✅ Final | `references/farm-operations-senya.md` |

### Property Management — London

| SOP | Status | Reference |
|-----|--------|-----------|
| Property Management | ✅ Final | `references/property-management-london.md` |

### Staff Management

| SOP | Status | Reference |
|-----|--------|-----------|
| Hiring, Onboarding, Performance & Communication | ✅ Final | `references/staff-management.md` |

### Cross-Cutting

| SOP | Status | Reference |
|-----|--------|-----------|
| Incident Reporting | ✅ Final | `references/incident-reporting.md` |
| Weekly Review Rhythm | ✅ Final | `references/weekly-review-rhythm.md` |

### Master Reference

| Document | Reference |
|----------|-----------|
| All Ventures SOP Master | `references/all-ventures-sop-master.md` |

## Key Business Facts (2 Real)

- **Zobase** (spelled with Z, not S) is the POS/inventory system
- **H enters inventory/stock amounts** into Zobase — not sales
- **Staff enter their own sales** into Zobase (John/Madam at Oyarifa, Sammy at Kantamanto)
- **H reviews** Zobase inputs and handles **discounts** (staff have no discount authority)
- **All payments are MoMo or cash** — no credit, no float
- **All prices come from Zobase POS** — Jiji, WhatsApp, Facebook, Kantamanto walk-in
- **Oyarifa off-Zobase is the ONLY pricing exception** — item photo goes to H, H sets price (cost + shipping + margin)
- **Kantamanto is on-Zobase only** — if not on Zobase, Sammy does not sell
- **John creates all adverts** — Jiji listings, WhatsApp posts, Facebook posts
- **Out-of-stock quotes:** 24-hour turnaround, John sources 3 comparables (UK eBay, direct company, competitive third party), posts in dedicated WhatsApp group, H sets final price

## Key Business Facts (Akoma)

- Target: schools first (administrators/principals), then parents
- Program: mBot robotics, ages 7-14, 10-week courses
- Price: 1,000 GHS per student
- John handles school outreach and demo sessions

## Staff Roles Summary

| Person | Role | Location | Key Responsibilities |
|--------|------|----------|---------------------|
| **H** | Owner | London / Ghana | Inventory entry (Zobase), pricing approval, discounts, off-Zobase quotes, review |
| **Madam (Ebony)** | Co-manager | Oyarifa | Sales (all channels), Zobase entry, customer service |
| **John** | Operations / Marketing | Oyarifa | Sales (all channels), Zobase entry, all adverts/listings, out-of-stock sourcing |
| **Sammy** | Sales | Kantamanto | Walk-in sales (on-Zobase only), Zobase entry, cash/MoMo reconciliation |
| **Matthias** | Site Supervisor | New Amanful / Borkro | Land/site visits, ground operations |
| **Ben** | Farm Manager | Senya Beraku | Coconuts, plantain, irrigation |
| **Kanzoni** | Farm Contact | — | Farm visits, wellbeing |

## Pitfalls

1. **Don't assume process** — H's operations have specific nuances. When in doubt, ask before drafting.
2. **Zobase spelling** — always "Zobase" with Z. Older content may say "Zobaze" but the correct spelling is Zobase.
3. **Don't give staff discount authority** in SOPs — only H approves discounts.
4. **Kantamanto boundary** — Sammy only sells items on Zobase POS. If it's not in Zobase, he doesn't sell it.
5. **Oyarifa off-Zobase** — the only exception to Zobase pricing. Photo to H first, always.
6. **SOPs are for reference, not automation** — staff may not follow them perfectly. H enforces, not the system.
7. **Who enters what** — H enters inventory/stock. Staff enter their own sales. H reviews. Don't mix these up.
8. **No float** — all sales are MoMo or cash. Everything sent to H daily. There is no float system.
9. **Content procedures are John's domain** — all adverts, listings, posts across all platforms are created by John. H provides direction and pricing.
10. **Telegram topic posting** — Use format `telegram:Agent Hermes / topic NNN` (with spaces around slash). The format `telegram:Agent Hermes:NNN` does NOT work. Always verify with `send_message(action='list')` first if unsure.
12. **SOP consolidation** — When multiple SOPs are created for one business, always create a compiled summary (`SOP_COMPILED.md`) in addition to individual files. Post the compiled version to the relevant Telegram topic for easy reference.
13. **Jiji Ghana Cloudflare blocking** — Jiji.com.gh is fully behind Cloudflare. Simple HTTP requests (curl, cloudscraper, python requests) all fail with 403. Only browser-based scraping works (Puppeteer/Playwright via Apify, or services like ScrapingBee). See `references/jiji-ghana-scraping-notes.md` for full research and options.
14. **Firecrawl key truncated** — The Firecrawl API key stored in config is truncated (`fc-3a3...52e6`). It cannot be used for direct scraping. Use Tavily for search, or fix the key in `~/.hermes/.env` and `~/.hermes/config.yaml` if the full key becomes available.
12. **AGENTS.md topic table** — When adding a new Telegram topic, update both the topic table AND the trigger list in the routing section. Use single-pipe `|` table format, not double-pipe `||`.

## File Structure

```
business-operations-sops/
├── SKILL.md (this file)
└── references/
    ├── 2real-sales-order-processing.md
    ├── 2real-cash-reconciliation.md
    ├── 2real-inventory-management.md
    ├── 2real-content-listing.md
    ├── 2real-gra-tax-filing.md
    ├── 2real-sop-compiled.md ← quick-reference summary of all 2 Real SOPs
    ├── 2real-returns-defects.md
    ├── 2real-pricing-authority.md
    ├── 2real-jiji-fb-listing-workflow.md
    ├── akoma-school-outreach.md
    ├── akoma-class-delivery.md
    ├── akoma-equipment-lifecycle.md
    ├── akoma-enrollment-payment.md
    ├── construction-site-management.md
    ├── farm-operations-senya.md
    ├── property-management-london.md
    ├── staff-management.md
    ├── incident-reporting.md
    ├── weekly-review-rhythm.md
    ├── all-ventures-sop-master.md ← master reference across all ventures
    └── jiji-ghana-scraping-notes.md
```

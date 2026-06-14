---
name: business-content-pipeline
description: Unified weekly content production pipeline for Akoma Robotics and 2Real Enterprises — merged alternating calendar, multi-platform production (IG, Facebook, TikTok, WhatsApp, Marketplace), image generation via ComfyUI, and delivery to John.
version: 1.0.0
author: hermes-agent
triggers:
  - User asks to plan, generate, or produce content for either or both businesses.
  - User mentions "content calendar", "social media plan", "content for the week".
  - User says "create content" or "generate posts" for Akoma or 2Real.
  - Sunday content engine cron job runs (generates full week plan).
platforms: [windows]
prerequisites:
  skills:
    - brand-assets (centralized brand reference — Akoma, 2Real, Taiwah)
    - comfyui (for image generation; must be installed and running)
  files:
    - references/akoma-brand-director.md (brand voice, audience, content types)
    - references/tworeal-brand-director.md (brand voice, audience, content types)
    - digital-presence-calendar.md (if migrating from old setup; legacy reference)
  cron_jobs:
    - sunday-content-engine (single job replacing old thu-akoma + fri-2real)
---

# Business Content Pipeline

## Overview

Single unified content system for **Akoma Robotics** (STEM education) and **2 Real Enterprises** (hardware/tools). Produces ready-to-post content for 6 platforms on an alternating daily schedule, delivered to Telegram topic 26 for review, then forwarded to John for posting.

## Merged Weekly Schedule

| Day | Brand | Content Focus | Platforms |
|-----|-------|--------------|-----------|
| **Monday** | 🤖 Akoma Robotics | Educational content — STEM value, coding benefits, infographics | IG Feed + Reel, FB Post, TikTok, WA Status |
| **Tuesday** | 🔧 2 Real Enterprises | Product showcase / New arrivals — catalogue shots, specs | IG Feed, FB Post, FB Marketplace, WA Status |
| **Wednesday** | 🤖 Akoma Robotics | Social proof — testimonials, student projects, instructor profiles | IG Feed + Reel, FB Post, TikTok, WA Status |
| **Thursday** | 🔧 2 Real Enterprises | Tips & how-to / Behind-the-scenes — tool guides, unboxing | IG Feed, FB Post, TikTok, WA Status |
| **Friday** | 🤖 Akoma Robotics | Engagement — polls, Q&A, fun content, workshop moments | IG Reel, FB Post, TikTok, WA Status |
| **Saturday** | 🔧 2 Real Enterprises | Deals / Taiwah influencer / Flash sales — urgency, price-first | All platforms + FB Marketplace + WA Broadcast |
| **Sunday** | 📢 Distribution | WhatsApp broadcasts, repurpose best content, weekly roundup | WA Broadcast lists, WA Status, FB Groups |

## Platform Matrix

| Platform | Akoma Posts | 2Real Posts | Content Type |
|----------|-------------|-------------|--------------|
| **Instagram Feed** | 2x/week (Mon, Wed) | 2x/week (Tue, Thu) | Single image + caption with CTA |
| **Instagram Reels** | 2x/week (Mon, Fri) | 1x/week (Sat) | Short video or image slideshow with trending audio |
| **Facebook Post** | 3x/week (Mon, Wed, Fri) | 3x/week (Tue, Thu, Sat) | Long-form caption + image, pinned to page |
| **Facebook Marketplace** | — | As stock allows (Tue/Sat) | Product listing with photos, specs, price, location |
| **TikTok** | 2x/week (Mon, Wed) | 2x/week (Thu, Sat) | Short-form vertical video ideas or slideshow scripts |
| **WhatsApp Status** | Daily (Mon, Wed, Fri) | Daily (Tue, Thu, Sat) | Quick 1-2 line punchy update with image |
| **WhatsApp Broadcast** | Weekly (Sun) — roundup | Weekly (Sun) — deals blast | Multi-message broadcast to customer lists |

## Production Pipeline

### Step 1: Generate Weekly Plan (Sunday Content Engine)
Single cron job (replaces old `thursday-content-akoma` + `friday-content-2real`).

**Inputs to gather before generating:**
- Current 2Real stock levels (identify high-stock items to push)
- Akoma enrollment status, upcoming workshops, events
- Any seasonal/calendar context (school term, holidays, rainy season)
- Past week's performance data (what got engagement)

**Output: Full week plan posted to Telegram topic 26:**
- 6 branded days (Mon–Sat) + Sunday distribution plan
- Per day: content type, platform, caption draft, image prompt, schedule notes

### Step 2: Write Captions
I write platform-specific copy per brand using the brand director references:
- **Akoma:** Warm, educational, aspirational, Ghanaian-proud. Address parent pain points.
- **2Real:** Direct, confident, value-focused, action-oriented. Every post drives WhatsApp enquiry.

### Step 3: Generate Images (via ComfyUI)

Use the `comfyui` skill for image generation. Two main branches:

**Product shots (2Real):**
- Clean product photography on white/grey backdrop
- Professional catalogue look
- Taiwah influencer shots on Saturdays (full character anchor)

**Educational/Engagement visuals (Akoma):**
- Infographic-style educational graphics with branding
- Student workshop scenes (diverse Ghanaian children, bright classroom)
- Fun/poll graphics for Friday engagement

**Taiwah Character Anchor** (for 2Real Saturday influencer content):
- 30-year-old Ghanaian woman, rich brown skin, oval face, high cheekbones
- Short textured black afro with plain headband, gold hoop earrings
- Athletic-feminine build, demonstrates/holds products
- Professional advertising quality, aspirational setting

### Step 4: Package for John
Organize into day-specific folders:

```
content/
├── monday-akoma/
│   ├── caption-ig.txt         # IG caption
│   ├── caption-fb.txt         # FB caption
│   ├── caption-tiktok.txt     # TikTok script
│   ├── status.txt             # WhatsApp Status text
│   ├── image-01.png           # Primary image
│   └── image-02.png           # Secondary image (if needed)
├── tuesday-2real/
│   ...
├── sent-log.md               # Tracks what was actually delivered to John
└── last-week-performance.md   # Stats for Saturday performance review
```

### Step 5: Deliver for Review
- Post full plan + images to Telegram topic 26 (content-calendar)
- H reviews, approves, or requests tweaks
- Once approved, forward to John via WhatsApp for posting

### Step 6: Track Performance
Weekly performance review job (`saturday-content-performance`):
- Compare planned vs posted
- Engagement metrics (likes, comments, shares, views)
- Conversion signals (WhatsApp enquiries from content)
- Feed into next week's plan

**First-Run / No-Data Protocol:** If no content has been produced or posted during the review period (expected for the first 1-2 weeks after pipeline setup), the performance report MUST:
1. State clearly that this is a baseline/first review with zero data
2. Document system status (cron jobs, Comfy Cloud, WhatsApp bridge)
3. List all blockers preventing content production
4. Provide historical context from OpenClaw era (last content sent, last plan generated)
5. Include the planned content calendar for the upcoming week
6. Save report to `~/.hermes/content-output/CONTENT_PERFORMANCE_[YYYY-MM-DD].md`
7. Format the Telegram post as a structured table: Brand | Platform | Post type | Performance notes | What worked | What didn't

**Zero-Data Report Template:**
```
📊 CONTENT PERFORMANCE REVIEW — Week of [DATE RANGE]

⚠️ BASELINE REVIEW — No content produced this period

[Brand tables with 🔴 No data per platform]

BLOCKERS:
1. [Blocker + impact]
2. [...]

NEXT WEEK: [Calendar summary]

Full report: CONTENT_PERFORMANCE_[DATE].md
Next review: [Date]
```

## Stock-Based Content Rules (2Real Enterprises)

| Condition | Action |
|-----------|--------|
| Stock HIGH | Push product showcase posts, Taiwah shots (Tue/Sat) |
| Stock LOW | Focus how-to/tips content (Thu), reduce CTAs |
| New shipment | Behind-the-scenes unboxing (Thu or Sat) |
| Clearance needed | Flash deals Saturday, urgency messaging |
| 🔴 **Golden Rule** | NEVER promote products with <2 units in stock |

## Cron Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| `sunday-content-engine` | 20:00 Sunday | Generate full week plan (replaces old thu-akoma + fri-2real) |
| `saturday-content-performance` | 09:11 Saturday | Weekly performance review |

**To set up the Sunday job:**
1. Delete old `thursday-content-akoma` and `friday-content-2real` cron jobs
2. Create new `sunday-content-engine` cron job with this skill as its content direction
3. Update Telegram topic 26 config to reflect merged calendar

## Related SOPs

- **First Performance Review Baseline** (`references/first-review-baseline-2026-05-16.md`) — Documents the system state, blockers, and cron job IDs at the time of the first-ever performance review (May 16, 2026). Useful for understanding the zero-data baseline and historical context.
- **Jiji/FB Listing Workflow** (`business-operations-sops/references/2real-jiji-fb-listing-workflow.md`) — Detailed step-by-step listing creation, quality standards, and listing tracker. John follows this for every Jiji and Facebook Marketplace listing.
- **Content & Listing Procedures** (`business-operations-sops/references/2real-content-listing.md`) — Platform-specific posting procedures (Instagram, TikTok, WhatsApp, Facebook).
- **Pricing Authority & Discount Guide** (`business-operations-sops/references/2real-pricing-authority.md`) — Who can set prices, discount rules, staff scripts.

## Pitfalls

1. **Don't overwrite the old cron jobs** until the new Sunday one is verified working — keep fallback.
2. **Gemini Gems are legacy** — the old `gem-akoma-content-director.md` and `gem-2real-content-director.md` were for OpenClaw's Gemini pipeline. Use the reference files in this skill instead.
3. **ComfyUI must be running** before image generation — verify with `health_check.py` first.
4. **WhatsApp bridge state** — if WhatsApp is down, content delivery to John falls back to Telegram DM.
5. **John can only action what's simple** — keep instructions per post to 1-2 lines max. Don't overcomplicate.
6. **TikTok scripts** are text-only — John would need to shoot/assemble the video. Include a clear 15-30 second script.
7. **Facebook Marketplace listings** need separate product photos (not the same as social posts). Generate specific white-background product shots.
8. **Comfy Cloud subscription required** — Free tier can browse models but returns 429
   PAYMENT_REQUIRED when generating images. Must have active paid subscription
   (Standard ~$10/mo minimum) before the Sunday Content Engine can produce images.
9. **Comfy Cloud model naming** — Cloud uses different paths than local ComfyUI.
   Flux Dev uses `flux1-dev-fp8.safetensors` in `checkpoints/` (not `unet/`),
   text encoders in `text_encoders/` (not `clip/`). See comfyui skill's
   `references/cloud-models.md` for full mapping. Always verify with
   `/api/experiment/models/*` before building workflows.
10. **First performance review will have zero data** — The Saturday content
    performance review will fire before any content has been produced. This is
    expected. Use the First-Run / No-Data Protocol (Step 6) to document system
    status, blockers, and upcoming calendar instead of engagement metrics.

## Verification

Before calling the plan done, run the brand-assets cross-check:

### ⚡ Brand Cross-Check (from brand-assets SKILL.md — MANDATORY)
For EVERY piece of content output:
- [ ] Phone numbers match brand-assets master: +233 20 425 2252 (2Real only)
- [ ] No phone number in Akoma CTAs (uses "Message us on WhatsApp to learn more" only)
- [ ] Logo descriptions match brand-assets master EXACTLY
- [ ] Brand colors are correct hex codes from brand-assets master
- [ ] Taglines/headlines match brand-assets master
- [ ] CTA templates match brand-assets master
- [ ] Hashtags are from the locked sets in brand-assets master
- [ ] Akoma content uses purple #6A0DAD + gold #FFD700 (NOT website template colors)
- [ ] 2Real content uses green #4CAF50 + yellow #FFC107

IF ANY mismatch → DELETE output and REWRITE from scratch. Do NOT patch in place.

### Standard Checks
- [ ] All 6 days assigned to correct brand
- [ ] All platforms covered per brand
- [ ] Stock rules respected (no <2 unit items promoted)
- [ ] Image prompts use correct brand director references
- [ ] Captions match brand voice per reference files
- [ ] WhatsApp Broadcast text is separate from Status text
- [ ] Cron job created/enabled, old jobs deleted
- [ ] Topic 26 prompt updated to reflect merged calendar
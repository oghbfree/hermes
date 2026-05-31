# Content Performance Review — Reference

## Purpose

The Saturday Content Performance cron job reviews the past week's content pipeline: what was planned, what was generated, what was posted, and what performance data exists. This file defines the review workflow and report structure.

## Workflow

### Step 1: Read the Sent Log

Read `content-output/sent-log.md` to get the high-level summary:
- Week identifiers and date ranges
- Total assets planned (images, captions, scripts, videos)
- Brands and platforms covered
- Generation status (which tools succeeded/failed)
- Performance tracking checkboxes (all unchecked = no data)

### Step 2: Inventory Content Directories

List `content-output/week-YYYY-MM-DD/` directories for the current and previous week.

For each week directory, enumerate:
- Subdirectories per day (monday-akoma, tuesday-2real, etc.)
- Files per platform subdirectory (instagram/, facebook/, tiktok/, whatsapp-status/, linkedin/, manim/, hyperframes/, marketplace/, whatsapp-broadcast/)
- File types present (.txt, .png, .mp4, .html, .py, .md)
- File sizes for video files (to verify renders completed vs. placeholder/partial)

### Step 3: Check for Performance Data

Search for any performance-related files:
- `*-performance*.md`
- `*analytics*`, `*metrics*`, `*engagement*`, `*report*`
- Platform-specific insight exports (not yet implemented)
- Posted logs or confirmations

If no performance files exist and sent-log checkboxes are all unchecked, status = "NO CONTENT POSTED."

### Step 4: Assess Pipeline Stage

For each completed week, determine the pipeline stage:

```
✅ Planning          — MASTER_PLAN.md exists with themes and platforms
✅ Writing           — Captions/scripts (.txt) exist for all platforms
✅ Image generation  — .png files exist (verify count vs. plan)
✅ Video production  — .mp4 files exist (check sizes for Manim; .html for Hyperframes)
❌ Pricing           — Any GHC [PRICE] placeholders unresolved
❌ H review          — No evidence of human approval step
❌ Posting           — No confirmation content reached any platform
❌ Performance       — No engagement/reach/conversion data
```

### Step 5: Write Performance Report

Save to `content-output/CONTENT_PERFORMANCE_YYYY-MM-DD.md` with this structure:

1. **Executive Summary** — One-line status: assets ready, posted count, key finding
2. **Planned vs. Posted** — Table per day per brand: planned content type, assets status, posted YES/NO
3. **Platform-by-Platform Breakdown** — Table: platforms × planned posts × published × metrics (all zeros if nothing posted)
4. **Brand-by-Brand Analysis** — Per brand: assets ready, blockers, positioning notes
5. **Top Performing Content Types** — Cannot be assessed if nothing posted; list highest-potential formats instead
6. **Blockers & Pipeline Status** — Numbered blockers with owner and impact
7. **Recommendations for Next Week** — Prioritized action items (P0/P1/P2)
8. **Appendix: File Inventory** — Exact file counts per week/directory

### Step 6: Post Summary to Telegram Topic 26

The cron delivery mechanism auto-sends the agent's final response. Format the Telegram summary as:

- Short enough to read in 60 seconds
- Use emoji section headers (📊 🤖 🔧 🔴 🟡 🟢)
- Lead with the critical finding (e.g., "NO CONTENT POSTED")
- End with top 3 priorities for next week
- Keep the full report as the saved file; Telegram gets the summary

## Report Template

See `templates/performance-report.md` for the full template.

## Known Failure Modes

### "Content generated but never posted" (Weeks 1–2, May 2026)

This is the #1 pipeline failure mode. All assets are produced but nothing reaches the audience. Root cause: no posting automation + no H approval workflow executed between generation and posting.

**Detection:** sent-log shows all assets complete; content directories full of PNG/TXT files; zero Telegram confirmations; zero performance data.

**Report format:** Explicitly state "X consecutive weeks with zero content delivered" and list the H-action items needed to break the cycle.

### "Comfy Cloud 429 on Week 1 images"

Comfy Cloud free tier returns HTTP 429 PAYMENT_REQUIRED. All 10 Week 1 images were never generated. Resolved by switching to xAI grok-imagine-image for Week 2.

**Detection:** Week directory has only CONTENT_PLAN.md files, no subdirectories with media files.

**Report format:** Note the migration (Comfy Cloud → xAI) and confirm all subsequent weeks use the working backend.

### "Hyperframes HTML without render"

Hyperframes compositions exist as .html files but the hyperframes skill may not be installed, preventing `npx hyperframes render`. HTML compositions are production-ready scaffolds but cannot become MP4 videos until the skill is reinstalled.

**Detection:** .html files in hyperframes/ subdirectories, no .mp4 files alongside them.

**Report format:** List as a P1 blocker: reinstall hyperframes skill → render compositions → post product videos.

### "Price placeholders never filled"

All 2Real Marketplace listings have `GHC [PRICE]` placeholders. H must fill these before any Marketplace post can go live. This has blocked Marketplace revenue for 2+ weeks.

**Detection:** title.txt and description.txt in marketplace/ directories contain `[PRICE]` literal strings.

**Report format:** Flag as H-action P0. Provide the exact file paths that need price insertion.

## Metrics to Track Once Posting Begins

Once content starts being posted, track weekly:
- **Reach:** Unique accounts that saw content (per platform)
- **Engagement:** Likes + comments + shares + saves (per post)
- **Conversion:** WhatsApp inquiries, Marketplace messages, DM requests
- **Video views:** TikTok plays, Reels views, Manim/Hyperframes watch time
- **Follower growth:** Net new followers per platform per week

Until then, the only metric that matters is: **Weeks since last post = X (target: 0)**

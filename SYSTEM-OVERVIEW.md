# OpenClaw — Complete System Overview

*AI-powered content automation for 2 Real Enterprises and Akoma Robotics*
*Last updated: 2026-04-02*

## What Is OpenClaw?

OpenClaw is an AI agent framework that runs locally on Windows and orchestrates content automation for two Ghanaian businesses.

### The Businesses

**2 Real Enterprises** - Hardware and building equipment supplier in Ghana
**Akoma Robotics** - STEM education for children (ages 8-14)

## Technology Stack

- OpenClaw: AI agent framework running on Windows
- Primary Model: OpenRouter API (deepseekv3.2)
- Image Generation: Gemini 3 Pro Image via OpenRouter
- Messaging: WhatsApp for delivery
- Database: PostgreSQL with pgvector (semantic search)

## Complete System Flow

### 1. Startup Sequence (Every Session)
1. Load Core Context (~4K tokens): memory/projects.md, MEMORY.md, SOUL.md, USER.md
2. Verify Workspace (check critical files, test gateway)
3. Vector Memory Sync (48h cycle via memory_flush.py)
4. Report Status to memory/YYYY-MM-DD.md

**Key Rule**: Daily notes are NEVER loaded at startup (archives only). Loaded on-demand.

### 2. Weekly Content Generation

**SUNDAY/MONDAY - Content Generation**
- OpenClaw generates 6 posts (3 Akoma + 3 2 Real)
- 6 images via Gemini 3 Pro Image API
- Formatted with hashtags, CTAs, posting notes
- Content sent to John (Ghana) via WhatsApp

**MONDAY-SATURDAY - Posting Schedule**
- Mon/Wed/Fri: Akoma Robotics content
- Tue/Thu/Sat: 2 Real Enterprises content
- Platforms: Facebook, WhatsApp Status, TikTok, Instagram

**SUNDAY - Distribution Day**
1. Share best content to WhatsApp Groups
2. Create & distribute weekly PDF (deals)
3. Repurpose top posts to WhatsApp Status
4. Review performance, adjust next week's strategy

### 3. Memory System (How I Remember)

**DAILY NOTES (archive)**
- memory/YYYY-MM-DD.md
- Raw logs, loaded on-demand only

**LONG-TERM MEMORY (curated)**
- MEMORY.md: Distilled insights (loaded at startup, ~3K tokens, max 400 lines)
- memory/projects.md: Project registry (loaded at startup, ~1K tokens, max 80 lines)

**VECTOR DB (pgvector + PostgreSQL)**
- Semantic search across all memory
- Synced every 48h via memory_flush.py

### 4. 48-Hour Maintenance Cycle

1. Memory Maintenance - Update MEMORY.md, projects.md, run memory_flush.py
2. Workspace Audit - Check files, clean temp/lock files
3. Agent Health Check - Verify 3 agents, test skills, check connections
4. Index Updates - Update MASTER_INDEX.md

## Content Calendar

| Day | Brand | Content Type |
|-----|-------|-------------|
| Monday | Akoma Robotics | Educational content |
| Tuesday | 2 Real Enterprises | Product showcase |
| Wednesday | Akoma Robotics | Student spotlight |
| Thursday | 2 Real Enterprises | Tips & how-to |
| Friday | Akoma Robotics | Engagement (polls, Q&A) |
| Saturday | 2 Real Enterprises | Taiwah influencer + Deals |
| Sunday | Both brands | Distribution + PDF |

## Workflow Details

1. **Content Generation** - Owner requests weekly batch, OpenClaw generates 6 posts with captions, images, and posting notes
2. **Delivery** - Content sent to John via WhatsApp (image + caption + platform + schedule)
3. **Posting** - John posts on schedule, responds to enquiries within 4 hours
4. **Sunday Distribution** - Share to WhatsApp Groups, create PDF, repurpose to Status
5. **Feedback Loop** - John reports engagement, OpenClaw adjusts next week's content

## Brand Guidelines

### 2 Real Enterprises Voice
- Direct, confident, professional but approachable
- Value-focused (quality AND price)
- Action-oriented, trust-building

### Akoma Robotics Voice
- Warm, encouraging, educational but accessible
- Aspirational, inclusive, Ghanaian-proud

## AI Brand Ambassador: Taiwah

A virtual Ghanaian woman (30yo, rich brown skin, oval face, short afro, gold earrings) used in marketing content for both businesses.
Appears in product photos, flash sales, and brand campaigns to build consistent brand recognition without expensive photoshoots.

## Key Personnel

- **H (Owner, UK-based)**: Oversees businesses, approves content strategy, manages OpenClaw
- **John (Employee, Ghana)**: Content poster, receives content via WhatsApp, posts on schedule

## Costs

- Text generation (6 captions): ~~.05-0.10.05-0.10 weekly
- Image generation (6 images): ~~.12-0.30.12-0.30 weekly
- Total: ~~.20-0.40.20-0.40 weekly, ~$1-2 monthly

## Files & Structure

C:\Users\User\.openclaw\workspace\
├── AGENTS.md, SOUL.md, USER.md, MEMORY.md, RULES.md
├── SYSTEM-OVERVIEW.md (this document)
├── memory/ (daily activity logs + projects.md)
└── insights/ (raw data insights)

## Integrations

- Gateway: OpenClaw Control on :18789
- WhatsApp: Primary delivery to John
- Telegram: Monitoring and alerts
- OpenRouter: AI models (text + image)
- PostgreSQL: Database with pgvector

## Future Plans

1. Full automation: Cron job generates content every Sunday automatically
2. Performance tracking: Automated metrics from social platforms
3. Inventory integration: Content adjusts based on real-time stock
4. Expanded platforms: Instagram Reels, TikTok video content
5. Multi-language: Twi translations for local market

## Contact

- **System Owner**: H (WhatsApp: +233204252252)
- **Content Poster**: John (WhatsApp: +233233352252)
- **System**: OpenClaw (local deployment, Windows 11)

---
*This document is maintained by OpenClaw and updated as the system evolves.*


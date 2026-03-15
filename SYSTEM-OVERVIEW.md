# OpenClaw Content Automation — System Overview

*This document explains how our AI-powered content creation system works.*
*Last updated: 2026-03-15*

---

## What Is This?

We run an **AI-powered content automation system** called **OpenClaw** that generates and distributes social media content for two businesses — **2 Real Enterprises** and **Akoma Robotics** — operating in Ghana.

The system replaces the need for a marketing agency or dedicated content team. One person (the owner) monitors and approves, while AI handles generation, formatting, and delivery.

---

## The Businesses

### 2 Real Enterprises
- **What**: Hardware and building equipment supplier
- **Market**: Ghana (sourced from UK)
- **Customers**: Contractors, tradesmen, electricians, plumbers, DIY builders
- **Brands stocked**: DeWalt, Bosch, Makita
- **Operations**: Retail shop in Kantamanto, warehouse in Accra
- **AI Brand Ambassador**: "Taiwah" — a virtual Ghanaian woman used in product photography

### Akoma Robotics
- **What**: STEM education programme teaching coding and robotics to children
- **Market**: Ghanaian schools (after-school programmes)
- **Students**: Ages 8-14, boys and girls, all skill levels
- **Curriculum**: mBot robotics, mBlock programming, sensors, autonomous navigation
- **Model**: Partner schools host, Akoma provides equipment, curriculum, and trained facilitators

---

## How It Works — The Full Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  SUNDAY / MONDAY                                            │
│                                                             │
│  1. OpenClaw generates the week's content batch             │
│     - 6 captions (3 Akoma + 3 2 Real)                       │
│     - 6 images via Gemini 3 Pro Image API                   │
│     - Formatted with hashtags, CTAs, posting notes          │
│                                                             │
│  2. Content is sent to John (Ghana) via WhatsApp            │
│     - Each post: image + caption + platform + schedule      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  MONDAY – SATURDAY                                          │
│                                                             │
│  John posts on schedule:                                    │
│  Mon/Wed/Fri → Akoma Robotics content                       │
│  Tue/Thu/Sat → 2 Real Enterprises content                   │
│                                                             │
│  Platforms: Facebook, Instagram, TikTok, LinkedIn, Jiji, WhatsApp│
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  SUNDAY — DISTRIBUTION DAY                                  │
│                                                             │
│  1. Share best content from the week into WhatsApp Groups   │
│  2. Create & distribute weekly PDF (deals + class schedule) │
│  3. Repurpose top posts to WhatsApp Status                  │
│  4. Review performance, adjust next week's strategy         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Technology Stack

### Core System
- **OpenClaw**: AI agent framework running on Windows
- **Model**: OpenRouter API (hunter-alpha / various models for text and image)
- **Image Generation**: Google Gemini 3 Pro Image Preview via OpenRouter
- **Messaging**: WhatsApp integration for delivery to team members
- **Scheduling**: Built-in cron jobs for automation

### What OpenClaw Does
1. **Content Generation** — Writes captions, hooks, CTAs, hashtags
2. **Image Generation** — Creates product photos, influencer content, educational graphics
3. **Scheduling** — Sends content on the right day to the right person
4. **Tracking** — Maintains content calendar and posting log
5. **Distribution** — Sunday WhatsApp group shares and PDF distribution

### What It Costs
| Item | Weekly Cost | Monthly Cost |
|------|-------------|--------------|
| Text generation (6 captions) | ~$0.05-0.10 | ~$0.20-0.40 |
| Image generation (6 images) | ~$0.12-0.30 | ~$0.50-1.20 |
| WhatsApp delivery | Free | Free |
| Scheduling (cron jobs) | Free | Free |
| **Total** | **~$0.20-0.40** | **~$1-2** |

---

## Content Calendar

| Day | Brand | Content Type | Platforms |
|-----|-------|-------------|-----------|
| **Monday** | Akoma Robotics | Educational content | Facebook, Instagram, LinkedIn, WhatsApp |
| **Tuesday** | 2 Real Enterprises | Product showcase | Facebook, Marketplace, Jiji, Instagram, WhatsApp |
| **Wednesday** | Akoma Robotics | Social proof (testimonials, projects) | Facebook, Instagram, TikTok, WhatsApp |
| **Thursday** | 2 Real Enterprises | Tips & how-to / Behind-the-scenes | Facebook, Instagram, TikTok, LinkedIn, WhatsApp |
| **Friday** | Akoma Robotics | Engagement (polls, Q&A) | Facebook, Instagram, TikTok, WhatsApp |
| **Saturday** | 2 Real Enterprises | Taiwah influencer + Flash deals | All platforms |
| **Sunday** | Both brands | Distribution to WhatsApp Groups + PDF | WhatsApp Groups, Broadcast, Status |

---

## Key Personnel

### H (Owner, UK-based)
- Oversees both businesses remotely from London
- Reviews and approves content strategy
- Manages OpenClaw system
- Has final say on brand voice and messaging

### John (Employee, Ghana)
- Front-line content poster
- Receives pre-made content via WhatsApp
- Posts to Facebook, Facebook Marketplace, Instagram, TikTok, LinkedIn, Jiji, WhatsApp Business, WhatsApp Status on schedule
- Also handles Akoma Robotics school enquiries
- Student — morning classes, afternoon warehouse work

---

## The AI Influencer: Taiwah

**Who she is**: A virtual Ghanaian woman created with AI image generation tools. She is the face of **both** brands.

**Physical appearance**: 30 years old, rich brown skin, oval face, high cheekbones, almond-shaped dark brown eyes, short textured black afro with plain headband, gold hoop earrings, athletic-feminine build.

**What she promotes**:
- **2 Real Enterprises**: Demonstrates tools, shows proper technique, advocates for quality tools over cheap alternatives — "Do it right, not shoddy"
- **Akoma Robotics**: Passionate advocate for STEM education, knowledgeable about robotics, explains how coding and building robots helps people of all ages, inspires the next generation of Ghanaian innovators

**Her personality**:
- Confident and knowledgeable about both tools and robotics
- Passionate about quality workmanship — no shoddy jobs
- Believes technology and proper tools can transform lives
- Speaks to all ages — kids, parents, tradesmen, professionals
- Ghanaian-proud, aspirational but relatable

**How she's used**:
- Saturday content slots (primarily 2 Real, crossover content)
- Product launches and flash deals
- Akoma Robotics awareness and enrollment campaigns
- Educational content (how-to, technique, why it matters)
- Brand awareness across both businesses

**Why**: A consistent face builds brand recognition across two different businesses. Taiwah bridges the gap — she shows that quality tools and STEM education are both about empowering people to build better.

---

## Content Types

### 2 Real Enterprises
- **Product Showcase**: Professional photos of tools with specs and pricing
- **Tips & How-To**: "How to choose the right drill bit" — builds trust and expertise
- **Behind-the-Scenes**: Warehouse, unboxing, real operations
- **Flash Deals**: Urgency-driven pricing with clear CTAs
- **Taiwah Influencer**: AI-generated lifestyle content with products

### Akoma Robotics
- **Educational**: "Why coding is the new literacy" — value-first content for parents
- **Social Proof**: Student projects, parent testimonials, instructor profiles
- **Engagement**: Polls, questions, "what does your child want to build?"
- **Student Spotlights**: Showcasing real learning outcomes

---

## Staff Performance Targets

| Metric | Target | Frequency |
|--------|--------|-----------|
| WhatsApp Status updates | 1+ per day | Daily |
| Facebook posts | 1 per brand day | Mon–Sat |
| Jiji listings (new/refreshed) | 5+ | Weekly |
| Customer response time | <4 hours | Ongoing |
| WhatsApp Group distribution | Top content shared | Sunday |
| Total quality posts | 12+ | Monthly |

---

## Workflow Details

### Step 1: Content Generation (OpenClaw)
- Owner requests weekly batch: "Generate this week's content"
- OpenClaw generates 6 posts (3 per brand) with:
  - Written captions (hooks, value, CTAs, hashtags)
  - Platform-specific formatting
  - Image generation via Gemini 3 Pro Image API
  - Posting notes for John (time, platform, special instructions)

### Step 2: Delivery (WhatsApp)
- OpenClaw sends each post to John via WhatsApp
- Package: Image + Caption + Platform + Day to post
- John receives ready-to-post content — no editing needed

### Step 3: Posting (John)
- John posts on the scheduled day and platform
- Responds to comments and enquiries within 4 hours
- Logs activity (optional — via Zobase inventory system)

### Step 4: Sunday Distribution
- Best content from the week shared into relevant WhatsApp Groups
- Weekly PDF created (2 Real deals + Akoma class schedule)
- Repurposed content posted to WhatsApp Status
- Performance review: what worked, what to adjust

### Step 5: Feedback Loop
- John reports engagement and enquiries back
- OpenClaw adjusts next week's content based on performance
- Owner reviews monthly metrics

---

## AI Brand Guidelines

### 2 Real Enterprises Voice
- Direct and confident
- Professional but approachable
- Value-focused (quality AND price)
- Action-oriented (every post → WhatsApp enquiry)
- Trust-building (genuine tools, reliable delivery)

### Akoma Robotics Voice
- Warm and encouraging (speaking to parents)
- Educational but accessible
- Aspirational (showing what's possible)
- Inclusive (boys AND girls, all skill levels)
- Ghanaian-proud

### What We Don't Do
- No fear-based messaging ("Your child will be LEFT BEHIND!")
- No unrealistic promises
- No Nigerian slang (we're Ghanaian-focused)
- No posts without clear CTAs
- No generic motivational content — we sell tools and education

---

## Files & Structure

```
openclaw-workspace/
├── digital-presence-calendar.md    # Merged content calendar + tracking
├── gem-2real-content-director.md   # Gemini Gem setup for 2 Real
├── gem-akoma-content-director.md   # Gemini Gem setup for Akoma
├── taiwah-character-reference.md   # Taiwah anchor prompt
├── MEMORY.md                       # System memory & people
├── memory/
│   └── 2026-03-15.md              # Daily activity log
├── insights/
│   └── raw-data-insights.md       # Historical data & conversations
└── SYSTEM-OVERVIEW.md             # This file
```

---

## Cost Optimisation Notes

- **Text generation**: Using OpenRouter's cheaper models (~$0.01-0.02 per caption)
- **Image generation**: Gemini 3 Pro Image via OpenRouter (~$0.02-0.05 per image)
- **No subscriptions**: No monthly fees for design tools, content calendars, or social media managers
- **Minimal human time**: ~10 minutes/week for owner review, ~15 min/day for John to post
- **No hosting costs**: Everything runs on local machine (Windows PC)

---

## Future Plans

1. **Full automation**: Cron job generates content every Sunday automatically
2. **Performance tracking**: Automated metrics collection from social platforms
3. **Inventory integration**: Content adjusts based on real-time stock levels (Zobase)
4. **Video content**: Short-form video for TikTok and Instagram Reels (Veo 3.1)
5. **Multi-language**: Twi translations for local market penetration
6. **Platform-specific formatting**: Auto-resize and adapt content per platform specs

---

## Contact

- **System Owner**: H (WhatsApp: +233204252252)
- **Content Poster**: John (WhatsApp: +233233352252)
- **System**: OpenClaw (local deployment, Windows 11)

---

*This document is maintained by OpenClaw and updated as the system evolves.*

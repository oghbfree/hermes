# Content Pipeline Architecture — Reference

## Tool Stack (as of 2026-05-18)

| Tool | Role | Status | Notes |
|------|------|--------|-------|
| **xAI** (image_gen) | Photorealistic images | ✅ Working | grok-imagine-image, $0.002/img. Key in `.env` as `XAI_API_KEY`. |
| **FAL.ai** (image_gen) | Photorealistic images | ⚠️ Key in `.env`, $0 balance | flux-2/klein/9b (fast) + flux-2-pro (production) |
| **Manim CE v0.20.1** | Akoma educational videos | ✅ Working | Installed with MSVC Build Tools + Windows SDK. Tested OK. |
| **Hyperframes v0.6.7** | 2Real product videos | ✅ Working | Tested OK. Skill may need reinstall after workspace consolidation. |
| **FFmpeg 8.1.1** | Video stitching | ✅ Working | — |
| **Node.js 24.14.1** | Hyperframes runtime | ✅ Working | — |
| **MSVC Build Tools 2022** | Manim dependency | ✅ Installed | cl.exe + Windows SDK 10.0.26100.0 |

## Image Generation Backends (priority order)

1. **xAI** — grok-imagine-image — $0.002/img (cheapest, configured and working as of May 2026)
2. **FAL.ai** — flux-2/klein/9b — $0.006/MP (key configured, needs credits)
3. **FAL.ai** — flux-2-pro — $0.03/MP (production quality)
4. **OpenAI** — gpt-image-2 — ~$0.03-0.06/img (key not yet obtained)

## Platform Lineup (7)

| # | Platform | Akoma | 2Real | Content Type |
|---|----------|-------|-------|-------------|
| 1 | Instagram | ✅ | ✅ | Feed posts, Reels |
| 2 | Facebook | ✅ | ✅ | Page posts |
| 3 | FB Marketplace | — | ✅ | Product listings |
| 4 | TikTok | ✅ | ✅ | Short-form video concepts |
| 5 | WhatsApp Status | ✅ | ✅ | Daily updates |
| 6 | WhatsApp Broadcast | ✅ | ✅ | Weekly roundup |
| 7 | LinkedIn | ✅ | ✅ | 2 posts + 1 article/week/brand |

## LinkedIn Cadence

- **Akoma:** Mon (article) + Wed (post) + Fri (post)
- **2Real:** Tue (post) + Thu (post) + Sat (article)
- Articles: 800-1200 words, markdown, saved to `linkedin/articles/`
- Posts: 150-300 words, saved to `linkedin/posts/`
- Header images: image_gen landscape 16:9

## Brand Schedule

| Day | Brand | Theme | Video Tool |
|-----|-------|-------|-----------|
| Mon | Akoma | Educational | Manim CE |
| Tue | 2Real | Product Showcase | Hyperframes |
| Wed | Akoma | Social Proof | Manim CE |
| Thu | 2Real | Tips & How-To | Hyperframes |
| Fri | Akoma | Engagement/Polls | Manim CE |
| Sat | 2Real | Deals/Flash Sale | Hyperframes |
| Sun | Both | Distribution | — |

## Brand Assets

### Akoma Robotics
- **Colors:** Purple #6A0DAD (primary), Gold #FFD700 (accent), White #FFFFFF, Circuit Blue #0000FF
- **Logo:** Heart + interlocking gears + handshake icon, "AKOMA ROBOTICS" uppercase
- **Tagline:** "The Heart of Robotics in Accra, Ghana | London, UK"
- **Files:** `content-assets/akoma/` — logo.png, AKOMA_BRAND_GUIDELINES.md, General Marketing/ (5 images)
- **Source:** Extracted from official marketing images via vision_analyze + website text from Drive folder

### 2 Real Enterprises
- **Colors:** ❌ NOT CONFIRMED — no logo/brand assets found in Drive folder
- **Tagline:** "Real Tools. Real Work. Real Ghana."
- **Files:** `content-assets/2real/` — 2REAL_BRAND_GUIDELINES.md, 2REAL_LINKEDIN_STRATEGY.md
- **Source:** LinkedIn strategy doc from Drive. Logo, website URL, and brand colors still needed from user.

## Cron Jobs

| Job | ID | Schedule | Skills | Deliver |
|-----|----|----------|--------|---------|
| Sunday Content Engine | b787e85493ea | Sun 20:00 | ai-influencer-content-pipeline, manim-video, hyperframes | TG topic 26 |
| Saturday Performance | 147a33d412c6 | Sat 09:11 | — | TG topic 26 |

## Lessons Learned

1. **Comfy Cloud → xAI migration:** Comfy Cloud subscription never paid. Replaced with xAI ($0.002/img) as primary, FAL.ai as backup.
2. **Hyperframes lost during consolidation:** When `.openclaw` was archived, `~/.hermes/skills/hyperframes/` was deleted. Always verify skills after workspace migrations.
3. **Manim on Python 3.14 requires MSVC Build Tools:** moderngl can't compile without C compiler + Windows SDK. Fix: download vs_buildtools.exe → install C++ workload (~8GB, 15-30 min) → set INCLUDE/LIB env vars → `pip install moderngl glcontext`. Confirmed working May 2026.
4. **LinkedIn tone:** Professional, no emoji-heavy captions, no price promotions. Thought leadership, not sales.
5. **FAL.ai free credits:** May not be available for new accounts. Have backup (xAI at $0.002/img) ready.
6. **MSVC env vars for moderngl:** Must set PATH, INCLUDE, and LIB manually in bash before `pip install moderngl`. The `call vcvars64.bat` pattern doesn't work in MSYS/bash — use explicit export paths.
7. **Google Drive gdown on Windows:** `gdown --folder` fails when paths contain special characters (colons, parentheses). Use `-O` with a simple short path. Some subfolders may need individual retry. Direct `uc?id=<file_id>` works for small individual files.
8. **Brand asset extraction workflow:** Drive folder → gdown → find images → vision_analyze each → read .txt files → compile BRAND_GUIDELINES.md with hex codes. Save both raw assets and extracted guidelines.
9. **Akoma colors corrected:** Purple #6A0DAD + Gold #FFD700 (NOT blue/white/orange as previously stated in older versions of this doc).

---
name: ai-influencer-content-pipeline
description: "End-to-end content pipeline for AI influencer characters: character anchor definition, multi-platform content planning, cron-scheduled generation, and brand-consistent image prompts. Use when setting up or operating a content pipeline that uses an AI-generated influencer persona for social media marketing."
version: 2.1.0
author: OWL/Hermes
---

# AI Influencer Content Pipeline

Operate a complete content creation pipeline using an AI influencer character for multi-platform social media marketing.

## User Communication Style

H prefers direct, execution-oriented communication:
- Short messages, minimal punctuation, uses "i" not "I"
- "Figure it out implement and produce" = decide and build, don't present options
- Expects AI to extract tasks from stream of consciousness
- No fluff, no "please/thank-you", no verbose explanations
- "Formalise" = document it. "Tidy up" = structure it. "Crunch numbers" = calculate with assumptions
- When he asks a question, he wants the answer — not a list of options to choose from
- Default to the most practical option and start working; ask only when truly blocked

- Setting up a new AI influencer character for a brand
- Creating a content calendar with alternating brands/themes
- Configuring cron jobs for automated content generation
- Generating platform-specific captions and image prompts
- Managing character consistency across image generations

## Architecture

```
Brand Assets (skills/creative/brand-assets/ — centralized reference)
    ↓
Character Anchor (references/taiwah-character.md)
    ↓
Master Prompts (TAIWAH_MASTER_PROMPT.md)
    ↓
Content Plan (per-week directory)
    ↓
Cron Jobs (Sunday engine + Saturday performance)
    ↓
Image Generation (Hermes image_gen tool — FAL.ai / OpenAI / xAI)
    ↓
Platform Delivery (IG, FB, TikTok, WA, LinkedIn, etc.)
```

**IMPORTANT:** Always load the `brand-assets` skill first. It is the single source of truth for all brand identity, character anchors, and platform specs.

## Step 1: Define the Character Anchor

Create a `CHARACTER_ANCHOR.md` with these sections:

1. **Core Character Identity** — name, age, nationality, background, role, personality
2. **Physical Appearance (EXACT)** — face, hair, earrings, build, hands/feet specifications
3. **Signature Wardrobe** — primary, secondary, and context-specific outfits
4. **Technical Rendering Standards** — what MUST and NEVER apply
5. **Camera Specifications** — lens, aperture, composition by shot type
6. **Lighting Scenarios** — studio, golden hour, workshop, dramatic
7. **Expression Library** — when to use each expression
8. **Setting Contexts** — workshop, studio, job site, lifestyle
9. **Consistency Rules (Non-Negotiable)** — 10+ rules that must never be broken
10. **Usage by Content Type** — how the character appears in each content format
11. **Image Generation Template** — copy-paste ready prompt structure
12. **Existing Asset Inventory** — table of all generated images

### Key Principles
- **Specificity over generality**: "medium gold hoop earrings" not "nice earrings"
- **Negative prompts are mandatory**: always include what to NEVER render
- **Grounded feet, correct hands**: specify these explicitly to avoid common AI artifacts
- **Wardrobe consistency**: define exact outfits for each content context

## Step 2: Create Master Prompts

Create a `MASTER_PROMPT.md` with copy-paste ready prompts for each content type:

- Product Showcase (multiple platform variants)
- Tips & How-To
- Deals / Flash Sale
- Brand Ambassador Portrait
- Behind-the-Scenes

Each template should include:
- Full prompt with `[BRACKETED]` placeholders
- Negative prompt
- Camera/lens specifications
- Platform-specific composition notes

## Step 3: Set Up Content Directory Structure

```
content-output/week-YYYY-MM-DD/
  MASTER_PLAN.md
  monday-brand/
    instagram/
      caption.txt
      image.png
    facebook/
      caption.txt
      image.png
    tiktok/
      script.txt
      concept.png
    whatsapp-status/
      caption.txt
      image.png
    linkedin/
      article.md OR post.txt
      header-image.png
    manim/ (Akoma only)
      script.py
      output.mp4
    hyperframes/ (2Real only)
      project/
        composition.html
        output.mp4
    marketplace/ (2Real only)
      title.txt
      description.txt
      price.txt
      image.png
  tuesday-brand/
    ...
  sunday-distribution/
    whatsapp-broadcast/
      message.txt
      image.png
```

## Step 4: Create Content Plans

For each day, write a `CONTENT_PLAN.md` containing:
- Content theme/topic
- Platform-specific captions (with hashtags, CTAs, emoji)
- TikTok scripts (hook → shots → CTA)
- Image generation prompts (referencing the master prompt templates)
- Marketplace listings (title, price, description)

### Caption Rules
- Always end with WhatsApp CTA
- 3-5 hashtags per post
- Platform-appropriate length (FB: 40-80 words, IG: hook + 3-5 sentences, TikTok: 1-2 lines, WA: 1-2 lines)
- Include brand-relevant emojis sparingly

## Step 5: Configure Cron Jobs

### Sunday Content Engine
- **Schedule**: Sunday 20:00 (gives time for review before Monday)
- **Deliver to**: Telegram topic or channel for review
- **Skills**: ai-influencer-content-pipeline, manim-video, hyperframes
- **Image generation**: Built-in `image_gen` tool (FAL.ai backend)
- **Prompt**: Read the SUNDAY_CONTENT_ENGINE_PROMPT.md and execute full generation

### Saturday Content Performance Review
- **Schedule**: Saturday 09:11
- **Deliver to**: Same Telegram topic
- **Task**: Review past week's content pipeline and report status
- **Workflow**: See `references/performance-review.md` for the complete 6-step review process (read sent-log → inventory directories → check performance data → assess pipeline stage → write report → post summary)
- **Report template**: `templates/performance-report.md`
- **Key rule**: If no content was posted, explicitly state "NO CONTENT POSTED — X consecutive weeks" and list H-action blockers as P0 items
- **Hyperframes render check**: When reviewing Hyperframes compositions, verify `.mp4` files exist alongside `.html`. If only `.html` exists → composition written but not rendered → list as blocker

## Step 6: Image Generation

**Primary method: Hermes built-in `image_gen` tool** (FAL.ai / OpenAI / xAI backends).

The `image_gen` tool is available natively in Hermes — no external scripts or API keys needed at the prompt level. Configure the backend once via `hermes tools` → 🎨 Image Generation, then use it directly in agent prompts.

### Available Backends

| Backend | Model | Speed | Strengths | Cost |
|---------|-------|-------|-----------|------|
| FAL.ai (default) | flux-2/klein/9b | <1s | Fast, crisp text | $0.006/MP |
| FAL.ai | flux-2-pro | ~6s | Studio photorealism | $0.03/MP |
| FAL.ai | gpt-image-2 | ~20s | Best text + CJK, photoreal | $0.04–0.06/img |
| FAL.ai | nano-banana-pro | ~8s | Reasoning depth | $0.15/img |
| FAL.ai | recraft-v4/pro | ~8s | Brand/design systems | $0.25/img |
| OpenAI | gpt-image-2 | ~15s | Prompt adherence | ~$0.034/img |
| xAI | grok-imagine-image | varies | — | varies |

**Recommended:** FAL.ai with `flux-2/klein/9b` for fast iterations + `flux-2-pro` for final production shots. FAL offers free credits to start.

### xAI Backend (Recommended — Cheapest)
- **Config format**: `image_gen.provider: xai`, `image_gen.model: grok-imagine-image` (NOT `xai/grok-imagine-image` as the model value — that format is for FAL.ai only)
- **Cost**: $0.002/img (1K resolution) — 3x cheaper than FAL.ai, 15-30x cheaper than OpenAI
- **Key env var**: `XAI_API_KEY` in `~/.hermes/.env`
- **Setup**: Sign up at https://console.x.ai → API Keys → create key → add to `.env`

### FAL.ai Backend
- **Config format**: `image_gen.provider: fal`, `image_gen.model: fal-ai/flux-2/klein/9b`
- **Key env var**: `FAL_KEY` in `~/.hermes/.env` (format: `key:secret`)
- **Note**: Free credits may not be available for new accounts. Check balance at fal.ai/dashboard/billing.
- **Cost**: $0.006/MP (klein 9b) or $0.03/MP (flux-2-pro)

### OpenAI Backend
- **Config format**: `image_gen.provider: openai`, `image_gen.model: gpt-image-2`
- **Key env var**: `OPENAI_API_KEY` in `~/.hermes/.env`
- **Cost**: ~$0.034-0.06/img
- `landscape` — 16:9 (posts, banners, LinkedIn articles)
- `square` — 1:1 (Instagram feed, FB posts)
- `portrait` — 9:16 (Stories, TikTok, WhatsApp Status)

### Usage in Agent Prompts
Simply describe what you want — the tool handles model selection, payload building, and download:
- "Generate a square portrait of Taiwah holding a power tool in a workshop"
- "Create a landscape image for a LinkedIn article about STEM education in Ghana"

### Legacy: Comfy Cloud (if still used)
Comfy Cloud remains an option for complex multi-step workflows (ControlNet, inpainting, etc.) but is **not required** for standard character-consistent image generation. If using Comfy Cloud:
- Requires paid subscription (free tier returns 429)
- Use `flux_dev_txt2img.json` workflow (NOT `flux_dev_fp8_cloud.json`)
- See the `comfyui` skill for full setup

### Critical Requirements
- **Always include the full character anchor in every prompt**
- **Always include the negative prompt**
- Generate at 1024×1024 minimum
- For FAL.ai: set `FAL_KEY` in `.env` or configure via `hermes tools`

## Multi-Brand Calendar Pattern

For alternating brands (e.g., Akoma Mon/Wed/Fri, 2Real Tue/Thu/Sat):

| Day | Brand | Content Focus |
|-----|-------|--------------|
| Mon | Brand A | Educational |
| Tue | Brand B | Product Showcase |
| Wed | Brand A | Social Proof |
| Thu | Brand B | Tips & How-To |
| Fri | Brand A | Engagement/Polls |
| Sat | Brand B | Deals/Influencer |
| Sun | Distribution | WA Broadcast, repurpose |

## Platform Matrix

| Platform | Format | Size | Caption Style |
|----------|--------|------|--------------|
| Instagram Feed | Square/Portrait | 1080×1080/1350 | Hook + body + CTA + hashtags |
| Facebook Post | Landscape | 1200×630 | Hook + 3-5 sentences + CTA |
| FB Marketplace | Product listing | Varied | Title + specs + price + description |
| TikTok | Vertical video | 1080×1920 | Script with hook, shots, CTA |
| WhatsApp Status | Vertical image | 1080×1920 | 1-2 lines max |
| WhatsApp Broadcast | Text + image | N/A | Value-first, not salesy |
| LinkedIn Post | Text + image | 1200×627 | 150-300 words, professional, CTA |
| LinkedIn Article | Long-form text + header | 1400×728 header | 800-1200 words, thought leadership |

## LinkedIn Content Strategy

### Akoma Robotics (2 posts + 1 article/week)
- **Monday:** Article — STEM education thought leadership (800-1200 words)
- **Wednesday:** Post — STEM tip, insight, or industry observation
- **Friday:** Post — Student spotlight, project showcase, or engagement
- Hashtags: #STEMeducation #Robotics #Ghana #EdTech #AkomaRobotics

### 2 Real Enterprises (2 posts + 1 article/week)
- **Tuesday:** Post — Industry insight, construction market, tool quality
- **Thursday:** Post — Business journey, entrepreneurship, lessons
- **Saturday:** Article — Hardware industry thought leadership (800-1200 words)
- Hashtags: #GhanaBusiness #Construction #Hardware #2RealEnterprises

### LinkedIn Content Rules
- Articles saved as markdown — ready to paste into LinkedIn editor
- Posts: 150-300 words, professional tone, question or CTA at end
- Header images generated via FAL.ai (flux-2-pro, landscape_16_9)
- No price placeholders on LinkedIn — link to website/WhatsApp for pricing

## Video Production

### Manim CE — Akoma Educational Videos
- **When:** Monday and Wednesday content
- **Style:** 3Blue1Brown-inspired, Akoma color palette (blue/white/orange)
- **Length:** 30-60 seconds
- **Output:** 1920×1080 MP4
- **Process:** Plan → Code → Draft render (-ql) → Production render (-qh) → Stitch
- **Skill:** manim-video

### Hyperframes — 2Real Product Videos
- **When:** Tuesday, Thursday, Saturday content
- **Style:** Branded product showcases, Taiwah character integration
- **Length:** 5-15 seconds
- **Output:** 1920×1080 MP4
- **Process:** Plan → `npx hyperframes init <name>` → edit `index.html` → `npx hyperframes lint` → `npx hyperframes render`
- **Skill:** hyperframes (may need reinstall after workspace consolidation: `hermes skills install official/creative/hyperframes`)
- **HTML Template:** `templates/hyperframes-composition.html` — proven-good scaffold with correct `data-composition-id="root"`, `class="clip"` + `data-start`/`data-duration`/`data-track-index` structure, GSAP timeline, and `window.__timelines["root"] = tl`. Copy and modify for each composition.
- **CRITICAL:** Use `window.__timelines["root"] = tl` — NOT `window.__hf`. This is the #1 mistake.
- **Required HTML structure:** `data-composition-id="root"` on stage div, `class="clip"` + `data-start` + `data-duration` + `data-track-index` on every animated element
- **2Real brand colors:** Green #4CAF50 (primary), Yellow #FFC107 (accent), White #FFFFFF, Black #000000. Logo = stylized tree with leaves forming "2", yellow-to-green gradient. Website: 2-real.zobaze.shop (Zobaze POS/CRM platform). Tagline: "Real Tools. Real Work. Real Ghana."

### Baoyu Infographic — Both Brands
- **When:** Any day requiring data visualization, product comparisons, educational graphics, or branded infographics
- **Style:** 21 layouts × 21 styles available; match to brand palette (Akoma: blue/white/orange, 2Real: brand colors)
- **Output:** SVG/PNG infographics
- **Use cases:** Product spec comparisons, market data, educational content, social media carousel slides
- **Skill:** baoyu-infographic

## Step 7: H Review & Approval Gate

**This is the critical human-in-the-loop step. Content cannot be posted without H's explicit approval.**

After the Sunday content engine generates all assets:

1. **Content engine delivers** the week's plan + all assets to Telegram topic 26
2. **H reviews** the content plan, captions, images, and videos
3. **H fills in prices** — All `GHC [PRICE]` placeholders in FB Marketplace listings must be replaced with actual prices
4. **H confirms stock** — Verify products have ≥2 units before approving promotion
5. **H gives approval** — Explicit "approve" or "post" instruction, or schedules the content

Until H completes steps 2-5, content remains in the "ready to post" state and must NOT be published.

### Post-Approval Workflow (Once H Approves)

1. Apply brand logos to all images (see Step 8)
2. Render any pending video files (Manim partial → full MP4, Hyperframes HTML → MP4)
3. Post to platforms per the content calendar
4. Log posted content in `sent-log.md` (check the performance tracking box)
5. Track engagement metrics starting 24h after first post

**Performance review tip:** If the Saturday review finds zero content posted, the H review gate is almost always the blocker. List it as P0 and provide H with the exact files that need review.

## Step 8: Apply Brand Logos to All Content

Every piece of visual content MUST include the correct brand logo. This is non-negotiable.

### Logo Files
- **Akoma Robotics:** `content-assets/akoma/AKOMA_ROBOTICS_LOGO_OFFICIAL.jpg` — Heart + robotic arms handshake, purple (#6A0DAD) + gold (#FFD700)
- **2 Real Enterprises:** `content-assets/2real/2REAL_LOGO.jpg` — Stylized tree forming "2", green (#4CAF50) + yellow (#FFC107)

### Logo Application Rules
1. **Every social media image** (Instagram, Facebook, LinkedIn, WhatsApp Status) gets the logo in the top-right corner
2. **Every video** (Manim, Hyperframes) gets the logo as an overlay
3. **LinkedIn article header images** get the logo
4. **WhatsApp broadcast/roundup images** get BOTH logos when featuring both brands
5. Logo size: ~150px wide for images, ~15% of frame width for videos
6. Position: top-right corner with ~20px margin, or top-left for Hyperframes compositions
7. Use the actual logo image file — NEVER use text as a substitute for the logo

### Image Logo Compositing (Pillow)
```python
from PIL import Image

logo = Image.open(logo_path).convert("RGBA")
logo_w = 150
ratio = logo_w / logo.width
logo_h = int(logo.height * ratio)
logo_resized = logo.resize((logo_w, logo_h), Image.LANCZOS)

img = Image.open(img_path).convert("RGBA")
x = img.width - logo_w - 20
y = 20
img.paste(logo_resized, (x, y), logo_resized)
final = img.convert("RGB")
final.save(img_path, quality=95)
```
**Note:** Run via `terminal` with `python`, NOT via `execute_code` — the sandboxed environment doesn't have Pillow.

### Manim Video Logo Overlay
```python
logo = ImageMobject("akoma-logo.jpg")  # or "2real-logo.jpg"
logo.scale(0.15)
logo.to_corner(UR, buff=0.3)
self.add(logo)  # Add as persistent element, not animated
```
Copy the logo image file into the same directory as the Manim script before rendering.

### Hyperframes Logo Integration
Use an `<img>` tag pointing to the logo file, NOT text:
```html
<img id="logo" class="clip" data-start="0.5" data-duration="7" data-track-index="2"
     src="2real-logo.jpg" alt="2 Real Enterprises"
     style="left:80px;top:60px;width:200px;height:auto;" />
```
Copy the logo image file into the Hyperframes project directory alongside `index.html`.

### Pre-Generation Checklist
- [ ] Official logo file exists in `content-assets/<brand>/`
- [ ] Logo is the correct file (not a placeholder or text-based substitute)
- [ ] For images: logo will be composited after generation
- [ ] For Manim: logo file copied to manim directory, `ImageMobject` added to script
- [ ] For Hyperframes: logo file copied to project directory, `<img>` tag in HTML

## Verification Checklist

### ⚡ Brand Cross-Check (from brand-assets SKILL.md — MANDATORY — RUN FIRST)
For EVERY piece of content output BEFORE delivery:
- [ ] Phone numbers: +233 20 425 2252 (2Real only). No invented numbers. Use `[number]` placeholder if unknown.
- [ ] Akoma CTAs use "Message us on WhatsApp to learn more" — NO phone number
- [ ] Logo descriptions match brand-assets master EXACTLY
- [ ] Brand colors match exact hex codes from brand-assets master (Akoma: #6A0DAD + #FFD700, 2Real: #4CAF50 + #FFC107)
- [ ] Taglines/headlines match brand-assets master
- [ ] CTA templates match brand-assets master
- [ ] Hashtags from locked sets only (no invented hashtags)
- [ ] Akoma content does NOT use website template colors (red/yellow/green from Ghana flag)

IF ANY mismatch → DELETE output and REWRITE from scratch. Do NOT patch in place.

### Standard Checks
- [ ] Character anchor has all 12 sections
- [ ] Master prompts cover all content types
- [ ] Negative prompts included in every template
- [ ] Cron jobs created and delivering to correct Telegram topic
- [ ] Image generation backend configured (`hermes tools` → 🎨 Image Generation)
- [ ] Content directory structure follows the standard layout
- [ ] All captions include WhatsApp CTA
- [ ] All image prompts reference the character anchor
- [ ] Price placeholders marked for business owner review
- [ ] LinkedIn content calendar added (articles + short posts schedule)
- [ ] Blog post templates created for both brands
- [ ] H has reviewed and approved the week's content plan
- [ ] All prices filled in (no remaining `[PRICE]` placeholders)
- [ ] Stock confirmed ≥2 units for all products being promoted

## Pitfalls

1. **Character inconsistency** — Always use the full anchor. Never let the AI "improvise" facial features, earrings, or hair style.
2. **FAL.ai not configured** — If `image_gen` tool is unavailable, run `hermes tools` → 🎨 Image Generation to set up a backend. Free credits available at fal.ai.
3. **Missing negative prompts** — Always include the full negative prompt to avoid plastic skin, extra fingers, floating.
4. **Ungrounded feet** — Always specify "grounded feet, single shadow system" in prompts.
5. **Stock rule violations** — Never promote products with <2 units in stock.
6. **Price placeholders** — Always use `[PRICE]` placeholders and have the business owner fill them in before posting.
7. **Earrings color drift** — AI image generators frequently default to silver/blue earrings. Always specify "gold hoop earrings" explicitly and include "no silver earrings, no blue earrings" in the negative prompt.
8. **Headband omission** — The character's signature headband must be mentioned in EVERY prompt, even casual/lifestyle shots.
9. **Manim render failures** — Always render draft (-ql) before production (-qh). Check LaTeX installation if equations fail.
10. **Hyperframes lint errors** — Always run `npx hyperframes lint` before `render`. GSAP/CSS transform conflicts are the most common issue.
11. **LinkedIn tone mismatch** — LinkedIn content must be professional and thought-leadership oriented. Never use casual/emoji-heavy IG style on LinkedIn. No hashtags in article body. No price promotions.
12. **Comfy Cloud references** — The old pipeline referenced Comfy Cloud. This has been replaced by FAL.ai (image_gen tool). Do NOT use Comfy Cloud scripts.
13. **Skills lost during consolidation** — When workspaces are merged/archived, custom skills in `~/.hermes/skills/` can be lost. Always verify critical skills (hyperframes, comfyui, etc.) still exist after any migration. Reinstall with `hermes skills install <name>` if missing. Hyperframes in particular was lost during the May 17 consolidation and needs reinstalling from `official/creative/hyperframes`.
14. **Manim CE now working on Python 3.14** — As of 2026-05-18, Manim CE v0.20.1 is installed and tested working. Required: MSVC Build Tools 2022 (C++ workload) + Windows 10 SDK. Install took ~30 min (~8GB download). See `manim-video` skill for full details.
15. **xAI cheapest image gen** — At $0.002/img, xAI's grok-imagine-image is 3x cheaper than FAL.ai and 15-30x cheaper than OpenAI. Recommended as primary backend when key is obtained.
16. **MSVC Build Tools install takes 15-30 min** — The C++ workload is ~8GB. Don't assume it's stuck; let it run. Check with `tasklist | grep vs_BuildTools`.
17. **Google Drive folder download via gdown** — `gdown --folder` fails on Windows when folder/file names contain special characters (colons, parentheses, long paths). Workaround: use `-O` with a simple short output path like `gdown <folder_url> --folder -O brand_assets`. Even then, some subfolders may fail with permission errors — retry individually with specific folder URLs. The `uc?id=<file_id>` direct download works for individual small files (<100MB).
18. **Google Drive gdown Windows path issues (additional)** — For critical brand assets, prefer individual file download via `gdown "https://drive.google.com/file/d/<FILE_ID>/view?usp=drive_link"` which is more reliable than folder download. Always verify downloaded file count matches expectations.
18. **Brand asset extraction workflow** — When given a Google Drive folder for brand assets: (1) `gdown --folder -O <simple_path>`, (2) `find` for image files (.png/.jpg/.svg/.webp), (3) `vision_analyze` each marketing image to extract colors/logo/typography, (4) `read_file` any .txt files (website copy, brand guidelines), (5) compile into `BRAND_GUIDELINES.md` with hex codes, logo description, tagline, tone. Always save both the raw assets and the extracted guidelines.
19. **Akoma brand colors — marketing materials are canonical, NOT the website** — The live website (akomarobotics.com) uses a Ghana flag color template (Red #CE1126, Yellow #FCD116, Green #006B3F, Gold #DAA520) which is a generic site template, NOT the brand identity. The OFFICIAL Akoma brand colors are Purple #6A0DAD + Gold #FFD700 from the marketing pullup banners, AR graphics, school flyer, and logo files. ALWAYS use purple/gold for Akoma content. Do NOT use the website template colors for any brand content. Font: Segoe UI (website only — not a brand font).
20. **Hyperframes new project scaffold** — Creating a new Hyperframes composition in a fresh directory requires copying the full scaffold from an existing working project: `package.json`, `meta.json`, `hyperframes.json`, `AGENTS.md`, and `CLAUDE.md`. Without these, `npm run render` fails with `ENOENT: no such file or directory, open 'package.json'`. The `index.html` alone is NOT sufficient. Always copy the scaffold first, then edit `index.html` and `meta.json` for the new composition. **Windows path note:** When copying scaffold files between Hyperframes projects on Windows, use `cp` in bash (not PowerShell `Copy-Item`) to preserve file permissions and avoid path encoding issues.
21. **Image-based PDF text extraction workflow** — When a PDF contains no extractable text (image-based/scanned): (1) Install PyMuPDF: `pip install PyMuPDF`, (2) Render pages to images: `python -c "import fitz; doc=fitz.open('file.pdf'); [p.get_pixmap(dpi=150).save(f'page_{i+1}.png') for i,p in enumerate(doc)]; doc.close()"`, (3) Use `vision_analyze` on each page image to read text, (4) Cross-reference across pages to find all instances of specific words (e.g., spelling errors). PyPDF2 alone only works on text-based PDFs — it returns empty strings for image-based ones. Always check if extracted text is empty before assuming the PDF has no content.
22. **Website brand identity extraction workflow** — When given a website URL to study brand identity: (1) `web_extract` the homepage for text/copy, (2) `curl -sL` the HTML source, (3) grep for `css/*.css` links and download them, (4) grep CSS for hex colors (`#[0-9a-fA-F]{3,8}`), (5) check `<meta property="og:image">` for the cover/hero image URL, (6) download and `vision_analyze` the OG image and any logo files from `/img/logo.*` paths, (7) compile into `BRAND_GUIDELINES.md`. **Important:** SPAs (Vue/React) render via JS — `web_extract` only gets the shell. Use `curl` + grep for the real assets. PHP sites use `.php` extensions — try `programs.php`, `enrollment.php`, etc. if clean URLs 404. **Critical:** Website template colors ≠ brand colors. Always cross-reference with marketing materials, logo files, and ad creative to determine the true brand palette.
23. **Logo must be on EVERY visual asset** — When the user provides an official logo, it must be applied to ALL visual content: social media images, videos, infographics, WhatsApp statuses, LinkedIn headers. No exceptions. If a piece of content doesn't have the logo, it's not ready to post. When generating new content, always ask "Where does the logo go?" before considering the task complete. For images: composite via Pillow (run in terminal, not execute_code — sandbox lacks Pillow). For Manim: use `ImageMobject` overlay with logo file in same directory as script. For Hyperframes: use `<img>` tag with actual logo file, never text as substitute.
24. **image_gen tool returns URLs, not local files** — The `image_gen` tool returns a URL in the `image` field. You MUST download each image via `curl -sL "<url>" -o "<local_path>"` in terminal. Plan the download step into your workflow — generate all images first, then batch-download. The tool does NOT save files locally by default.
25. **Batch image generation pattern** — When generating many images for a full week: (1) Generate all images first using `image_gen` with appropriate aspect_ratio per platform, (2) Collect all returned URLs, (3) Batch download with `curl -sL` in a single terminal command chain, (4) Copy/rename files to the correct platform subdirectories. This is faster than generating and downloading one at a time.
26. **Hyperframes skill still missing (confirmed May 2026)** — The hyperframes skill was not found and was skipped. Hyperframes compositions can still be written as HTML files (the HTML structure is known), but `npx hyperframes render` cannot be executed until the skill is reinstalled. Write the HTML compositions anyway so they're ready when the skill is available. Notify the user that video rendering is pending on hyperframes installation.
27. **Manim CE confirmed working on Windows (May 2026)** — Both Monday and Wednesday videos rendered successfully at `-ql` quality. The Manim CE v0.20.1 + MSVC Build Tools setup is stable. Always render `-ql` draft first to verify, then `-qh` for production. Stitch scenes with ffmpeg concat.
28. **H review gate is the primary bottleneck (confirmed May 2026)** — Two consecutive weeks (May 18–24 and May 25–31) produced 84 total assets but zero content was posted. The consistent blocker: H has not reviewed, approved, or scheduled any content. The pipeline is production-ready but human-gated. Saturday performance reports must explicitly call this out and provide H with the exact files needing review. Until H actively participates in the review step, the pipeline will continue generating content that never reaches the audience.

## Reference

- `references/content-pipeline-architecture.md` — Full tool stack, platform lineup, hardware constraints, FAL.ai setup checklist, and lessons learned
- `references/brand-guidelines.md` — Complete brand colors, logos, typography, tone, and asset locations for both Akoma Robotics and 2 Real Enterprises
- `references/full-week-generation-workflow.md` — Validated end-to-end workflow for the Sunday content engine cron job, including execution order, image generation patterns, render commands, and asset counts
- `references/performance-review.md` — Complete 6-step performance review workflow for the Saturday cron job: how to read sent-log, inventory directories, check performance data, assess pipeline stage, write report, and post summary to Telegram
- `templates/manim-akoma-script.py` — Proven-good Manim CE scene template with Akoma color palette (purple/gold), correct imports, and 4-scene structure
- `templates/hyperframes-composition.html` — Proven-good Hyperframes HTML scaffold with correct `data-composition-id="root"`, `class="clip"` GSAP structure, and `window.__timelines["root"] = tl`
- `templates/performance-report.md` — Content Performance Report template with all required sections: executive summary, planned vs. posted, platform breakdown, brand analysis, blockers, and recommendations

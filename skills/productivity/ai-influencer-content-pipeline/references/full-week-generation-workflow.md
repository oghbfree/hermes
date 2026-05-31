# Full Week Content Generation — Validated Workflow (May 2026)

## Pattern: Sunday Content Engine Cron Job

The Sunday content engine generates ALL content for the coming week (Mon-Sun) in a single session. This document captures the validated workflow.

### Directory Structure Created
```
content-output/week-YYYY-MM-DD/
  MASTER_PLAN.md
  monday-akoma/       — instagram, facebook, tiktok, whatsapp-status, linkedin, manim
  tuesday-2real/      — instagram, facebook, marketplace, tiktok, whatsapp-status, linkedin, hyperframes
  wednesday-akoma/    — instagram, facebook, tiktok, whatsapp-status, linkedin, manim
  thursday-2real/    — instagram, facebook, marketplace, tiktok, whatsapp-status, linkedin, hyperframes
  friday-akoma/       — instagram, facebook, tiktok, whatsapp-status, linkedin
  saturday-2real/     — instagram, facebook, marketplace, tiktok, whatsapp-status, linkedin, hyperframes
  sunday-distribution/— whatsapp-broadcast
```

### Execution Order (validated)
1. Create all directories with `mkdir -p`
2. Write ALL text content first (captions, scripts, articles, marketplace listings)
3. Generate ALL images via `image_gen` tool (returns URLs)
4. Batch download all images via `curl -sL "<url>" -o "<path>"`
5. Copy images to secondary locations (tiktok/concept.png, linkedin/header-image.png, marketplace/image.png)
6. Write Manim scripts (Akoma days) and render with `manim -ql`
7. Write Hyperframes HTML compositions (2Real days)
8. Write MASTER_PLAN.md
9. Update sent-log.md

### Image Generation Pattern
- **Akoma (educational graphics):** `aspect_ratio="square"` for IG, `"landscape"` for FB/LinkedIn, `"portrait"` for WA Status
- **2Real (Taiwah + product):** Full character anchor in every prompt, negative prompt always included
- **LinkedIn headers:** `aspect_ratio="landscape"` (16:9)
- **WA Status/TikTok:** `aspect_ratio="portrait"` (9:16)
- **FB/IG posts:** `aspect_ratio="square"` (1:1)

### Manim Render Commands
```bash
# Draft (fast, for verification)
manim -ql script.py Scene1 Scene2 Scene3 Scene4

# Production (final quality)
manim -qh script.py Scene1 Scene2 Scene3 Scene4

# Stitch scenes
cat > concat.txt << 'EOF'
file 'media/videos/script/480p15/Scene1.mp4'
file 'media/videos/script/480p15/Scene2.mp4'
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy output.mp4
```

### Hyperframes Render Commands
```bash
cd project-directory/
npx hyperframes lint    # Always lint first
npx hyperframes render  # Then render
```

### Asset Count (May 25-31, 2026 week)
- 22 images generated (xAI grok-imagine-image)
- 28 captions/scripts
- 3 LinkedIn articles (800-1200 words each)
- 4 LinkedIn short posts (150-300 words each)
- 2 Manim video scripts (4 scenes each, 8 MP4s rendered)
- 3 Hyperframes HTML compositions (render-ready)
- 2 Marketplace listings
- 1 WA broadcast message
- Total: 201 files

### Key Learnings
- `image_gen` returns URLs — must `curl` to download
- Manim `-ql` renders in ~2-5 min per scene on Windows
- Hyperframes skill was NOT available — compositions written but not rendered
- xAI grok-imagine-image works reliably for both character and graphic generation
- Batch `mkdir -p` with `&&` chains works well for directory creation
- Copy pattern: generate once, copy to tiktok/concept.png and linkedin/header-image.png

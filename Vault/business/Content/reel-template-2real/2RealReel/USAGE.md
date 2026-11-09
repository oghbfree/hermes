# 2Real Reel Template — reusable HyperFrames composition

Build a branded 2Real 9:16 reel from **one script + one render command**. Captions,
price pill, and CTA pill are all baked in deterministically — no hand-written
`ffmpeg drawtext` per reel.

**Location:** `Vault/business/Content/reel-template-2real/2RealReel/`
**Verified:** `npx hyperframes check` PASS (0 errors) · draft render test OK (20.4s,
1080×1920, 30fps, h264+aac).

## What it does
- Places **5 full-frame scene clips** back-to-back (single continuous world — NO PiP,
  matching the 2Real V3 doctrine).
- Overlays **Poppins narration caption** on each beat (one per moment, compact pill).
- Shows a **green price pill** (detail line + big digits) then a **CTA pill**
  (`WhatsApp 0204252252`), both animated.
- Muxes the **VO** track (separate `<audio>`; video clips stay muted).

## Per-reel usage — ONE command

1. Drop this reel's 5 scene clips + VO + Poppins fonts into `assets/`
   (or point the variables at their real paths — see Variables below).
2. Render, overriding the content variables:
   ```bash
   cd "Vault/business/Content/reel-template-2real/2RealReel"
   npx hyperframes render --quality looks --output reel4.mp4 \
     --variables '{
       "clip1": "assets/r4s1.mp4", ... fi ve clip paths ...,
       "vo": "assets/r4vo.m4a",
       "caption1": "Fix it yourself in 10 minutes.",
       "priceText": "GH₵ 200",
       "detailLine": "Stanley Staple Gun 704400 - UK pre-owned, tested working",
       "cta": "Message me on WhatsApp 0204252252"
     }'
   ```
3. Verify: `ffprobe -v error -show_format -show_streams reel4.mp4`
   (expect 1080×1920, ~duration ≈ VO length, h264+aac).

## Variables
| id | type | default | meaning |
|----|------|---------|---------|
| clip1..clip5 | string | assets/clipN.mp4 | the 5 full-frame scene clips |
| vo | string | assets/vo.m4a | voiceover audio (aac/m4a recommended) |
| caption1..4 | string | demo lines | narration captions per beat |
| priceText | string | `1,300 cedis` | big digits on the green pill |
| detailLine | string | DeWalt... | small line above the price digits |
| cta | string | Msg...0204252252 | bottom CTA pill |

> Note: clip/video `data-duration` and pill `data-start` are **hardcoded** to the
> Reel-3 timeline (4.6/4.1/2.4/3.7/5.6s; price @15s, CTA @17.6s). To change beat
> lengths for a different script, edit those in `index.html` (root `data-duration`
> + each `data-duration`/`data-start`) BEFORE rendering — same as the picture-cut-to-VO
> rule. A future improvement could expose them as variables too.

## Cheap vs full
- `--quality draft` = fast iteration.
- `--quality looks` = first real encode (the 2Real standard).
- `--quality delivery` = final.
- `npx hyperframes preview --background` = Studio preview before render.

## Rules honoured from the V3 doctrine
- One continuous world, no PiP/avatar-rectangle (all full-frame clips). ✅
- Price/CTA as **digit pills, not spoken** (no garbled-price risk). ✅
- Poppins captions, one per moment. ✅
- CTA `0204252252` single source. ✅
- Deterministic render (no clocks/random; `gsap paused` timeline). ✅
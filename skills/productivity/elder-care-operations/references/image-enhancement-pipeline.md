# Image Enhancement Pipeline for Scanned Documents

Reusable pipeline for enhancing photographed/scanned book pages, music notation, and text documents.

## When to Use
- Phone-camera photos of book pages that need to be print-ready
- Scanned documents with low contrast or blur
- Music notation pages that need sharpening for readability
- Any document where the source is a photo rather than a flatbed scan

## The Pipeline (PIL, run via system Python)

```python
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

img = Image.open(src_path)

# 1. 2x Lanczos upscaling (best resampling for text/line art)
w, h = img.size
img = img.resize((w * 2, h * 2), Image.LANCZOS)

# 2. Auto contrast (clip 0.5% from each end)
img = ImageOps.autocontrast(img, cutoff=0.5)

# 3. Unsharp mask — THE critical step for crisp text/music
img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=200, threshold=2))

# 4. Contrast boost
img = ImageEnhance.Contrast(img).enhance(1.15)

# 5. Final sharpness
img = ImageEnhance.Sharpness(img).enhance(1.3)

img.save(out_path, "PNG")
```

## Critical: Use System Python, Not Sandbox

The execute_code sandbox venv does NOT have PIL. Run via system Python:
`python /c/Users/User/.hermes/workspace/script.py`

## Quality Expectations

| Source Quality | After Enhancement | Print Ready? |
|---|---|---|
| Flatbed scan 600 DPI | 9-10/10 | Yes |
| Phone photo, good light, flat | 7-8/10 | Marginal for music |
| Phone photo, angled, shadows | 5-7/10 | No — rescan needed |
| Phone photo of music notation | 6-7/10 | Use MuseScore re-engrave |

## For Music Notation

Enhancement CANNOT add detail that isn't in the source. For organist-quality output:
1. Best: Re-engrave in MuseScore (free)
2. Good: Flatbed scan at 1200 DPI
3. OK: Enhanced phone photo — readable but not performance-quality
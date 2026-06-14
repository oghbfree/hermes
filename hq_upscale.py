"""
High-quality upscaling for book pages using Lanczos resampling + sharpening.
Optimized for text and music notation.
"""
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import os

CACHE = r"C:\Users\User\.hermes\cache\images"
OUT = r"C:\Users\User\.hermes\workspace"

pages = [
    ("img_da8a6200fcda.jpg", "page_contents_portrait"),
    ("img_7c90133ac951.jpg", "page_biography_dad"),
    ("img_97f80585341f.jpg", "page_short_life_history"),
    ("img_9d27a9fe6348.jpg", "page_preface_acknowledgements"),
]

for fname, label in pages:
    src = os.path.join(CACHE, fname)
    img = Image.open(src)
    w, h = img.size
    
    # 2x Lanczos upscaling — excellent for text and line art
    img_up = img.resize((w * 2, h * 2), Image.LANCZOS)
    
    # Sharpen for crisp text
    img_up = img_up.filter(ImageFilter.UnsharpMask(radius=1.2, percent=200, threshold=2))
    
    # Auto contrast
    img_up = ImageOps.autocontrast(img_up, cutoff=0.5)
    
    # Slight contrast boost
    img_up = ImageEnhance.Contrast(img_up).enhance(1.15)
    
    # Final sharpness
    img_up = ImageEnhance.Sharpness(img_up).enhance(1.3)
    
    out_path = os.path.join(OUT, f"hq_{label}.png")
    img_up.save(out_path, "PNG")
    print(f"{label}: {w}x{h} -> {w*2}x{h*2} | {os.path.getsize(out_path):,} bytes")

print("\nDone.")

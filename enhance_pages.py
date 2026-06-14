"""
Enhance scanned book pages for better text/music readability.
Uses PIL for image processing + tries Real-ESRGAN for AI upscaling.
"""
from PIL import Image, ImageFilter, ImageEnhance
import os

CACHE = r"C:\Users\User\.hermes\cache\images"
OUT = r"C:\Users\User\.hermes\workspace"
os.makedirs(OUT, exist_ok=True)

pages = [
    ("img_da8a6200fcda.jpg", "page_contents_portrait"),
    ("img_7c90133ac951.jpg", "page_biography_dad"),
    ("img_97f80585341f.jpg", "page_short_life_history"),
    ("img_9d27a9fe6348.jpg", "page_preface_acknowledgements"),
]

for fname, label in pages:
    src = os.path.join(CACHE, fname)
    if not os.path.exists(src):
        print(f"MISSING: {src}")
        continue
    
    img = Image.open(src)
    w, h = img.size
    print(f"\n{label}: {w}x{h}")
    
    # Step 1: Auto-contrast
    from PIL import ImageOps
    img_enhanced = ImageOps.autocontrast(img, cutoff=1)
    
    # Step 2: Sharpen
    img_enhanced = img_enhanced.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=3))
    
    # Step 3: Increase contrast slightly
    enhancer = ImageEnhance.Contrast(img_enhanced)
    img_enhanced = enhancer.enhance(1.2)
    
    # Step 4: Increase sharpness
    enhancer2 = ImageEnhance.Sharpness(img_enhanced)
    img_enhanced = enhancer2.enhance(1.5)
    
    # Save enhanced version
    out_path = os.path.join(OUT, f"enhanced_{label}.png")
    img_enhanced.save(out_path, "PNG", quality=95)
    print(f"  Saved: {out_path} ({os.path.getsize(out_path):,} bytes)")

print("\nDone. Enhanced versions saved.")

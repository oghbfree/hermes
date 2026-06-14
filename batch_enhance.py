"""
Batch enhance hymnal book pages only.
Process the specific pages sent for the Robertsville Hymnal project.
"""
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import os

CACHE = r"C:\Users\User\.hermes\cache\images"
OUT = r"C:\Users\User\.hermes\workspace\book_pages_enhanced"
os.makedirs(OUT, exist_ok=True)

# The hymnal page images (based on what was sent)
pages = [
    # Front matter
    ("img_da8a6200fcda.jpg", "01_contents_portrait"),
    ("img_7c90133ac951.jpg", "02_biography_dad"),
    ("img_97f80585341f.jpg", "03_short_life_history"),
    ("img_9d27a9fe6348.jpg", "04_preface_acknowledgements"),
    ("img_8ebf3100e5ac.jpg", "05_life_history_dad"),
    ("img_8449c07eacbd.jpg", "06_copyright_warning"),
    ("img_d0bb8381a084.jpg", "07_table_of_contents"),
    # Music pages
    ("img_99ae22e3d063.jpg", "08_hymns_03_04"),
    ("img_5f6018844516.jpg", "09_hymns_05_06"),
    ("img_685091129e23.jpg", "10_hymns_07_08"),
    ("img_82dda36bc3b6.jpg", "11_hymns_09_10"),
    ("img_20909fc64b5b.jpg", "12_hymns_11_12"),
    ("img_da7e9350e084.jpg", "13_hymns_13_14"),
    ("img_ec001b699793.jpg", "14_hymns_15_16"),
    ("img_0d63b04a6f09.jpg", "15_hymns_17_18"),
    ("img_299a8747fbf2.jpg", "16_hymns_19_20"),
    ("img_f033d84d3e17.jpg", "17_hymns_21_22"),
    ("img_51c971ae0eaf.jpg", "18_hymns_23_24"),
    ("img_f31f128494ee.jpg", "19_hymns_25_26"),
    ("img_2aa539b1b157.jpg", "20_hymns_27_28"),
    ("img_991f795be259.jpg", "21_hymns_29_30"),
    ("img_546f62fbebb1.jpg", "22_hymns_31_32"),
    ("img_929ff2681d69.jpg", "23_hymns_33_34"),
    ("img_7f0d9e91e8b5.jpg", "24_hymns_35_36"),
    ("img_528f5b1fd178.jpg", "25_hymns_37_38"),
    ("img_786f700a01c8.jpg", "26_hymns_39_40"),
    ("img_05e12755b44c.jpg", "27_hymn_41"),
    ("img_8b06efe40764.jpg", "28_compositions_list"),
    ("img_e59ad2c58110.jpg", "29_hymns_42_43"),
    ("img_c3945a91c16a.jpg", "30_hymns_44_45"),
    ("img_0052e3d46fd7.jpg", "31_hymns_46_47"),
    ("img_47ecdf8fde5b.jpg", "32_hymns_48_49"),
    ("img_bd91a708135f.jpg", "33_hymns_50_51"),
]

processed = 0
skipped = 0

for fname, label in pages:
    src = os.path.join(CACHE, fname)
    if not os.path.exists(src):
        print(f"  SKIP (not found): {fname}")
        skipped += 1
        continue
    
    img = Image.open(src)
    w, h = img.size
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 2x Lanczos upscaling
    img_up = img.resize((w * 2, h * 2), Image.LANCZOS)
    
    # Auto contrast
    img_up = ImageOps.autocontrast(img_up, cutoff=0.5)
    
    # Unsharp mask for crisp text and music notation
    img_up = img_up.filter(ImageFilter.UnsharpMask(radius=1.2, percent=200, threshold=2))
    
    # Contrast boost
    img_up = ImageEnhance.Contrast(img_up).enhance(1.15)
    
    # Final sharpness
    img_up = ImageEnhance.Sharpness(img_up).enhance(1.3)
    
    out_path = os.path.join(OUT, f"{label}.png")
    img_up.save(out_path, "PNG")
    
    processed += 1
    size_kb = os.path.getsize(out_path) // 1024
    print(f"  [{processed}] {label}: {w}x{h} -> {w*2}x{h*2} ({size_kb}KB)")

print(f"\nDone. {processed} pages enhanced, {skipped} skipped.")
print(f"Output: {OUT}")

"""
Generate social media graphic for Robertsville Hymnal.
1080x1080px square format for Instagram/Facebook.
"""
from PIL import Image, ImageDraw, ImageFont
import os

WORKSPACE = r"C:\Users\User\.hermes\workspace"
SOCIAL_PATH = os.path.join(WORKSPACE, "robertsville-hymnal-social.png")

# === COLORS ===
GREEN_DARK = (26, 58, 42)
GREEN_MID = (45, 90, 63)
GREEN_BTN = (45, 106, 79)
GOLD = (201, 168, 76)
BEIGE = (245, 240, 225)
WHITE = (255, 255, 255)
TEXT_DARK = (26, 26, 26)

W, H = 1080, 1080
img = Image.new("RGB", (W, H), BEIGE)
draw = ImageDraw.Draw(img)

# === FONT LOADING ===
def get_font(name, size):
    """Try to load a nice font, fall back to default."""
    font_paths = [
        f"C:/Windows/Fonts/{name}.ttf",
        f"C:/Windows/Fonts/{name}.TTF",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

# Try to find good fonts
def find_font(keyword):
    import glob
    matches = glob.glob(f"C:/Windows/Fonts/*{keyword}*.ttf") + glob.glob(f"C:/Windows/Fonts/*{keyword}*.TTF")
    return matches[0] if matches else None

georgia = find_font("georgia")
georgia_bold = find_font("georgiab")
georgia_italic = find_font("georgiai")
arial = find_font("arial")
arial_bold = find_font("arialbd")
times = find_font("times")
times_bold = find_font("timesbd")

def font_or_default(path, size):
    if path:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass
    return ImageFont.load_default()

# Header fonts
font_now = font_or_default(arial_bold, 22)
font_the_new = font_or_default(arial, 28)
font_title = font_or_default(georgia_bold, 90)
font_hymnal = font_or_default(georgia_italic if georgia_italic else georgia, 48)
font_tagline = font_or_default(georgia_italic if georgia_italic else georgia, 24)
font_label = font_or_default(arial_bold, 18)
font_btn = font_or_default(arial_bold, 22)
font_body = font_or_default(georgia, 22)
font_quote = font_or_default(georgia_italic if georgia_italic else georgia, 22)
font_credit = font_or_default(arial_bold, 16)
font_price = font_or_default(georgia_bold, 56)
font_price_sub = font_or_default(georgia, 24)
font_isbn = font_or_default(arial, 16)
font_contact_label = font_or_default(arial_bold, 16)
font_contact_val = font_or_default(arial, 18)
font_footer = font_or_default(arial_bold, 14)
font_footer_tag = font_or_default(georgia_italic if georgia_italic else georgia, 18)
font_compositions = font_or_default(arial_bold, 20)
font_section_title = font_or_default(arial_bold, 18)

# === DRAW HEADER ===
header_h = 380
draw.rectangle([0, 0, W, header_h], fill=GREEN_DARK)

# Subtle grid
for gx in range(0, W, 20):
    draw.line([(gx, 0), (gx, header_h)], fill=(255, 255, 255, 8), width=1)
for gy in range(0, header_h, 20):
    draw.line([(0, gy), (W, gy)], fill=(255, 255, 255, 8), width=1)

y = 40

# NOW AVAILABLE
draw.text((W // 2, y), "★  NOW AVAILABLE  ★", fill=WHITE, font=font_now, anchor="mt")
y += 40

# THE NEW
draw.text((W // 2, y), "THE NEW", fill=WHITE, font=font_the_new, anchor="mt")
y += 50

# ROBERTSVILLE
draw.text((W // 2, y), "Robertsville", fill=WHITE, font=font_title, anchor="mt")
y += 100

# HYMNAL
draw.text((W // 2, y), "Hymnal", fill=GOLD, font=font_hymnal, anchor="mt")
y += 65

# Gold line
line_w = 160
draw.line([(W // 2 - line_w // 2, y), (W // 2 + line_w // 2, y)], fill=GOLD, width=3)
y += 25

# Tagline
draw.text((W // 2, y), "A masterful collection of sacred music — 61 compositions", fill=(255, 255, 255, 200), font=font_tagline, anchor="mt")
y += 32
draw.text((W // 2, y), "honouring a century of Ghanaian Methodist heritage", fill=(255, 255, 255, 200), font=font_tagline, anchor="mt")

# === MAIN CONTENT ===
y = header_h + 30

# FEATURING
draw.text((W // 2, y), "FEATURING", fill=GREEN_MID, font=font_label, anchor="mt")
y += 35

# Buttons
btn_labels = ["Kofibon", "Da Yie", "Afrinbyia Pa!"]
btn_ws = [180, 140, 200]
btn_h = 45
total_w = sum(btn_ws) + 20 * 2
bx = (W - total_w) // 2
for i, label in enumerate(btn_labels):
    bw = btn_ws[i]
    draw.rounded_rectangle([bx, y, bx + bw, y + btn_h], radius=8, fill=GREEN_BTN)
    draw.text((bx + bw // 2, y + btn_h // 2), label, fill=WHITE, font=font_btn, anchor="mm")
    bx += bw + 20

y += btn_h + 20

# Compositions box
box_w, box_h = 280, 35
bx = (W - box_w) // 2
draw.rounded_rectangle([bx, y, bx + box_w, y + box_h], radius=6, outline=GREEN_MID, width=2)
draw.text((W // 2, y + box_h // 2), "46 + 15 COMPOSITIONS", fill=GREEN_MID, font=font_compositions, anchor="mm")

y += box_h + 30

# Divider
draw.line([(60, y), (W - 60, y)], fill=(26, 58, 42, 30), width=1)
y += 25

# TWO COLUMNS
col_w = (W - 120) // 2 - 15
cx1 = 60
cx2 = W // 2 + 15

# Column 1: The Artistry
draw.text((cx1 + col_w // 2, y), "♪  THE ARTISTRY", fill=(180, 140, 60), font=font_section_title, anchor="mt")
y2 = y + 30
artistry_lines = [
    "Oman G. Blankson, A.Mus. V.C.M.",
    "(London) — Former Organist &",
    "Choirmaster, Winneba Methodist",
    "Church, Ghana. First published 1949;",
    "16 compositions adopted into the",
    "New Methodist Hymn Book."
]
for line in artistry_lines:
    draw.text((cx1 + col_w // 2, y2), line, fill=TEXT_DARK, font=font_body, anchor="mt")
    y2 += 28

col1_bottom = y2

# Column 2: The Edition
y3 = y + 30
edition_lines = [
    "Compiled, reviewed, edited &",
    "published by Professor Dr Sir",
    "Robert A. Herbert-Blankson,",
    "MBA., PhD., ABSC., ACL —",
    "ensuring the highest standards",
    "of theological integrity."
]
draw.text((cx2 + col_w // 2, y), "📖  THE EDITION", fill=(180, 140, 60), font=font_section_title, anchor="mt")
for line in edition_lines:
    draw.text((cx2 + col_w // 2, y3), line, fill=TEXT_DARK, font=font_body, anchor="mt")
    y3 += 28

col2_bottom = y3
y = max(col1_bottom, col2_bottom) + 25

# QUOTE BOX
quote_h = 130
GREEN_DRAW = GREEN_DARK
draw.rounded_rectangle([40, y, W - 40, y + quote_h], radius=10, fill=GREEN_DRAW)

# Grid on quote
for gx in range(40, W - 40, 20):
    draw.line([(gx, y), (gx, y + quote_h)], fill=(255, 255, 255, 6), width=1)
for gy in range(y, y + quote_h, 20):
    draw.line([(40, gy), (W - 40, gy)], fill=(255, 255, 255, 6), width=1)

quote_lines = [
    "\"This isn't just a hymnal — it is a legacy of",
    "faith, family, and professional excellence",
    "spanning over seven decades of sacred music",
    "in the Methodist tradition.\""
]
qy = y + 20
for line in quote_lines:
    draw.text((W // 2, qy), line, fill=(255, 255, 255, 220), font=font_quote, anchor="mt")
    qy += 28

draw.text((W // 2, y + quote_h - 18), "PUBLISHED 2026  ·  LAST & FINAL EDITION", fill=GOLD, font=font_credit, anchor="mt")

y += quote_h + 30

# PURCHASE
draw.text((W // 2, y), "★  SECURE YOUR COPY  ★", fill=GREEN_MID, font=font_label, anchor="mt")
y += 35

draw.text((W // 2 - 30, y), "£9.99", fill=GREEN_DARK, font=font_price, anchor="mt")
draw.text((W // 2 + 100, y + 15), "per copy", fill=TEXT_DARK, font=font_price_sub, anchor="mt")
y += 65

draw.text((W // 2, y), "ISBN 978-1-918465-47-1", fill=(136, 136, 136), font=font_isbn, anchor="mt")
y += 35

# Contact info
contacts = [
    ("ADDRESS", "40 Archdale Road, East Dulwich\nLondon SE22 9HJ"),
    ("WHATSAPP", "+44 7983 254 695"),
    ("EMAIL", "profblankson34@gmail.com"),
]
cw = W // 3
for i, (label, value) in enumerate(contacts):
    cx = i * cw + cw // 2
    draw.text((cx, y), label, fill=GREEN_MID, font=font_contact_label, anchor="mt")
    y2 = y + 25
    for j, vl in enumerate(value.split('\n')):
        draw.text((cx, y2 + j * 22), vl, fill=TEXT_DARK, font=font_contact_val, anchor="mt")

y += 80

# === FOOTER ===
footer_h = 60
draw.rectangle([0, H - footer_h, W, H], fill=GREEN_DARK)
draw.text((W // 2, H - footer_h + 15), "DESIGN & PRINT BY CATFORD PRINT CENTRE", fill=WHITE, font=font_footer, anchor="mt")
draw.text((W // 2, H - footer_h + 38), "Bring the spirit of Robertsville to your church or home", fill=(255, 255, 255, 150), font=font_footer_tag, anchor="mt")

# Save
img.save(SOCIAL_PATH, "PNG", quality=95)
print(f"Social media graphic saved: {SOCIAL_PATH}")
print(f"Size: {os.path.getsize(SOCIAL_PATH):,} bytes")
print(f"Dimensions: {W}x{H}")

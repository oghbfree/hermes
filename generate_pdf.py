"""
Generate PDF and social media graphic for Robertsville Hymnal flyer.
Uses reportlab for PDF and Pillow for social media image.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont
import os

# === COLORS ===
GREEN_DARK = HexColor("#1a3a2a")
GREEN_MID = HexColor("#2d5a3f")
GREEN_BTN = HexColor("#2d6a4f")
GOLD = HexColor("#c9a84c")
BEIGE = HexColor("#f5f0e1")
WHITE = HexColor("#ffffff")
TEXT_DARK = HexColor("#1a1a1a")

# === PATHS ===
WORKSPACE = r"C:\Users\User\.hermes\workspace"
PDF_PATH = os.path.join(WORKSPACE, "robertsville-hymnal-flyer.pdf")
SOCIAL_PATH = os.path.join(WORKSPACE, "robertsville-hymnal-social.png")

# Try to register nice fonts
FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"

# Check for system fonts that might be nicer
import glob
font_dirs = [
    "C:/Windows/Fonts",
]
available_fonts = []
for d in font_dirs:
    if os.path.exists(d):
        available_fonts.extend(glob.glob(os.path.join(d, "*.ttf")))

# Look for preferred fonts
georgia_regular = None
georgia_bold = None
georgia_italic = None
times_regular = None
times_bold = None

for f in available_fonts:
    fl = f.lower()
    if "georgia" in fl and "bold" not in fl and "italic" not in fl:
        georgia_regular = f
    elif "georgia" in fl and "bold" in fl and "italic" not in fl:
        georgia_bold = f
    elif "georgia" in fl and "italic" in fl:
        georgia_italic = f
    elif "times" in fl and "bold" not in fl and "italic" not in fl and "roman" in fl:
        times_regular = f
    elif "times" in fl and "bold" in fl:
        times_bold = f

# Register Georgia if available
if georgia_regular and georgia_bold:
    try:
        pdfmetrics.registerFont(TTFont('Georgia', georgia_regular))
        pdfmetrics.registerFont(TTFont('Georgia-Bold', georgia_bold))
        if georgia_italic:
            pdfmetrics.registerFont(TTFont('Georgia-Italic', georgia_italic))
            FONT_ITALIC = 'Georgia-Italic'
        FONT_REGULAR = 'Georgia'
        FONT_BOLD = 'Georgia-Bold'
        print("Using Georgia font")
    except Exception as e:
        print(f"Font registration failed: {e}")

# =============================================
# PDF GENERATION
# =============================================
def create_pdf():
    page_w, page_h = A4  # 210mm x 297mm
    c = canvas.Canvas(PDF_PATH, pagesize=A4)
    
    # Scale factor: design was 612px wide, A4 is ~595pt
    # We'll work in points (1pt = 1/72 inch)
    
    margin = 20 * mm
    content_w = page_w - 2 * margin
    
    y = page_h  # Start from top
    
    # --- HEADER ---
    header_h = 140 * mm
    y -= header_h
    c.setFillColor(GREEN_DARK)
    c.rect(margin, y, content_w, header_h, fill=1, stroke=0)
    
    # Grid pattern overlay (subtle)
    c.setStrokeColor(HexColor("#ffffff"))
    c.setLineWidth(0.2)
    for gx in range(int(margin), int(margin + content_w), 10):
        c.line(gx, y, gx, y + header_h)
    for gy in range(int(y), int(y + header_h), 10):
        c.line(margin, gy, margin + content_w, gy)
    
    # Header text
    text_y = y + header_h - 18 * mm
    
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 8)
    c.drawCentredString(page_w / 2, text_y, "★  NOW AVAILABLE  ★")
    text_y -= 8 * mm
    
    c.setFont(FONT_REGULAR, 11)
    c.drawCentredString(page_w / 2, text_y, "THE NEW")
    text_y -= 12 * mm
    
    c.setFont(FONT_BOLD, 42)
    c.drawCentredString(page_w / 2, text_y, "Robertsville")
    text_y -= 10 * mm
    
    c.setFont(FONT_ITALIC, 20)
    c.setFillColor(GOLD)
    c.drawCentredString(page_w / 2, text_y, "Hymnal")
    text_y -= 8 * mm
    
    # Gold line
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(page_w / 2 - 30 * mm, text_y, page_w / 2 + 30 * mm, text_y)
    text_y -= 7 * mm
    
    c.setFillColor(HexColor("#ffffffcc"))
    c.setFont(FONT_ITALIC, 9)
    c.drawCentredString(page_w / 2, text_y, "A masterful collection of sacred music — 61 compositions")
    text_y -= 4 * mm
    c.drawCentredString(page_w / 2, text_y, "honouring a century of Ghanaian Methodist heritage")
    
    # --- MAIN CONTENT ---
    main_y = y - 4 * mm  # slight overlap
    main_top = main_y
    main_h = y - margin - 30 * mm  # leave room for footer
    
    c.setFillColor(BEIGE)
    c.rect(margin, main_y - main_h, content_w, main_h, fill=1, stroke=0)
    
    my = main_y - 12 * mm
    
    # FEATURING
    c.setFillColor(GREEN_MID)
    c.setFont(FONT_BOLD, 8)
    c.drawCentredString(page_w / 2, my, "FEATURING")
    my -= 8 * mm
    
    # Feature buttons
    btn_labels = ["Kofibon", "Da Yie", "Afrinbyia Pa!"]
    btn_total_w = content_w * 0.7
    btn_w = btn_total_w / 3 - 3 * mm
    btn_h = 10 * mm
    btn_start_x = (page_w - btn_total_w) / 2
    
    for i, label in enumerate(btn_labels):
        bx = btn_start_x + i * (btn_w + 3 * mm)
        c.setFillColor(GREEN_BTN)
        c.roundRect(bx, my - btn_h / 2 - 2 * mm, btn_w, btn_h, 3 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 10)
        c.drawCentredString(bx + btn_w / 2, my - 1 * mm, label)
    
    my -= 14 * mm
    
    # Compositions box
    box_w = 50 * mm
    box_h = 7 * mm
    c.setStrokeColor(GREEN_MID)
    c.setLineWidth(1)
    c.setFillColor(BEIGE)
    c.roundRect((page_w - box_w) / 2, my - box_h / 2 - 1 * mm, box_w, box_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(GREEN_MID)
    c.setFont(FONT_BOLD, 9)
    c.drawCentredString(page_w / 2, my - 0.5 * mm, "46 + 15 COMPOSITIONS")
    
    my -= 12 * mm
    
    # Divider
    c.setStrokeColor(HexColor("#1a3a2a20"))
    c.setLineWidth(0.5)
    c.line(margin + 10 * mm, my, margin + content_w - 10 * mm, my)
    my -= 10 * mm
    
    # TWO COLUMNS
    col_w = (content_w - 8 * mm) / 2
    
    # Column 1: The Artistry
    cx1 = margin + 4 * mm
    c.setFillColor(GOLD)
    c.setFont(FONT_BOLD, 8)
    c.drawCentredString(cx1 + col_w / 2, my, "♪  THE ARTISTRY")
    my -= 7 * mm
    
    c.setFillColor(TEXT_DARK)
    c.setFont(FONT_REGULAR, 9)
    artistry_text = [
        "Oman G. Blankson, A.Mus. V.C.M. (London)",
        "— Former Organist & Choirmaster, Winneba",
        "Methodist Church, Ghana. First published",
        "1949; 16 compositions adopted into the",
        "New Methodist Hymn Book."
    ]
    for line in artistry_text:
        c.drawCentredString(cx1 + col_w / 2, my, line)
        my -= 4.5 * mm
    
    col1_bottom = my
    
    # Column 2: The Edition
    cx2 = margin + col_w + 8 * mm
    my2 = main_y - 12 * mm - 22 * mm - 12 * mm - 10 * mm  # reset to same level
    
    # Recalculate: start from the divider
    my2 = main_y - 12 * mm  # top
    my2 -= 8 * mm + 8 * mm + 14 * mm + 12 * mm + 10 * mm  # featuring + buttons + box + divider
    
    c.setFillColor(GOLD)
    c.setFont(FONT_BOLD, 8)
    c.drawCentredString(cx2 + col_w / 2, my2, "📖  THE EDITION")
    my2 -= 7 * mm
    
    c.setFillColor(TEXT_DARK)
    c.setFont(FONT_REGULAR, 9)
    edition_text = [
        "Compiled, reviewed, edited & published",
        "by Professor Dr Sir Robert A.",
        "Herbert-Blankson, MBA., PhD., ABSC.,",
        "ACL — ensuring the highest standards",
        "of theological integrity."
    ]
    for line in edition_text:
        c.drawCentredString(cx2 + col_w / 2, my2, line)
        my2 -= 4.5 * mm
    
    col2_bottom = my2
    my = min(col1_bottom, col2_bottom) - 6 * mm
    
    # QUOTE BOX
    quote_h = 28 * mm
    c.setFillColor(GREEN_DARK)
    c.rect(margin + 4 * mm, my - quote_h, content_w - 8 * mm, quote_h, fill=1, stroke=0)
    
    # Grid on quote
    c.setStrokeColor(HexColor("#ffffff08"))
    c.setLineWidth(0.2)
    for gx in range(int(margin + 4 * mm), int(margin + content_w - 4 * mm), 10):
        c.line(gx, my - quote_h, gx, my)
    for gy in range(int(my - quote_h), int(my), 10):
        c.line(margin + 4 * mm, gy, margin + content_w - 4 * mm, gy)
    
    c.setFillColor(HexColor("#ffffffdd"))
    c.setFont(FONT_ITALIC, 9)
    quote_lines = [
        "\"This isn't just a hymnal — it is a legacy of faith,",
        "family, and professional excellence spanning over",
        "seven decades of sacred music in the Methodist tradition.\""
    ]
    qy = my - 10 * mm
    for line in quote_lines:
        c.drawCentredString(page_w / 2, qy, line)
        qy -= 5 * mm
    
    c.setFillColor(GOLD)
    c.setFont(FONT_BOLD, 7)
    c.drawCentredString(page_w / 2, my - quote_h + 3 * mm, "PUBLISHED 2026  ·  LAST & FINAL EDITION")
    
    my -= quote_h + 8 * mm
    
    # PURCHASE SECTION
    c.setFillColor(GREEN_MID)
    c.setFont(FONT_BOLD, 8)
    c.drawCentredString(page_w / 2, my, "★  SECURE YOUR COPY  ★")
    my -= 10 * mm
    
    c.setFillColor(GREEN_DARK)
    c.setFont(FONT_BOLD, 28)
    c.drawCentredString(page_w / 2, my, "£9.99")
    c.setFont(FONT_REGULAR, 12)
    c.drawCentredString(page_w / 2 + 22 * mm, my, "per copy")
    my -= 6 * mm
    
    c.setFillColor(HexColor("#888888"))
    c.setFont(FONT_REGULAR, 8)
    c.drawCentredString(page_w / 2, my, "ISBN 978-1-918465-47-1")
    my -= 10 * mm
    
    # Contact grid
    contact_y = my
    contacts = [
        ("ADDRESS", "40 Archdale Road\nEast Dulwich\nLondon SE22 9HJ"),
        ("WHATSAPP", "+44 7983 254 695"),
        ("EMAIL", "profblankson34@gmail.com"),
    ]
    cw = content_w / 3
    for i, (label, value) in enumerate(contacts):
        cx = margin + i * cw + cw / 2
        c.setFillColor(GREEN_MID)
        c.setFont(FONT_BOLD, 7)
        c.drawCentredString(cx, contact_y, label)
        contact_y -= 5 * mm
        c.setFillColor(TEXT_DARK)
        c.setFont(FONT_REGULAR, 8.5)
        for j, vl in enumerate(value.split('\n')):
            c.drawCentredString(cx, contact_y - j * 4 * mm, vl)
        contact_y -= len(value.split('\n')) * 4 * mm
    
    # --- FOOTER ---
    footer_h = 18 * mm
    c.setFillColor(GREEN_DARK)
    c.rect(margin, margin, content_w, footer_h, fill=1, stroke=0)
    
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 7)
    c.drawCentredString(page_w / 2, margin + 10 * mm, "DESIGN & PRINT BY CATFORD PRINT CENTRE")
    c.setFillColor(HexColor("#ffffff99"))
    c.setFont(FONT_ITALIC, 8)
    c.drawCentredString(page_w / 2, margin + 4 * mm, "Bring the spirit of Robertsville to your church or home")
    
    c.save()
    print(f"PDF saved: {PDF_PATH}")
    print(f"PDF size: {os.path.getsize(PDF_PATH):,} bytes")

create_pdf()

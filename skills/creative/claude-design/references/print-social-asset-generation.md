# Print & Social Media Asset Generation

## When to Use Code-Based Design

When the user needs printable PDFs or social media graphics (not just HTML mockups), use Python libraries directly instead of relying on HTML-to-PDF conversion.

## PDF Generation with reportlab

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

c = canvas.Canvas("output.pdf", pagesize=A4)
page_w, page_h = A4
c.setFillColor(HexColor("#1a3a2a"))
c.rect(margin, y, content_w, header_h, fill=1, stroke=0)
c.setFillColor(HexColor("#ffffff"))
c.setFont("Helvetica-Bold", 42)
c.drawCentredString(page_w / 2, y, "Title")
c.save()
```

**Install:** `python -m pip install reportlab`

## Social Media Graphics with Pillow

```python
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
img = Image.new("RGB", (W, H), (245, 240, 225))
draw = ImageDraw.Draw(img)
font_title = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 90)
draw.text((W // 2, 100), "Title", fill=(255, 255, 255), font=font_title, anchor="mt")
img.save("output.png", "PNG", quality=95)
```

**Install:** `python -m pip install Pillow`

## Common Social Media Sizes

| Platform | Size (px) |
|---|---|
| Instagram square | 1080×1080 |
| Instagram story | 1080×1920 |
| Facebook post | 1200×630 |
| A4 print PDF | 595×842 pt |

## Workflow
1. Check available fonts on the system first
2. Design in code using reportlab (PDF) or Pillow (PNG)
3. Verify output with vision_analyze
4. Send to user via send_message with MEDIA:/path/to/file

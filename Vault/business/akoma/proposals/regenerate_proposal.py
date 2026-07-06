# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, 
                                  Table, TableStyle, HRFlowable)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

output_path = r"C:\Users\User\.hermes\workspace\memories\business\akoma\proposals\royal-zion-intl-school-integrated.pdf"

# Register a font that supports the Cedi sign
font_paths = [
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\tahoma.ttf",
]
reg_font = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', fp))
            pdfmetrics.registerFont(TTFont('CustomFontBold', fp.replace('arial','arialbd').replace('segoeui','segoeuib').replace('tahoma','tahomabd')))
            reg_font = 'CustomFont'
            break
        except:
            continue

base_font = reg_font if reg_font else 'Helvetica'
base_font_bold = reg_font if reg_font else 'Helvetica-Bold'

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=20*mm,
    leftMargin=20*mm,
    topMargin=20*mm,
    bottomMargin=20*mm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Title'],
    fontSize=18, spaceAfter=2*mm, textColor=HexColor('#1a1a2e'),
    fontName=base_font_bold
)
subtitle_style = ParagraphStyle(
    'CustomSubtitle', parent=styles['Normal'],
    fontSize=11, spaceAfter=6*mm, textColor=HexColor('#555555'), alignment=1,
    fontName=base_font
)
h2_style = ParagraphStyle(
    'CustomH2', parent=styles['Heading2'],
    fontSize=13, spaceBefore=4*mm, spaceAfter=2*mm, textColor=HexColor('#16213e'),
    fontName=base_font_bold
)
body_style = ParagraphStyle(
    'CustomBody', parent=styles['Normal'],
    fontSize=9.5, spaceAfter=2*mm, leading=14,
    fontName=base_font
)
bullet_style = ParagraphStyle(
    'CustomBullet', parent=styles['Normal'],
    fontSize=9.5, spaceAfter=1.5*mm, leftIndent=8*mm, bulletIndent=4*mm, leading=14,
    fontName=base_font
)
bold_style = ParagraphStyle(
    'CustomBold', parent=styles['Normal'],
    fontSize=9.5, spaceAfter=2*mm, leading=14, fontName=base_font_bold
)

accent = HexColor('#0f3460')
light_accent = HexColor('#e8f0fe')

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc'), spaceAfter=3*mm, spaceBefore=2*mm)

story = []

# Use GH\u00a2 for the Cedi sign
cedi = 'GH\u00a2'

story.append(Paragraph(f"<b>AKOMA ROBOTICS \u2014 SCHOOL-INTEGRATED</b><br/>PROGRAM PROPOSAL", title_style))
story.append(Paragraph("Royal Zion International School", subtitle_style))
story.append(hr())

story.append(Paragraph("<b>THE MODEL</b>", h2_style))
story.append(Paragraph(
    "Replace the standalone after-school robotics club with a <b>whole-class program integrated into school fees</b>. "
    "Every student in the enrolled class/year group participates \u2014 no opt-in, no separate payment from parents.",
    body_style
))
story.append(Spacer(1, 2*mm))
story.append(Paragraph("<b>How it works:</b>", bold_style))
story.append(Paragraph(f"1. Royal Zion International School adds <b>{cedi}100/student/term</b> to existing school fees", bullet_style))
story.append(Paragraph("2. Akoma provides: certified facilitator, mBot robotics kits, 12-week curriculum, AI Awareness module, final showcase + certificates", bullet_style))
story.append(Paragraph("3. School provides: classroom space, computer access if available", bullet_style))
story.append(Paragraph("4. Fee is collected through the school's existing billing \u2014 zero admin for parents, zero collection risk for Akoma", bullet_style))

story.append(hr())

story.append(Paragraph("<b>EQUIPMENT LOGISTICS</b>", h2_style))
story.append(Paragraph("\u2022 Akoma does <b>not</b> store equipment on-site between sessions", bullet_style))
story.append(Paragraph("\u2022 All equipment is transported to and from school for each weekly session", bullet_style))
story.append(Paragraph("\u2022 As uptake is assessed, we will evaluate consolidating into a <b>single whole-school day</b> (all classes held in one day)", bullet_style))

story.append(hr())

story.append(Paragraph("<b>WHAT'S INCLUDED (12-WEEK TERM)</b>", h2_style))
story.append(Paragraph("\u2705 One Akoma-certified facilitator, on-site weekly (1-hour sessions)", bullet_style))
story.append(Paragraph("\u2705 mBot robotics kit per pair of students (class set provided and transported by Akoma)", bullet_style))
story.append(Paragraph("\u2705 12-week structured curriculum:", bullet_style))
story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Weeks 1\u20134: Robot assembly, basic coding (mBlock), sensors, obstacle avoidance", bullet_style))
story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Weeks 5\u20138: Line following, remote control, sensor fusion, team project kickoff", bullet_style))
story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;Weeks 9\u201310: AI Awareness module \u2014 \"What is AI?\", smart sensors, machine learning concepts", bullet_style))
story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Weeks 11\u201312: Build & test final projects, showcase day with certificates", bullet_style))
story.append(Paragraph("\u2705 Final Showcase Day for parents and staff", bullet_style))
story.append(Paragraph("\u2705 Participation certificates for all students", bullet_style))

story.append(hr())

story.append(Paragraph("<b>PRICING</b>", h2_style))

price_data = [
    ['Item', 'Cost'],
    ['Per student per term', f'{cedi}100'],
]
price_table = Table(price_data, colWidths=[100*mm, 50*mm])
price_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), base_font_bold),
    ('FONTNAME', (0, 1), (0, 1), base_font_bold),
    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('BACKGROUND', (0, 0), (-1, 0), light_accent),
    ('LINEBELOW', (0, 0), (-1, 0), 0.5, accent),
    ('LINEBELOW', (0, 1), (-1, 1), 0.5, colors.grey),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(price_table)

story.append(hr())

story.append(Paragraph("<b>WHY THIS WORKS FOR ROYAL ZION INTERNATIONAL SCHOOL</b>", h2_style))
story.append(Paragraph(f"\u2022 <b>Previous proposal was {cedi}800/student</b> (after-school, parent-pays-directly) \u2014 too expensive for most families", bullet_style))
story.append(Paragraph(f"\u2022 <b>This is {cedi}100/student/term</b> rolled into fees \u2014 parents barely notice it", bullet_style))
story.append(Paragraph("\u2022 <b>No separate enrollment</b> \u2014 every student in the class participates, no marketing needed each term", bullet_style))
story.append(Paragraph("\u2022 Akoma handles equipment, staffing, and curriculum \u2014 zero lift from school teachers", bullet_style))
story.append(Paragraph("\u2022 Showcase Day gives the school a visible parent-facing event every term", bullet_style))
story.append(Paragraph("\u2022 Positions Royal Zion International School as a STEM-forward institution at minimal cost", bullet_style))

story.append(hr())

story.append(Paragraph("<b>COMPARISON: OLD VS NEW</b>", h2_style))

comp_data = [
    ['Factor', 'Old Proposal', 'New Proposal'],
    ['Price to parent', f'{cedi}800 (one-off)', f'{cedi}100/term (in fees)'],
    ['Who pays', 'Parent directly', 'Via school fees'],
    ['Enrollment', 'Voluntary opt-in', 'Whole class'],
    ['Akoma risk', 'Low enrollment', 'Guaranteed headcount'],
    ['Equipment', 'Akoma provides', 'Akoma provides and transports'],
]
comp_table = Table(comp_data, colWidths=[45*mm, 52*mm, 55*mm])
comp_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), base_font_bold),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), light_accent),
    ('LINEBELOW', (0, 0), (-1, 0), 0.5, accent),
    ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.lightgrey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f8f9fa')]),
]))
story.append(comp_table)

doc.build(story)
print("PDF generated:", output_path)

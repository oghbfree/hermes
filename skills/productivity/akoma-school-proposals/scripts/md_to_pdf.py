import os, re, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def clean(t):
    t = t.strip()
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t)
    t = re.sub(r'\*(.+?)\*', r'\1', t)
    t = t.replace("&", "&amp;")
    return t

def md_table(rows):
    data = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        data.append(cells)
    if len(data) < 2:
        return None
    W = A4[0] - 40 * mm
    col_count = len(data[0])
    col_w = W / col_count
    t = Table(data, colWidths=[col_w] * col_count, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0f3460")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7f9fc"), HexColor("#ffffff")]),
        ("GRID",       (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",(0, 0), (-1, -1), 6),
        ("RIGHTPADDING",(0,0), (-1, -1), 6),
    ]))
    return t

def convert(md_path, pdf_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    margin = 20 * mm
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=margin, rightMargin=margin,
        topMargin=margin, bottomMargin=margin,
        title=os.path.basename(pdf_path),
        author="Akoma Robotics"
    )

    s = getSampleStyleSheet()
    title_s = ParagraphStyle("Title", parent=s["Title"], fontSize=18, leading=22,
                            spaceAfter=4, textColor=HexColor("#1a1a2e"))
    h1_s = ParagraphStyle("H1", parent=s["Heading1"], fontSize=14, leading=18,
                           spaceBefore=14, spaceAfter=4, textColor=HexColor("#0f3460"))
    body_s = ParagraphStyle("Body", parent=s["Normal"], fontSize=10, leading=14,
                             spaceAfter=4, textColor=HexColor("#222222"))
    bullet_s = ParagraphStyle("Bullet", parent=s["Normal"], fontSize=10, leading=14,
                                leftIndent=12, spaceAfter=2, bulletIndent=0,
                                textColor=HexColor("#333333"))

    flow = []
    i = 0
    table_rows = []

    while i < len(lines):
        raw = lines[i].rstrip()
        if raw.strip() == "":
            if table_rows:
                t = md_table(table_rows)
                if t:
                    flow.append(Spacer(1, 4*mm))
                    flow.append(t)
                    flow.append(Spacer(1, 4*mm))
                table_rows = []
            i += 1; continue

        if re.match(r'^-{3,}$', raw.strip()):
            if table_rows:
                t = md_table(table_rows)
                if t: flow.append(t)
                table_rows = []
            flow.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#cccccc"),
                         spaceBefore=4*mm, spaceAfter=4*mm))
            i += 1; continue

        m = re.match(r'^(#{1,3})\s+(.*)', raw)
        if m:
            if table_rows:
                t = md_table(table_rows)
                if t: flow.append(t)
                table_rows = []
            level = len(m.group(1))
            text = clean(m.group(2))
            if level == 1:
                flow.append(Spacer(1, 2*mm))
                flow.append(Paragraph(text, title_s))
                flow.append(HRFlowable(width="100%", thickness=1.2, color=HexColor("#0f3460"),
                             spaceAfter=4*mm))
            else:
                flow.append(Paragraph(text, h1_s))
            i += 1; continue

        if raw.strip().startswith("|"):
            table_rows.append(raw)
            i += 1; continue

        m = re.match(r'^[-•]\s+(.*)', raw)
        if m:
            flow.append(Paragraph("• " + clean(m.group(1)), bullet_s))
            i += 1; continue

        m = re.match(r'^\d+\.\s+(.*)', raw)
        if m:
            flow.append(Paragraph(clean(m.group(1)), bullet_s))
            i += 1; continue

        m = re.match(r'^\*\*(.+?)\*\*\s*(.*)', raw)
        if m:
            flow.append(Paragraph(f"<b>{clean(m.group(1))}</b> {clean(m.group(2))}", body_s))
            i += 1; continue

        text = clean(raw)
        if text:
            flow.append(Paragraph(text, body_s))
        i += 1

    if table_rows:
        t = md_table(table_rows)
        if t:
            flow.append(Spacer(1, 4*mm))
            flow.append(t)

    doc.build(flow)
    return pdf_path

if __name__ == "__main__":
    md = sys.argv[1] if len(sys.argv) > 1 else None
    pdf = sys.argv[2] if len(sys.argv) > 2 else None
    if not md or not pdf:
        print("Usage: python md_to_pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    convert(md, pdf)
    print(f"PDF: {pdf}")

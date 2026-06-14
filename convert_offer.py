import fitz, os, re

doc = fitz.open()
PW, PH = 595, 842
M = 36
CW = PW - 2 * M
FS = 9   # base font size
LH = FS + 2  # line height ~11

with open(r'C:\Users\User\.hermes\workspace\skills\productivity\elder-care-operations\templates\employment-offer-stephanie.md', 'r', encoding='utf-8') as f:
    raw = f.read()

# Strip YAML frontmatter
lines = raw.split('\n')
clean, skip = [], False
for line in lines:
    if line.strip() == '---':
        skip = not skip; continue
    if not skip: clean.append(line)
lines = clean

def new_page():
    global page, y
    page = doc.new_page(width=PW, height=PH)
    y = M

page = doc.new_page(width=PW, height=PH)
y = M

def tw(t, fn, sz): return fitz.get_text_length(t, fontname=fn, fontsize=sz)
def spw(sz): return tw(' ', 'helvetica', sz)

def chk(n):
    global y
    if y + n > PH - M: new_page()

def wrap(t, fn, sz, mw):
    words = t.split()
    out, cur, sw = [], '', spw(sz)
    for w in words:
        test = (cur + ' ' + w).strip() if cur else w
        if tw(test, fn, sz) <= mw: cur = test
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out or ['']

def rpara(text, sz=FS, bold=False, indent=0, bc=None):
    """Render word-wrapped paragraph with inline **bold**."""
    global y
    fn = 'helvetica-bold' if bold else 'helvetica'
    mw = CW - indent
    if bc:
        page.insert_text((M + indent - 10, y), bc, fontname='helvetica', fontsize=sz)
    # parse **bold** inline
    words = []
    s, ib = text, False
    while '**' in s:
        i = s.index('**')
        if i:
            for w in s[:i].split(): words.append((w, ib))
        ib = not ib; s = s[i+2:]
    if s:
        for w in s.split(): words.append((w, ib))
    if not words: return
    sw = spw(sz)
    cw, first = [], True
    for w, wb in words:
        ww = tw(w, 'helvetica-bold' if wb else 'helvetica', sz)
        if cw and sum(tw(x, 'helvetica-bold' if xb else 'helvetica', sz) for x, xb in cw) + len(cw)*sw + ww > mw:
            chk(LH); x = M + indent
            for lw, lb in cw:
                fn2 = 'helvetica-bold' if lb else 'helvetica'
                page.insert_text((x, y), lw, fontname=fn2, fontsize=sz)
                x += tw(lw, fn2, sz) + sw
            y += LH; cw = [(w, wb)]; first = False
        else:
            cw.append((w, wb))
    if cw:
        chk(LH); x = M + indent
        for lw, lb in cw:
            fn2 = 'helvetica-bold' if lb else 'helvetica'
            page.insert_text((x, y), lw, fontname=fn2, fontsize=sz)
            x += tw(lw, fn2, sz) + sw
        y += LH

def rtable(tbl_lines):
    global y
    rows = [[c.strip() for c in tl.strip().split('|')[1:-1]] for tl in tbl_lines]
    if not rows: return
    nc = max(len(r) for r in rows)
    cw = CW / nc; fs = 7.5; pad = 4; lsp = fs + 2
    rhs = []
    for ri, row in enumerate(rows):
        if ri == 1: rhs.append(1); continue
        ml = 1
        for ci, cell in enumerate(row):
            if ci >= nc: break
            fn = 'helvetica-bold' if ri == 0 else 'helvetica'
            ml = max(ml, len(wrap(cell, fn, fs, cw - pad*2)))
        rhs.append(ml * lsp + pad*2)
    total = sum(rhs) + 8
    chk(total)
    cy = y
    for ri, row in enumerate(rows):
        if ri == 1:
            page.draw_line((M, cy), (PW-M, cy), color=(0.7,0.7,0.7), width=0.3); cy += 1; continue
        cx = M; rh = rhs[ri]
        for ci, cell in enumerate(row):
            if ci >= nc: break
            bold = ri == 0; fn = 'helvetica-bold' if bold else 'helvetica'
            if ri == 0: page.draw_rect((cx, cy, cx+cw, cy+rh), color=None, fill=(0.92,0.92,0.95))
            for li, line in enumerate(wrap(cell, fn, fs, cw-pad*2)):
                page.insert_text((cx+pad, cy+pad+fs+li*lsp), line, fontname=fn, fontsize=fs)
            page.draw_rect((cx, cy, cx+cw, cy+rh), color=(0.5,0.5,0.5), width=0.3)
            cx += cw
        cy += rh
    y = cy + 6

# ── Main ──
i = 0
while i < len(lines):
    line = lines[i]
    if not line.strip(): y += 2; i += 1; continue
    if line.strip() == '---':
        chk(8); page.draw_line((M, y), (PW-M, y), color=(0.6,0.6,0.6), width=0.6); y += 4; i += 1; continue
    if re.match(r'^# [^#]', line):
        chk(24); y += 6; rpara(line[2:].strip(), sz=14, bold=True)
        page.draw_line((M, y), (PW-M, y), color=(0,0,0), width=0.8); y += 4; i += 1; continue
    if line.startswith('## '):
        chk(16); y += 3; rpara(line[3:].strip(), sz=12, bold=True); y += 2; i += 1; continue
    if line.startswith('### '):
        chk(14); y += 2; rpara(line[4:].strip(), sz=10, bold=True); y += 2; i += 1; continue
    if line.strip().startswith('|'):
        tbl = []
        while i < len(lines) and lines[i].strip().startswith('|'): tbl.append(lines[i]); i += 1
        chk(30); rtable(tbl); continue
    if re.match(r'^[-*] ', line.strip()):
        items = []
        while i < len(lines) and re.match(r'^[-*] ', lines[i].strip()): items.append(lines[i].strip()); i += 1
        for it in items:
            t = re.sub(r'^[-*] ', '', it).strip()
            chk(LH+2); rpara(t, indent=12, bc='•'); y += 1
        continue
    if line.strip().startswith('- ['):
        items = []
        while i < len(lines) and lines[i].strip().startswith('- ['): items.append(lines[i].strip()); i += 1
        for it in items:
            chk(LH+2)
            m = re.match(r'^- \[([ x])\] (.*)', it)
            checked = m and m.group(1) == 'x'
            text = m.group(2) if m else it[6:]
            page.draw_rect((M, y-6, M+8, y+1), color=(0,0,0), width=0.5)
            if checked: page.insert_text((M+2, y-1), '✓', fontname='helvetica-bold', fontsize=7)
            rpara(text, sz=8.5, indent=14); y += 1
        continue
    if re.match(r'^\d+\. ', line.strip()):
        items = []
        while i < len(lines) and re.match(r'^\d+\. ', lines[i].strip()): items.append(lines[i].strip()); i += 1
        for it in items:
            m = re.match(r'^(\d+\. )(.*)', it); num, text = m.group(1), m.group(2)
            chk(LH+2); nw = tw(num, 'helvetica', FS)
            page.insert_text((M+2, y), num, fontname='helvetica', fontsize=FS)
            rpara(text, indent=int(nw+6)); y += 1
        continue
    chk(LH); rpara(line.strip()); y += 1; i += 1

out = r'C:\Users\User\.hermes\workspace\employment-offer-stephanie.pdf'
np = len(doc); doc.save(out); doc.close()
print(f'Done: {out}  ({os.path.getsize(out)} bytes, {np} pages)')

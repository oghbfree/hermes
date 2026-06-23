from PIL import Image, ImageFilter, ImageDraw

src_path = r'C:\Users\User\.hermes\workspace\content-output\week-2026-05-18\wednesday-akoma\instagram\student-spotlight.jpg'
logo_path = r'C:\Users\User\.hermes\workspace\memories\business\Content\content-assets\akoma\AKOMA_ROBOTICS_LOGO_OFFICIAL.png'

src = Image.open(src_path).convert('RGBA')
logo = Image.open(logo_path).convert('RGBA')
W, H = src.size

# Heart graphic only — content y=48 to y=148 (confirmed from purple-pixel scan)
heart = logo.crop((0, 48, logo.width, 148))
print(f'Heart: {heart.size}')

# Background strip covering both old logos
SX0, SY0, SX1, SY1 = W - 160, 0, W, 115

# Sample true photo background around the strip
samples = []
for y in range(SY0, SY1):
    for x in range(max(0, SX0 - 16), max(0, SX0 - 4)):
        samples.append(src.getpixel((x, y)))
for x in range(SX0, SX1):
    for y in range(SY1 + 4, min(H, SY1 + 30)):
        samples.append(src.getpixel((x, y)))
avg = tuple(int(sum(c[i] for c in samples) / len(samples)) for i in range(4))
print(f'Bg avg: {avg[:3]}')

result = src.copy().convert('RGB')
for yy in range(SY0, SY1):
    for xx in range(SX0, SX1):
        result.putpixel((xx, yy), avg[:3])

pad = 22
px1 = max(0, SX0 - pad); py1 = max(0, SY0 - pad)
px2 = min(W, SX1 + pad); py2 = min(H, SY1 + pad)
blurred = result.crop((px1, py1, px2, py2)).filter(ImageFilter.GaussianBlur(radius=14))
result.paste(blurred, (px1, py1))

# Enlarged placement — keep aspect ratio, aim for ~135x~100 px
lw, lh = heart.size  # 572x100
target_w, target_h = 135, 100
scale = min(target_w / lw, target_h / lh)
nw, nh = int(lw * scale), int(lh * scale)
heart_scaled = heart.resize((nw, nh), Image.LANCZOS)
lx = W - nw - 8
ly = 6
print(f'Heart: {nw}x{nh} at ({lx},{ly})')

# Soft shadow
offset = 13
shadow = Image.new('RGBA', (nw + offset*2, nh + offset*2), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle(
    [offset, offset, nw+offset, nh+offset], radius=6, fill=(80, 60, 40, 42)
)
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=6))

rgba = result.convert('RGBA')
rgba.paste(shadow, (lx - offset, ly - offset), shadow)
rgba.paste(heart_scaled, (lx, ly), heart_scaled)

rgba.convert('RGB').save(src_path, quality=95)
print('Saved.')

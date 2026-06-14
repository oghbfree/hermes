from PIL import Image, ImageFilter, ImageDraw
import numpy as np

src_path = r'C:\Users\User\.hermes\workspace\content-output\week-2026-05-18\wednesday-akoma\instagram\student-spotlight.jpg'
logo_path = r'C:\Users\User\.hermes\workspace\content-assets\akoma\AKOMA_ROBOTICS_LOGO.png'

src = Image.open(src_path).convert('RGBA')
logo = Image.open(logo_path).convert('RGBA')
W, H = src.size

# Crop heart graphic only — content y=48..520 (no text)
heart = logo.crop((0, 48, logo.width, 520))
print(f'Heart: {heart.size}')

# Bottom overlay region
BOTTOM_Y = 649

# Get accurate purple footer color from existing strip
footer_samples = []
for y in range(710, 730):
    for x in range(W//2 - 50, W//2 + 50):
        footer_samples.append(src.getpixel((x, y)))
footer_avg = tuple(int(sum(c[i] for c in footer_samples) / len(footer_samples)) for i in range(4))
print(f'Footer purple: {footer_avg[:3]}')

# Get photo background above footer (transition zone y=670-695)
photo_samples = []
for y in range(670, 696):
    for x in range(W//2 - 80, W//2 + 80):
        p = src.getpixel((x, y))
        if p[0] > 30:  # avoid black
            photo_samples.append(p)
photo_avg = tuple(int(sum(c[i] for c in photo_samples) / len(photo_samples)) for i in range(4))
print(f'Photo bg above footer: {photo_avg[:3]}')

result = src.copy()

# Fill dark band y=649-695 with photo-average, blur-feather
result_rgb = result.convert('RGB')
for y in range(649, 696):
    for x in range(W):
        result_rgb.putpixel((x, y), photo_avg[:3])

# Feather the dark-band removal
band_patch = result_rgb.crop((0, 649-15, W, 696+15))
blurred_band = band_patch.filter(ImageFilter.GaussianBlur(radius=8))
result_rgb.paste(blurred_band, (0, 649-15))

# Place heart in purple footer, centered, large
lw, lh = heart.size
max_w = 180
max_h = 100
scale = min(max_w / lw, max_h / lh)
nw, nh = int(lw * scale), int(lh * scale)
heart_scaled = heart.resize((nw, nh), Image.LANCZOS)
lx = (W - nw) // 2
ly = 698 + (65 - nh) // 2  # center in purple strip
print(f'Place heart: {nw}x{nh} at ({lx},{ly})')

# Soft glow shadow on purple footer
offset = 10
shadow = Image.new('RGBA', (nw + offset*2, nh + offset*2), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle(
    [offset, offset, nw+offset, nh+offset], radius=5, fill=(60, 20, 80, 50)
)
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))

res = result_rgb.convert('RGBA')
res.paste(shadow, (lx - offset, ly - offset), shadow)
res.paste(heart_scaled, (lx, ly), heart_scaled)

res.convert('RGB').save(src_path, quality=95)
print('Saved.')

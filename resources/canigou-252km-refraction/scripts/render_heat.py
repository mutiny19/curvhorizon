"""False-color 'thermal style' render of the near-IR panorama, with an honest legend."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

a = np.asarray(Image.open('../PANO_RAW_1.jpg').convert('L')).astype(np.float32)
H, W = a.shape

# --- Ironbow LUT (classic thermal-camera palette) ---
stops = [
    (0.00, (0, 0, 20)), (0.10, (20, 6, 90)), (0.25, (85, 15, 145)),
    (0.40, (155, 25, 140)), (0.55, (215, 70, 85)), (0.70, (245, 130, 30)),
    (0.85, (255, 200, 30)), (1.00, (255, 255, 230)),
]
lut = np.zeros((256, 3), np.uint8)
xs = np.arange(256) / 255.0
for c in range(3):
    xp = [s[0] for s in stops]; fp = [s[1][c] for s in stops]
    lut[:, c] = np.interp(xs, xp, fp).astype(np.uint8)

# mild percentile stretch for contrast (keeps relative ordering)
lo, hi = np.percentile(a, 0.5), np.percentile(a, 99.7)
idx = np.clip((a - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
rgb = lut[idx]

img = Image.fromarray(rgb)

# --- legend strip on top ---
LEG_H = 150
canvas = Image.new('RGB', (W, H + LEG_H), (10, 10, 14))
canvas.paste(img, (0, LEG_H))
d = ImageDraw.Draw(canvas)
fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 52)
fm = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 40)
fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 34)

# color bar
bx0, bx1, by0, by1 = 7000, 13000, 45, 105
bar = lut[np.clip((np.linspace(0, 255, bx1 - bx0)).astype(int), 0, 255)]
bar_img = Image.fromarray(np.tile(bar[None, :, :], (by1 - by0, 1, 1)))
canvas.paste(bar_img, (bx0, by0))
d.rectangle([bx0, by0, bx1, by1], outline=(230, 230, 230), width=3)
for frac, lab in [(0.0, 'darker  (low NIR return)'), (0.5, 'relative near-IR brightness'), (1.0, 'brighter  (high NIR return)')]:
    x = bx0 + frac * (bx1 - bx0)
    anch = 'la' if frac == 0 else ('ma' if frac == 0.5 else 'ra')
    d.text((x, by1 + 8), lab, font=fm, fill=(235, 235, 235), anchor=anch)
d.text((bx0 - 40, (by0 + by1) // 2), 'IR-COLD look', font=fm, fill=(160, 190, 255), anchor='rm')
d.text((bx1 + 40, (by0 + by1) // 2), 'IR-HOT look', font=fm, fill=(255, 190, 120), anchor='lm')

d.text((60, 20), 'CANIGOU  >  GULF OF LION  |  false-color render of Antoine Mangiavacca’s 1000 nm near-IR panorama, 12 Sep 2019 19:15', font=fb, fill=(255, 255, 255))
d.text((60, 88), 'HONEST SCALE NOTE: this is reflected NEAR-infrared (1000 nm), not thermal LWIR — pixel brightness is NIR reflectance + haze penetration, NOT temperature. '
                 'No °C/°F can be measured from it. Ambient refs that evening: sea surface ≈21 °C / 70 °F, summit air ≈8 °C / 46 °F.',
       font=fs, fill=(255, 210, 120))

canvas.save('../Canigou_pano_falsecolor_full.jpg', quality=90)
canvas.resize((4000, int((H + LEG_H) * 4000 / W)), Image.LANCZOS).save('../Canigou_pano_falsecolor_preview.jpg', quality=90)
print('saved false-color renders', canvas.size)

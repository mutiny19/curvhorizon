"""Refraction (k-coefficient) overlay on the near-IR panorama."""
import numpy as np, math
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

R0, Hobs = 6371000.0, 2786.16
K = 0.126
Re = R0 / (1 - K)
dh = math.sqrt(2 * Re * Hobs)

a = np.asarray(Image.open('../PANO_RAW_1.jpg').convert('L'))
H, W = a.shape
base = np.stack([a] * 3, -1)
img = Image.fromarray((base * 0.82).astype(np.uint8))

TOP = 170
canvas = Image.new('RGB', (W, H + TOP), (8, 10, 16))
canvas.paste(img, (0, TOP))
d = ImageDraw.Draw(canvas, 'RGBA')
F = lambda s, b=0: ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf", s)
fT, fL, fM, fS = F(56, 1), F(38, 1), F(34), F(29)

def hidden_m(D):
    return 0.0 if D <= dh else (D - dh) ** 2 / (2 * Re)

# landmarks: name, pano_x, D_m, base_elev(None=terrain), top_elev, card_center_x
LM = [
    ("Barre des Écrins", 2949, 412600, None, 4102, 2949),
    ("Mont Ventoux", 4203, 293500, None, 1910, 4203),
    ("25 wind turbines\nPort-St-Louis", 10700, 214700, 2, 77, 10700),
    ("Chapelle N-D-de-Vie\n(Rocher de Vitrolles)", 12761, 250400, 111, 119, 12300),
    ("HV pylons, Réaltor corridor\n(Arbois crest, ~60-70 m)", 13218, 253500, 210, 275, 12820),
    ("Ste-Victoire\n(Pic des Mouches)", 13360, 284700, None, 1011, 13360),
    ("Pic du Taoumé", 15525, 265700, None, 668, 14150),
    ("Grande Tête Rouge", 15546, 264100, None, 520, 14680),
    ("Tête Ronde", 15664, 267100, None, 638, 15210),
    ("Garlaban", 15738, 268200, None, 714, 15740),
    ("Notre-Dame\nde la Garde", 15801, 252740, 154, 224, 16280),
    ("Super Rouvière B", 16471, 255700, 145, 225, 16810),
    ("Mont Puget", 16995, 256400, None, 565, 17360),
]

# horizon row (measured sea edge, gentle bow) as function of x
hx = np.array([9000, 10500, 13300, 15150, 15800, 16400, 17500, 19000])
hy = np.array([812.9, 812.7, 811.5, 810.1, 809.5, 811.6, 813.6, 809.2])
coef = np.polyfit(hx, hy, 2)
horizon = lambda x: np.polyval(coef, np.clip(x, 9000, 19000)) + TOP

# dashed horizon line
for x0 in range(0, W, 160):
    y = horizon(x0)
    d.line([x0, y, min(x0 + 90, W), horizon(x0 + 90)], fill=(80, 220, 255, 210), width=4)

# --- landmark cards ---
lanes = [360, 560, 360, 620, 330, 560, 330, 530, 330, 530, 330, 530, 330]
for (name, x, D, be, te, cx), ylane in zip(LM, lanes):
    hm = hidden_m(D)
    vis = max(0.0, te - hm)
    tot = te - (be if be is not None else 0)
    hid_of_obj = min(tot, max(0.0, hm - (be if be is not None else 0))) if be is not None else min(te, hm)
    yh = horizon(x)
    d.line([cx, ylane + 8, x, yh], fill=(80, 220, 255, 150), width=3)
    d.ellipse([x - 7, yh - 7, x + 7, yh + 7], outline=(80, 220, 255, 230), width=3)
    # card
    lines = name.split('\n')
    cw = 460
    ch = 96 + 34 * len(lines) + 60
    x0 = int(np.clip(cx - cw / 2, 20, W - cw - 20)); y0 = ylane - ch
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], 14, fill=(10, 14, 24, 215), outline=(80, 220, 255, 220), width=3)
    ty = y0 + 12
    for ln in lines:
        d.text((x0 + 18, ty), ln, font=fL, fill=(255, 255, 255)); ty += 42
    d.text((x0 + 18, ty), f"D = {D/1000:.0f} km   hidden below horizon: {hm:.0f} m", font=fS, fill=(255, 170, 130)); ty += 36
    if be is not None:
        msg = f"structure: {max(0,vis):.0f} m visible / {hid_of_obj:.0f} m hidden" if vis > 0 else "entirely hidden at this k"
    else:
        msg = f"relief visible: top {vis:.0f} m of {te} m peak"
    d.text((x0 + 18, ty), msg, font=fS, fill=(150, 255, 170) if vis > 0 else (255, 120, 120)); ty += 36
    # stacked bar
    bw = cw - 36; bx = x0 + 18; by = ty + 4
    fr = min(1.0, hm / te)
    d.rectangle([bx, by, bx + bw, by + 22], fill=(60, 200, 90, 255))
    d.rectangle([bx, by, bx + bw * fr, by + 22], fill=(235, 80, 60, 255))
    d.rectangle([bx, by, bx + bw, by + 22], outline=(230, 230, 230, 255), width=2)

# Cap Sicié note at right edge
d.text((W - 30, 900), "Cap Sicié (358 m, 284 km) → just off-frame right — needs k ≥ 0.19; at k=0.126 it is 112 m below the horizon (author saw it only next dawn)",
       font=fM, fill=(255, 200, 120), anchor='rm')

# --- header ---
d.text((50, 18), "REFRACTION ANALYSIS  |  Canigou 2 786 m → Gulf of Lion, 12 Sep 2019 19:15  |  solved from this image: k = 0.126 ± 0.02  (effective Earth radius R′ = R/(1−k) = 7 290 km, horizon at 201.5 km)",
       font=fT, fill=(255, 255, 255))
d.text((50, 92), "hidden height beyond horizon:  h = (D − √(2R′H))² / 2R′    |    fit: NDG spike 6.0 px, Garlaban 53 px, Mont Puget 49.5 px, turbine tips 9.9 px above sea horizon (5.92″/px)    |    weather-model prediction k ≈ 0.14–0.16    |    cyan dashes = sea horizon",
       font=fM, fill=(170, 210, 255))

# k gradient bar
kx0, kx1, ky0, ky1 = 14200, 19500, 30, 86
stops = [(0, (20, 6, 90)), (0.35, (155, 25, 140)), (0.6, (235, 80, 60)), (0.8, (245, 160, 30)), (1, (255, 240, 180))]
g = np.zeros((ky1 - ky0, kx1 - kx0, 3), np.uint8)
xs = np.linspace(0, 1, kx1 - kx0)
for c in range(3):
    g[..., c] = np.interp(xs, [s[0] for s in stops], [s[1][c] for s in stops])[None, :]
canvas.paste(Image.fromarray(g), (kx0, ky0))
d.rectangle([kx0, ky0, kx1, ky1], outline=(240, 240, 240), width=3)
for kv, lab, strong in [(0.0, "k=0 geometric\n188 km", 0), (0.126, "k=0.126 THIS PHOTO\n201.5 km", 1),
                        (0.155, "k≈0.155 std atm\n205 km", 0), (0.19, "k=0.19 Cap Sicié\n209 km", 0), (0.30, "k=0.30 strong duct\n225 km", 0)]:
    x = kx0 + kv / 0.30 * (kx1 - kx0)
    d.line([x, ky0 - 6, x, ky1 + 6], fill=(255, 255, 255), width=5 if strong else 3)
    d.multiline_text((x, ky1 + 10), lab, font=F(26, strong), fill=(255, 255, 160) if strong else (220, 220, 220), anchor='ma', align='center')

canvas.save('../Canigou_pano_k_refraction_full.jpg', quality=90)
canvas.resize((4000, int((H + TOP) * 4000 / W)), Image.LANCZOS).save('../Canigou_pano_k_refraction_preview.jpg', quality=90)
print('saved overlay', canvas.size)

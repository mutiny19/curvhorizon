"""Refraction geometry: Canigo -> Gulf of Lion / Marseille landmarks.

Model: effective earth radius R' = R/(1-k).
Observer height H above sea level. Horizon distance d_h = sqrt(2 R' H).
For target at distance D > d_h, hidden height at target:
    h_hidden = (D - d_h)^2 / (2 R')
Apparent altitude (radians, relative to observer horizontal) of a point at
elevation E, distance D:  alpha = (E - H)/D - D/(2 R')
Sea-horizon dip: -sqrt(2 H / R')
"""
import math, json
from geographiclib.geodesic import Geodesic

R0 = 6371000.0
geod = Geodesic.WGS84

CANIGO = (42.519167, 2.456528, 2784.66)   # summit; camera ~ +1.5 m
H_OBS = 2784.66 + 1.5

# name: (lat, lon, base_elev_m, top_elev_m, note)
targets = {
    "Wind turbines Port-St-Louis (tip)": (43.435639, 4.773781, 2, 77, "hub ~50 m ASL, tip ~77 m ASL, 25 units"),
    "Notre-Dame de la Garde (statue top)": (43.284050, 5.371310, 154, 224, "hill 149-154 m; structure to ~224 m"),
    "Super Rouviere bldg B (top)": (43.24400, 5.42100, 115, 195, "site 80-160 m, bldg ~80 m"),
    "Grande Tete Rouge": (43.33720, 5.49480, None, 520, "peak"),
    "Pic du Taoume": (43.34500, 5.51200, None, 668, "peak"),
    "Tete Ronde": (43.33520, 5.53470, None, 638, "peak"),
    "Garlaban": (43.33250, 5.54970, None, 714, "peak"),
    "Crete de la Lare": (43.35300, 5.56700, None, 598, "ridge E of Garlaban, approx"),
    "Mont Puget": (43.21700, 5.44700, None, 565, "peak"),
    "Sainte-Victoire (Pic des Mouches)": (43.54110, 5.65970, None, 1011, "peak"),
    "Mont Ventoux": (44.17410, 5.27860, None, 1910, "peak"),
    "Cap Sicie": (43.06440, 5.85140, None, 358, "NOT seen evening; seen at dawn w/ strong refraction"),
    "Barre des Ecrins": (44.92390, 6.35970, None, 4102, "Alps, ~412 km per blog"),
}

def dist_az(lat, lon):
    g = geod.Inverse(CANIGO[0], CANIGO[1], lat, lon)
    return g["s12"], g["azi1"] % 360

def hidden(D, k, H=H_OBS):
    Re = R0 / (1 - k)
    dh = math.sqrt(2 * Re * H)
    if D <= dh: return 0.0
    return (D - dh) ** 2 / (2 * Re)

def app_alt(E, D, k, H=H_OBS):
    Re = R0 / (1 - k)
    return (E - H) / D - D / (2 * Re)   # radians

ks = [0.00, 0.13, 0.17, 0.20, 0.25, 0.30]
print(f"Observer: Canigo summit {H_OBS:.0f} m")
for k in ks:
    Re = R0/(1-k)
    print(f"  k={k:.2f}: horizon = {math.sqrt(2*Re*H_OBS)/1000:.1f} km, dip = {math.degrees(math.sqrt(2*H_OBS/Re)):.3f} deg")
print()
hdr = f"{'Target':38s} {'D km':>7s} {'Az':>6s} {'Top m':>6s}" + "".join(f" h(k={k:.2f})" for k in ks)
print(hdr)
res = {}
for name, (lat, lon, base, top, note) in targets.items():
    D, az = dist_az(lat, lon)
    hs = [hidden(D, k) for k in ks]
    res[name] = dict(D=D, az=az, base=base, top=top, note=note, hidden={str(k): h for k, h in zip(ks, hs)})
    print(f"{name:38s} {D/1000:7.1f} {az:6.1f} {top:6.0f}" + "".join(f" {h:8.0f}" for h in hs))

# ---- constraints on k from what the photo shows ----
print("\n--- k required for given visibility thresholds ---")
def k_for_hidden(D, h_target, lo=-0.5, hi=0.99):
    # find k such that hidden(D,k) == h_target (hidden decreases with k)
    for _ in range(200):
        mid = (lo + hi) / 2
        if hidden(D, mid) > h_target: lo = mid
        else: hi = mid
    return (lo + hi) / 2

D_wind, _ = dist_az(43.435639, 4.773781)
D_ndg, _  = dist_az(43.284050, 5.371310)
D_sic, _  = dist_az(43.06440, 5.85140)
D_sr, _   = dist_az(43.24400, 5.42100)
print(f"Windmills D={D_wind/1000:.1f} km: nacelles(50m) visible needs k>{k_for_hidden(D_wind,50):.3f}; "
      f"tips(77m) visible needs k>{k_for_hidden(D_wind,77):.3f}; base(2m) visible needs k>{k_for_hidden(D_wind,2):.3f}")
print(f"NDG D={D_ndg/1000:.1f} km: statue top(224m) visible needs k>{k_for_hidden(D_ndg,224):.3f}; "
      f"esplanade(154m) visible needs k>{k_for_hidden(D_ndg,154):.3f}; tower base(160m): k>{k_for_hidden(D_ndg,160):.3f}")
print(f"Super Rouviere D={D_sr/1000:.1f} km: top(195m) visible needs k>{k_for_hidden(D_sr,195):.3f}; base(115m): k>{k_for_hidden(D_sr,115):.3f}")
print(f"Cap Sicie D={D_sic/1000:.1f} km: summit(358m) visible needs k>{k_for_hidden(D_sic,358):.3f}  (NOT visible evening => k below this)")

json.dump(res, open("/sessions/awesome-blissful-johnson/mnt/outputs/work/geometry.json", "w"), indent=1)
print("\nsaved geometry.json")

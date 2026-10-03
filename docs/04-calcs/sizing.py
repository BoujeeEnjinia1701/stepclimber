"""StepClimber sizing calculations, SCM-CAL-001 v0.3 (TRL 3, constructable design, SCM-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
First-principles paper estimates; nothing here is measured.

2D climbing model (section 3): X points away from the stair (toward the lower floor), Z up.
The riser being climbed has its face at X = 0 from Z = 0 to Z = h; its nosing corner is at
(n, h), where n is the nosing overhang. The next riser face is at X = -T. The cluster
rotates one third of a turn per step: first about the wheel lodged against the riser (the
pivot) until the swinging wheel lands on the tread above, then about the landed wheel until
the hub is back at 30 degrees above it. The courier then rolls the truck back on the landed
wheel to the next riser.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, derived, case_outline, axle_plate_outline, flange_outline, BRG  # noqa: E402  (no build123d)

D = derived()
G = 9.81
OUT = []   # (key, value, unit) rows for results.csv


def rec(key, value, unit=""):
    OUT.append((key, value, unit))
    return value


def head(t):
    print(f"\n=== {t} ===")


# ---------------------------------------------------------------- 1. Assumptions
M_PAYLOAD = 60.0            # kg, rated stair load (R1, decided 2026-09-25)
STEEL, ALU = 7.85e-6, 2.70e-6   # kg/mm3


def made_masses():
    """Masses (kg) of the parts added or itemised to make the design buildable (SCM-DDR-003), from the
    model outlines and stock sizes. Holes are ignored, which is conservative."""
    py0, py1 = P["plate_y"]; iy0, iy1 = P["inner_y"]
    outline = case_outline()
    m = {
        "axle plate, plain side (4 mm steel)": axle_plate_outline().area * (P["axle_plate_y"][1] - P["axle_plate_y"][0]) * STEEL,
        "case outer plate (3 mm steel)": outline.area * (py1 - py0) * STEEL,
        "case inner plate (3 mm aluminium)": outline.area * (iy1 - iy0) * ALU,
        "case band (1.5 mm aluminium)": outline.length * (py0 - iy1) * P["band_t"] * ALU,
        "case spacers (2, 16 mm bar)": 2 * math.pi * P["spacer_r"] ** 2 * (py0 - iy1) * STEEL,
        "component uprights (2, aluminium 30 x 6)": 2 * P["up_w"] * P["up_t"] * (P["bars"][2] - P["bars"][0] + 2 * P["bar_r"]) * ALU,
        "skid standoffs (4, 20 x 20 x 1.5 tube)": 4 * (20 * 20 - 17 * 17) * (P["rail_x"] - P["skid_x"] - 10) * STEEL,
        "stub axles (6, 20 mm bar)": 6 * math.pi * P["stub_r"] ** 2 * 55 * STEEL,
    }
    return m


MADE = made_masses()
# Shafts, bearings, sprockets and chains itemised from catalogue-class masses (SCM-DDR-003, P11);
# the TRL 3 concept carried a 2.5 kg allowance for this group.
DRIVE = {"cluster shaft 25 x 490": math.pi * 12.5 ** 2 * 2 * P["shaft_half"] * STEEL,
         "countershaft 20 x 124": math.pi * 10 ** 2 * 124 * STEEL,
         "two 25 mm two-bolt flange bearings": 2 * 0.60, "two 20 mm two-bolt flange bearings": 2 * 0.45,
         "four sprockets": 0.70, "two chains": 0.55}
MASS = {                    # kg, truck mass roll-up (BOM line numbers)
    "1 frame and toe plate (as bought; replacement low bar replaces the bar cut off)": 8.0,
    "2 clusters (pair)": 5.5, "2 stub axles": MADE["stub axles (6, 20 mm bar)"],
    "3 shafts, bearings, sprockets, chains": sum(DRIVE.values()),
    "4 worm gearmotor with brake": 4.5, "5 and 6 driver, controller, IMU": 0.8, "7 pack and cradle": 2.6,
    "8 switch, fuse, harness": 0.5, "9 handle controls": 0.6, "10 strap": 0.4, "11 skids": 0.4,
    "13 enclosure and hardware": 0.5,
    "14 axle plates and chain case": sum(v for k, v in MADE.items() if k.startswith(("axle", "case"))),
    "15 component uprights": MADE["component uprights (2, aluminium 30 x 6)"],
    "16 skid standoffs": MADE["skid standoffs (4, 20 x 20 x 1.5 tube)"],
    "17 fixings added for construction": 0.5,
}
H_CG = 500.0                # mm, combined center of mass above the shaft, along the frame
STEPS_PER_MIN = 16.0        # R3 for the first prototype, decided 2026-10-02 (SCM-DEC-001, item 3): 3.75 s per third of a turn
ETA_DRV, ETA_MOT, ETA_WORM, ETA_CHAIN = 0.95, 0.80, 0.45, 0.95
ETA_CHAIN2 = 0.97           # second chain stage (08B), added by the rework
DYN = 1.3                   # friction and dynamics factor on static shaft torque
LEAD = 4.0                  # deg, worm lead angle (single start, ratio about 75)
I_WORM = 75.0               # worm gear ratio (motor about 3,000 rpm to 40 rpm)
T_BRAKE = 2.0               # N m, spring-applied brake on the motor shaft (typical wheelchair motor)
GM_RATED = 30.0             # N m, gearmotor rated output torque
P_MOTOR = 250.0             # W, motor rated output
E_PACK = 256.0              # Wh, 8S 10 Ah LiFePO4
DOD = 0.90                  # usable fraction
STANDBY = 1.10              # factor for standby, starts and stops
CHG_V, CHG_A, ETA_CHG, CV_TAIL = 29.2, 3.0, 0.90, 0.3   # charger; CV tail in h
CRR = 0.03                  # rolling resistance, solid rubber on a smooth floor
WINDOW = 3.0                # deg, R7 tilt window for the first loaded trials, decided 2026-10-02 (SCM-DEC-001, item 4)
F_HANDLE_MAX = 100.0        # N, R6
NOSE = (0.0, 32.0)          # mm, nosing overhang range (R2)
H_DESIGN, T_DESIGN = 196.0, 254.0   # IRC maximum riser and minimum tread
LAND_MIN = 30.0             # mm, landing contact past the nosing edge (IRC nosing radius up to 9.5 mm, plus wear)
ENV_MARGIN = 10.0           # mm, clearance wanted between a shaft-mounted envelope and a nosing
SY_SHAFT, SY_PLATE, SY_TUBE = 655.0, 275.0, 250.0   # MPa: 4140 quenched and tempered shaft (decided 2026-10-02; minimum yield, to be confirmed by the mill certificate), S275 plate, welded steel tube
SUT_SHAFT = 1000.0          # MPa, 4140 quenched and tempered, minimum tensile strength assumed
KT_KEY = 2.0                # keyway stress concentration
SHOCK = 3.0                 # dropped-step dynamic factor
CHAIN_BREAK = {"06B": (9.525, 8.9e3), "08B": (12.7, 17.8e3)}   # pitch mm, ISO 606 minimum tensile N
R5_MAX = 35.0               # kg, R5 truck mass for the first prototype, decided 2026-10-02 (SCM-DEC-001, item 2)
BUDGET = 650.0              # USD, value-engineering target (budget_usd), set 2026-09-25 (SCM-DDR-002)

a, r = P["arm"], P["wheel_r"]
d = D["spacing"]
m_truck = sum(MASS.values())
m_tot = M_PAYLOAD + m_truck
W = m_tot * G
L_H = D["handle_len"]       # grip distance from the shaft along the frame
TILT = P["tilt"]

head("1. Load case")
print(f"Truck mass {m_truck:.1f} kg; payload {M_PAYLOAD:.0f} kg; total {m_tot:.1f} kg; weight {W:.0f} N")
rec("truck_mass_kg", round(m_truck, 1), "kg"); rec("total_mass_kg", round(m_tot, 1), "kg"); rec("weight_N", round(W), "N")

# ---------------------------------------------------------------- 2. Cluster geometry
head("2. Cluster geometry")
print(f"Arm {a:.0f} mm, wheel radius {r:.0f} mm, spacing {d:.1f} mm, hub height {D['hub_z']:.1f} mm, "
      f"cluster diameter {D['cluster_dia']:.0f} mm")
rec("wheel_spacing_mm", round(d, 1), "mm"); rec("hub_height_mm", round(D["hub_z"], 1), "mm")


def pivot_x(h, n):
    """Pivot wheel center X: against the riser face, or against the nosing lip on low risers."""
    x = r
    if h - r < r:
        x = max(x, n + math.sqrt(r * r - (h - r) ** 2))
    return x


def landing(h, n):
    """Landing contact distance past the nosing edge, and landed wheel center X."""
    xp = pivot_x(h, n)
    xl = xp - math.sqrt(d * d - h * h)
    return n - xl, xl


h_max_land = math.sqrt(d * d - (r + LAND_MIN) ** 2)
print(f"Largest riser with landing {LAND_MIN:.0f} mm past the nosing edge (no overhang): {h_max_land:.0f} mm")
rec("riser_max_landing_mm", round(h_max_land), "mm")
print("Riser  landing past nosing (n=0 / n=32)  min tread for landing")
for h in (100, 150, 175, 196, 200, 210, 220, 241):
    if h >= d:
        print(f"{h:5.0f}  riser exceeds the {d:.0f} mm wheel spacing: the cluster cannot reach the tread")
        rec(f"landing_h{h}_n0_mm", "none", "mm")
        continue
    l0, xl0 = landing(h, 0.0); l32, _ = landing(h, 32.0)
    t_min = r - xl0
    print(f"{h:5.0f}  {l0:7.1f} / {l32:6.1f} mm                    {t_min:6.1f} mm")
    rec(f"landing_h{h}_n0_mm", round(l0, 1), "mm")
    rec(f"tread_min_h{h}_mm", round(t_min, 1), "mm")


# ---------------------------------------------------------------- 3. Climb kinematics and clearances
def seg_dist(p, a0, a1):
    ax, az = a0; bx, bz = a1; px, pz = p
    vx, vz = bx - ax, bz - az
    t = max(0.0, min(1.0, ((px - ax) * vx + (pz - az) * vz) / (vx * vx + vz * vz)))
    return math.hypot(px - ax - t * vx, pz - az - t * vz)


def climb_states(h, n, steps=240):
    """Yield (phase, pivot, hub, wheels) through one step. Angles in degrees, CCW positive."""
    xp = pivot_x(h, n)
    piv = (xp, r)
    phi_land = 180.0 - math.degrees(math.asin(h / d))      # landing wheel direction from the pivot
    hub0 = 30.0
    for i in range(steps + 1):
        rot = (phi_land - 60.0) * i / steps
        ang = hub0 + rot
        hub = (piv[0] + a * math.cos(math.radians(ang)), piv[1] + a * math.sin(math.radians(ang)))
        wheels = [(hub[0] + a * math.cos(math.radians(ang + 180 + k * 120)),
                   hub[1] + a * math.sin(math.radians(ang + 180 + k * 120))) for k in range(3)]
        yield "1", piv, hub, wheels
    land = (piv[0] + d * math.cos(math.radians(phi_land)), piv[1] + d * math.sin(math.radians(phi_land)))
    hx, hz = hub
    ang2_0 = math.degrees(math.atan2(hz - land[1], hx - land[0]))
    for i in range(steps + 1):
        ang = ang2_0 + (30.0 - ang2_0) * i / steps
        hub = (land[0] + a * math.cos(math.radians(ang)), land[1] + a * math.sin(math.radians(ang)))
        wheels = [(hub[0] + a * math.cos(math.radians(ang + 180 + k * 120)),
                   hub[1] + a * math.sin(math.radians(ang + 180 + k * 120))) for k in range(3)]
        yield "2", land, hub, wheels


def clearances(h, n, T=T_DESIGN):
    corners = [(n, h), (n - T, 2 * h)]
    hub_min = arm_min = wheel_min = 1e9
    for ph, piv, hub, wheels in climb_states(h, n):
        for c in corners:
            hub_min = min(hub_min, math.hypot(hub[0] - c[0], hub[1] - c[1]))
            for w in wheels:
                arm_min = min(arm_min, seg_dist(c, hub, w) - P["arm_w"] / 2)
                if math.hypot(w[0] - piv[0], w[1] - piv[1]) > 1.0:       # the pivot wheel rests on a tread
                    wheel_min = min(wheel_min, math.hypot(w[0] - c[0], w[1] - c[1]) - r)
    return hub_min, arm_min, wheel_min


head("3. Nosing clearances through one step")
RISERS = (100, 125, 150, 175, 196, 200)


def sweep(n):
    """Worst clearances over the R2 riser range for one nosing overhang."""
    hm = am = wm = 1e9
    for h in RISERS:
        if h < d:
            x = clearances(h, n)
            hm, am, wm = min(hm, x[0]), min(am, x[1]), min(wm, x[2])
    return hm, am, wm


print("Riser  overhang  hub-to-nosing min  arm clearance  wheel clearance")
for h in RISERS:
    for n in NOSE:
        hm, am, wm = clearances(h, n)
        print(f"{h:5.0f}  {n:6.0f}    {hm:8.1f} mm        {am:7.1f} mm     {wm:7.1f} mm")
        rec(f"hub_nosing_min_h{h}_n{int(n)}_mm", round(hm, 1), "mm")
        rec(f"arm_clear_h{h}_n{int(n)}_mm", round(am, 1), "mm")
        rec(f"wheel_clear_h{h}_n{int(n)}_mm", round(wm, 1), "mm")
env = {n: sweep(n)[0] - ENV_MARGIN for n in NOSE}
n_arm_ok = max(n for n in range(0, 33) if sweep(float(n))[1] >= 0.0)
print(f"Allowed radius of anything on the shaft line (minimum hub-to-nosing distance less {ENV_MARGIN:.0f} mm): "
      f"{env[0.0]:.0f} mm with no overhang, {env[32.0]:.0f} mm with 32 mm overhang")
print(f"Largest nosing overhang the straight spider arms clear over the R2 riser range: {n_arm_ok} mm")
rec("env_radius_n0_mm", round(env[0.0]), "mm"); rec("env_radius_n32_mm", round(env[32.0]), "mm")
rec("overhang_max_arms_mm", n_arm_ok, "mm")
ENVELOPE = [("Shaft", P["shaft_d"] / 2), ("Spider boss", P["boss_r"]), ("Flange bearing housing", P["bearing_r"]),
            (f"{P['z_driven']}T 08B sprocket guard", D["guard_r"])]
for name, rad in ENVELOPE:
    print(f"  {name:28s} radius {rad:5.1f} mm: {'clear' if rad <= env[0.0] else 'HITS'} (no overhang), "
          f"{'clear' if rad <= env[32.0] else 'HITS'} (32 mm overhang)")
env_exact = sweep(32.0)[0] - ENV_MARGIN
print(f"Shaft-line guard radius {D['guard_r']:.1f} mm against {env_exact:.1f} mm allowed with 32 mm overhang: "
      f"margin {env_exact - D['guard_r']:.1f} mm (plus the {ENV_MARGIN:.0f} mm clearance)")
rec("guard_radius_mm", round(D["guard_r"], 1), "mm"); rec("guard_margin_n32_mm", round(env_exact - D["guard_r"], 1), "mm")

# Countershaft guard (fixed to the frame, cs_z up the frame from the shaft) against every nosing
u = (-math.sin(math.radians(TILT)), math.cos(math.radians(TILT)))       # up the frame
nx = (math.cos(math.radians(TILT)), math.sin(math.radians(TILT)))       # toward the load side of the frame
cs_min = 1e9
for h in RISERS:
    for n in NOSE:
        for ph, piv, hub, wheels in climb_states(h, n):
            c_s = (hub[0] + P["cs_z"] * u[0] + P["cs_x"] * nx[0], hub[1] + P["cs_z"] * u[1] + P["cs_x"] * nx[1])
            for c in [(n, h), (n - T_DESIGN, 2 * h), (n - 2 * T_DESIGN, 3 * h)]:
                cs_min = min(cs_min, math.hypot(c_s[0] - c[0], c_s[1] - c[1]))
print(f"Countershaft {P['cs_z']:.0f} mm up the frame and {-P['cs_x']:.0f} mm toward the stair: nearest nosing {cs_min:.0f} mm; guard radius {D['cs_guard_r']:.0f} mm; "
      f"clearance {cs_min - D['cs_guard_r']:.0f} mm")
rec("countershaft_nosing_clear_mm", round(cs_min - D["cs_guard_r"]), "mm")

# Frame-fixed outlines near the shaft (constructable design, SCM-DDR-003) against every nosing, in the
# frame's own coordinates (x toward the load side, z up the frame from the shaft line)
from shapely.geometry import Point as _Pt, box as _sbox  # noqa: E402
from shapely import affinity as _aff  # noqa: E402
noses = []
for h in RISERS:
    for n in NOSE:
        for ph, piv, hub, wheels in climb_states(h, n):
            for c in [(n, h), (n - T_DESIGN, 2 * h), (n - 2 * T_DESIGN, 3 * h)]:
                v = (c[0] - hub[0], c[1] - hub[1])
                noses.append((v[0] * nx[0] + v[1] * nx[1], v[0] * u[0] + v[1] * u[1]))
g5, g4 = BRG["205"], BRG["204"]
gx, _, gzz = P["gm_box"]
OUTLINES = [
    ("Chain case and drive-side axle plate", case_outline()),
    ("Plain-side axle plate", axle_plate_outline()),
    ("Main flange bearing", flange_outline(g5["bolt"], g5["r_mid"], g5["r_end"])),
    ("Countershaft flange bearing", _aff.translate(flange_outline(g4["bolt"], g4["r_mid"], g4["r_end"]), P["cs_x"], P["cs_z"])),
    ("Gearmotor gearbox", _sbox(P["cs_x"] - gx / 2, P["gm_z"] - gzz / 2, P["cs_x"] + gx / 2, P["gm_z"] + gzz / 2)),
    ("Motor and brake", _sbox(P["motor_x"] - P["motor_r"], P["gm_z"] + gzz / 2, P["motor_x"] + P["motor_r"], P["gm_z"] + gzz / 2 + P["motor_l"])),
    ("Replacement low cross bar", _Pt(P["rail_x"], P["low_bar"]).buffer(P["bar_r"])),
    ("Rails (load side of the shaft)", _sbox(P["rail_x"] - P["rail_r"], -P["rail_below"], P["rail_x"] + P["rail_r"], 400)),
]
print(f"Frame-fixed outlines against every nosing (need {ENV_MARGIN:.0f} mm or more):")
outline_clear = {}
for name, poly in OUTLINES:
    g = min(poly.distance(_Pt(*q)) for q in noses)
    inside = any(poly.contains(_Pt(*q)) for q in noses)
    outline_clear[name] = -1.0 if inside else g
    print(f"  {name:38s} nearest nosing {g:6.1f} mm{'  HITS' if inside or g < ENV_MARGIN else ''}")
    rec("nosing_clear_" + name.split(" (")[0].lower().replace(" ", "_").replace(",", "").replace("-", "_") + "_mm", round(g, 1), "mm")
skid_poly = _sbox(P["skid_x"], P["skid_z"][0], P["skid_x"] + 10, P["skid_z"][1])
skid_clear = min(skid_poly.distance(_Pt(*q)) for q in noses)
print(f"  Nosing guard skids (meant to be the nearest part) nearest nosing {skid_clear:6.1f} mm")
rec("nosing_clear_skids_mm", round(skid_clear, 1), "mm")
case_clear = outline_clear["Chain case and drive-side axle plate"]
all_outlines_ok = all(v >= ENV_MARGIN for v in outline_clear.values())

# Frame back vs the nosings above, beyond the shaft-line region, on the design stair at the set tilt
u = (-math.sin(math.radians(TILT)), math.cos(math.radians(TILT)))       # up the frame
nb = (-math.cos(math.radians(TILT)), -math.sin(math.radians(TILT)))     # frame back normal
back_depth = abs(P["skid_x"])
fb_min = 1e9
for ph, piv, hub, wheels in climb_states(H_DESIGN, 0.0):
    for k in range(1, 5):
        c = (0.0 - (k - 1) * T_DESIGN, k * H_DESIGN)
        v = (c[0] - hub[0], c[1] - hub[1])
        along = v[0] * u[0] + v[1] * u[1]
        if 150 < along < L_H:
            fb_min = min(fb_min, v[0] * nb[0] + v[1] * nb[1])
print(f"Frame back above the shaft region: nearest nosing {fb_min:.0f} mm behind the shaft line; skid face at "
      f"{back_depth:.0f} mm; clearance {fb_min - back_depth:.0f} mm")
rec("frame_back_nosing_clear_mm", round(fb_min - back_depth), "mm")

# Cluster sizes compared (the basis of the rework decided in SCM-DDR-002)
print("Alternative clusters: arm, wheel dia -> hub clearance n0/n32, arm clearance n0/n32, landing at 200, tread needed at 100")
_save = (a, r, d)
ALT = {}
for arm_alt, r_alt in ((135, 75), (135, 100), (150, 75), (150, 100), (165, 100)):
    a, r, d = arm_alt, r_alt, arm_alt * math.sqrt(3)
    s0, s32 = sweep(0.0), sweep(32.0)
    l200 = landing(200, 0.0)[0]
    t100 = r - landing(100, 0.0)[1]
    ALT[(arm_alt, r_alt)] = (s0, s32, l200, t100)
    print(f"  {arm_alt:3d} mm, {2 * r_alt:3d} mm: hub {s0[0]:4.0f}/{s32[0]:4.0f}, arms {s0[1]:4.0f}/{s32[1]:4.0f}, "
          f"landing {l200:4.0f}, tread {t100:4.0f} mm; hub height {r_alt + arm_alt / 2:.0f} mm")
    rec(f"alt_a{arm_alt}_w{2 * r_alt}_hub_n32_mm", round(s32[0]), "mm")
    rec(f"alt_a{arm_alt}_w{2 * r_alt}_arm_n32_mm", round(s32[1]), "mm")
a, r, d = _save
# ---------------------------------------------------------------- 4. Torque, speed and power
head("4. Torque, speed and power")
w_shaft = 2 * math.pi / 3 / (60.0 / STEPS_PER_MIN)          # rad/s
rpm_shaft = w_shaft * 60 / (2 * math.pi)
print(f"Shaft speed {w_shaft:.3f} rad/s ({rpm_shaft:.2f} rpm)")


def torque_profile(h, n, f_h):
    tmax = 0.0; tmean = []
    for ph, piv, hub, wheels in climb_states(h, n):
        t = W * abs(hub[0] - piv[0]) / 1000 + f_h * abs(hub[1] - piv[1]) / 1000
        tmax = max(tmax, t); tmean.append(t)
    return tmax, sum(tmean) / len(tmean)


# handle force from section 7 feeds the torque; compute the balance first
offs = [(hub[0] - piv[0]) for ph, piv, hub, w in climb_states(H_DESIGN, 0.0)] + [a * math.cos(math.radians(30))]
o_min, o_max = min(offs), max(offs)
c_set = -(o_max + o_min) / 2                   # CoM offset from the hub at the best set angle
swing = (o_max - o_min) / 2
shift = H_CG * math.sin(math.radians(WINDOW))


def handle_force(win_deg, model="horizontal", c=c_set):
    s = H_CG * math.sin(math.radians(win_deg))
    worst = 0.0
    for ph, piv, hub, w in climb_states(H_DESIGN, 0.0):
        o = abs(hub[0] - piv[0] + c) + s
        if model == "horizontal":
            lever = hub[1] - piv[1] + L_H * math.cos(math.radians(TILT))
        else:
            lever = abs(hub[0] - L_H * math.sin(math.radians(TILT)) - piv[0])
        worst = max(worst, W * o / 1000 / (lever / 1000))
    return worst


F_edge = handle_force(WINDOW)
t_static, t_mean_prof = torque_profile(H_DESIGN, 0.0, F_edge)
t_peak = t_static * DYN
lift_J = W * H_DESIGN / 1000
t_mean = lift_J / (2 * math.pi / 3)
p_shaft = t_peak * w_shaft
p_motor = p_shaft / (ETA_CHAIN * ETA_CHAIN2 * ETA_WORM)
ratio = D["ratio"]
gm_rpm = rpm_shaft * ratio
gm_torque = t_peak / (ratio * ETA_CHAIN * ETA_CHAIN2)
print(f"Lift work per step {lift_J:.0f} J; mean shaft torque {t_mean:.0f} N m")
print(f"Peak static shaft torque {t_static:.0f} N m (weight on the arm plus handle force), x{DYN} -> {t_peak:.0f} N m")
print(f"Peak shaft power {p_shaft:.0f} W; peak motor output {p_motor:.0f} W against {P_MOTOR:.0f} W rated "
      f"(margin {100 * (1 - p_motor / P_MOTOR):.0f} %)")
print(f"Chain ratio {D['ratio1']:.1f} x {D['ratio2']:.1f} = {ratio:.1f}:1; gearmotor {gm_rpm:.0f} rpm, {gm_torque:.1f} N m against {GM_RATED:.0f} N m rated")
for k, v, un in [("lift_work_J", round(lift_J), "J"), ("shaft_torque_mean_Nm", round(t_mean), "N m"),
                 ("shaft_torque_static_Nm", round(t_static), "N m"), ("shaft_torque_peak_Nm", round(t_peak), "N m"),
                 ("shaft_rpm", round(rpm_shaft, 2), "rpm"), ("shaft_power_peak_W", round(p_shaft), "W"),
                 ("motor_output_peak_W", round(p_motor), "W"), ("gearmotor_rpm", round(gm_rpm), "rpm"),
                 ("gearmotor_torque_Nm", round(gm_torque, 1), "N m")]:
    rec(k, v, un)
chain_t = t_peak / (D["sprocket_pd"] / 2000)
sf_chain = CHAIN_BREAK["08B"][1] / chain_t
t_cs = t_peak / (D["ratio2"] * ETA_CHAIN2)
chain1_t = t_cs / (D["cs1_pd"] / 2000)
sf_chain1 = CHAIN_BREAK["06B"][1] / chain1_t
spm_max = STEPS_PER_MIN * P_MOTOR / p_motor
print(f"Final stage 08B, {P['z_driven']}T on the shaft: chain pull {chain_t:.0f} N, safety factor {sf_chain:.1f}")
print(f"First stage 06B, {P['z_cs1']}T on the countershaft ({t_cs:.0f} N m): chain pull {chain1_t:.0f} N, "
      f"safety factor {sf_chain1:.1f}")
print(f"Fastest climb on the {P_MOTOR:.0f} W motor: {spm_max:.1f} steps/min")
print(f"Chain centres: final stage {D['c2']:.1f} mm for {P['links2']} links of 08B (whole chain needs {D['c2_whole']:.1f} mm); "
      f"first stage {D['c1']:.1f} mm for {P['links1']} links of 06B ({D['c1_whole']:.1f} mm); slots give 4 mm of take-up")
rec("centres_08B_mm", round(D["c2"], 1), "mm"); rec("centres_06B_mm", round(D["c1"], 1), "mm")
rec("chain_pull_08B_N", round(chain_t), "N"); rec("chain_sf_08B", round(sf_chain, 1))
rec("chain_pull_06B_N", round(chain1_t), "N"); rec("chain_sf_06B", round(sf_chain1, 1))
rec("steps_per_min_max_250W", round(spm_max, 1), "steps/min")
# Motor output the TRL 3 baseline rate of 20 steps/min would need with this cluster
p20 = p_motor * 20.0 / STEPS_PER_MIN
print(f"At 20 steps/min this cluster would need {p20:.0f} W from the motor")
rec("motor_output_at_20spm_W", round(p20), "W")

# ---------------------------------------------------------------- 5. Energy and endurance
head("5. Energy and endurance")
eta_up = ETA_DRV * ETA_MOT * ETA_WORM * ETA_CHAIN * ETA_CHAIN2
e_up = lift_J / eta_up
rho = math.degrees(math.atan(math.tan(math.radians(LEAD)) / ETA_WORM)) - LEAD
lower_ratio = math.tan(math.radians(rho - LEAD)) / math.tan(math.radians(LEAD))
e_down = lift_J * ETA_CHAIN * ETA_CHAIN2 * lower_ratio / (ETA_MOT * ETA_DRV)
e_use = E_PACK * DOD * 3600
n_steps = e_use / ((e_up + e_down) * STANDBY)
t_chg = E_PACK / (CHG_V * CHG_A * ETA_CHG) + CV_TAIL
print(f"Drive efficiency up {100 * eta_up:.1f} %; pack energy per loaded step up {e_up:.0f} J ({e_up / 3600:.2f} Wh)")
print(f"Worm friction angle {rho:.2f} deg (lead {LEAD:.0f} deg); lowering needs {100 * lower_ratio:.0f} % of the lift "
      f"work at the worm; pack energy per loaded step down {e_down:.0f} J")
print(f"Usable pack energy {e_use / 1000:.0f} kJ; loaded steps per charge, up and down: {n_steps:.0f}")
print(f"Typical day: {n_steps / 48:.0f} drops of three floors (48 steps); charge time {t_chg:.1f} h")
for k, v, un in [("energy_up_J", round(e_up), "J"), ("energy_down_J", round(e_down), "J"),
                 ("steps_per_charge", round(n_steps), "steps"), ("charge_time_h", round(t_chg, 1), "h"),
                 ("worm_friction_angle_deg", round(rho, 2), "deg")]:
    rec(k, v, un)
flow = [("Pack output", e_up), ("Driver output", e_up * ETA_DRV), ("Motor shaft", e_up * ETA_DRV * ETA_MOT),
        ("Worm output", e_up * ETA_DRV * ETA_MOT * ETA_WORM), ("Lift at clusters", lift_J)]
print("Energy flow per step up (J): " + ", ".join(f"{k} {v:.0f}" for k, v in flow))

# ---------------------------------------------------------------- 6. Holding (R8)
head("6. Holding on the stair")
t_hold = t_static
eta_back = 2 - 1 / ETA_WORM
brake_need = t_hold / (I_WORM * ratio)
print(f"Holding torque at the shaft {t_hold:.0f} N m; at the gearmotor output {t_hold / ratio:.1f} N m")
print(f"Worm back-drive efficiency 2 - 1/eta = {eta_back:.2f} (<= 0 means statically self-locking)")
print(f"Brake alone (worm assumed free, 100 % back-drive): needs {brake_need:.2f} N m at the motor; "
      f"{T_BRAKE:.1f} N m fitted -> margin {T_BRAKE / brake_need:.1f}x")
rec("hold_torque_Nm", round(t_hold), "N m"); rec("worm_backdrive_eff", round(eta_back, 2))
rec("brake_margin", round(T_BRAKE / brake_need, 1), "x")

# ---------------------------------------------------------------- 7. Balance and handle force (R6, R7, R10)
head("7. Balance and handle force")
print(f"Hub offset from the support wheel over a step: {o_min:.0f} to {o_max:.0f} mm; best set point puts the "
      f"CoM {-c_set:.0f} mm stair side of the hub; swing +/-{swing:.0f} mm")
print(f"CoM shift at the {WINDOW:.0f} deg window edge: {shift:.0f} mm")
F_set = handle_force(0.0)
F_vert = handle_force(WINDOW, "vertical")
win_ok = next(w / 10 for w in range(80, 0, -1) if handle_force(w / 10) <= F_HANDLE_MAX)
F_win_ok = handle_force(win_ok)
print(f"Horizontal grip force (courier uphill): {F_set:.0f} N at the set angle, {F_edge:.0f} N at the window edge")
print(f"Vertical grip force model (hand truck on the flat convention): {F_vert:.0f} N at the window edge")
print(f"Widest window meeting {F_HANDLE_MAX:.0f} N: +/-{win_ok:.1f} deg ({F_win_ok:.0f} N)")
push = CRR * W
print(f"Push force on the flat: {push:.0f} N")
for k, v, un in [("com_swing_mm", round(swing), "mm"), ("handle_force_set_N", round(F_set), "N"),
                 ("handle_force_edge_N", round(F_edge), "N"), ("handle_force_vertical_N", round(F_vert), "N"),
                 ("window_for_100N_deg", win_ok, "deg"), ("push_force_N", round(push), "N")]:
    rec(k, v, un)

# ---------------------------------------------------------------- 8. Structure (R1)
head("8. Structure")
ds = P["shaft_d"]
tau = 16 * t_peak * 1000 / (math.pi * ds ** 3)
y_brg = P["axle_plate_y"][0] - BRG["205"]["t"]          # main bearing centre, on the inside of the axle plates (SCM-DDR-003)
overhang = P["cluster_y"] - y_brg
m_b = SHOCK * W / 2 * overhang / 1000
sig = 32 * m_b * 1000 / (math.pi * ds ** 3)
vm = math.sqrt(sig ** 2 + 3 * tau ** 2)
sf_shaft = SY_SHAFT / (KT_KEY * vm)
print(f"Shaft {ds:.0f} mm: torsion {tau:.0f} MPa at {t_peak:.0f} N m; bending {sig:.0f} MPa at {SHOCK:.0f} g over "
      f"{overhang:.0f} mm; von Mises {vm:.0f} MPa; with Kt {KT_KEY:.0f} safety factor {sf_shaft:.1f} on yield")
f_wheel = SHOCK * W / 2
m_arm = f_wheel * a / 1000
z_arm = P["spider_t"] * P["arm_w"] ** 2 / 6
s_arm = m_arm * 1000 / z_arm
t_off = f_wheel * P["spider_off"] / 1000
bt = P["arm_w"] / P["spider_t"]
alpha = 0.333 * (1 - 0.63 / bt)
tau_arm = t_off * 1000 / (alpha * P["arm_w"] * P["spider_t"] ** 2)
vm_arm = math.sqrt(s_arm ** 2 + 3 * tau_arm ** 2)
print(f"Spider arm {P['arm_w']:.0f} x {P['spider_t']:.0f} mm: bending {s_arm:.0f} MPa, torsion from the {P['spider_off']:.0f} mm "
      f"wheel offset {tau_arm:.0f} MPa, von Mises {vm_arm:.0f} MPa at {SHOCK:.0f} g; safety factor {SY_PLATE / vm_arm:.1f}")
m_rail = F_edge * L_H / 1000 / 2
ro, ri = 14.0, 12.5
z_rail = math.pi * (ro ** 4 - ri ** 4) / (4 * ro)
s_rail = m_rail * 1000 / z_rail
print(f"Rail 28 x 1.5 mm tube: {m_rail:.0f} N m each from the window-edge grip force; {s_rail:.0f} MPa; "
      f"safety factor {SY_TUBE / s_rail:.1f}")
# Fatigue of the keyed cluster shaft (4140), added 2026-10-02 (SCM-DEC-001, item 1). Modified Goodman with the
# distortion-energy combination (Shigley form): bending is fully reversed once per revolution at the 1 g stair load
# on the bearing overhang; torque is pulsating from zero to the peak shaft torque at each step.
KF_B, KFS_T = 2.0, 2.0                                   # fatigue stress concentration of the end-milled keyway (bending, torsion)
ka = 4.51 * SUT_SHAFT ** -0.265                          # machined surface
kb = 1.24 * ds ** -0.107                                 # size, 25 mm
ke = 0.814                                               # 99 % reliability
se = 0.5 * SUT_SHAFT * ka * kb * ke
ma_1g = W / 2 * overhang / 1000                          # N m, alternating bending moment at 1 g
ta = tm = t_peak / 2
term_a = math.sqrt(4 * (KF_B * ma_1g) ** 2 + 3 * (KFS_T * ta) ** 2) * 1000
term_m = math.sqrt(3 * (KFS_T * tm) ** 2) * 1000
n_fat = 1 / (16 / (math.pi * ds ** 3) * (term_a / se + term_m / SUT_SHAFT))
sf_3g_static = SY_SHAFT / (KT_KEY * vm)
print(f"Cluster shaft in 4140 quenched and tempered (yield {SY_SHAFT:.0f} MPa, tensile {SUT_SHAFT:.0f} MPa assumed): safety factor on yield "
      f"{sf_3g_static:.1f} at 3 g (was 1.4 on 1018 at 370 MPa)")
print(f"Fatigue: endurance limit {se:.0f} MPa after surface {ka:.2f}, size {kb:.2f} and reliability {ke:.3f} factors; alternating bending "
      f"{ma_1g:.0f} N m at 1 g; pulsating torque 0 to {t_peak:.0f} N m; keyway Kf {KF_B:.1f} (bending) and {KFS_T:.1f} (torsion); "
      f"Goodman safety factor {n_fat:.1f} (needs more than 1 for a long life; to be confirmed with a mill certificate and, at TRL 4, a test)")
for k, v, un in [("shaft_fatigue_se_MPa", round(se), "MPa"), ("shaft_fatigue_sf_goodman", round(n_fat, 1), ""),
                 ("shaft_vm_MPa", round(vm), "MPa"), ("shaft_sf", round(sf_shaft, 1), ""), ("arm_vm_MPa", round(vm_arm), "MPa"),
                 ("arm_sf", round(SY_PLATE / vm_arm, 1), ""), ("rail_MPa", round(s_rail), "MPa"), ("rail_sf", round(SY_TUBE / s_rail, 1), "")]:
    rec(k, v, un)

# ---------------------------------------------------------------- 9. Mass and size (R5, R11)
head("9. Mass and size")
print("Mass roll-up: " + "; ".join(f"{k} {v:.2f}" for k, v in MASS.items()) + f" -> {m_truck:.1f} kg")
print("  Parts added for construction: " + "; ".join(f"{k} {v:.2f}" for k, v in MADE.items()))
print("  Drive itemised: " + "; ".join(f"{k} {v:.2f}" for k, v in DRIVE.items()) + f" -> {sum(DRIVE.values()):.2f} kg (was a 2.5 kg allowance)")
rec("drive_mass_kg", round(sum(DRIVE.values()), 2), "kg")
rec("added_parts_mass_kg", round(sum(MADE.values()), 2), "kg")
print(f"Width {D['width']:.0f} mm at the wheel faces, {D['width_bolts']:.0f} mm over the wheel end screws; upright height {D['height_upright']:.0f} mm")
rec("width_over_screws_mm", round(D["width_bolts"]), "mm")
print(f"Option C folding hinge {P['fold_z']:.0f} mm above the shaft: folded height {D['folded_height']:.0f} mm "
      f"(about +0.4 kg, +$20; study only)")
rec("width_mm", round(D["width"]), "mm"); rec("height_upright_mm", round(D["height_upright"]), "mm")
rec("folded_height_mm", round(D["folded_height"]), "mm")

# ---------------------------------------------------------------- 10. Cost (R12)
head("10. Cost")
rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
cost = sum(float(x["qty"]) * float(x["unit_cost_usd"]) for x in rows)
print(f"BOM lines {len(rows)}, estimated cost USD {cost:.2f}; value-engineering target USD {BUDGET:.0f} "
      f"(USD {abs(cost - BUDGET):.0f} {'over' if cost > BUDGET else 'under'} the target)")
rec("bom_total_usd", round(cost, 2), "USD")

# ---------------------------------------------------------------- 11. Requirements
REQ = [
    ("R1", "Rated stair load", "60 kg up and down; 100 kg on the flat",
     f"Shaft SF {sf_shaft:.1f} (fatigue {n_fat:.1f}), spider SF {SY_PLATE / vm_arm:.1f}, rail SF {SY_TUBE / s_rail:.1f} at {SHOCK:.0f} g", "met"),
    ("R2", "Stair range", "Risers 100 to 200 mm, treads 250 mm or more, nosing up to 32 mm",
     f"Landing {landing(200, 0)[0]:.0f} mm past the nosing at 200 mm; tread needed {r - landing(100, 0)[1]:.0f} mm; "
     f"arms clear nosings up to {n_arm_ok} mm overhang", "met" if n_arm_ok >= 32 else "not met"),
    ("R3", "Climb speed", f"{STEPS_PER_MIN:.0f} steps/min or more at rated load",
     f"{p_motor:.0f} W peak motor output on a {P_MOTOR:.0f} W motor", "met" if p_motor <= P_MOTOR else "not met"),
    ("R4", "Endurance", "1,000 loaded steps up plus 1,000 down per charge", f"{n_steps:,.0f}", "met"),
    ("R5", "Truck mass", f"{R5_MAX:.0f} kg or less; pack 3 kg or less", f"{m_truck:.1f} kg; pack {MASS['7 pack and cradle']} kg",
     "met" if m_truck <= R5_MAX else "not met"),
    ("R6", "Operator handle force", "100 N or less inside the tilt window",
     f"{F_edge:.0f} N at the +/-{WINDOW:.0f} deg edge; {F_set:.0f} N at the set angle",
     "met" if F_edge <= F_HANDLE_MAX else "not met"),
    ("R7", "Tilt control", f"100 Hz IMU, +/-{WINDOW:.0f} deg window, stop within 0.2 s", "Control concept only", "not verifiable at TRL 3"),
    ("R8", "Hold on any loss", "Holds with power off; drift 5 mm or less in 10 min",
     f"Worm self-locking (back-drive {eta_back:.2f}); brake margin {T_BRAKE / brake_need:.1f}x; drift unmeasured",
     "not verifiable at TRL 3"),
    ("R9", "Hold-to-run", "Stops within 0.2 s of grip release", "Circuit concept only", "not verifiable at TRL 3"),
    ("R10", "Flat rolling", "40 N or less at rated load", f"{push:.0f} N", "met"),
    ("R11", "Size", "Width 600 mm or less; upright height 1,500 mm or less",
     f"{D['width_bolts']:.0f} mm over the wheel screws; {D['height_upright']:.0f} mm",
     "met" if D["width_bolts"] <= 600 and D["height_upright"] <= 1500 else "not met"),
    ("R12", "Affordable", f"Value-engineering target USD {BUDGET:.0f}", f"USD {cost:.0f}",
     "under the target" if cost <= BUDGET else f"over the target by USD {cost - BUDGET:.0f}"),
    ("R13", "Battery", "24 V LiFePO4, BMS, fused, 0 to 45 degC charge window, 4 h charge", f"{t_chg:.1f} h", "met"),
    ("R14", "Environment", "0 to 40 degC, IP54, rain on stoops", "Enclosure concept only", "not verifiable at TRL 3"),
    ("R15", "Stair and building protection", "No steel contact with stairs; skids over nosings",
     f"{P['z_driven']}T sprocket guard radius {D['guard_r']:.1f} mm against {env_exact:.1f} mm allowed; "
     f"countershaft guard clears by {cs_min - D['cs_guard_r']:.0f} mm; every frame-fixed outline at least "
     f"{min(outline_clear.values()):.0f} mm from every nosing",
     "met" if D["guard_r"] <= env_exact and cs_min > D["cs_guard_r"] + ENV_MARGIN and all_outlines_ok else "not met"),
]
head("11. Requirements")
for rid, name, tgt, val, st in REQ:
    print(f"{rid:4s} {st:24s} {val}")
counts = {}
for *_, st in REQ:
    counts[st] = counts.get(st, 0) + 1
print("Counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()))

with (Path(__file__).parent / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["key", "value", "unit"])
    w.writerows(OUT)
    w.writerow([])
    w.writerow(["requirement", "name", "target", "value", "status"])
    w.writerows(REQ)
print("\nWrote docs/04-calcs/results.csv")

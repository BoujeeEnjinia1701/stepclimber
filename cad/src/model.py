"""StepClimber parametric model (build123d), TRL 3, constructable design (SCM-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl, print envelopes and checks
    python cad/src/model.py --check    run the constructability checks only

Every component is a single made or bought piece (or a matched set of fixings), so the build
plan pictures (cad/src/build_plan_media.py) and the constructability checks use the same parts.
SCM-DDR-002 set the cluster and drive; SCM-DDR-003 records what changed to make it buildable:
axle plates and a closed chain case on the frame, four flange bearings, a countershaft carried
at both ends and moved 15 mm toward the stair side, chain centres set to whole chains, weld-on
hubs and stub axles on the spiders, component uprights, skid standoffs, the lowest cross bar
moved, and a worm gearmotor whose motor stands up the frame.

Axes (upright pose, as stored in a van): X toward the load side (toe plate), Y across the
truck (+Y is the drive side), Z up, floor at Z = 0. The cluster shaft sits at X = 0,
Z = hub height with two wheels of each cluster on the floor. The frame back (stair side while
climbing) faces -X. `tilted()` returns the same parts rotated back about the shaft to the
climbing angle. Heights in PARAMS marked "rel" are measured up the frame from the shaft line.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # Tri-star clusters (SCM-PRC-001 v0.4; rework decided 2026-09-25, SCM-DDR-002)
    "wheel_r": 100.0,          # 200 mm solid rubber wheels
    "wheel_w": 45.0,
    "wheel_hub_l": 45.0,       # wheel hub length (bearings 20 mm bore)
    "arm": 150.0,              # cluster hub to wheel centre
    "arm_w": 45.0,             # spider arm width
    "spider_t": 6.0,           # laser-cut steel spider plate
    "spider_disc_r": 48.0,     # spider centre disc round the weld-on hub (inside the 54.2 mm envelope)
    "boss_r": 38.0,            # weld-on taper-lock hub, outside radius
    "boss_l": 26.0,
    "cluster_y": 262.0,        # wheel mid-plane half-spacing
    "spider_off": 30.0,        # spider mid-plane inboard of the wheel mid-plane
    "stub_r": 10.0,            # 20 mm stub axle
    # Shaft and two-stage chain drive (SCM-CAL-001 v0.3 section 4)
    "shaft_d": 25.0,
    "shaft_half": 245.0,       # shaft ends at +/- this Y (flush with the hub outer faces)
    "bearing_r": 45.0,         # flange bearing housing envelope radius (nosing check)
    "chain_pitch": 12.7,       # final stage 08B
    "z_driven": 20, "z_cs2": 10,
    "chain1_pitch": 9.525,     # first stage 06B
    "z_cs1": 35, "z_drive": 10,
    "links2": 38, "links1": 54,  # whole chains with even link counts (SCM-DDR-003, P6)
    "cs_x": -15.0,             # countershaft and gearmotor output toward the stair side of the shaft line (P5)
    "cs_z": 143.9,             # countershaft up the frame from the shaft (38 links of 08B)
    "gm_z": 289.0,             # gearmotor output up the frame (54 links of 06B from the countershaft)
    "chain_c": 289.0,          # kept for older scripts: gearmotor output above the shaft
    "guard_gap": 10.0,         # sprocket tip to chain case clearance
    "sprocket_y": 110.0,       # first stage (06B) plane
    "sprocket2_y": 133.0,      # final stage (08B) plane
    # Chain case and axle plates (SCM-DDR-003, P1 to P4)
    "plate_y": (183.0, 186.0), # case outer plate (drive-side axle plate), 3 mm steel, welded to the inside of the rail
    "axle_plate_y": (182.0, 186.0),  # plain-side axle plate, 4 mm steel, welded to the inside of the rail
    "inner_y": (94.0, 97.0),   # case inner plate, 3 mm aluminium, bolted
    "band_t": 1.5,             # case band, 1.5 mm aluminium
    "case_clip_x": 52.0,       # load-side limit of the case (rails at 26 to 54)
    "gm_lobe_r": 60.0,
    "spacer_r": 8.0, "spacer_dx": 40.0, "spacer_z": 262.0,
    # Frame (bought steel hand truck, modified)
    "rail_y": 200.0, "rail_r": 14.0, "rail_x": 40.0,
    "rail_below": 142.5, "frame_h": 1150.0, "handle_rise": 110.0, "handle_x": -40.0, "grip_r": 16.0,
    "bar_r": 11.0, "bars": (380.0, 700.0, 1000.0),  # cross bars kept (rel)
    "bar_cut": 60.0,           # the cross bar cut off (rel)
    "low_bar": -105.0,         # replacement lowest cross bar (rel)
    "toe_l": 240.0, "toe_w": 380.0, "toe_t": 8.0,
    # Gearmotor (worm, motor standing up the frame)
    "gm_box": (95.0, 90.0, 95.0), "gm_y0": 4.0,
    "motor_r": 42.0, "motor_l": 150.0, "motor_x": -25.0,
    # Component uprights and parts on them (rel heights)
    "up_y": 120.0, "up_w": 30.0, "up_t": 6.0,
    "ebox_z": 550.0, "ebox": (50.0, 340.0, 110.0),
    "pack_z": 800.0, "pack": (75.0, 180.0, 170.0),
    "switch_z": 660.0,
    "skid_x": -100.0, "skid_z": (40.0, 540.0), "skid_y": 200.0, "standoff_z": (140.0, 510.0),
    "strap_z": 650.0, "strap_reach": 260.0,
    # Pose
    "tilt": 30.0,
    "fold_z": 950.0,           # Option C folding hinge height (study only)
}


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought" or "fixing"
    group: str         # key of the concept-media group (build() groups components by it)


def _chain_c(n, p, z1, z2):
    lo, hi = 10.0, 2000.0
    for _ in range(80):
        m = (lo + hi) / 2
        L = 2 * m / p + (z1 + z2) / 2 + ((z2 - z1) / (2 * math.pi)) ** 2 * p / m
        lo, hi = (m, hi) if L < n else (lo, m)
    return lo


def derived(p=PARAMS):
    """Key derived dimensions, shared with docs/04-calcs/sizing.py (no build123d needed)."""
    a, r = p["arm"], p["wheel_r"]
    hub_z = r + a * math.sin(math.radians(30))
    pd = lambda n, t=p["chain_pitch"]: t / math.sin(math.pi / n)  # noqa: E731
    od = lambda n, t=p["chain_pitch"]: t * (0.6 + 1 / math.tan(math.pi / n))  # noqa: E731
    t1 = p["chain1_pitch"]
    width = 2 * (p["cluster_y"] + p["wheel_w"] / 2)
    top = hub_z + p["frame_h"] + p["handle_rise"] + p["grip_r"]
    c2 = math.hypot(p["cs_x"], p["cs_z"])
    c1 = p["gm_z"] - p["cs_z"]
    return {
        "spacing": a * math.sqrt(3), "hub_z": hub_z, "cluster_dia": 2 * (a + r),
        "sprocket_pd": pd(p["z_driven"]), "sprocket_od": od(p["z_driven"]),
        "cs2_pd": pd(p["z_cs2"]), "cs2_od": od(p["z_cs2"]),
        "cs1_pd": pd(p["z_cs1"], t1), "cs1_od": od(p["z_cs1"], t1),
        "drive_pd": pd(p["z_drive"], t1), "drive_od": od(p["z_drive"], t1),
        "ratio1": p["z_cs1"] / p["z_drive"], "ratio2": p["z_driven"] / p["z_cs2"],
        "ratio": (p["z_cs1"] / p["z_drive"]) * (p["z_driven"] / p["z_cs2"]),
        "guard_r": od(p["z_driven"]) / 2 + p["guard_gap"],
        "cs_guard_r": od(p["z_cs1"], t1) / 2 + p["guard_gap"],
        "c2": c2, "c1": c1,
        "c2_whole": _chain_c(p["links2"], p["chain_pitch"], p["z_cs2"], p["z_driven"]),
        "c1_whole": _chain_c(p["links1"], t1, p["z_drive"], p["z_cs1"]),
        "width": width, "width_bolts": 2 * (p["cluster_y"] + p["wheel_w"] / 2 + 3 + 6.4),
        "height_upright": top,
        "handle_len": p["frame_h"] + p["handle_rise"],
        "folded_height": hub_z + p["fold_z"] + p["rail_r"],
    }


# ------------------------------------------------------------------ 2D outlines (shapely, no build123d)
def case_outline(p=PARAMS):
    """Chain case and drive-side axle plate outline in the frame plane: shapely Polygon in
    (x, z rel) mm, shaft at (0, 0)."""
    from shapely.geometry import Point, box as sbox
    from shapely.ops import unary_union
    D = derived(p)
    cs, gm = (p["cs_x"], p["cs_z"]), (p["cs_x"], p["gm_z"])
    blobs = [Point(0, 0).buffer(D["guard_r"], 64), Point(*cs).buffer(D["cs_guard_r"], 64),
             Point(*gm).buffer(p["gm_lobe_r"], 64), Point(0, -49.5).buffer(20, 32)]
    hull = unary_union(blobs).convex_hull
    return hull.intersection(sbox(-500, -500, p["case_clip_x"], 1000))


def axle_plate_outline(p=PARAMS):
    """Plain-side axle plate outline (x, z rel): 92 x 144 mm with 15 mm corners."""
    from shapely.geometry import box as sbox
    return sbox(-25, -57, 37, 57).buffer(15, 16)


def flange_outline(bolt, r_mid, r_end):
    """Two-bolt flange bearing outline, long axis up the frame (x, z) about its own centre."""
    from shapely.geometry import Point
    from shapely.ops import unary_union
    return unary_union([Point(0, 0).buffer(r_mid, 48), Point(0, bolt).buffer(r_end, 24),
                        Point(0, -bolt).buffer(r_end, 24)]).convex_hull


BRG = {  # two-bolt flange units: bolt half-spacing, mid and end radii, flange and boss thickness, insert width and radius
    "205": dict(bolt=49.5, r_mid=37.0, r_end=15.0, t=13.0, boss_r=33.0, boss_t=13.0, ins_w=34.0, ins_r=19.0, bolt_d=12.0),
    "204": dict(bolt=45.0, r_mid=30.0, r_end=13.0, t=11.0, boss_r=28.0, boss_t=11.0, ins_w=31.0, ins_r=16.0, bolt_d=10.0),
}


# ------------------------------------------------------------------ build123d helpers
def _b():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def bx(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def ycyl(x, y0, y1, z, r):
    """Cylinder along Y from y0 to y1."""
    b = _b()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, abs(y1 - y0))


def zcyl(x, y, z0, z1, r):
    b = _b()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, abs(z1 - z0))


def xcyl(x0, x1, y, z, r):
    b = _b()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, abs(x1 - x0))


def tube(a, c, r):
    b = _b()
    a = b.Vector(*a); c = b.Vector(*c); d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def yhex(x, y0, y1, z, af):
    b = _b()
    s = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), abs(y1 - y0) / 2, both=True)
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * s


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def poly_y(poly, y0, y1, z0, holes=()):
    """Extrude a shapely polygon in (x, z rel) from y0 to y1, at hub height z0. holes: (x, z, r) or
    (x, z, r, slot_half_length) slots running up the frame."""
    b = _b()
    pts = list(poly.exterior.coords)[:-1]
    f = b.Face(b.Wire.make_polygon([b.Vector(x, y0, z0 + z) for x, z in pts], close=True))
    s = b.extrude(f, y1 - y0, dir=(0, 1, 0))
    for h in holes:
        x, z, r = h[:3]
        sl = h[3] if len(h) > 3 else 0.0
        cut = ycyl(x, y0 - 1, y1 + 1, z0 + z, r)
        if sl:
            cut = fuse([cut, ycyl(x, y0 - 1, y1 + 1, z0 + z - sl, r), ycyl(x, y0 - 1, y1 + 1, z0 + z + sl, r),
                        bx(x - r, x + r, y0 - 1, y1 + 1, z0 + z - sl, z0 + z + sl)])
        s = s - cut
    return s


def _rot_cluster(shape, deg, z0):
    """Rotate a cluster part about the shaft axis (Y) by deg."""
    b = _b()
    return b.Pos(0, 0, z0) * b.Rot(0, deg, 0) * b.Pos(0, 0, -z0) * shape


# ------------------------------------------------------------------ components
def bearing(kind, x, z, face_y, side, z0):
    """Two-bolt flange bearing with its flange on a plate face at face_y; the housing stands
    toward `side` (+1 or -1 in Y). Returns (bearing, bolts) at hub height z0."""
    b = _b()
    g = BRG[kind]
    fl = flange_outline(g["bolt"], g["r_mid"], g["r_end"])
    y_far = face_y + side * g["t"]
    flange = poly_y(fl, min(face_y, y_far), max(face_y, y_far), 0)
    flange = b.Pos(x, 0, z0 + z) * flange
    by = face_y + side * (g["t"] + g["boss_t"])
    boss = ycyl(x, y_far, by, z0 + z, g["boss_r"])
    ymid = face_y + side * (g["t"] + g["boss_t"]) / 2
    ins = ycyl(x, ymid - g["ins_w"] / 2, ymid + g["ins_w"] / 2, z0 + z, g["ins_r"])
    shaft_r = 12.5 if kind == "205" else 10.0
    body = fuse([flange, boss, ins]) - ycyl(x, ymid - 30, ymid + 30, z0 + z, shaft_r)
    for dz in (-g["bolt"], g["bolt"]):
        body = body - ycyl(x, face_y - 20, face_y + 20, z0 + z + dz, g["bolt_d"] / 2 + 0.5)
    return body, ymid


def bolt_y(x, z, y_head, y_nut, d, head_side):
    """Hex bolt along Y: head bearing on y_head (standing away from the joint, toward head_side),
    nut bearing on y_nut. Shank from head to nut, clear in its holes."""
    af = {5: 8, 6: 10, 8: 13, 10: 16, 12: 18}[int(d)]
    hk = 0.7 * d
    s = -head_side
    head = yhex(x, y_head, y_head + head_side * hk, z, af)
    nut = yhex(x, y_nut, y_nut + s * 0.9 * d, z, af)
    shank = ycyl(x, y_head, y_nut, z, d / 2)
    return fuse([head, shank, nut])


def build_components(p=PARAMS):
    """Return {key: Comp} for every component in the upright pose."""
    b = _b()
    from shapely.geometry import LineString, Point
    from shapely.ops import unary_union
    D = derived(p)
    Z0 = D["hub_z"]
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    rx, ry, rr = p["rail_x"], p["rail_y"], p["rail_r"]
    ztop = Z0 + p["frame_h"]
    gz = ztop + p["handle_rise"]
    hx = p["handle_x"]

    # ---- 1 Frame, as bought, with the cross bar at 60 mm cut off
    fr = [tube((rx, s * ry, Z0 - p["rail_below"]), (rx, s * ry, ztop), rr) for s in (-1, 1)]
    fr += [b.Pos(rx, s * ry, ztop) * b.Sphere(rr) for s in (-1, 1)]
    fr += [tube((rx, -ry, Z0 + dz), (rx, ry, Z0 + dz), p["bar_r"]) for dz in p["bars"]]
    fr += [tube((rx, s * ry, ztop), (hx, s * 150, gz), rr) for s in (-1, 1)]
    fr += [b.Pos(hx, s * 150, gz) * b.Sphere(rr) for s in (-1, 1)]
    fr += [tube((hx, -150, gz), (hx, 150, gz), p["grip_r"])]
    zt = Z0 - p["rail_below"]
    fr += [bx(30, 30 + p["toe_l"], -p["toe_w"] / 2, p["toe_w"] / 2, zt - p["toe_t"], zt)]
    add("frame", "Hand truck frame and toe plate (bought)", fuse(fr), 1, "bought", "frame")
    rails = fuse([tube((rx, s * ry, Z0 - p["rail_below"] - 1), (rx, s * ry, ztop + 1), rr) for s in (-1, 1)])
    zl = Z0 + p["low_bar"]
    low = tube((rx, -ry, zl), (rx, ry, zl), p["bar_r"]) - rails
    add("low_bar", "Replacement lowest cross bar", low, 16, "made", "frame")

    # ---- 14 Axle plates and chain case
    py0, py1 = p["plate_y"]
    iy0, iy1 = p["inner_y"]
    cs, gm = (p["cs_x"], p["cs_z"]), (p["cs_x"], p["gm_z"])
    g5, g4 = BRG["205"], BRG["204"]
    main_holes = [(0, 0, 22.0)] + [(0, s * g5["bolt"], g5["bolt_d"] / 2 + 0.5) for s in (-1, 1)]
    cs_holes = [(cs[0], cs[1], 18.0, 4.0)] + [(cs[0], cs[1] + s * g4["bolt"], g4["bolt_d"] / 2 + 0.5, 4.0) for s in (-1, 1)]
    sp = [(cs[0] + s * p["spacer_dx"], p["spacer_z"]) for s in (-1, 1)]
    sp_holes = [(x, z, 4.5) for x, z in sp]
    gm_bolts = [(gm[0] - 40, gm[1]), (gm[0] + 40, gm[1]), (gm[0], gm[1] + 40)]
    ay0, ay1 = p["axle_plate_y"]
    left = poly_y(axle_plate_outline(p), -ay1, -ay0, Z0, main_holes)
    add("axle_plate", "Axle plate, plain side", left, 14, "made", "drive")
    outline = case_outline(p)
    outer = poly_y(outline, py0, py1, Z0, main_holes + cs_holes + sp_holes)
    add("case_outer", "Chain case outer plate (drive-side axle plate)", outer, 14, "made", "drive")
    inner = poly_y(outline, iy0, iy1, Z0, [(0, 0, 16.0)] + cs_holes + sp_holes + [(gm[0], gm[1], 14.0)]
                   + [(x, z, 4.5, 4.0) for x, z in gm_bolts])
    add("case_inner", "Chain case inner plate", inner, 14, "made", "drive")
    band = poly_y(outline, iy1, py0, Z0) - poly_y(outline.buffer(-p["band_t"], 32), iy1 - 1, py0 + 1, Z0)
    add("case_band", "Chain case band", band, 14, "made", "drive")
    spacers = fuse([ycyl(x, iy1, py0, Z0 + z, p["spacer_r"]) for x, z in sp])
    add("spacers", "Case spacers (2), tapped M8", spacers, 14, "made", "drive")
    sp_fix = fuse([fuse([ycyl(x, iy0 - 4.4, iy0, Z0 + z, 7.0), ycyl(x, iy0, iy1, Z0 + z, 4.0),
                         ycyl(x, py0, py1, Z0 + z, 4.0)]) for x, z in sp])
    add("spacer_screws", "M8 screws for the spacers", sp_fix, 17, "fixing", "drive")

    # ---- 3 Bearings, shafts, sprockets, chains
    brg_l, yl = bearing("205", 0, 0, -ay0, +1, Z0)
    brg_r, yr = bearing("205", 0, 0, py0, -1, Z0)
    add("brg_main_l", "Main shaft flange bearing, plain side", brg_l, 3, "bought", "drive")
    add("brg_main_r", "Main shaft flange bearing, drive side", brg_r, 3, "bought", "drive")
    brg_co, _ = bearing("204", cs[0], cs[1], py0, -1, Z0)
    brg_ci, _ = bearing("204", cs[0], cs[1], iy0, -1, Z0)
    add("brg_cs_out", "Countershaft flange bearing, outer", brg_co, 3, "bought", "drive")
    add("brg_cs_in", "Countershaft flange bearing, inner", brg_ci, 3, "bought", "drive")
    bb = []
    for s in (-1, 1):
        face = s * (py0 if s > 0 else ay0)
        for dz in (-g5["bolt"], g5["bolt"]):
            bb.append(bolt_y(0, Z0 + dz, face - s * g5["t"], s * py1, 12, -s))
    for dz in (-g4["bolt"], g4["bolt"]):
        bb.append(bolt_y(cs[0], Z0 + cs[1] + dz, py0 - g4["t"], py1, 10, -1))
        # inner countershaft bearing: countersunk screws flush with the case side of the inner plate, nuts on the flange
        zz = Z0 + cs[1] + dz
        bb.append(fuse([ycyl(cs[0], iy0 - g4["t"], iy1, zz, 5.0), yhex(cs[0], iy0 - g4["t"] - 9, iy0 - g4["t"], zz, 16)]))
    add("brg_bolts", "Bearing bolts (M12 and M10, nyloc nuts)", fuse(bb), 17, "fixing", "drive")
    sh = ycyl(0, -p["shaft_half"], p["shaft_half"], Z0, p["shaft_d"] / 2)
    add("shaft", "Cluster shaft, 25 mm keyed, 4140 quenched and tempered", sh, 3, "bought", "drive")
    csy0 = iy0 - g4["t"] - g4["boss_t"] / 2 - g4["ins_w"] / 2
    add("cs_shaft", "Countershaft, 20 mm keyed", ycyl(cs[0], csy0, py1, Z0 + cs[1], 10.0), 3, "bought", "drive")
    y1, y2 = p["sprocket_y"], p["sprocket2_y"]

    def sprocket(x, z, od, y, t, bore, hub_r, hub_y0, hub_y1):
        disc = ycyl(x, y - t / 2, y + t / 2, Z0 + z, od / 2)
        hub = ycyl(x, hub_y0, hub_y1, Z0 + z, hub_r)
        return fuse([disc, hub]) - ycyl(x, min(hub_y0, y - t) - 1, max(hub_y1, y + t) + 1, Z0 + z, bore)
    t8, t6 = 7.2, 5.3
    s_main = sprocket(0, 0, D["sprocket_od"], y2, t8, 12.5, 22.0, y2 - t8 / 2 - 12, y2)
    add("spr_main", f"{p['z_driven']}-tooth 08B sprocket (cluster shaft)", s_main, 3, "bought", "drive")
    s_cs1 = sprocket(cs[0], cs[1], D["cs1_od"], y1, t6, 10.0, 18.0, y1, y1 + t6 / 2 + 6.5)
    s_cs2 = sprocket(cs[0], cs[1], D["cs2_od"], y2, t8, 10.0, 13.5, y1 + t6 / 2 + 6.5, y2)
    add("spr_cs", "Countershaft sprockets: 35-tooth 06B and 10-tooth 08B", fuse([s_cs1, s_cs2]), 3, "bought", "drive")
    s_gm = sprocket(gm[0], gm[1], D["drive_od"], y1, t6, 10.0, 12.0, y1, y1 + t6 / 2 + 11)
    add("spr_gm", "10-tooth 06B sprocket (gearmotor)", s_gm, 3, "bought", "drive")

    def chain(c0, r0, c1, r1, y, h, w):
        outer = unary_union([Point(*c0).buffer(r0 + h, 48), Point(*c1).buffer(r1 + h, 48)]).convex_hull
        inner = unary_union([Point(*c0).buffer(r0 - h, 48), Point(*c1).buffer(r1 - h, 48)]).convex_hull
        return poly_y(outer, y - w / 2, y + w / 2, Z0) - poly_y(inner, y - w / 2 - 1, y + w / 2 + 1, Z0)
    ch2 = chain((0, 0), D["sprocket_pd"] / 2, cs, D["cs2_pd"] / 2, y2, 5.9, 17.0)
    ch1 = chain(cs, D["cs1_pd"] / 2, gm, D["drive_pd"] / 2, y1, 4.1, 13.0)
    add("chain2", f"08B chain, {p['links2']} links (final stage)", ch2, 3, "bought", "drive")
    add("chain1", f"06B chain, {p['links1']} links (first stage)", ch1, 3, "bought", "drive")

    # ---- 4 Worm gearmotor with brake: gearbox face bolted to the inside of the inner plate
    gx, gyl, gzz = p["gm_box"]
    gb = bx(gm[0] - gx / 2, gm[0] + gx / 2, p["gm_y0"], iy0, Z0 + gm[1] - gzz / 2, Z0 + gm[1] + gzz / 2)
    out_sh = ycyl(gm[0], iy0, y1 + t6 / 2 + 11, Z0 + gm[1], 10.0)
    ymc = (p["gm_y0"] + iy0) / 2
    can = zcyl(p["motor_x"], ymc, Z0 + gm[1] + gzz / 2, Z0 + gm[1] + gzz / 2 + p["motor_l"], p["motor_r"])
    add("gearmotor", "Worm gearmotor with brake, 24 V", fuse([gb, out_sh, can]), 4, "bought", "gearmotor")
    gmb = fuse([fuse([ycyl(x, iy1, iy1 + 4.4, Z0 + z, 6.5), ycyl(x, iy0 - 12, iy1, Z0 + z, 4.0)]) for x, z in gm_bolts])
    add("gm_bolts", "Gearmotor screws (3 x M8)", gmb, 17, "fixing", "gearmotor")

    # ---- 2 Clusters: spider, weld-on hub, stub axles, wheels, wheel fixings
    a = p["arm"]
    angs = (90, 210, 330)
    wpts = [(a * math.cos(math.radians(t)), a * math.sin(math.radians(t))) for t in angs]
    prof = unary_union([LineString([(0, 0), w]).buffer(p["arm_w"] / 2, 32) for w in wpts] +
                       [Point(0, 0).buffer(p["spider_disc_r"], 64)])
    for side in (1, -1):
        tag = "r" if side > 0 else "l"
        yw = side * p["cluster_y"]
        ys = yw - side * p["spider_off"]
        t = p["spider_t"]
        sy0, sy1 = sorted((ys - t / 2, ys + t / 2))
        holes = [(0, 0, p["boss_r"])] + [(x, z, p["stub_r"]) for x, z in wpts]
        add(f"spider_{tag}", f"Spider ({'drive' if side > 0 else 'plain'} side)", poly_y(prof, sy0, sy1, Z0, holes), 2, "made", "clusters")
        hy = (ys - p["boss_l"] / 2, ys + p["boss_l"] / 2)
        hub = ycyl(0, hy[0], hy[1], Z0, p["boss_r"]) - ycyl(0, hy[0] - 1, hy[1] + 1, Z0, p["shaft_d"] / 2)
        add(f"hub_{tag}", f"Weld-on taper-lock hub ({'drive' if side > 0 else 'plain'} side)", hub, 2, "bought", "clusters")
        inner_face = ys - side * t / 2
        wy = sorted((yw - p["wheel_w"] / 2, yw + p["wheel_w"] / 2))
        w_in, w_out = (wy[0], wy[1]) if side > 0 else (wy[1], wy[0])
        stub_end = w_out - side * 0.5
        stubs = fuse([ycyl(x, inner_face, stub_end, Z0 + z, p["stub_r"]) for x, z in wpts])
        add(f"stubs_{tag}", "Stub axles (3)", stubs, 2, "made", "clusters")
        wheels = []
        for x, z in wpts:
            w = ycyl(x, wy[0], wy[1], Z0 + z, p["wheel_r"]) - ycyl(x, wy[0] - 1, wy[1] + 1, Z0 + z, p["stub_r"])
            wheels.append(w)
        add(f"wheels_{tag}", "Solid rubber wheels (3)", fuse(wheels), 2, "bought", "clusters")
        outer_face = ys + side * t / 2
        fx = []
        for x, z in wpts:
            fx.append(ycyl(x, outer_face, w_in, Z0 + z, 15.0) - ycyl(x, outer_face - 1, w_in + 1, Z0 + z, p["stub_r"]))
            fx.append(ycyl(x, w_out, w_out + side * 3, Z0 + z, 18.0))
            fx.append(yhex(x, w_out + side * 3, w_out + side * 9.4, Z0 + z, 16))
        add(f"wheel_fix_{tag}", "Spacers, washers and M10 end screws", fuse(fx), 17, "fixing", "clusters")

    # ---- 15 Component uprights, electronics box, pack cradle, switch box
    xb = rx - p["bar_r"]                       # back of the cross bars
    ut, uw = p["up_t"], p["up_w"]
    zu0, zu1 = Z0 + p["bars"][0] - p["bar_r"], Z0 + p["bars"][2] + p["bar_r"]
    ups = fuse([bx(xb - ut, xb, s * p["up_y"] - uw / 2, s * p["up_y"] + uw / 2, zu0, zu1) for s in (-1, 1)])
    add("uprights", "Component uprights (2)", ups, 15, "made", "electronics")
    upb = fuse([xcyl(xb - ut - 4, rx + p["bar_r"] + 4, s * p["up_y"], Z0 + dz, 3.0) for s in (-1, 1) for dz in p["bars"]])
    add("up_bolts", "Upright bolts (6 x M6 through the cross bars)", upb, 17, "fixing", "electronics")
    xf = xb - ut                                  # front of the parts hung on the uprights
    ex, ey, ez = p["ebox"]
    ezc = Z0 + p["ebox_z"]
    shell = bx(xf - ex, xf, -ey / 2, ey / 2, ezc - ez / 2, ezc + ez / 2)
    shell = shell - bx(xf - ex + 2.5, xf - 2.5, -ey / 2 + 2.5, ey / 2 - 2.5, ezc - ez / 2 + 2.5, ezc + ez / 2 - 2.5)
    add("ebox", "Electronics box (IP54), drilled", shell, 13, "bought", "driver")
    boards = fuse([bx(xf - 14, xf - 4, -150, -10, ezc - 40, ezc + 40),
                   bx(xf - 14, xf - 4, 10, 150, ezc - 35, ezc + 35)])
    stand = fuse([xcyl(xf - 4, xf - 2.5, y, ezc + dz, 3.0) for y in (-140, -20, 20, 140) for dz in (-30, 30)])
    add("driver", "Motor driver and controller boards, on standoffs", fuse([boards, stand]), 5, "bought", "driver")
    px, pyy, pz = p["pack"]
    pzc = Z0 + p["pack_z"]
    cradle = fuse([bx(xf - 3, xf, -130, 130, pzc - pz / 2 - 10, pzc + pz / 2 + 10),
                   bx(xf - px, xf - 3, -95, 95, pzc - pz / 2 - 5, pzc - pz / 2),
                   bx(xf - px, xf - px + 3, -95, 95, pzc - pz / 2 - 5, pzc - pz / 2 + 15)])
    add("cradle", "Pack cradle (with the pack)", cradle, 7, "bought", "pack")
    pack = bx(xf - px + 3, xf - 3, -pyy / 2, pyy / 2, pzc - pz / 2, pzc + pz / 2)
    add("pack", "24 V LiFePO4 pack, 10 Ah", pack, 7, "bought", "pack")
    szc = Z0 + p["switch_z"]
    sw = bx(xf - 40, xf, p["up_y"] - 20, p["up_y"] + 20, szc - 20, szc + 20)
    sw = fuse([sw, xcyl(xf - 46, xf - 40, p["up_y"] - 8, szc, 9.0), xcyl(xf - 45, xf - 40, p["up_y"] + 10, szc, 6.0)])
    add("switchbox", "Key switch and 40 A fuse box", sw, 8, "bought", "harness")
    hz = Z0 + p["frame_h"]
    can_top = Z0 + gm[1] + gzz / 2 + p["motor_l"]
    cables = [   # each starts and ends 4 mm off a face, so the cable end touches it
        [(xf - 28, pyy / 2 + 4, pzc - 20), (xf - 28, p["up_y"] - 8, szc + 24)],             # pack lead to the fuse box
        [(xf - 28, p["up_y"] + 8, szc - 24), (xf - 28, p["up_y"] + 8, ezc + ez / 2 + 4)],   # fuse box to the electronics box
        [(xf - 30, 49, ezc - ez / 2 - 4), (p["motor_x"], 49, can_top + 4)],                  # driver to the motor and brake
        [(xf - 20, -150, ezc + ez / 2 + 4), (xf - 20, -150, hz - 30), (hx, -30, gz - 34)],   # controls lead to the handle pod
    ]
    cab = []
    for pts in cables:
        cab.append(b.Pos(*pts[0]) * b.Sphere(4.0))
        for c0, c1 in zip(pts, pts[1:]):
            cab.append(tube(c0, c1, 4.0))
            cab.append(b.Pos(*c1) * b.Sphere(4.0))
    add("harness", "Harness (cables, cable-tied)", fuse(cab), 8, "bought", "harness")

    # ---- 9 Handle controls: pod clamped round the grip, dead-man lever on the pod
    pod = bx(hx - 22, hx + 22, -45, 45, gz - 30, gz + 18) - tube((hx, -60, gz), (hx, 60, gz), p["grip_r"])
    lever = bx(hx - 30, hx - 22, -100, 100, gz - 26, gz - 12)
    add("controls", "Handle controls: pod, thumb switch and dead-man lever", fuse([pod, lever]), 9, "bought", "handle")

    # ---- 11 Skids on standoffs (16)
    sx0 = p["skid_x"]
    skids = fuse([bx(sx0, sx0 + 10, s * p["skid_y"] - 12.5, s * p["skid_y"] + 12.5, Z0 + p["skid_z"][0], Z0 + p["skid_z"][1]) for s in (-1, 1)])
    add("skids", "Nosing guard skids (2), UHMW", skids, 11, "bought", "skids")
    so = []
    for s in (-1, 1):
        for zz in p["standoff_z"]:
            t_ = bx(sx0 + 10, rx, s * p["skid_y"] - 10, s * p["skid_y"] + 10, Z0 + zz - 10, Z0 + zz + 10)
            so.append(t_ - tube((rx, s * ry, Z0 + zz - 20), (rx, s * ry, Z0 + zz + 20), rr))
    add("standoffs", "Skid standoffs (4), 20 mm square tube", fuse(so), 16, "made", "skids")
    sks = fuse([xcyl(sx0 - 0.0, sx0 + 22, s * p["skid_y"], Z0 + zz + dz, 2.5) for s in (-1, 1) for zz in p["standoff_z"] for dz in (0,)])
    add("skid_screws", "Skid screws (4 x M5 countersunk)", sks, 17, "fixing", "skids")

    # ---- 10 Load strap (shown round a 240 mm deep load)
    sz = Z0 + p["strap_z"]
    reach = rx + p["strap_reach"]
    legs = [bx(rx, reach, s * 196 - 1.5, s * 196 + 1.5, sz - 12.5, sz + 12.5) - rails for s in (-1, 1)]
    front = bx(reach, reach + 3, -197.5, 197.5, sz - 12.5, sz + 12.5)
    ratchet = bx(reach + 3, reach + 28, -40, 40, sz - 20, sz + 20)
    add("strap", "Ratchet load strap, hooked round the rails", fuse(legs + [front, ratchet]), 10, "bought", "strap")
    return C


GROUPS = {  # concept-media groups (kept from the TRL 3 concept) and the keys in each
    "frame": ("frame", "low_bar"),
    "clusters": ("spider_l", "spider_r", "hub_l", "hub_r", "stubs_l", "stubs_r", "wheels_l", "wheels_r", "wheel_fix_l", "wheel_fix_r"),
    "drive": ("axle_plate", "case_outer", "case_inner", "case_band", "spacers", "spacer_screws", "brg_main_l", "brg_main_r",
              "brg_cs_out", "brg_cs_in", "brg_bolts", "shaft", "cs_shaft", "spr_main", "spr_cs", "spr_gm", "chain1", "chain2"),
    "gearmotor": ("gearmotor", "gm_bolts"),
    "driver": ("ebox",),
    "controller": ("driver",),
    "pack": ("cradle", "pack"),
    "harness": ("switchbox", "harness"),
    "handle": ("controls",),
    "skids": ("skids", "standoffs", "skid_screws"),
    "strap": ("strap",),
    "uprights": ("uprights", "up_bolts"),
}
CLUSTER_KEYS = GROUPS["clusters"]


def build(p=PARAMS):
    """Return {group: shape} in the upright pose (the grouping the concept media and GA use)."""
    C = build_components(p)
    return {g: fuse([C[k].shape for k in ks]) for g, ks in GROUPS.items()}


def tilted(parts, p=PARAMS):
    """Rotate frame-mounted parts back about the shaft (top toward -X). Clusters stay put."""
    from build123d import Pos, Rot
    z0 = derived(p)["hub_z"]
    return {k: v if k == "clusters" else Pos(0, 0, z0) * Rot(0, -p["tilt"], 0) * Pos(0, 0, -z0) * v
            for k, v in parts.items()}


# ------------------------------------------------------------------ constructability checks
def _vol(a, c):
    try:
        s = a & c
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch or keep a clearance. Returns (description, overlap mm3, gap mm, expect, ok)."""
    from build123d import Compound
    C = build_components(p)
    S = lambda *ks: C[ks[0]].shape if len(ks) == 1 else Compound(children=[C[k].shape for k in ks])  # noqa: E731
    D = derived(p)
    rows = []

    def chk(desc, a, c, expect):
        v = _vol(a, c)
        gp = a.distance_to(c)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    rails = S("frame")
    chk("Replacement low cross bar welded between the rails", S("low_bar"), rails, "touch")
    chk("Plain-side axle plate on its rail", S("axle_plate"), rails, "touch")
    chk("Case outer plate on the drive-side rail", S("case_outer"), rails, "touch")
    chk("Plain-side main bearing on its axle plate", S("brg_main_l"), S("axle_plate"), "touch")
    chk("Drive-side main bearing on the case outer plate", S("brg_main_r"), S("case_outer"), "touch")
    chk("Outer countershaft bearing on the case outer plate", S("brg_cs_out"), S("case_outer"), "touch")
    chk("Inner countershaft bearing on the case inner plate", S("brg_cs_in"), S("case_inner"), "touch")
    chk("Cluster shaft in both main bearings", S("shaft"), S("brg_main_l", "brg_main_r"), "touch")
    chk("Countershaft in both countershaft bearings", S("cs_shaft"), S("brg_cs_out", "brg_cs_in"), "touch")
    chk("Cluster shaft clear of the rails", S("shaft"), rails, 10.0)
    chk("Cluster shaft clear of the inner plate (through its hole)", S("shaft"), S("case_inner"), 3.0)
    chk("Countershaft clear of the plates (through their holes)", S("cs_shaft"), S("case_inner", "case_outer"), 3.0)
    chk("Case band on the outer plate", S("case_band"), S("case_outer"), "touch")
    chk("Case band against the inner plate", S("case_band"), S("case_inner"), "touch")
    chk("Spacers between the case plates", S("spacers"), S("case_outer"), "touch")
    chk("Spacers against the inner plate", S("spacers"), S("case_inner"), "touch")
    chk("Main sprocket on the cluster shaft", S("spr_main"), S("shaft"), "touch")
    chk("Countershaft sprockets on the countershaft", S("spr_cs"), S("cs_shaft"), "touch")
    chk("Gearmotor sprocket on its output shaft", S("spr_gm"), S("gearmotor"), "touch")
    chk("Gearmotor face on the inner plate", S("gearmotor"), S("case_inner"), "touch")
    chk("Gearmotor screws on the inner plate", S("gm_bolts"), S("case_inner"), "touch")
    chk("Bearing bolts clear of the rails", S("brg_bolts"), rails, 2.0)
    chk("Spacer screws clear of the rails", S("spacer_screws"), rails, 2.0)
    chk("Spacer screws clear of the chains", S("spacer_screws"), S("chain1", "chain2"), 3.0)
    for k in ("spr_main", "spr_cs", "spr_gm", "chain1", "chain2"):
        chk(f"{C[k].name} clear of the case band", S(k), S("case_band"), 3.0)
        chk(f"{C[k].name} clear of the case plates", S(k), S("case_inner", "case_outer"), 2.0)
        chk(f"{C[k].name} clear of the bearings", S(k), S("brg_main_r", "brg_cs_out", "brg_cs_in"), 2.0)
        chk(f"{C[k].name} clear of the spacers", S(k), S("spacers"), 3.0)
        chk(f"{C[k].name} clear of the bearing and gearmotor screws", S(k), S("brg_bolts", "gm_bolts"), 1.0)
    chk("Final-stage chain clear of the first-stage parts", S("chain2"), S("spr_gm", "chain1"), 3.0)
    chk("First-stage chain clear of the main sprocket", S("chain1"), S("spr_main"), 3.0)
    chk("Gearmotor clear of the inner countershaft bearing", S("gearmotor"), S("brg_cs_in"), 5.0)
    chk("Gearmotor clear of the cross bars", S("gearmotor"), rails, 5.0)
    chk("Gearmotor clear of the uprights", S("gearmotor"), S("uprights"), 5.0)
    chk("Motor clear of the electronics box", S("gearmotor"), S("ebox"), 5.0)
    chk("Low cross bar clear of the case and axle plates", S("low_bar"), S("case_outer", "case_band", "case_inner", "axle_plate"), 10.0)
    chk("Low cross bar clear of the bearings", S("low_bar"), S("brg_main_l", "brg_main_r", "brg_bolts"), 5.0)
    chk("Chain case clear of the kept cross bars", S("case_inner", "case_band"), rails - fuse([tube((p["rail_x"], s * p["rail_y"], -500), (p["rail_x"], s * p["rail_y"], 3000), p["rail_r"]) for s in (-1, 1)]), 10.0)
    chk("Uprights on the cross bars", S("uprights"), rails, "touch")
    chk("Electronics box on the uprights", S("ebox"), S("uprights"), "touch")
    chk("Boards inside the electronics box", S("driver"), S("ebox"), "touch")
    chk("Pack cradle on the uprights", S("cradle"), S("uprights"), "touch")
    chk("Pack in its cradle", S("pack"), S("cradle"), "touch")
    chk("Fuse box on the drive-side upright", S("switchbox"), S("uprights"), "touch")
    chk("Pack clear of the electronics box", S("pack", "cradle"), S("ebox"), 10.0)
    chk("Harness clear of the rails and cross bars", S("harness"), rails, 3.0)
    chk("Harness clear of the uprights", S("harness"), S("uprights"), 2.0)
    chk("Harness touches its ends (pack, fuse box, electronics box, motor, pod)", S("harness"), S("pack", "switchbox", "ebox", "gearmotor", "controls"), "touch")
    chk("Handle pod clamped on the grip", S("controls"), rails, "touch")
    chk("Skid standoffs welded to the rails", S("standoffs"), rails, "touch")
    chk("Skids on the standoffs", S("skids"), S("standoffs"), "touch")
    chk("Skid standoffs clear of the case and axle plates", S("standoffs"), S("case_outer", "axle_plate", "brg_bolts"), 3.0)
    chk("Skid standoffs clear of the electronics box", S("standoffs"), S("ebox"), 10.0)
    chk("Strap hooked on the rails", S("strap"), rails, "touch")
    chk("Strap clear of the cross bars", S("strap"), rails - fuse([tube((p["rail_x"], s * p["rail_y"], -500), (p["rail_x"], s * p["rail_y"], 3000), p["rail_r"] + 0.01) for s in (-1, 1)]), 1.0)
    for tag, s in (("plain", "l"), ("drive", "r")):
        chk(f"Weld-on hub on the cluster shaft ({tag} side)", S(f"hub_{s}"), S("shaft"), "touch")
        chk(f"Spider round its hub ({tag} side)", S(f"spider_{s}"), S(f"hub_{s}"), "touch")
        chk(f"Stub axles in the spider ({tag} side)", S(f"stubs_{s}"), S(f"spider_{s}"), "touch")
        chk(f"Wheels on their stub axles ({tag} side)", S(f"wheels_{s}"), S(f"stubs_{s}"), "touch")
        chk(f"Wheel spacers and washers on the wheels ({tag} side)", S(f"wheel_fix_{s}"), S(f"wheels_{s}"), "touch")
        chk(f"Wheels clear of the spider ({tag} side)", S(f"wheels_{s}"), S(f"spider_{s}"), 3.0)
    chk("Lower wheels on the floor", S("wheels_l", "wheels_r"), box(0, 0, -5, 2000, 2000, 10), "touch")
    # the clusters turn: check every 15 degrees of a third of a turn against the frame-fixed parts
    fixed = S("frame", "low_bar", "axle_plate", "case_outer", "brg_main_l", "brg_main_r", "brg_bolts", "skids",
              "standoffs", "skid_screws", "strap", "spacer_screws")
    clus = S(*[k for k in CLUSTER_KEYS if not k.startswith("hub")])
    hubs = S("hub_l", "hub_r")
    worst = (1e9, None)
    worst_h = (1e9, None)
    for deg in range(0, 120, 15):
        g = _rot_cluster(clus, deg, D["hub_z"]).distance_to(fixed)
        worst = min(worst, (g, deg))
        gh = _rot_cluster(hubs, deg, D["hub_z"]).distance_to(fixed - S("brg_main_l", "brg_main_r"))
        worst_h = min(worst_h, (gh, deg))
    rows.append(("Turning spiders, wheels and stub axles clear of every frame part (every 15 deg)", 0.0, worst[0], 5.0, worst[0] >= 5.0))
    rows.append(("Turning hubs clear of the rails and axle plates", 0.0, worst_h[0], 3.0, worst_h[0] >= 3.0))
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:72s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def masses(p=PARAMS):
    """Masses (kg) of the made parts, from the model volumes (steel 7,850, aluminium 2,700 kg/m3).
    The 25 mm cluster shaft is 4140 quenched and tempered alloy steel (decided 2026-10-02), density 7,850 kg/m3, so its mass
    is unchanged from the 1018 bar."""
    C = build_components(p)
    rho = {"axle_plate": 7.85, "case_outer": 7.85, "case_inner": 7.85, "case_band": 7.85, "spacers": 7.85,
           "low_bar": 7.85, "uprights": 2.70, "standoffs": 7.85, "spider_l": 7.85, "spider_r": 7.85,
           "stubs_l": 7.85, "stubs_r": 7.85, "shaft": 7.85, "cs_shaft": 7.85}
    out = {}
    for k, r in rho.items():
        v = C[k].shape.volume
        if k in ("low_bar", "spacers", "standoffs"):
            v *= {"low_bar": 0.26, "spacers": 0.50, "standoffs": 0.28}[k]   # tube wall fraction of the solid modelled
        out[k] = v * r / 1e6
    return out


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    if "--mass" in sys.argv:
        for k, v in masses().items():
            print(f"{k:12s} {v:6.3f} kg")
        sys.exit(0)
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    # The STEP writer refuses a shape already written into another file, so each export gets its own build.
    for name, keys in [("stepclimber-assembly", None), ("stepclimber-cluster-pair", GROUPS["clusters"]),
                       ("stepclimber-frame", GROUPS["frame"] + GROUPS["uprights"] + GROUPS["skids"]),
                       ("stepclimber-drive", GROUPS["drive"] + GROUPS["gearmotor"])]:
        C = build_components()
        shapes = [c.shape for c in C.values()] if keys is None else [C[k].shape for k in keys]
        shape = Compound(children=shapes)
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"Width {D['width']:.0f} mm at the wheel faces, {D['width_bolts']:.0f} mm over the wheel end screws; "
          f"upright height {D['height_upright']:.0f} mm")
    print(f"Final stage 08B {PARAMS['z_cs2']}T to {PARAMS['z_driven']}T: centres {D['c2']:.1f} mm "
          f"({PARAMS['links2']} links need {D['c2_whole']:.1f} mm); guard radius {D['guard_r']:.1f} mm")
    print(f"First stage 06B {PARAMS['z_drive']}T to {PARAMS['z_cs1']}T: centres {D['c1']:.1f} mm "
          f"({PARAMS['links1']} links need {D['c1_whole']:.1f} mm); overall ratio {D['ratio']:.0f}:1")
    print(f"Case outline area {case_outline().area / 1e3:.1f} x 1000 mm2")
    print_checks()

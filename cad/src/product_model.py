"""StepClimber product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a powder-coated steel frame with welded rail bends,
toe plate gussets and an anti-slip ribbed toe plate; teal laser-cut tri-star spiders with
lightening slots, cast hub bosses, hub bolts and shaft end caps; six grooved rubber tyres on
light grey rims with axle caps; the constructable drive of SCM-DDR-003 taken from model.py (axle
plates welded inside the rails, a closed chain case of two plates and a band on spacers, four
flange bearings with their bolts, a 4140 cluster shaft, countershaft, sprockets and chains, two
aluminium component uprights, skid standoffs and the lowered cross bar); the worm gearmotor
standing up the frame on the inner case plate, with a ribbed gearbox, brake housing and a
teal brake-release lever; the IP54 electronics box, hung on the uprights, with a lid frame, a clear window over the
controller and IMU board and lid screws; the battery pack with a state-of-charge light bar,
charge port, teal release latch and wordmark on its cradle; a key switch and fuse holder;
cables; ribbed rubber grip sleeves, the dead-man lever and a control pod with a lit status
light bar and an up and down rocker; UHMW nosing skids with screws; and the load strap and
ratchet round three parcel cartons. Context is a four-step stair (196 mm risers, 254 mm treads,
oak treads) and the shared clay mannequin, two steps up, steadying the handle.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and build() in model.py. Axes
as model.py: X toward the load side, Y across the truck, Z up, floor at Z = 0. Frame-mounted
parts are built upright and then tilted back about the cluster shaft by PARAMS["tilt"], exactly
as model.tilted() does; the clusters stay put with two wheels of each on the floor and the
lower rear wheels against the first riser, as in concept_media.py.

Groups: "shell" is the frame, handle, enclosures, pack, skids and strap; "internal" is the
drive train (clusters, shaft, bearings, chain case and chains, gearmotor and its mounts) so the
"detail" view can frame it on its own; "context" is the stair, cartons and mannequin.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Circle, Cylinder, GeomType, Location, Plane, Polygon, Pos,  # noqa: E402
                       Rectangle, RegularPolygon, Rot, SlotCenterToCenter, Solid, Sphere, Text,
                       Vector, extrude, fillet)
from model import PARAMS, build_components, derived  # noqa: E402

TITLE = "StepClimber: motor-assisted stair-climbing hand truck"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 16, "az": -58,
     "note": "Product render from the front right, slightly above (about 16 deg elevation); the truck is "
             "tilted back at the foot of the stair with parcels strapped on, the courier two steps up "
             "steadying the handle, and the teal tri-star wheel clusters against the first riser"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 24, "az": -128,
     "note": "Exploded view from the front left and above (about 24 deg elevation), seen from the stair "
             "side: tri-star clusters and wheels, chain case, gearmotor, electronics box and boards, "
             "battery pack and cradle, handle controls, skids and load strap"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 14, "az": -135,
     "note": "Detail from the front left, slightly above (about 14 deg elevation): the tri-star wheel "
             "clusters, cluster shaft and bearings, chain case with its clear window and the worm "
             "gearmotor with its brake, without the frame or stair"},
]

FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

# Stair context (design stair of SCM-CAL-001) and the mannequin pose fitted to the handle
RISER, TREAD, N_STEPS, STAIR_W, NOSE = 196.0, 254.0, 4, 900.0, 20.0
MANNEQUIN_H = 1750.0
MANNEQUIN_JOINTS = dict(torso_lean=27.0, hip_flex_l=20.5, hip_flex_r=9.4, knee_flex_l=38.2,
                        knee_flex_r=24.6, shoulder_flex_l=28.7, shoulder_flex_r=28.7,
                        shoulder_abd_l=-6.0, shoulder_abd_r=-6.0, elbow_flex_l=5.1, elbow_flex_r=5.1,
                        ankle_flex_l=9.1, ankle_flex_r=17.1)

# Colours (restrained product palette; kit accent on the spiders and controls)
C_FRAME = "#2B3037"
C_ACCENT = "#0F766E"
C_TYRE = "#1E2124"
C_RIM = "#D6D9DD"
C_CAST = "#8F969E"
C_STEEL = "#B8BEC6"
C_DARK = "#3A3F47"
C_BLACK = "#1C1F24"
C_ALU = "#BFC4CA"
C_SHELL = "#E4E6E9"
C_PACK = "#30353C"
C_WINDOW = "#DCEBF5"
C_PCB = "#166534"
C_CHIP = "#111827"
C_LABEL = "#F4F4F2"
C_UHMW = "#34383E"
C_STRAP = "#3B4047"
C_LED_G = "#22C55E"
C_LED_OFF = "#2E3A33"
C_CARTON = "#C8A26B"
C_TAPE = "#B38B55"
C_OAK = "#B48A5E"
C_RISER = "#E7E5E1"
C_CLAY = "#9CA3AF"


# ------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _hex_y(x, y, z, af, h):
    """Hex prism along Y (across flats `af`), centred on (x, y, z)."""
    return Pos(x, y + h / 2, z) * extrude(Plane.XZ * RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x, y, z, af, h):
    return Pos(x - h / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=h)


def _rod(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r, end_balls=False):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = _rod(a, c, r)
        out = seg if out is None else out + seg
    joints = points if end_balls else points[1:-1]
    for q in joints:
        out += Pos(*q) * Sphere(r)
    return out


def _band(a, b, w, t):
    """Flat strap of width w (in Z) and thickness t from a to b (horizontal run)."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    pl = Plane(origin=(a + b) * 0.5, x_dir=d.normalized(), z_dir=(0, 0, 1))
    return Location(pl) * Box(d.length, t, w)


def _xz_prism(pts, y0, y1):
    """Prism of the XZ polygon `pts` between y0 and y1."""
    f = Plane.XZ * Polygon(*pts, align=None)
    s = extrude(f, amount=y1 - y0)                  # Plane.XZ normal is -Y
    bb = s.bounding_box()
    return Pos(0, y0 - bb.min.Y, 0) * s


def _stadium_y(x, za, ra, zb, rb, y0, y1):
    """Closed belt outline round two circles on a vertical line (centres za < zb), as a Y prism."""
    d = zb - za
    sphi = (ra - rb) / d
    cphi = math.sqrt(max(0.0, 1 - sphi ** 2))
    pts = [(x - ra * cphi, za + ra * sphi), (x + ra * cphi, za + ra * sphi),
           (x + rb * cphi, zb + rb * sphi), (x - rb * cphi, zb + rb * sphi)]
    w = y1 - y0
    return (_xz_prism(pts, y0, y1) + _ycyl(x, (y0 + y1) / 2, za, ra, w) + _ycyl(x, (y0 + y1) / 2, zb, rb, w))


def _circle_edges(s, r, tol=0.2):
    return [e for e in s.edges() if e.geom_type == GeomType.CIRCLE and abs(e.radius - r) < tol]


def _faces_edges(s, axis, i):
    return s.faces().sort_by(axis)[i].edges()


def _text_plate(txt, size, origin, x_dir, z_dir, h=0.5):
    """Raised text of height h on the plane given (reads correctly looking along -z_dir)."""
    try:
        sk = Text(txt, font_size=size, font_path=FONT)
        return Location(Plane(origin=origin, x_dir=x_dir, z_dir=z_dir)) * extrude(sk, amount=h)
    except Exception:
        return None


def _union(shapes):
    out = None
    for s in shapes:
        if s is not None:
            out = s if out is None else out + s
    return out


# ------------------------------------------------------------------ model
def product_parts(P=PARAMS):
    D = derived(P)
    Z0 = D["hub_z"]
    MC = build_components(P)          # constructable-design parts of model.py, used for the drive, mounts and fixings
    TL = Pos(0, 0, Z0) * Rot(0, -P["tilt"], 0) * Pos(0, 0, -Z0)
    out = []

    def vec(v):
        q = (Rot(0, -P["tilt"], 0) * Pos(*v)).position
        return (q.X, q.Y, q.Z)

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0), tilt=True, shift=None):
        if shape is None:
            return
        if shift is not None:
            shape = Pos(*shift) * shape
        if tilt:
            shape = TL * shape
            explode = vec(explode)
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    rx, ry, rr = P["rail_x"], P["rail_y"], P["rail_r"]
    ztop = Z0 + P["frame_h"]
    gz = Z0 + P["frame_h"] + P["handle_rise"]
    hx = P["handle_x"]
    zbot = Z0 - P["rail_below"]
    plate_top = zbot

    # ============================================================ 1 frame (shell)
    rails = None
    for s in (-1, 1):
        r = _pipe([(rx, s * ry, zbot + 2), (rx, s * ry, ztop), (hx, s * 150, gz)], rr)
        r += Pos(hx, s * 150, gz) * Sphere(rr)
        rails = r if rails is None else rails + r
    for dz in P["bars"] + (P["low_bar"],):          # three bars kept, the bar at 60 mm cut off, a lower bar added
        rails += _rod((rx, -ry, Z0 + dz), (rx, ry, Z0 + dz), P["bar_r"])
    add("Steel frame rails and cross bars (powder coat)", rails, C_FRAME, "painted", 1, "shell")

    tl, tw, tt = P["toe_l"], P["toe_w"], P["toe_t"]
    tcx = rx + tl / 2 - 10
    toe = _box(tcx, 0, zbot - tt / 2, tl, tw, tt)
    toe = _fillet_try(toe, [e for e in toe.edges().filter_by(Axis.Z) if e.center().X > tcx], [30.0, 20.0, 10.0])
    toe = _fillet_try(toe, _faces_edges(toe, Axis.Z, -1), [2.0, 1.0])
    for k in range(6):
        rib = _box(rx + 45 + 34 * k, 0, plate_top + 0.75, 5, tw - 60, 1.5)
        toe += _fillet_try(rib, rib.edges().filter_by(Axis.Y), [0.7, 0.4])
    for s in (-1, 1):
        g = _xz_prism([(rx, plate_top), (rx + 90, plate_top), (rx, plate_top + 90)], s * ry - 3, s * ry + 3)
        toe += g
    add("Toe plate with ribs and gussets", toe, C_FRAME, "painted", 1, "shell")

    # ============================================================ constructable-design mounts (from model.py)
    add("Component uprights (aluminium flat bar)", MC["uprights"].shape, C_ALU, "metal", 15, "shell")
    add("Upright bolts", MC["up_bolts"].shape, C_STEEL, "metal", 17, "shell")
    add("Skid standoffs (square tube)", MC["standoffs"].shape, C_FRAME, "painted", 16, "shell", (-50, 0, 0))

    # ============================================================ axle plates, chain case, bearings
    add("Axle plate, plain side (welded)", MC["axle_plate"].shape, C_FRAME, "painted", 14, "internal", (0, -160, 0))
    add("Chain case outer plate (drive-side axle plate)", MC["case_outer"].shape, C_FRAME, "painted", 14, "internal", (0, 160, 0))
    add("Chain case inner plate (aluminium)", MC["case_inner"].shape, C_ALU, "metal", 14, "internal", (0, -80, 0))
    add("Chain case band (aluminium)", MC["case_band"].shape, C_ALU, "metal", 14, "internal", (0, 80, 0))
    add("Chain case spacers", MC["spacers"].shape, C_STEEL, "metal", 14, "internal", (0, 40, 0))
    add("Chain case spacer screws", MC["spacer_screws"].shape, C_STEEL, "metal", 17, "internal", (0, 120, 0))
    add("Main shaft flange bearings", _union([MC["brg_main_l"].shape, MC["brg_main_r"].shape]), C_DARK, "painted", 3, "internal")
    add("Countershaft flange bearings", _union([MC["brg_cs_out"].shape, MC["brg_cs_in"].shape]), C_DARK, "painted", 3, "internal", (0, 40, 0))
    add("Flange bearing bolts", MC["brg_bolts"].shape, C_STEEL, "metal", 17, "internal")

    # ============================================================ 3 shafts, sprockets and chains
    ES = (-40, 0, 30)
    add("Cluster shaft, 25 mm keyed (4140 steel)", MC["shaft"].shape, C_STEEL, "metal", 3, "internal")
    add("Countershaft (20 mm)", MC["cs_shaft"].shape, C_STEEL, "metal", 3, "internal", ES)
    spr = _union([MC["spr_main"].shape, MC["spr_cs"].shape, MC["spr_gm"].shape])
    add("Sprockets, 06B and 08B", spr, C_STEEL, "metal", 3, "internal", ES)
    add("Roller chains", _union([MC["chain1"].shape, MC["chain2"].shape]), "#4A4F57", "metal", 3, "internal", ES)

    # ============================================================ 4 worm gearmotor with brake
    # Gearbox bolted to the inside of the case inner plate, motor can standing up the frame (model.py)
    gx, gyl, gzz = P["gm_box"]
    gm = (P["cs_x"], Z0 + P["gm_z"])
    iy0 = P["inner_y"][0]
    gy0 = P["gm_y0"]
    ymc = (gy0 + iy0) / 2
    EG = (-260, -40, 330)
    gb = _box(gm[0], ymc, gm[1], gx, iy0 - gy0, gzz)
    gb = _fillet_try(gb, gb.edges(), [8.0, 6.0, 4.0])
    for k in range(4):
        gb += _box(gm[0] - gx / 2 - 1.5, gy0 + 18 + 18 * k, gm[1], 3, 3, gzz - 24)   # cast fins on the stair side
    add("Worm gearbox housing (cast aluminium)", gb, C_ALU, "metal", 4, "internal", EG)
    osh = _ycyl(gm[0], (iy0 + P["sprocket_y"] + 8) / 2, gm[1], 10, P["sprocket_y"] + 8 - iy0)
    add("Gearmotor output shaft", osh, C_STEEL, "metal", 4, "internal", EG)
    mr, ml = P["motor_r"], P["motor_l"]
    zb = gm[1] + gzz / 2
    can = _zcyl(P["motor_x"], ymc, zb + (ml - 30) / 2, mr, ml - 30)
    can = _fillet_try(can, _circle_edges(can, mr), [3.0, 2.0])
    add("Gearmotor can, 24 V", can, C_BLACK, "painted", 4, "internal", EG)
    brk = _zcyl(P["motor_x"], ymc, zb + ml - 15, mr + 1, 30)
    brk = _fillet_try(brk, _faces_edges(brk, Axis.Z, -1), [6.0, 4.0, 2.0])
    add("Spring-applied brake housing", brk, C_ALU, "metal", 4, "internal", EG)
    lev = _box(P["motor_x"] - mr - 6, ymc, zb + ml - 20, 10, 8, 50)
    lev = _fillet_try(lev, lev.edges(), [2.5, 1.5])
    add("Brake release lever", lev, C_ACCENT, "plastic", 4, "internal", EG)
    band = _zcyl(P["motor_x"], ymc, zb + 60, mr + 0.4, 36) - _zcyl(P["motor_x"], ymc, zb + 60, mr - 1, 40)
    band &= _box(P["motor_x"] - mr, ymc, zb + 60, mr * 1.4, mr * 2 + 2, 40)
    add("Gearmotor rating label", band, C_LABEL, "paper", 4, "internal", EG)
    glm = _xcyl(P["motor_x"] + mr + 4, ymc, zb + 90, 7, 8)
    add("Gearmotor cable gland", glm, C_DARK, "plastic", 8, "internal", EG)
    add("Gearmotor screws (3 x M8)", MC["gm_bolts"].shape, C_STEEL, "metal", 17, "internal", EG)
    gmz = gm[1]

    # ============================================================ 2 tri-star clusters (not tilted)
    a, wr, ww = P["arm"], P["wheel_r"], P["wheel_w"]
    t = P["spider_t"]
    spiders, bosses, hbolts, tyres, rims, stubs, caps = [], [], [], [], [], [], []
    sk = Circle(P["boss_r"] + 8)                       # hub disk r 46, inside the 54.2 mm nosing envelope
    for ang in (90, 210, 330):
        sk += Rot(0, 0, ang) * Pos(a / 2, 0) * Rectangle(a, P["arm_w"])
        sk += Rot(0, 0, ang) * Pos(a, 0) * Circle(P["arm_w"] / 2 + 6)
    try:
        sk = fillet(sk.vertices(), 6)
    except Exception:
        pass
    for ang in (90, 210, 330):
        sk -= Rot(0, 0, ang) * Pos(a * 0.52, 0) * SlotCenterToCenter(36, 15)
    plate0 = extrude(Plane.XZ * sk, amount=t)
    b0 = plate0.bounding_box()
    for s in (-1, 1):
        yw = s * P["cluster_y"]
        ys = yw - s * P["spider_off"]
        spiders.append(Pos(0, ys - (b0.min.Y + b0.max.Y) / 2, Z0) * plate0)
        boss = _ycyl(0, ys, Z0, P["boss_r"], 26)
        boss = _fillet_try(boss, _circle_edges(boss, P["boss_r"]), [4.0, 2.0])
        bosses.append(boss)
        yo = ys + s * 13
        for k in range(6):
            q = math.radians(60 * k)
            hbolts.append(_hex_y(27 * math.cos(q), yo + s * 2, Z0 + 27 * math.sin(q), 10, 4))
        hbolts.append(_ycyl(0, yo + s * 2, Z0, 16, 4) + _hex_y(0, yo + s * 6, Z0, 13, 4))
        for ang in (90, 210, 330):
            q = math.radians(ang)
            wx, wz = a * math.cos(q), Z0 + a * math.sin(q)
            tyre = _ycyl(wx, yw, wz, wr, ww) - _ycyl(wx, yw, wz, 62, ww + 2)
            tyre = _fillet_try(tyre, _circle_edges(tyre, wr), [12.0, 9.0, 6.0])
            for dy in (-8, 0, 8):
                tyre -= _ycyl(wx, yw + dy, wz, wr + 1, 2.5) - _ycyl(wx, yw + dy, wz, wr - 2.5, 3)
            tyres.append(tyre)
            rim = _ycyl(wx, yw, wz, 62, ww - 4)
            rim = _fillet_try(rim, _circle_edges(rim, 62), [2.0, 1.0])
            for sd in (-1, 1):
                rim -= _ycyl(wx, yw + sd * (ww / 2 - 2 - 1.5), wz, 50, 3.2) - _ycyl(wx, yw, wz, 24, ww + 2)
                for k in range(5):
                    p5 = math.radians(72 * k + 18)
                    rim -= _ycyl(wx + 37 * math.cos(p5), yw + sd * (ww / 2 - 2 - 1.5), wz + 37 * math.sin(p5), 7, 3.4)
            rims.append(rim)
            st = _ycyl(wx, (yw + ys) / 2 + s * 5, wz, 20, P["wheel_hub_l"])
            stubs.append(st)
            yc = yw + s * (ww / 2 + 1)
            cap = _hex_y(wx, yc + s * 2, wz, 19, 4) + Pos(wx, yc + s * 4.5, wz) * Sphere(8) \
                & _box(wx, yc + s * 7, wz, 20, 10, 20)
            caps.append(cap)
    # explode: each side's parts move outboard in steps (world offsets, clusters are not tilted)
    for s, side in ((-1, "left"), (1, "right")):
        k_ = 1.0 if s < 0 else 0.4
        pick = lambda lst: _union([x for x in lst if (x.center().Y > 0) == (s > 0)])
        add(f"Cluster hub boss, {side} (cast)", pick(bosses), C_CAST, "metal", 2, "internal", (0, s * k_ * 140, 0), tilt=False)
        add(f"Cluster hub bolts, {side}", pick(hbolts), C_STEEL, "metal", 13, "internal", (0, s * k_ * 170, 0), tilt=False)
        add(f"Tri-star spider plate, {side} (laser-cut steel)", pick(spiders), C_ACCENT, "painted", 2, "internal",
            (0, s * k_ * 210, 0), tilt=False)
        add(f"Wheel axle bosses, {side}", pick(stubs), C_CAST, "metal", 2, "internal", (0, s * k_ * 270, 0), tilt=False)
        add(f"Solid rubber tyres, {side} (200 mm)", pick(tyres), C_TYRE, "rubber", 2, "internal", (0, s * k_ * 340, 0),
            tilt=False)
        add(f"Wheel rims, {side}", pick(rims), C_RIM, "plastic", 2, "internal", (0, s * k_ * 340, 0), tilt=False)
        add(f"Wheel axle caps, {side}", pick(caps), C_STEEL, "metal", 13, "internal", (0, s * k_ * 410, 0), tilt=False)

    # ============================================================ 5, 6, 13 electronics box
    ex, ey, ez = P["ebox"]
    x0e, x1e = -ex - 12, -12                            # -62 .. -12, as model.py
    ezc = Z0 + P["ebox_z"]
    wall = 2.5
    base_o = _box((x0e + 6 + x1e) / 2, 0, ezc, x1e - x0e - 6, ey, ez)
    base_o = _fillet_try(base_o, base_o.edges().filter_by(Axis.X), [8.0, 6.0, 4.0])
    base_o = _fillet_try(base_o, _faces_edges(base_o, Axis.X, -1), [2.0, 1.0])
    base = base_o - _box((x0e + 6 + x1e) / 2 - wall, 0, ezc, x1e - x0e - 6, ey - 2 * wall, ez - 2 * wall)
    add("Electronics enclosure base (IP54)", base, C_SHELL, "plastic", 13, "shell", (-200, 0, 400), shift=(35, 0, 0))
    lid_o = _box(x0e + 3, 0, ezc, 6, ey, ez)
    lid_o = _fillet_try(lid_o, lid_o.edges().filter_by(Axis.X), [8.0, 6.0, 4.0])
    lid_o = _fillet_try(lid_o, _faces_edges(lid_o, Axis.X, 0), [2.0, 1.0])
    wy0, wy1 = 12.0, ey / 2 - 14
    lid = lid_o - _box(x0e + 3, (wy0 + wy1) / 2, ezc, 10, wy1 - wy0, ez - 28)
    for k in range(7):                                                          # driver side cooling ribs
        lid += _box(x0e - 0.8, -150 + 14 * k + 20, ezc - 6, 1.6, 5, ez - 44)
    add("Electronics enclosure lid", lid, C_DARK, "plastic", 13, "shell", (-400, 0, 400), shift=(35, 0, 0))
    pane = _box(x0e + 3, (wy0 + wy1) / 2, ezc, 2.0, wy1 - wy0 + 4, ez - 24)
    add("Enclosure window (clear polycarbonate)", pane, C_WINDOW, "clear", 13, "shell", (-400, 0, 400), shift=(35, 0, 0))
    ls = []
    for yy in (-ey / 2 + 9, 0.0, ey / 2 - 9):
        for zz in (-ez / 2 + 9, ez / 2 - 9):
            if yy == 0.0 and zz < 0:
                continue
            s_ = _xcyl(x0e - 0.6, yy, ezc + zz, 3.2, 1.2)
            s_ -= _box(x0e - 1.2, yy, ezc + zz, 1.0, 3.8, 0.8)
            ls.append(s_)
    add("Enclosure lid screws", _union(ls), C_STEEL, "metal", 13, "shell", (-450, 0, 400), shift=(35, 0, 0))
    npl = _box(x0e - 0.25, -85, ezc + ez / 2 - 12, 0.5, 90, 8)
    add("Enclosure name plate", npl, C_ACCENT, "painted", 13, "shell", (-400, 0, 400), shift=(35, 0, 0))

    EBD = (-300, 0, 400)
    pcb_c = _box(-18, (wy0 + wy1) / 2, ezc, 1.6, wy1 - wy0 + 6, ez - 20)
    add("Controller board with IMU", pcb_c, C_PCB, "plastic", 6, "shell", EBD, shift=(35, 0, 0))
    comp_c = (_box(-22, 55, ezc + 18, 6, 36, 30) + _box(-21, 115, ezc + 20, 4, 14, 14)
              + _box(-21, 115, ezc - 20, 4, 30, 10) + _box(-23, 60, ezc - 28, 8, 60, 12))
    add("Controller microcontroller and IMU", comp_c, C_CHIP, "plastic", 6, "shell", EBD, shift=(35, 0, 0))
    led_c = _box(-19.4, 140, ezc + 30, 1.2, 4, 4)
    add("Controller heartbeat light (lit)", led_c, C_LED_G, "emissive", 6, "shell", EBD, shift=(35, 0, 0))
    pcb_d = _box(-18, -(wy0 + wy1) / 2, ezc, 1.6, wy1 - wy0 + 6, ez - 20)
    add("Motor driver board", pcb_d, C_PCB, "plastic", 5, "shell", EBD, shift=(35, 0, 0))
    hs = _box(-26, -90, ezc, 14, 80, 60)
    for k in range(8):
        hs -= _box(-31, -90 - 35 + 10 * k, ezc, 8, 4, 64)
    add("Motor driver heat sink", hs, C_ALU, "metal", 5, "shell", EBD, shift=(35, 0, 0))
    caps_d = _xcyl(-26, -150, ezc + 25, 7, 14) + _xcyl(-26, -150, ezc - 5, 7, 14) + _box(-22, -30, ezc - 30, 6, 20, 16)
    add("Motor driver capacitors and terminals", caps_d, C_CHIP, "plastic", 5, "shell", EBD, shift=(35, 0, 0))

    # ============================================================ 7 battery pack and cradle
    px, py, pz = P["pack"]
    pcx, pcz = -px / 2 - 8, Z0 + P["pack_z"]
    EP = (-280, 0, 560)
    pk = _box(pcx, 0, pcz, px, py, pz)
    pk = _fillet_try(pk, pk.edges(), [8.0, 6.0, 4.0])
    pk -= _box(pcx, 0, pcz + pz / 2 - 30, px + 2, py + 2, 1.0) - _box(pcx, 0, pcz + pz / 2 - 30, px - 1.4, py - 1.4, 2)
    add("Battery pack housing, 24 V LiFePO4", pk, C_PACK, "plastic", 7, "shell", EP, shift=(28, 0, 0))
    lat = _box(pcx, 0, pcz + pz / 2 + 4, 40, 70, 10)
    lat = _fillet_try(lat, lat.edges(), [4.0, 3.0, 2.0])
    add("Pack release latch", lat, C_ACCENT, "plastic", 7, "shell", EP, shift=(28, 0, 0))
    xf = pcx - px / 2
    lb = _box(xf - 1, 50, pcz + 50, 2, 44, 10)
    lb = _fillet_try(lb, lb.edges().filter_by(Axis.X), [2.0, 1.0])
    add("State-of-charge light housing", lb, C_BLACK, "plastic", 7, "shell", EP, shift=(28, 0, 0))
    for k in range(4):
        seg = _box(xf - 2.3, 50 - 15 + 10 * k, pcz + 50, 0.8, 7, 5)
        lit = k < 3
        add(f"State-of-charge light {k + 1}{' (lit)' if lit else ''}", seg, C_LED_G if lit else C_LED_OFF,
            "emissive" if lit else "plastic", 7, "shell", EP)
    port = _xcyl(xf - 3, -50, pcz + 45, 10, 6)
    port = _fillet_try(port, _circle_edges(port, 10), [2.0, 1.0])
    add("Charge port cap", port, C_BLACK, "rubber", 7, "shell", EP, shift=(28, 0, 0))
    lab = _box(xf - 0.25, 0, pcz - 25, 0.5, 130, 44)
    add("Pack rating label", lab, C_LABEL, "paper", 7, "shell", EP, shift=(28, 0, 0))
    wm = _text_plate("StepClimber", 15, (xf - 0.5, 0, pcz - 16), (0, -1, 0), (-1, 0, 0), h=0.4)
    add("Pack wordmark", wm, C_ACCENT, "painted", 7, "shell", EP, shift=(28, 0, 0))
    ink = _box(xf - 0.6, 0, pcz - 34, 0.3, 100, 3) + _box(xf - 0.6, -20, pcz - 41, 0.3, 60, 3)
    add("Pack label print", ink, C_DARK, "paper", 7, "shell", EP, shift=(28, 0, 0))
    add("Pack quick-release cradle", MC["cradle"].shape, C_FRAME, "painted", 7, "shell", (-120, 0, 400))

    # ============================================================ 8 switch, fuse and harness
    kb = _box(-35, 150, Z0 + P["pack_z"] - 100, 40, 40, 40)
    kb = _fillet_try(kb, kb.edges(), [5.0, 3.0])
    add("Key switch and fuse holder", kb, C_DARK, "plastic", 8, "shell", (-150, 0, 0), shift=(38, -30, -40))
    ks = _xcyl(-57, 150, Z0 + P["pack_z"] - 92, 9, 4) + _xcyl(-60, 150, Z0 + P["pack_z"] - 92, 3, 4)
    ks += _box(-64, 150, Z0 + P["pack_z"] - 92, 6, 3, 14)
    add("Key switch and key", ks, C_STEEL, "metal", 8, "shell", (-150, 0, 0), shift=(38, -30, -40))
    fc = _xcyl(-57, 150, Z0 + P["pack_z"] - 112, 6, 5)
    add("Fuse holder cap (40 A)", fc, "#B91C1C", "plastic", 8, "shell", (-150, 0, 0), shift=(38, -30, -40))
    add("Wiring harness cables", MC["harness"].shape, C_BLACK, "rubber", 8, "shell")
    gl = _union([_zcyl(-30, y, ezc + sz * (ez / 2 + 4), 7, 8) + _zcyl(-30, y, ezc + sz * (ez / 2 + 1), 9, 2)
                 for y, sz in ((-20, 1), (150, 1), (-60, -1))])
    add("Enclosure cable glands", gl, C_DARK, "plastic", 13, "shell", (-200, 0, 400), shift=(35, 0, 0))

    # ============================================================ 9 handle controls
    grip = _rod((hx, -150, gz), (hx, 150, gz), P["grip_r"])
    add("Handle grip tube", grip, C_FRAME, "painted", 9, "shell")
    for s in (-1, 1):
        sl = _ycyl(hx, s * 100, gz, P["grip_r"] + 3, 90)
        sl = _fillet_try(sl, _circle_edges(sl, P["grip_r"] + 3), [2.5, 1.5])
        for k in range(8):
            sl -= _ycyl(hx, s * (100 - 35 + 10 * k), gz, P["grip_r"] + 4, 2.0) - _ycyl(hx, s * (100 - 35 + 10 * k), gz, P["grip_r"] + 1.8, 3)
        add(f"Rubber grip sleeve, {'left' if s < 0 else 'right'}", sl, C_BLACK, "rubber", 9, "shell", (0, s * 120, 80))
    lvr = _box(hx - 30, 0, gz - 14, 20, 200, 14)
    lvr = _fillet_try(lvr, lvr.edges(), [5.0, 3.0, 2.0])
    lvr += _ycyl(hx - 30, 0, gz - 7, 4, 214)
    add("Dead-man grip lever", lvr, C_DARK, "plastic", 9, "shell", (-80, 0, 60))
    pod = _box(hx - 22, 0, gz - 40, 36, 90, 30)
    pod = _fillet_try(pod, pod.edges(), [6.0, 4.0, 2.0])
    add("Control pod", pod, C_SHELL, "plastic", 9, "shell", (-150, 0, 80))
    rk = _box(hx - 40.5, -18, gz - 40, 3, 16, 22)
    rk = _fillet_try(rk, rk.edges(), [1.2, 0.8])
    add("Up and down rocker switch", rk, C_ACCENT, "plastic", 9, "shell", (-150, 0, 80))
    lbh = _box(hx - 26, 20, gz - 24.5, 16, 40, 1.5)
    lbh = _fillet_try(lbh, lbh.edges().filter_by(Axis.Z), [2.0, 1.0])
    add("Status light bar housing", lbh, C_BLACK, "plastic", 9, "shell", (-150, 0, 80))
    for k, (col, mat, nm) in enumerate([(C_LED_G, "emissive", "Status light bar, green (lit)"),
                                        (C_LED_G, "emissive", "Status light bar, green 2 (lit)"),
                                        ("#6E5315", "plastic", "Status light bar, amber"),
                                        ("#5E1C1C", "plastic", "Status light bar, red")]):
        add(nm, _box(hx - 26, 5 + 10 * k, gz - 23.5, 8, 6, 0.8), col, mat, 9, "shell", (-150, 0, 80))
    bz = _union([_xcyl(hx - 40.2, 18 + 5 * i, gz - 40 + 5 * j, 1.0, 0.8) for i in range(3) for j in (-1, 0, 1)])
    add("Buzzer grille", bz, C_DARK, "plastic", 6, "shell", (-150, 0, 80))

    # ============================================================ 11 nosing guard skids
    z0s, z1s = P["skid_z"]
    sx = P["skid_x"]
    skids, sscr = [], []
    for s in (-1, 1):
        sk_ = _box(sx + 5, s * P["skid_y"], Z0 + (z0s + z1s) / 2, 10, 25, z1s - z0s)
        sk_ = _fillet_try(sk_, sk_.edges(), [4.0, 3.0, 1.5])
        skids.append(sk_)
        for zz in P["standoff_z"]:
            sscr.append(_xcyl(sx - 0.4, s * P["skid_y"], Z0 + zz, 3.0, 0.8))
    add("Nosing guard skids (UHMW)", _union(skids), C_UHMW, "plastic", 11, "shell", (-120, 0, 0))
    add("Skid screws", _union(sscr), C_STEEL, "metal", 17, "shell", (-140, 0, 0))

    # ============================================================ context cartons (ride on the toe plate)
    cb = plate_top + 1.5
    cartons = [(56, 232, 360, 330), (56, 212, 330, 300), (56, 192, 300, 260)]
    z = cb
    ctn, tape, labs = [], [], []
    for i, (xa, dx, dy, dz) in enumerate(cartons):
        c = _box(xa + dx / 2, 0, z + dz / 2, dx, dy, dz)
        c = _fillet_try(c, c.edges(), [3.0, 2.0])
        ctn.append(c)
        tape.append(_box(xa + dx / 2, 0, z + dz + 0.3, dx + 0.6, 50, 0.6))
        tape.append(_box(xa + dx + 0.3, 0, z + dz - 30, 0.6, 50, 60))
        if i < 2:
            labs.append(_box(xa + dx + 0.3, -dy / 2 + 70 if i == 0 else 60, z + dz / 2 - 20, 0.6, 90, 60))
        z += dz
    top_c = z
    add("Parcel cartons (corrugated board)", _union(ctn), C_CARTON, "paper", None, "context")
    add("Parcel tape", _union(tape), C_TAPE, "paper", None, "context")
    add("Shipping labels", _union(labs), C_LABEL, "paper", None, "context")

    # ============================================================ 10 load strap round the top carton
    zs = Z0 + 700
    xa, dx, dy = cartons[2][0], cartons[2][1], cartons[2][2]
    xf_ = xa + dx + 1.2
    pts = [(rx, -ry - 16, zs), (xf_ - 20, -dy / 2 - 1.2, zs), (xf_, -dy / 2 + 20, zs),
           (xf_, dy / 2 - 20, zs), (xf_ - 20, dy / 2 + 1.2, zs), (rx, ry + 16, zs)]
    stp = _union([_band(p, q, 25, 2) for p, q in zip(pts, pts[1:])])
    add("Load strap webbing", stp, C_STRAP, "fabric", 10, "shell", (160, 0, 0))
    rat = _box(xf_ + 7, 0, zs, 12, 60, 32)
    rat = _fillet_try(rat, rat.edges(), [2.5, 1.5])
    rat += _box(xf_ + 14, 0, zs + 6, 4, 64, 8)
    add("Strap ratchet", rat, C_STEEL, "metal", 10, "shell", (220, 0, 0))
    hooks = _union([_rod((rx - 4, s * (ry + 14), zs), (rx + 18, s * (ry + 14), zs), 3.5) for s in (-1, 1)])
    add("Strap anchor loops", hooks, C_STEEL, "metal", 10, "shell", (160, 0, 0))
    _ = top_c

    # ============================================================ context stair (not tilted)
    rear_wheel_x = a * math.cos(math.radians(210)) - wr
    x0 = rear_wheel_x - 3
    xb = x0 - N_STEPS * TREAD
    hw = STAIR_W / 2
    carcass, treads = [], []
    for i in range(N_STEPS):
        zt = (i + 1) * RISER
        xr = x0 - i * TREAD
        carcass.append(_box((xb + xr) / 2, 0, (zt - 25) / 2, xr - xb, STAIR_W, zt - 25))
        tr = _box((x0 - (i + 1) * TREAD + xr + NOSE) / 2, 0, zt - 12.5, TREAD + NOSE, STAIR_W, 25)
        tr = _fillet_try(tr, [e for e in tr.edges().filter_by(Axis.Y) if e.center().X > xr], [8.0, 5.0])
        treads.append(tr)
    add("Stair risers and stringers (painted)", _union(carcass), C_RISER, "painted", None, "context", tilt=False)
    add("Stair treads (oak)", _union(treads), C_OAK, "wood", None, "context", tilt=False)

    # ============================================================ context mannequin, hands on the grip
    try:
        from context_parts import mannequin, mannequin_landmarks
        lm = mannequin_landmarks(MANNEQUIN_H, "push", **MANNEQUIN_JOINTS)
        hl, hr_ = lm["hands"]
        g = (TL * Pos(hx, 0, gz)).position
        fx, fy, fz = -(hl[1] + hr_[1]) / 2, (hl[0] + hr_[0]) / 2, (hl[2] + hr_[2]) / 2
        person = Pos(g.X - fx, g.Y - fy, g.Z - fz) * Rot(0, 0, 90) * mannequin(MANNEQUIN_H, "push", **MANNEQUIN_JOINTS)
        add("Courier (clay mannequin, 1.75 m)", person, C_CLAY, "clay", None, "context", tilt=False)
    except Exception as e:  # pragma: no cover
        print("mannequin skipped:", e)
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:50s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")

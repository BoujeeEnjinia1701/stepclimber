"""StepClimber parametric model (build123d), TRL 3, cluster and drive rework (SCM-DDR-002).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl and prints the main envelopes.

Massing-plus detail: correct interfaces (cluster geometry, shaft line, chain centers,
gearmotor, pack cradle, handle) and main dimensions; not fabrication detail.

Axes (upright pose, as stored in a van): X toward the load side (toe plate), Y across the
truck, Z up, floor at Z = 0. The cluster shaft sits at X = 0, Z = hub height with two wheels
of each cluster on the floor. The frame back (stair side while climbing) faces -X.
`tilted()` returns the same parts rotated back about the shaft to the climbing angle.
"""
import math
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # Tri-star clusters (SCM-PRC-001 v0.4; rework decided 2026-09-25, SCM-DDR-002)
    "wheel_r": 100.0,          # 200 mm solid rubber wheels (were 150 mm)
    "wheel_w": 45.0,
    "wheel_hub_l": 55.0,       # wheel hub and axle boss length
    "arm": 150.0,              # cluster hub to wheel center (was 135 mm)
    "arm_w": 45.0,             # spider arm width
    "spider_t": 6.0,           # laser-cut steel spider plate
    "boss_r": 38.0,            # spider hub boss radius
    "cluster_y": 262.0,        # cluster (wheel) mid-plane half-spacing
    "spider_off": 30.0,        # spider plate inboard of the wheel mid-plane
    # Shaft and two-stage chain drive (SCM-CAL-001 v0.2 section 4)
    "shaft_d": 25.0,
    "bearing_r": 45.0,         # flange bearing housing radius
    "chain_pitch": 12.7,       # final stage: 08B roller chain, countershaft to cluster shaft
    "z_driven": 20,            # cluster shaft sprocket teeth, 08B (was 60T 06B)
    "z_cs2": 10,               # countershaft final-stage sprocket teeth, 08B
    "cs_z": 150.0,             # countershaft above the cluster shaft, along the frame
    "chain1_pitch": 9.525,     # first stage: 06B roller chain, gearmotor to countershaft
    "z_cs1": 35,               # countershaft first-stage sprocket teeth, 06B (7:1 overall)
    "z_drive": 10,             # gearmotor sprocket teeth, 06B
    "chain_c": 290.0,          # gearmotor output above the cluster shaft, along the frame
    "guard_gap": 10.0,         # sprocket to guard clearance, plus sheet
    "sprocket_y": 120.0,       # sprocket plane
    # Frame (steel hand truck)
    "rail_y": 200.0,           # rail centerline half-spacing
    "rail_r": 14.0,            # 28 mm rail tube
    "rail_x": 40.0,            # rail centerline toward the load side of the shaft
    "rail_below": 142.5,       # rail length below the shaft (toe plate about 25 mm off the floor)
    "frame_h": 1150.0,         # rail length above the shaft
    "handle_rise": 110.0,      # loop handle rise above the rail tops
    "handle_x": -40.0,         # grip centerline
    "grip_r": 16.0,
    "toe_l": 240.0, "toe_w": 380.0, "toe_t": 8.0,
    # Components on the frame back (upright Z above the shaft, depth toward -X)
    "gm_z": 290.0,             # gearmotor output axis above the shaft (equals chain_c)
    "gm_box": (95.0, 90.0, 95.0),
    "motor_r": 42.0, "motor_l": 150.0,
    "ebox_z": 520.0, "ebox": (50.0, 340.0, 110.0),     # driver and controller, one IP54 box
    "pack_z": 800.0, "pack": (75.0, 180.0, 170.0),      # 8S 10 Ah LiFePO4 in its cradle
    "skid_x": -100.0,          # skid face line on the frame back
    "skid_z": (40.0, 900.0),   # skid span above the shaft
    # Pose
    "tilt": 30.0,              # frame tilt back from vertical while climbing
    "fold_z": 950.0,           # Option C folding hinge height above the shaft (study only)
}


def derived(p=PARAMS):
    """Key derived dimensions, shared with docs/04-calcs/sizing.py."""
    a, r = p["arm"], p["wheel_r"]
    hub_z = r + a * math.sin(math.radians(30))
    pd = lambda n, t=p["chain_pitch"]: t / math.sin(math.pi / n)
    od = lambda n, t=p["chain_pitch"]: t * (0.6 + 1 / math.tan(math.pi / n))
    t1 = p["chain1_pitch"]
    width = 2 * (p["cluster_y"] + p["wheel_w"] / 2)   # wheel outer faces
    top = hub_z + p["frame_h"] + p["handle_rise"] + p["grip_r"]
    return {
        "spacing": a * math.sqrt(3), "hub_z": hub_z, "cluster_dia": 2 * (a + r),
        "sprocket_pd": pd(p["z_driven"]), "sprocket_od": od(p["z_driven"]),
        "cs2_pd": pd(p["z_cs2"]), "cs1_pd": pd(p["z_cs1"], t1), "cs1_od": od(p["z_cs1"], t1),
        "drive_pd": pd(p["z_drive"], t1),
        "ratio1": p["z_cs1"] / p["z_drive"], "ratio2": p["z_driven"] / p["z_cs2"],
        "ratio": (p["z_cs1"] / p["z_drive"]) * (p["z_driven"] / p["z_cs2"]),
        "guard_r": od(p["z_driven"]) / 2 + p["guard_gap"],
        "cs_guard_r": od(p["z_cs1"], t1) / 2 + p["guard_gap"],
        "width": width, "height_upright": top,
        "handle_len": p["frame_h"] + p["handle_rise"],
        "folded_height": hub_z + p["fold_z"] + p["rail_r"],
    }


def build(p=PARAMS):
    """Return {name: shape} for the main parts in the upright pose."""
    from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector, Compound

    D = derived(p)
    Z0 = D["hub_z"]

    def tube(a, b, r):
        a = Vector(*a); b = Vector(*b); d = b - a
        return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))

    def ycyl(x, y, z, r, w):
        return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, w)

    def box(cx, cy, cz, sx, sy, sz):
        return Pos(cx, cy, cz) * Box(sx, sy, sz)

    parts = {}

    # 1 Frame: rails, cross bars, loop handle, toe plate, axle mount plates
    rx, ry = p["rail_x"], p["rail_y"]
    ztop = Z0 + p["frame_h"]
    fr = [tube((rx, s * ry, Z0 - p["rail_below"]), (rx, s * ry, ztop), p["rail_r"]) for s in (-1, 1)]
    fr += [tube((rx, -ry, Z0 + dz), (rx, ry, Z0 + dz), 11) for dz in (60, 380, 700, 1000)]
    gz = ztop + p["handle_rise"]
    fr += [tube((rx, s * ry, ztop), (p["handle_x"], s * 150, gz), p["rail_r"]) for s in (-1, 1)]
    fr += [box(rx + p["toe_l"] / 2 - 10, 0, Z0 - p["rail_below"] - p["toe_t"] / 2, p["toe_l"], p["toe_w"], p["toe_t"])]
    fr += [box(15, s * ry, Z0, 80, 16, 90) for s in (-1, 1)]
    parts["frame"] = Compound(children=fr)

    # 2 Tri-star clusters (pair): spider plate with three arms, boss, three wheels each
    cl = []
    a, wr, ww = p["arm"], p["wheel_r"], p["wheel_w"]
    for s in (-1, 1):
        yw = s * p["cluster_y"]
        ys = yw - s * p["spider_off"]
        for ang in (90, 210, 330):
            t = math.radians(ang)
            wx, wz = a * math.cos(t), Z0 + a * math.sin(t)
            cl.append(Pos(wx / 2, ys, (Z0 + wz) / 2) * Rot(0, -ang, 0) * Box(a, p["spider_t"], p["arm_w"]))
            wheel = ycyl(wx, yw, wz, wr, ww) - ycyl(wx, yw, wz, 22, ww + 2)
            cl.append(wheel)
            cl.append(ycyl(wx, (yw + ys) / 2 + s * 5, wz, 20, p["wheel_hub_l"]))
        cl.append(ycyl(0, ys, Z0, p["boss_r"], 26))
    parts["clusters"] = Compound(children=cl)

    # 3 Shaft, flange bearings and two-stage chain drive with guards
    # Final stage (08B) in the plane y2: countershaft 10T to cluster shaft 20T.
    # First stage (06B) in the plane y1: gearmotor 10T to countershaft 30T.
    y1, y2 = p["sprocket_y"], p["sprocket_y"] - 25
    zc, zg = Z0 + p["cs_z"], Z0 + p["gm_z"]
    sh = [ycyl(0, 0, Z0, p["shaft_d"] / 2, 2 * (p["cluster_y"] - p["spider_off"]) + 26)]
    sh += [ycyl(0, s * (ry + 14), Z0, p["bearing_r"], 16) for s in (-1, 1)]
    sh += [ycyl(0, y2, Z0, D["sprocket_od"] / 2, 8)]                        # 20T 08B on the cluster shaft
    sh += [ycyl(0, (y2 + ry) / 2, zc, 10, ry - y2 + 20)]                      # 20 mm countershaft
    sh += [ycyl(0, ry - 14, zc, 28, 16)]                                      # countershaft bearing on the rail
    sh += [ycyl(0, y2, zc, D["cs2_pd"] / 2 + 6, 8)]                           # 10T 08B on the countershaft
    sh += [ycyl(0, y1, zc, D["cs1_od"] / 2, 6)]                               # 30T 06B on the countershaft
    sh += [ycyl(0, y1, zg, D["drive_pd"] / 2 + 5, 6)]                         # 10T 06B on the gearmotor
    # guards: flat sheet rings round the sprockets and plates along both chain runs (fixed to the frame)
    gr, cr = D["guard_r"], D["cs_guard_r"]
    ring = lambda z, y, rr, w: ycyl(0, y, z, rr, w) - ycyl(0, y, z, rr - 2, w - 4)
    guard = ring(Z0, y2, gr, 30) + ring(zc, y1, cr, 26)
    for s_ in (-1, 1):
        guard += box(s_ * (gr - 1), y2, (Z0 + zc) / 2, 2, 30, p["cs_z"])
        guard += box(s_ * (cr - 1), y1, (zc + zg) / 2, 2, 26, zg - zc)
    sh += [guard]
    parts["drive"] = Compound(children=sh)

    # 4 Worm gearmotor with brake
    gx, gy, gzz = p["gm_box"]
    gmz = Z0 + p["gm_z"]
    parts["gearmotor"] = Compound(children=[
        box(-gx / 2 + 2, 60, gmz, gx, gy, gzz),
        ycyl(-gx / 2 + 2, -40, gmz, p["motor_r"], p["motor_l"])])

    # 5 and 6 Motor driver and controller with IMU, side by side in one IP54 box
    ex, ey, ez = p["ebox"]
    parts["driver"] = box(-ex / 2 - 12, -ey / 4, Z0 + p["ebox_z"], ex, ey / 2 - 2, ez)
    parts["controller"] = box(-ex / 2 - 12, ey / 4, Z0 + p["ebox_z"], ex, ey / 2 - 2, ez)

    # 8 Main switch, fuse and harness (runs on the frame back)
    parts["harness"] = Compound(children=[
        tube((-30, -20, Z0 + p["pack_z"] - p["pack"][2] / 2), (-30, -20, Z0 + p["ebox_z"] + ez / 2), 6),
        tube((-30, -60, Z0 + p["ebox_z"] - ez / 2), (-30, -60, Z0 + p["gm_z"] + p["motor_r"]), 6),
        tube((-30, 150, Z0 + p["ebox_z"] + ez / 2), (-30, 150, ztop - 60), 5),
        box(-35, 150, Z0 + p["pack_z"] - 100, 40, 40, 40)])

    # 7 Battery pack in a quick-release cradle
    px, py, pz = p["pack"]
    parts["pack"] = box(-px / 2 - 8, 0, Z0 + p["pack_z"], px, py, pz)

    # 9 Handle grip with dead-man lever and control pod
    parts["handle"] = Compound(children=[
        tube((p["handle_x"], -150, gz), (p["handle_x"], 150, gz), p["grip_r"]),
        box(p["handle_x"] - 30, 0, gz - 14, 20, 200, 14),
        box(p["handle_x"] - 22, 0, gz - 40, 36, 90, 30)])

    # 11 Nosing guard skids (UHMW strips on the frame back, outboard of the components)
    z0s, z1s = p["skid_z"]
    parts["skids"] = Compound(children=[
        box(p["skid_x"] + 5, s * 150, Z0 + (z0s + z1s) / 2, 10, 25, z1s - z0s) for s in (-1, 1)] +
        [tube((p["skid_x"] + 5, s * 150, Z0 + z0s), (rx, s * ry, Z0 - 40), 6) for s in (-1, 1)] +
        [tube((p["skid_x"] + 5, s * 150, Z0 + z1s), (rx, s * ry, Z0 + z1s + 60), 6) for s in (-1, 1)])

    # 10 Load strap
    parts["strap"] = box(rx + 55, 0, Z0 + 700, 10, 420, 40)
    return parts


def tilted(parts, p=PARAMS):
    """Rotate frame-mounted parts back about the shaft (top toward -X). Clusters stay put."""
    from build123d import Pos, Rot
    z0 = derived(p)["hub_z"]
    out = {}
    for k, v in parts.items():
        out[k] = v if k == "clusters" else Pos(0, 0, z0) * Rot(0, -p["tilt"], 0) * Pos(0, 0, -z0) * v
    return out


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    # The STEP writer refuses a shape already written into another file, so each export gets
    # its own fresh build.
    for name, key in [("stepclimber-assembly", None), ("stepclimber-cluster-pair", "clusters"),
                      ("stepclimber-frame", "frame"), ("stepclimber-drive", "drive")]:
        fresh = build()
        shape = Compound(children=list(fresh.values())) if key is None else fresh[key]
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
    parts = build()
    asm = Compound(children=list(parts.values()))
    bb = asm.bounding_box()
    D = derived()
    print(f"Assembly bounding box (upright): {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (X x Y x Z)")
    print(f"Width {D['width']:.0f} mm, upright height {D['height_upright']:.0f} mm (formula), model top {bb.max.Z:.0f} mm")
    print(f"Hub height {D['hub_z']:.1f} mm, wheel spacing {D['spacing']:.1f} mm, cluster diameter {D['cluster_dia']:.0f} mm")
    print(f"Final stage 08B {PARAMS['z_cs2']}T to {PARAMS['z_driven']}T: shaft sprocket PD {D['sprocket_pd']:.1f} mm, "
          f"OD {D['sprocket_od']:.1f} mm; guard radius {D['guard_r']:.1f} mm")
    print(f"First stage 06B {PARAMS['z_drive']}T to {PARAMS['z_cs1']}T; countershaft guard radius {D['cs_guard_r']:.1f} mm; "
          f"overall ratio {D['ratio']:.0f}:1")
    print(f"Folded height with Option C hinge (study): {D['folded_height']:.0f} mm")

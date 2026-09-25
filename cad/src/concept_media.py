"""StepClimber concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X points toward the load side (the toe plate), Y across the truck,
Z up, floor at Z = 0. The cluster drive shaft (axle) sits at X = 0, Z = AXLE_Z.
The truck is shown tilted back 30 degrees, as it is held while climbing, at the foot
of a stair that rises toward -X. The operator climbs ahead of the truck and pulls it up
backwards, one step per one-third turn of the tri-star clusters.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# ---------------- key parameters (concept values, proposed) ----------------
WHEEL_R = 75.0          # 150 mm solid rubber wheels
WHEEL_W = 45.0
ARM = 135.0             # cluster hub to wheel center; wheel-center spacing = ARM * sqrt(3), about 234 mm
AXLE_Z = WHEEL_R + ARM * math.sin(math.radians(30))   # hub height with two wheels on the floor, about 143 mm
TILT = 30.0             # frame tilt back from vertical while climbing, degrees
RAIL_Y = 200.0          # rail centerline half-spacing
CLUSTER_Y = 262.0       # cluster mid-plane half-spacing; overall width about 570 mm
FRAME_H = 1150.0        # rail length above the axle
RISER, TREAD, N_STEPS = 180.0, 260.0, 5   # context stair (IRC allows up to 196 mm and down to 254 mm)

STEEL = "#4B5563"
RUBBER = "#1F2937"


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def yaxis_cyl(x, y, z, r, w):
    """Cylinder with its axis along Y, centered at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, w)


def tilt(shape):
    """Tilt a frame-mounted shape back about the axle (top toward -X)."""
    return Pos(0, 0, AXLE_Z) * Rot(0, -TILT, 0) * Pos(0, 0, -AXLE_Z) * shape


# Frame parts are modeled upright (frame vertical, axle at X = 0), then tilted.
Z0 = AXLE_Z  # shorthand

# 1 Steel hand truck frame: two rails, cross bars, loop handle and toe plate
rails = None
for s in (-1, 1):
    r = tube3((40, s * RAIL_Y, Z0 - 110), (40, s * RAIL_Y, Z0 + FRAME_H), 15)
    rails = r if rails is None else rails + r
cross = None
for dz in (60, 380, 700, 1000):
    c = tube3((40, -RAIL_Y, Z0 + dz), (40, RAIL_Y, Z0 + dz), 11)
    cross = c if cross is None else cross + c
loop = (tube3((40, -RAIL_Y, Z0 + FRAME_H), (-40, -150, Z0 + FRAME_H + 110), 13)
        + tube3((40, RAIL_Y, Z0 + FRAME_H), (-40, 150, Z0 + FRAME_H + 110), 13))
toe = Pos(40 + 120, 0, Z0 - 110 - 4) * Box(240, 380, 8)
axle_mount = None
for s in (-1, 1):
    m = Pos(15, s * RAIL_Y, Z0) * Box(80, 16, 90)
    axle_mount = m if axle_mount is None else axle_mount + m
frame = rails + cross + loop + toe + axle_mount

# 2 Tri-star wheel clusters (pair): spider plates and three wheels each
clusters = None
for s in (-1, 1):
    y = s * CLUSTER_Y
    for a in (90, 210, 330):
        t = math.radians(a)
        wx, wz = ARM * math.cos(t), Z0 + ARM * math.sin(t)
        arm = tube3((0, y - s * 30, Z0), (wx, y - s * 30, wz), 16)
        wheel = yaxis_cyl(wx, y, wz, WHEEL_R, WHEEL_W) - yaxis_cyl(wx, y, wz, 22, WHEEL_W + 2)
        hub = yaxis_cyl(wx, y, wz, 22, WHEEL_W + 20)
        piece = arm + wheel + hub
        clusters = piece if clusters is None else clusters + piece
    boss = yaxis_cyl(0, y - s * 30, Z0, 38, 26)
    clusters = clusters + boss

# 3 Cluster drive shaft, bearings and chain drive (guarded) from the gearbox down to the shaft
shaft = yaxis_cyl(0, 0, Z0, 14, 2 * CLUSTER_Y - 40)
bearings = yaxis_cyl(0, RAIL_Y + 14, Z0, 30, 20) + yaxis_cyl(0, -RAIL_Y - 14, Z0, 30, 20)
guard = Pos(-45, 120, Z0 + 125) * Box(80, 24, 330)
drive = shaft + bearings + guard

# 4 Worm gearmotor, 24 V about 250 W, with built-in spring-applied brake (wheelchair type)
gearbox = Pos(-45, 60, Z0 + 290) * Box(95, 90, 95)
motor = yaxis_cyl(-45, -40, Z0 + 290, 42, 150)
gearmotor = gearbox + motor

# 5 Motor driver and 6 controller with IMU in one sealed enclosure on the back of the frame
driver = Pos(-35, -95, Z0 + 520) * Box(50, 150, 110)
ctrl = Pos(-35, 95, Z0 + 520) * Box(50, 150, 110)

# 7 24 V LiFePO4 pack, 8S about 10 Ah, in a quick-release cradle between the rails
pack = Pos(-45, 0, Z0 + 800) * Box(75, 180, 170)

# 8 Main switch, fuse and harness
harness = (tube3((-30, -20, Z0 + 715), (-30, -20, Z0 + 580), 6)
           + tube3((-30, -60, Z0 + 465), (-30, -60, Z0 + 340), 6)
           + tube3((-30, 150, Z0 + 580), (-30, 150, Z0 + 1060), 5))
switch = Pos(-35, 150, Z0 + 700) * Box(40, 40, 40)
wiring = harness + switch

# 9 Handle with dead-man grip lever, up and down thumb switch and status light bar
grip = tube3((-40, -150, Z0 + FRAME_H + 110), (-40, 150, Z0 + FRAME_H + 110), 17)
lever = Pos(-70, 0, Z0 + FRAME_H + 95) * Box(22, 200, 16)
pod = Pos(-40, 0, Z0 + FRAME_H + 145) * Box(60, 90, 40)
handle = grip + lever + pod

# 10 Load strap with ratchet, and 11 stair-nosing guard skids (UHMW strips on the frame back)
strap = Pos(95, 0, Z0 + 700) * Box(10, 420, 40)
skids = None
for s in (-1, 1):
    k = tube3((25, s * (RAIL_Y - 45), Z0 + 150), (25, s * (RAIL_Y - 45), Z0 + 650), 9)
    skids = k if skids is None else skids + k

T = tilt
parts = [
    Part("Steel hand truck frame and toe plate", T(frame), STEEL, 1, (0, 0, 0)),
    Part("Tri-star wheel clusters (pair)", clusters, RUBBER, 2, (0, 0, -260)),
    Part("Cluster shaft, bearings and chain drive", T(drive), "#D4A017", 3, (-250, -450, -200)),
    Part("Worm gearmotor with brake, 24 V", T(gearmotor), "#0F766E", 4, (-560, -560, -60)),
    Part("Motor driver, 24 V 30 A", T(driver), "#115E59", 5, (-380, -380, 230)),
    Part("Controller with IMU tilt sensor", T(ctrl), "#7C3AED", 6, (380, 380, 230)),
    Part("24 V LiFePO4 pack, 10 Ah", T(pack), "#C2410C", 7, (-250, -250, 330)),
    Part("Main switch, fuse and harness", T(wiring), "#111827", 8, (520, 680, -300)),
    Part("Handle with dead-man grip", T(handle), "#2563EB", 9, (-160, 0, 300)),
    Part("Load strap with ratchet", T(strap), "#EAB308", 10, (480, 0, 120)),
    Part("Nosing guard skids", T(skids), "#94A3B8", 11, (-60, -300, -330)),
]

# ---------------- context for the hero only ----------------
# Stair rising toward -X; the rear lower wheels just touch the first riser.
rear_wheel_x = ARM * math.cos(math.radians(210)) - WHEEL_R
x0 = rear_wheel_x - 3
stair = None
for i in range(N_STEPS):
    blk = Pos(x0 - i * TREAD - (N_STEPS - i) * TREAD / 2, 0, (i + 1) * RISER / 2) * Box((N_STEPS - i) * TREAD, 1000, (i + 1) * RISER)
    stair = blk if stair is None else stair + blk
# Payload: a stack of parcels on the toe plate, tilted with the frame
parcels = T(Pos(160, 0, Z0 - 106 + 160) * Box(230, 340, 320))
context = [Part("Stair, 180 mm risers and 260 mm treads", stair, "#D1D5DB"),
           Part("Parcel carton", parcels, "#C8A26B")]

render_all(
    parts, project="StepClimber", title="Powered tri-star hand truck concept", dwg_no="SCM-DWG-010",
    key_figures=["Rated stair load 60 kg (132 lb) payload (proposed)",
                 "Tri-star clusters: 150 mm wheels, 234 mm wheel spacing",
                 "One step per 1/3 turn; about 20 steps/min (target)",
                 "About 500 J (0.14 Wh) from pack per loaded step up (estimate)",
                 "About 1,300 loaded steps per 256 Wh charge (estimate)",
                 "About 24 kg truck mass; about $580 parts (indicative)"],
    cut=False, context=context, date="2026-09-25",
    flow={"title": "energy for one loaded step up, J per step (estimates: 84 kg, 196 mm riser)", "unit": "J",
          "stages": [("Pack output", 499), ("Driver output", 474), ("Motor shaft", 379),
                     ("Worm output", 171), ("Lift at clusters", 162)],
          "losses": [(0, "Driver (5 %)", 25), (1, "Motor (20 %)", 95),
                     (2, "Self-locking worm (55 %)", 208), (3, "Chain and bearings (5 %)", 9)]},
)

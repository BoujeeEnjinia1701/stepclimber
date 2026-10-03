"""StepClimber concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py (build and tilted); not for fabrication.

The truck is shown tilted back to its climbing angle at the foot of a stair that rises
toward -X. The operator climbs ahead of the truck and pulls it up backwards, one step per
one third of a turn of the tri-star clusters. Figures on the sheet come from
docs/04-calcs/sizing.py (SCM-CAL-001).
"""
import math
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / ".kit"))
sys.path.insert(0, str(HERE))
from build123d import Box, Pos, Rot  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import PARAMS as P, build, tilted, derived  # noqa: E402
import svg_fix  # noqa: E402,F401  (SVG export workaround)

D = derived()
S = tilted(build())
STEEL, RUBBER = "#4B5563", "#1F2937"

parts = [
    Part("Steel hand truck frame and toe plate", S["frame"], STEEL, 1, (0, 0, 0)),
    Part("Tri-star wheel clusters (pair)", S["clusters"], RUBBER, 2, (0, 0, -260)),
    Part("Cluster shaft, bearings and chain drive", S["drive"], "#D4A017", 3, (-250, -450, -200)),
    Part("Worm gearmotor with brake, 24 V", S["gearmotor"], "#0F766E", 4, (-560, -560, -60)),
    Part("Motor driver, 24 V 30 A", S["driver"], "#115E59", 5, (-380, -420, 230)),
    Part("Controller with IMU tilt sensor", S["controller"], "#7C3AED", 6, (380, 420, 230)),
    Part("24 V LiFePO4 pack, 10 Ah", S["pack"], "#C2410C", 7, (-250, -250, 330)),
    Part("Main switch, fuse and harness", S["harness"], "#111827", 8, (520, 680, -300)),
    Part("Handle with dead-man grip", S["handle"], "#2563EB", 9, (-160, 0, 300)),
    Part("Load strap with ratchet", S["strap"], "#EAB308", 10, (480, 0, 120)),
    Part("Nosing guard skids", S["skids"], "#94A3B8", 11, (-60, -300, -330)),
    Part("Component uprights", S["uprights"], "#A8A29E", 15, (-200, 300, 450)),
]

# ---------------- context for the hero only ----------------
# Design stair (196 mm risers, 254 mm treads) rising toward -X; the lower rear wheels touch the first riser.
RISER, TREAD, N_STEPS = 196.0, 254.0, 5
rear_wheel_x = P["arm"] * math.cos(math.radians(210)) - P["wheel_r"]
x0 = rear_wheel_x - 3
stair = None
for i in range(N_STEPS):
    blk = Pos(x0 - i * TREAD - (N_STEPS - i) * TREAD / 2, 0, (i + 1) * RISER / 2) * Box((N_STEPS - i) * TREAD, 1000, (i + 1) * RISER)
    stair = blk if stair is None else stair + blk
z0 = D["hub_z"]
carton = Pos(P["rail_x"] + 140, 0, z0 - P["rail_below"] + 160) * Box(230, 340, 320)
parcels = Pos(0, 0, z0) * Rot(0, -P["tilt"], 0) * Pos(0, 0, -z0) * carton
context = [Part("Stair, 196 mm risers and 254 mm treads", stair, "#D1D5DB"),
           Part("Parcel carton", parcels, "#C8A26B")]

render_all(
    parts, project="StepClimber", title="Powered tri-star hand truck concept", dwg_no="SCM-DWG-010",
    key_figures=["Rated stair load 60 kg (132 lb) payload (decided)",
                 "Tri-star clusters: 200 mm wheels, 150 mm arms, 260 mm spacing",
                 "One step per 1/3 turn; 244 W peak at 16 steps/min (calc)",
                 "575 J (0.16 Wh) from the pack per loaded step up (calc)",
                 "About 1,215 loaded steps per 256 Wh charge (calc)",
                 "34.2 kg truck; R3, R5, R6 met on paper for the first prototype (SCM-CAL-001 v0.5)"],
    cut=False, context=context, date="2026-10-02",
    flow={"title": "energy for one loaded step up, J per step (calculated: 94 kg, 196 mm riser)", "unit": "J",
          "stages": [("Pack output", 575), ("Driver output", 546), ("Motor shaft", 437),
                     ("Worm output", 197), ("Lift at clusters", 181)],
          "losses": [(0, "Driver (5 %)", 29), (1, "Motor (20 %)", 109),
                     (2, "Self-locking worm (55 %)", 240), (3, "Chains (8 %)", 16)]},
)

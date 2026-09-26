"""StepClimber general arrangement sheet SCM-DWG-001 Rev P2.

Run from the repo root:  python cad/src/sheets.py
Geometry from cad/src/model.py (upright pose); figures from docs/04-calcs/sizing.py (SCM-CAL-001).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad/src"))
from build123d import Compound  # noqa: E402
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, build, derived, tilted  # noqa: E402

D = derived()
parts = build()
asm = Compound(children=list(parts.values()))
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
tilt_views = project_views(Compound(children=list(tilted(build()).values())), work / "tilt")

s = Sheet(project="StepClimber", title="General arrangement", dwg_no="SCM-DWG-001",
          rev="P2", author="Amish Chadha", date="2026-09-25",
          material="Steel frame and spiders; solid rubber wheels; see bom/bom.csv. Figures from SCM-CAL-001 v0.2",
          revisions=[("P1", "Preliminary general arrangement, TRL 3", "2026-09-25", "AC"),
                     ("P2", "200 mm wheels, 150 mm arms, two-stage drive (SCM-DDR-002)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale")
s.add_svg(tilt_views["front"], 176, 100, 60, 70, scale=1 / 20, label="Front view, climbing pose",
          sublabel="Tilted 30 deg about the shaft; scale 1:20")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Overall width {D['width']:.0f} (wheel outer faces); upright height {D['height_upright']:.0f}",
    f"Clusters: arm {P['arm']:.0f}, wheel dia {2 * P['wheel_r']:.0f}, spacing {D['spacing']:.1f}",
    f"Shaft {P['shaft_d']:.0f} dia at {D['hub_z']:.1f} above floor; bearings {2 * P['rail_y']:.0f} + 28 apart",
    f"Cluster mid-planes {2 * P['cluster_y']:.0f} apart; rails {2 * P['rail_y']:.0f} apart, 28 tube",
    f"Drive 06B {P['z_drive']}T:{P['z_cs1']}T then 08B {P['z_cs2']}T:{P['z_driven']}T ({D['ratio']:.0f}:1)",
    f"Countershaft {P['cs_z']:.0f} and gearmotor {P['chain_c']:.0f} above the shaft, along the frame",
    f"Shaft sprocket OD {D['sprocket_od']:.0f}; guard radius {D['guard_r']:.1f} (limit 54.2, R15 met)",
    f"Grip {D['handle_len']:.0f} from the shaft along the frame; toe plate {P['toe_l']:.0f} x {P['toe_w']:.0f}",
    f"Pack cradle {P['pack'][0]:.0f} x {P['pack'][1]:.0f} x {P['pack'][2]:.0f}, center {P['pack_z']:.0f} above shaft",
    "Climbing tilt 30 deg back; tilt window +/-6 deg; 60 kg rated stair load",
], x=240, y=150, width=172)
s.save(ROOT / "cad/drawings/SCM-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("Wrote cad/drawings/SCM-DWG-001.svg, .pdf and .png")

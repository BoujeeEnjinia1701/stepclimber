"""StepClimber prototype build plan pictures (SCM-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SCM-DWG-101 to 109        making sketches for the made and modified components
    docs/05-build-plan/case-holes.png      hole layout of the axle plate and both chain case plates
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
A single picture can be drawn with, for example, `steps 4` or `sheets 105`.
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, case_outline, BRG, fuse, bx  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
Z0 = D["hub_z"]
_C = None


def C():
    global _C
    if _C is None:
        _C = build_components(P)
    return _C


def S(*ks):
    return fuse([C()[k].shape for k in ks])


COL = {"frame": "#9CA3AF", "low_bar": "#B45309", "plate": "#57534E", "outer": "#0E7490", "inner": "#94A3B8",
       "band": "#CBD5E1", "spacer": "#7C3AED", "brg": "#1D4ED8", "shaft": "#6B7280", "spr": "#D4A017",
       "chain": "#111827", "gm": "#0F766E", "spider": "#0F766E", "hub": "#1E3A8A", "stub": "#B45309",
       "wheel": "#1F2937", "fix": "#111827", "up": "#A8A29E", "ebox": "#E5E7EB", "driver": "#16A34A",
       "pack": "#C2410C", "cradle": "#78716C", "switch": "#7C3AED", "harness": "#111827", "controls": "#2563EB",
       "skid": "#F5F5F4", "standoff": "#B45309", "strap": "#EAB308"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def floor(w=900, d=700):
    return part("Floor", bx(-d / 2, d / 2, -w / 2, w / 2, -3, 0), "#E5E7EB")


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "frame": part("Hand truck frame (bought)", S("frame"), COL["frame"]),
        "low_bar": part("Replacement lowest cross bar", S("low_bar"), COL["low_bar"]),
        "axle_plate": part("Axle plate, plain side", S("axle_plate"), COL["plate"]),
        "outer": part("Chain case outer plate", S("case_outer"), COL["outer"]),
        "standoffs": part("Skid standoffs (4)", S("standoffs"), COL["standoff"]),
        "brg_main": part("Main shaft bearings (2)", S("brg_main_l", "brg_main_r"), COL["brg"]),
        "brg_cs_out": part("Outer countershaft bearing", S("brg_cs_out"), COL["brg"]),
        "inner": part("Chain case inner plate and spacers", S("case_inner", "spacers", "spacer_screws"), COL["inner"]),
        "brg_cs_in": part("Inner countershaft bearing", S("brg_cs_in"), COL["brg"]),
        "shaft": part("Cluster shaft and 20-tooth sprocket", S("shaft", "spr_main"), COL["shaft"]),
        "cs": part("Countershaft and its two sprockets", S("cs_shaft", "spr_cs"), COL["spr"]),
        "gm": part("Worm gearmotor and 10-tooth sprocket", S("gearmotor", "spr_gm", "gm_bolts"), COL["gm"]),
        "chains": part("Chains (2)", S("chain1", "chain2"), COL["chain"]),
        "band": part("Chain case band", S("case_band"), COL["band"]),
        "spiders": part("Spiders with weld-on hubs and stub axles (2)", S("spider_l", "spider_r", "hub_l", "hub_r", "stubs_l", "stubs_r"), COL["spider"]),
        "wheels": part("Wheels (6) and their fixings", S("wheels_l", "wheels_r", "wheel_fix_l", "wheel_fix_r"), COL["wheel"]),
        "uprights": part("Component uprights (2)", S("uprights", "up_bolts"), COL["up"]),
        "ebox": part("Electronics box with driver and controller", S("ebox", "driver"), COL["ebox"]),
        "switch": part("Fuse box and key switch", S("switchbox"), COL["switch"]),
        "pack": part("Pack cradle and pack", S("cradle", "pack"), COL["pack"]),
        "harness": part("Harness", S("harness"), COL["harness"]),
        "controls": part("Handle controls", S("controls"), COL["controls"]),
        "skids": part("Nosing guard skids (2)", S("skids", "skid_screws"), "#D6D3D1"),
        "strap": part("Load strap", S("strap"), COL["strap"]),
    }


ORDER = ["frame", "low_bar", "axle_plate", "outer", "standoffs", "brg_main", "brg_cs_out", "inner", "brg_cs_in",
         "shaft", "cs", "gm", "chains", "band", "spiders", "wheels", "uprights", "ebox", "switch", "pack",
         "harness", "controls", "skids", "strap"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"frame": (0, 0, 0), "low_bar": (0, -150, -330), "axle_plate": (0, -380, -150), "outer": (0, 450, -200),
           "standoffs": (-330, 0, 0), "brg_main": (0, 0, -520), "brg_cs_out": (0, 650, -60), "inner": (0, 850, -200),
           "brg_cs_in": (0, 1050, -60), "shaft": (0, 0, -680), "cs": (0, 650, 230), "gm": (0, 1080, 330),
           "chains": (0, 850, 330), "band": (0, 650, -420), "spiders": (0, -650, -700), "wheels": (0, -650, -1080),
           "uprights": (-450, -350, 0), "ebox": (-650, -650, 50), "switch": (-650, -650, 300), "pack": (-650, -650, 520),
           "harness": (-450, -1050, -450), "controls": (-200, 0, 350), "skids": (-650, -200, -300), "strap": (500, 0, 250)}
    parts = []
    for k in ORDER:
        p = M[k]
        parts.append(mv(p, off[k]))
    return bv.overview(parts, OUT / "overview.png", "StepClimber prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Upright, seen from the drive side and the back (the stair side)",
                       elev=14, azim=135, size=(12, 10), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def flat_y(shape, y0):
    """A plate lying in the frame plane, moved so its outline is drawn as the front view."""
    import build123d as b
    return b.Pos(0, -y0, -Z0) * shape


def sheets(which=None):
    import build123d as b
    M = made()
    base = dict(project="StepClimber", date=DATE)
    out = []
    cs, gm = (P["cs_x"], P["cs_z"]), (P["cs_x"], P["gm_z"])
    o = case_outline(P)
    ob = o.bounds
    want = lambda n: which is None or str(n) in which  # noqa: E731

    if want(101):
        out.append(bv.component_sheet(
            Part("Axle plate", S("axle_plate"), COL["plate"]), [M["frame"], M["brg_main"], M["shaft"]],
            dwg_no="SCM-DWG-101", title="StepClimber axle plate, plain side: making sketch", material="Steel plate 4 mm, S275 or similar",
            view_shape=flat_y(S("axle_plate"), 0), inset_view=(18, -120),
            notes=["Laser cut 92 x 144 mm, 15 mm corner radius, from 4 mm steel.",
                   "Bearing bore 44 mm: 40 mm from the back edge, 72 mm from the bottom.",
                   "Bearing bolt holes 13 mm, 49.5 mm above and below the bore centre.",
                   "The back edge faces the stair; the front edge faces the load.",
                   "Fit: weld it to the inside face of the left rail, its bore centre",
                   "  40 mm behind the rail centre line and 142.5 mm above the toe plate.",
                   "  Fillet weld both sides along the rail, 150 mm long.",
                   "Weld it with the outer case plate on a straight 25 mm bar through",
                   "  both bores, so the two bores line up.",
                   "The 25 mm flange bearing bolts to its inside face with two M12",
                   "  bolts, nyloc nuts on the outside.",
                   "Check: the bar turns freely in both bores after welding."],
            **base))
    if want(102):
        out.append(bv.component_sheet(
            Part("Chain case outer plate", S("case_outer"), COL["outer"]), [M["frame"], M["brg_main"], M["brg_cs_out"], M["shaft"]],
            dwg_no="SCM-DWG-102", title="StepClimber chain case outer plate: making sketch", material="Steel plate 3 mm, S275 or similar",
            view_shape=flat_y(S("case_outer"), 0), inset_view=(18, 60),
            notes=[f"Laser cut to the outline shown, {ob[2] - ob[0]:.0f} x {ob[3] - ob[1]:.0f} mm, from 3 mm steel.",
                   "All positions from the main bore centre, up the plate and toward",
                   "  the back (the stair side); the hole layout picture repeats them.",
                   "Main bore 44 mm; its bolt holes 13 mm at 49.5 mm above and below.",
                   f"Countershaft bore: a 36 mm slot, {cs[1]:.1f} mm up, {-cs[0]:.0f} mm back,",
                   "  8 mm long up the plate; bolt slots 11 mm wide, 45 mm above and",
                   "  below it, also 8 mm long. The slots let the chains be tensioned.",
                   f"Spacer holes 9 mm, {P['spacer_z']:.0f} mm up, {P['spacer_dx'] - cs[0]:.0f} mm back and {P['spacer_dx'] + cs[0]:.0f} mm",
                   "  forward; countersink them on the outside face.",
                   "Fit: weld to the inside face of the right rail like the axle plate,",
                   "  on the same alignment bar; the countersinks face the rail.",
                   "Check: nothing stands proud of the outside face but the welds."],
            **base))
    if want(103):
        out.append(bv.component_sheet(
            Part("Chain case inner plate", S("case_inner", "spacers"), COL["inner"]), [M["outer"], M["band"], M["gm"], M["brg_cs_in"]],
            dwg_no="SCM-DWG-103", title="StepClimber chain case inner plate and spacers: making sketch",
            material="Aluminium plate 3 mm, 5052 or 5083; spacers 16 mm steel bar",
            view_shape=flat_y(S("case_inner"), 0), inset_view=(18, -60),
            notes=["Laser cut to the same outline as the outer plate, from 3 mm aluminium.",
                   "Holes from the main shaft centre, as on the outer plate, except:",
                   "  shaft hole 32 mm (clearance, no bearing on this plate);",
                   f"  gearmotor output hole 28 mm, {gm[1]:.0f} mm up, {-gm[0]:.0f} mm back;",
                   "  gearmotor screw slots 9 mm wide, 8 mm long up the plate: 40 mm",
                   "  either side of the output hole and 40 mm above it;",
                   "  countershaft bolt slots countersunk on the case side.",
                   "Spacers (make 2): 16 mm bar, 86 mm long, ends square, drilled 6.8",
                   "  and tapped M8 20 deep at both ends.",
                   "Fit: the spacers stand between the plates on M8 screws, countersunk",
                   "  through the outer plate, button heads on this plate's outside.",
                   "Check: the plates are parallel, 86 mm apart, at the spacers."],
            **base))
    if want(104):
        band = S("case_band")
        out.append(bv.component_sheet(
            Part("Chain case band", band, COL["band"]), [M["outer"], M["inner"], M["chains"]],
            dwg_no="SCM-DWG-104", title="StepClimber chain case band: making sketch", material="Aluminium sheet 1.5 mm, 5052",
            view_shape=flat_y(band, 0), inset_view=(18, 60),
            notes=[f"Cut a strip 86 mm wide and {o.length + 30:.0f} mm long from 1.5 mm aluminium.",
                   "Bend it round the plate outline (front view), starting at the bottom",
                   "  of the load side; the ends overlap 30 mm there.",
                   "Bend the tight curves over a 50 mm round bar; ease the long",
                   "  straights by hand. Keep the edges straight and square.",
                   "Rivet eight small aluminium angle tabs inside the band, 3 mm in",
                   "  from each edge: four for each plate, spread round the outline.",
                   "Drill each tab and the plate behind it 4.5 mm for an M4 screw.",
                   "Fit: the band sits between the plates, flush with their edges.",
                   "  It goes on last, after the chains are tensioned.",
                   "Check: no gap wider than 2 mm between the band and either plate;",
                   "  turn the shafts by hand: nothing rubs the band."],
            **base))
    if want(105):
        sp = S("spider_r", "hub_r", "stubs_r")
        out.append(bv.component_sheet(
            Part("Spider with hub and stub axles", sp, COL["spider"]), [M["shaft"], M["wheels"], M["frame"]],
            dwg_no="SCM-DWG-105", title="StepClimber spider with hub and stub axles (make 2): making sketch",
            material="Steel plate 6 mm S275; 1610 weld-on hub; 20 mm bright bar",
            view_shape=flat_y(sp, 0), inset_view=(15, 60),
            notes=["Laser cut two spiders from 6 mm steel: three arms 45 mm wide at",
                   "  120 degrees, round ends of 22.5 mm radius, a 96 mm centre disc.",
                   "Holes: 76 mm in the centre for the hub; 20 mm for each stub axle,",
                   "  150 mm from the centre (260 mm apart, hole to hole).",
                   "Hub: a 1610 weld-on taper-lock hub, 76 mm across and 26 mm long,",
                   "  through the centre hole, 10 mm proud each side; weld both sides.",
                   "Stub axles (make 6): 20 mm bright bar cut to 55 mm; drill 8.5 mm",
                   "  and tap M10 20 deep in one end. Push through each 20 mm hole,",
                   "  plain end flush with the spider's inner face; weld both sides.",
                   "Make the two spiders as a mirrored pair: stubs on the outer side.",
                   "Check: the stubs are square to the spider within 0.5 mm over",
                   "  50 mm, and all three at 150 mm, within 0.5 mm, from the centre."],
            **base))
    if want(106):
        sh = S("shaft", "cs_shaft")
        out.append(bv.component_sheet(
            Part("Cluster shaft and countershaft", sh, COL["shaft"]), [M["outer"], M["axle_plate"], M["brg_main"], M["spiders"]],
            dwg_no="SCM-DWG-106", title="StepClimber cluster shaft and countershaft: making sketch",
            material="Keyed bright steel shaft 25 mm and 20 mm, with keys",
            view_shape=b.Pos(0, 0, -Z0) * sh, inset_view=(18, 125),
            notes=[f"Cluster shaft: cut 25 mm keyed shaft to {2 * P['shaft_half']:.0f} mm; chamfer both ends 1 mm.",
                   "  The key runs its full length (bought keyed stock).",
                   "Countershaft: cut 20 mm keyed shaft to 124 mm; chamfer both ends.",
                   "The cluster shaft runs in the two 25 mm flange bearings 336 mm",
                   "  apart and carries the 20-tooth sprocket inside the chain case.",
                   "Each end carries a hub: the taper-lock bush clamps it to the",
                   "  shaft, its outer face flush with the shaft end.",
                   f"The countershaft sits {cs[1]:.1f} mm up the frame and {-cs[0]:.0f} mm behind the",
                   "  cluster shaft, in two 20 mm flange bearings 86 mm apart, one on",
                   "  each case plate; its two sprockets sit between them.",
                   "Check: both shafts slide through their bearings by hand before",
                   "  the bearing grub screws are tightened."],
            **base))
    if want(107):
        up = S("uprights")
        one = up & bx(-300, 300, 0, 400, -100, 3000)
        out.append(bv.component_sheet(
            Part("Component upright", one, COL["up"]), [M["frame"], M["ebox"], M["pack"]],
            dwg_no="SCM-DWG-107", title="StepClimber component upright (make 2): making sketch",
            material="Aluminium flat bar 30 x 6 mm, 6082 or 6063",
            view_shape=b.Pos(0, -P["up_y"], -Z0 - P["bars"][0] + P["bar_r"]) * one, inset_view=(15, 125),
            notes=["Cut two 642 mm lengths of 30 x 6 mm aluminium flat bar.",
                   "Holes 6.5 mm on the centre line, 11, 331 and 631 mm from the",
                   "  bottom: these bolt through the three upper cross bars.",
                   "Mark the cross bars through the uprights and drill them 6.5 mm,",
                   "  front to back. M6 x 70 bolts, nyloc nuts on the load side.",
                   "The uprights stand 120 mm either side of the centre line on the",
                   "  back of the cross bars, bottom 11 mm below the lower bar.",
                   "Drill for the parts they carry, from the bottom of the upright:",
                   "  electronics box 126 to 236 mm; fuse box 271 to 311 mm;",
                   "  pack cradle 336 to 526 mm. Use each part's own mounting holes.",
                   "Deburr all holes. Do not weld aluminium to the steel frame.",
                   "Check: both uprights sit flat on all three bars."],
            **base))
    if want(108):
        so = S("standoffs", "skids") & bx(-300, 300, 0, 400, Z0 + 20, Z0 + 600)
        out.append(bv.component_sheet(
            Part("Skid standoffs and skid", so, COL["standoff"]), [M["frame"], M["outer"], M["uprights"]],
            dwg_no="SCM-DWG-108", title="StepClimber skid standoffs (make 4) and skids (2): making sketch",
            material="Steel square tube 20 x 20 x 1.5 mm; UHMW strip 25 x 10 mm",
            view_shape=b.Pos(0, -P["skid_y"], -Z0) * so, inset_view=(15, 125),
            notes=["Standoffs (make 4): cut 20 x 20 x 1.5 mm tube to 130 mm. Cope one",
                   "  end to fit the 28 mm rail (file to a 14 mm radius saddle).",
                   "Weld a 3 mm cap on the other end; drill 4.2 and tap it M5.",
                   "Weld each standoff square to the back of a rail, 140 and 510 mm",
                   "  above the shaft line, so the capped ends stand 100 mm behind",
                   "  the shaft line (90 mm to the cap face).",
                   "Skids (2): UHMW strip 25 x 10 mm cut to 500 mm. Countersink two",
                   "  holes 100 and 470 mm from the lower end; screw to the caps with",
                   "  M5 countersunk screws, heads below the skid face.",
                   "The skid runs from 40 to 540 mm above the shaft line.",
                   "Check: both skid faces in one plane, within 1 mm; the cluster",
                   "  turns past them with 15 mm or more to spare."],
            **base))
    if want(109):
        lb = S("low_bar")
        out.append(bv.component_sheet(
            Part("Replacement lowest cross bar", lb, COL["low_bar"]), [M["frame"], M["axle_plate"], M["outer"]],
            dwg_no="SCM-DWG-109", title="StepClimber frame changes and replacement lowest cross bar: making sketch",
            material="Steel tube 22 x 1.5 mm",
            view_shape=b.Pos(0, 0, -Z0 - P["low_bar"]) * lb, inset_view=(15, 125),
            notes=["Strip the bought frame: wheels, axle and axle brackets off.",
                   "Mark the shaft line on both rails, 142.5 mm above the toe plate.",
                   "Cut off any cross bar between 80 mm below and 360 mm above the",
                   "  shaft line (on the model frame, the bar 60 mm above it); grind",
                   "  the rails smooth and paint the bare steel.",
                   "Cut 22 mm tube to fit between the rails (372 mm inside); cope both",
                   "  ends to the 28 mm rails.",
                   "Weld it between the rails 105 mm below the shaft line, on the rail",
                   "  centre line, square to both rails.",
                   "The axle plates and skid standoffs then weld to the rails",
                   "  (sheets 101, 102 and 108).",
                   "Check: rails still 400 mm apart, within 1 mm, at the new bar."],
            **base))
    return out


# ----------------------------------------------------------------- hole layout of the plates
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MPoly, Circle, FancyBboxPatch
    from model import axle_plate_outline
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    cs, gm = (P["cs_x"], P["cs_z"]), (P["cs_x"], P["gm_z"])
    o = case_outline(P)
    fig = plt.figure(figsize=(13, 10), dpi=150)
    fig.text(0.03, 0.975, "Axle plate and chain case plates: hole layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.948, "Each plate drawn flat with the load side (forward) to the right and the stair side (back) to the left. "
             "Figures in mm, measured from the main shaft centre:\nup the plate, and back or forward of it. Slots run up the plate.",
             fontsize=8.5, color=MUT, va="top")

    def hole(ax, x, z, r, sl):
        if sl:
            ax.add_patch(FancyBboxPatch((x, z - sl), 1e-6, 2 * sl, boxstyle=f"round,pad={r}", fc="white", ec=INK, lw=0.9))
        else:
            ax.add_patch(Circle((x, z), r, fc="white", ec=INK, lw=0.9))
        ax.plot([x - r - 3, x + r + 3], [z, z], color=MUT, lw=0.35)
        ax.plot([x, x], [z - r - sl - 3, z + r + sl + 3], color=MUT, lw=0.35)

    def panel(x0, w, title, outline, holes, key, weld=True):
        ax = fig.add_axes([x0, 0.36, w, 0.51]); ax.set_aspect("equal"); ax.set_axis_off()
        xs, zs = outline.exterior.xy
        ax.add_patch(MPoly(list(zip(xs, zs)), closed=True, fc="#F3F4F6", ec=INK, lw=1.1))
        for n, (x, z, r, sl, dx, dz) in enumerate(holes, 1):
            hole(ax, x, z, r, sl)
            ax.text(x + dx, z + dz, str(n), fontsize=7, fontweight="bold", color="white", ha="center", va="center",
                    bbox=dict(boxstyle="circle,pad=0.25", fc=AC, ec="white", lw=0.6), zorder=5)
        b_ = outline.bounds
        if weld:
            ax.plot([40, 40], [b_[1] + 2, b_[3] - 2], color="#B45309", lw=1.0, ls=(0, (4, 2)))
        ax.plot([0, 0], [b_[1] - 10, b_[3] + 8], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
        ax.text(b_[0] - 4, b_[1] - 16, "back", ha="left", fontsize=7, color=MUT)
        ax.text(b_[2] + 4, b_[1] - 16, "forward", ha="right", fontsize=7, color=MUT)
        ax.set_xlim(-100, 75); ax.set_ylim(-95, 365)
        fig.text(x0, 0.885, title, fontsize=9.5, fontweight="bold", color=INK, va="bottom")
        for i, t in enumerate(key):
            fig.text(x0, 0.33 - i * 0.022, t, fontsize=7.8, color=INK, va="top")
        return ax
    g5 = BRG["205"]
    up, bk = lambda z: f"{z:g} up", lambda x: (f"{-x:g} back" if x < 0 else f"{x:g} forward" if x > 0 else "on the centre line")  # noqa: E731
    main = [(0, 0, 22, 0, 30, 18), (0, g5["bolt"], 6.5, 0, 16, 8), (0, -g5["bolt"], 6.5, 0, 16, -8)]
    csh = [(cs[0], cs[1], 18, 4, -32, 18), (cs[0], cs[1] + 45, 5.5, 4, 16, 6), (cs[0], cs[1] - 45, 5.5, 4, 16, -6)]
    sph = [(cs[0] - P["spacer_dx"], P["spacer_z"], 4.5, 0, -12, 12), (cs[0] + P["spacer_dx"], P["spacer_z"], 4.5, 0, 12, 12)]
    weld = "Dashed line: weld to the inside of the rail, 40 forward."
    panel(0.03, 0.26, "Axle plate, plain side (4 mm steel)", axle_plate_outline(P), main,
          ["1  Bearing bore 44, at 0, 0", "2  Bearing bolt hole 13, 49.5 up", "3  Bearing bolt hole 13, 49.5 down",
           "Plate 92 x 144, corners 15 radius; bore 40 from", "  the back edge and 72 from the bottom.", weld])
    panel(0.36, 0.28, "Case outer plate (3 mm steel)", o, main + csh + sph,
          ["1  Main bearing bore 44, at 0, 0", "2, 3  Bearing bolt holes 13, 49.5 up and down",
           f"4  Countershaft slot 36 wide, 8 long: {up(cs[1])}, {bk(cs[0])}",
           f"5, 6  Its bolt slots 11 wide, 8 long, 45 above and below 4",
           f"7  Spacer hole 9: {up(P['spacer_z'])}, {bk(cs[0] - P['spacer_dx'])} (countersunk outside)",
           f"8  Spacer hole 9: {up(P['spacer_z'])}, {bk(cs[0] + P['spacer_dx'])} (countersunk outside)", weld])
    gmh = [(gm[0], gm[1], 14, 0, 26, 16), (gm[0] - 40, gm[1], 4.5, 4, -14, 14), (gm[0] + 40, gm[1], 4.5, 4, 14, 14),
           (gm[0], gm[1] + 40, 4.5, 4, 16, 8)]
    panel(0.69, 0.28, "Case inner plate (3 mm aluminium)", o, [(0, 0, 16, 0, 26, 16)] + csh + sph + gmh,
          ["1  Shaft clearance hole 32, at 0, 0 (no bearing here)", "2 to 4  Countershaft slots as the outer plate;",
           "  bolt slots 3 and 4 countersunk on the case side", "5, 6  Spacer holes 9, as the outer plate",
           f"7  Gearmotor output hole 28: {up(gm[1])}, {bk(gm[0])}", "8 to 10  Gearmotor screw slots 9 wide, 8 long:",
           "  40 either side of 7 and 40 above it", "Same outline as the outer plate; no weld."], weld=False)
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/stepclimber", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "case-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "case-holes.png"


# ----------------------------------------------------------------- joints
def joints(which=None):
    out = []
    want = lambda n: which is None or str(n) in which  # noqa: E731
    W = lambda sh, x0, x1, y0, y1, z0, z1: sh & bx(x0, x1, y0, y1, Z0 + z0, Z0 + z1)  # noqa: E731
    cs, gm = (P["cs_x"], P["cs_z"]), (P["cs_x"], P["gm_z"])
    if want(1):   # plain-side axle plate on the rail with its bearing, from inside
        bxw = (-70, 80, -240, -120, -95, 95)
        out.append(bv.joint([
            part("Left rail", W(S("frame"), *bxw), COL["frame"]),
            part("Axle plate, welded to the rail", W(S("axle_plate"), *bxw), COL["plate"]),
            part("25 mm flange bearing", W(S("brg_main_l"), *bxw), COL["brg"]),
            part("M12 bolts, nuts outside", W(S("brg_bolts"), *bxw), COL["fix"]),
            part("Cluster shaft", W(S("shaft"), *bxw), COL["shaft"])],
            OUT / "joint-01.png", "Joint 1: axle plate and main bearing, plain side",
            subtitle="Seen from inside the truck. The plate is welded to the inside of the rail; the bearing bolts to its inside face",
            elev=15, azim=115, size=(8, 6)))
    if want(2):   # chain case opened: inner plate and gearmotor left off, seen from inside
        bxw = (-150, 120, 90, 200, -110, 380)
        out.append(bv.joint([
            part("Case outer plate", W(S("case_outer"), *bxw), COL["outer"]),
            part("Case band", W(S("case_band"), *bxw), COL["band"]),
            part("Main bearing and countershaft bearing", W(S("brg_main_r", "brg_cs_out"), *bxw), COL["brg"]),
            part("20-tooth sprocket on the cluster shaft", W(S("spr_main", "shaft"), *bxw), COL["spr"]),
            part("Countershaft sprockets", W(S("spr_cs", "cs_shaft"), *bxw), "#B45309"),
            part("08B chain (lower) and 06B chain (upper)", W(S("chain1", "chain2"), *bxw), COL["chain"]),
            part("Spacers", W(S("spacers"), *bxw), COL["spacer"]),
            part("Gearmotor sprocket", W(S("spr_gm"), *bxw), COL["gm"])],
            OUT / "joint-02.png", "Joint 2: inside the chain case (inner plate and gearmotor left off)",
            subtitle="Seen from inside the truck. Both chains run between the plates; the band closes the edge all round",
            elev=8, azim=-75, size=(8, 7.5)))
    if want(3):   # gearmotor on the inner plate
        bxw = (-150, 120, -10, 200, 150, 520)
        out.append(bv.joint([
            part("Case inner plate (aluminium)", W(S("case_inner"), *bxw), COL["inner"]),
            part("Case outer plate", W(S("case_outer"), *bxw), COL["outer"]),
            part("Gearbox face on the inner plate", W(S("gearmotor"), *bxw), COL["gm"]),
            part("Three M8 screws in slots", W(S("gm_bolts"), *bxw), COL["fix"]),
            part("Inner countershaft bearing", W(S("brg_cs_in"), *bxw), COL["brg"]),
            part("Spacers", W(S("spacers"), *bxw), COL["spacer"])],
            OUT / "joint-03.png", "Joint 3: worm gearmotor on the chain case inner plate",
            subtitle="Seen from inside the truck and behind. The motor stands up the frame; its output shaft passes into the case",
            elev=10, azim=-140, size=(8, 6.5)))
    if want(4):   # hub, spider and rail, cut through the shaft centre
        bxw = (-120, 120, 150, 300, -60, 60)
        out.append(bv.joint([
            part("Right rail", W(S("frame"), *bxw), COL["frame"]),
            part("Case outer plate", W(S("case_outer"), *bxw), COL["outer"]),
            part("Main bearing", W(S("brg_main_r"), *bxw), COL["brg"]),
            part("Cluster shaft", W(S("shaft"), *bxw), COL["shaft"]),
            part("Weld-on hub, 5 mm clear of the rail", W(S("hub_r"), *bxw), COL["hub"]),
            part("Spider", W(S("spider_r"), *bxw), COL["spider"])],
            OUT / "joint-04.png", "Joint 4: cluster hub on the shaft end (drive side, cut through the shaft)",
            subtitle="Seen from the back. The taper-lock bush clamps the hub to the shaft; the hub clears the rail by 5 mm",
            cut="+X", elev=18, azim=-150, size=(8, 6)))
    if want(5):   # wheel on its stub axle, cut
        a = P["arm"]
        x, z = a * math.cos(math.radians(330)), a * math.sin(math.radians(330))
        bxw = (x - 115, x + 115, 215, 300, z - 55, z + 55)
        out.append(bv.joint([
            part("Spider arm", W(S("spider_r"), *bxw), COL["spider"]),
            part("Stub axle, welded in the spider", W(S("stubs_r"), *bxw), COL["stub"]),
            part("Wheel with two 20 mm bearings", W(S("wheels_r"), *bxw), COL["wheel"]),
            part("Spacer, washer and M10 end screw", W(S("wheel_fix_r"), *bxw), "#D4A017")],
            OUT / "joint-05.png", "Joint 5: wheel on its stub axle (cut through the axle)",
            subtitle="Seen from the back, cut through the axle. The end screw clamps the bearing inner races between washer and spacer",
            cut="+X", elev=8, azim=-172, size=(8, 6)))
    if want(6):   # upright on a cross bar with electronics box and cradle
        bxw = (-70, 70, 60, 200, 470, 760)
        out.append(bv.joint([
            part("Frame: rail and cross bars", W(S("frame"), *bxw), COL["frame"]),
            part("Upright (aluminium flat bar)", W(S("uprights"), *bxw), COL["up"]),
            part("M6 bolt through the cross bar", W(S("up_bolts"), *bxw), COL["fix"]),
            part("Electronics box", W(S("ebox"), *bxw), "#CBD5E1"),
            part("Fuse box and key switch", W(S("switchbox"), *bxw), COL["switch"]),
            part("Pack cradle", W(S("cradle"), *bxw), COL["cradle"])],
            OUT / "joint-06.png", "Joint 6: drive-side upright with the parts it carries",
            subtitle="Seen from the drive side and behind. Each part bolts flat to the upright; the upright bolts to the back of the cross bars",
            elev=14, azim=125, size=(8, 6)))
    if want(7):   # skid standoff on the rail
        bxw = (-120, 70, 170, 230, 90, 190)
        out.append(bv.joint([
            part("Right rail", W(S("frame"), *bxw), COL["frame"]),
            part("Standoff, coped and welded to the rail", W(S("standoffs"), *bxw), COL["standoff"]),
            part("Skid (UHMW)", W(S("skids"), *bxw), "#D6D3D1"),
            part("M5 countersunk screw into the cap", W(S("skid_screws"), *bxw), COL["fix"])],
            OUT / "joint-07.png", "Joint 7: skid on its standoff (drive side, lower standoff)",
            subtitle="Seen from above and behind. The skid face is 100 mm behind the shaft line",
            elev=35, azim=-150, size=(8, 6)))
    if want(8):   # handle pod on the grip
        gz = P["frame_h"] + P["handle_rise"]
        bxw = (-120, 40, -130, 130, gz - 60, gz + 40)
        out.append(bv.joint([
            part("Grip (part of the frame)", W(S("frame"), *bxw), COL["frame"]),
            part("Control pod, clamped round the grip", W(S("controls"), *bxw), COL["controls"]),
            part("Controls lead", W(S("harness"), *bxw), COL["harness"])],
            OUT / "joint-08.png", "Joint 8: handle controls on the grip",
            subtitle="Seen from behind and below. The pod clamps round the grip; the dead-man lever sits behind it",
            elev=-15, azim=-150, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(which=None):
    M = made()
    out = []
    want = lambda n: which is None or str(n) in which  # noqa: E731

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    fr = M["frame"]
    frl = part("Hand truck frame (lower part shown)", S("frame") & bx(-500, 500, -500, 500, -10, Z0 + 560), COL["frame"])
    st(1, [fr], [mv(M["low_bar"], (300, 0, 0))], "replacement lowest cross bar",
       "Wheels, axle and the bar 60 mm above the shaft line removed; new bar welded 105 mm below it",
       elev=15, azim=125, label_done=True)
    st(2, [frl, M["low_bar"]], [mv(M["axle_plate"], (0, 150, 0)), mv(M["outer"], (0, -150, 0))],
       "axle plate and case outer plate onto the rails",
       "Welded to the inside of each rail on a 25 mm alignment bar through both bores",
       elev=30, azim=150, label_done=False)
    base2 = [frl, M["low_bar"], M["axle_plate"], M["outer"]]
    st(3, base2, [mv(M["standoffs"], (-200, 0, 0))], "skid standoffs onto the rails",
       "Four standoffs, coped ends welded to the backs of the rails, 140 and 510 mm above the shaft line",
       elev=15, azim=125, label_done=False)
    base3 = base2 + [M["standoffs"]]
    st(4, base3, [mv(M["brg_main"], (0, 0, -150)), mv(M["brg_cs_out"], (-150, 0, 0))],
       "main bearings and outer countershaft bearing",
       "Bolted to the inside faces of the plates: M12 for the main bearings, M10 in the slots for the countershaft",
       elev=10, azim=-60, label_done=False)
    base4 = base3 + [M["brg_main"], M["brg_cs_out"]]
    inner_spr = part("Inner plate and spacers", S("case_inner", "spacers", "spacer_screws"), COL["inner"])
    st(5, base4, [mv(inner_spr, (0, -200, 0)), mv(M["brg_cs_in"], (0, -380, 0))],
       "case inner plate, spacers and inner countershaft bearing",
       "Two spacers on M8 screws; the inner bearing bolts to the gearbox side of the inner plate",
       elev=10, azim=-60, label_done=False)
    base5 = base4 + [M["inner"], M["brg_cs_in"]]
    st(6, base5, [mv(M["shaft"], (0, -450, 0))], "cluster shaft and 20-tooth sprocket",
       "Slide the shaft in from the plain side; the sprocket goes on it inside the case before it reaches the drive side",
       elev=10, azim=-60, label_done=False)
    base6 = base5 + [M["shaft"]]
    st(7, base6, [mv(M["cs"], (0, -300, 0))], "countershaft and its sprockets",
       "Slide in from inside the truck through the inner bearing, the sprockets and into the outer bearing",
       elev=10, azim=-60, label_done=False)
    base7 = base6 + [M["cs"]]
    st(8, base7, [mv(M["gm"], (0, -250, 0))], "worm gearmotor",
       "Gearbox face on the inner plate, three M8 screws in the slots; sprocket on its output shaft inside the case",
       elev=10, azim=-135, label_done=False)
    base8 = base7 + [M["gm"]]
    st(9, base8, [mv(M["chains"], (-250, 0, 0))], "chains on, then tension them",
       "Final stage first by sliding the countershaft bearings, then the first stage by sliding the gearmotor",
       elev=10, azim=-60, label_done=False)
    base9 = base8 + [M["chains"]]
    st(10, base9, [mv(M["band"], (-250, 0, 0))], "close the chain case with the band",
       "Band between the plates, flush with their edges, M4 screws through the tabs into both plates",
       elev=12, azim=125, label_done=False)
    base10 = base9 + [M["band"]]
    spl = part("Plain-side spider", S("spider_l", "hub_l", "stubs_l"), COL["spider"])
    spr = part("Drive-side spider", S("spider_r", "hub_r", "stubs_r"), COL["spider"])
    st(11, base10, [mv(spl, (0, -280, 0)), mv(spr, (0, 280, 0))], "spiders onto the shaft ends",
       "Hub on the shaft end, key in, taper-lock bush tightened; outer face flush with the shaft end",
       elev=12, azim=125, label_done=False)
    base11 = base10 + [M["spiders"]]
    wl = part("Wheels and fixings, plain side", S("wheels_l", "wheel_fix_l"), COL["wheel"])
    wr = part("Wheels and fixings, drive side", S("wheels_r", "wheel_fix_r"), COL["wheel"])
    st(12, base11, [mv(wl, (0, -250, 0)), mv(wr, (0, 250, 0))], "wheels onto the stub axles",
       "Spacer, wheel, 36 mm washer and M10 end screw on each stub axle; the wheel must spin freely",
       elev=12, azim=125, label_done=False)
    base12 = [fr] + base11[1:] + [M["wheels"]]
    st(13, base12, [mv(M["uprights"], (-300, 0, 0))], "component uprights onto the cross bars",
       "Two uprights on the back of the three upper cross bars, M6 bolts through each bar",
       elev=12, azim=125, label_done=False)
    base13 = base12 + [M["uprights"]]
    st(14, base13, [mv(M["ebox"], (-250, 0, 0)), mv(M["switch"], (-250, 0, 0)), mv(M["pack"], (-350, 0, 0))],
       "electronics box, fuse box and pack cradle",
       "Each bolted flat to both uprights (the fuse box to the drive-side upright); the pack stays out",
       elev=12, azim=125, label_done=False)
    base14 = base13 + [M["ebox"], M["switch"], M["pack"]]
    st(15, base14, [mv(M["harness"], (-150, 0, 0)), mv(M["controls"], (-150, 0, 100))],
       "harness and handle controls",
       "Pod clamped round the grip; cables tied to the uprights and the drive-side handle tube",
       elev=12, azim=125, label_done=False)
    base15 = base14 + [M["harness"], M["controls"]]
    st(16, base15, [mv(M["skids"], (-200, 0, 0)), mv(M["strap"], (250, 0, 0))],
       "skids and load strap",
       "Skids screwed to the standoff caps; strap hooks round the rails, ratchet on the load side",
       elev=12, azim=125, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "StepClimber prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw "
            "terminal; crimped, keyed connectors at the pack and the motor.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/stepclimber", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    ax.add_patch(FancyBboxPatch((50, 14), 50, 44, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(51.5, 56.8, "Inside the electronics box (IP54)", fontsize=8, color=MUT, va="top")
    blk(3, 40, 16, 13, "Battery pack", "24 V LiFePO4, 8S 10 Ah,\nBMS, keyed plug", "#C2410C")
    blk(26, 40, 17, 13, "Fuse box", "40 A fuse, then\nkey switch", "#7C3AED")
    blk(56, 40, 18, 13, "Motor driver", "24 V 30 A H-bridge,\ncurrent sense", "#16A34A")
    blk(80, 36, 17, 17, "Controller", "microcontroller,\n6-axis IMU,\nbuzzer", "#0F766E")
    blk(56, 18, 18, 12, "5 V converter", "24 V to 5 V,\n1 A, fused 2 A", "#16A34A")
    blk(103, 40, 15, 13, "Gearmotor", "24 V motor\nand brake coil", "#0F766E")
    blk(103, 14, 15, 15, "Handle pod", "dead-man lever,\nup and down switch,\nlight bar", "#2563EB")
    blk(3, 14, 16, 12, "Charge port", "on the pack;\n29.2 V 3 A charger", "#C2410C")
    wire([(19, 47), (26, 47)], RED); lab(22.5, 49.5, "2.5 mm²", RED, "center")
    wire([(43, 47), (56, 47)], RED); lab(49.5, 49.5, "2.5 mm²", RED, "center")
    wire([(74, 45), (103, 45)], RED); lab(88.5, 32.5, "motor 2.5 mm²", RED, "center")
    wire([(88.5, 34), (88.5, 45)], RED, 0.01)
    wire([(74, 50), (103, 50)], GRY, 1.2); lab(97, 52, "brake 0.5 mm²", GRY, "center")
    wire([(65, 40), (65, 30)], RED, 1.4); lab(65.6, 35, "0.75 mm²", RED)
    wire([(74, 24), (88.5, 24), (88.5, 36)], RED, 1.4); lab(81, 26, "5 V, 0.5 mm²", RED, "center")
    wire([(80, 42), (74, 42)], BLU, 1.2); lab(77, 39.5, "PWM, dir", BLU, "center")
    wire([(97, 40), (100, 40), (100, 22), (103, 22)], BLU, 1.2); lab(95.5, 30, "pod lead,\n0.25 mm²", BLU, "right")
    wire([(11, 26), (11, 40)], RED, 1.4); lab(11.6, 33, "charge lead", RED)
    ax.text(3, 9.6, "Safety: pack unplugged until the stop points in section 6 of the plan are passed. Releasing the dead-man lever cuts the "
            "drive and the brake coil, so the brake applies.", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 6.2, "Red: power. Blue: signal. Grey: brake coil. All circuits are extra-low voltage (29.2 V at most while charging). "
            "The brake is spring-applied: no power, brake on.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    i = 0
    while i < len(args):
        w = args[i]; sel = None
        if i + 1 < len(args) and args[i + 1].isdigit():
            sel = [args[i + 1]]; i += 1
        r = fns[w](sel) if sel and w in ("sheets", "joints", "steps") else fns[w]()
        print(w, sel or "", "->", r)
        i += 1

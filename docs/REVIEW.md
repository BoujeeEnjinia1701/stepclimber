# Review note: StepClimber

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (SCM-PRB-001 v0.2): problem with cited injury data (US emergency department data for couriers, NIOSH-funded courier study, NIOSH lifting equation), market gap between about $100 manual tri-star trucks and about $4,400 powered climbers, users, operating environment (IRC stair limits), constraints, out of scope, cited prior work, open questions and a user research checklist.
- `docs/03-requirements.md` (SCM-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with a design load case, a status column against the estimates, and an explicit list of requirements not met or at risk.
- `docs/02-concept.md` (SCM-PRC-001 v0.2): how it works, numbered components, cluster geometry, drive torque and power, energy and endurance, balance and handle force, mass, cost, key design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of the tilted hand truck with 11 BOM-numbered parts; a residential stair and a parcel carton as hero-only context; 1.75 m scale figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with callouts 1 to 11, `flow.png` (energy per loaded step, estimates), `model.glb` and `viewer.html`. No cutaway: the drive train is shown clearly in the exploded view, and a section adds little at this stage.
- `bom/bom.csv` (13 lines, indicative USD, items 1 to 11 match the exploded view) and `bom/bom-notes.md` (cost roll-up).
- `README.md`: hero image and links line before "## Problem"; concept paragraph, key components and safety note updated to match the precis.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Design load case | 60 kg payload plus 24.3 kg truck, 84 kg total; 196 mm risers, 254 mm treads | R1 |
| Lift work per step | about 162 J | |
| Peak shaft torque | about 145 N·m | |
| Peak motor output at 20 steps/min | about 236 W on a 250 W motor | R3 met, thin margin |
| Pack energy per loaded step up | about 500 J (0.14 Wh); the self-locking worm loses about 208 J | |
| Loaded steps per charge, up and down (256 Wh LiFePO4) | about 1,300 | R4 met |
| Handle force at the plus or minus 8 degree tilt window edge | about 91 N | R6 met |
| Push force on the flat | about 25 N | R10 met |
| Truck mass | about 24.3 kg | R5 met, thin margin |
| Width; upright height | about 570 mm; about 1,460 mm | Width met; **R11 height not met** |
| Parts cost | about $580 including charger | R12 met, about 3 % margin |

Requirements not met or at risk:

- **R11 (upright height 1,300 mm or less) not met:** about 1,460 mm, because the handle must sit about 1,230 mm above the floor when tilted for climbing.
- **R2 (stair range) at risk:** the fixed 234 mm wheel spacing lands the wheel only about 16 mm onto the tread at a 220 mm riser, so steep old or service stairs are not covered.
- **R3, R5 and R12 have thin margins** of a few percent.
- **R6 to R9** rely on tilt control, brake and hold-to-run behavior that exists only as a concept.

### Proposed, awaiting Amish

1. **Meaning of the pitch's tilt sensor (pitch-level).** The truck cannot hold its own angle; only the courier's hands and the clusters touch it. Option A: operator-in-the-loop tilt control (speed shaping, tilt window, stop and alert). Option B: an actuator that tilts the load platform, about $60 to $90 and 2 kg more, which breaks R5 and R12. Recommendation: A, and reword the pitch to "a tilt sensor that helps the courier hold the load angle steady". The `project.yaml` pitch and problem are unchanged; the numbers found support the problem statement as written.
2. **Handle height (R11).** Option A: fixed handle, relax R11 to about 1,500 mm. Option B: telescoping handle (about $25, 0.8 kg; pushes R5 and R12 to their limits). Option C: folding handle hinge, studied at TRL 3. Recommendation: A for the first prototype, C at TRL 3.
3. **Rated stair load of 60 kg** rather than 40 or 80 kg, until couriers are asked.
4. **Tri-star clusters** rather than a stepping arm or tracks (as the pitch states).
5. **Self-locking worm plus spring-applied brake** rather than an efficient gearbox with a brake alone (about twice the endurance but one hold).
6. **24 V LiFePO4 pack rather than the 48 V SwapCell pack.** SwapCell (about $370) would take more than half the $600 budget and needs a CAN host adapter. Recommendation: stay at 24 V.
7. **First user group** for interviews: gig couriers, a parcel company pilot or appliance and moving crews.

The budget is within `budget_usd` ($600); no budget change is proposed.

### Safety concerns

- Runaway or tip-over of an 84 kg load on a stair with the operator uphill of it: two independent holds, hold-to-run, tilt window and a rated load label are required; nobody below the truck on a stair.
- Operator falls while walking backwards up a stair.
- Pinch and entanglement at the rotating clusters (up to about 145 N·m) and the chain drive near the feet: full guarding.
- 256 Wh LiFePO4 pack: BMS, fuse, safe charging, low-temperature charge block.
- Unsecured parcels sliding as the frame pitches: the strap is mandatory.

### Problems and notes

- The kit hero note names only the 1.75 m person; the stair and carton in the hero are identified in the precis caption (Figure 1).
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- Some published sources (PubMed Central, Wiley) blocked automated fetching; figures were taken from the accessible abstract on ScienceDirect and the CDC Stacks record.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the cluster geometry against a stair survey, the drive torque and brake holding margin, frame pitch and handle force through a step, and structural stresses, and to produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish approved all TRL 2 recommendations on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them.") This session took StepClimber to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (SCM-DDR-001 v0.1): eight decided items, two open items and three new proposals.
- `docs/04-calcs/01-sizing.md` (SCM-CAL-001 v0.1) and `docs/04-calcs/sizing.py`, which prints every quoted number and writes `docs/04-calcs/results.csv`. It includes a 2D climb simulation that checks the hub, arms and wheels against stair nosings.
- `cad/src/model.py`: parametric build123d model (clusters, frame, shaft and chain drive, gearmotor, driver, controller, pack, harness, handle, skids, strap) with an upright pose and a `tilted()` climbing pose. It exports `cad/step/` and `cad/stl/` files for the assembly, cluster pair, frame and drive.
- `cad/src/sheets.py` produces `cad/drawings/SCM-DWG-001.svg`, `.pdf` and `.png`: general arrangement at Rev P1, marked "CONCEPT, NOT FOR FABRICATION", with third-angle views, a climbing-pose view and key dimensions. The concept blueprint keeps its number, SCM-DWG-010.
- `bom/bom.csv`: all 13 lines priced, supplier types named, notes tied to the calculations; `bom/bom-notes.md` gives the $580 total against $600.
- `cad/src/concept_media.py` now builds from the model. `media/` was regenerated (hero, blueprint, exploded, flow, GLB and viewer) and every image checked; the temporary `_views` folders were deleted.
- SCM-PRB-001, SCM-PRC-001 and SCM-REQ-001 moved to v0.3 with the decisions and the calculated figures. `project.yaml` is at `trl: 3`, `trl_target: 3` with the new evidence, and `README.md` has the reworded pitch.

### Requirements (SCM-CAL-001): 8 met, 3 not met, 4 not verifiable at TRL 3

| ID | Status | Value |
| --- | --- | --- |
| **R2** stair range | **Not met** | Climbs risers to 209 mm and fits 250 mm treads, but the straight arms clear nosing overhangs only up to 23 mm (32 mm required) |
| **R6** grip force | **Not met** | 107 N at the plus or minus 8 degree window edge (100 N limit); 54 N at the set angle |
| **R15** stair protection | **Not met** | Nosings pass within 58 mm of the shaft line; the 60-tooth sprocket guard reaches 104 mm, so it strikes by about 46 mm |
| R1 load | Met | Safety factors 2.0 shaft, 1.8 spider, 2.9 rail at 3 g |
| R3 speed | Met, 4 % margin | 239 W peak on a 250 W motor |
| R4 endurance | Met | 1,394 loaded steps up and down per charge |
| R5 mass | Met, 0.7 kg margin | 24.3 kg |
| R10 flat push | Met | 25 N |
| R11 size | Met | 569 mm wide, 1,418 mm tall (relaxed target 1,500 mm) |
| R12 cost | Met, 3.3 % margin | $580 |
| R13 battery | Met | 3.5 h charge |
| R7, R8, R9, R14 | Not verifiable at TRL 3 | Worm statically self-locking (back-drive efficiency -0.22), brake margin 8.0 times; drift, stop time and IP rating need hardware |

TRL 2 figures corrected: endurance 1,300 to 1,394 steps; energy per step down 60 to 42 J; grip force 91 to 107 N (the support point moves during a step); landing at a 220 mm riser 16 to 4 mm; upright height 1,460 to 1,418 mm; charge 3.2 to 3.5 h.

### Decisions recorded (SCM-DDR-001, decided by Amish, 2026-09-25: go with recommendation)

1. Tilt sensor as operator-in-the-loop control; pitch reworded to "a tilt sensor that helps the courier hold the load angle steady" (`project.yaml`, `README.md`). The problem line is unchanged.
2. Fixed handle for the first prototype; R11 relaxed to 1,500 mm. The folding hinge (Option C) was studied: it folds to 1,106 mm for about 0.4 kg and $20 more, and was not adopted.
3. Rated stair load 60 kg.
4. Tri-star clusters.
5. Self-locking worm plus spring-applied brake.
6. 24 V LiFePO4, not SwapCell. The SwapCell interface v0.3 items and the shared-pack pricing rule do not apply.
7. Courier always uphill of the truck.
8. Budget kept at $600.

### Still awaiting Amish

- First user group (no recommendation was made).
- Partner courier group or co-design partner (to be chosen per area later).
- **New: cluster and drive rework for R2 and R15.** Recommendation: 150 mm arms, 200 mm wheels and a two-stage chain drive with an 08B 20-tooth final sprocket (54 mm envelope; chain safety factor 4.4). This raises the peak torque to 163 N·m (266 W at 20 steps/min, or 18.8 steps/min on the present motor) and roughly adds 1.5 kg and $35, so R5 and R12 would likely be exceeded. The model and BOM stay at the baseline until Amish decides.
- **New: tilt window.** Recommendation: tighten from plus or minus 8 to plus or minus 6 degrees so the grip force stays under 100 N (plus or minus 6.8 degrees is the limit).
- **New: follow-on targets** (R3, R5, R12) if the rework goes ahead.

### Safety concerns

- The nosing strike is a safety issue as well as a stair-damage issue: a guard catching a nosing mid-step could jerk the frame toward the courier or stall the climb with the load half-lifted. No loaded climb should be tried on the baseline drive.
- Runaway and tip-over with the courier uphill: the holding figures are static; worm creep under vibration and the real brake torque are unverified.
- Grip force at the window edge (107 N) is above the target; a tired courier may not hold the angle on a long flight.
- Pinch and entanglement at the clusters (146 N·m peak) and the chain; 256 Wh LiFePO4 pack handling and charging; unsecured parcels.

### Problems and notes

- No TRL 4 material exists in the repo; `build-log/README.md` is the original scaffold and was left untouched. No test plans, build procedures, firmware or PCB files were created.
- The review listed no unchecked citations; the earlier note about PubMed Central and Wiley blocking automated fetching stands. No new sources were added.
- The build123d STEP writer refuses a shape already written to another file, so `model.py` builds each export afresh.
- The chain strengths (ISO 606 minimums) and the brake torque are typical catalog values, to be confirmed with suppliers.

### Recommended next step

TRL 4 is on hold by Amish's instruction. The next step is for Amish to decide the cluster and drive rework and the tilt window (SCM-DDR-001 items 11 to 13), after which the TRL 3 model, calculations, drawing and BOM would be revised in place at TRL 3. For the record only, TRL 4 would later need: a bench test article of one cluster and drive on a mock stair (landing, nosing clearance, torque and current), a hold test of the worm and brake under vibration (R8), a tilt control and hold-to-run bench test (R7, R9), a grip force measurement (R6), a test report (TST) with `environment: lab`, and build log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open StepClimber item that carried a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (SCM-DDR-002 v0.1). SCM-DDR-001 moved to v0.2 with the new statuses. TRL stays at 3.

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| 11 | Cluster and drive rework (Option A) | 135 mm arms, 150 mm wheels, one 06B stage 10T to 60T (6:1) | 150 mm arms, 200 mm wheels, 06B 10T to 35T then 08B 10T to 20T (7:1) through a countershaft 150 mm up the frame |
| 11 | Shaft-line guard against nosings (R15) | 104 mm radius against 48 mm allowed | 53.9 mm against 54.2 mm allowed (32 mm overhang); countershaft guard clears by 96 mm |
| 11 | Nosing overhang the arms clear (R2) | 23 mm | 32 mm |
| 12 | Tilt window (R7) | Plus or minus 8 degrees | Plus or minus 6 degrees |
| 13 | R3 climb speed | 20 steps/min | 17 steps/min on the same 250 W motor (238 W peak) |
| 13 | R5 truck mass | 25 kg (truck 24.3 kg) | 27 kg (truck 26.3 kg) |
| 13 | R12 and `budget_usd` | $600 (BOM $580) | $650 (BOM $633) |

Files changed: `cad/src/model.py` (parameters and drive geometry; STEP and STL re-exported), `cad/src/sheets.py` (SCM-DWG-001 Rev P1 to P2), `cad/src/concept_media.py` (key figures and energy flow; `media/` regenerated and checked), `docs/04-calcs/sizing.py` and `results.csv`, SCM-CAL-001 v0.1 to v0.2, SCM-REQ-001 v0.3 to v0.4, SCM-PRC-001 v0.3 to v0.4, SCM-PRB-001 v0.3 to v0.4, `bom/bom.csv` (items 2 to 4), `bom/bom-notes.md`, `project.yaml` (`budget_usd` 650, DDR-002 added to the evidence) and `README.md`.

Other figures that moved: endurance 1,394 to 1,327 loaded steps per charge; pack energy per step up 499 to 527 J; peak shaft torque 146 to 166 N·m; gearmotor output 25.7 to 25.8 N·m; safety factors shaft 2.0 to 1.8, spider 1.8 to 1.7, rail 2.9 to 2.8; upright height 1,418 to 1,451 mm; brake margin 8.0 to 8.2 times.

### Requirement status (SCM-CAL-001 v0.2): 10 met, 1 not met, 4 not verifiable at TRL 3

| ID | Status | Value |
| --- | --- | --- |
| **R6** grip force | **Not met** | 111 N at the plus or minus 6 degree window edge (100 N limit); 70 N at the set angle |
| R1, R4, R10, R11, R13 | Met | Safety factors 1.7 or more; 1,327 steps; 25 N; 569 x 1,451 mm; 3.5 h charge |
| R2 stair range | Met | Climbs to 225 mm risers, needs 240 mm treads, clears 32 mm overhangs |
| R3 speed | Met, 5 % margin | 238 W at 17 steps/min |
| R5 mass | Met, 0.7 kg margin | 26.3 kg |
| R12 cost | Met, 2.6 % margin | $633 |
| R15 stair protection | Met, no spare radius | Guard 53.9 mm against 54.2 mm |
| R7, R8, R9, R14 | Not verifiable at TRL 3 | Need hardware |

### Still awaiting Amish

- Item 9: first user group (no recommendation was made).
- Item 10: partner courier group or co-design partner (to be chosen per area later).
- **New item 14: grip force after the rework (R6).** The longer arm widens the load's swing about its support wheel (plus or minus 71 to 89 mm), so the plus or minus 6 degree window gives 111 N rather than the 99 N it gave on the old cluster. Recommendation: keep plus or minus 6 degrees and relax R6 to 115 N until grip force is measured at TRL 4; alternatives are a plus or minus 4 degree window (4.4 degrees meets 100 N) or a longer handle.

### Cross-repo actions

None. StepClimber keeps its own 24 V pack, so no SwapCell or other repo change follows from these decisions.

### Other changes this session

- `README.md` gained the sections "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea". The inspiration point is Eshcol S. Gross's manual lever-and-ratchet stair climbing dolly with three-armed wheel groups (US 3,515,401, 1970).
- All documents, drawings and media were regenerated so the footers read designmolecule.com; older PDFs in `docs/pdf/` were removed.

### Safety concerns

- The shaft-line guard is sized exactly to its nosing envelope; a bent guard or a stair outside the R2 range could still strike a nosing mid-step.
- The grip force at the window edge (111 N) is above target; a tired courier may not hold the angle on a long flight.
- Runaway and tip-over with the courier uphill, worm creep under vibration, pinch points at the clusters (166 N·m peak) and two chain stages, and the 256 Wh pack remain as in the TRL 3 session.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No test articles, test plans, build procedures, firmware or PCB files were created.

### Recommended next step

Amish decides item 14 (R6); the TRL 3 package is otherwise complete.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; it changes no dimension, interface, requirement, calculation or BOM line.

### What was done

- `cad/src/product_model.py`: `product_parts()` returns 88 named parts (50 in the "shell" group, 32 in the drive train group "internal" and 6 context parts) with colour, material, BOM line, group and exploded-view offset, built from `PARAMS`, `derived()` and the geometry of `model.py`. Frame-mounted parts are tilted back 30 degrees about the cluster shaft, as `model.tilted()` does; the clusters stay put against the first riser, as in `concept_media.py`. It adds:
  - powder-coated frame with welded rail bends, toe plate gussets, anti-slip ribs and rounded toe plate corners;
  - teal laser-cut tri-star spiders with lightening slots, cast hub bosses with six hub bolts and shaft end caps, grooved solid rubber tyres on light grey rims, axle caps and flange bearings with bolts;
  - a closed chain case round both chain stages with a clear inspection window over the final stage chain, and the sprockets, chains and countershaft inside it;
  - the worm gearmotor with a ribbed gearbox, brake housing, teal brake-release lever, rating label and cable gland;
  - the IP54 electronics box with a lid frame, driver-side cooling ribs, lid screws, a name plate and a clear window over the controller and IMU board (a lit heartbeat light), and the motor driver board with its heat sink inside;
  - the battery pack with a parting line, a teal release latch, a state-of-charge light bar (three segments lit), a charge port cap, a rating label and a raised wordmark, in its cradle;
  - key switch and 40 A fuse holder, cables and cable glands;
  - ribbed rubber grip sleeves, the dead-man lever and a control pod with an up and down rocker, a lit status light bar and a buzzer grille;
  - UHMW nosing skids with screws, and the load strap with its ratchet round three parcel cartons.
- Context (group "context"): a four-step stair on the design stair (196 mm risers, 254 mm oak treads with 20 mm nosings), three strapped parcel cartons on the toe plate, and the shared clay mannequin (1.75 m, "push" pose with joint overrides) standing two steps up with both hands on the grip. The hands are placed from `mannequin_landmarks()`, so they stay on the grip if the handle moves.
- `TITLE` and `RENDER_VIEWS`: "hero" (front right, about 16 degrees elevation, with the stair and courier), "exploded" (front left, about 24 degrees, seen from the stair side so the pack, electronics box and gearmotor faces show) and "detail" (front left, about 14 degrees). The "internal" group holds the drive train (clusters, shaft, bearings, chain case and chains, gearmotor and its mounts), so the detail view frames the tri-star clusters and drive on their own.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files are produced later by the orchestrator.
- Self-check previews (matplotlib, clear parts left out) were reviewed in `/tmp/stepclimber-prod/`.

### Where the appearance model differs from model.py

Each item is **Proposed, awaiting Amish**.

1. **Component mounts added.** `model.py` shows the gearmotor, electronics box and pack floating behind the rails. The appearance model adds a 3 mm component mounting panel behind the rails, a gearmotor bracket tied to the second cross bar, a sheet steel pack cradle and four enclosure standoffs. As drawn in steel they would weigh roughly 8 kg, far beyond the 0.7 kg margin on R5 (27 kg). Recommendation: treat them as illustrative only; at the next CAD revision replace them with light brackets (two flat-bar uprights or 2 mm aluminium) and carry their mass in SCM-CAL-001.
2. **Chain case closed.** `model.py` models the guards as sprocket rings plus flat plates. The appearance model closes them into one stadium-shaped case on the same planes and radii (53.9 mm on the shaft line), caps the first stage at the gearmotor sprocket with the same 65.8 mm radius and adds a clear window in the back plate. Recommendation: adopt the closed case, since it also answers the pinch hazard; the window does not change the guard radius or R15.
3. **Spider outline.** The rectangular arms become a rounded tri-star profile with the same 45 mm arm width and 150 mm arm length, a 46 mm hub disk, 6 mm fillets and rounded arm ends round each wheel axle. Recommendation: keep it, but check the hub disk and fillets against the 54.2 mm nosing envelope in SCM-CAL-001 before any drawing is updated.
4. **Load strap.** `model.py` shows the strap as a flat bar across the rails at 700 mm above the shaft; the appearance model keeps that height and anchors it on the rails but wraps it round the load, with a ratchet. Recommendation: adopt for renders; no calculation depends on it.
5. **Minor.** The motor can and brake share the 150 mm motor length (brake housing 1 mm larger in radius); the flange bearings are drawn 14 mm thick on the outer face of the axle plates instead of 16 mm overlapping them; the handle cable is routed on to the control pod; the toe plate has rounded front corners, ribs and gussets; the nosing skids are shown in black UHMW. Recommendation: accept as appearance only.

### Scope and TRL

This is an appearance model only: no tolerances, fabrication detail, PCB layouts or firmware. `trl` stays 3 in `project.yaml`, and TRL 4 remains on hold by Amish's instruction.

### Recommended next step

Amish reviews the orchestrator's renders and decides items 1 to 4 above, together with the open item 14 (R6 grip force).

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

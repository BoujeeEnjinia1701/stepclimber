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

## Session 2026-10-01: constructable design and prototype build plan (kit 1.7.0)

Amish approved the build plan format on 2026-09-30 and asked for it in every repo, with outstanding decisions kept in a separate design decisions register; on 2026-09-30 he also wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." This session installed kit 1.7.0, made StepClimber constructable under that instruction and wrote the illustrated build plan. TRL stays at 3.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` copied from `.kit/CLAUDE.md`.
- `cad/src/model.py` rebuilt as a component model (`build_components()`, 40 components) with 90 build123d constructability checks (`python cad/src/model.py --check`), all passing, including the clusters turned through a third of a turn against every frame part. `build()` and `tilted()` keep the concept-media grouping. STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (SCM-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/04-calcs/sizing.py` and `01-sizing.md` (SCM-CAL-001 v0.3): itemised mass, chain centres for whole chains, shaft overhang from the new bearing positions, and a new check of every frame-fixed outline near the shaft against every stair nosing; `results.csv` rewritten.
- `bom/bom.csv`: lines 1 to 3 and 13 respecified and repriced; lines 14 to 17 added (axle plates and chain case, component uprights, frame modification steel, fixings).
- `cad/src/build_plan_media.py`: overview, making sketches SCM-DWG-101 to 109, a hole layout of the three plates, 8 joint close-ups, 16 assembly step pictures and a block wiring diagram (`docs/05-build-plan/`, `cad/drawings/`).
- `docs/05-build-plan.md` (SCM-BLD-001 v0.1) and `docs/06-design-decisions.md` (SCM-DEC-001 v0.1).
- SCM-DWG-001 general arrangement moved to Rev P4; concept media regenerated from the new model.
- `cad/src/svg_fix.py`: a local workaround, imported by `sheets.py` and `concept_media.py`, for a build123d SVG export failure on the climbing-pose projection (a full ellipse not flagged as closed made svgpathtools stop with an AssertionError). Such an ellipse is drawn as a fine polyline. Reported as a kit issue; `.kit/` is unchanged.
- `docs/pdf/` regenerated for all nine controlled documents; `python .kit/drawing.py --check-text` finds no text overlaps on any sheet or the concept blueprint.
- SCM-REQ-001 v0.5 and SCM-PRC-001 v0.5 updated; `project.yaml` gains `design_state: constructable` and the three new documents in `trl_evidence`; README links line and a "Building the prototype" section.

### Design changes made for construction (SCM-DDR-003)

1. Bearings moved inside the rails onto two welded axle plates (plain side 4 mm steel; drive side the 3 mm steel outer plate of the chain case); shaft overhang 48 to 93 mm.
2. Countershaft carried in two 20 mm flange bearings, one on each chain case plate, in slots for chain tension.
3. Closed chain case (outer plate, 3 mm aluminium inner plate on two spacers, 1.5 mm aluminium band) in place of the loose guards, with the same radii on the shaft line (53.9 mm) and round the countershaft (65.8 mm).
4. Lowest cross bar (60 mm above the shaft line, through the chain) cut off and replaced 105 mm below the shaft line.
5. Countershaft and gearmotor output moved 15 mm toward the stair so nothing stands in front of the rails.
6. Chain centres set for whole chains: 38 links of 08B (countershaft 143.9 mm up), 54 links of 06B (gearmotor 289 mm up).
7. Worm gearmotor redrawn with the motor at right angles, standing up the frame; gearbox face bolted to the case inner plate.
8. Spiders carry 1610 weld-on taper-lock hubs and welded 20 mm stub axles; wheels on two bearings with spacer, washer and M10 end screw; 96 mm spider centre disc.
9. Two aluminium component uprights bolted through the cross bars carry the electronics box (raised 30 mm to clear the motor), fuse box and pack cradle.
10. Skids shortened to the 500 mm in the BOM, moved to 200 mm off centre on four welded square-tube standoffs; face still 100 mm behind the shaft line.
11. Handle pod clamped to the grip, strap hooked round the rails, harness routed connector to connector.

### Key results (SCM-CAL-001 v0.3)

| Quantity | Value | Requirement |
| --- | --- | --- |
| Truck mass | 34.2 kg (was 26.3 kg): drive itemised at 5.5 kg (was a 2.5 kg allowance); parts added 3.9 kg plus 0.5 kg of fixings | **R5 not met** (27 kg) |
| Peak motor output at 17 steps/min | 260 W on a 250 W motor; 16.3 steps/min on that motor | **R3 not met** |
| Grip force at the plus or minus 6 degree window edge | 121 N | **R6 not met** (100 N) |
| Loaded steps per charge | 1,215 | R4 met |
| Safety factors at 3 g | Shaft 1.4 (was 1.8), spider 1.5, rail 2.6 | R1 met |
| Width over the wheel end screws; height | 588 mm; 1,451 mm | R11 met |
| Nearest nosing to any frame-fixed outline | 10.3 mm (chain case) against 10 mm wanted | R15 met, no spare |
| Cost | Value-engineering target: USD 650. Estimated cost of the constructable design: USD 776 (USD 126 over the target) | R12 against target |

Requirement status: 7 met on paper, 3 not met (R3, R5, R6), 4 not verifiable at TRL 3, R12 reported against the value-engineering target.

### Proposed, awaiting Amish

All open decisions are in `docs/06-design-decisions.md`: review of the SCM-DDR-003 changes; R5 (recommend 35 kg for the first prototype, try the savings when buying); R3 (recommend 16 steps/min for the first prototype); R6 (recommend 125 N until measured); bringing the appearance model and renders to the constructable design; first user group; partner courier group.

### Stale media (to regenerate on Amish's Mac)

The design changed visibly (chain case, bearings, uprights, skid standoffs, hubs and motor), so `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` (which still builds the concept mounts) are stale. They were not regenerated here.

### Safety concerns

- The chain case sits at the edge of its nosing envelope (10.3 mm against 10 mm); a bent case or a stair outside the R2 range could be struck.
- The shaft safety factor falls to 1.4 at 3 g with the bearings inside the frame; fatigue of the keyed shaft and the welded frame is still not assessed.
- The heavier truck raises the grip force to 121 N at the window edge.
- Runaway and tip-over with the courier uphill, worm creep, pinch points (now enclosed in the chain case) and the 256 Wh pack remain as before; the build plan carries welding and pack safety stops.

### Recommended next step

Amish reviews SCM-DDR-003 and decides register items 1 to 4; then update the appearance model and renders on the Mac. TRL 4 remains on hold.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved every recommendation written for the open decisions: "i approve your recommendations for all 555 open decisions." trl stays 3; nothing was built or tested.

### Decisions recorded

7 decisions recorded in the design decisions register (SCM-DEC-001, Decisions made, dated 2026-10-02): SCM-DDR-003 accepted with one exception, the cluster shaft in 4140 instead of 1018 (1); R5 35 kg for the first prototype (2); R3 16 steps/min for the first prototype (3); tilt window plus or minus 3 degrees for the first loaded trials, R6 kept at 100 N (4), which replaces the record's earlier recommendation to relax R6; appearance model and renders to the constructable design (5); first user group, parcel couriers serving walk-up buildings, then gig couriers (6); a regional parcel or last-mile company for a small supervised pilot (7), the first candidate type to approach and not an agreed partner.

### Documents changed

- `docs/06-design-decisions.md` (SCM-DEC-001 v0.2): all 7 open items moved to Decisions made; Open decisions now reads "None"; item 8 of "To confirm when parts are bought" updated and the 4140 shaft added as item 9.
- `docs/decisions/0003-design-for-construction.md` (SCM-DDR-003 v0.2): acceptance with the 4140 shaft exception; A1 and A2 accepted, A3 decided as the tighter window; status stays Draft.
- `docs/decisions/0002-recommendations-accepted.md` (SCM-DDR-002 v0.2): items 9, 10 and 14 recorded as decided.
- `docs/decisions/0001-trl2-review-decisions.md` (SCM-DDR-001 v0.3): items 9 and 10 recorded as decided, including the co-design partner note.
- `docs/01-problem.md` (SCM-PRB-001 v0.5): first user group and pilot partner type; mass constraint for the first prototype.
- `docs/03-requirements.md` (SCM-REQ-001 v0.6): R3 set to 16 steps/min and R5 to 35 kg for the first prototype; R7 window plus or minus 3 degrees for the first loaded trials; R3, R5 and R6 now met on paper.
- `docs/04-calcs/01-sizing.md` (SCM-CAL-001 v0.4): R3, R5, R6 and R7 rows of Table 10, the summary and the R3, R5 and R6 text follow the 2026-10-02 decisions; no computed number changed.
- `docs/02-concept.md` (SCM-PRC-001 v0.6): R3, R5 and R6 met after the decisions; plus or minus 3 degree window; 4140 shaft; user group and pilot partner; open questions answered.
- `docs/05-build-plan.md` (SCM-BLD-001 v0.2): cluster shaft in 4140 (section 3.6); first checks at 16 steps/min and a 3 degree tilt stop.
- `README.md`: climb speed, tilt window and requirement sentence; the register sentence.
- `bom/bom-notes.md`: 4140 cluster shaft noted; the BOM change is a follow-up.
- PDFs re-rendered with `python .kit/render.py`; superseded versions removed.

No CAD model, BOM quantity or price, or picture was changed. Requirement status after the decisions: ten met on paper (R3, R5 and R6 now met as set for the first prototype), four not verifiable at TRL 3 (R7, R8, R9, R14), R12 USD 126 over the value-engineering target.

### Follow-up actions to carry approved decisions into the design

1. Decision 1 (bom): Change BOM line 3 to a 25 mm keyed cluster shaft in quenched and tempered alloy steel such as 4140, and reprice it.
2. Decision 1 (drawings): Update the shaft material on the making sketch SCM-DWG-106 and in `cad/src/model.py` (material and mass), and regenerate the drawing.
3. Decision 1 (calcs): Recalculate the cluster shaft in SCM-CAL-001 for 4140 (yield and the 1.4 factor at 3 g) and add a fatigue assessment before any loaded stair trial.
4. Decision 2 (calcs): Rerun `docs/04-calcs/sizing.py` with R5 at 35 kg, R3 at 16 steps/min (3.75 s per third of a turn) and the plus or minus 3 degree window, so `results.csv`, the inputs table and the energy and endurance figures follow the decisions.
5. Decision 4 (docs): Set the plus or minus 3 degree window in the firmware sketch and controller notes when the firmware is written (TRL 4, on hold).
6. Decision 5 (pictures): Bring `cad/src/product_model.py` to the constructable design (drive, bearings, mounts) and regenerate the photoreal renders, `media/card.png` and `media/social-preview.png` on Amish's Mac.
7. Decision 3 (pictures): Update the concept media labels and blueprint key figures that show 17 steps per minute and the plus or minus 6 degree window when the media are next regenerated.

### Points found in the review

- Items 6 and 7 overlap (user group for interviews and co-design partner); they could be one decision.
- Three requirements are now not met (mass, climb speed and grip force) and the cost is USD 776 against USD 650 (USD 126 over); items 2 to 4 relax or trade all three.
- The cluster shaft's 1.4 factor at a 3 g load is on 1018 steel with fatigue not assessed; this deserves attention before any loaded stair trial.

### Safety

The cluster shaft is to be 4140 rather than 1018; its strength must be recalculated and its fatigue assessed before any loaded stair trial. The plus or minus 3 degree window keeps the grip force at 100 N or less on paper but may cause frequent stops on uneven stairs; it is widened only after grip force is measured. R3 and R5 are relaxed for the first prototype only.

### Recommended next step

Update BOM line 3 and recalculate the cluster shaft for 4140 with a fatigue check, then rerun `sizing.py` with the decided targets. TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that every follow-up action from the open-decision sign-off be carried out. trl stays 3; nothing was built or tested. The follow-ups listed in the "Follow-up actions" list of the "open decisions decided" section above are marked here.

### Approved follow-ups carried out

1. Done. Decision 1 (BOM): line 3 is now a 25 mm keyed cluster shaft in 4140 quenched and tempered alloy steel with a mill certificate, repriced from USD 96 to USD 108 (about USD 22 per metre for 25 mm bar, 0.5 m, keyway milled, against about USD 8 for 1018 bar; indicative). `bom/bom.csv`, `bom/bom-notes.md`.
2. Done. Decision 1 (drawings): shaft material in `cad/src/model.py` (part name; mass unchanged at 1.89 kg because both steels are 7,850 kg/m3) and on making sketch SCM-DWG-106, now Rev P2. STEP and STL re-exported; 90 of 90 constructability checks pass.
3. Done. Decision 1 (calcs): SCM-CAL-001 v0.5 recalculates the shaft for 4140 (655 MPa minimum yield assumed): factor 2.5 at 3 g (1.4 on 1018). Fatigue assessed (section 8): endurance limit 259 MPa, Goodman factor 1.8. The 1,000 MPa tensile strength is an assumption to confirm from the mill certificate.
4. Done. Decision 2 (calcs): `docs/04-calcs/sizing.py` rerun at R5 35 kg, R3 16 steps/min (3.75 s per third of a turn) and the plus or minus 3 degree window; `results.csv`, inputs table, torque, power, chain, grip force and structure figures updated.
5. Not done: set the plus or minus 3 degree window in the firmware sketch and controller notes; this is firmware, TRL 4 work, on hold.
6. Done as far as possible here. Decision 5 (pictures): `cad/src/product_model.py` now takes the drive, bearings, axle plates, chain case, uprights, standoffs, lowered cross bar and fixings from `model.py`, with the gearmotor standing up the frame on the inner case plate, the electronics box, pack, cradle and switch on the uprights, and the skids on standoffs. Render scenes exported (hero, exploded, detail). Not done: photoreal renders, `media/card.png` and `media/social-preview.png`, which are made on Amish's Mac.
7. Done. Decision 3 (pictures): concept media labels and key figures now read 244 W at 16 steps/min and R3, R5 and R6 met on paper; `media/` regenerated.

### Requirement status changes (SCM-CAL-001 v0.5)

None in status against v0.4 (R3, R5 and R6 stay met on paper as set for the first prototype). Figures changed: R3 244 W needed from the 250 W motor (16.4 steps/min at most); R6 99 N at the plus or minus 3 degree edge; R1 shaft factor 2.5 (fatigue 1.8), rail 3.2. Ten met, four not verifiable at TRL 3 (R7, R8, R9, R14), R12 over the target.

### Cost and mass

Value-engineering target: USD 650. Estimated cost of the constructable design: USD 788 (USD 138 over the target). `budget_usd` is unchanged at 650. Truck mass 34.2 kg (unchanged), against the 35 kg target for the first prototype.

### Documents and pictures changed

- `docs/04-calcs/01-sizing.md` (SCM-CAL-001 v0.5), `docs/03-requirements.md` (SCM-REQ-001 v0.7), `docs/02-concept.md` (SCM-PRC-001 v0.7), `docs/05-build-plan.md` (SCM-BLD-001 v0.3), `docs/06-design-decisions.md` (SCM-DEC-001 v0.3), `README.md`, `bom/bom.csv`, `bom/bom-notes.md` (rewritten to the 17 current lines; it still showed the 2026-09-25 total).
- General arrangement SCM-DWG-001 Rev P5; making sketch SCM-DWG-106 Rev P2; `media/concept-blueprint`, `hero.png`, `exploded.png`, `flow.png`, `model.glb`. No other build plan picture changed because no geometry changed.
- Appearance deviations (Proposed, awaiting Amish): the chain case of the appearance model is now the constructable case, so the earlier inspection window over the chain is dropped (the case sits on the inside of the rail); sprockets and chains are shown as in the CAD model, without individual teeth; the controller wiring is the CAD harness.

### Cross-repo actions

None found for this repo.

### Safety

The 4140 shaft factors rest on assumed minimum strengths and a keyway fatigue factor; confirm from the mill certificate and test before any loaded stair trial. The 99 N grip force leaves almost no margin under 100 N, and the tight window may stop the climb often on uneven stairs.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.

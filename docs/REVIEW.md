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

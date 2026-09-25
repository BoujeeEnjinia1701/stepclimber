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

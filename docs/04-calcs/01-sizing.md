---
doc_id: SCM-CAL-001
title: StepClimber sizing calculations
project: StepClimber
doc_type: Calculation note
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (cluster geometry, nosing clearances, torque, energy, holding, handle force, structure, mass, size, cost) with a status for every requirement
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); recalculated for 200 mm wheels, 150 mm arms, a two-stage chain drive, a plus or minus 6 degree tilt window and the revised R3, R5 and R12 targets
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Recalculated for the constructable design (SCM-DDR-003); mass itemised, chain centres to whole chains, bearings inside the frame, frame-fixed outlines checked against the nosings; budget reported as a value-engineering target
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: Table 10 rows R3, R5, R6 and R7, the summary and the R3, R5 and R6 text of their sections follow the 2026-10-02 decisions (SCM-DEC-001, items 1 to 4); no computed number changed
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Recalculated with the approved targets (R3 16 steps/min, R5 35 kg, plus or minus 3 degree window) and the 4140 cluster shaft; fatigue of the shaft assessed; BOM line 3 repriced (USD 788 total); R3, R5 and R6 met on paper
---

# StepClimber sizing calculations

This version recalculates StepClimber for the constructable design of SCM-DDR-003, made on 2026-10-01 under Amish's 2026-09-30 instruction to make the design physically buildable. The cluster, ratios, tilt window and stair geometry of SCM-DDR-002 are unchanged. What changed is that every part now exists and is fixed to its neighbours: the bearings sit inside the frame on welded axle plates, the countershaft runs in two bearings in a closed chain case, the chain centres suit whole chains, and the parts on the frame back hang on uprights. Naming every part also lets the mass be added up rather than allowed for, and the truck comes out at 34.2 kg (26.3 kg in v0.2).

**Ten requirements are met on paper** and four cannot be verified without hardware; R12 is USD 138 over the value-engineering target. Amish's decisions of 2026-10-02 (SCM-DEC-001, items 1 to 4) set R5 to 35 kg and R3 to 16 steps/min for the first prototype, the tilt window to plus or minus 3 degrees for the first loaded trials, and the cluster shaft to 4140 quenched and tempered alloy steel. With those inputs the climb needs 244 W from the 250 W motor (R3 met, 2 % margin), the truck is 34.2 kg (R5 met, 0.8 kg spare) and the grip force at the window edge is 99 N (R6 met). Every frame-fixed part near the shaft clears every nosing in the R2 range by 10 mm or more (R15). At a 3 g dropped step the safety factors are 2.5 for the 4140 shaft (1.4 on 1018), 1.5 for the spider and 3.2 for the rails, and the shaft has a fatigue factor of 1.8 (section 8). The pack gives about 1,215 loaded steps per charge. The estimated cost is USD 788 against the USD 650 value-engineering target (the 4140 shaft adds USD 12).

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates for a paper design; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Payload | 60 kg (132 lb) | R1, decided 2026-09-25 (SCM-DDR-001) |
| Truck mass | 34.2 kg (roll-up in section 9); target 35 kg for the first prototype | Component estimates and the constructable model; R5 set 2026-10-02 (SCM-DEC-001, item 2) |
| Combined center of mass | 500 mm above the shaft, along the frame | Parcels stacked on the toe plate |
| Design stair | 196 mm (7.75 in) risers, 254 mm (10 in) treads; nosing overhang 0 to 32 mm | IRC limits; R2 |
| Climb speed | 16 steps/min: one third of a turn in 3.75 s | R3 for the first prototype, set 2026-10-02 (SCM-DEC-001, item 3) |
| Tilt window | Plus or minus 3 degrees about the set angle | R7 for the first loaded trials, set 2026-10-02 (SCM-DEC-001, item 4) |
| Drive efficiencies | Driver 95 %, brushed motor 80 %, self-locking worm 45 %, first chain stage and bearings 95 %, second chain stage 97 % | Typical parts |
| Worm | Single start, 4 degree lead, ratio about 75 | Typical wheelchair worm gearmotor, 40 rpm output |
| Brake | 2.0 N·m spring-applied on the motor shaft | Typical wheelchair motor brake |
| Dynamics factor | 1.3 on static shaft torque | Friction and the landing thump |
| Dropped-step shock | 3 g on the structure | A cluster dropping off a nosing |
| Materials | Cluster shaft 4140 quenched and tempered, 655 MPa minimum yield and 1,000 MPa tensile assumed (to confirm with the mill certificate); spider plate S275; frame tube 250 MPa after welding | Shaft material decided 2026-10-02 (SCM-DEC-001, item 1); common stock otherwise |
| Chain | 06B: 9.525 mm pitch, 8.9 kN minimum tensile; 08B: 12.7 mm, 17.8 kN | ISO 606 catalog minimums, to confirm with the supplier |
| Pack | 256 Wh LiFePO4, 90 % usable, 10 % extra for standby, starts and stops | R13 |
| Charger | 29.2 V, 3 A, 90 % efficient, plus 0.3 h constant-voltage tail | R13 |
| Rolling resistance | 0.03 | Solid rubber on a smooth floor |
| Operator | Stands uphill of the truck and pushes or pulls the grip horizontally while climbing | Normal hand truck practice on stairs |

The design load is 94.2 kg in total, a weight of 924 N. The clusters are assumed to carry all of it while lifting, which is conservative.

## 2. Cluster geometry (R2)

The cluster has three 200 mm wheels on 150 mm arms, so the wheel centers are 259.8 mm apart, the shaft sits 175.0 mm above the floor and the cluster is 500 mm across.

A climb starts with the wheel nearest the stair lodged against the riser. The cluster turns about that wheel (the pivot) until the top wheel lands on the tread above, 259.8 mm from the pivot and one riser higher. The landing wheel's contact point is therefore sqrt(*d*² minus *h*²) minus 100 mm past the riser face, plus the nosing overhang. Table 2 shows how far it lands past the nosing edge.

*Table 2. Landing point of the swinging wheel past the nosing edge.*

| Riser | No overhang | 32 mm overhang | Tread needed to land |
| --- | --- | --- | --- |
| 100 mm | 139.8 mm | 139.8 mm | 239.8 mm |
| 150 mm | 112.1 mm | 125.5 mm | 212.1 mm |
| 175 mm | 92.0 mm | 124.0 mm | 192.0 mm |
| 196 mm | 70.5 mm | 102.5 mm | 170.5 mm |
| 200 mm | 65.8 mm | 97.8 mm | 165.8 mm |
| 210 mm | 53.0 mm | 85.0 mm | 153.0 mm |
| 220 mm | 38.2 mm | 70.2 mm | 138.2 mm |
| 241 mm | Does not land on a square nosing (minus 2.9 mm) | 29.1 mm | |

With at least 30 mm of landing past a square nosing, the largest riser the cluster climbs is 225 mm (209 mm on the v0.1 cluster), which covers the 100 to 200 mm range of R2 with room for steeper older stairs. The longest tread needed is 239.8 mm, on low risers, so every tread of 250 mm or more is long enough; this is the one geometric cost of the longer arm.

After the landing, the cluster turns on about the landed wheel for the rest of the third of a turn, which lifts the old pivot wheel clear, and the courier rolls the truck back on the landed wheel to the next riser.

## 3. Nosing clearances (R2, R15)

The script steps the cluster through a full climb in 2D and records how close the hub, the spider arms and the wheels come to the nosing corners.

*Table 3. Closest approach to a nosing during one step.*

| Riser | Overhang | Hub to nosing | Spider arm clearance | Wheel clearance |
| --- | --- | --- | --- | --- |
| 100 mm | 0 | 119.6 mm | 57.0 mm | 0.0 mm |
| 100 mm | 32 mm | 119.6 mm | 57.0 mm | 0.0 mm |
| 125 mm | 0 | 105.6 mm | 50.0 mm | 3.1 mm |
| 125 mm | 32 mm | 105.0 mm | 47.3 mm | 0.0 mm |
| 150 mm | 0 | 93.9 mm | 47.4 mm | 11.8 mm |
| 150 mm | 32 mm | 89.5 mm | 35.2 mm | 0.0 mm |
| 175 mm | 0 | 87.1 mm | 50.0 mm | 25.0 mm |
| 175 mm | 32 mm | 71.6 mm | 19.5 mm | 0.5 mm |
| 196 mm | 0 | 87.8 mm | 49.1 mm | 22.4 mm |
| 196 mm | 32 mm | **64.6 mm** | 25.9 mm | 16.6 mm |
| 200 mm | 0 | 88.8 mm | 48.4 mm | 19.7 mm |
| 200 mm | 32 mm | **64.2 mm** | 27.7 mm | 19.9 mm |

The nosing passes through the gap between the two lower arms, close to the shaft line, at the moment the swinging wheel lands. Anything on the shaft line must therefore stay within the minimum hub-to-nosing distance less a 10 mm margin: **77 mm with square nosings and 54.2 mm with 32 mm overhangs** (48 and 26 mm on the v0.1 cluster).

- The 25 mm shaft, the 38 mm weld-on hubs, the 48 mm spider centre discs and the 45 mm flange bearing housings clear every nosing in the R2 range.
- **The 08B 20-tooth shaft sprocket (88 mm across) and its guard sweep a 53.9 mm radius, 0.3 mm inside the 54.2 mm limit**, so the 10 mm clearance is kept with 32 mm overhangs. R15 is met, with the guard sized to the limit; a thinner guard gap would add margin.
- The countershaft sits 143.9 mm up the frame from the cluster shaft and 15 mm toward the stair (SCM-DDR-003, P5 and P6). Its 35-tooth sprocket guard (65.8 mm radius) passes no closer than 146 mm to any nosing, a clearance of 80 mm.
- The constructable design adds parts on the frame near the shaft. The script turns every nosing position of the climb into the frame's own coordinates and measures the distance to each outline (Table 3a). All clear by 10 mm or more.
- **The spider arms clear nosing overhangs of 32 mm** in the R2 riser range, with 19.5 mm to spare at the worst case (175 mm riser). R2 is met. The wheels touching a nosing briefly (clearance near zero) is acceptable: they are rubber and roll over it.
- The frame back clears the nosings above the countershaft by 109 mm beyond the skid face at the 30 degree climbing tilt.

*Table 3a. Frame-fixed outlines near the shaft against every nosing in the R2 range (10 mm needed).*

| Outline | Nearest nosing |
| --- | --- |
| Chain case and drive-side axle plate (53.9 mm on the shaft line, 65.8 mm round the countershaft) | 10.3 mm |
| Plain-side axle plate, 92 x 144 mm | 13.5 mm |
| Main flange bearing | 27.2 mm |
| Countershaft flange bearing | 113.6 mm |
| Gearmotor gearbox | 118.5 mm |
| Motor and brake | 127.2 mm |
| Replacement low cross bar | 96.6 mm |
| Rails, load side of the shaft | 79.5 mm |
| Nosing guard skids (meant to be the nearest part) | 28.4 mm |

*Table 4. Cluster sizes compared at v0.1 (hub to nosing and arm clearance with square and 32 mm nosings). The 150 mm arm with 200 mm wheels was recommended and decided.*

| Arm | Wheel | Hub to nosing | Arm clearance | Landing at 200 mm riser | Tread needed at 100 mm | Hub height |
| --- | --- | --- | --- | --- | --- | --- |
| 135 mm | 150 mm | 58 / 36 mm | 21 / -8 mm | 46 mm | 211 mm | 142 mm |
| 135 mm | 200 mm | 93 / 70 mm | 54 / 29 mm | 21 mm | 211 mm | 168 mm |
| 150 mm | 150 mm | 52 / 29 mm | 14 / -15 mm | 91 mm | 240 mm | 150 mm |
| **150 mm** | **200 mm** | **87 / 64 mm** | **47 / 20 mm** | **66 mm** | **240 mm** | **175 mm** |
| 165 mm | 200 mm | 81 / 64 mm | 42 / 12 mm | 104 mm | 268 mm | 182 mm |

The 54 mm envelope takes an 08B 20-tooth sprocket (chain safety factor 4.0, section 4) or a 06B 27-tooth one (safety factor 2.2, too low). Because the final stage is then only 2:1, the drive has a second chain stage: a 06B 10-tooth sprocket on the gearmotor drives a 35-tooth sprocket on the countershaft (3.5:1), for 7:1 overall.

## 4. Torque, speed and power (R3)

At 16 steps/min the shaft turns at 0.559 rad/s (5.33 rpm). Lifting 924 N through 196 mm takes 181 J per step, a mean shaft torque of 86 N·m over a third of a turn.

The drive torque at any instant equals the vertical load times the horizontal distance from the support wheel to the hub, plus the grip force times the vertical distance. The peak is 139 N·m static, when the hub passes level with the landed wheel (the full 150 mm arm), and 181 N·m with the 1.3 dynamics factor (the peak is a little lower than in v0.4 because the handle force is smaller inside the plus or minus 3 degree window). That needs 101 W at the shaft and **244 W from the motor**, a 2 % margin under its 250 W rating. **R3 is met** at the 16 steps/min Amish set for the first prototype on 2026-10-02 (SCM-DEC-001, item 3): the fastest climb this motor supports at the new mass is 16.4 steps/min. At 17 steps/min the climb would need 260 W, and at 20 steps/min 305 W.

*Table 5. Two-stage chain drive at the peak torque.*

| Stage | Sprockets and chain | Ratio | Centres | Chain pull | Safety factor on minimum tensile |
| --- | --- | --- | --- | --- | --- |
| First, gearmotor to countershaft | 06B, 10T to 35T, 54 links | 3.5:1 | 145.1 mm | 1,759 N (93 N·m at the countershaft) | 5.1 |
| Final, countershaft to cluster shaft | 08B, 10T to 20T, 38 links | 2:1 | 144.7 mm | 4,465 N | 4.0 |

The centres are set so that each chain is a whole number of links (even counts, so no offset link); slots let the countershaft bearings and the gearmotor move 4 mm either way to tension them. The 7:1 drive needs the gearmotor to give 40 rpm and 28.1 N·m, inside its 30 N·m rating.

## 5. Energy and endurance (R4, R13)

*Table 6. Energy per loaded step on the design stair.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Drive efficiency up | 31.5 % | 0.95 x 0.80 x 0.45 x 0.95 x 0.97 |
| Pack energy per step up | 575 J (0.16 Wh) | 181 J / 0.315 |
| Pack energy per step down | 46 J | Lowering through a self-locking worm |
| Usable pack energy | 829 kJ | 256 Wh x 90 % |
| Loaded steps per charge, up and down | **1,215** | 829 kJ / ((575 + 46) J x 1.1) |
| Typical day | 25 drops of three floors (48 steps) | |
| Charge time | 3.5 h | 256 Wh / (29.2 V x 3 A x 0.9) plus 0.3 h |

Lowering: a 45 % efficient worm with a 4 degree lead has a friction angle of 4.83 degrees. Driving it while the load pushes needs tan(4.83 minus 4) / tan 4 = 21 % of the lift work at the worm, so the motor supplies 46 J per step down instead of braking.

The energy flow for one step up is 575 J from the pack, 546 J after the driver, 437 J at the motor shaft, 197 J after the worm and 181 J of lift (Figure 2 of SCM-PRC-001). R4 (1,000 steps each way) and R13 (4 h charge) are met.

## 6. Holding on the stair (R8)

The shaft must hold 139 N·m at the worst point of a step, or 19.9 N·m at the gearmotor output.

- **Worm.** Its back-drive efficiency is 2 minus 1/0.45 = -0.22. A value at or below zero means the worm cannot be driven backwards by the load when static, so it holds without power. Vibration can lower the friction and let a self-locking worm creep; this cannot be checked on paper.
- **Brake.** If the worm were fully back-drivable, the motor brake would need 140 / (75 x 7) = 0.27 N·m. A 2.0 N·m brake gives a 7.5-times margin.

Two independent holds exist on paper. The drift limit in R8 (5 mm in 10 minutes) needs a test and is not verifiable at TRL 3.

## 7. Balance and handle force (R6, R7, R10)

During a step the hub moves relative to the wheel carrying the load: from 29 mm on the stair side of the support wheel to 150 mm on the far side. The frame angle is held, so the center of mass moves with the hub. The best set angle puts the center of mass 61 mm on the stair side of the hub, which leaves a swing of plus or minus 89 mm about the support point. At the edge of the plus or minus 3 degree window the center of mass moves a further 26 mm.

*Table 7. Grip force during a climb on the design stair.*

| Case | Grip force |
| --- | --- |
| At the set angle, worst point of the step | 76 N |
| At the plus or minus 3 degree window edge | **99 N** (R6 met) |
| For reference, at a plus or minus 6 degree window edge | 121 N (over R6) |
| Widest window that meets 100 N | Plus or minus 3.1 degrees (99 N) |
| Vertical grip force at the plus or minus 3 degree window edge (flat hand truck convention) | 222 N |

The horizontal-force case is the relevant one: the courier stands uphill and pushes or pulls the grip, which is about 1.1 m above the support wheel. At a plus or minus 6 degree window R6 would be missed by 21 % (121 N). Amish decided on 2026-10-02 (SCM-DEC-001, item 4) to tighten the window to plus or minus 3 degrees for the first loaded trials, which keeps the grip force at 99 N, so **R6 is met on paper**. A window this tight may stop the climb often on uneven stairs; it is widened only after the grip force is measured.

Pushing on the flat takes 0.03 x 924 N = 28 N, which meets R10.

## 8. Structure (R1)

*Table 8. Stresses at the peak torque and a 3 g dropped-step load.*

| Part | Load | Stress | Safety factor on yield |
| --- | --- | --- | --- |
| Shaft, 25 mm, 4140 quenched and tempered | 181 N·m torsion (59 MPa); bending over the 93 mm from the bearing centre to the wheel plane (84 MPa) | 132 MPa von Mises; keyway factor 2 | 2.5 (was 1.4 on 1018 at 370 MPa) |
| Spider arm, 45 x 6 mm, 150 mm long | 1.39 kN at the wheel: bending 103 MPa; twist from the 30 mm wheel offset 84 MPa | 178 MPa von Mises | 1.5 |
| Frame rail, 28 x 1.5 mm tube | 76 N·m each from the window-edge grip force | 97 MPa | 2.6 |

R1 is met statically. The shaft margin is lower than in v0.2 (1.8) because the bearings now sit inside the frame, where they can be fixed, so the shaft overhangs its bearing by 93 mm rather than 48 mm (SCM-DDR-003, P1). The shaft was 1018 cold drawn in v0.4 and earlier (factor 1.4); Amish decided on 2026-10-02 to make it from 4140 quenched and tempered alloy steel (SCM-DEC-001, item 1), which raises the factor to 2.5 on a minimum yield of 655 MPa.

**Fatigue of the cluster shaft.** The bending load turns with the shaft, so at the 1 g stair load the bending is fully reversed once per revolution, with an alternating moment of 43 N·m on the 93 mm overhang; the torque is pulsating, from zero to the 181 N·m peak at each step. The endurance limit is half the 1,000 MPa tensile strength (500 MPa), reduced by a machined-surface factor of 0.72, a size factor of 0.88 for 25 mm and a 99 % reliability factor of 0.814, giving 259 MPa. Each of the keyway's two stress concentrations is taken as 2.0. A modified Goodman line with the distortion-energy combination gives a **fatigue safety factor of 1.8**, so the shaft has a long life on paper. The tensile strength is an assumed minimum for the bar and must be confirmed from the mill certificate, and the keyway and the welded hubs make a test at TRL 4 worth doing before any loaded stair trial. Fatigue of the welded frame is not assessed here.

## 9. Mass and size (R5, R11)

*Table 9. Mass roll-up. Lines 14 to 17 and the stub axles were added to make the design buildable (SCM-DDR-003); line 3 is now itemised.*

| Item | Mass |
| --- | --- |
| 1 Frame and toe plate (the replacement low bar replaces the bar cut off) | 8.0 kg |
| 2 Clusters (pair), 200 mm wheels | 5.5 kg |
| 2 Stub axles (6), 20 mm bar | 0.8 kg |
| 3 Cluster shaft 1.9 kg, countershaft 0.3 kg, four flange bearings 2.1 kg, four sprockets 0.7 kg, two chains 0.6 kg | 5.5 kg |
| 4 Worm gearmotor with brake | 4.5 kg |
| 5 and 6 Driver, controller, IMU | 0.8 kg |
| 7 Pack and cradle | 2.6 kg |
| 8 Switch, fuse, harness | 0.5 kg |
| 9 Handle controls | 0.6 kg |
| 10 Strap | 0.4 kg |
| 11 Skids | 0.4 kg |
| 13 Enclosure and hardware | 0.5 kg |
| 14 Axle plate 0.4 kg, case outer plate 1.1 kg, case inner plate 0.4 kg, band 0.3 kg, spacers 0.3 kg | 2.5 kg |
| 15 Component uprights | 0.6 kg |
| 16 Skid standoffs | 0.5 kg |
| 17 Fixings added for construction | 0.5 kg |
| **Total** | **34.2 kg** |

**R5 is met on paper at the 35 kg set for the first prototype** (0.8 kg spare); against the earlier 27 kg it would be 7.2 kg over. About 3.0 kg of the rise comes from itemising the drive, which v0.2 carried as a 2.5 kg allowance (the 25 mm shaft alone is 1.9 kg), and about 4.4 kg from the parts and fixings added to make the design buildable. The case plates are already thin steel and aluminium; Amish set R5 to 35 kg for the first prototype on 2026-10-02 (SCM-DEC-001, item 2), which the truck meets, and the savings of SCM-DDR-003 item A1 are tried when parts are bought. The 4140 shaft has the same density as 1018, so the mass is unchanged. The pack is 2.6 kg (3 kg or less, met).

From the model, the truck is 569 mm wide at the wheel faces and 588 mm over the wheel end screws, and 1,451 mm tall upright, which meets R11 (600 and 1,500 mm). A folding hinge 950 mm above the shaft (the Option C study, not adopted) would fold the truck to 1,139 mm.

## 10. Cost (R12)

Value-engineering target: USD 650 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 788, from the 17 BOM lines (USD 138 over the target). Line 3 rose by USD 12 for the 4140 shaft (about USD 22 per metre for 25 mm bar, 0.5 m, keyway milled, mill certificate, against about USD 8 for 1018). The parts added for construction (lines 14 to 17) cost USD 99, and the weld-on hubs, the extra bearing and the connecting links USD 44 more on lines 2 and 3. The main cost drivers and the savings worth trying are listed in the design decisions register (SCM-DEC-001).

## 11. Requirement status

*Table 10. Every requirement against the calculations. The status is met, not met or not verifiable at TRL 3; R12 is reported against the value-engineering target.*

| ID | Requirement | Target | Value | Status |
| --- | --- | --- | --- | --- |
| R3 | Climb speed | 16 steps/min or more at rated load for the first prototype (set 2026-10-02; was 17) | 244 W needed on the 250 W motor; 16.4 steps/min at most | Met on paper |
| R5 | Truck mass | 35 kg or less for the first prototype (set 2026-10-02; was 27 kg); pack 3 kg or less | 34.2 kg; pack 2.6 kg | Met on paper |
| R6 | Operator handle force | 100 N or less inside the tilt window (plus or minus 3 degrees for the first loaded trials, set 2026-10-02) | 99 N at the plus or minus 3 degree edge; 76 N at the set angle (121 N at a plus or minus 6 degree edge) | Met on paper at the plus or minus 3 degree window |
| R1 | Rated stair load | 60 kg up and down; 100 kg on the flat | Safety factors 2.5 shaft (fatigue 1.8), 1.5 spider, 3.2 rail at 3 g | Met |
| R2 | Stair range | Risers 100 to 200 mm, treads 250 mm or more, nosing up to 32 mm | Landing 66 mm past the nosing at 200 mm; tread needed 240 mm; arms clear 32 mm overhangs | Met |
| R4 | Endurance | 1,000 loaded steps up plus 1,000 down | 1,215 | Met |
| R10 | Flat rolling | 40 N or less | 28 N | Met |
| R11 | Size | Width 600 mm or less; upright height 1,500 mm or less | 588 mm over the wheel end screws; 1,451 mm | Met |
| R13 | Battery | 24 V LiFePO4, BMS, fused, 0 to 45 °C charge window, 4 h charge | 3.5 h | Met |
| R15 | Stair and building protection | No steel contact with stairs; skids over nosings | Shaft-line guard 53.9 mm against 54.2 mm allowed; countershaft guard clears by 80 mm; every frame-fixed outline 10 mm or more from every nosing | Met |
| R12 | Affordable | Value-engineering target USD 650 | USD 788 | USD 138 over the target |
| R7 | Tilt control | 100 Hz IMU, plus or minus 3 degree window for the first loaded trials (set 2026-10-02), stop within 0.2 s | Control concept only | Not verifiable at TRL 3 |
| R8 | Hold on any loss | Holds with power off; drift 5 mm or less in 10 min | Worm self-locking; brake margin 7.5 times | Not verifiable at TRL 3 |
| R9 | Hold-to-run | Stops within 0.2 s of grip release | Circuit concept only | Not verifiable at TRL 3 |
| R14 | Environment | 0 to 40 °C, IP54, rain on stoops | Enclosure concept only | Not verifiable at TRL 3 |

Counts: 10 met, 4 not verifiable at TRL 3, and R12 reported against the value-engineering target (USD 138 over).

## Safety

> **Safety:** These are paper numbers for a 94 kg load moving on a stair with a person uphill of it. The design keeps steel parts clear of nosings on paper, but the chain case sits at the limit of its envelope on the shaft line, so a bent case or a nosing outside the R2 range could still be struck; a strike mid-step could jerk the frame toward the courier or stall the climb with the load half-lifted. The grip force at the plus or minus 3 degree window edge (99 N) is only just under the 100 N target; at a plus or minus 6 degree window it would be 121 N. The holding figures in section 6 assume a static load; worm creep under vibration and the brake's real holding torque must be confirmed before anyone climbs with a load. The 3 g shock factor is a judgment, not a measurement.

## References

- SCM-REQ-001 v0.7, requirements.
- SCM-PRC-001 v0.7, design precis.
- SCM-DDR-001, TRL 2 review decisions; SCM-DDR-002, recommendations accepted; SCM-DDR-003, design for construction.
- SCM-BLD-001, prototype build plan; SCM-DEC-001, design decisions register.
- Flange bearing, weld-on hub and sprocket masses: catalogue-class values for 20 and 25 mm two-bolt flange units, 1610 weld-on hubs and plate sprockets, to confirm when bought.
- ISO 606, short-pitch transmission precision roller chains (minimum tensile strengths, confirm with the chain supplier's catalog).
- US International Residential Code, stair riser and tread limits, as summarized in SCM-PRB-001.

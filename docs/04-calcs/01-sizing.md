---
doc_id: SCM-CAL-001
title: StepClimber sizing calculations
project: StepClimber
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# StepClimber sizing calculations

This version recalculates StepClimber for the cluster and drive rework Amish decided on 2026-09-25 (SCM-DDR-002): 200 mm wheels on 150 mm arms, a two-stage chain drive with an 08B 20-tooth sprocket on the cluster shaft, a tilt window of plus or minus 6 degrees, and revised speed, mass and budget targets. On paper the design now meets ten of its fifteen requirements, misses one and leaves four that cannot be verified without hardware. The two stair-contact failures of v0.1 are fixed: the shaft-line guard now sweeps a 53.9 mm radius inside the 54.2 mm envelope that nosings leave free (R15; it was 104 mm against 48 mm), and the spider arms clear nosing overhangs of 32 mm (R2; they cleared 23 mm). **One requirement is not met.** R6: the larger cluster widens the swing of the load about its support wheel, so the courier's grip force reaches 111 N at the plus or minus 6 degree window edge against a 100 N limit. The drive gives 238 W peak on the 250 W motor at 17 steps/min, about 1,330 loaded steps per charge, an 8-times brake margin and safety factors of 1.7 or more at a 3 g dropped-step load. The truck weighs 26.3 kg and costs $633 in parts.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates for a paper design; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Payload | 60 kg (132 lb) | R1, decided 2026-09-25 (SCM-DDR-001) |
| Truck mass | 26.3 kg (roll-up in section 9) | Component estimates |
| Combined center of mass | 500 mm above the shaft, along the frame | Parcels stacked on the toe plate |
| Design stair | 196 mm (7.75 in) risers, 254 mm (10 in) treads; nosing overhang 0 to 32 mm | IRC limits; R2 |
| Climb speed | 17 steps/min: one third of a turn in 3.5 s | R3, revised 2026-09-25 (SCM-DDR-002) |
| Tilt window | Plus or minus 6 degrees about the set angle | R7, decided 2026-09-25 (SCM-DDR-002) |
| Drive efficiencies | Driver 95 %, brushed motor 80 %, self-locking worm 45 %, first chain stage and bearings 95 %, second chain stage 97 % | Typical parts |
| Worm | Single start, 4 degree lead, ratio about 75 | Typical wheelchair worm gearmotor, 40 rpm output |
| Brake | 2.0 N·m spring-applied on the motor shaft | Typical wheelchair motor brake |
| Dynamics factor | 1.3 on static shaft torque | Friction and the landing thump |
| Dropped-step shock | 3 g on the structure | A cluster dropping off a nosing |
| Materials | Shaft 1018 cold drawn, 370 MPa yield; spider plate S275; frame tube 250 MPa after welding | Common stock |
| Chain | 06B: 9.525 mm pitch, 8.9 kN minimum tensile; 08B: 12.7 mm, 17.8 kN | ISO 606 catalog minimums, to confirm with the supplier |
| Pack | 256 Wh LiFePO4, 90 % usable, 10 % extra for standby, starts and stops | R13 |
| Charger | 29.2 V, 3 A, 90 % efficient, plus 0.3 h constant-voltage tail | R13 |
| Rolling resistance | 0.03 | Solid rubber on a smooth floor |
| Operator | Stands uphill of the truck and pushes or pulls the grip horizontally while climbing | Normal hand truck practice on stairs |

The design load is 86.3 kg in total, a weight of 847 N. The clusters are assumed to carry all of it while lifting, which is conservative.

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

- The 25 mm shaft, the 38 mm spider bosses and the 45 mm flange bearing housings clear every nosing in the R2 range.
- **The 08B 20-tooth shaft sprocket (88 mm across) and its guard sweep a 53.9 mm radius, 0.3 mm inside the 54.2 mm limit**, so the 10 mm clearance is kept with 32 mm overhangs. R15 is met, with the guard sized to the limit; a thinner guard gap would add margin.
- The countershaft sits 150 mm up the frame from the cluster shaft. Its 35-tooth sprocket guard (65.8 mm radius) passes no closer than 162 mm to any nosing, a clearance of 96 mm.
- **The spider arms clear nosing overhangs of 32 mm** in the R2 riser range, with 19.5 mm to spare at the worst case (175 mm riser). R2 is met. The wheels touching a nosing briefly (clearance near zero) is acceptable: they are rubber and roll over it.
- The frame back clears the nosings above the countershaft by 109 mm beyond the skid face at the 30 degree climbing tilt.

*Table 4. Cluster sizes compared at v0.1 (hub to nosing and arm clearance with square and 32 mm nosings). The 150 mm arm with 200 mm wheels was recommended and decided.*

| Arm | Wheel | Hub to nosing | Arm clearance | Landing at 200 mm riser | Tread needed at 100 mm | Hub height |
| --- | --- | --- | --- | --- | --- | --- |
| 135 mm | 150 mm | 58 / 36 mm | 21 / -8 mm | 46 mm | 211 mm | 142 mm |
| 135 mm | 200 mm | 93 / 70 mm | 54 / 29 mm | 21 mm | 211 mm | 168 mm |
| 150 mm | 150 mm | 52 / 29 mm | 14 / -15 mm | 91 mm | 240 mm | 150 mm |
| **150 mm** | **200 mm** | **87 / 64 mm** | **47 / 20 mm** | **66 mm** | **240 mm** | **175 mm** |
| 165 mm | 200 mm | 81 / 64 mm | 42 / 12 mm | 104 mm | 268 mm | 182 mm |

The 54 mm envelope takes an 08B 20-tooth sprocket (chain safety factor 4.3, section 4) or a 06B 27-tooth one (safety factor 2.2, too low). Because the final stage is then only 2:1, the drive has a second chain stage: a 06B 10-tooth sprocket on the gearmotor drives a 35-tooth sprocket on the countershaft (3.5:1), for 7:1 overall.

## 4. Torque, speed and power (R3)

At 17 steps/min the shaft turns at 0.593 rad/s (5.67 rpm). Lifting 847 N through 196 mm takes 166 J per step, a mean shaft torque of 79 N·m over a third of a turn.

The drive torque at any instant equals the vertical load times the horizontal distance from the support wheel to the hub, plus the grip force times the vertical distance. The peak is 128 N·m static, when the hub passes level with the landed wheel (the full 150 mm arm), and 166 N·m with the 1.3 dynamics factor. That needs 99 W at the shaft and **238 W from the motor**, 5 % under its 250 W rating. R3, revised to 17 steps/min on 2026-09-25, is met. The fastest climb this motor supports is 17.8 steps/min; the v0.1 rate of 20 steps/min would need 280 W.

*Table 5. Two-stage chain drive at the peak torque.*

| Stage | Sprockets | Ratio | Chain pull | Safety factor on minimum tensile |
| --- | --- | --- | --- | --- |
| First, gearmotor to countershaft | 06B, 10T to 35T | 3.5:1 | 1,615 N (86 N·m at the countershaft) | 5.5 |
| Final, countershaft to cluster shaft | 08B, 10T to 20T | 2:1 | 4,102 N | 4.3 |

The 7:1 drive needs the gearmotor to give 40 rpm and 25.8 N·m, inside its 30 N·m rating. Staying at 6:1 would have asked for 30.0 N·m, at the rating, which is why the countershaft sprocket was raised from 30 to 35 teeth.

## 5. Energy and endurance (R4, R13)

*Table 6. Energy per loaded step on the design stair.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Drive efficiency up | 31.5 % | 0.95 x 0.80 x 0.45 x 0.95 x 0.97 |
| Pack energy per step up | 527 J (0.15 Wh) | 166 J / 0.315 |
| Pack energy per step down | 42 J | Lowering through a self-locking worm |
| Usable pack energy | 829 kJ | 256 Wh x 90 % |
| Loaded steps per charge, up and down | **1,327** | 829 kJ / ((527 + 42) J x 1.1) |
| Typical day | 28 drops of three floors (48 steps) | |
| Charge time | 3.5 h | 256 Wh / (29.2 V x 3 A x 0.9) plus 0.3 h |

Lowering: a 45 % efficient worm with a 4 degree lead has a friction angle of 4.83 degrees. Driving it while the load pushes needs tan(4.83 minus 4) / tan 4 = 21 % of the lift work at the worm, so the motor supplies 42 J per step down instead of braking.

The energy flow for one step up is 527 J from the pack, 500 J after the driver, 400 J at the motor shaft, 180 J after the worm and 166 J of lift (Figure 2 of SCM-PRC-001). R4 (1,000 steps each way) and R13 (4 h charge) are met. Endurance falls from 1,394 steps in v0.1 because the truck is 2 kg heavier and the drive has a second stage.

## 6. Holding on the stair (R8)

The shaft must hold 128 N·m at the worst point of a step, or 18.3 N·m at the gearmotor output.

- **Worm.** Its back-drive efficiency is 2 minus 1/0.45 = -0.22. A value at or below zero means the worm cannot be driven backwards by the load when static, so it holds without power. Vibration can lower the friction and let a self-locking worm creep; this cannot be checked on paper.
- **Brake.** If the worm were fully back-drivable, the motor brake would need 128 / (75 x 7) = 0.24 N·m. A 2.0 N·m brake gives an 8.2-times margin.

Two independent holds exist on paper. The drift limit in R8 (5 mm in 10 minutes) needs a test and is not verifiable at TRL 3.

## 7. Balance and handle force (R6, R7, R10)

During a step the hub moves relative to the wheel carrying the load: from 29 mm on the stair side of the support wheel to 150 mm on the far side. The frame angle is held, so the center of mass moves with the hub. The best set angle puts the center of mass 61 mm on the stair side of the hub, which leaves a swing of plus or minus 89 mm about the support point (71 mm on the v0.1 cluster). At the edge of the plus or minus 6 degree window the center of mass moves a further 52 mm.

*Table 7. Grip force during a climb on the design stair.*

| Case | Grip force |
| --- | --- |
| At the set angle, worst point of the step | 70 N |
| At the plus or minus 6 degree window edge | **111 N** (R6 not met) |
| Widest window that meets 100 N | Plus or minus 4.4 degrees (100 N) |
| Vertical grip force at the window edge (flat hand truck convention) | 250 N |

The horizontal-force case is the relevant one: the courier stands uphill and pushes or pulls the grip, which is about 1.1 m above the support wheel. **R6 is not met by 11 %.** Tightening the window to plus or minus 6 degrees, as decided, would have met R6 on the v0.1 cluster (99 N at 6.8 degrees) but not on the longer arm. The options are set out as SCM-DDR-002 item 14, proposed, awaiting Amish.

Pushing on the flat takes 0.03 x 847 N = 25 N, which meets R10.

## 8. Structure (R1)

*Table 8. Stresses at the peak torque and a 3 g dropped-step load.*

| Part | Load | Stress | Safety factor on yield |
| --- | --- | --- | --- |
| Shaft, 25 mm | 166 N·m torsion (54 MPa); bending over 48 mm overhang (40 MPa) | 102 MPa von Mises; keyway factor 2 | 1.8 |
| Spider arm, 45 x 6 mm, 150 mm long | 1.27 kN at the wheel: bending 94 MPa; twist from the 30 mm wheel offset 77 MPa | 163 MPa von Mises | 1.7 |
| Frame rail, 28 x 1.5 mm tube | 70 N·m each from the window-edge grip force | 89 MPa | 2.8 |

R1 is met statically. Fatigue of the keyed shaft and the welded frame over many thousands of steps is not assessed here and belongs with a later test.

## 9. Mass and size (R5, R11)

*Table 9. Mass roll-up.*

| Item | Mass |
| --- | --- |
| 1 Frame and toe plate | 8.0 kg |
| 2 Clusters (pair), 200 mm wheels | 5.5 kg |
| 3 Shaft, countershaft, bearings, sprockets, chains, guards | 2.5 kg |
| 4 Worm gearmotor with brake | 4.5 kg |
| 5 and 6 Driver, controller, IMU | 0.8 kg |
| 7 Pack and cradle | 2.6 kg |
| 8 Switch, fuse, harness | 0.5 kg |
| 9 Handle controls | 0.6 kg |
| 10 Strap | 0.4 kg |
| 11 Skids | 0.4 kg |
| 13 Enclosure and hardware | 0.5 kg |
| **Total** | **26.3 kg** |

R5, revised to 27 kg on 2026-09-25, is met with 0.7 kg to spare. From the model, the truck is 569 mm wide at the wheel faces and 1,451 mm tall upright, which meets R11 (1,500 mm). A folding hinge 950 mm above the shaft (the Option C study, not adopted) would fold the truck to 1,139 mm.

## 10. Cost (R12)

The 13 BOM lines total **$633.00** against the $650 budget set on 2026-09-25, a 2.6 % margin. R12 is met. The rework added $23 to the clusters and $30 to the drive.

## 11. Requirement status

*Table 10. Every requirement against the calculations. The status is met, not met or not verifiable at TRL 3.*

| ID | Requirement | Target | Value | Status |
| --- | --- | --- | --- | --- |
| R6 | Operator handle force | 100 N or less inside the tilt window | 111 N at the plus or minus 6 degree edge; 70 N at the set angle | **Not met** |
| R1 | Rated stair load | 60 kg up and down; 100 kg on the flat | Safety factors 1.8 shaft, 1.7 spider, 2.8 rail at 3 g | Met |
| R2 | Stair range | Risers 100 to 200 mm, treads 250 mm or more, nosing up to 32 mm | Landing 66 mm past the nosing at 200 mm; tread needed 240 mm; arms clear 32 mm overhangs | Met |
| R3 | Climb speed | 17 steps/min or more at rated load | 238 W peak on a 250 W motor | Met (5 % margin) |
| R4 | Endurance | 1,000 loaded steps up plus 1,000 down | 1,327 | Met |
| R5 | Truck mass | 27 kg or less; pack 3 kg or less | 26.3 kg; pack 2.6 kg | Met (0.7 kg margin) |
| R10 | Flat rolling | 40 N or less | 25 N | Met |
| R11 | Size | Width 600 mm or less; upright height 1,500 mm or less | 569 mm; 1,451 mm | Met |
| R12 | Affordable | $650 or less | $633 | Met (2.6 % margin) |
| R13 | Battery | 24 V LiFePO4, BMS, fused, 0 to 45 °C charge window, 4 h charge | 3.5 h | Met |
| R15 | Stair and building protection | No steel contact with stairs; skids over nosings | Shaft-line guard 53.9 mm against 54.2 mm allowed; countershaft guard clears by 96 mm | Met |
| R7 | Tilt control | 100 Hz IMU, plus or minus 6 degree window, stop within 0.2 s | Control concept only | Not verifiable at TRL 3 |
| R8 | Hold on any loss | Holds with power off; drift 5 mm or less in 10 min | Worm self-locking; brake margin 8.2 times | Not verifiable at TRL 3 |
| R9 | Hold-to-run | Stops within 0.2 s of grip release | Circuit concept only | Not verifiable at TRL 3 |
| R14 | Environment | 0 to 40 °C, IP54, rain on stoops | Enclosure concept only | Not verifiable at TRL 3 |

Counts: 10 met, 1 not met, 4 not verifiable at TRL 3.

## Safety

> **Safety:** These are paper numbers for an 86 kg load moving on a stair with a person uphill of it. The rework keeps steel parts clear of nosings on paper, but the shaft-line guard sits at the limit of its envelope, so a bent guard or a nosing outside the R2 range could still be struck; a strike mid-step could jerk the frame toward the courier or stall the climb with the load half-lifted. The grip force at the window edge (111 N) is above target. The holding figures in section 6 assume a static load; worm creep under vibration and the brake's real holding torque must be confirmed before anyone climbs with a load. The 3 g shock factor is a judgment, not a measurement.

## References

- SCM-REQ-001 v0.4, requirements.
- SCM-PRC-001 v0.4, design precis.
- SCM-DDR-001, TRL 2 review decisions; SCM-DDR-002, recommendations accepted.
- ISO 606, short-pitch transmission precision roller chains (minimum tensile strengths, confirm with the chain supplier's catalog).
- US International Residential Code, stair riser and tread limits, as summarized in SCM-PRB-001.

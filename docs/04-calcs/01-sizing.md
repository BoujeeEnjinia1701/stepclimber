---
doc_id: SCM-CAL-001
title: StepClimber sizing calculations
project: StepClimber
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (cluster geometry, nosing clearances, torque, energy, holding, handle force, structure, mass, size, cost) with a status for every requirement
---

# StepClimber sizing calculations

On paper, StepClimber meets eight of its fifteen requirements, misses three and leaves four that cannot be verified without hardware. The drive, battery, mass, size and cost targets are met, several with thin margins. **Three requirements are not met.** R15: the 60-tooth driven sprocket and its guard sweep a 104 mm radius around the cluster shaft, but a stair nosing passes within 58 mm of the shaft line during each step, so the guard would strike the nosing by about 46 mm. R2: the straight spider arms clear nosing overhangs only up to 23 mm, not the 32 mm the requirement names. R6: the courier's grip force reaches 107 N at the edge of the plus or minus 8 degree tilt window, against a 100 N limit. The drive and structure otherwise work: 239 W peak motor output on a 250 W motor, about 1,390 loaded steps per charge, an 8-times brake margin and safety factors of 1.8 or more at a 3 g dropped-step load.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates for a paper design; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Payload | 60 kg (132 lb) | R1, decided 2026-09-25 (SCM-DDR-001) |
| Truck mass | 24.3 kg (roll-up in section 9) | Component estimates |
| Combined center of mass | 500 mm above the shaft, along the frame | Parcels stacked on the toe plate |
| Design stair | 196 mm (7.75 in) risers, 254 mm (10 in) treads; nosing overhang 0 to 32 mm | IRC limits; R2 |
| Climb speed | 20 steps/min: one third of a turn in 3 s | R3 |
| Drive efficiencies | Driver 95 %, brushed motor 80 %, self-locking worm 45 %, chain and bearings 95 % | Typical parts |
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

The design load is 84.3 kg in total, a weight of 827 N. The clusters are assumed to carry all of it while lifting, which is conservative.

## 2. Cluster geometry (R2)

The cluster has three 150 mm wheels on 135 mm arms, so the wheel centers are 233.8 mm apart, the shaft sits 142.5 mm above the floor and the cluster is 420 mm across.

A climb starts with the wheel nearest the stair lodged against the riser. The cluster turns about that wheel (the pivot) until the top wheel lands on the tread above, 233.8 mm from the pivot and one riser higher. The landing wheel's contact point is therefore sqrt(*d*² minus *h*²) minus 75 mm past the riser face, plus the nosing overhang. Table 2 shows how far it lands past the nosing edge.

*Table 2. Landing point of the swinging wheel past the nosing edge.*

| Riser | No overhang | 32 mm overhang | Tread needed to land |
| --- | --- | --- | --- |
| 100 mm | 136.4 mm | 140.7 mm | 211.4 mm |
| 150 mm | 104.4 mm | 136.4 mm | 179.4 mm |
| 175 mm | 80.1 mm | 112.1 mm | 155.1 mm |
| 196 mm | 52.5 mm | 84.5 mm | 127.5 mm |
| 200 mm | 46.1 mm | 78.1 mm | 121.1 mm |
| 210 mm | 27.8 mm | 59.8 mm | 102.8 mm |
| 220 mm | 4.2 mm | 36.2 mm | 79.2 mm |
| 241 mm | Cannot climb: riser exceeds the 234 mm wheel spacing | | |

With at least 30 mm of landing past a square nosing, the largest riser the cluster climbs is 209 mm, which covers the 100 to 200 mm range of R2. Every tread of 250 mm or more is long enough. The TRL 2 precis quoted 16 mm of landing at a 220 mm riser; the correct figure is 4 mm, so 220 mm risers are out of range, as the precis concluded.

After the landing, the cluster turns on about the landed wheel for the rest of the third of a turn, which lifts the old pivot wheel clear, and the courier rolls the truck back on the landed wheel to the next riser (about 126 mm on the design stair).

## 3. Nosing clearances (R2, R15)

This is the main finding of the note. The script steps the cluster through a full climb in 2D and records how close the hub, the spider arms and the wheels come to the nosing corners.

*Table 3. Closest approach to a nosing during one step.*

| Riser | Overhang | Hub to nosing | Spider arm clearance | Wheel clearance |
| --- | --- | --- | --- | --- |
| 100 mm | 0 | 86.0 mm | 25.0 mm | 4.1 mm |
| 100 mm | 32 mm | 86.2 mm | 21.4 mm | 0.0 mm |
| 125 mm | 0 | 70.6 mm | 20.7 mm | 15.1 mm |
| 125 mm | 32 mm | 69.9 mm | 3.8 mm | -1.5 mm |
| 150 mm | 0 | 59.2 mm | 22.2 mm | 30.3 mm |
| 150 mm | 32 mm | 51.9 mm | **-7.9 mm** | 3.2 mm |
| 175 mm | 0 | 57.8 mm | 23.3 mm | 33.8 mm |
| 175 mm | 32 mm | **36.0 mm** | -0.4 mm | 24.0 mm |
| 196 mm | 0 | 69.2 mm | 20.6 mm | 16.5 mm |
| 196 mm | 32 mm | 38.4 mm | 6.0 mm | 30.4 mm |
| 200 mm | 0 | 72.9 mm | 21.0 mm | 13.1 mm |
| 200 mm | 32 mm | 41.4 mm | 5.6 mm | 26.6 mm |

The nosing passes through the gap between the two lower arms, close to the shaft line, at the moment the swinging wheel lands. Anything on the shaft line (sprocket, guard, bearing housings, spider bosses) must therefore stay within the minimum hub-to-nosing distance less a 10 mm margin: **48 mm radius with square nosings and 26 mm with 32 mm overhangs**.

- The 25 mm shaft clears.
- The 38 mm spider bosses and 45 mm flange bearing housings clear square nosings but strike nosings with 32 mm overhang.
- **The 60-tooth 06B driven sprocket (187 mm across) and its guard (104 mm radius) strike every nosing, by about 46 mm with square nosings.** R15 is not met. This confirms the TRL 2 open question on sprocket clearance.
- **The straight 45 mm spider arms clear overhangs only up to 23 mm** and strike a 32 mm overhang by 7.9 mm on a 150 mm riser. R2 is not met for its full overhang range. The wheels touching a nosing briefly (clearance near zero or slightly negative) is acceptable: they are rubber and roll over it.
- The frame back clears the nosings above the shaft region by 88 mm beyond the skid face at the 30 degree climbing tilt.

A smaller final sprocket alone cannot fix R15: with square nosings a 48 mm envelope leaves room for a 9-tooth 06B sprocket, far too small for the torque. A larger cluster moves the hub away from the nosing. Table 4 compares options.

*Table 4. Alternative cluster sizes (hub to nosing and arm clearance with square and 32 mm nosings).*

| Arm | Wheel | Hub to nosing | Arm clearance | Landing at 200 mm riser | Tread needed at 100 mm | Hub height |
| --- | --- | --- | --- | --- | --- | --- |
| 135 mm | 150 mm | 58 / 36 mm | 21 / -8 mm | 46 mm | 211 mm | 142 mm |
| 135 mm | 200 mm | 93 / 70 mm | 54 / 29 mm | 21 mm | 211 mm | 168 mm |
| 150 mm | 150 mm | 52 / 29 mm | 14 / -15 mm | 91 mm | 240 mm | 150 mm |
| 150 mm | 200 mm | 87 / 64 mm | 47 / 20 mm | 66 mm | 240 mm | 175 mm |
| 165 mm | 200 mm | 81 / 64 mm | 42 / 12 mm | 104 mm | 268 mm | 182 mm |

Bigger wheels help most, because they hold the pivot farther from the riser and higher. The 150 mm arm with 200 mm wheels clears 32 mm overhangs, lands 66 mm past a 200 mm riser, fits 250 mm treads and allows a 54 mm shaft-line envelope. At the higher torque of the longer arm (163 N·m, below), that envelope takes an 08B 20-tooth sprocket (88 mm across, chain pull 4.0 kN, safety factor 4.4) or a 06B 27-tooth sprocket (safety factor 2.2, too low). Because the final stage is then only about 2:1, the drive needs a second chain stage. The longer arm also raises the peak shaft torque to 163 N·m and the motor output to 266 W at 20 steps/min, or 18.8 steps/min on the 250 W motor. This rework is proposed, awaiting Amish (see SCM-DDR-001); the model and BOM stay at the TRL 2 baseline.

## 4. Torque, speed and power (R3)

The shaft turns at 0.698 rad/s (6.67 rpm). Lifting 827 N through 196 mm takes 162 J per step, a mean shaft torque of 77 N·m over a third of a turn.

The drive torque at any instant equals the vertical load times the horizontal distance from the support wheel to the hub, plus the grip force times the vertical distance. The peak is 113 N·m static, when the hub passes level with the landed wheel (the full 135 mm arm), and 146 N·m with the 1.3 dynamics factor. That needs 102 W at the shaft and **239 W from the motor**, 4 % under its 250 W rating. R3 is met with a thin margin; a brushed motor carries this briefly, since the peak lasts a fraction of each step.

The 6:1 chain drive needs the gearmotor to give 40 rpm and 25.7 N·m, inside its 30 N·m rating. The 06B chain pulls 1,608 N at the peak, a safety factor of 5.5 on its minimum tensile strength.

## 5. Energy and endurance (R4, R13)

*Table 5. Energy per loaded step on the design stair.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Drive efficiency up | 32.5 % | 0.95 x 0.80 x 0.45 x 0.95 |
| Pack energy per step up | 499 J (0.14 Wh) | 162 J / 0.325 |
| Pack energy per step down | 42 J | Lowering through a self-locking worm |
| Usable pack energy | 829 kJ | 256 Wh x 90 % |
| Loaded steps per charge, up and down | **1,394** | 829 kJ / ((499 + 42) J x 1.1) |
| Typical day | 29 drops of three floors (48 steps) | |
| Charge time | 3.5 h | 256 Wh / (29.2 V x 3 A x 0.9) plus 0.3 h |

Lowering: a 45 % efficient worm with a 4 degree lead has a friction angle of 4.83 degrees. Driving it while the load pushes needs tan(4.83 minus 4) / tan 4 = 21 % of the lift work at the worm, so the motor supplies 42 J per step down instead of braking. The TRL 2 estimate of about 60 J was high.

The energy flow for one step up is 499 J from the pack, 474 J after the driver, 379 J at the motor shaft, 171 J after the worm and 162 J of lift (Figure 2 of SCM-PRC-001). R4 (1,000 steps each way) and R13 (4 h charge) are met.

## 6. Holding on the stair (R8)

The shaft must hold 113 N·m at the worst point of a step, or 18.8 N·m at the gearmotor output.

- **Worm.** Its back-drive efficiency is 2 minus 1/0.45 = -0.22. A value at or below zero means the worm cannot be driven backwards by the load when static, so it holds without power. Vibration can lower the friction and let a self-locking worm creep; this cannot be checked on paper.
- **Brake.** If the worm were fully back-drivable, the motor brake would need 113 / (75 x 6) = 0.25 N·m. A 2.0 N·m brake gives an 8.0-times margin.

Two independent holds exist on paper. The drift limit in R8 (5 mm in 10 minutes) needs a test and is not verifiable at TRL 3.

## 7. Balance and handle force (R6, R7, R10)

During a step the hub moves relative to the wheel carrying the load: from 117 mm on the far side of the pivot at the start, to 7 mm on the stair side at the landing, then to 135 mm on the far side while the cluster turns about the landed wheel. The frame angle is held, so the center of mass moves with the hub. The best set angle puts the center of mass 64 mm on the stair side of the hub, which leaves a swing of plus or minus 71 mm about the support point. At the edge of the plus or minus 8 degree window the center of mass moves a further 70 mm.

*Table 6. Grip force during a climb on the design stair.*

| Case | Grip force |
| --- | --- |
| At the set angle, worst point of the step | 54 N |
| At the plus or minus 8 degree window edge | **107 N** (R6 not met) |
| Widest window that meets 100 N | Plus or minus 6.8 degrees (99 N) |
| Vertical grip force at the window edge (flat hand truck convention) | 235 N |

The horizontal-force case is the relevant one: the courier stands uphill and pushes or pulls the grip, which is about 1.1 m above the support wheel. The vertical case shows why a courier should not try to lift the truck over the step. The TRL 2 figure of 91 N ignored the shift of the support point during a step. **R6 is not met by 7 %.** Tightening the stop window to plus or minus 6 degrees would meet it; that changes R7 and is proposed, awaiting Amish.

Pushing on the flat takes 0.03 x 827 N = 25 N, which meets R10.

## 8. Structure (R1)

*Table 7. Stresses at the peak torque and a 3 g dropped-step load.*

| Part | Load | Stress | Safety factor on yield |
| --- | --- | --- | --- |
| Shaft, 25 mm | 146 N·m torsion (48 MPa); bending over 48 mm overhang (39 MPa) | 91 MPa von Mises; keyway factor 2 | 2.0 |
| Spider arm, 45 x 6 mm | 1.24 kN at the wheel: bending 83 MPa; twist from the 30 mm wheel offset 75 MPa | 154 MPa von Mises | 1.8 |
| Frame rail, 28 x 1.5 mm tube | 68 N·m each from the window-edge grip force | 86 MPa | 2.9 |

R1 is met statically. Fatigue of the keyed shaft and the welded frame over many thousands of steps is not assessed here and belongs with a later test.

## 9. Mass and size (R5, R11)

*Table 8. Mass roll-up.*

| Item | Mass |
| --- | --- |
| 1 Frame and toe plate | 8.0 kg |
| 2 Clusters (pair) | 4.0 kg |
| 3 Shaft, bearings, sprockets, chain, guard | 2.0 kg |
| 4 Worm gearmotor with brake | 4.5 kg |
| 5 and 6 Driver, controller, IMU | 0.8 kg |
| 7 Pack and cradle | 2.6 kg |
| 8 Switch, fuse, harness | 0.5 kg |
| 9 Handle controls | 0.6 kg |
| 10 Strap | 0.4 kg |
| 11 Skids | 0.4 kg |
| 13 Enclosure and hardware | 0.5 kg |
| **Total** | **24.3 kg** |

R5 (25 kg) is met with 0.7 kg to spare; the rework in section 3 would likely exceed it. From the model, the truck is 569 mm wide at the wheel faces and 1,418 mm tall upright, which meets R11 as relaxed to 1,500 mm on 2026-09-25. The folding handle studied as Option C, with a hinge 950 mm above the shaft, would fold the truck to 1,106 mm for about 0.4 kg and $20 more (indicative); it is not in the baseline.

## 10. Cost (R12)

The 13 BOM lines total **$580.00** against the $600 budget, a 3.3 % margin. R12 is met.

## 11. Requirement status

*Table 9. Every requirement against the calculations. The status is met, not met, at risk or not verifiable at TRL 3.*

| ID | Requirement | Target | Value | Status |
| --- | --- | --- | --- | --- |
| R2 | Stair range | Risers 100 to 200 mm, treads 250 mm or more, nosing up to 32 mm | Landing 46 mm past the nosing at 200 mm; arms clear nosings only up to 23 mm overhang | **Not met** |
| R6 | Operator handle force | 100 N or less inside the tilt window | 107 N at the plus or minus 8 degree edge; 54 N at the set angle | **Not met** |
| R15 | Stair and building protection | No steel contact with stairs; skids over nosings | 60T sprocket guard radius 104 mm against 48 mm allowed | **Not met** |
| R1 | Rated stair load | 60 kg up and down; 100 kg on the flat | Safety factors 2.0 shaft, 1.8 spider, 2.9 rail at 3 g | Met |
| R3 | Climb speed | 20 steps/min or more at rated load | 239 W peak on a 250 W motor | Met (4 % margin) |
| R4 | Endurance | 1,000 loaded steps up plus 1,000 down | 1,394 | Met |
| R5 | Truck mass | 25 kg or less; pack 3 kg or less | 24.3 kg; pack 2.6 kg | Met (0.7 kg margin) |
| R10 | Flat rolling | 40 N or less | 25 N | Met |
| R11 | Size | Width 600 mm or less; upright height 1,500 mm or less | 569 mm; 1,418 mm | Met |
| R12 | Affordable | $600 or less | $580 | Met (3.3 % margin) |
| R13 | Battery | 24 V LiFePO4, BMS, fused, 0 to 45 °C charge window, 4 h charge | 3.5 h | Met |
| R7 | Tilt control | 100 Hz IMU, window, stop within 0.2 s | Control concept only | Not verifiable at TRL 3 |
| R8 | Hold on any loss | Holds with power off; drift 5 mm or less in 10 min | Worm self-locking; brake margin 8.0 times | Not verifiable at TRL 3 |
| R9 | Hold-to-run | Stops within 0.2 s of grip release | Circuit concept only | Not verifiable at TRL 3 |
| R14 | Environment | 0 to 40 °C, IP54, rain on stoops | Enclosure concept only | Not verifiable at TRL 3 |

Counts: 8 met, 3 not met, 4 not verifiable at TRL 3.

## Safety

> **Safety:** These are paper numbers for an 84 kg load moving on a stair with a person uphill of it. The nosing strike found in section 3 matters for safety as well as for the stairs: a guard or boss catching a nosing mid-step could jerk the frame toward the courier or stall the climb with the load half-lifted. The holding figures in section 6 assume a static load; worm creep under vibration and the brake's real holding torque must be confirmed before anyone climbs with a load. The 3 g shock factor is a judgment, not a measurement.

## References

- SCM-REQ-001 v0.3, requirements.
- SCM-PRC-001 v0.3, design precis.
- SCM-DDR-001, TRL 2 review decisions.
- ISO 606, short-pitch transmission precision roller chains (minimum tensile strengths, confirm with the chain supplier's catalog).
- US International Residential Code, stair riser and tread limits, as summarized in SCM-PRB-001.

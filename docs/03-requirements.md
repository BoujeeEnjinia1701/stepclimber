---
doc_id: SCM-REQ-001
title: StepClimber requirements
project: StepClimber
doc_type: Requirements
version: "0.7"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions (R1 rating, R11 relaxed to 1,500 mm, R12 budget kept); status against SCM-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); R3, R5, R7 and R12 revised; status against SCM-CAL-001 v0.2
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status against SCM-CAL-001 v0.5 for the constructable design (SCM-DDR-003); R3 and R5 now not met; R12 reported against the value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: R3 (16 steps/min) and R5 (35 kg) set for the first prototype, and the R7 tilt window tightened to plus or minus 3 degrees for the first loaded trials, by Amish on 2026-10-02 (SCM-DEC-001, items 2 to 4); R3, R5 and R6 met on paper
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: Status against SCM-CAL-001 v0.5, recalculated with the approved targets and the 4140 cluster shaft (fatigue assessed); R12 USD 138 over the target after the shaft repricing
---

# StepClimber requirements

These requirements are checked by calculation in SCM-CAL-001 v0.5, which models the constructable design of SCM-DDR-003 (2026-10-01) on the cluster and drive Amish decided on 2026-09-25 (SCM-DDR-002). On paper, ten are met and four cannot be verified without hardware, after Amish's decisions of 2026-10-02 (SCM-DEC-001): R5 is 35 kg and R3 16 steps/min for the first prototype, and the tilt window is plus or minus 3 degrees for the first loaded trials, which brings R6 within 100 N. Before those decisions R3, R5 and R6 were not met; R12 is reported against the value-engineering target. Targets are still to be revised after user research (see SCM-PRB-001). Decisions are recorded in SCM-DDR-001 to SCM-DDR-003 and indexed in the design decisions register SCM-DEC-001.

The **design load case** is a 60 kg (132 lb) payload on a 34.2 kg truck, 94.2 kg in total, climbing a residential stair with 196 mm (7.75 in) risers and 254 mm (10 in) treads, the steepest the US residential code allows.

*Table 1. Requirements and status at TRL 3.*

| ID | Requirement | Target | Status at TRL 3 (SCM-CAL-001 v0.5) | Verification (later) |
| --- | --- | --- | --- | --- |
| R1 | Rated stair load | 60 kg (132 lb) payload up and down stairs; 100 kg on the flat. Rating decided by Amish, 2026-09-25 | Met: safety factors 2.5 (4140 shaft), 1.5 (spider), 3.2 (rail) at a 3 g dropped-step load; shaft fatigue factor 1.8; fatigue of the welded frame not assessed | Proof load |
| R2 | Stair range | Straight flights with risers 100 to 200 mm, treads 250 mm or more and nosing overhang up to 32 mm | Met: lands 66 mm past a square nosing at a 200 mm riser (climbs to 225 mm), needs 240 mm of tread at most, and the arms clear 32 mm overhangs | Stair survey; trial climbs |
| R3 | Climb speed | 16 steps/min or more, up and down, at rated load, for the first prototype. Set by Amish on 2026-10-02 (SCM-DEC-001, item 3); revised from 20 to 17 steps/min on 2026-09-25 (SCM-DDR-002) | Met on paper: the climb needs 244 W from the 250 W motor, which gives at most 16.4 steps/min at the 34.2 kg constructable mass (260 W for 17) | Timed climb |
| R4 | Endurance | 1,000 or more loaded steps up plus 1,000 down per charge | Met: 1,215 | Logged use |
| R5 | Truck mass | 35 kg or less with battery for the first prototype; battery removable and 3 kg or less. Set by Amish on 2026-10-02 (SCM-DEC-001, item 2); revised from 25 to 27 kg on 2026-09-25 (SCM-DDR-002) | Met on paper: 34.2 kg (pack 2.6 kg); weighed at TRL 4, with savings tried when parts are bought | Weighing |
| R6 | Operator handle force | 100 N or less at the grip while climbing inside the tilt window (R7) | Met on paper with the plus or minus 3 degree window of R7 for the first loaded trials (99 N at the edge; plus or minus 3.1 degrees gives 99 N too); 121 N at a plus or minus 6 degree edge; 76 N at the set angle. Decided by Amish on 2026-10-02 (SCM-DEC-001, item 4) | Force gauge |
| R7 | Tilt control | IMU measures frame angle at 100 Hz or faster; the controller stores the balance angle when a climb starts, shapes motor speed to keep the angle within plus or minus 3 degrees of it for the first loaded trials, and stops and alerts within 0.2 s if the angle leaves that window or the range 15 to 45 degrees back from vertical. The window is widened toward plus or minus 6 degrees only when grip force is measured at 100 N or less, or operators are shown to handle the measured force safely. Set by Amish on 2026-10-02 (SCM-DEC-001, item 4); tightened from 8 to 6 degrees on 2026-09-25 (SCM-DDR-002) | Not verifiable at TRL 3 (control concept only) | Bench test |
| R8 | Hold on any loss | Load holds on the stair with power off, grip released, battery removed or any fault; drift 5 mm or less in 10 min at rated load | Not verifiable at TRL 3: worm statically self-locking (back-drive efficiency -0.22) and brake margin 7.5 times, but drift needs a test | Hold test |
| R9 | Hold-to-run | Motion only while the dead-man grip is held and a direction is selected; release stops the clusters within 0.2 s | Not verifiable at TRL 3 (circuit concept only) | Bench test |
| R10 | Flat rolling | Push force 40 N or less at rated load on a smooth floor at walking pace, with the clusters parked | Met: 28 N | Pull test |
| R11 | Size | Overall width 600 mm or less; upright height 1,500 mm or less with a fixed handle. Height relaxed from 1,300 mm by Amish, 2026-09-25 | Met: 569 mm wide at the wheel faces, 588 mm over the wheel end screws, 1,451 mm tall (model) | Model check; measurement |
| R12 | Affordable | Parts cost for one prototype, charger included, against the value-engineering target of USD 650 (`budget_usd`, a hypothetical control target set 2026-09-25, SCM-DDR-002) | Estimated cost of the constructable design USD 788: USD 138 over the value-engineering target | Priced BOM (`bom/bom.csv`) |
| R13 | Battery | 24 V class LiFePO4 with BMS and fused output; charging blocked below 0 °C and above 45 °C; full charge in 4 h or less | Met: 3.5 h; protections by specification | Datasheets |
| R14 | Environment | Operate from 0 to 40 °C; electronics IP54 or better; survive rain on outdoor stoops | Not verifiable at TRL 3 (enclosure concept only) | Spray test |
| R15 | Stair and building protection | No steel contact with stairs or walls in normal use; non-marking wheels; skids over stair nosings | Met: the chain case sweeps 53.9 mm on the shaft line against the 54.2 mm that 32 mm nosings leave free; the countershaft guard clears nosings by 80 mm; every frame-fixed outline near the shaft clears every nosing by 10 mm or more | Model check; trial climbs |

## Requirements not met or at risk

- **R5** was not met against 27 kg, by 7.2 kg; it is met against the 35 kg set for the first prototype on 2026-10-02, with 0.8 kg to spare on estimated masses. Making the design buildable named every part: the drive, carried at TRL 3 as a 2.5 kg allowance, weighs 5.5 kg itemised, and the axle plates, chain case, stub axles, uprights, standoffs and fixings add 4.4 kg (SCM-DDR-003). The savings in SCM-DDR-003 item A1 are to be tried when parts are bought.
- **R3** was not met by 4 % at 17 steps/min (260 W needed from a 250 W motor); it is met at the 16 steps/min set for the first prototype on 2026-10-02, needing 244 W from the 250 W motor (a 2 % margin).
- **R6** is met on paper only with the plus or minus 3 degree window set on 2026-10-02 for the first loaded trials; at plus or minus 6 degrees it is 21 % over (121 N). A tight window may cause frequent stops on uneven stairs; it is widened only after grip force is measured.
- **R15 is met with no spare radius:** the chain case is sized to its envelope on the shaft line (10.3 mm from the nearest nosing against 10 mm wanted). A bent case or a stair outside the R2 range could still be struck.
- **R12:** the estimated cost is USD 138 over the USD 650 value-engineering target (the 4140 cluster shaft added USD 12); the main cost drivers are in SCM-DEC-001.
- R7, R8, R9 and R14 depend on control, brake and enclosure behavior that needs hardware to verify.

## Assumptions

- Payload 60 kg; truck 34.2 kg (mass roll-up in SCM-CAL-001 v0.5); total 94.2 kg.
- The clusters carry the whole weight while lifting (conservative; the operator's grip carries some in practice).
- Center of mass about 500 mm above the cluster shaft; frame tilted about 30 degrees back while climbing.
- The courier stands uphill and pushes or pulls the grip horizontally while climbing.
- Drive efficiencies: motor driver 95 %, brushed motor 80 %, self-locking worm 45 %, first chain stage and bearings 95 %, second chain stage 97 %.
- Rolling resistance coefficient about 0.03 for solid rubber wheels on a smooth floor.
- Stair geometry from the US International Residential Code (196 mm maximum riser, 254 mm minimum tread); national and local codes vary.

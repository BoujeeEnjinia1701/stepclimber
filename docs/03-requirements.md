---
doc_id: SCM-REQ-001
title: StepClimber requirements
project: StepClimber
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-09-25'
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
---

# StepClimber requirements

These requirements are checked by calculation in SCM-CAL-001 v0.2, which models the cluster and drive rework Amish decided on 2026-09-25 (SCM-DDR-002). On paper, ten are met, one is not met (R6) and four cannot be verified without hardware. Targets are still to be revised after user research (see SCM-PRB-001). Decisions are recorded in SCM-DDR-001 and SCM-DDR-002.

The **design load case** is a 60 kg (132 lb) payload on a 26.3 kg truck, 86.3 kg in total, climbing a residential stair with 196 mm (7.75 in) risers and 254 mm (10 in) treads, the steepest the US residential code allows.

*Table 1. Requirements and status at TRL 3.*

| ID | Requirement | Target | Status at TRL 3 (SCM-CAL-001 v0.2) | Verification (later) |
| --- | --- | --- | --- | --- |
| R1 | Rated stair load | 60 kg (132 lb) payload up and down stairs; 100 kg on the flat. Rating decided by Amish, 2026-09-25 | Met: safety factors 1.8 (shaft), 1.7 (spider), 2.8 (rail) at a 3 g dropped-step load; fatigue not assessed | Proof load |
| R2 | Stair range | Straight flights with risers 100 to 200 mm, treads 250 mm or more and nosing overhang up to 32 mm | Met: lands 66 mm past a square nosing at a 200 mm riser (climbs to 225 mm), needs 240 mm of tread at most, and the arms clear 32 mm overhangs | Stair survey; trial climbs |
| R3 | Climb speed | 17 steps/min or more, up and down, at rated load. Revised from 20 steps/min by Amish, 2026-09-25 (SCM-DDR-002) | Met: 238 W peak motor output on a 250 W motor (5 % margin) | Timed climb |
| R4 | Endurance | 1,000 or more loaded steps up plus 1,000 down per charge | Met: 1,327 | Logged use |
| R5 | Truck mass | 27 kg or less with battery; battery removable and 3 kg or less. Revised from 25 kg by Amish, 2026-09-25 (SCM-DDR-002) | Met: 26.3 kg, pack 2.6 kg (0.7 kg margin) | Weighing |
| R6 | Operator handle force | 100 N or less at the grip while climbing inside the tilt window (R7) | **Not met:** 111 N at the plus or minus 6 degree window edge; 70 N at the set angle. Options in SCM-DDR-002 item 14, proposed, awaiting Amish | Force gauge |
| R7 | Tilt control | IMU measures frame angle at 100 Hz or faster; the controller stores the balance angle when a climb starts, shapes motor speed to keep the angle within plus or minus 6 degrees of it, and stops and alerts within 0.2 s if the angle leaves that window or the range 15 to 45 degrees back from vertical. Window tightened from 8 degrees by Amish, 2026-09-25 (SCM-DDR-002) | Not verifiable at TRL 3 (control concept only) | Bench test |
| R8 | Hold on any loss | Load holds on the stair with power off, grip released, battery removed or any fault; drift 5 mm or less in 10 min at rated load | Not verifiable at TRL 3: worm statically self-locking (back-drive efficiency -0.22) and brake margin 8.2 times, but drift needs a test | Hold test |
| R9 | Hold-to-run | Motion only while the dead-man grip is held and a direction is selected; release stops the clusters within 0.2 s | Not verifiable at TRL 3 (circuit concept only) | Bench test |
| R10 | Flat rolling | Push force 40 N or less at rated load on a smooth floor at walking pace, with the clusters parked | Met: 25 N | Pull test |
| R11 | Size | Overall width 600 mm or less; upright height 1,500 mm or less with a fixed handle. Height relaxed from 1,300 mm by Amish, 2026-09-25 | Met: 569 mm wide, 1,451 mm tall (model) | Model check; measurement |
| R12 | Affordable | Parts cost $650 or less for one prototype, charger included. Budget revised from $600 by Amish, 2026-09-25 (SCM-DDR-002) | Met: $633 (2.6 % margin) | Priced BOM (`bom/bom.csv`) |
| R13 | Battery | 24 V class LiFePO4 with BMS and fused output; charging blocked below 0 °C and above 45 °C; full charge in 4 h or less | Met: 3.5 h; protections by specification | Datasheets |
| R14 | Environment | Operate from 0 to 40 °C; electronics IP54 or better; survive rain on outdoor stoops | Not verifiable at TRL 3 (enclosure concept only) | Spray test |
| R15 | Stair and building protection | No steel contact with stairs or walls in normal use; non-marking wheels; skids over stair nosings | Met: the shaft-line guard sweeps 53.9 mm against the 54.2 mm that 32 mm nosings leave free; the countershaft guard clears nosings by 96 mm | Model check; trial climbs |

## Requirements not met or at risk

- **R6 is not met** by 11 % at the plus or minus 6 degree window edge. The longer 150 mm arm widens the swing of the load about its support wheel, so the tighter window decided on 2026-09-25 is not enough on its own. Options (relax R6 to 115 N, tighten the window to plus or minus 4 degrees, or lengthen the handle) are proposed, awaiting Amish (SCM-DDR-002 item 14).
- **R15 is met with no spare radius:** the shaft-line guard is sized to its envelope. A bent guard or a stair outside the R2 range could still be struck.
- **R3, R5 and R12 have thin margins** (5 %, 0.7 kg and 2.6 %) against their revised targets.
- R7, R8, R9 and R14 depend on control, brake and enclosure behavior that needs hardware to verify.

## Assumptions

- Payload 60 kg; truck 26.3 kg (mass roll-up in SCM-CAL-001); total 86.3 kg.
- The clusters carry the whole weight while lifting (conservative; the operator's grip carries some in practice).
- Center of mass about 500 mm above the cluster shaft; frame tilted about 30 degrees back while climbing.
- The courier stands uphill and pushes or pulls the grip horizontally while climbing.
- Drive efficiencies: motor driver 95 %, brushed motor 80 %, self-locking worm 45 %, first chain stage and bearings 95 %, second chain stage 97 %.
- Rolling resistance coefficient about 0.03 for solid rubber wheels on a smooth floor.
- Stair geometry from the US International Residential Code (196 mm maximum riser, 254 mm minimum tread); national and local codes vary.

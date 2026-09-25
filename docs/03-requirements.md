---
doc_id: SCM-REQ-001
title: StepClimber requirements
project: StepClimber
doc_type: Requirements
version: "0.3"
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
---

# StepClimber requirements

These requirements are checked by calculation in SCM-CAL-001 v0.1. On paper, eight are met, three are not met (R2, R6 and R15) and four cannot be verified without hardware. Targets are still to be revised after user research (see SCM-PRB-001). Decisions recorded on 2026-09-25 are in SCM-DDR-001.

The **design load case** is a 60 kg (132 lb) payload on a 24.3 kg truck, 84.3 kg in total, climbing a residential stair with 196 mm (7.75 in) risers and 254 mm (10 in) treads, the steepest the US residential code allows.

*Table 1. Requirements and status at TRL 3.*

| ID | Requirement | Target | Status at TRL 3 (SCM-CAL-001) | Verification (later) |
| --- | --- | --- | --- | --- |
| R1 | Rated stair load | 60 kg (132 lb) payload up and down stairs; 100 kg on the flat. Rating decided by Amish, 2026-09-25 | Met: safety factors 2.0 (shaft), 1.8 (spider), 2.9 (rail) at a 3 g dropped-step load; fatigue not assessed | Proof load |
| R2 | Stair range | Straight flights with risers 100 to 200 mm, treads 250 mm or more and nosing overhang up to 32 mm | **Not met:** the cluster climbs risers up to 209 mm and fits 250 mm treads, but the straight spider arms clear nosing overhangs only up to 23 mm | Stair survey; trial climbs |
| R3 | Climb speed | 20 steps/min or more, up and down, at rated load | Met: 239 W peak motor output on a 250 W motor (4 % margin) | Timed climb |
| R4 | Endurance | 1,000 or more loaded steps up plus 1,000 down per charge | Met: 1,394 | Logged use |
| R5 | Truck mass | 25 kg or less with battery; battery removable and 3 kg or less | Met: 24.3 kg, pack 2.6 kg (0.7 kg margin) | Weighing |
| R6 | Operator handle force | 100 N or less at the grip while climbing inside the tilt window (R7) | **Not met:** 107 N at the plus or minus 8 degree window edge; 54 N at the set angle | Force gauge |
| R7 | Tilt control | IMU measures frame angle at 100 Hz or faster; the controller stores the balance angle when a climb starts, shapes motor speed to keep the angle within plus or minus 8 degrees of it, and stops and alerts within 0.2 s if the angle leaves that window or the range 15 to 45 degrees back from vertical | Not verifiable at TRL 3 (control concept only). A window of plus or minus 6 degrees would meet R6; proposed, awaiting Amish | Bench test |
| R8 | Hold on any loss | Load holds on the stair with power off, grip released, battery removed or any fault; drift 5 mm or less in 10 min at rated load | Not verifiable at TRL 3: worm statically self-locking (back-drive efficiency -0.22) and brake margin 8.0 times, but drift needs a test | Hold test |
| R9 | Hold-to-run | Motion only while the dead-man grip is held and a direction is selected; release stops the clusters within 0.2 s | Not verifiable at TRL 3 (circuit concept only) | Bench test |
| R10 | Flat rolling | Push force 40 N or less at rated load on a smooth floor at walking pace, with the clusters parked | Met: 25 N | Pull test |
| R11 | Size | Overall width 600 mm or less; upright height 1,500 mm or less with a fixed handle. Height relaxed from 1,300 mm by Amish, 2026-09-25 | Met: 569 mm wide, 1,418 mm tall (model) | Model check; measurement |
| R12 | Affordable | Parts cost $600 or less for one prototype, charger included. Budget kept at $600 by Amish, 2026-09-25 | Met: $580 (3.3 % margin) | Priced BOM (`bom/bom.csv`) |
| R13 | Battery | 24 V class LiFePO4 with BMS and fused output; charging blocked below 0 °C and above 45 °C; full charge in 4 h or less | Met: 3.5 h; protections by specification | Datasheets |
| R14 | Environment | Operate from 0 to 40 °C; electronics IP54 or better; survive rain on outdoor stoops | Not verifiable at TRL 3 (enclosure concept only) | Spray test |
| R15 | Stair and building protection | No steel contact with stairs or walls in normal use; non-marking wheels; skids over stair nosings | **Not met:** the 60-tooth sprocket guard (104 mm radius) strikes nosings, which pass within 58 mm of the shaft line; limit 48 mm | Model check; trial climbs |

## Requirements not met or at risk

- **R15 is not met.** Anything on the cluster shaft line must stay within a 48 mm radius (26 mm with 32 mm nosing overhangs). The baseline sprocket and guard reach 104 mm. A cluster and drive rework is proposed, awaiting Amish (SCM-DDR-001 item 11).
- **R2 is not met** for nosing overhangs above 23 mm; the same rework fixes it.
- **R6 is not met** by 7 % at the tilt window edge. Tightening the window to plus or minus 6 degrees is proposed, awaiting Amish (SCM-DDR-001 item 12).
- **R3, R5 and R12 have thin margins** (4 %, 0.7 kg and 3.3 %). The proposed rework would likely take R5 and R12 past their limits and R3 below 20 steps/min on the present motor.
- R7, R8, R9 and R14 depend on control, brake and enclosure behavior that needs hardware to verify.

## Assumptions

- Payload 60 kg; truck 24.3 kg (mass roll-up in SCM-CAL-001); total 84.3 kg.
- The clusters carry the whole weight while lifting (conservative; the operator's grip carries some in practice).
- Center of mass about 500 mm above the cluster shaft; frame tilted about 30 degrees back while climbing.
- The courier stands uphill and pushes or pulls the grip horizontally while climbing.
- Drive efficiencies: motor driver 95 %, brushed motor 80 %, self-locking worm 45 %, chain and bearings 95 %.
- Rolling resistance coefficient about 0.03 for solid rubber wheels on a smooth floor.
- Stair geometry from the US International Residential Code (196 mm maximum riser, 254 mm minimum tread); national and local codes vary.

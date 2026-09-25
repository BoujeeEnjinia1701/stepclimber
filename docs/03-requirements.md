---
doc_id: SCM-REQ-001
title: StepClimber requirements
project: StepClimber
doc_type: Requirements
version: "0.2"
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
---

# StepClimber requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with couriers, and will be checked by calculation at TRL 3 and revised after user research (see SCM-PRB-001). The status column compares each target with the first-order estimates in SCM-PRC-001; no requirement has been verified.

The **design load case** is a 60 kg (132 lb) payload on a truck of about 24 kg, about 84 kg in total, climbing a residential stair with 196 mm (7.75 in) risers and 254 mm (10 in) treads, the steepest the US residential code allows.

| ID | Requirement | Target | Status at TRL 2 | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Rated stair load | 60 kg (132 lb) payload up and down stairs; 100 kg on the flat | By design; structure unverified | Load and torque calculation; later proof load |
| R2 | Stair range | Straight flights with risers 100 to 200 mm, treads 250 mm or more and nosing overhang up to 32 mm | **At risk.** Fixed tri-star geometry; stairs steeper than this (for example 241 mm industrial risers) are **not** covered | Cluster geometry study against a stair survey |
| R3 | Climb speed | 20 steps/min or more, up and down, at rated load | Met on power estimate (about 236 W peak motor output against 250 W rated); thin margin | Drive calculation; later timed climb |
| R4 | Endurance | 1,000 or more loaded steps up plus 1,000 down per charge | Met on estimate (about 1,300) | Energy calculation; later logged use |
| R5 | Truck mass | 25 kg or less with battery; battery removable and 3 kg or less | Met on estimate (about 24.3 kg, pack about 2.6 kg); thin margin | Mass roll-up; later weighing |
| R6 | Operator handle force | 100 N or less at the grip while climbing inside the tilt window (R7) | Met on estimate (about 91 N at the window edge) | Static balance calculation; later force gauge |
| R7 | Tilt control | IMU measures frame angle at 100 Hz or faster; the controller stores the balance angle when a climb starts, shapes motor speed to keep the angle within plus or minus 8 degrees of it, and stops and alerts within 0.2 s if the angle leaves that window or the range 15 to 45 degrees back from vertical | Concept only; unverified | Control design review; later bench test |
| R8 | Hold on any loss | Load holds on the stair with power off, grip released, battery removed or any fault; drift 5 mm or less in 10 min at rated load | By design (self-locking worm plus spring-applied brake); unverified | Brake and worm calculation; later hold test |
| R9 | Hold-to-run | Motion only while the dead-man grip is held and a direction is selected; release stops the clusters within 0.2 s | By design; unverified | Circuit review; later bench test |
| R10 | Flat rolling | Push force 40 N or less at rated load on a smooth floor at walking pace, with the clusters parked | Met on estimate (about 25 N) | Rolling calculation; later pull test |
| R11 | Size | Overall width 600 mm or less; upright height 1,300 mm or less to fit a car trunk or van shelf | Width met (about 570 mm). **Height not met** (about 1,460 mm) | Model check |
| R12 | Affordable | Parts cost $600 or less for one prototype, charger included | Met on estimate (about $580, indicative); about 3 % margin | Priced BOM (`bom/bom.csv`) |
| R13 | Battery | 24 V class LiFePO4 with BMS and fused output; charging blocked below 0 °C and above 45 °C; full charge in 4 h or less | By design; charge about 3.2 h (estimate) | Datasheets |
| R14 | Environment | Operate from 0 to 40 °C; electronics IP54 or better; survive rain on outdoor stoops | By design; unverified | Enclosure review; later spray test |
| R15 | Stair and building protection | No steel contact with stairs or walls in normal use; non-marking wheels; skids over stair nosings | By design; sprocket clearance over nosings unverified | Model check |

## Requirements not met or at risk

- **R11 height is not met.** The handle must stand about 1,230 mm above the floor when the truck is tilted 30 degrees for climbing, which puts the upright height at about 1,460 mm. A telescoping or folding handle would fix this but adds cost and mass (see SCM-PRC-001, key design choices).
- **R2 is at risk.** A tri-star cluster is sized for one stair geometry. The proposed cluster (234 mm wheel spacing) targets residential stairs; steeper or shallower stairs may make it slip or bump.
- **R3, R5 and R12 have thin margins** of a few percent on the estimates.
- R6 to R9 depend on control and brake behavior that exists only as a concept.

## Assumptions

- Payload 60 kg; truck about 24.3 kg (mass roll-up in SCM-PRC-001); total 84 kg.
- The clusters carry the whole weight while lifting (conservative; the operator's grip carries some in practice).
- Load center of mass about 500 mm above the cluster shaft; frame tilted about 30 degrees back while climbing.
- Drive efficiencies: motor driver 95 %, brushed motor 80 %, self-locking worm 45 %, chain and bearings 95 %.
- Rolling resistance coefficient about 0.03 for solid rubber wheels on a smooth floor.
- Stair geometry from the US International Residential Code (196 mm maximum riser, 254 mm minimum tread); national and local codes vary.

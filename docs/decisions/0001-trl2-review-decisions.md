---
doc_id: SCM-DDR-001
title: StepClimber TRL 2 review decisions
project: StepClimber
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review, the items still open, and the new TRL 3 proposals
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 8); items 9 to 13 remain proposed, awaiting Amish

## Context

The TRL 2 review note (`docs/REVIEW.md`, session "/populate to a strong TRL 2") and the key design choices in SCM-PRC-001 v0.2 listed the StepClimber design choices as "Proposed, awaiting Amish", most with a recommendation. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." He also approved three cross-cutting SwapCell interface additions (a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles), a rule that shared SwapCell packs are priced once and excluded from each dependent kit budget, and a rule that co-design partners are chosen per area later.

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for items 1 to 8 are in `docs/REVIEW.md` (TRL 2 session) and SCM-PRC-001 v0.2 and are not repeated here. The options for the new items 11 to 13 are in SCM-CAL-001 v0.1.

## Decision

*Table 1. Decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation".*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Meaning of the pitch's tilt sensor | Option A: operator-in-the-loop tilt control (speed shaping, tilt window, stop and alert); no actuated load platform. Pitch reworded to "a tilt sensor that helps the courier hold the load angle steady" | `project.yaml`, `README.md`, SCM-PRC-001 v0.3 |
| 2 | Handle height (R11) | Option A: fixed handle for the first prototype, R11 relaxed to an upright height of 1,500 mm or less. Option C (folding hinge) studied at TRL 3 and not adopted | SCM-REQ-001 v0.3 R11; SCM-CAL-001 section 9 |
| 3 | Rated stair load | 60 kg (132 lb) payload until couriers are asked | SCM-REQ-001 v0.3 R1 |
| 4 | Climbing mechanism | Tri-star clusters rather than a stepping arm or tracks | SCM-PRC-001 v0.3 |
| 5 | Holding | Self-locking worm gearmotor plus a spring-applied brake (two independent holds) rather than an efficient gearbox with a brake alone | SCM-PRC-001 v0.3; SCM-CAL-001 section 6 |
| 6 | Battery | 24 V LiFePO4, 8S 10 Ah, rather than the 48 V SwapCell pack | SCM-PRC-001 v0.3; R13 |
| 7 | Operator position | The courier always stands uphill of the truck, going up and down; stated on labels and in the user guide | SCM-PRC-001 v0.3 safety |
| 8 | Budget | No change: `budget_usd` stays at $600; the priced BOM is $580 | `project.yaml`; SCM-REQ-001 R12 |

Consequences of the cross-cutting decisions for this repo:

- **SwapCell interface v0.3 items** (wake method, charge-while-discharging, latch vibration rating) do not apply, because item 6 keeps StepClimber on its own 24 V pack.
- **Shared SwapCell pack pricing** does not apply for the same reason; the pack stays in this BOM.
- **Co-design partners** are chosen per area later (item 10 stays open).

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| 9 | First user group for interviews: gig couriers, a parcel company pilot, or appliance and moving crews | Proposed, awaiting Amish (no recommendation was made) |
| 10 | Partner courier group or co-design partner | Proposed, awaiting Amish (to be chosen per area later) |
| 11 | Cluster and drive rework to meet R2 and R15 (SCM-CAL-001 section 3). Options: (A) 150 mm arms, 200 mm wheels, a two-stage chain drive with an 08B 20-tooth final sprocket, and a 54 mm shaft-line envelope; this likely pushes R5 past 25 kg and R12 past $600 and needs a larger motor or 18.8 steps/min. (B) Keep the cluster, restrict R2 to square nosings and find a shaft-line drive within a 48 mm radius (none identified at 146 N·m). (C) Change to a stepping-arm or tracked mechanism, which reverses item 4. Recommendation: A, with R5, R12 and R3 revisited once the parts are priced | Proposed, awaiting Amish |
| 12 | Tilt window (R6, R7). Options: tighten the stop window from plus or minus 8 to plus or minus 6 degrees so the grip force stays under 100 N, or relax R6 to about 110 N. Recommendation: tighten to plus or minus 6 degrees | Proposed, awaiting Amish |
| 13 | Follow-on target changes if item 11 A is chosen: R5 mass, R12 budget and R3 speed or motor size | Proposed, awaiting Amish |

## Consequences

- SCM-PRC-001, SCM-REQ-001 and SCM-PRB-001 move to v0.3 with these decisions; the design choices in items 1 to 8 are no longer "proposed".
- The parametric model, drawing SCM-DWG-001 Rev P1 and BOM stay at the baseline cluster and drive. They show the R15 conflict rather than an unapproved fix.
- TRL 3 is the hard stop. Nothing in this record starts TRL 4 work.

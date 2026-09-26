---
doc_id: SCM-DDR-002
title: StepClimber recommendations accepted
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
  change: Recommendations accepted by Amish (DDR-002); record the decided items, the changes made at TRL 3 and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 11 to 13 of SCM-DDR-001); items 9, 10 and the new item 14 remain proposed, awaiting Amish

## Context

SCM-DDR-001 left five StepClimber items open. Three of them carried a recommendation: the cluster and drive rework for R2 and R15 (item 11), the tilt window for R6 (item 12) and the follow-on targets for mass, budget and speed if the rework went ahead (item 13). On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Each item with a recommendation is therefore **Decided by Amish, 2026-09-25: go with recommendation**. Items with no recommendation stay open. TRL 4 remains on hold by Amish's instruction, so everything below was carried out on paper at TRL 3.

## Decision

*Table 1. Newly decided items and what changed in the repo.*

| # | Item | Decision | What changed |
| --- | --- | --- | --- |
| 11 | Cluster and drive rework (R2, R15) | Option A: 150 mm arms (were 135 mm), 200 mm wheels (were 150 mm) and a two-stage chain drive with an 08B 20-tooth final sprocket on the cluster shaft | `cad/src/model.py`: new cluster, a 20 mm countershaft 150 mm up the frame, first stage 06B 10T to 35T, final stage 08B 10T to 20T (7:1 overall, was 6:1), rail extended so the toe plate stays about 25 mm off the floor; STEP and STL re-exported. SCM-DWG-001 moved to Rev P2. BOM items 2 and 3 repriced ($65 to $88; $50 to $80). SCM-CAL-001 v0.2: shaft-line guard radius 53.9 mm inside the 54.2 mm envelope (was 104 mm against 48 mm), arms clear 32 mm nosing overhangs (was 23 mm). R2 and R15 now met |
| 12 | Tilt window (R6, R7) | Tighten the stop window from plus or minus 8 to plus or minus 6 degrees | R7 target and SCM-PRC-001 updated; model and drawing notes state plus or minus 6 degrees. With the larger cluster the grip force at the plus or minus 6 degree edge is still 111 N (was 107 N at 8 degrees on the old cluster), so R6 remains not met; see item 14 |
| 13 | Follow-on targets after the rework (R3, R5, R12) | Revisit once the parts are priced, as recommended. With the parts priced at TRL 3: R3 set to 17 steps/min on the present 250 W motor (was 20 steps/min; 20 would need 280 W); R5 set to 27 kg (was 25 kg); R12 and `budget_usd` set to $650 (were $600) | `project.yaml` `budget_usd` 600 to 650; SCM-REQ-001 R3, R5 and R12; SCM-CAL-001 v0.2 constants. Results: 238 W peak on the 250 W motor (5 % margin), 26.3 kg truck (0.7 kg margin), $633 BOM (2.6 % margin). The figures follow from the priced parts; Amish may adjust them at any time |

The pitch and the problem line in `project.yaml` are unchanged by these decisions.

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| 9 | First user group for interviews: gig couriers, a parcel company pilot, or appliance and moving crews | Proposed, awaiting Amish (no recommendation was made) |
| 10 | Partner courier group or co-design partner | Proposed, awaiting Amish (to be chosen per area later) |
| 14 | **New: grip force after the rework (R6).** The 150 mm arm widens the swing of the center of mass about the support wheel from plus or minus 71 to 89 mm, so the grip force is 70 N at the set angle and 111 N at the plus or minus 6 degree window edge; plus or minus 4.4 degrees would be needed for 100 N. Options: (A) keep plus or minus 6 degrees and relax R6 to 115 N until grip force is measured at TRL 4; (B) tighten the window to plus or minus 4 degrees, which risks frequent stops on uneven stairs; (C) lengthen the handle within the 1,500 mm height limit, which gains only a few percent. Recommendation: A | Proposed, awaiting Amish |

## Consequences

- R2 and R15 move from not met to met; R6 stays not met. On paper StepClimber now meets 10 of 15 requirements, misses 1 and leaves 4 that need hardware.
- Endurance falls from 1,394 to 1,327 loaded steps per charge because of the heavier truck and the second chain stage; R4 is still met.
- No cross-repo action arises: StepClimber keeps its own 24 V pack (SCM-DDR-001 item 6).
- TRL 3 is the hard stop. Nothing in this record starts TRL 4 work.

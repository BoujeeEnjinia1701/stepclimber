---
doc_id: SCM-DDR-003
title: StepClimber design for construction
project: StepClimber
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are **Proposed, awaiting Amish**.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of SCM-DDR-002 showed what StepClimber does: its cluster geometry, shaft line, chain centres, gearmotor, pack and handle were right in size and place. It was a massing model, though, and checking it with build123d showed that it could not be built as drawn. The flange bearings sat inside the rails and the spider hubs, the countershaft had one bearing that overlapped a rail, the chain guards and every part on the frame back floated with no fixing, the lowest cross bar ran through the chain, and the chain centres did not suit whole chains.

The changes keep what the truck does: the same clusters, shaft line, ratios, tilt control, holds, pack, handle, stair range and nosing envelope. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now builds each component separately and runs 90 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must not touch keep a stated clearance, and the clusters are turned through a third of a turn in 15 degree steps to check that nothing on the frame is struck. All 90 pass. `docs/04-calcs/sizing.py` adds a check of every frame-fixed outline near the shaft against every stair nosing.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The flange bearings were drawn at the rails, overlapping the rail tubes, the axle mount blocks and the spider hubs. With the clusters 262 mm off centre and the rails at 200 mm there is no room outboard of the rails for a bearing, a hub, a spider and a wheel inside the 600 mm width limit (R11). | Two axle plates welded to the inside faces of the rails: a 4 mm steel plate on the plain side and, on the drive side, the 3 mm steel outer plate of the chain case. A 25 mm two-bolt flange bearing bolts to the inside face of each, so the bearing centres are 168 mm off centre. The plates are welded on a straight bar through both bores so the bores line up. | The bearings sit inside the frame, protected, and the clusters stay where SCM-DDR-002 put them (width 569 mm at the wheel faces, 588 mm over the wheel end screws). The cost is a longer overhang from bearing to wheel (93 mm, was 48 mm): the shaft safety factor at 3 g falls from 1.8 to 1.4, still above 1 (R1 stays met). |
| P2 | The countershaft had one bearing, half inside a rail, with both its sprockets overhung. | The countershaft runs in two 20 mm two-bolt flange bearings, one on each chain case plate, 86 mm apart, with both sprockets between them. Their bolts sit in 8 mm slots up the frame. | A shaft carrying 4.5 kN of chain pull needs a bearing each side of its sprockets. The slots tension the final-stage chain. |
| P3 | The chain guards were rings and strips with no fixing and open sides. | A closed chain case: the outer plate (P1), a 3 mm aluminium inner plate held 86 mm away by two spacers, and a 1.5 mm aluminium band round the edge on riveted tabs and M4 screws. The case outline keeps the concept's guard radii: 53.9 mm on the shaft line and 65.8 mm round the countershaft. | It fixes the guard, encloses both chains (the pinch hazard) and carries the countershaft and gearmotor. It is the closed case that the appearance-model note of 2026-09-26 recommended (item 2). |
| P4 | The lowest cross bar, 60 mm above the shaft line, ran through the final-stage chain and both axle plates. | That bar is cut off and a new 22 mm bar is welded 105 mm below the shaft line, 22 mm below the case. | The frame keeps four cross bars and the chain case has a clear run. |
| P5 | The 35-tooth sprocket stood 2 mm, and its guard 12 mm, in front of the rails, in the space where the load sits. | The countershaft and the gearmotor output move 15 mm toward the stair side of the shaft line. The case now stays 2 mm behind the front of the rails. | The load rests against flat rails and cross bars. The countershaft clearance to the nearest nosing falls from 96 to 80 mm; every frame-fixed outline near the shaft still clears every nosing by 10 mm or more (R15). |
| P6 | The chain centres (150 and 140 mm) needed 38.8 and 53.0 links. | Countershaft 143.9 mm up the frame (38 links of 08B), gearmotor output 145.1 mm above it (54 links of 06B). The countershaft bearings and the gearmotor screws sit in 8 mm slots for tension. The 10-tooth sprocket hubs are kept clear of the chain plates. | Chains come in whole links; even link counts need no offset link. The ratios are unchanged (7:1). |
| P7 | The gearmotor had its motor parallel to the output shaft, which is not how a worm gearmotor is made, and it floated behind the frame. | The motor stands up the frame at right angles to the output, as in a wheelchair worm gearmotor. The gearbox face bolts to the inside of the case inner plate with three M8 screws in slots; its output shaft passes into the case. | A face-mounted gearbox is held where its torque reacts, and the motor fits between the case and the electronics box. |
| P8 | The spider hubs and wheels had no fixing: the wheel hubs passed through the spiders and there was no axle. | Each spider (6 mm laser-cut steel, with a 96 mm centre disc) carries a 1610 weld-on taper-lock hub through a 76 mm hole, welded both sides, and three 20 mm stub axles welded in its arms. Each wheel runs on two 20 mm bearings, between a 4.5 mm spacer and a washer held by an M10 end screw. | Bought hubs give a keyed, clamped fit on the 25 mm shaft without machining. The centre disc (48 mm radius) stays inside the 54.2 mm nosing envelope. |
| P9 | The electronics box, pack, fuse box and gearmotor floated behind the rails with nothing holding them (also noted on 2026-09-26, appearance item 1). | Two 30 x 6 mm aluminium uprights bolt through the three upper cross bars. The electronics box, the pack cradle and the fuse box bolt to them. The electronics box moves up 30 mm to clear the motor; it and the pack move 35 and 30 mm toward the rails to sit on the uprights. | Light (0.6 kg for both), bolted rather than welded, and the cross bars carry the load. The centre of mass moves by under 2 mm, which the calculation does not see. |
| P10 | The skids were 860 mm long (500 mm in the BOM) on thin rods, 150 mm off centre. | 500 mm UHMW skids from 40 to 540 mm above the shaft line, screwed to four 20 mm square-tube standoffs welded to the backs of the rails, 140 and 510 mm up. The skids move to 200 mm off centre, behind the rails; their face stays 100 mm behind the shaft line. | Straight standoffs from the rails; the skid face, and so the frame-back clearance of 109 mm, is unchanged. The turning clusters clear the skids and standoffs by 15 mm. |
| P11 | The handle pod and dead-man lever floated beside the grip; the load strap was a bar in mid-air; the harness ran through other parts. | The pod clamps round the grip and carries the lever; the ratchet strap hooks round the rails; the harness runs from connector to connector, tied to the uprights and the drive-side handle tube. | Every part has a fixing. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Truck 34.2 kg (was 26.3 kg). The parts added for construction weigh 3.9 kg (axle plates and case 2.5 kg, stub axles 0.8 kg, uprights 0.6 kg, skid standoffs 0.5 kg) plus 0.5 kg of fixings. The shafts, bearings, sprockets and chains are now itemised from catalogue-class masses at 5.5 kg; the concept carried a 2.5 kg allowance for them, and the 25 mm shaft alone is 1.9 kg. **R5 (27 kg) is not met**, by 7.2 kg. | The constructable design names every part, so its mass can be added up. |
| Climb speed | At 94.2 kg total the peak motor output at 17 steps/min is 260 W against the 250 W motor; the fastest climb on that motor is 16.3 steps/min. **R3 is not met**, by 4 %. | Follows from the mass. |
| Other figures | Endurance 1,215 loaded steps per charge (R4 met); grip force 121 N at the window edge (R6 still not met, was 111 N); gearmotor output 28.2 N·m against 30 N·m rated; final-stage chain safety factor 4.0; safety factors on yield at 3 g: shaft 1.4, spider 1.5, rail 2.6 (R1 met); brake margin 7.5 times. | Follows from the mass and P1. |
| Cost | BOM lines 1 to 3 and 13 repriced; lines 14 to 17 added. Value-engineering target: USD 650. Estimated cost of the constructable design: USD 776 (USD 126 over the target). | Parts added for construction; see the design decisions register for the main cost drivers. |
| Drawing | SCM-DWG-001 Rev P4; making sketches SCM-DWG-101 to 109 added. | Follows the model. |
| Documents | SCM-CAL-001 v0.3, SCM-REQ-001 v0.5, SCM-PRC-001 v0.5: mass, speed, structure, cost and nosing figures updated; R3 and R5 move to not met. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | R5: the constructable truck weighs 34.2 kg against 27 kg. | (a) Set R5 to 35 kg for the first prototype and weigh it at TRL 4. (b) Take mass out first: an aluminium chain case outer plate bolted to a welded steel tab (about 0.7 kg), a lighter frame bought without wheels or with a 25 mm rail (about 1 to 2 kg), lighter wheels; even so, 27 kg is unlikely. (c) A smaller payload rating, which changes R1. | (a), and try the savings in (b) when parts are bought. |
| A2 | R3: 17 steps/min needs 260 W from a 250 W motor at the new mass. | (a) Set R3 to 16 steps/min for the first prototype. (b) Fit a 300 W class worm gearmotor (more cost, about 0.5 kg more). (c) Lower the climb speed only near the top of a flight. | (a): the controller sets the speed, so a faster motor can come later without other changes. |
| A3 | R6, item 14 of SCM-DDR-002, now at 121 N rather than 111 N at the plus or minus 6 degree window edge. | As in SCM-DDR-002 item 14: relax R6 (now to 125 N) until the grip force is measured, tighten the window (plus or minus 3.1 degrees would meet 100 N), or lengthen the handle. | Relax R6 to 125 N until it is measured at TRL 4. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan SCM-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`). Open decisions are in the design decisions register SCM-DEC-001.
- Requirement status (SCM-CAL-001 v0.3): 7 met on paper (R1, R2, R4, R10, R11, R13, R15), 3 not met (R3, R5, R6), 4 not verifiable at TRL 3 (R7, R8, R9, R14), and R12 is reported against the value-engineering target (USD 126 over).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept drive, bearings and mounts; they need updating on Amish's Mac, where Blender is.
- The gearmotor, flange bearings, weld-on hubs, wheels and frame are chosen at TRL 4; the sizes the model assumes for them are listed in the register to be checked when they are bought.
- TRL stays at 3. Nothing in this record starts TRL 4 work.

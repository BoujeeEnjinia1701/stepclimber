---
doc_id: SCM-DEC-001
title: StepClimber design decisions register
project: StepClimber
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open decisions from SCM-DDR-001 to SCM-DDR-003 and the review note; budget treated as a value-engineering target
---

# StepClimber design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Review the design-for-construction changes (bearings on axle plates inside the rails, closed chain case, countershaft in two bearings, chain centres for whole chains, weld-on hubs and stub axles, component uprights, skid standoffs, lowest cross bar moved) | Accept as made; or change any of them | Accept as made | The whole build plan | SCM-DDR-003, Table 1 (P1 to P11) |
| 2 | Truck mass (R5): the constructable truck weighs 34.2 kg against 27 kg | (a) Set R5 to 35 kg for the first prototype and weigh it at TRL 4; (b) take mass out first (aluminium case outer plate on a welded tab, a lighter frame, lighter wheels); (c) a lower payload rating | (a), trying the savings in (b) when parts are bought | None in the plan; the prototype is weighed in the first checks | SCM-DDR-003, A1 |
| 3 | Climb speed (R3): at the new mass 17 steps/min needs 260 W from the 250 W motor | (a) Set R3 to 16 steps/min for the first prototype; (b) a 300 W class worm gearmotor; (c) slow only near the top of a flight | (a): the controller sets the speed, so a faster motor can follow later | Controller speed setting; gearmotor choice | SCM-DDR-003, A2 |
| 4 | Grip force (R6): 121 N at the plus or minus 6 degree window edge against 100 N | (a) Keep the window and relax R6 to 125 N until grip force is measured; (b) tighten the window (plus or minus 3.1 degrees meets 100 N), which risks frequent stops; (c) lengthen the handle within 1,500 mm | (a) | Controller tilt window; handle length | SCM-DDR-002 item 14; SCM-DDR-003, A3 |
| 5 | Appearance model and photoreal renders: bring them to the constructable design | (a) Update `cad/src/product_model.py` and re-render on Amish's Mac; (b) keep the concept renders, marked as concept | (a) | None in the build; storefront images | Review note 2026-09-26 items 1 to 5; SCM-DDR-003 |
| 6 | First user group for interviews | Gig couriers, a parcel company pilot, or appliance and moving crews | None was made | None in the build; stair survey and load cases | SCM-DDR-001 item 9 |
| 7 | Partner courier group or co-design partner | To be chosen per area later | None yet | None in the build | SCM-DDR-001 item 10 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The hand truck frame: 28 mm rails 400 mm apart, a toe plate 142.5 mm below the shaft line, and three cross bars at about 380, 700 and 1,000 mm above it | The axle plates, uprights and skid standoffs are placed from the rails and cross bars | SCM-DDR-003, P4, P9, P10 |
| 2 | The worm gearmotor: face-mounted gearbox about 95 x 90 x 95 mm with tapped holes 40 mm from the output (or a pattern the inner plate can be drilled to), 20 mm keyed output shaft at least 25 mm long, motor at right angles no more than 84 mm across and 150 mm long, spring-applied brake | The case inner plate and its screw slots are cut to suit it | SCM-DDR-003, P7 |
| 3 | The flange bearings: 25 mm and 20 mm two-bolt units with bolt centres of 99 and 90 mm and flanges no wider than 74 and 60 mm | Plate holes and the clearances to the chains and the rails | SCM-DDR-003, P1, P2 |
| 4 | The 1610 weld-on taper-lock hubs: about 76 mm across and 26 mm long, with 25 mm keyed bushes | The spider's centre hole and the 5 mm clearance to the rails | SCM-DDR-003, P8 |
| 5 | The wheels: 200 mm solid rubber, 45 mm hub length, two 20 mm bore sealed bearings | The stub axle length and the overall width (588 mm) | SCM-DDR-003, P8 |
| 6 | The sprockets: 20-tooth 08B bored 25 mm keyed; 10-tooth 08B and 35-tooth 06B bored 20 mm keyed, the 10-tooth hub no more than 27 mm across; 10-tooth 06B bored to the gearmotor shaft | The hubs must clear the chain plates | SCM-DDR-003, P6 |
| 7 | The electronics box (about 340 x 110 x 50 mm, IP54) and the pack cradle mounting pattern | The upright hole positions | SCM-DDR-003, P9 |
| 8 | Weigh each bought part against the mass roll-up of SCM-CAL-001 v0.3 | R5 and R3 depend on it | SCM-CAL-001 v0.3, section 9 |

## Value engineering

Value-engineering target: USD 650 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 776 (USD 126 over the target). Main cost drivers and savings worth trying:

- The largest lines are the battery pack (USD 120), the clusters with their weld-on hubs (USD 116), the worm gearmotor (USD 110), the shafts, bearings, sprockets and chains (USD 96), the frame (USD 70) and the laser-cut axle plates and chain case (USD 55).
- Making the design buildable added USD 143: lines 14 to 17 (axle plates and chain case, uprights, frame steel and fixings, USD 99), the weld-on hubs (USD 28) and the second countershaft bearing and chain connecting links (USD 16).
- Savings worth trying: order the spiders, axle plates and case plates in one laser-cut batch (one setup and one shipment, perhaps USD 15); buy a hand truck frame without wheels or a used one, since its wheels and axle are discarded (perhaps USD 20 to 30); a reconditioned wheelchair worm gearmotor with brake (perhaps USD 40); bore-to-size plate sprockets instead of hubbed ones (perhaps USD 10).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 8: operator-in-the-loop tilt control and the reworded pitch, fixed handle with R11 at 1,500 mm, 60 kg stair rating, tri-star clusters, self-locking worm plus spring-applied brake, 24 V LiFePO4 pack, operator always uphill, budget kept | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | SCM-DDR-001 |
| 2026-09-25 | Cluster and drive rework (150 mm arms, 200 mm wheels, two-stage chain drive), plus or minus 6 degree tilt window, R3 17 steps/min, R5 27 kg, `budget_usd` 650 | Amish: "i accept all your recommendations, go with them across all repos." | SCM-DDR-002 |
| 2026-09-25 | TRL 4 on hold for the portfolio | Amish | `project.yaml`; SCM-DDR-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The changes made under this instruction are open for his review (open decision 1) | SCM-DDR-003 |
| 2026-10-01 | Budgets are value-engineering targets, not limits | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; SCM-REQ-001 R12 |

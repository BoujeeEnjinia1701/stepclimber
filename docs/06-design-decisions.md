---
doc_id: SCM-DEC-001
title: StepClimber design decisions register
project: StepClimber
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open decisions from SCM-DDR-001 to SCM-DDR-003 and the review note; budget treated as a value-engineering target
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations of open items 1 to 7 on 2026-10-02; all moved to decisions made; R5 and shaft material lines to confirm updated
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Follow-ups carried out; figures from SCM-CAL-001 v0.5; shaft repriced (USD 788 total); item 9 to confirm updated
---

# StepClimber design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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
| 8 | Weigh each bought part against the mass roll-up of SCM-CAL-001 v0.5 | R5 (35 kg for the first prototype, set 2026-10-02) and R3 depend on it | SCM-CAL-001 v0.5, section 9 |
| 9 | The 25 mm keyed cluster shaft is quenched and tempered alloy steel such as 4140, not 1018 (decided 2026-10-02), with a mill certificate | Safety factor 2.5 at a 3 g load and fatigue factor 1.8 are on assumed minimum strengths (655 MPa yield, 1,000 MPa tensile); confirm from the certificate | Decision of 2026-10-02 (open item 1); SCM-CAL-001 |

## Value engineering

Value-engineering target: USD 650 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 788 (USD 138 over the target). Main cost drivers and savings worth trying:

- The largest lines are the battery pack (USD 120), the clusters with their weld-on hubs (USD 116), the worm gearmotor (USD 110), the shafts, bearings, sprockets and chains (USD 108, including USD 12 for the 4140 cluster shaft), the frame (USD 70) and the laser-cut axle plates and chain case (USD 55).
- Making the design buildable added USD 143: lines 14 to 17 (axle plates and chain case, uprights, frame steel and fixings, USD 99), the weld-on hubs (USD 28) and the second countershaft bearing and chain connecting links (USD 16).
- Savings worth trying: order the spiders, axle plates and case plates in one laser-cut batch (one setup and one shipment, perhaps USD 15); buy a hand truck frame without wheels or a used one, since its wheels and axle are discarded (perhaps USD 20 to 30); a reconditioned wheelchair worm gearmotor with brake (perhaps USD 40); bore-to-size plate sprockets instead of hubbed ones (perhaps USD 10).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 8: operator-in-the-loop tilt control and the reworded pitch, fixed handle with R11 at 1,500 mm, 60 kg stair rating, tri-star clusters, self-locking worm plus spring-applied brake, 24 V LiFePO4 pack, operator always uphill, budget kept | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | SCM-DDR-001 |
| 2026-09-25 | Cluster and drive rework (150 mm arms, 200 mm wheels, two-stage chain drive), plus or minus 6 degree tilt window, R3 17 steps/min, R5 27 kg, `budget_usd` 650 | Amish: "i accept all your recommendations, go with them across all repos." | SCM-DDR-002 |
| 2026-09-25 | TRL 4 on hold for the portfolio | Amish | `project.yaml`; SCM-DDR-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The changes made under this instruction were accepted on 2026-10-02 with one exception (below) | SCM-DDR-003 |
| 2026-10-01 | Budgets are value-engineering targets, not limits | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; SCM-REQ-001 R12 |
| 2026-10-02 | Open item 1: design for construction accepted, P1 to P11 and their knock-on changes, with one exception: the 25 mm cluster shaft is made from a quenched and tempered alloy steel such as 4140 instead of 1018 | Amish: "i approve your recommendations for all 555 open decisions." | SCM-DDR-003, Table 1 (P1 to P11) |
| 2026-10-02 | Open item 2: R5 set to 35 kg for the first prototype (34.2 kg, met on paper); the prototype is weighed at TRL 4, and the savings are tried when parts are bought | Amish: "i approve your recommendations for all 555 open decisions." | SCM-DDR-003, A1 |
| 2026-10-02 | Open item 3: R3 set to 16 steps/min for the first prototype (the 250 W motor gives 16.3, met on paper) | Amish: "i approve your recommendations for all 555 open decisions." | SCM-DDR-003, A2 |
| 2026-10-02 | Open item 4: grip force (R6): the tilt window is tightened to plus or minus 3 degrees for the first loaded trials, and widened toward plus or minus 6 degrees only when grip force is measured at 100 N or less, or operators are shown to handle the measured force safely. R6 stays at 100 N. This replaces the record's recommendation to relax R6 to 125 N | Amish: "i approve your recommendations for all 555 open decisions." | SCM-DDR-002 item 14; SCM-DDR-003, A3 |
| 2026-10-02 | Open item 5: the appearance model is brought to the constructable design and re-rendered on Amish's Mac | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26 items 1 to 5; SCM-DDR-003 |
| 2026-10-02 | Open item 6: first user group: interview parcel couriers who deliver to walk-up apartment buildings first, with gig couriers as a second group; appliance and moving crews are left out | Amish: "i approve your recommendations for all 555 open decisions." | SCM-DDR-001 item 9 |
| 2026-10-02 | Open item 7: co-design partner: seek a regional parcel or last-mile delivery company willing to run a small supervised pilot, chosen from the interviews of item 6; the first candidate type to approach, not yet agreed | Amish: "i approve your recommendations for all 555 open decisions." | SCM-DDR-001 item 10 |

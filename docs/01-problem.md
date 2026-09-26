---
doc_id: SCM-PRB-001
title: StepClimber problem statement
project: StepClimber
doc_type: Problem statement
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, cited prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the rated load and the pitch wording (SCM-DDR-001); note the nosing finding of SCM-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); budget, mass constraint and stair survey question updated for the cluster rework
---

# StepClimber problem statement

Last-mile couriers carry heavy parcels up stairs to walk-up apartments by hand, which causes injuries and slows deliveries. Low-cost manual stair trucks exist but leave the lifting to the courier, and powered stair climbers work well but cost several thousand US dollars, so there is a gap for an open, repairable, motor-assisted stair truck at a few hundred dollars.

## The problem

Overexertion is the leading cause of injury for delivery workers, and the problem is growing. A study of US emergency department data for 2015 to 2022 estimated about 182,000 injuries among couriers and messengers, rising from about 13,000 a year in 2015 to about 35,000 in 2022; overexertion and bodily reaction caused about 42 % of them, and falls, slips and trips about one fifth ([Iacobucci et al., *Journal of Safety Research*, 2024](https://www.sciencedirect.com/science/article/pii/S0022437524001646)). Earlier NIOSH-funded work found overexertion caused 35.5 % of courier injuries with days away from work, and an industry injury rate of 12.8 per 100 full-time workers, 2.6 times the private-sector average ([Hoskin et al., CDC Stacks](https://stacks.cdc.gov/view/cdc/190995)). Manual handling while loading and unloading is a recognized musculoskeletal risk for couriers ([PubMed 36463479](https://pubmed.ncbi.nlm.nih.gov/36463479/)).

Stairs make it worse. On a flat sidewalk a hand truck carries the load; on stairs the courier either carries each parcel in their arms or drags the hand truck up one bump at a time, taking the full weight on every step while walking backwards. The revised NIOSH lifting equation starts from a load constant of 23 kg (51 lb) for an ideal lift and reduces it for carrying posture, reach and frequency ([NIOSH publication 94-110](https://www.cdc.gov/niosh/publications/numbered/94-110.html)), so a 30 kg appliance or a stack of water cases on a stair is well past a safe single-person lift.

The tools on sale fall into two groups:

1. **Manual tri-star stair trucks** cost about $100 but are rated for much less on stairs than on the flat, for example 70 kg (154 lb) on the flat and 35 kg (77 lb) on stairs ([Mount-It MI-953](https://www.mount-it.com/products/tri-wheel-stair-climber-hand-truck-with-foldable-design-mi-953)). The courier still supplies all the lift.
2. **Powered stair climbers** use a stepping mechanism or tracks and carry 110 to 170 kg at up to 48 steps per minute ([SANO Liftkar SAL](https://www.sano-stairclimbers.com/load-transporters/products/liftkar-sal)), but a typical unit sells for about $4,400 ([Zoro listing](https://www.zoro.com/sano-liftkar-pro-uni-loop-grip-stairclimbing-hand-truck-245-lbs-cap-puncture-proof-wheels-wl-sp11un03lo18/i/G416283780/)). That is out of reach for gig couriers and small delivery firms, and the units are closed designs.

StepClimber aims at the gap: a motor-driven tri-star hand truck that lifts about 60 kg one step at a time for a parts cost of about $650, with a tilt sensor that helps the courier hold the load at a safe angle.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Gig or contract courier | Get heavy parcels and multi-parcel drops up two to five flights without lifting them by hand | Own vehicle, many stops a day, paid per drop, no company equipment |
| Parcel company driver | Reduce strain on heavy-package days (water, appliances, furniture boxes) | Van with limited space, route time targets, company safety rules |
| Small moving or appliance crew | Move 30 to 60 kg items up narrow walk-up stairs with one person instead of two | Older buildings, tight landings |
| Building superintendent or caretaker | Move supplies up and down stairs in a building without an elevator | Occasional use, one building |
| Residents of the buildings | Stairs, walls and other residents not harmed by the truck | Shared stairwells, children, pets |

### Operating environment

- **Stairs:** straight flights in walk-up apartment buildings. US residential code allows risers up to 196 mm (7.75 in) and treads down to 254 mm (10 in); commercial stairs are gentler ([Lapeyre Stair summary of IRC and IBC](https://www.lapeyrestair.com/blog/stair-riser-height-tread-depth/)). Older buildings and service stairs can be steeper; OSHA permits up to 241 mm (9.5 in) on some industrial stairs. Landings may turn 90 or 180 degrees.
- **Surfaces:** wood, concrete, tile, carpet and metal treads, with worn or protruding nosings; wet outdoor stoops.
- **Loads:** parcels of 5 to 32 kg, stacked to about 60 kg; bulky single items such as small appliances.
- **Duty:** several stair drops a day, each two to five floors (about 30 to 80 steps up and the same down).
- **Climate:** outdoor use from about 0 to 40 °C, rain on stoops and sidewalks.
- **Transport:** lifted in and out of a van or car trunk many times a day.

## Constraints

- Garage-buildable prototype, about $650 USD in parts (budget revised from $600 by Amish on 2026-09-25, SCM-DDR-002).
- Light enough to lift into a vehicle by one person: 27 kg or less including the battery (SCM-REQ-001 R5, revised on 2026-09-25).
- Fits standard residential stairs and doors (about 760 mm (30 in) clear width) without adjustment.
- Hold-to-run control, and the load must stay put on the stair if power, the motor or the operator's grip is lost.
- Low-voltage (24 V class) battery with a BMS; no exposed mains.
- Open design (CERN-OHL-S) built from generic parts: wheelchair-type worm gearmotors, hand truck frames, LiFePO4 packs.

## Out of scope

- Carrying people. Stair chairs for people are a regulated medical and mobility product.
- Spiral stairs and ladders.
- Loads over the rated stair load, and pallet-scale moving.
- Autonomous or remote-controlled climbing; an operator is always holding the truck.
- Gas cylinders and other hazardous goods.

## Prior work

- **Tri-star wheels.** Robert and John Forsyth's three-wheel cluster was assigned to Lockheed in 1967 and used on the Terra Star vehicle ([Wikipedia: Tri-star wheel arrangement](https://en.wikipedia.org/wiki/Tri-star_(wheel_arrangement))). Manual tri-star hand trucks are now common among couriers for light deliveries, typically around 60 to 80 kg ([Wikipedia: Stairclimber](https://en.wikipedia.org/wiki/Stairclimber)).
- **Powered stair trolleys.** Makers group them as tri-star, support-arm (stepping) and tracked types. Powered tri-star units tend to be light-duty, while stepping and tracked units carry 150 to 250 kg ([XSTO overview](https://www.xstoclimbers.com/blogs/news/3-types-of-stair-trolley-tri-star-vs-support-arm-vs-tracked-systems)).
- **Stepping climbers.** The SANO Liftkar family climbs up to 48 steps per minute, handles risers up to 210 mm, uses a 24 V lithium-ion or lead-acid pack, and brakes on descent with an eddy-current brake ([SANO Liftkar SAL](https://www.sano-stairclimbers.com/load-transporters/products/liftkar-sal)).
- **Academic and student builds.** Many university projects have built motorized tri-star trolleys and robots, for example a published tri-star mechanical design for a stair-climbing robot ([ResearchGate](https://www.researchgate.net/publication/256942417_Mechanical_design_and_development_of_tri-star_wheel_system_for_stair_climbing_robot)). Few are documented well enough to rebuild, and most omit the safety interlocks a courier would need.

## Open questions

- Which user group first: gig couriers, a parcel company pilot, or appliance and moving crews? Proposed, awaiting Amish (SCM-DDR-001 item 9).
- What stair load do couriers need most often: 40, 60 or 80 kg? Amish decided on 2026-09-25 to rate the prototype at 60 kg until couriers are asked; interviews should confirm it.
- How steep are the walk-up stairs in the first target city, and how far do their nosings overhang? Riser, tread and nosing survey needed: the reworked cluster (SCM-DDR-002) covers risers to about 225 mm and nosing overhangs to 32 mm, and needs treads of about 240 mm or more.
- Would a courier accept a truck of about 26 kg in the van, or is mass the main barrier to use?
- Are building owners concerned about nosing damage, and what protection is enough?

## User research

- [ ] Interview couriers and drivers about stair drops, loads and current tools
- [ ] Survey riser, tread and landing sizes in a sample of walk-up buildings
- [ ] Revise the requirements (SCM-REQ-001) from findings before freezing the design

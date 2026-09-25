---
doc_id: SCM-PRC-001
title: StepClimber design precis
project: StepClimber
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, cluster geometry, drive and energy numbers, tilt control, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions (SCM-DDR-001); replace estimates with SCM-CAL-001 figures; nosing clearance, handle force and landing corrections; media from the TRL 3 model
---

# StepClimber design precis

StepClimber is a steel hand truck whose two wheels are replaced by a pair of powered tri-star clusters on one shaft. A 24 V worm gearmotor with a built-in brake turns the clusters one third of a turn per step, lifting 60 kg of parcels up a residential stair while the courier walks ahead and steadies the handle. An IMU on the frame watches the tilt angle, shapes the motor speed so the courier can hold the load near its balance point, and stops the climb if the angle drifts. The TRL 3 calculations (SCM-CAL-001) give 20 steps per minute at 239 W peak, about 1,390 loaded steps per charge from a 256 Wh LiFePO4 pack, a 24.3 kg truck and $580 in parts, inside the $600 budget. **Three requirements are not met on paper:** the 60-tooth sprocket and its guard strike stair nosings (R15), the straight spider arms catch nosings with more than 23 mm overhang (R2), and the grip force reaches 107 N at the tilt window edge (R6). A cluster and drive rework and a tighter tilt window are proposed, awaiting Amish.

![Hero render](../media/hero.png)

*Figure 1. StepClimber tilted back for climbing at the foot of a residential stair (196 mm risers, 254 mm treads), with a parcel carton on the toe plate and a 1.75 m person for scale. Rendered from the TRL 3 model (`cad/src/model.py`). The stair and carton are context only.*

## How it works

1. **Load.** The courier stacks parcels on the toe plate against the frame and tightens the ratchet strap. On the flat the truck rolls on two wheels of each cluster like any hand truck; the gearmotor holds the clusters still and each wheel spins freely on its own axle.
2. **Set.** At the foot of the stair the courier backs the truck up to the first riser, tilts it back to the balance point (about 30 degrees from vertical for a typical load), squeezes the dead-man grip and presses "up". The controller stores the current frame angle as the set angle.
3. **Climb.** The gearmotor turns the cluster shaft through a 6:1 chain drive. The lower rear wheel of each cluster presses against the riser and becomes the pivot; the cluster turns about it until the top wheel lands on the tread above, then turns about the landed wheel for the rest of the third of a turn. Each one-third turn lifts the truck one step, and the courier rolls it back on the landed wheel to the next riser (about 126 mm on the design stair). The courier walks up backwards one step ahead, holding the handle.
4. **Hold the angle.** The frame pitches as the clusters roll over each nosing. The IMU reads the frame angle at 100 Hz or faster. The controller slows the motor near the end of each third of a turn so the landing wheel does not thump, and slows further if the angle moves away from the set angle so the courier can correct it. If the angle leaves a window of plus or minus 8 degrees, or the range 15 to 45 degrees back from vertical, the motor stops and the spring-applied brake holds, and a light bar and buzzer on the handle tell the courier which way to move the handle.
5. **Descend.** "Down" drives the clusters backwards at the same controlled speed. The worm drive is self-locking, so the load cannot run away down the stair; the motor drives the descent rather than a brake restraining it.
6. **Stop.** Releasing the grip, a fault, a flat battery or a pulled pack all leave the truck held on the step by the self-locking worm and the motor's spring-applied brake.

Tilt control keeps the operator in the loop. The truck has only the clusters on the stair and the courier's hands on the handle, so it cannot hold its own angle; the IMU makes the climb slow down and stop in a way that helps the courier hold it. Amish decided this reading on 2026-09-25, and the pitch now says "a tilt sensor that helps the courier hold the load angle steady" (SCM-DDR-001 item 1).

![Energy flow](../media/flow.png)

*Figure 2. Energy for one loaded step up, in joules per step, from the pack to the lift at the clusters. Design load case of 84 kg total on a 196 mm riser. Values from SCM-CAL-001 (calculated, not measured).*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

*Table 1. Main components.*

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Hand truck frame | Steel loop-handle hand truck, 28 mm rails 400 mm apart, grip 1,260 mm from the shaft, 380 x 240 mm toe plate, with added axle mounts | Commercial frame modified; about 8 kg |
| 2 | Tri-star wheel clusters (pair) | Laser-cut steel spiders, 135 mm hub-to-wheel arms, three 150 mm solid rubber wheels on sealed bearings each | Wheel spacing about 234 mm; non-marking tread |
| 3 | Cluster shaft and chain drive | 25 mm steel shaft in two flange bearings; 06B roller chain, 10 to 60 teeth (6:1), driven sprocket 187 mm across, guarded | **Strikes nosings (R15); rework proposed** |
| 4 | Worm gearmotor with brake | 24 V brushed, about 250 W, worm gearbox about 40 rpm output and 30 N·m rated, spring-applied electromagnetic brake (wheelchair type) | Self-locking worm plus brake: two independent holds |
| 5 | Motor driver | 24 V, 30 A brushed H-bridge with current sensing and a brake output | Current limit caps cluster torque |
| 6 | Controller with IMU | Small microcontroller, 6-axis IMU, light bar and buzzer, in a sealed box with item 5 | Tilt window, speed shaping, hold-to-run logic |
| 7 | Battery pack | 24 V LiFePO4, 8S, 10 Ah (256 Wh), BMS, quick-release cradle | About 2.6 kg |
| 8 | Main switch, fuse and harness | Key switch, 40 A fuse near the pack, keyed connectors | |
| 9 | Handle controls | Dead-man grip lever, up and down thumb switch, status light bar | Works with gloves |
| 10 | Load strap | Ratchet strap across the load, fixed to the frame | Stops parcels sliding off when pitching |
| 11 | Nosing guard skids | UHMW polyethylene strips on the back of the frame, 100 mm behind the shaft line | Protect stairs if the frame touches a nosing |
| 12 | Charger | 29.2 V, 3 A LiFePO4 charger | No exploded-view callout |
| 13 | Enclosure and hardware | Sealed box, fasteners, cable ties | No exploded-view callout |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

## Key numbers

All values are from SCM-CAL-001 v0.1, printed by `docs/04-calcs/sizing.py`. They are paper calculations, not measurements. The design load case is a 60 kg payload on a 24.3 kg truck (84.3 kg total) on a stair with 196 mm risers and 254 mm treads. The clusters are assumed to carry the whole weight while lifting, which is conservative.

### Cluster geometry and nosing clearance

A tri-star cluster climbs by pivoting about the wheel pressed against the riser. With a wheel-center spacing *d* and riser *h*, the landing wheel's center comes down sqrt(*d*² minus *h*²) from the pivot's center, and its contact point lands that distance less the 75 mm wheel radius past the riser face.

*Table 2. Cluster geometry.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Arm length (hub to wheel center) | 135 mm | Chosen |
| Wheel-center spacing *d* | 233.8 mm | 135 mm x sqrt(3) |
| Hub height on the flat | 142.5 mm | 75 mm wheel radius + 135 mm x sin 30° |
| Cluster overall diameter | 420 mm | 2 x (135 + 75) mm |
| Landing past a square nosing, 196 mm riser | 52.5 mm | sqrt(233.8² minus 196²) minus 75 |
| Landing past a square nosing, 200 mm riser | 46.1 mm | |
| Landing past a square nosing, 220 mm riser | 4.2 mm (the TRL 2 figure of 16 mm was wrong) | Out of range |
| Largest riser with 30 mm of landing | 209 mm | R2 range of 100 to 200 mm covered |
| Closest approach of a nosing to the shaft line | 57.8 mm (square nosing), 36.0 mm (32 mm overhang) | Section 3 of SCM-CAL-001 |
| Largest radius allowed on the shaft line | 48 mm (square), 26 mm (32 mm overhang) | Less a 10 mm margin |
| Driven sprocket guard radius | 104 mm | **R15 not met** |
| Nosing overhang the straight arms clear | 23 mm | **R2 not met** (32 mm required) |

The nosing passes through the gap between the two lower arms, close to the shaft, as the swinging wheel lands. The 60-tooth sprocket and its guard therefore strike every nosing, and the bearing housings and spider bosses strike nosings with large overhangs. SCM-CAL-001 compares larger clusters: 150 mm arms with 200 mm wheels clear 32 mm overhangs and allow a 54 mm envelope on the shaft line, enough for an 08B 20-tooth final sprocket behind a second chain stage. That rework is proposed, awaiting Amish (SCM-DDR-001 item 11); this precis and the model keep the baseline.

### Drive, speed and torque

Assumptions: 20 steps per minute, so one third of a turn every 3 s (6.67 rpm, 0.698 rad/s at the shaft); drive efficiencies as in SCM-REQ-001.

*Table 3. Drive.*

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Lift work per step | 162 J | 84.3 kg x 9.81 m/s² x 0.196 m | |
| Mean shaft torque | 77 N·m | 162 J / 2.09 rad | |
| Peak shaft torque | 113 N·m static, 146 N·m with a 1.3 factor | Full load on the 135 mm arm, plus the grip force | |
| Peak shaft power | 102 W | 146 N·m x 0.698 rad/s | |
| Peak motor output | 239 W | 102 W / (0.95 chain x 0.45 worm) | R3 met, 4 % margin on a 250 W motor |
| Gearmotor output | 25.7 N·m at 40 rpm | 146 N·m / (6 x 0.95) | Inside a 30 N·m rating |
| Chain pull at the peak | 1,608 N | Safety factor 5.5 on 06B | |

### Energy and endurance

*Table 4. Energy.*

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Pack energy per loaded step up | 499 J (0.14 Wh) | 162 J / (0.95 x 0.80 x 0.45 x 0.95) | |
| Pack energy per loaded step down | 42 J | Driving a self-locking worm while the load assists takes 21 % of the lift work, plus motor and driver losses | |
| Usable pack energy | 829 kJ | 256 Wh x 90 % | |
| Loaded steps per charge, up and down | 1,394 | 829 kJ / (541 J x 1.1 for standby and starts) | R4 met |
| Typical day | 29 drops of three floors (48 steps) each | | |
| Charge time | 3.5 h | 256 Wh / (87.6 W x 0.9) plus a 0.3 h constant-voltage tail | R13 met |

The self-locking worm wastes more than half the drive energy (Figure 2). It is kept because it holds the load without power (SCM-DDR-001 item 5). Its back-drive efficiency is -0.22, so it cannot be driven backwards by a static load; the 2 N·m motor brake alone would hold the load with an 8-times margin.

### Balance, handle force and rolling

During a step the support point moves under the hub: the hub goes from 117 mm beyond the pivot to 7 mm on the stair side of it, then to 135 mm beyond the landed wheel. With the frame angle held, the center of mass swings plus or minus 71 mm about the support point even at the best set angle, and a further 70 mm at the edge of the plus or minus 8 degree window.

*Table 5. Handle force.*

| Quantity | Value | Requirement |
| --- | --- | --- |
| Grip force at the set angle, worst point of a step | 54 N | |
| Grip force at the plus or minus 8 degree window edge | 107 N | **R6 not met** |
| Widest window that keeps the grip force at 100 N | Plus or minus 6.8 degrees | Tightening to 6 degrees proposed |
| Push force on the flat | 25 N | R10 met |

The TRL 2 figure of 91 N assumed the load pivoted about the shaft; the support point in fact moves during each step.

### Structure

At the 146 N·m peak and a 3 g dropped-step load, the safety factors on yield are 2.0 for the keyed 25 mm shaft, 1.8 for the 6 mm spider arms and 2.9 for the 28 mm frame rails (R1 met statically; fatigue not assessed).

### Mass and size

*Table 6. Mass and size.*

| Item | Value |
| --- | --- |
| Frame 8.0, clusters 4.0, shaft and chain 2.0, gearmotor 4.5, electronics 0.8, pack 2.6, harness 0.5, handle controls 0.6, strap 0.4, skids 0.4, hardware 0.5 kg | 24.3 kg (R5 met, 0.7 kg margin) |
| Overall width at the wheel faces | 569 mm (R11 met) |
| Upright height, fixed handle | 1,418 mm (R11 met at the 1,500 mm target decided on 2026-09-25) |
| Folded height with a hinge 950 mm above the shaft (Option C study) | 1,106 mm, for about 0.4 kg and $20 more; not adopted |

### Cost

$580 in parts including the charger (R12 met with a 3.3 % margin). See `bom/bom.csv`.

## Key design choices

Items marked **decided** were decided by Amish on 2026-09-25 (SCM-DDR-001), going with the recommendation.

- **Tri-star clusters rather than a stepping arm or tracks (decided).** Tri-stars are simple, roll on the flat without extra parts and are well understood. Stepping-arm climbers carry more and handle more stair shapes, and tracks are smoothest, but both are harder to build in a garage and cost more ([XSTO overview](https://www.xstoclimbers.com/blogs/news/3-types-of-stair-trolley-tri-star-vs-support-arm-vs-tracked-systems)). The cost of the tri-star is the thump at each nosing, a fixed stair range and, as SCM-CAL-001 shows, very little room near the shaft.
- **Operator-in-the-loop tilt control (decided).** Speed shaping, a tilt window, stop and alert, with no actuated load platform. The pitch was reworded to match.
- **Self-locking worm plus spring-applied brake (decided).** Two independent holds on a stair, at the cost of more than half the drive energy.
- **24 V LiFePO4, not the 48 V SwapCell pack (decided).** The drive needs about 240 W peak and 230 Wh per shift; LiFePO4 is the more forgiving chemistry for a pack that is dropped in and out of vans. SwapCell would add a CAN host adapter and cost more than half the budget. The SwapCell interface v0.3 items do not apply.
- **Fixed handle for the first prototype (decided).** R11 is relaxed to 1,500 mm; the 1,418 mm truck meets it. A folding hinge (Option C) was studied and not adopted.
- **Rated stair load of 60 kg (decided).** Higher than manual tri-star trucks (about 35 kg on stairs) and lower than stepping climbers (110 to 170 kg).
- **Operator above, truck below (decided).** The courier always stands uphill of the truck, going up (pulling) and going down (lowering). This goes on the labels and in the user guide.
- **Cluster and drive rework for R2 and R15.** Proposed, awaiting Amish: 150 mm arms, 200 mm wheels and a two-stage chain drive, with the mass, budget and speed targets revisited.
- **Tilt window of plus or minus 6 degrees for R6.** Proposed, awaiting Amish.

## Safety

> **Safety:** StepClimber moves an 84 kg mass on a stair with a person directly uphill of it, has a pinch-prone chain and rotating clusters, and carries a 256 Wh lithium iron phosphate pack. A fall of the loaded truck down a stair could crush or seriously injure the operator or anyone below. Treat every item here as a hazard to design out before any loaded climb.

- **Runaway and tip-over on the stair.** The main hazard. Two independent holds (self-locking worm and spring-applied brake), hold-to-run control, the tilt window and a rated load label are all required. Nobody may stand downhill of the truck on the stair. The frame must not be able to pass over center toward the operator if the grip is released: the tilt limits of 15 and 45 degrees protect against this only if the brake holds, which is unverified.
- **Operator falls.** The courier walks backwards up the stair. Speed is limited to 20 steps per minute and stops the moment the grip opens. The handle should leave one hand free for a stair rail where possible; this is an open question.
- **Pinch and entanglement.** The clusters rotate with up to about 146 N·m and the chain runs near the operator's feet. The chain and sprockets are fully guarded; the cluster spiders have no open gaps large enough for fingers when the truck is at rest; clothing and straps must be kept clear.
- **Lithium iron phosphate pack.** LiFePO4 is less prone to thermal runaway than other lithium-ion chemistries but can still vent and burn if crushed, shorted or overcharged. Use a pack with a BMS and cell-level protection, fuse the output (item 8), charge on a non-combustible surface away from sleeping areas, and never charge a damaged or wet pack. Charging below 0 °C must be blocked by the BMS.
- **Stair and building damage, and nosing strike.** Rubber wheels and skids protect nosings, but SCM-CAL-001 shows the baseline sprocket guard strikes every nosing mid-step. Apart from damaging the stair, a strike could jerk the frame toward the courier or stall the climb with the load half-lifted. The truck must not climb with a load until the rework (SCM-DDR-001 item 11) is settled.
- **Loads and grip force.** Unsecured parcels can slide as the frame pitches. The strap is mandatory. Loads with a high center of mass (tall boxes) shift the balance angle and raise the handle force, which already reaches 107 N at the window edge on the design load.

## Open questions

- Decide the cluster and drive rework (SCM-DDR-001 item 11) and, with it, the mass, budget and speed targets.
- Decide the tilt window (SCM-DDR-001 item 12).
- Survey riser, tread and nosing sizes in walk-up buildings in the first target city (R2).
- Confirm that the worm stays self-locking under vibration and measure the brake's holding torque (R8); these need hardware and wait for TRL 4, which is on hold.
- Assess fatigue of the keyed shaft and the welded frame.
- Choose the first user group and a partner courier group (SCM-DDR-001 items 9 and 10).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: [SCM-DWG-001 Rev P1](../cad/drawings/SCM-DWG-001.pdf).

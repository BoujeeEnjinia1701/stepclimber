---
doc_id: SCM-PRC-001
title: StepClimber design precis
project: StepClimber
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, cluster geometry, drive and energy numbers, tilt control, safety, media)
---

# StepClimber design precis

StepClimber is a steel hand truck whose two wheels are replaced by a pair of powered tri-star clusters on one shaft. A 24 V worm gearmotor with a built-in brake turns the clusters one third of a turn per step, lifting about 60 kg of parcels up a residential stair while the courier walks ahead and steadies the handle. An IMU on the frame watches the tilt angle, shapes the motor speed to keep the load near its balance point, and stops the climb if the angle drifts. First-order estimates give about 20 steps per minute, about 1,300 loaded steps per charge from a 256 Wh LiFePO4 pack, a truck mass of about 24 kg and a parts cost of about $580, inside the $600 budget. The upright height (about 1,460 mm) misses the 1,300 mm target (R11).

![Hero render](../media/hero.png)

*Figure 1. StepClimber tilted back for climbing at the foot of a residential stair, with a parcel carton on the toe plate and a 1.75 m person for scale. The stair and carton are context only.*

## How it works

1. **Load.** The courier stacks parcels on the toe plate against the frame and tightens the ratchet strap. On the flat the truck rolls on two wheels of each cluster like any hand truck; the gearmotor holds the clusters still and each wheel spins freely on its own axle.
2. **Set.** At the foot of the stair the courier backs the truck up to the first riser, tilts it back to the balance point (about 30 degrees from vertical for a typical load), squeezes the dead-man grip and presses "up". The controller stores the current frame angle as the set angle.
3. **Climb.** The gearmotor turns the cluster shaft through a 6:1 chain drive. The lower rear wheel of each cluster presses against the riser and becomes the pivot; the cluster rolls over it and the next wheel lands on the tread above. Each one-third turn lifts the truck one step. The courier walks up backwards one step ahead, holding the handle.
4. **Hold the angle.** The frame pitches as the clusters roll over each nosing. The IMU reads the frame angle at 100 Hz or faster. The controller slows the motor near the end of each third of a turn so the landing wheel does not thump, and slows further if the angle moves away from the set angle so the courier can correct it. If the angle leaves a window of plus or minus 8 degrees, or the range 15 to 45 degrees back from vertical, the motor stops and the spring-applied brake holds, and a light bar and buzzer on the handle tell the courier which way to move the handle.
5. **Descend.** "Down" drives the clusters backwards at the same controlled speed. The worm drive is self-locking, so the load cannot run away down the stair; the motor drives the descent rather than a brake restraining it.
6. **Stop.** Releasing the grip, a fault, a flat battery or a pulled pack all leave the truck held on the step by the self-locking worm and the motor's spring-applied brake.

Tilt control keeps the operator in the loop. The truck has only the clusters on the stair and the courier's hands on the handle, so it cannot hold its own angle; the IMU makes the climb slow down and stop in a way that helps the courier hold it. The pitch wording "holds the load angle steady" should be read this way (see key design choices).

![Energy flow](../media/flow.png)

*Figure 2. Energy for one loaded step up, in joules per step, from the pack to the lift at the clusters. Design load case of 84 kg total on a 196 mm riser. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Hand truck frame | Steel loop-handle hand truck, about 1,260 mm rails, 380 x 240 mm toe plate, with added axle mounts | Commercial frame modified; about 8 kg |
| 2 | Tri-star wheel clusters (pair) | Laser-cut steel spiders, 135 mm hub-to-wheel arms, three 150 mm solid rubber wheels on sealed bearings each | Wheel spacing about 234 mm; non-marking tread |
| 3 | Cluster shaft and chain drive | 25 mm steel shaft in two flange bearings; 06B roller chain, 10 to 60 teeth (about 6:1), large sprocket about 180 mm across, guarded | Sprocket clearance over nosings is an open question |
| 4 | Worm gearmotor with brake | 24 V brushed, about 250 W, worm gearbox about 40 rpm output and 30 N·m rated, spring-applied electromagnetic brake (wheelchair type) | Self-locking worm plus brake: two independent holds |
| 5 | Motor driver | 24 V, 30 A brushed H-bridge with current sensing and a brake output | Current limit caps cluster torque |
| 6 | Controller with IMU | Small microcontroller, 6-axis IMU, light bar and buzzer, in a sealed box with item 5 | Tilt window, speed shaping, hold-to-run logic |
| 7 | Battery pack | 24 V LiFePO4, 8S, 10 Ah (256 Wh), BMS, quick-release cradle | About 2.6 kg |
| 8 | Main switch, fuse and harness | Key switch, 40 A fuse near the pack, keyed connectors | |
| 9 | Handle controls | Dead-man grip lever, up and down thumb switch, status light bar | Works with gloves |
| 10 | Load strap | Ratchet strap across the load, fixed to the frame | Stops parcels sliding off when pitching |
| 11 | Nosing guard skids | UHMW polyethylene strips on the back of the frame | Protect stairs if the frame touches a nosing |
| 12 | Charger | 29.2 V, 3 A LiFePO4 charger | No exploded-view callout |
| 13 | Enclosure and hardware | Sealed box, fasteners, cable ties | No exploded-view callout |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. The design load case is a 60 kg payload on a 24.3 kg truck (84 kg total) on a stair with 196 mm risers and 254 mm treads. The clusters are assumed to carry the whole weight while lifting, which is conservative.

### Cluster geometry

A tri-star cluster climbs by pivoting about the wheel pressed against the riser. With a wheel-center spacing *d* and riser *h*, the landing wheel's center comes down about sqrt(*d*² minus *h*²) behind the pivot wheel's center.

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Arm length (hub to wheel center) | 135 mm | Chosen |
| Wheel-center spacing *d* | about 234 mm | 135 mm x sqrt(3) |
| Hub height on the flat | about 143 mm | 75 mm wheel radius + 135 mm x sin 30° |
| Cluster overall diameter | about 420 mm | 2 x (135 + 75) mm |
| Landing point on a 196 mm riser | wheel center about 128 mm past the pivot, wheel edge about 53 mm onto the tread | sqrt(234² minus 196²) |
| Landing point on a 200 mm riser | about 45 mm onto the tread | |
| Landing point on a 220 mm riser | about 16 mm onto the tread | Too little: risers above about 200 mm are not covered (R2) |

### Drive, speed and torque

Assumptions: 20 steps per minute, so one third of a turn every 3 s (about 6.7 rpm, 0.70 rad/s at the shaft); drive efficiencies as in SCM-REQ-001.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Lift work per step | about 162 J | 84 kg x 9.81 m/s² x 0.196 m | |
| Mean shaft torque | about 77 N·m | 162 J / 2.09 rad | |
| Peak shaft torque | about 145 N·m | 84 kg x 9.81 x 0.135 m arm = 111 N·m, x 1.3 for friction and dynamics | |
| Peak shaft power | about 101 W | 145 N·m x 0.70 rad/s | |
| Peak motor output | about 236 W | 101 W / (0.95 chain x 0.45 worm) | R3 met, thin margin on a 250 W motor |
| Gearmotor output torque needed | about 25 N·m at about 40 rpm | 145 N·m / (6 x 0.95) | Inside a 30 N·m rating |

### Energy and endurance

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Pack energy per loaded step up | about 500 J (0.14 Wh) | 162 J / (0.95 x 0.80 x 0.45 x 0.95) | |
| Pack energy per loaded step down | about 60 J | Driving a self-locking worm backwards costs about a fifth of the lift work, plus losses | |
| Usable pack energy | about 230 Wh (830 kJ) | 256 Wh x 90 % | |
| Loaded steps per charge, up and down | about 1,300 | 830 kJ / (560 J x 1.1 for standby and starts) | R4 met |
| Typical day | about 25 drops of three floors (48 steps) each | 1,300 / 48 | |
| Charge time | about 3.2 h | 256 Wh / (88 W x 0.9) | R13 met |

The self-locking worm wastes more than half the drive energy (Figure 2). It is kept because it holds the load without power. A more efficient gear with a brake alone would roughly double the steps per charge; see key design choices.

### Balance, handle force and rolling

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Horizontal handle distance from shaft at 30 degrees | about 630 mm | 1,260 mm x sin 30° | |
| Load offset at 8 degrees off balance | about 70 mm | 500 mm x sin 8° | |
| Handle force at the window edge | about 91 N | 84 kg x 9.81 x 0.070 / 0.63 | R6 met |
| Handle force at 15 degrees off balance | about 170 N | | Why the window is needed |
| Push force on the flat | about 25 N | 0.03 x 84 kg x 9.81 | R10 met |

### Mass and size

| Item | Estimate |
| --- | --- |
| Frame 8.0, clusters 4.0, shaft and chain 2.0, gearmotor 4.5, pack 2.6, electronics 0.8, harness 0.5, handle controls 0.6, strap 0.4, skids 0.4, hardware 0.5 kg | about 24.3 kg (R5 met, thin margin) |
| Overall width | about 570 mm (R11 met) |
| Upright height | about 1,460 mm (**R11 not met**) |

### Cost

About $580 in parts including the charger (R12 met with about 3 % margin). See `bom/bom.csv`.

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Tri-star clusters rather than a stepping arm or tracks.** Tri-stars are simple, roll on the flat without extra parts and are well understood. Stepping-arm climbers carry more and handle more stair shapes, and tracks are smoothest, but both are harder to build in a garage and cost more ([XSTO overview](https://www.xstoclimbers.com/blogs/news/3-types-of-stair-trolley-tri-star-vs-support-arm-vs-tracked-systems)). The cost of the tri-star is the thump at each nosing and a fixed stair range (R2). Recommendation: tri-star, as the pitch states.
- **Meaning of "holds the load angle steady".** Option A: operator-in-the-loop tilt control as described (speed shaping, a tilt window, stop and alert), which fits the budget. Option B: add an actuator that tilts the load platform relative to the frame to keep the parcels level, about $60 to $90 more and 2 kg heavier, which would break R5 and R12. Recommendation: Option A, and if Amish agrees, reword the pitch to "a tilt sensor that helps the courier hold the load angle steady". The `project.yaml` pitch is unchanged.
- **Self-locking worm plus spring-applied brake.** Two independent holds on a stair, at the cost of more than half the drive energy. The alternative is an efficient spur or planetary gearbox with a brake alone (about twice the steps per charge, but one hold only). Recommendation: worm plus brake for the first prototype.
- **24 V LiFePO4, not the 48 V SwapCell pack.** The drive needs about 250 W peak and 230 Wh per shift; LiFePO4 is the more forgiving chemistry for a pack that is dropped in and out of vans. SwapCell (about 468 Wh, 48 V class, about $370) would give more endurance and shared charging but costs more than half the budget and adds a CAN host adapter. Recommendation: stay at 24 V; revisit SwapCell only if a courier fleet uses it elsewhere.
- **Handle height (R11).** Option A: keep a fixed handle and relax R11 to about 1,500 mm. Option B: a telescoping handle, about $25 and 0.8 kg more, which puts R5 and R12 at or over their limits. Option C: a folding handle hinge above the pack. Recommendation: Option A for the first prototype, with C studied at TRL 3.
- **Rated stair load of 60 kg.** Higher than manual tri-star trucks (about 35 kg on stairs) and lower than stepping climbers (110 to 170 kg). An 80 kg rating would need a larger motor and pack. Recommendation: 60 kg until couriers are asked.
- **Operator above, truck below.** The courier always stands uphill of the truck, going up (pulling) and going down (lowering), which is the practice for hand trucks on stairs. Recommendation: state this in the labels and the user guide.

## Safety

> **Safety:** StepClimber moves an 84 kg mass on a stair with a person directly uphill of it, has a pinch-prone chain and rotating clusters, and carries a 256 Wh lithium iron phosphate pack. A fall of the loaded truck down a stair could crush or seriously injure the operator or anyone below. Treat every item here as a hazard to design out at TRL 3.

- **Runaway and tip-over on the stair.** The main hazard. Two independent holds (self-locking worm and spring-applied brake), hold-to-run control, the tilt window and a rated load label are all required. Nobody may stand downhill of the truck on the stair. The frame must not be able to pass over center toward the operator if the grip is released: the tilt limits of 15 and 45 degrees protect against this only if the brake holds, which is unverified.
- **Operator falls.** The courier walks backwards up the stair. Speed is limited to 20 steps per minute and stops the moment the grip opens. The handle should leave one hand free for a stair rail where possible; this is an open question.
- **Pinch and entanglement.** The clusters rotate with up to about 145 N·m and the chain runs near the operator's feet. The chain and sprockets are fully guarded; the cluster spiders have no open gaps large enough for fingers when the truck is at rest; clothing and straps must be kept clear.
- **Lithium iron phosphate pack.** LiFePO4 is less prone to thermal runaway than other lithium-ion chemistries but can still vent and burn if crushed, shorted or overcharged. Use a pack with a BMS and cell-level protection, fuse the output (item 8), charge on a non-combustible surface away from sleeping areas, and never charge a damaged or wet pack. Charging below 0 °C must be blocked by the BMS.
- **Stair and building damage.** Rubber wheels and skids protect nosings; the sprocket must clear the nosings (open question).
- **Loads.** Unsecured parcels can slide as the frame pitches. The strap is mandatory. Loads with a high center of mass (tall boxes) shift the balance angle and raise the handle force.

## Open questions for TRL 3

- Check the cluster geometry against a stair survey (risers, treads, nosing overhang) and decide whether an adjustable arm length is worth adding (R2).
- Confirm the sprocket and shaft clear stair nosings through a full third of a turn.
- Model the frame pitch through one step and tune the speed profile and tilt window; confirm the courier can hold the angle (R6, R7).
- Size the worm and brake holding torque with a margin over the 145 N·m peak, and confirm the worm stays self-locking under vibration (R8).
- Check frame, spider and shaft stresses at the peak torque and at a dropped-step shock load.
- Choose between the handle height options (R11).
- Find a partner courier group for user interviews.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).

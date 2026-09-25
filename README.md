# StepClimber

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $600 USD · **Difficulty:** 3 of 5

Motor-assisted hand truck on tri-star wheel clusters that climb stairs one step at a time, with a tilt sensor that helps the courier hold the load angle steady.

![StepClimber concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/SCM-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Last-mile couriers carry heavy parcels up stairs to walk-up apartments by hand, which causes injuries and slows deliveries.

## Concept

A steel hand truck on a pair of powered tri-star wheel clusters. A 24 V worm gearmotor with a spring-applied brake turns the clusters one third of a turn per step, lifting 60 kg (132 lb) of parcels up a residential stair at 20 steps per minute while the courier steadies the handle. An IMU on the frame slows the climb and stops it if the tilt angle leaves a safe window, so the courier can hold the load at its balance point. The TRL 3 calculations give about 1,390 loaded steps per charge from a 256 Wh LiFePO4 pack, a 24.3 kg truck and $580 in parts. They also show three requirements not yet met: the drive sprocket strikes stair nosings, the cluster arms catch large nosing overhangs, and the grip force at the edge of the tilt window is 107 N against 100 N. A fix is proposed for review. All figures are paper calculations, not measurements.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Steel hand truck frame with toe plate
- Tri-star wheel clusters (pair), 150 mm solid rubber wheels
- Cluster shaft with 6:1 chain drive
- 24 V worm gearmotor with spring-applied brake
- Motor driver and controller with IMU tilt sensor
- 24 V LiFePO4 pack, 10 Ah, with BMS
- Handle with dead-man grip and up and down switch

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> **Safety:** Runaway and tipping risk on stairs with the operator uphill of the load. Hold-to-run control, two independent holds when power is lost (self-locking worm and spring-applied brake), a tilt window and a rated load limit are required, and nobody may stand below the truck on a stair. Rotating clusters and the chain drive are pinch hazards and must be guarded. Contains a lithium iron phosphate pack: use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface. See the safety section of [docs/02-concept.md](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Sizing calculations are in [docs/04-calcs/01-sizing.md](docs/04-calcs/01-sizing.md) (SCM-CAL-001), the parametric model in [cad/src/model.py](cad/src/model.py) with STEP and STL exports, and the general arrangement drawing in [cad/drawings/SCM-DWG-001.pdf](cad/drawings/SCM-DWG-001.pdf).

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SCM-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SCM-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).

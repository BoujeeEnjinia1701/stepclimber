# StepClimber

**Area:** Mobility and Logistics · **Status:** Concept · **Prototype budget:** about $600 USD · **Difficulty:** 3 of 5

Motor-assisted hand truck on tri-star wheel clusters that climb stairs one step at a time, with a tilt sensor that holds the load angle steady.

## Problem

Last-mile couriers carry heavy parcels up stairs to walk-up apartments by hand, which causes injuries and slows deliveries.

## Concept

Motor-assisted hand truck on tri-star wheel clusters that climb stairs one step at a time, with a tilt sensor that holds the load angle steady.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Tri-star wheel clusters (2)
- Geared DC motor with worm drive
- Steel hand truck frame
- IMU tilt sensor
- Motor driver
- 24 V LiFePO4 pack
- Dead-man grip switch

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Tipping risk on stairs. Hold-to-run control, a mechanical brake that engages when power is lost, and a rated load limit are required. Contains a lithium battery pack. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).

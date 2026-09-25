# AirStreet

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $180 USD · **Difficulty:** 3 of 5

A street-level air quality node measuring PM2.5 and NO2, calibrated on CalRig, for neighborhood-scale pollution maps.

## Concept rationale

Dense, calibrated networks show where pollution is worst and whether interventions work.

## Burning platform

Air pollution is one of the largest environmental health risks worldwide.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It depends on CalRig for credible data.

## Problem

Regulatory air monitors are few and far apart, missing the streets where people breathe traffic pollution.

## Concept

A street-level air quality node measuring PM2.5 and NO2, calibrated on CalRig, for neighborhood-scale pollution maps.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Optical PM2.5 sensor
- Electrochemical NO2 sensor
- Temperature and humidity sensor
- FieldNode core
- Radiation shield

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.

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

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (AST-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `AST-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.

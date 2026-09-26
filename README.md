# AirStreet

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $180 USD · **Difficulty:** 3 of 5

A street-level air quality node measuring PM2.5 and NO2, calibrated on CalRig, for neighborhood-scale pollution maps.

![AirStreet concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Concept rationale

Traffic pollution changes from one block to the next, so a map of it needs many measurement points at street level, each with a known calibration. AirStreet puts a small sensor pod and radiation shield under the lab's FieldNode solar core on a street light pole: an optical sensor for PM2.5, a four-electrode electrochemical sensor for NO2, and a shielded temperature and humidity sensor for corrections. Particle, temperature and humidity response are checked on CalRig. CalRig does not cover NO2, so each NO2 sensor is calibrated by field collocation with a reference station before deployment and at intervals afterward. The node sends raw signals so calibrations can be improved and reapplied.

It is open and garage-buildable because the places with the fewest official monitors are the least able to buy closed commercial networks and their subscriptions. The sensors are sold worldwide, the pod and shield are 3D-printed, the mount uses band clamps and flat bar, and the calibration method is published with the design so that others can check any map made with it.

## Burning platform

Air pollution is one of the largest environmental health risks worldwide. Ambient air pollution caused an estimated 4.2 million premature deaths in 2019 ([WHO](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)). Even in the European Union, with dense monitoring, 48,000 deaths in 2022 were attributable to NO2 above the WHO guideline level of 10 µg/m³ ([EEA, 2024](https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024)).

Monitoring misses the streets where exposure is highest. Reference-grade mapping in Oakland, California, found NO2 and black carbon varying by up to 5 to 8 times within single city blocks ([Apte et al., 2017](https://pubs.acs.org/doi/10.1021/acs.est.7b00891)), while monitoring is not legally required at all in at least 37 % of countries ([UNEP, 2021](https://www.unep.org/news-and-stories/press-release/one-three-countries-world-lack-any-legally-mandated-standards)).

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal environment and transport | Before and after maps for low-traffic streets, school streets, bus corridors and clean air zones |
| Public health agencies | Street-level exposure data near schools, clinics and care homes, labeled as indicative |
| Street lighting and utilities | A light, self-powered add-on for existing poles that needs no pole wiring |
| Logistics and ports | Tracking NO2 and PM2.5 along freight routes and depot access roads |
| Universities and schools | Open, raw data and a documented calibration for teaching and exposure research |
| Community groups and NGOs | Evidence for local campaigns, with the calibration version stated on every map |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | More than 45 million people live within about 90 m (300 ft) of a major transportation facility ([US EPA](https://www.epa.gov/air-research/research-near-roadway-and-other-near-source-air-pollution)); street-scale variation is well documented ([Apte et al., 2017](https://pubs.acs.org/doi/10.1021/acs.est.7b00891)) |
| European Union and United Kingdom | 48,000 deaths in the EU in 2022 were attributable to NO2 above the WHO guideline ([EEA, 2024](https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024)); dense reference stations make field collocation of NO2 practical |
| India | Only 12 % of 4,041 census cities and towns have air quality monitoring ([CSE, 2023](https://www.cseindia.org/only-12-per-cent-of-india-s-census-cities-and-towns-have-air-quality-monitoring-stations-11779)) |
| East Africa (Uganda, Kenya, Ethiopia, Tanzania) | Listed by OpenAQ in 2020 among populous countries with no public national monitoring program ([OpenAQ, 2020](https://documents.openaq.org/reports/Open+Air+Quality+Data+Global+State+of+Play+2020.pdf)); AirQo already runs more than 400 low-cost PM2.5 sensors across 14 African countries ([AirQo](https://www.airqo.net/)) |
| Pakistan and Nigeria | The two most populous countries on the same OpenAQ list, at about 221 million and 206 million people ([OpenAQ, 2020](https://documents.openaq.org/reports/Open+Air+Quality+Data+Global+State+of+Play+2020.pdf)); the first reference station for collocation may itself be scarce |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It depends on CalRig for credible data. The real-world trigger is the evidence that pollution varies within single city blocks ([Apte et al., 2017](https://pubs.acs.org/doi/10.1021/acs.est.7b00891)) together with the finding that low-cost sensors become useful only after correction against reference data ([Barkjohn et al., 2021](https://amt.copernicus.org/articles/14/4617/2021/)).

## Problem

Regulatory air monitors are few and far apart, missing the streets where people breathe traffic pollution. Full problem statement: [docs/01-problem.md](docs/01-problem.md).

## Concept

A street-level air quality node measuring PM2.5 and NO2 for neighborhood-scale pollution maps. The sensor pod and radiation shield hang below a FieldNode core on a street light pole, inlets about 3.0 m above the sidewalk (proposed), and send one record every 5 min over LoRaWAN. PM, temperature and humidity are checked on CalRig; **NO2 is calibrated by field collocation with a reference station** for at least 14 days before deployment and at least every 6 months, because CalRig does not cover NO2.

Estimated performance (TRL 2, to be checked at TRL 3): about 45 mW average sensor power, within FieldNode's 115 mW allowance; about 3.0 kg on the pole; about $391 in parts including the FieldNode core, or about $265 for the sensor head alone. Not met: the $180 budget, and resolving NO2 near the WHO annual guideline of 10 µg/m³ (expected hourly error about 5 ppb, or 9.4 µg/m³). Only pollutant levels, temperature and humidity leave the device; no images or audio.

Full design precis: [docs/02-concept.md](docs/02-concept.md). Requirements: [docs/03-requirements.md](docs/03-requirements.md).

## Key components

1. FieldNode core (enclosure, LiFePO4 cell, MPPT charger, LoRaWAN radio)
2. FieldNode 6 W panel hood
3. Band clamps and mounting rail (no drilling)
4. Sensor pod with insect mesh and drip lid
5. Optical PM2.5 sensor (Sensirion SPS30 class)
6. Electrochemical NO2 sensor (Alphasense NO2-B43F class, ozone filtered)
7. NO2 potentiostat front end and 16-bit ADC
8. Multi-plate radiation shield
9. Temperature and humidity sensor (Sensirion SHT45 class)
10. Sensor cables with M12 plugs

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> **Safety:** Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require. Never open a street light pole's access door or tap its mains supply; AirStreet runs only on its own solar and battery supply.
>
> The FieldNode core holds a lithium iron phosphate cell: fuse it and charge only within the maker's limits. Electrochemical gas sensors contain an acid electrolyte; do not open or heat them. AirStreet data are indicative, not a regulatory measurement or health advice.

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

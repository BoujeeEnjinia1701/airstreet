---
doc_id: AST-REQ-001
title: AirStreet requirements
project: AirStreet
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
---

# AirStreet requirements

These are first-pass requirements for the concept. Targets are proposals for review, awaiting Amish and the first co-design partner, and will be checked by calculation at TRL 3. Status reflects the TRL 2 estimates in [02-concept.md](02-concept.md). Two requirements are **not met** (R3 and R15) and four are at risk.

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Measure PM2.5 at street level | 0 to 500 µg/m³; hourly mean after humidity correction within ±5 µg/m³ or ±30 % (whichever is larger) of a collocated reference | CalRig chamber check, then field collocation | Plausible; field result unverified |
| R2 | Measure NO2 at street level | 0 to 200 ppb (about 0 to 380 µg/m³); hourly mean absolute error 5 ppb or less against a reference station after field calibration | Field collocation with a chemiluminescence reference station | At risk; literature suggests about 3.5 ppb is reachable ([Zimmerman et al., 2018](https://amt.copernicus.org/articles/11/291/2018/)) |
| R3 | Resolve NO2 near the WHO annual guideline | Annual mean uncertainty 2 µg/m³ or less at 10 µg/m³ | Collocation statistics | **Not met.** 5 ppb (about 9.4 µg/m³) hourly error is similar to the guideline itself; long averages help, but drift is unverified |
| R4 | Distinguish streets that exceed the EU NO2 limit value | Classify annual means above or below 40 µg/m³ with 90 % confidence | Collocation statistics | Plausible |
| R5 | Measure temperature and humidity for corrections | ±0.5 °C and ±3 % RH inside the shield; radiation error 1 °C or less in full sun at 1 m/s wind | CalRig chamber check; side-by-side field test against an aspirated reference | At risk; shield performance unverified |
| R6 | Calibrate with a stated method | T, RH and PM checked on CalRig before deployment; NO2 collocated with a reference station for at least 14 days before deployment and at least every 6 months | Calibration record per node | Met by design |
| R7 | Keep raw data for recalibration | Send raw NO2 working and auxiliary electrode signals, PM, T and RH with a calibration version tag | Firmware and data schema review | Met by design |
| R8 | Report often enough for street maps | One record every 5 min; hourly means published within 15 min; 7 days of store and forward | Timing and storage calculation | Met by design (estimate) |
| R9 | Fit the FieldNode power budget | Sensor average 115 mW or less; energy neutral at the FieldNode design sun hours | Power budget calculation | Met, about 45 mW (estimate) |
| R10 | Stay within radio duty-cycle rules | LoRaWAN airtime below 1 % in EU868 sub-bands | Airtime calculation | Met, about 0.06 % at SF9 and 0.5 % at SF12 (estimate) |
| R11 | Mount on street poles without drilling | Poles 80 to 200 mm diameter; band clamps only; inlets between 1.5 and 4 m above ground | Design review | Met by design |
| R12 | Survive outdoors | Pod inlets face down behind insect mesh with drip lid; electronics in the FieldNode IP65 enclosure; -10 to 50 °C | Design review, later field trial | At risk; condensation and insect ingress unverified |
| R13 | Light and compact on the pole | Mass 3.5 kg or less; frontal area 0.12 m² or less | Massing model | Met, about 3.0 kg and 0.09 m² (estimate) |
| R14 | Collect levels only | No images, audio or personal identifiers collected or sent | Design review | Met by design |
| R15 | Low cost | Parts $180 or less per node | Priced BOM | **Not met.** About $391 with the FieldNode core; about $265 for the sensor head alone |
| R16 | Serviceable in the field | NO2 sensor and PM sensor replaceable in 15 min at the pole with hand tools | Design review | At risk; access from a ladder unverified |

## Assumptions

- NO2 conversions use 1 ppb = 1.88 µg/m³ at 25 °C and 101.325 kPa.
- The WHO guideline level for annual NO2 is 10 µg/m³ and for PM2.5 is 5 µg/m³, as cited by the European Environment Agency ([EEA, 2024](https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024)). The EU annual limit value for NO2 is 40 µg/m³ under Directive 2008/50/EC, which also sets sampling inlets between 1.5 m and 4 m above ground ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050)).
- FieldNode allows about 115 mW average for sensors (FieldNode README, lab shared components set).
- R1 and R2 targets are proposals for review, set with reference to published field results; they are not taken from a standard.

---
doc_id: AST-REQ-001
title: AirStreet requirements
project: AirStreet
doc_type: Requirements
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from AST-CAL-001; R15 redefined as the sensor-head cost (AST-DDR-001 D1); R6, R8 and R11 rest on adopted choices
---

# AirStreet requirements

These requirements are checked by calculation in [AST-CAL-001](04-calcs/01-sizing.md). Targets remain proposals for review with the first co-design partner. R15 now covers the AirStreet sensor head only, with the FieldNode core costed in the FieldNode repo; this redefinition and the choices behind R6, R8 and R11 are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review ([AST-DDR-001](decisions/0001-trl2-review-decisions.md)). Three requirements are **not met** (R3, R13 and R15), six are at risk, three are met on paper and four are met by design.

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (AST-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Measure PM2.5 at street level | 0 to 500 µg/m³; hourly mean after humidity correction within ±5 µg/m³ or ±30 % (whichever is larger) of a collocated reference | CalRig chamber check, then field collocation | At risk: within the bound up to 80 % RH; outside it above 85 % RH, where water uptake makes the correction uncertain (AST-CAL-001 E) |
| R2 | Measure NO2 at street level | 0 to 200 ppb (about 0 to 380 µg/m³); hourly mean absolute error 5 ppb or less against a reference station after field calibration | Field collocation with a chemiluminescence reference station | At risk: hourly MAE about 3.9 ppb from a budget of literature and assumed terms (AST-CAL-001 C) |
| R3 | Resolve NO2 near the WHO annual guideline | Annual mean uncertainty 2 µg/m³ or less at 10 µg/m³ | Collocation statistics | **Not met.** Annual uncertainty about 4.2 µg/m³ (1σ); a reference-to-street transfer bias does not average away (AST-CAL-001 C) |
| R4 | Distinguish streets that exceed the EU NO2 limit value | Classify annual means above or below 40 µg/m³ with 90 % confidence | Collocation statistics | At risk: decisive only for annual means below 34.6 or above 45.4 µg/m³ |
| R5 | Measure temperature and humidity for corrections | ±0.5 °C and ±3 % RH inside the shield; radiation error 1 °C or less in full sun at 1 m/s wind | CalRig chamber check; side-by-side field test against an aspirated reference | At risk: SHT45 meets the sensor figures; shield error 0.43 to 0.89 K at 1 m/s, which reads 4.2 % RH low at 85 % RH |
| R6 | Calibrate with a stated method | T, RH and PM checked on CalRig before deployment; NO2 collocated with a reference station for at least 14 days before deployment and at least every 6 months | Calibration record per node | Met by design (AST-DDR-001 D3) |
| R7 | Keep raw data for recalibration | Send raw NO2 working and auxiliary electrode signals, PM, T and RH with a calibration version tag | Firmware and data schema review | Met by design |
| R8 | Report often enough for street maps | One record every 5 min; hourly means published within 15 min; 7 days of store and forward | Timing and storage calculation | Met on paper: 5 min records, hourly mean within about 5 min, 7 days in 40.3 kB |
| R9 | Fit the FieldNode power budget | Sensor average 115 mW or less; energy neutral at the FieldNode design sun hours | Power budget calculation | Met on paper: 48.0 mW design load; 1.29 Wh/day drawn against 7.75 Wh stored in the worst month; 11.9 days without sun |
| R10 | Stay within radio duty-cycle rules | LoRaWAN airtime below 1 % in EU868 sub-bands | Airtime calculation | Met on paper: 0.082 % at SF9, 0.60 % at SF12 |
| R11 | Mount on street poles without drilling | Poles 80 to 200 mm diameter; band clamps only; inlets between 1.5 and 4 m above ground | Design review | Met by design (inlet 3.0 m, AST-DDR-001 D7) |
| R12 | Survive outdoors | Pod inlets face down behind insect mesh with drip lid; electronics in the FieldNode IP65 enclosure; -10 to 50 °C | Design review, later field trial | At risk: FieldNode is rated to 45 °C ambient; SPS30 recommended range 20 to 80 % RH; condensation and insects unverified |
| R13 | Light and compact on the pole | Mass 3.5 kg or less; frontal area 0.12 m² or less | Massing model | **Not met.** 3.65 kg and 0.138 m² from the model; FieldNode is 2.41 kg, not the 1.7 kg assumed at TRL 2 |
| R14 | Collect levels only | No images, audio or personal identifiers collected or sent | Design review | Met by design |
| R15 | Low cost | AirStreet sensor-head parts $180 or less per node (`budget_usd`); FieldNode core excluded and costed in FieldNode | Priced BOM (AST-CAL-001 I) | **Not met.** Sensor head $283.00, against $180 (`budget_usd`) and the $280 proposed in AST-DDR-001, awaiting Amish; $409.00 with the FieldNode core |
| R16 | Serviceable in the field | NO2 sensor and PM sensor replaceable in 15 min at the pole with hand tools | Design review | At risk: about 14 min estimated; a new NO2 sensor needs collocation, so a pre-collocated spare pod is the practical exchange unit |

## Assumptions

- NO2 conversions use 1 ppb = 1.88 µg/m³ at 25 °C and 101.325 kPa.
- The WHO guideline level for annual NO2 is 10 µg/m³ and for PM2.5 is 5 µg/m³, as cited by the European Environment Agency ([EEA, 2024](https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024)). The EU annual limit value for NO2 is 40 µg/m³ under Directive 2008/50/EC, which also sets sampling inlets between 1.5 m and 4 m above ground ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050)).
- FieldNode allows 115 mW average for sensors at its 5-day autonomy ceiling, with 100 mW proposed as its published design value (FND-CAL-001); AirStreet fits either.
- The $280 sensor-head budget recommended in AST-DDR-001 D1 is recorded only; `budget_usd` in `project.yaml` stays $180 until Amish decides.
- R1 and R2 targets are proposals for review, set with reference to published field results; they are not taken from a standard.

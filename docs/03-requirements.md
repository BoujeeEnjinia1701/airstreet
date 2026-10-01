---
doc_id: AST-REQ-001
title: AirStreet requirements
project: AirStreet
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-09-30'
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-30'
  author: Amish Chadha
  change: Status from AST-CAL-001 v0.3 after the design was made constructable (AST-DDR-003); R13 and R15 not met, proposed to Amish
---

# AirStreet requirements

These requirements are checked by calculation in [AST-CAL-001](04-calcs/01-sizing.md) v0.3. Targets remain proposals for review with the first co-design partner. On 2026-09-25 Amish accepted the recommendations in [AST-DDR-001](decisions/0001-trl2-review-decisions.md) and [AST-DDR-002](decisions/0002-recommendations-accepted.md). As a result R3 is withdrawn and kept as a research question, R8, R12, R13, R15 and R16 are restated, and R15 uses the $285 `budget_usd`. On 2026-09-30 the design was made constructable ([AST-DDR-003](decisions/0003-design-for-construction.md)), which raised the mass and the sensor-head cost: two requirements are **not met** (R13 mass, R15 cost), both proposed to Amish with options; five are at risk, four are met on paper, four are met by design and one is withdrawn.

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (AST-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Measure PM2.5 at street level | 0 to 500 µg/m³; hourly mean after humidity correction within ±5 µg/m³ or ±30 % (whichever is larger) of a collocated reference | CalRig chamber check, then field collocation | At risk: within the bound up to 80 % RH; outside it above 85 % RH, where water uptake makes the correction uncertain (AST-CAL-001 E) |
| R2 | Measure NO2 at street level | 0 to 200 ppb (about 0 to 380 µg/m³); hourly mean absolute error 5 ppb or less against a reference station after field calibration | Field collocation with a chemiluminescence reference station | At risk: hourly MAE about 3.9 ppb from a budget of literature and assumed terms (AST-CAL-001 C) |
| R3 | Resolve NO2 near the WHO annual guideline | Withdrawn as a requirement (AST-DDR-002). Kept as a research question: can the annual mean be resolved to 2 µg/m³ at 10 µg/m³? | Collocation statistics (research) | Withdrawn. Annual uncertainty about 4.2 µg/m³ (1σ); AirStreet ranks streets and checks the EU limit (R4) and makes no WHO guideline claim |
| R4 | Distinguish streets that exceed the EU NO2 limit value | Classify annual means above or below 40 µg/m³ with 90 % confidence | Collocation statistics | At risk: decisive only for annual means below 34.6 or above 45.4 µg/m³ |
| R5 | Measure temperature and humidity for corrections | ±0.5 °C and ±3 % RH inside the shield; radiation error 1 °C or less in full sun at 1 m/s wind | CalRig chamber check; side-by-side field test against an aspirated reference | At risk: SHT45 meets the sensor figures; shield error 0.43 to 0.89 K at 1 m/s, which reads 4.2 % RH low at 85 % RH |
| R6 | Calibrate with a stated method | T, RH and PM checked on CalRig before deployment; NO2 collocated with a reference station for at least 14 days before deployment and at least every 6 months | Calibration record per node | Met by design (AST-DDR-001 D3) |
| R7 | Keep raw data for recalibration | Send raw NO2 working and auxiliary electrode signals, PM, T and RH with a calibration version tag | Firmware and data schema review | Met by design |
| R8 | Report often enough for street maps | One record every 5 min through a private gateway (TwinKit by default); one every 15 min on The Things Network; hourly means published within 15 min; 7 days of store and forward | Timing, airtime and storage calculation | Met on paper: 5 min records on the private gateway; at 15 min TTN fair use is met up to SF9; 7 days in 40.3 kB |
| R9 | Fit the FieldNode power budget | Sensor average 115 mW or less; energy neutral at the FieldNode design sun hours | Power budget calculation | Met on paper: 87.0 mW design load with the 60 s PM run; 2.33 Wh/day drawn against 7.75 Wh stored in the worst month; 6.6 days without sun |
| R10 | Stay within radio duty-cycle rules | LoRaWAN airtime below 1 % in EU868 sub-bands | Airtime calculation | Met on paper: 0.082 % at SF9, 0.60 % at SF12 |
| R11 | Mount on street poles without drilling | Poles 80 to 200 mm diameter; band clamps only; inlets between 1.5 and 4 m above ground | Design review | Met by design (inlet 3.0 m, AST-DDR-001 D7; 140° V-saddles and bands cut to length fit the range, AST-DDR-003) |
| R12 | Survive outdoors | Pod inlets face down behind insect mesh with drip lid; electronics in the FieldNode IP65 enclosure; -10 to 50 °C, with FieldNode's sun shield required at sites where ambient exceeds 45 °C | Design review, later field trial | At risk: the FieldNode sun shield is now designed (FND-DDR-003) and fixes to AirStreet's adapter plates (AST-DDR-003); SPS30 recommended range 20 to 80 % RH; condensation and insects unverified |
| R13 | Light and compact on the pole | Mass 3.5 kg or less; frontal area 0.15 m² or less (relaxed from 0.12 m², AST-DDR-002) | Constructable model | **Not met**: 3.84 kg (4.00 kg with FieldNode's sun shield) against 3.5 kg; frontal area 0.143 m², met. The constructable FieldNode core and the parts that make AirStreet buildable add 0.58 kg (AST-DDR-003, A1: proposed, awaiting Amish) |
| R14 | Collect levels only | No images, audio or personal identifiers collected or sent | Design review | Met by design |
| R15 | Low cost | AirStreet sensor-head parts $285 or less per node (`budget_usd`); FieldNode core excluded and costed in FieldNode | Priced BOM (AST-CAL-001 I) | **Not met**: sensor head $303.00, $18.00 over; $434.00 with the FieldNode core (AST-DDR-003, A2: proposed, awaiting Amish) |
| R16 | Serviceable in the field | Pre-collocated sensor pod exchanged in 15 min at the pole with hand tools; no sensor-level swaps at the pole (AST-DDR-002) | Design review | Met on paper: about 14 min for a pod exchange; the exchanged pod is serviced and recollocated at the reference site |

## Assumptions

- NO2 conversions use 1 ppb = 1.88 µg/m³ at 25 °C and 101.325 kPa.
- The WHO guideline level for annual NO2 is 10 µg/m³ and for PM2.5 is 5 µg/m³, as cited by the European Environment Agency ([EEA, 2024](https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024)). The EU annual limit value for NO2 is 40 µg/m³ under Directive 2008/50/EC, which also sets sampling inlets between 1.5 m and 4 m above ground ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050)).
- FieldNode allows 115 mW average for sensors at its 5-day autonomy ceiling, with 100 mW proposed as its published design value (FND-CAL-001); AirStreet fits either.
- `budget_usd` in `project.yaml` is $285 for the sensor head (AST-DDR-002).
- R1 and R2 targets are proposals for review, set with reference to published field results; they are not taken from a standard.

---
doc_id: AST-PRS-001
title: AirStreet product requirements and specifications
project: AirStreet
doc_type: Product requirements and specifications
version: "0.10"
status: Draft
date: '2026-10-30'
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
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R13 mass limit set at 4.0 kg including FieldNode's sun shield (AST-DDR-003 A1, accepted 2026-10-02); R13 now at risk"
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Status from AST-CAL-001 v0.6 with the four lightening steps carried into the design: R13 at risk to met on paper (3.78 kg with the sun shield); R15 over the target by $17.50; R5 figures updated"
- version: "0.9"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: AST-REQ-001 becomes AST-PRS-001; R1 to R16 become PR-001 to PR-016, each traced to a user requirement (AST-URS-001) with target, tolerance and units, the old number under Was; STEM check fixes of AST-DDR-005 (rated-range flags in PR-007, NO2 noise and ozone filter in AST-CAL-001 v0.7); PR-013 3.77 kg with the hollow shield spacers; PR-017 and PR-018 added for UR-014 and UR-015, proposed, awaiting Amish"
- version: "0.10"
  date: '2026-10-30'
  author: Amish Chadha
  change: "Amish's decisions of 2026-10-30 (AST-DDR-006): PR-004 against 40 and 20 ug/m3; PR-017 and PR-018 accepted; PR-019 added; PR-013 and PR-015 restated"
supersedes: AST-REQ-001
---

# AirStreet product requirements and specifications

What the node must do, each requirement traced to a user need in AST-URS-001 (links in AST-RTM-001, `03b-traceability.md`). Until kit 1.8 this document was AST-REQ-001; R1 to R16 are now PR-001 to PR-016 with the same text and targets, and the old number is in the "Was" column, which the calculation note AST-CAL-001 and earlier records still cite. The requirements are checked by calculation in [AST-CAL-001](04-calcs/01-sizing.md) v0.7 and by the STEM check [AST-STM-001](01b-stem-check.md); targets remain proposals for review with the first co-design partner.

On 2026-09-25 Amish accepted the recommendations in [AST-DDR-001](decisions/0001-trl2-review-decisions.md) and [AST-DDR-002](decisions/0002-recommendations-accepted.md): PR-003 (was R3) is withdrawn and kept as a research question, PR-008, PR-012, PR-013, PR-015 and PR-016 are restated, and PR-015 uses the $285 `budget_usd`. On 2026-09-30 the design was made constructable ([AST-DDR-003](decisions/0003-design-for-construction.md)); on 2026-10-02 Amish set PR-013's mass limit at 4.0 kg including FieldNode's sun shield, with the four lightening steps carried into the design. On 2026-10-24 the STEM check found four details to fix (AST-DDR-005, made under Amish's standing instruction of 2026-10-23): the NO2 noise term now follows the sensor datasheet, the NO2 cell is replaced before its ozone filter is used up, every record carries rated-range flags (PR-007), and the band thickness in the model matches the calculation; the hollow shield spacers of the D3 model take 0.01 kg off (PR-013 now 3.77 kg). The independent review of the same day corrected the NO2 budget (hourly MAE about 4.3 ppb, from 3.9) and the EU limit band; no status changed. Status: five at risk, five met on paper, six met by design (PR-017 and PR-018 among them, proposed), one over the value-engineering target and one withdrawn; none is not met.

Table 1. Product requirements and specifications. Status at TRL 3 from AST-CAL-001 v0.8 and AST-STM-001 v0.2.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | PM2.5 at street level | The node shall measure PM2.5 over 0 to 500 ug/m3 with an hourly mean, after humidity correction, within the tolerance of a collocated reference | 0 to 500 | ±5 ug/m3 or ±30 %, whichever is larger | ug/m3 | Analysis (AST-CAL-001 E), TRL 3; CalRig chamber check and field collocation, TRL 4 | At risk: within the bound up to 80 % RH; outside it at 85 % RH and above, where water uptake makes the correction uncertain | R1 |
| PR-002 | UR-002 | Performance | NO2 at street level | The node shall measure NO2 over 0 to 200 ppb (about 0 to 380 ug/m3) with an hourly mean absolute error after field calibration against a reference station | 5 | max | ppb (hourly MAE) | Analysis (AST-CAL-001 C), TRL 3; collocation with a chemiluminescence reference, TRL 4 | At risk: about 4.3 ppb from a budget of literature and assumed terms, with the datasheet noise over 12 independent records an hour and a 5 % slope term (AST-DDR-005 F1 and the independent review); hours outside the sensor's rated range are flagged (PR-007) | R2 |
| PR-003 | UR-003 | Performance | NO2 near the WHO annual guideline | Withdrawn as a requirement (AST-DDR-002). Research question: can the annual mean be resolved to 2 ug/m3 at 10 ug/m3? | 2 | max | ug/m3 (annual, 1 sigma) | Collocation statistics (research) | Withdrawn: annual uncertainty about 4.65 ug/m3 (1 sigma); no WHO guideline claim | R3 |
| PR-004 | UR-003 | Performance | Streets above the EU NO2 limit value | The data shall classify a street's annual NO2 mean above or below both 40 ug/m3 (Directive 2008/50/EC) and 20 ug/m3 (Directive (EU) 2024/2881, from 2030) with 90 % confidence | 40 and 20 | 90 % one-sided confidence | ug/m3 | Analysis (AST-CAL-001 C), TRL 3; collocation statistics, TRL 4 | At risk: decisive only below 33.9 or above 46.1 ug/m3 against 40, and below 13.9 or above 26.1 ug/m3 against 20 (at the directive's 20 degC; AST-CAL-001 [C9]). Both limits since Amish's decision 4 of 2026-10-30 (AST-DDR-006); the recast directive sets 20 ug/m3 from 2030 (AST-REG-001 A2) | R4 |
| PR-005 | UR-001, UR-002 | Performance | Temperature and humidity for corrections | The node shall measure air temperature and RH inside a radiation shield for the PM and NO2 corrections | ±0.5 degC, ±3 % RH; radiation error 1 degC or less in full sun at 1 m/s | max | degC; % RH | Analysis (AST-CAL-001 D), TRL 3; CalRig and side-by-side with an aspirated reference, TRL 4 | At risk: SHT45 meets the sensor figures; shield error 0.42 to 0.87 K at 1 m/s, which reads 4.1 % RH low at 85 % RH | R5 |
| PR-006 | UR-005 | Performance | Stated calibration method | T, RH and PM shall be checked on CalRig before deployment; NO2 shall be collocated with a reference station for at least 14 days before deployment and at least every 6 months | 14 days; 6 months | min; max | days; months | Inspection of the calibration record per node, TRL 4 | Met by design (AST-DDR-001 D3) | R6 |
| PR-007 | UR-006 | Software | Raw data for recalibration | The node shall send raw NO2 working and auxiliary electrode signals, PM, T and RH with a calibration version tag, and flags for readings outside the sensors' rated temperature and humidity ranges (AST-DDR-005 F2) | All raw signals, version tag, range flags | Pass or fail | n/a | Inspection of the firmware and data schema, TRL 4 | Met by design: flags set when the shield air is above 35 degC, RH above 80 % (PM) or 85 % (NO2) or below 20 % (PM) or 15 % (NO2), or below 10 degC (PM) | R7 |
| PR-008 | UR-004 | Software | Reporting for street maps | One record every 5 min through a private gateway (TwinKit by default), one every 15 min on The Things Network; hourly means published within 15 min; 7 days of store and forward | 5 (private), 15 (TTN); 15; 7 | max; max; min | min; min; days | Analysis of timing, airtime and storage (AST-CAL-001 B), TRL 3 | Met on paper: at 15 min TTN fair use is met up to SF9; 7 days in 40.3 kB | R8 |
| PR-009 | UR-013 | Electrical | FieldNode power budget | The sensor load shall fit FieldNode's allowance and be energy neutral at FieldNode's design sun hours | 115 (ceiling); 100 (design) | max | mW | Power budget (AST-CAL-001 A), TRL 3; energy log, TRL 4 | Met on paper: 87.0 mW design load; 2.33 Wh/day against 7.75 Wh stored in the worst month; 6.6 days without sun | R9 |
| PR-010 | UR-016 | Electrical | Radio duty cycle | LoRaWAN airtime shall stay below 1 % in each EU868 sub-band, and within the 400 ms dwell time in US915 | 1; 400 | max | %; ms | Airtime calculation (AST-CAL-001 B), TRL 3 | Met on paper: 0.082 % at SF9, 0.60 % at SF12; 247 ms at SF9 in US915 | R10 |
| PR-011 | UR-007 | Physical architecture | Pole mounting without drilling | The node shall fit poles 80 to 200 mm in diameter with band clamps only, inlets between 1.5 and 4 m above ground | 80 to 200; 1.5 to 4 | range | mm; m | Design review and model (AST-CAL-001 F), TRL 3 | Met by design: inlet 3.0 m (AST-DDR-001 D7); 140 degree V-saddles and bands cut to length | R11 |
| PR-012 | UR-009 | Physical architecture | Survive outdoors | Pod inlets face down behind insect mesh under a drip lid; electronics in FieldNode's IP65 enclosure; survive -10 to 50 degC, with FieldNode's sun shield at sites above 45 degC | -10 to 50 | range | degC | Design review (AST-CAL-001 H), TRL 3; field trial, TRL 4 | At risk: the NO2 cell is rated to 40 degC and 85 % RH and the SPS30 is recommended to 40 degC and 80 % RH, so hours beyond are flagged (PR-007); condensation and insects unverified | R12 |
| PR-013 | UR-008 | Physical architecture | Light and compact | Mass on the pole including FieldNode's sun shield, and frontal area seen from the street | 4.0; 0.15 | max | kg; m2 | Constructable model (AST-CAL-001 F), TRL 3; weighing, TRL 4 | Met on paper: 3.86 kg with the sun shield (3.70 kg without), 0.14 kg margin; 0.144 m2, 0.006 m2 under the limit, with the tube hood of AST-DDR-006; the pole owner's confirmation of the load is still to come | R13 |
| PR-014 | UR-011 | Software | Levels only | No images, audio or personal identifiers shall be collected or sent | None | Pass or fail | n/a | Design review, TRL 3 | Met by design | R14 |
| PR-015 | UR-012 | Cost | Low cost | AirStreet sensor-head parts at or under the $285 value-engineering target per node (`budget_usd`, a hypothetical control target); FieldNode core excluded and costed in FieldNode | 285 (value-engineering target) | max | USD | Priced BOM (AST-CAL-001 I), TRL 3 | **Over the value-engineering target by $21.00**: sensor head $306.00 (the tube hood and its fixings add $3.50); $437.00 with the FieldNode core | R15 |
| PR-016 | UR-010 | Maintenance | Serviceable in the field | A pre-collocated sensor pod shall be exchanged at the pole with hand tools; no sensor-level swaps at the pole (AST-DDR-002); the NO2 cell is replaced on the ground at the pod exchange every 12 months, or 18 or 24 where the site's ozone record keeps its filter under 500 ppm h (AST-DDR-005 F3) | 15 | max | min | Service time estimate (AST-CAL-001 H), TRL 3; timed exchange, TRL 4 | Met on paper: about 14 min for a pod exchange | R16 |
| PR-017 | UR-014 | Materials | Open and garage buildable | Every made part shall be printable in ASA on a 250 mm class printer, or cut and drilled from standard aluminium bar, angle and sheet with hand tools and a drill; bought parts are specified by class, not brand | All made parts by printing, sawing and drilling | Pass or fail | n/a | Inspection of the build plan AST-BLD-001 and the drawings, TRL 3 | Met by design (text accepted by Amish on 2026-10-30, AST-DDR-006) | |
| PR-018 | UR-015 | Safety | Installation and service safety | The node shall be installed and serviced only with the pole owner's written permission, from a work platform or secured ladder with traffic management, without opening the pole; mass and wind load are stated for the owner's check; the FieldNode cell is fused and protected | Owner's permission; no pole access; load stated | Pass or fail | n/a | Inspection of the build plan safety stops and AST-RSK-001, TRL 3 | Met by design (text accepted by Amish on 2026-10-30, AST-DDR-006) | |
| PR-019 | UR-003 | Performance | Independent check of annual NO2 | The anchor node of a network and one node in five shall carry a printed hood with three clips for NO2 diffusion tubes (Palmes type) under the cross arm, changed every two to four weeks by the partner, as an independent check of the annual NO2 means and of the street transfer bias | 3 tubes; 1 node in 5 and the anchor node; 2 to 4 weeks | min; min; range | tubes; nodes; weeks | Inspection of the model, BOM line 12 and drawing AST-DWG-110, TRL 3; tube results against the node's annual mean, TRL 4 | Met by design: hood and three clips in the model, 0.081 kg, $2.50 in the BOM; the tubes are bought with laboratory analysis (about £8 each, 2015 price) and are a running cost, not in the BOM (decision 2 of 2026-10-30, AST-DDR-006) | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- NO2 conversions use 1 ppb = 1.88 ug/m3 at 25 degC and 101.325 kPa.
- The WHO guideline level for annual NO2 is 10 ug/m3 and for PM2.5 is 5 ug/m3, as cited by the European Environment Agency ([EEA, 2024](https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024)). The EU annual limit value for NO2 is 40 ug/m3 under Directive 2008/50/EC, which also sets sampling inlets between 1.5 m and 4 m above ground ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050)); the recast Directive (EU) 2024/2881 lowers it to 20 ug/m3 from 2030 ([REHVA summary](https://www.rehva.eu/eu-policy/policy-issues/ambient-air-quality-directives-aaqd), checked 2026-10-24).
- FieldNode allows 115 mW average for sensors at its 5-day autonomy ceiling, with 100 mW proposed as its published design value (FND-CAL-001); AirStreet fits either.
- `budget_usd` in `project.yaml` is $285 for the sensor head (AST-DDR-002).
- PR-001 and PR-002 targets are proposals for review, set with reference to published field results; they are not taken from a standard.
- PR-017 and PR-018 were added on 2026-10-24 so that UR-014 and UR-015 each have a product requirement; Amish accepted their text as written on 2026-10-30 (AST-DDR-006). PR-019 was added on 2026-10-30 for the diffusion tube cross-check he chose.

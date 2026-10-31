---
doc_id: AST-FEA-001
title: AirStreet feasibility assessment
project: AirStreet
doc_type: Feasibility assessment
version: "0.2"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First feasibility assessment (kit 1.9.1 upgrade)
- version: "0.2"
  date: '2026-10-30'
  author: Amish Chadha
  change: "PR-004 wording follows decision 4 of 2026-10-30"
---

# AirStreet feasibility assessment

AirStreet is feasible to build and run as a prototype: every part is printed, cut from standard aluminium or bought, the power and radio budgets close on FieldNode's shared core, and the science holds (AST-STM-001); what is not yet shown is how accurate the sensors are on a real street after calibration, which only a collocation with a reference station at TRL 4 can show. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | The working principle (electrochemical NO2, laser-scattering PM, passive shield, field calibration by collocation) is established in the literature and in community networks; the constructable model passes 77 constructability checks and has no overlapping parts | High | PM2.5 above 85 % RH (PR-001), field NO2 accuracy (PR-002) and EU limit classification near 40 ug/m3 (PR-004) are at risk | AST-STM-001, AST-CAL-001, `cad/fidelity.json` |
| Materials | Printed ASA (UV stable), 6063 aluminium bar, angle and sheet, stainless bands and fasteners, brass inserts | High | Creep of the printed saddles under band preload in summer heat is plausible, to check at TRL 4 (S25) | AST-STM-001 S25, BOM |
| Manufacturing and assembly | A 3D printer with a 250 mm class bed, a saw, a drill and hand tools; 16 assembly steps in the build plan | High | Heat-set inserts need a soldering iron and a steady hand; the pod is the service exchange unit, so spare pods double the printing | AST-BLD-001 |
| Power and controls | 87.0 mW design sensor load inside FieldNode's 100 mW allowance; 6.6 days without sun; the NO2 bias held continuously on port B | High | Charging stops below 0 degC (S4); cold spells longer than 4.6 days at -20 degC would empty the cell | AST-CAL-001 A |
| Data and radio | 20-byte records every 5 min on a private gateway or 15 min on The Things Network; within EU868 and US915 rules | High | The radio band follows the partner (AST-DEC-001); range at SF9 in US915 to check in the field | AST-CAL-001 B, AST-REG-001 R1 to R3 |
| Calibration route | CalRig for T, RH and PM; 14-day collocation and every 6 months for NO2 | Medium | Needs a partner with a street-level reference station (AST-DEC-001); the street transfer bias is assumed (2 ppb) | AST-CAL-001 C, AST-PRC-001 |
| Supply of parts | SPS30 and SHT45 priced at retail (2026-09-25); NO2-B43F class cell and its front end estimated, not quoted | Medium | The NO2 cell and front end are single-source in practice; prices are indicative until quoted by a distributor | BOM, AST-MKT-001 |
| Regulatory | Indicative data only; radio rules met on paper; pole owner's permission needed per site | Medium | The 2030 EU NO2 limit of 20 ug/m3 changes what PR-004 classifies against (decided on 2026-10-30: both 40 and 20 ug/m3) | AST-REG-001 |

Ratings: High, Medium, Low.

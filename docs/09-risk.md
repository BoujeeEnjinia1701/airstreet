---
doc_id: AST-RSK-001
title: AirStreet risk register and hazard analysis
project: AirStreet
doc_type: Risk register
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First risk register, preliminary hazard analysis and first-pass design FMEA (kit 1.9.1 upgrade)
---

# AirStreet risk register and hazard analysis

The largest project risks are that no partner with a street-level NO2 reference station is found, and that the field NO2 accuracy after calibration is worse than the 5 ppb target; the largest hazards are work at height beside traffic and a node or part falling from the pole. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be found) to 5 (unlikely to be found).

> **Safety:** Mounting on a street pole is work at height next to traffic, beside a pole that carries mains voltage inside. Install only with the pole owner's written permission, by trained crews from a work platform or a secured ladder with a second person and traffic management, and never open the pole's access door. The FieldNode core holds a lithium iron phosphate cell; the NO2 cell holds an acid electrolyte.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No collocation partner | No city or agency with a street-level NO2 reference station agrees to host nodes and share data | NO2 cannot be calibrated; the method is unproven | 3 | 5 | Project lead | Approach the first candidate (TCEQ Dallas-Fort Worth network with a university or city partner, AST-DEC-001); keep a list of alternates |
| P2 | Field NO2 accuracy worse than 5 ppb hourly | Calibration residual, drift and street transfer bias larger than assumed (AST-CAL-001 C) | PR-002 not met; maps can rank streets only coarsely | 3 | 4 | Design lead | Collocation statistics at TRL 4; the diffusion tube cross-check (open decision 2) |
| P3 | PM2.5 wrong in humid weather | Water uptake above 85 % RH (PR-001) | Overestimated PM on humid nights and in humid climates | 4 | 3 | Design lead | Humidity flags (F2); collocation in the humid season; a switched inlet heater as a later idea (AST-OPT-001) |
| P4 | Pole owner refuses the load or the mount | 3.77 kg and 125 N of wind load at 3.3 m; insurance | No sites | 2 | 4 | Project lead | Give the owner the load and wind figures; no drilling or pole power (PR-011, PR-018) |
| P5 | FieldNode does not accept the adapter plate mount | AirStreet leaves off FieldNode's back plate (AST-DDR-002) | A redesign of the mount | 2 | 3 | Project lead | Cross-repo request already approved (AST-DEC-001) |
| P6 | Cost over the value-engineering target | NO2 cell and front end at about USD 150 together | USD 17.50 over the USD 285 target (PR-015) | 5 | 2 | Design lead | Open two-channel front end (TRL 4 work on hold); quotes from distributors |
| P7 | NO2 cell price or supply | One maker in practice; price not quoted | Cost and lead time | 3 | 3 | Design lead | Quote at TRL 4; name an equivalent class of cell |
| P8 | Theft or vandalism | Device in public reach at 3 m | Lost nodes and data | 2 | 3 | Partner organization | Inlet height 3.0 m; no exposed fixings below the pod; owner's inspection rounds |
| P9 | The 2030 EU limit makes PR-004 out of date | Directive (EU) 2024/2881 lowers the NO2 limit to 20 ug/m3 | Classification is against the wrong value | 4 | 2 | Project lead | Open decision 4 |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Fall from height | Installing or exchanging the pod at 3 m from a ladder | Serious injury | 5 | 2 | Work platform or secured ladder with a second person; the pod exchange is done whole, with no sensor work at height (PR-016) | Low with trained crews |
| H2 | Struck by traffic | Work beside the kerb | Serious injury | 5 | 2 | Traffic management as local rules require (AST-REG-001 S2); work from the footway side | Low |
| H3 | Falling node or part onto the footway | Band slip, a loose screw, a cracked printed part | Injury to the public | 4 | 2 | Two bands with a slip factor of 25 (AST-CAL-001 [G2]); nyloc nuts and inserts; re-torque at the first pod exchange (S25); safety stops in the build plan | Low; insert pull-out to check at TRL 4 |
| H4 | Electric shock from the pole | Opening the pole's access door or tapping pole power | Death | 5 | 1 | Never open the pole; AirStreet runs only on FieldNode's solar and battery supply (PR-018) | Very low |
| H5 | Lithium cell fire or venting | Damage, overcharge, charging below 0 degC or above the maker's limit, a hot site without the sun shield | Fire at height | 4 | 1 | Fused, protected LiFePO4 cell; charge temperature limits in FieldNode; sun shield above 45 degC (AST-DDR-002) | Low |
| H6 | Acid electrolyte | Crushing or heating an electrochemical cell | Burns to skin or eyes | 3 | 1 | Cells fitted and replaced on the ground, returned for disposal (AST-REG-001 S3) | Very low |
| H7 | Cuts | Band ends and cut aluminium | Minor cuts | 2 | 3 | Deburr, gloves (AST-BLD-001) | Low |
| H8 | Misleading data | Readings outside the sensors' rated range or before calibration taken at face value | Wrong decisions about a street | 3 | 3 | Rated-range flags in every record (F2); calibration version on every published value; data stated as indicative (PR-007) | Medium until collocation |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Bands and V-saddles | Hold the node on the pole | Preload lost, node slips or turns | Node drops or faces the wrong way | Creep of printed ASA, band housing slip | 4 | 2 | 3 | 24 | Band torque figure from the maker (AST-DEC-001 item 1); re-torque at the first pod exchange; creep check at TRL 4 |
| F2 | Pod hanging screws and inserts | Hold the pod under the cross arm | Insert pulls out | Pod falls | Insert set badly; ASA softened in sun | 4 | 2 | 3 | 24 | Insert pull-out test at TRL 4 (item 8); safety stop before the first lift |
| F3 | NO2 cell | Measure NO2 | Sensitivity loss or ozone breakthrough | NO2 biased | Ozone filter used up; electrolyte dried at high temperature | 3 | 3 | 2 | 18 | Replacement every 12 months, or 18 to 24 with the site's ozone record (F3); 6-monthly collocation; flags above 35 degC and outside 15 to 85 % RH (F2) |
| F4 | Particle sensor | Measure PM | Fan or optics fouled | PM biased low | Dust and traffic spray | 3 | 3 | 3 | 27 | Duty cycle of 60 s in 300 s; checked at each CalRig visit |
| F5 | Radiation shield | Give air temperature and RH | Warm bias in low wind | RH low, PM correction wrong | Too little air through the plates | 3 | 3 | 3 | 27 | Side-by-side with an aspirated reference at TRL 4 (PR-005) |
| F6 | Pod | Keep rain and insects out of the sensors | Water or insects reach the sensors | Sensor failure or false PM | Driven rain under the drip lid; nests | 3 | 3 | 2 | 18 | Mesh aperture to confirm (item 9); inspection at the pod exchange |
| F7 | Sensor cables and glands | Carry power and data to FieldNode | Water in a gland or plug | Lost data, corrosion | Gland not tightened; plug not seated | 3 | 2 | 2 | 12 | Gland check in the pod exchange steps; uplink check before leaving the pole |
| F8 | Front end and ADC | Hold the bias and read WE and AE | Bias lost on a power dip | Hours of settling after each dip | Port B not always on | 3 | 2 | 3 | 18 | FieldNode's confirmation of the always-on port B (AST-DEC-001 action 4) |
| F9 | FieldNode core | Power and radio | Cell empty in a long cold spell | Gap in data | No charging below 0 degC (S4) | 2 | 2 | 1 | 4 | Partner climate data; store and forward 7 days |
| F10 | Adapter plates | Carry the FieldNode enclosure and panel bracket | Crack at a lightening window corner | Enclosure loose | Vibration; window corner radius too small | 3 | 1 | 3 | 9 | 5 mm corner radius and 5 mm of metal round every hole (AST-DDR-003) |

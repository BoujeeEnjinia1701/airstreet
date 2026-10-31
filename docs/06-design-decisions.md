---
doc_id: AST-DEC-001
title: AirStreet design decisions register
project: AirStreet
doc_type: Design decisions register
version: "0.6"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Register opened with the open decisions from REVIEW.md, the decision records and the build plan work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for open decisions 1 to 8 (2026-10-02); moved to decisions made (AST-DDR-003 accepted)"
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Value engineering restated after the A1 lightening (USD 302.50, USD 17.50 over); actions that carry the 2026-10-02 decisions outside the design listed"
- version: "0.5"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: open decisions 1 to 5 (concept selection, diffusion tube cross-check, flagged hot hours, the 2030 EU limit, PR-017 and PR-018), proposed, awaiting Amish; STEM check fixes F1 to F5 recorded as decided under Amish's standing instruction of 2026-10-23 (AST-DDR-005)"
- version: "0.6"
  date: '2026-10-30'
  author: Amish Chadha
  change: "Amish decided open decisions 1 to 5 on 2026-10-30 (AST-DDR-006); the tube hood (decision 2) added to the design, cost USD 306.00; actions 7 and 8 added"
---

# AirStreet design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. Amish decided all five on 2026-10-30 ("on the calls - i go with your recommendations"); see "Decisions made" below and AST-DDR-006. Two follow-on actions are listed under "Actions that carry the decisions outside the design".

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The band roll and housings close round both an 80 mm and a 200 mm pole with the saddle, and the band maker's torque for about 1,000 N of preload | The slip and twist checks assume 1,000 N per band | AST-CAL-001 [F7], [G2] |
| 2 | The NO2 front end board's size and mounting holes (model: 86 x 55 mm, holes 76 x 43 mm apart) and how the B4 sensor connects to it | They set the back wall bosses and the lead length to the sensor | AST-DDR-003, P8 |
| 3 | The particle sensor's interface select pin and logic levels on its datasheet | Sets the terminal block wiring | Build plan section 3.10 |
| 4 | Heat-set insert sizes (M5 and M3) and the hole size their maker gives | The printed holes are drawn 6.8 and 4.0 mm | AST-DWG-102, 106, 109 |
| 5 | The M8 4-pin socket's panel hole and the M16 glands' hole size | The pod's printed holes are 8.2 and 16.2 mm | AST-DWG-106 |
| 6 | FieldNode's enclosure lug kit positions match FieldNode's back plate pattern | The adapter plates copy that pattern | FND-DDR-003 |
| 7 | The FieldNode panel's frame has a flat back lip at least 12 mm wide | FieldNode's panel clips bolt through it | FND-DDR-003 |
| 8 | The pull-out strength of the M5 heat-set inserts in printed ASA (at least 200 N assumed in the STEM check) | The pod hangs on two of them | AST-STM-001 S26 |
| 9 | The insect mesh aperture against the smallest local insects | Insects and spiders in the pod | AST-STM-001 S31 |

## Value engineering

Value-engineering target: USD 285. Estimated cost of the constructable design: USD 306.00 (USD 21.00 over the target).

The target is `budget_usd`, a hypothetical control target, not a limit, and covers the sensor head only; with the FieldNode core, which is costed in FieldNode, the node is USD 437.00. Main cost drivers and savings worth trying:

- The rise from USD 285 came from making the design constructable (AST-DDR-003): line 3, band stock, adapter plates and cross arm (USD 4.50, after the A1 lightening: the thinner rail saves about USD 0.50 and the saddles are repriced at about USD 3.00 of filament at 40 % infill); line 9, probe tube (USD 1); line 10, probe lead with its M8 plug (USD 4); and line 11, inserts, glands, probe socket, terminal block and fixings (USD 8). Line 8 is back to USD 9.00: the 1.5 mm shield plates save about as much filament as the spacers use.
- The tube hood (decision 2 of 2026-10-30, AST-DDR-006) added USD 3.50: line 12, the printed hood and three clips (about 0.081 kg of ASA, USD 2.50, an estimate), and USD 1.00 in line 11 for two inserts, two screws and two washers (an estimate). The tubes are a running cost, not in the BOM. `budget_usd` is not raised.
- Savings worth trying: the open two-channel NO2 front end (about USD 35 cheaper, PCB work that is on hold with TRL 4) would recover the USD 21.00, and cheaper band hardware and fixings can be sought at purchase.

## Actions that carry the decisions outside the design

These follow from decisions already made; none is an open decision.

| # | Action | Who | From |
| --- | --- | --- | --- |
| 1 | Ask the pole owner of the first site to confirm a load of 4.0 kg on the pole (3.86 kg with the sun shield as designed) and about 125 N of wind load 3.3 m up | Amish, once a site is chosen | Mass decision (R13), 2026-10-02 |
| 2 | Approach the first candidate partner, the Texas Commission on Environmental Quality's Dallas-Fort Worth monitoring network, with a local university or city partner; nothing is agreed yet | Amish | First partner decision, 2026-10-02 |
| 3 | When the partner is agreed, fix the radio band and FieldNode antenna in the BOM; for US915, restate R10 against the 400 ms dwell limit (SF9 or lower) | Next design update after the partner is agreed | Radio band decision, 2026-10-02 |
| 4 | Send FieldNode the adapter plate request and track its confirmation of port B's always-on 5 V and the 5 min private-gateway interval | Cross-repo (see REVIEW.md) | Decisions of 2026-10-02 on FieldNode |
| 5 | Propose the common M12 pin assignment to FieldNode, with CurbCount; once FieldNode agrees, update the pod wiring in build plan section 3.10 and its wiring picture | Cross-repo (see REVIEW.md) | Pin assignment decision, 2026-10-02 |
| 6 | Check LoRaWAN signal strength with the pod fitted; move the pod 8 mm left in the model and pictures only if the check shows a loss | TRL 4 (on hold) | Antenna whip decision, 2026-10-02 |
| 7 | When the partner is agreed, seek a NO2 cell rated above 40 degC with the partner (decision 3, option (b)) | Amish, with the partner | Decision 3, 2026-10-30 |
| 8 | Agree with the partner who buys and analyses the diffusion tubes (about £8 each with analysis, 2015 price), changes them every two to four weeks, and which nodes carry the hood (the anchor node and one in five); plan the extra climbs (hazard H9) | Amish, with the partner | Decision 2, 2026-10-30 |

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-30 | Decision 1, concept selection: option A, the current design (221 of 260 against 198 for C and 188 for B; no option within 10 %), kept as the design of record. `concept_chosen: A` | Amish: "on the calls - i go with your recommendations." | AST-DDR-004 (accepted), AST-DDR-006, AST-OPT-001 |
| 2026-10-30 | Decision 2, diffusion tube cross-check: option (a), triplicate NO2 diffusion tubes at the anchor node and one node in five. A printed hood with three tube clips hangs from the cross arm (no change to the arm); the tubes are changed every two to four weeks by the partner. In the model, BOM line 12 and drawing AST-DWG-110 | Amish: "on the calls - i go with your recommendations." | AST-DDR-006, AST-OPT-001 |
| 2026-10-30 | Decision 3, validity above the sensors' rated range: option (a) now, accept flagged hours (the flags of AST-DDR-005 F2 stay); (b), seeking a NO2 cell rated above 40 degC, follows when the partner is agreed (action 7 below) | Amish: "on the calls - i go with your recommendations." | AST-DDR-006, AST-DDR-005 F2 |
| 2026-10-30 | Decision 4, PR-004 target: option (b), classify against both 40 and 20 ug/m3; the band is 33.9 to 46.1 round 40 and 13.9 to 26.1 round 20 | Amish: "on the calls - i go with your recommendations." | AST-DDR-006, AST-CAL-001 [C9] |
| 2026-10-30 | Decision 5, text of PR-017 and PR-018: option (a), accepted as written | Amish: "on the calls - i go with your recommendations." | AST-DDR-006, AST-PRS-001 |
| 2026-10-24 | F1: NO2 noise per sample taken from the NO2-B43F data sheet (7.5 ppb, 1 sigma), averaged over the 12 independent records of an hour, with a 5 % slope term (the last two after the independent review); hourly total 5.45 ppb, MAE about 4.3 ppb | Decided under Amish's standing instruction of 2026-10-23 ("propose and implement the best fix ... and record it in DEC as decided under that instruction"); reversible by Amish | AST-DDR-005 F1 |
| 2026-10-24 | F2: rated-range flags in every record (shield air above 35 degC, RH above 80 % for PM or 85 % for NO2 and below 20 % or 15 %, below 10 degC for PM); flagged hours published with the flag | Decided under the standing instruction of 2026-10-23 | AST-DDR-005 F2 |
| 2026-10-24 | F3: the NO2 cell is replaced every 12 months at the pod exchange, or at 18 or 24 months where the site's ozone record keeps its filter under 500 ppm h | Decided under the standing instruction of 2026-10-23 | AST-DDR-005 F3 |
| 2026-10-24 | F4: band drawn 12.7 x 0.6 mm and read by the calculation | Decided under the standing instruction of 2026-10-23 | AST-DDR-005 F4 |
| 2026-10-24 | F5: D3 model fit details (pod boss webs, M3 insert holes in the back wall bosses, hollow shield spacers, probe lead route, M5 x 14 arm screws with washers) | Made under Amish's 2026-09-30 instruction to make the design physically buildable | AST-DDR-005 F5 |
| 2026-09-25 | TRL 2 review items D1 to D9: budget covers the sensor head only; pitch wording; NO2 collocation plan; NO2-B43F class sensor; ISB class front end bought first; SPS30 class particle sensor; 3.0 m inlets; 5 min records with raw signals; open data | Amish: "i accept all your recommendations, go with them across all repos." | AST-DDR-001, AST-DDR-002 |
| 2026-09-25 | `budget_usd` $285 for the sensor head; FieldNode back plate left off with the enclosure and bracket on the AirStreet rail; frontal area limit 0.15 m²; R3 (WHO guideline) withdrawn and kept as research; 60 s particle run; 5 min records on a private gateway and 15 min on The Things Network; FieldNode sun shield at sites above 45 °C; pre-collocated pod exchange for service | Amish, same instruction: go with recommendation | AST-DDR-002, N1 to N7 |
| 2026-10-02 | Design for construction accepted as a whole: the changes P1 to P10 (adapter plates, 140° V-saddles, bands in saddle grooves, cross arm, two-part pod, cable entries, shield spacers and probe tube) and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | AST-DDR-003, Table 1 |
| 2026-10-02 | Mass (R13): option (c). The R13 limit is set at 4.0 kg including FieldNode's sun shield, the pole owner is asked to confirm that load, and the four lightening steps (saddles at 40 % infill, 40 x 4 mm rail, 1.5 mm shield plates, windows in the adapter plates) are carried into the TRL 4 build to give margin | Amish: "i approve your recommendations for all 555 open decisions." | AST-DDR-003, A1 |
| 2026-10-02 | Antenna whip: accept the 15 mm clearance to the pod's drip lid and check signal strength with the pod fitted at TRL 4; move the pod 8 mm left only if that check shows a loss | Amish: "i approve your recommendations for all 555 open decisions." | AST-DDR-003, A3 |
| 2026-10-02 | First partner chosen by one rule: a city or air agency that runs a regulatory NO2 reference station at a street-level site AirStreet can mount beside, and that will share its data. First candidate to approach: the Texas Commission on Environmental Quality's Dallas-Fort Worth monitoring network, with a local university or city partner | Amish: "i approve your recommendations for all 555 open decisions." | AST-DDR-001, O1 |
| 2026-10-02 | Agree with FieldNode: send FieldNode the request to mount its enclosure, plate clips and sun shield on AirStreet's two adapter plates, and to keep its model stable since AirStreet carries a copy | Amish: "i approve your recommendations for all 555 open decisions." | AST-DDR-002 N2, AST-DDR-003 |
| 2026-10-02 | Port B's always-on 5 V supply and the 5 min interval on a private gateway: closed as already decided on 2026-09-25 (AST-DDR-002, N5 and its cross-repo actions); FieldNode's confirmation is tracked as a cross-repo action, not a decision | Amish: "i approve your recommendations for all 555 open decisions." | AST-DDR-002 |
| 2026-10-02 | FieldNode port pin assignment: propose to FieldNode one common assignment for both M12 ports (supply, ground, I2C data, I2C clock and one spare line), with each port's supply voltage set per project by its supply module (5 V on both ports for AirStreet) | Amish: "i approve your recommendations for all 555 open decisions." | FND-DDR-001, O2 |
| 2026-10-02 | Radio band set with the partner of the first-partner decision above (not with the adapter plates, as the register said): US915 for a North American partner, EU868 for a European one, with the matching FieldNode antenna | Amish: "i approve your recommendations for all 555 open decisions." | FND-DDR-001, O1 |

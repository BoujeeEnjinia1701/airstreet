---
doc_id: AST-DEC-001
title: AirStreet design decisions register
project: AirStreet
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-02'
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
---

# AirStreet design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

## Value engineering

Value-engineering target: USD 285. Estimated cost of the constructable design: USD 302.50 (USD 17.50 over the target).

The target is `budget_usd`, a hypothetical control target, not a limit, and covers the sensor head only; with the FieldNode core, which is costed in FieldNode, the node is USD 433.50. Main cost drivers and savings worth trying:

- The rise from USD 285 came from making the design constructable (AST-DDR-003): line 3, band stock, adapter plates and cross arm (USD 4.50, after the A1 lightening: the thinner rail saves about USD 0.50 and the saddles are repriced at about USD 3.00 of filament at 40 % infill); line 9, probe tube (USD 1); line 10, probe lead with its M8 plug (USD 4); and line 11, inserts, glands, probe socket, terminal block and fixings (USD 8). Line 8 is back to USD 9.00: the 1.5 mm shield plates save about as much filament as the spacers use.
- Savings worth trying: the open two-channel NO2 front end (about USD 35 cheaper, PCB work that is on hold with TRL 4) would recover the USD 17.50, and cheaper band hardware and fixings can be sought at purchase.

## Actions that carry the decisions outside the design

These follow from decisions already made; none is an open decision.

| # | Action | Who | From |
| --- | --- | --- | --- |
| 1 | Ask the pole owner of the first site to confirm a load of 4.0 kg on the pole (3.78 kg with the sun shield as designed) and about 125 N of wind load 3.3 m up | Amish, once a site is chosen | Mass decision (R13), 2026-10-02 |
| 2 | Approach the first candidate partner, the Texas Commission on Environmental Quality's Dallas-Fort Worth monitoring network, with a local university or city partner; nothing is agreed yet | Amish | First partner decision, 2026-10-02 |
| 3 | When the partner is agreed, fix the radio band and FieldNode antenna in the BOM; for US915, restate R10 against the 400 ms dwell limit (SF9 or lower) | Next design update after the partner is agreed | Radio band decision, 2026-10-02 |
| 4 | Send FieldNode the adapter plate request and track its confirmation of port B's always-on 5 V and the 5 min private-gateway interval | Cross-repo (see REVIEW.md) | Decisions of 2026-10-02 on FieldNode |
| 5 | Propose the common M12 pin assignment to FieldNode, with CurbCount; once FieldNode agrees, update the pod wiring in build plan section 3.10 and its wiring picture | Cross-repo (see REVIEW.md) | Pin assignment decision, 2026-10-02 |
| 6 | Check LoRaWAN signal strength with the pod fitted; move the pod 8 mm left in the model and pictures only if the check shows a loss | TRL 4 (on hold) | Antenna whip decision, 2026-10-02 |

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
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

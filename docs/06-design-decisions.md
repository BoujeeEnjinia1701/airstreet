---
doc_id: AST-DEC-001
title: AirStreet design decisions register
project: AirStreet
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
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
---

# AirStreet design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction as a whole: the changes that make the node buildable (adapter plates, 140° V-saddles, bands in saddle grooves, cross arm, two-part pod, cable entries, shield spacers and probe tube) | Accept; or ask for changes | Accept | The whole build plan | AST-DDR-003, Table 1 |
| 2 | Mass on the pole: 3.84 kg (4.00 kg with FieldNode's sun shield) against R13's 3.5 kg | (a) raise the R13 limit to 4.0 kg, pole owner to confirm the load; (b) lighten (saddles at 40 % infill, 40 x 4 mm rail, 1.5 mm shield plates, windows in the adapter plates) to about 3.6 kg, still over; (c) both | (c) | Rail, plates and printed parts; first check "Mass" | AST-DDR-003, A1 |
| 3 | Antenna whip 15 mm from the pod's drip lid (23 mm in the concept) | (a) accept and check the radio link with the pod fitted at TRL 4; (b) move the pod 8 mm further left | (a) | Pod position on the cross arm | AST-DDR-003, A3 |
| 4 | First partner, city and reference station for co-design and collocation | Open; no recommendation made | None yet | Not part of the TRL 3 build; sets the radio band and the first site | AST-DDR-001, O1 |
| 5 | FieldNode to accept its enclosure, plate clips and sun shield on AirStreet's two adapter plates in place of its back plate | Agree with FieldNode; or restore FieldNode's back plate (heavier) | Agree with FieldNode | Sections 3.3 and 3.5 of the build plan | AST-DDR-002 N2, AST-DDR-003 |
| 6 | FieldNode to keep port B's 5 V supply on at all times for the NO2 bias, and to allow a 5 min interval on a private gateway | Agree with FieldNode | Agree | Pod wiring and FieldNode's firmware (not part of the TRL 3 build) | AST-DDR-002 |
| 7 | Port pin assignment of FieldNode's two M12 ports | Agreed between FieldNode and the projects that use it | None yet (FieldNode's decision) | Pod wiring, section 3.10 | FND-DDR-001, O2 |
| 8 | Radio band and antenna for the pilot region | Follows decision 5 | None yet | FieldNode's antenna | FND-DDR-001, O1 |

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

Value-engineering target: USD 285 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 303 for the sensor head (USD 18 over the target); USD 434 with the FieldNode core, which is costed in FieldNode. Main cost drivers and savings worth trying:

- The rise from USD 285 came from making the design constructable (AST-DDR-003): line 3, band stock, adapter plates and cross arm (USD 4); line 8, spacers (USD 1); line 9, probe tube (USD 1); line 10, probe lead with its M8 plug (USD 4); and line 11, inserts, glands, probe socket, terminal block and fixings (USD 8).
- Savings worth trying: the open two-channel NO2 front end (about USD 35 cheaper, PCB work that is on hold with TRL 4) would recover the USD 18, and cheaper band hardware and fixings can be sought at purchase.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: budget covers the sensor head only; pitch wording; NO2 collocation plan; NO2-B43F class sensor; ISB class front end bought first; SPS30 class particle sensor; 3.0 m inlets; 5 min records with raw signals; open data | Amish: "i accept all your recommendations, go with them across all repos." | AST-DDR-001, AST-DDR-002 |
| 2026-09-25 | `budget_usd` $285 for the sensor head; FieldNode back plate left off with the enclosure and bracket on the AirStreet rail; frontal area limit 0.15 m²; R3 (WHO guideline) withdrawn and kept as research; 60 s particle run; 5 min records on a private gateway and 15 min on The Things Network; FieldNode sun shield at sites above 45 °C; pre-collocated pod exchange for service | Amish, same instruction: go with recommendation | AST-DDR-002, N1 to N7 |

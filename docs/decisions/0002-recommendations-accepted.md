---
doc_id: AST-DDR-002
title: AirStreet recommendations accepted
project: AirStreet
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Item O1 decided by Amish on 2026-10-02 (AST-DEC-001)"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below that carried a recommendation is decided by Amish, 2026-09-25: go with recommendation.

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This record covers every AirStreet item that was "Proposed, awaiting Amish" or "Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review" and that carried a recommendation, in `docs/REVIEW.md` (both 2026-09-25 sessions) and in [AST-DDR-001](0001-trl2-review-decisions.md). Where a recommendation offered several options, the recommended option is the decision. Items with no recommendation stay open. The portfolio stays at TRL 3: any decision that needs building, buying, testing or field work is recorded as decided but on hold, because TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, TRL 3, "Still awaiting Amish") and in AST-DDR-001, Table 1.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 to D9 | TRL 2 review items (AST-DDR-001) | Budget scope, pitch, NO2 collocation plan, NO2-B43F class sensor, ISB class front end bought first, SPS30 class PM sensor, 3.0 m inlets, reporting and raw signals, open data | AST-DDR-001 v0.2 status wording; AST-PRB-001, AST-PRC-001 and AST-REQ-001 no longer describe these as open for review. Buying the front end (D5), field collocation (D3) and publishing data (D9) are on hold with TRL 4 |
| N1 | Budget figure | Set `budget_usd` to about $285 for the sensor head; revisit the open front end later | `project.yaml` `budget_usd` $180 to $285; README budget line; R15 target $285. Sensor head $285.00 (was $283.00; +$2 for the adapter bars of N2), R15 met on paper with no margin. The open two-channel front end is PCB work and on hold with TRL 4 |
| N2 | Mass and area (R13) | Option (a): leave off FieldNode's back plate and fix its enclosure and bracket to the AirStreet rail, agreed with FieldNode; plus relax the area limit to 0.15 m² | `cad/src/model.py`: `fnd_plate` False, enclosure on the rail, two 180 x 25 x 3 mm adapter bars for the panel bracket feet; STEP and STL re-exported; AST-DWG-001 P1 to P2; BOM line 3 $15.00 to $17.00. Mass 3.65 to 3.26 kg (3.19 kg quoted before left out the adapters), frontal area 0.138 to 0.126 m² against a limit raised from 0.12 to 0.15 m²; R13 met on paper. FieldNode's agreement is a cross-repo action |
| N3 | WHO guideline (R3) | Drop R3 as a requirement; keep it as an open research question | R3 withdrawn in AST-REQ-001 v0.4; research question in AST-PRC-001 and AST-PRB-001. Annual uncertainty unchanged at about 4.2 µg/m³ |
| N4 | PM run length | 60 s run per 5 min record | `sizing.py` run 30 to 60 s; design sensor load 48.0 to 87.0 mW (inside 100 mW); daily draw 1.29 to 2.33 Wh; autonomy without sun 11.9 to 6.6 days (4.6 days at -20 °C); media flow label |
| N5 | Fair use on The Things Network | 5 min records on the private TwinKit gateway; 15 min on TTN | R8 restated; AST-CAL-001 [B8]: at 15 min, 12.8 s/day at SF8 and 23.7 s/day at SF9, inside 30 s; SF10 (43.5 s/day) is not. Firmware rule recorded in AST-PRC-001; firmware itself is on hold with TRL 4 |
| N6 | R12 temperature range | Require FieldNode's sun shield at sites above 45 °C | R12 target restated; AST-PRC-001 components, choices and safety; BOM line 1 note. The shield is FieldNode's to design (cross-repo action); R12 stays at risk |
| N7 | Service unit (R16) | Exchange a pre-collocated pod rather than individual sensors at the pole | R16 restated; AST-CAL-001 H re-estimated for a pod exchange, about 14 min against 15 min; R16 at risk to met on paper. Spare pods are a fleet cost, noted in `bom/bom-notes.md` |

*Table 2. Items open on 2026-09-25; O1 decided on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner, city and reference station for co-design and collocation. No recommendation was made. | Decided by Amish, 2026-10-02: a city or air agency with a street-level regulatory NO2 reference station that will share its data; first candidate to approach, TCEQ's Dallas-Fort Worth monitoring network with a local university or city partner (AST-DEC-001) |

## Consequences

- Requirement status (AST-CAL-001 v0.2): none not met (was R3, R13 and R15); five at risk (R1, R2, R4, R5, R12); six met on paper (R8, R9, R10, R13, R15, R16); four met by design (R6, R7, R11, R14); R3 withdrawn.
- Documents revised with the change "Recommendations accepted by Amish (DDR-002)": AST-PRB-001 v0.4, AST-PRC-001 v0.4, AST-REQ-001 v0.4, AST-CAL-001 v0.2, AST-DDR-001 v0.2; drawing AST-DWG-001 Rev P2.
- Cross-repo actions, not made here: FieldNode to accept an enclosure mounted without its back plate and bracket feet on AirStreet adapter bars (N2), to provide the sun shield for sites above 45 °C (N6), to keep port B's 5 V rail on continuously for the NO2 bias, and to allow a 5 min interval on a private gateway (N5); TwinKit to serve as the default private gateway (N5); CalRig to take the pod across two bays if it is checked assembled.
- TRL stays at 3. Nothing was built, bought or tested.

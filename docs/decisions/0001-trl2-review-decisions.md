---
doc_id: AST-DDR-001
title: AirStreet TRL 2 review decisions
project: AirStreet
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Items D1 to D9 are decided by Amish, 2026-09-25: go with recommendation ([AST-DDR-002](0002-recommendations-accepted.md)). Item O1 had no recommendation and remains "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish", nine of them with a recommendation. On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carries a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. None of them is recorded as decided or approved by Amish. The item without a recommendation stays open.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in AST-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items decided (v0.1 recorded them as adopted for TRL 3 work, open for review; accepted by Amish on 2026-09-25).*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Budget | Option (a): `budget_usd` covers the AirStreet sensor head only; the FieldNode core is costed in the FieldNode repo. R15 is redefined as the sensor-head cost. The figure itself was set at $285 under AST-DDR-002 (the $280 recommended here was overtaken by the TRL 3 price of $283.00). | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Pitch wording | "A street-level air quality node measuring PM2.5 and NO2, with particles checked on CalRig and NO2 calibrated against a reference station, for neighborhood-scale pollution maps." Applied to `project.yaml` and `README.md`. | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | NO2 calibration method | Field collocation with a regulatory reference station for at least 14 days before deployment and at least every 6 months after, with one permanently collocated anchor node; multiple linear regression first, random forest later. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | NO2 sensor | Alphasense NO2-B43F class (four electrodes, ozone filter), not a three-electrode sensor. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | NO2 front end | Buy an ISB class board for the first units; the open two-channel potentiostat stays a later cost option. | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | PM sensor | Sensirion SPS30 class, not a Plantower PMS5003 class sensor. | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Inlet height | About 3.0 m above the sidewalk, within the EU 1.5 to 4 m range. | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | Reporting | One record every 5 min, PM sensor run 30 s per record, raw signals sent. | Decided by Amish, 2026-09-25: go with recommendation |
| D9 | Open data | Publish calibrated hourly data, with the calibration version, to an open platform such as OpenAQ, subject to the partner's agreement. | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner, city and reference station for co-design and collocation. No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: pitch replaced per D2; `budget_usd` set to $285 under AST-DDR-002 (D1 fixed its scope, the sensor head). The problem line is unchanged, since no rewording was recommended.
- AST-REQ-001 v0.3: R15 now covers the sensor head only, with the FieldNode core excluded and costed in FieldNode (D1). Targets for R6, R8 and R11 are unchanged but now rest on adopted rather than proposed choices (D3, D7, D8).
- AST-PRC-001 v0.3 and AST-PRB-001 v0.3: the design choices above are no longer shown as proposed; they are adopted for TRL 3 work, open for Amish's review.
- AST-CAL-001 v0.2 states the sensor-head cost, $285.00, against the $285 `budget_usd`.
- The TRL 3 calculations raised further items; Amish accepted their recommendations on 2026-09-25, and they are recorded in AST-DDR-002.
- Purchasing (D5), field collocation (D3) and data publication (D9) are TRL 4 and later work and are on hold by Amish's instruction.

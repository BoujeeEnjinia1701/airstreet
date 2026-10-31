---
doc_id: AST-DDR-004
title: AirStreet concept selection
project: AirStreet
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Concept selection among options A, B and C of AST-OPT-001 (kit 1.9.1 upgrade); recommendation A, proposed, awaiting Amish"
- version: "0.2"
  date: '2026-10-30'
  author: Amish Chadha
  change: "Accepted by Amish on 2026-10-30 (option A)"
---

# 0004: Concept selection

- **Date:** 2026-10-24
- **Status:** accepted. Amish, 2026-10-30: "on the calls - i go with your recommendations." The recommendation was option A, the current design; decision 1 of the design decisions register AST-DEC-001 (recorded in AST-DDR-006).

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements (STANDARDS section 21), and kit 1.9 asks for each to be modelled to the repo's detail level (D3 at P3). AirStreet was designed before kit 1.8, so its current design is option A and is not redesigned without Amish's go. The user requirements are AST-URS-001; the options, their numbers and the scoring are in AST-OPT-001; their science is in AST-STM-001.

## Options considered

| Option | Working principle | Score (of 260) | Main strength | Main weakness |
| --- | --- | --- | --- | --- |
| A, electrochemical and optical node on FieldNode (current) | Naturally ventilated pod with an electrochemical NO2 cell and a laser-scattering PM sensor; passive shield for T and RH; FieldNode solar core; raw signals every 5 min, calibrated by collocation | 221 | Hourly NO2 and PM2.5 within the pole load, on the lab's shared core | PM2.5 at risk above 85 % RH; field NO2 accuracy unproven (about 4.3 ppb hourly MAE on paper); sensors flagged above 35 degC |
| B, aspirated, heated-inlet sampling node | Pump draws the sample up a heated inlet past the NO2 cell and the PM sensor; fan-aspirated shield; own 30 W solar supply | 188 | Dry, steady sample for the PM sensor | About 6 kg and 0.25 m² on the pole; about 28 Wh a day; nitrate loss in the heated inlet |
| C, passive diffusion tubes with a battery PM logger | Palmes tubes absorb NO2 on triethanolamine for a month and are analysed in a laboratory; battery PM logger read monthly | 198 | Light, cheap to build, an established method for annual NO2 | Monthly NO2 only; a visit at height every month; laboratory cost per tube |

C is 10.4 % below A and B is 14.9 % below A, so no option is within 10 % of the leader and a pick is given.

## Decision

Decided by Amish on 2026-10-30: carry option A forward as the design of record. `concept_chosen` in `project.yaml` is "A".

## Consequences

- A is confirmed, so nothing in the choice of working principle changes; the drawing, priced BOM and build plan describe A. The one addition is the runner-up's best idea, chosen on the same day (below).
- The runner-up's best idea was chosen separately on 2026-10-30 (AST-DEC-001 decision 2, AST-DDR-006), and is now in the model: triplicate diffusion tubes under a small hood on the cross arm at a few nodes, as an independent check of the annual NO2 means and of the street transfer bias. It adds a hood, three clips and laboratory cost per tube.
- Amish did not choose C, so the pitch (hourly NO2 and PM2.5) is unchanged; the D3 model of C in `cad/src/ast_options.py` stays as the record of the comparison.
- Options B and C are modelled to D3 in `cad/src/ast_options.py` and exported as `cad/step/B-assembly.step` and `cad/step/C-assembly.step`.

---
doc_id: AST-DDR-005
title: AirStreet STEM check fixes
project: AirStreet
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Fixes F1 to F4 for the STEM check rows that failed (AST-STM-001 S10, S14, S15, S24) and the D3 model fit details F5, made under Amish's standing instruction of 2026-10-23 and the 2026-09-30 instruction to make the design physically buildable; F1 to F3 tightened after the independent review of the same day; S33 sent to Amish"
---

# 0005: STEM check fixes

- **Date:** 2026-10-24
- **Status:** decided under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it in DEC as decided under that instruction"). Each fix can be reversed by Amish. None changes the working principle, the pitch or the user-facing scope. F5 records model fit details found while modelling the design at D3 under the 2026-09-30 instruction to make the design physically buildable.

## Context

The first STEM check of AirStreet (AST-STM-001, kit 1.9.1 upgrade) found four rows that failed in a detail while the working principle held. This record weighs the options for each, states the fix made and what it changed.

## Options considered and decisions

### F1: NO2 noise term (AST-STM-001 S10)

The calculation note assumed 5 ppb (1 sigma) of noise per 1 s NO2 sample because the sensor maker's pages could not be fetched at TRL 3. The NO2-B43F data sheet gives 15 ppb at 2 sigma, 7.5 ppb at 1 sigma.

- (a) Keep 5 ppb and mark it optimistic. (b) Use the data sheet figure. (c) Average more samples to recover the margin.
- **Decision: (b).** AST-CAL-001 v0.7 uses 7.5 ppb. The independent review then showed that the 10 samples of one record fall within the cell's response time, so only the 12 records of an hour are independent, and that a slope term was missing; both are now in the budget (a 5 % slope error at a 20 ppb street mean, assumed). The hourly noise term is 2.17 ppb, the hourly total 5.45 ppb (4.92 before) and the mean absolute error about 4.3 ppb (3.9 before), still under PR-002's 5 ppb, which stays at risk. No cost.

### F2: rated ranges of the sensors (AST-STM-001 S15)

The NO2-B43F is rated -30 to 40 degC and 15 to 85 % RH continuous; the SPS30 is recommended for 10 to 40 degC and 20 to 80 % RH. PR-012 asks the node to survive -10 to 50 degC, and street air often passes 85 % RH at night.

- (a) Narrow PR-012 to 40 degC (a scope change, so for Amish). (b) Cool or dry the pod (option B's principle, a change of working principle). (c) Keep the design and flag every reading taken outside the rated ranges, so that maps show those hours as such. (d) Seek a cell rated above 40 degC (a supplier change, for Amish with the first partner).
- **Decision: (c).** Each record carries flags set from the shield's T and RH, which are already in the record: shield air above 35 degC (the cell's 40 degC less an estimated 5 K by which the sunlit pod air runs above the shield air, to measure at TRL 4; 3 K before the independent review called it unsupported), RH above 80 % for PM and above 85 % for NO2, RH below 20 % for PM and below 15 % for NO2 (added after the review), and below 10 degC for PM. Flagged hours are published with the flag, not dropped. The 2-byte flags field of the 20-byte record carries them, so the record, airtime and power do not change. PR-007 now names the flags (met by design); PR-012 stays at risk. No cost. The flags mark the hours but do not make them valid, so the original claim (valid readings across -10 to 50 degC) stays open as AST-STM-001 S33, Fails, fix proposed: whether the first partner accepts flagged hot afternoons, or option (a) or (d) is wanted, is open decision 3 in AST-DEC-001.

### F3: ozone filter life (AST-STM-001 S14)

The cell's ozone filter holds more than 500 ppm h. At a 40 ppb annual mean ozone that lasts 17 months (23 months at 30 ppb; 11 to 14 months at the 50 to 60 ppb of hot, sunny sites, as the independent review pointed out), before the two-year replacement assumed in the BOM notes.

- (a) Replace every cell at 12 months. (b) Replace at the pod exchange before the site's ozone dose since fitting reaches 500 ppm h, and by 24 months at the latest. (c) Keep two years and accept ozone breakthrough.
- **Decision: (a) with the extension of (b).** The cell is replaced every 12 months at the pod exchange (on the ground), and at 18 or 24 months only where the collocated reference station's ozone record shows the dose since fitting stays under 500 ppm h by then; not every site has an ozone record, so the default is the safe one (the first proposal was (b) alone; the review showed it fails at hot sites). Running cost: one cell a year at most sites instead of one every two years (AST-CAL-001 [C7], [I3]); not in the per-node BOM. PR-016 names the rule.

### F4: band thickness (AST-STM-001 S24)

The model drew the stainless bands 12.7 x 0.8 mm while the mass calculation used 0.6 mm.

- (a) Use 0.8 mm in the calculation (+0.02 kg). (b) Draw 0.6 mm, the common thickness of a 12.7 mm worm-drive band, and read it from the model.
- **Decision: (b).** `PARAMS["band"]` is (12.7, 0.6) and `sizing.py` reads it. The band carries its 1,000 N preload at 131 MPa, under 137 MPa (205 MPa minimum yield of annealed 304 stainless over 1.5); cold-rolled band is stronger (S23). Mass unchanged. BOM line 3 states the thickness; no price change.

### F5: D3 model fit details

Modelling every part at D3 (STANDARDS section 24) and checking every pair of parts for overlap found five places where parts clashed or did not join as drawn:

| Item | As drawn before | As drawn now | Effect |
| --- | --- | --- | --- |
| Pod shell floor screw bosses | Touched the walls on a line only, so the shell was five separate solids | A 3 mm web joins each boss to the two walls beside it | One printable part; no dimension of the pod changes |
| Pod back wall bosses for the front end | 7 mm bosses with 3.2 mm holes, too small for the M3 heat-set inserts in the BOM | 8 mm bosses with 4.0 mm holes for M3 inserts | Matches BOM line 11 and AST-DEC-001 item 4 |
| Shield spacers | Solid printed cylinders that the M5 rods ran through | Tubes with a 5.5 mm bore | 0.01 kg lighter: 3.77 kg with the sun shield (was 3.78) |
| Probe lead | Ran along the middle of the arm, across the top of the left shield cap screw | Runs along the flat leg against the upright leg, as the build plan says, clear of the cap screw heads, and enters the M8 plug from behind | Lead length about the same (0.5 m) |
| Fixings | Cross arm M5 x 12 button heads too short for rail, arm, washer and nyloc nut; the BOM named M5 x 16 countersunk screws for the saddles and plates where the model and the 10 mm insert holes take 14; no washers drawn | Cross arm M5 x 14 with washers; saddle and plate screws M5 x 14; a washer under every pan head screw and nut; M3 x 8 floor screws with washers; pod screws M5 x 12 | BOM line 11 and the build plan text updated; no price change |

Every one keeps the design's dimensions and what the node does. `python cad/src/model.py --check` passes 77 of 77 constructability checks, and `python .kit/cad_check.py --export` finds no overlap between any two parts of the 195 in option A.

## Consequences

- AST-CAL-001 v0.7, AST-PRS-001 v0.9 (PR-002, PR-007, PR-012, PR-013, PR-016), AST-PRC-001, AST-BLD-001 (wiring, service and the spacers), BOM lines 3, 8 and 11 (text only), the model, drawings and build plan pictures carry the fixes.
- AST-STM-001 rows S10, S14, S15 and S24 are closed by these fixes; S33 (validity above the rated range) goes to Amish; the check stays open for S33 and the plausible rows listed there.
- The independent review also corrected calculation errors that are not design fixes (the cross arm bolt force, the rail check with twist and minimum yield, the EU reference temperature) and added sensitivity lines; they are in AST-CAL-001 v0.7, Table 8, and AST-STM-001, Table 3.
- Value engineering: no change to the sensor-head cost (USD 302.50, USD 17.50 over the USD 285 target); the cell replacement interval raises the running cost.

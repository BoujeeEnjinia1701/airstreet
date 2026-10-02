# Review note: AirStreet

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (AST-PRB-001 v0.2): problem with cited figures, users, operating environment, constraints, out of scope, prior work, open questions; co-design checklist kept.
- `docs/02-concept.md` (AST-PRC-001 v0.2): how it works, numbered components, design choices, calibration route (CalRig for PM, temperature and humidity; field collocation with a reference station for NO2), first-order numbers with assumptions, safety, open questions.
- `docs/03-requirements.md` (AST-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets and a status column.
- `cad/src/concept_media.py`: massing model of the node on a street light pole (FieldNode core and panel, band clamps and rail, sensor pod, PM sensor, NO2 sensor, front end, radiation shield, temperature and humidity sensor, cables), with a pole, sidewalk, kerb, carriageway and 1.75 m person as grey context. The scene is shifted down 3 m in the script because the kit's cutaway cutter is centered on Z = 0.
- `media/`: hero, blueprint sheet (PNG, PDF, SVG), cutaway, exploded view with BOM callouts, measurement and data flow diagram, `model.glb` and `viewer.html`. Temporary `_views` folders removed.
- `bom/bom.csv`: 11 lines numbered to match the exploded view, with indicative costs. `bom/bom-notes.md` updated to state totals and the budget gap.
- `README.md`: hero and links line; Concept rationale, Burning platform, Where it could be used, What sparked the idea, Concept, Key components and Safety expanded. The README states that NO2 is calibrated by field collocation, not on CalRig.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Sensor average power | about 41 mW (45 mW with margin) of FieldNode's 115 mW | R9 met |
| Record interval and payload | 5 min, about 20 bytes | R8 met |
| LoRaWAN airtime | about 0.06 % (SF9) to 0.5 % (SF12) | R10 met |
| NO2 hourly error after field calibration | about 5 ppb (9.4 µg/m³), target | R2 at risk |
| NO2 near the WHO annual guideline (10 µg/m³) | not resolvable | **R3 not met** |
| Mass and frontal area on the pole | about 3.0 kg, 0.09 m² | R13 met |
| Parts cost | about $391 per node with FieldNode core; about $265 sensor head only | **R15 not met** ($180 budget) |

Requirements not met or at risk:

- **R15 (cost) not met:** about $391 per node, or $265 without the FieldNode core, against $180.
- **R3 (NO2 near the WHO guideline) not met:** expected hourly error is about the size of the guideline level; AirStreet can rank streets and check the EU 40 µg/m³ limit (R4) but cannot confirm WHO guideline compliance.
- **At risk:** R2 (NO2 accuracy and seasonal drift unverified), R5 (radiation shield error in low wind), R12 (condensation and insects in the pod), R16 (sensor swap at height within 15 min).

### Proposed, awaiting Amish (status updated 2026-09-25, see AST-DDR-002)

1. **Budget.** Options: (a) budget covers the sensor head only, with the FieldNode core costed in FieldNode, and rises to about $280; (b) raise `budget_usd` to about $400 for the whole node; (c) keep $180 with a cheaper PM sensor and a three-electrode NO2 sensor, at a clear loss of NO2 accuracy. Recommendation: (a). `project.yaml` is unchanged. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
2. **Pitch wording.** The pitch says "calibrated on CalRig", but CalRig covers only temperature, humidity, CO2 and particles. Proposed: "A street-level air quality node measuring PM2.5 and NO2, with particles checked on CalRig and NO2 calibrated against a reference station, for neighborhood-scale pollution maps." Recommendation: adopt. `project.yaml` and the README intro are unchanged until Amish decides. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
3. **NO2 calibration method.** Field collocation with a regulatory reference station for at least 14 days before deployment, at least every 6 months after, and one permanently collocated anchor node; multiple linear regression first, random forest later. Alternative: collocation only at deployment. Recommendation: the full plan. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
4. **NO2 sensor.** Alphasense NO2-B43F class (four electrodes, ozone filter) versus a cheaper three-electrode sensor. Recommendation: B43F class. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
5. **NO2 front end.** Buy an ISB class board for the first units versus an open two-channel potentiostat (saves about $35). Recommendation: buy first, study the open design at TRL 3. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
6. **PM sensor.** Sensirion SPS30 class versus a Plantower PMS5003 class sensor (about $25 cheaper). Recommendation: SPS30 class. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
7. **Inlet height.** About 3.0 m (proposed) versus about 2.5 m, both within the EU 1.5 to 4 m range. Recommendation: 3.0 m. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
8. **Reporting.** One record every 5 min, PM sensor run 30 s per record, raw signals sent. Recommendation: adopt. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
9. **Open data.** Publish calibrated hourly data, with calibration version, to an open platform such as OpenAQ. Recommendation: yes, subject to the partner's agreement. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
10. **First partner, city and reference station** for co-design and collocation. Still proposed, awaiting Amish (no recommendation).

### Safety concerns

- Work at height beside traffic when mounting; wind load on the pole unverified.
- Mains voltage inside street light poles: never open the pole or tap its supply.
- Lithium iron phosphate cell in the FieldNode core.
- Acid electrolyte in the electrochemical sensor; sharp edges on clamps and flat bar.
- Misuse of indicative data as regulatory or health evidence: every map must carry its calibration version and uncertainty.

### Problems and notes

- The README intro paragraph still repeats the pitch ("calibrated on CalRig"); it was kept pending decision 2, and the rest of the README states the NO2 route.
- Prices are indicative and were not checked against suppliers (the web search quota was exhausted; figures in the documents were verified by fetching the cited pages). NO2 sensor and front-end prices and power draws are estimates.
- FieldNode figures ($126, 1.7 kg, 115 mW) come from the FieldNode README, which is being written in parallel; recheck when it settles.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the power, airtime, mass and wind-load estimates by calculation, write the collocation and calibration method as a calculation note, and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Nothing here is recorded as decided or approved by Amish. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (AST-DDR-001 v0.1, status proposed): D1 to D9 adopted as recommended for TRL 3, open for Amish's review; O1 left open.
- `docs/04-calcs/01-sizing.md` (AST-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: power and energy, airtime and storage, NO2 error budget, radiation shield, PM2.5 humidity error, geometry, projected area and mass, wind and mounting, service time, cost, and a status for every requirement. The script imports the model's PARAMS and part solids, reads the BOM and `project.yaml`, prints every quoted number with a tag and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model at massing-plus detail (FieldNode core envelope at FieldNode's dimensions and penetrations, panel and bracket, rail, V-saddles, band clamps, shield arm, pod with slots, mesh and drip lid, SPS30, NO2 sensor, front end, eight-plate shield, T and RH probe, cables). Exports `cad/step/` and `cad/stl/` for `airstreet-assembly` (with a pole stub), `airstreet-sensor-head` and `airstreet-mount`.
- `cad/src/sheets.py` and `cad/drawings/AST-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:10, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". AST-DWG-001 was free because the concept blueprint is AST-DWG-010.
- `bom/bom.csv` (11 lines, all priced with a supplier or supplier type) and `bom/bom-notes.md`. SPS30 and SHT45 prices checked by WebFetch; cables shortened to 0.5 m; saddles added to line 3.
- `cad/src/concept_media.py` now builds from the model; all of `media/` re-rendered and every image checked; temporary `_views` folders deleted.
- AST-PRB-001, AST-PRC-001 and AST-REQ-001 revised to v0.3. `README.md` (badge, TRL line, pitch, links, performance paragraph; the required sections are unchanged in order and wording) and `project.yaml` (pitch per D2, `trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

### Requirement status (AST-CAL-001, Table 3)

3 not met, 6 at risk, 3 met on paper, 4 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R3 NO2 near the WHO guideline | **Not met** | Annual uncertainty 4.2 µg/m³ (1σ) against 2 µg/m³; would need a transfer bias of 0.16 ppb |
| R13 Mass and area | **Not met** | 3.65 kg against 3.5 kg; 0.138 m² against 0.12 m² (TRL 2 said 3.0 kg and 0.09 m², using 1.7 kg for FieldNode instead of 2.41 kg) |
| R15 Cost | **Not met** | Sensor head $283.00 against $180 (`budget_usd`) and $280 (proposed); $409.00 with the FieldNode core |
| R1 PM2.5 | At risk | Within ±5 µg/m³ or ±30 % up to 80 % RH; outside it at 85 % RH and above |
| R2 NO2 hourly | At risk | About 3.9 ppb MAE from assumed terms, against 5 ppb |
| R4 EU limit | At risk | Decisive only below 34.6 or above 45.4 µg/m³ |
| R5 T and RH | At risk | Shield 0.43 to 0.89 K at 1 m/s; 4.2 % RH low at 85 % RH |
| R12 Outdoors | At risk | FieldNode rated to 45 °C ambient against R12's 50 °C; SPS30 recommended to 80 % RH |
| R16 Service | At risk | About 14 min against 15; a new NO2 sensor needs collocation |
| R8, R9, R10 | Met on paper | 40.3 kB for 7 days; 48.0 mW design load, 1.29 Wh/day, 11.9 days without sun; 0.60 % duty at SF12 |
| R6, R7, R11, R14 | Met by design | |

Key numbers: 247 ms per uplink at SF9 (1.81 s at SF12, not the 1.3 s of TRL 2); 124 N and 414 N·m at the pole base in a 35 m/s gust; clamp slip factor 25; whip clearance to the pod 23 mm.

### Decisions recorded (AST-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (now decided by Amish, 2026-09-25: go with recommendation, see AST-DDR-002): D1 budget covers the sensor head only, FieldNode core costed in FieldNode (R15 redefined; the $280 figure is recorded only and `budget_usd` stays $180); D2 pitch reworded and applied to `project.yaml` and `README.md`; D3 full NO2 collocation plan; D4 NO2-B43F class sensor; D5 buy an ISB class front end first; D6 SPS30 class PM sensor; D7 inlets at 3.0 m; D8 5 min records, 30 s PM run, raw signals; D9 open data subject to the partner's agreement.

### Still awaiting Amish (status updated 2026-09-25, see AST-DDR-002)

1. **O1, first partner, city and reference station.** No recommendation was made. Still proposed, awaiting Amish.
2. **Budget figure.** `budget_usd` is $180; $280 is recommended (D1); the sensor head is now $283.00. Options: accept about $285; find $3 (for example quantity pricing on the SPS30, $57.48 at 25 or more); or the open front end at about $25 instead of $60 once designed. Recommendation: set about $285 for now and revisit the open front end later. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
3. **New, mass and area (R13).** Options: (a) leave off FieldNode's 0.47 kg back plate and fix its enclosure and bracket to the AirStreet rail (3.19 kg, area slightly lower), which changes the FieldNode mounting interface; (b) relax R13 to 4.0 kg and 0.15 m²; (c) both. Recommendation: (a), agreed with FieldNode, plus relaxing the area limit to 0.15 m², since the panel alone is set by FieldNode. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
4. **New, WHO guideline (R3).** Options: drop R3 and state plainly that AirStreet ranks streets and checks the EU limit only; or keep R3 as a research goal needing an anchor node at every site. Recommendation: drop it as a requirement and keep it as an open research question. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
5. **New, PM run length.** The SPS30 needs up to 30 s to a first reading in clean air. Options: keep 30 s; or run 60 s (design load 87.0 mW, still inside 100 mW). Recommendation: 60 s. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
6. **New, fair use on The Things Network.** At 5 min, only SF7 fits the 30 s/day policy. Options: 5 min on private gateways only; or 15 min on TTN at SF8 and slower. Recommendation: 5 min on the TwinKit gateway, 15 min on TTN. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
7. **New, R12 temperature range.** FieldNode is rated to 45 °C ambient. Options: cap R12 at 45 °C; or require FieldNode's proposed sun shield at hot sites. Recommendation: require the shield at sites above 45 °C, consistent with FieldNode's own recommendation. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).
8. **New, service unit (R16).** Recommendation: exchange a pre-collocated pod rather than individual sensors at the pole. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (AST-DDR-002).

### Cross-repo consistency

- **FieldNode** (TRL 3 in its repo): enclosure 150 x 90 x 200 mm, back plate 180 x 320 x 3 mm, ports at x = -52 and -22 mm, whip at x = 58 mm, panel 290 x 200 mm at 40°, $126.00 and 2.41 kg are used as FieldNode states them. Conflicts noted here, FieldNode not edited: (a) FieldNode's V-block mount fits 40 to 60 mm poles, so AirStreet brings its own mount for 80 to 200 mm poles; (b) AirStreet needs port B's 5 V rail held on continuously for the NO2 bias, while FieldNode describes switched rails that are off while the node sleeps; (c) FieldNode's 15 min default and its R9 fair-use target do not fit AirStreet's 5 min records on TTN (item 6); (d) FieldNode is rated to 45 °C ambient against AirStreet's 50 °C (item 7). AirStreet's 48 mW fits both the 115 mW ceiling and the 100 mW FieldNode proposes.
- **CalRig:** CalRig's A5 (NO2 by field collocation only) matches D2 and D3. CalRig's R10 bay (90 x 70 x 50 mm) takes the SPS30 and SHT45 probe individually but not the assembled 170 x 110 x 95 mm pod; the pod fits the chamber if it takes two bays. Noted, CalRig not edited.
- **TwinKit:** the default gateway (FND-DDR-001 D7) is assumed; no TwinKit interface is used here.

### Safety concerns

- Work at height beside traffic; the node adds about 124 N and 414 N·m at the pole base in a 35 m/s gust, which the pole owner must check.
- Band clamps carry every mounting margin on an assumed 1,000 N preload; installers need a torque figure.
- Mains voltage inside street light poles: never open the pole or tap its supply.
- LiFePO4 cell in the FieldNode core; FieldNode runs hot above 45 °C ambient, and its 45 °C charge lockout must not be defeated.
- Acid electrolyte in the NO2 sensor; sharp edges on clamps and flat bar.
- Misuse of indicative data: R3 is not met, so no map should claim WHO guideline compliance for NO2.

### Gaps and notes

- Citations: the TRL 2 note listed no unchecked citations. WebFetch confirmed the SPS30 datasheet values (current, operating ranges, start-up time, mass, precision) and the SPS30 and SHT45 prices. The Alphasense pages are blocked to fetching, so NO2 sensor and front-end prices, power, gain and noise remain stated assumptions. WebSearch was not used (quota exhausted).
- The NO2 and shield results rest on assumed terms (transfer bias, drift, inner air speed); AST-CAL-001 lists each one.
- The kit's cutaway cuts at the mean Y of the parts and its cutter is centered at Z = 0, so `concept_media.py` shifts the scene down by the inlet height (3,000 mm), as at TRL 2. The cutaway shows the pod interior and the shield plates; the T and RH probe mostly falls in the removed half. In the exploded view the callouts for the small parts 5, 6 and 9 partly cover them.
- Existing material beyond TRL 3: none. `build-log/README.md` is the stock header; `electronics/` and `firmware/` are empty. None was extended.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on AST-DDR-001 and on items 1 to 8 above. For the record only, TRL 4 would need: a bench-built sensor head on a FieldNode core; a lab test report (TST, `environment: lab`) covering port power draw, SPS30 start-up in clean air, shield error under a lamp and fan, CalRig checks of the SPS30 and SHT45, and NO2 zero and noise with the chosen front end; and build log entries. Field collocation belongs to TRL 5. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every AirStreet item with a recommendation is now decided by Amish, 2026-09-25: go with recommendation, and is recorded in `docs/decisions/0002-recommendations-accepted.md` (AST-DDR-002). Items without a recommendation stay open.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| D1 to D9 (AST-DDR-001) | As recommended | Adopted for TRL 3, open for review | Decided; AST-DDR-001 v0.2 |
| Budget | About $285 for the sensor head | `budget_usd` $180 | `budget_usd` $285; sensor head $283.00 to $285.00 (adapter bars +$2); R15 met with no margin |
| R13 mass and area | Leave off FieldNode's back plate, enclosure to the rail; area limit 0.15 m² | 3.65 kg, 0.138 m² against 3.5 kg, 0.12 m² | 3.26 kg, 0.126 m² against 3.5 kg, 0.15 m²; model, STEP, STL, AST-DWG-001 Rev P2, BOM line 3 |
| R3 WHO guideline | Drop as a requirement, keep as research | Not met (4.2 µg/m³ against 2) | Withdrawn; research question |
| PM run | 60 s per record | 30 s; 48.0 mW design load; 11.9 days without sun | 60 s; 87.0 mW; 6.6 days (4.6 days at -20 °C) |
| TTN fair use | 5 min on the TwinKit gateway, 15 min on TTN | 5 min fits TTN only at SF7 | 15 min on TTN fits up to SF9 (23.7 s/day); R8 restated |
| R12 heat | FieldNode sun shield required above 45 °C | Target -10 to 50 °C without a rule | Shield required above 45 °C; still at risk until FieldNode designs it |
| R16 service | Exchange a pre-collocated pod | Sensor swap, 14 min, recollocation needed | Pod exchange, about 14 min; met on paper |

Documents revised with the change "Recommendations accepted by Amish (DDR-002)": AST-PRB-001 v0.4, AST-PRC-001 v0.4, AST-REQ-001 v0.4, AST-CAL-001 v0.2 (script rerun, `results.csv` regenerated), AST-DDR-001 v0.2 and the new AST-DDR-002 v0.1. `project.yaml` (`budget_usd`, evidence list), `README.md` (budget, performance paragraph, components, new "What sparked the idea"), `bom/bom.csv` and `bom/bom-notes.md` updated. All media, the drawing and the PDFs were regenerated; temporary `_views` folders deleted.

### Requirement status now (AST-CAL-001 v0.2)

- **Not met:** none (was R3, R13 and R15).
- **At risk (5):** R1 PM2.5 above 85 % RH; R2 NO2 hourly error rests on assumed terms; R4 EU limit decisive only outside 34.6 to 45.4 µg/m³; R5 shield error in low wind; R12 FieldNode sun shield not yet designed, humidity, condensation and insects.
- **Met on paper (6):** R8, R9, R10, R13, R15 (no margin), R16.
- **Met by design (4):** R6, R7, R11, R14.
- **Withdrawn (1):** R3, kept as a research question.

The 60 s PM run leaves 13 mW under FieldNode's 100 mW design value, and autonomy at -20 °C (4.6 days) is below the 5 days FieldNode's own R6 asks of its core. AirStreet has no autonomy requirement, so this is noted, not a failure.

### Still awaiting Amish

1. **O1, first partner, city and reference station** for co-design and collocation. No recommendation was made.

### Cross-repo actions (not made here)

- **FieldNode:** accept an enclosure bolted to the AirStreet rail without its back plate, with the panel bracket feet on two AirStreet adapter bars (R13); design and supply the sun shield for sites above 45 °C (R12); keep port B's 5 V rail on continuously for the NO2 bias; allow a 5 min interval on a private gateway alongside its 15 min TTN default.
- **TwinKit:** serve as AirStreet's default private gateway for 5 min records.
- **CalRig:** take the assembled pod across two bays if it is checked whole.

### Other changes

- "What sparked the idea" in `README.md` now cites the Ella Adoo Kissi-Debrah inquest (coroner's finding, December 2020; Prevention of Future Deaths report, 20 April 2021), verified by fetching the judiciary, CIEH and IAQM pages. The previous text about a portfolio review was removed. `docs/01-problem.md` did not attribute the idea to a review.
- All generated files (docs PDFs, drawing, concept media) were rebuilt; none shows the old personal domain.

### TRL

TRL 4 remains on hold by Amish's instruction. Decisions that need TRL 4 or later work are decided but on hold: buying the ISB class front end (D5), field collocation (D3), publishing open data (D9), the open two-channel front end (budget item), the firmware reporting rule, and spare pods. `trl: 3` and `trl_target: 3` are unchanged.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose AirStreet on 2026-09-26 for the first batch of product renders. This session adds an appearance model for photoreal renders. It changes no design parameter, requirement, calculation or BOM line.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 66 parts (45 shell, 20 internal, 1 context), each with a colour, a render material, its BOM line, a group and an explode offset; `TITLE` and `RENDER_VIEWS` (hero on the pole, exploded, and a detail view without the pole). It imports `PARAMS`, `derived()` and `build_parts()` from `cad/src/model.py`, so every main dimension and interface is unchanged: pole axis, 3.0 m inlet plane, rail, saddles, 375 mm clamp spacing, adapter bars, FieldNode envelope, ports, whip, 40 deg panel, pod, sensors, front end, shield and arm.
- Appearance detail added: filleted FieldNode enclosure with parting line, gasket, side ribs, lid screws, lid label and a lit green status light; M12 sockets with knurled plugs and cables; blanked glands; whip antenna with a swivel knuckle; aluminium panel frame with cell grid and junction box; filleted pod with side ribs, lid screws, cable glands, stainless mesh and a label strip; dished shield plates with spacers, stainless rods and acorn nuts; worm housings and screws on the band clamps; slotted rail; cable clips on the shield arm; the FieldNode board and LiFePO4 cell inside; a short section of 140 mm pole as context.
- `README.md`: the hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately.

### Differences from model.py (Proposed, awaiting Amish)

1. **Clear service window in the pod's street face.** Not in `model.py` or the BOM; added so the renders show the PM sensor, NO2 sensor and front end. A window lets sun heat the pod and adds a seal. Recommendation: keep the window in the renders only and keep the pod opaque ASA in the design; if Amish wants it in the design, use UV-stabilized polycarbonate and add it to BOM line 4.
2. **Radiation shield plates drawn with a 6 mm downturned lip and rod spacers.** `model.py` has flat rings. The lip and spacers are the usual multi-plate shield form and keep the 120 mm OD, 56 mm ID, 13 mm pitch and eight plates. Recommendation: adopt the lipped plate as the reference form at the next design update; the shield error in AST-CAL-001 does not depend on it.
3. **FieldNode interior (power and radio board, LiFePO4 cell in a cradle).** Illustrative envelopes only, placed for the exploded view; FieldNode's own model governs them. Recommendation: accept as illustration, no change to FieldNode.
4. **Label wording on the FieldNode lid** ("AirStreet", "PM2.5 + NO2 STREET NODE", "RAW SIGNALS, OPEN CALIBRATION", band "FIELDNODE CORE") and the pod strip ("INLET BELOW · PM · NO2"). Naming and wording are Amish's call. Recommendation: keep; the wording matches the pitch and does not claim certification.

### TRL

Appearance only: no tolerances, fabrication detail, PCB layouts or TRL 4 work. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: kit 1.7.0, design for construction and the prototype build plan

On 2026-09-30 Amish approved the FieldNode build plan as the format for every repo ("this is the correct build plan ... this is a good quality document format. Extend this across all the other repos") and asked that outstanding decisions go in a separate design decisions register, not in the build plan. He also wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." This session applied both to AirStreet.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced by `.kit/CLAUDE.md`.
- `cad/src/fieldnode_core.py` (new): an unchanged, vendored copy of FieldNode's constructable model (FND-DDR-003), so AirStreet builds the FieldNode core exactly as FieldNode does.
- `cad/src/model.py` rewritten as a constructable model (components, fixings and 71 constructability checks, all passing: `python cad/src/model.py --check`). STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (AST-DDR-003 v0.1, Draft): every change, its reason, the knock-on changes and three items proposed to Amish.
- `cad/src/build_plan_media.py` (new) and its pictures: overview, hole layout, wiring, nine making sketches (AST-DWG-101 to 109), eight joint close-ups and sixteen step pictures in `docs/05-build-plan/` and `cad/drawings/`. Every picture was looked at and fixed where unclear.
- `docs/05-build-plan.md` (AST-BLD-001 v0.1) and `docs/06-design-decisions.md` (AST-DEC-001 v0.1) written from the kit templates.
- Recalculated: `docs/04-calcs/sizing.py` and AST-CAL-001 v0.3 (mass from the model's volumes, new mount loads, cost). AST-REQ-001 v0.5 and AST-PRC-001 v0.5 updated. `bom/bom.csv` lines 1, 2, 3, 4, 8, 9, 10 and 11 revised.
- AST-DWG-001 Rev P4 regenerated; concept media regenerated from the new model (`media/hero.png`, `exploded.png`, `cutaway.png`, `flow.png`, `concept-blueprint.*`, `model.glb`).
- `project.yaml`: `design_state: constructable`; the DDR, build plan and register added to `trl_evidence`. `README.md`: links line and a "Building the prototype" section.
- `cad/src/product_model.py`: given the concept-only parameters it needs so it still runs; it still shows the concept (see Stale media).

### Design changes made for construction (AST-DDR-003, Draft, open for Amish's review)

1. FieldNode core taken from FieldNode's own constructable model; the pod moved from 70 to 90 mm left of the pole because FieldNode's whip moved; whip clearance to the drip lid 15 mm (was 23 mm).
2. Two 3 mm aluminium adapter plates (180 x 75 and 180 x 110 mm) on the rail, drilled to FieldNode's back plate pattern, carry the enclosure lugs, the plate clips and (hot sites) the sun shield; they replace the two adapter bars.
3. Adapter plate heights set so FieldNode's sun shield screws land on them.
4. Printed V-saddles 100 x 50 x 24 mm with a 140° V that seats 80 to 200 mm poles (was a round seat for 140 mm only).
5. Bands cut to length from a 12.7 mm worm-drive band roll, running in a groove across the back of each saddle, between saddle and rail.
6. Saddles fixed to the rail by two M5 countersunk screws into heat-set inserts.
7. A 30 x 30 x 3 mm angle cross arm bolted to the rail carries the pod and the shield cap on screws from above; the rail shortened to 451 mm.
8. Pod split into a printed shell (walls, roof, drip lid) and a printed sensor floor with a PM sensor cradle and an NO2 sensor collar, closed from below over the mesh by four M3 screws; front end on standoffs on the back wall; inlet slots 50 x 50 and 50 x 40 mm.
9. Two M16 glands in the pod roof under FieldNode's ports; an M8 socket in the pod wall for the probe lead, so the pod unplugs for exchange.
10. Shield: 24 spacers, rods through the cap with nuts, cap screwed under the arm, probe on a 6 mm tube through the cap and the arm.

### Key results

- Mass 3.84 kg on the pole (4.00 kg with FieldNode's sun shield): **R13 not met** (3.5 kg). Frontal area 0.143 m², met.
- Sensor head $303.00 against the $285 value-engineering target (`budget_usd`): **R15 over the target by $18.00**. FieldNode core as used $131.00; whole node $434.00.
- Wind 128 N and 428 N·m at the pole base in a 35 m/s gust; clamp slip factor 24; cross arm 4.5 MPa; rail 16.4 MPa.
- Requirement status: 1 not met (R13), 1 over the value-engineering target (R15), 5 at risk (R1, R2, R4, R5, R12), 4 met on paper, 4 met by design, R3 withdrawn.

### Proposed, awaiting Amish

All open decisions, with options and recommendations, are in the design decisions register (AST-DEC-001). New this session: acceptance of the design changes as a whole; the R13 mass limit (recommend lightening at TRL 4 and a 4.0 kg limit); the R15 cost, now a value-engineering note (the open front end is the route back under the $285 target); the 15 mm whip clearance (recommend accept and check at TRL 4); FieldNode's agreement to the adapter plates.

### Safety

No change to the safety case. The build plan adds safety stops for the NO2 sensor's shorting spring and the pole stub stand, and repeats the street pole, mains and lithium cell warnings. The higher wind load (128 N) is in AST-PRC-001's safety note and the build plan's stop S6.

### Stale media

`media/card.png` and `media/social-preview.png`, and the photoreal renders made on Amish's Mac (`media/render-*.png`), show the concept mount and pod: the design changed visibly (adapter plates, cross arm, saddles, pod). They, and `cad/src/product_model.py`, need updating on Amish's Mac.

### Recommended next step

Amish reviews AST-DDR-003 and the register (decisions 1 to 4), then FieldNode is asked to accept the adapter plates. TRL stays at 3; nothing was built, bought or tested.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation written for every open decision in the design decisions register (AST-DEC-001). trl stays 3; nothing was built, bought or tested, and TRL 4 remains on hold.

### Decisions recorded (8)

| Register item | Decision |
| --- | --- |
| 1 | AST-DDR-003 accepted as a whole: P1 to P10 and their knock-on changes |
| 2 | R13 set at 4.0 kg including FieldNode's sun shield; pole owner to confirm the load; the four lightening steps carried into the TRL 4 build |
| 3 | 15 mm whip clearance accepted; signal strength checked with the pod fitted at TRL 4; pod moved 8 mm left only if that shows a loss |
| 4 | First partner rule: a city or air agency with a street-level regulatory NO2 reference station that will share data; first candidate to approach, TCEQ's Dallas-Fort Worth network with a local university or city partner |
| 5 | Agree with FieldNode: send the request for its enclosure, plate clips and sun shield on AirStreet's adapter plates, and for a stable model |
| 6 | Closed as already decided on 2026-09-25 (AST-DDR-002, N5); FieldNode's confirmation tracked as a cross-repo action |
| 7 | Propose to FieldNode one common pin assignment for both M12 ports, supply voltage per project by supply module (5 V on both for AirStreet) |
| 8 | Radio band set with the partner of item 4 (not item 5): US915 in North America, EU868 in Europe, with the matching FieldNode antenna |

All 8 moved to Decisions made in AST-DEC-001, dated 2026-10-02; the Open decisions section now reads "None."

### Documents changed

- `docs/06-design-decisions.md` (AST-DEC-001 v0.3): items 1 to 8 moved to Decisions made; Open decisions reads "None"; item 8's link corrected to the partner decision
- `docs/decisions/0003-design-for-construction.md` (AST-DDR-003 v0.3): status accepted (kept Draft), A1 and A3 marked accepted, consequence for R13 added
- `docs/03-requirements.md` (AST-REQ-001 v0.7): R13 relaxed to 4.0 kg including the sun shield; status at risk (no margin); counts updated
- `docs/04-calcs/01-sizing.md` (AST-CAL-001 v0.5): R13 status and Table 3 counts against the 4.0 kg limit; note that the script still prints the 3.5 kg result
- `docs/02-concept.md` (AST-PRC-001 v0.7): R13 wording; first partner rule and first candidate; radio band follows the partner; FieldNode request approved
- `docs/01-problem.md` (AST-PRB-001 v0.5): first partner rule and first candidate to approach
- `docs/05-build-plan.md` (AST-BLD-001 v0.2): section 2 says AST-DDR-003 is accepted; no open decisions added
- `README.md`: R13 wording; AST-DDR-003 accepted
- `docs/decisions/0001-trl2-review-decisions.md` (AST-DDR-001 v0.3): item O1 ("Proposed, awaiting Amish") recorded as decided
- `docs/decisions/0002-recommendations-accepted.md` (AST-DDR-002 v0.2): item O1 recorded as decided
- PDFs regenerated with `python3 .kit/render.py`; superseded versions removed.

### Follow-up actions to carry approved decisions into the design

The model, BOM quantities and prices, calculations and pictures were not changed in this session. These actions carry the approved decisions into them:

1. Decision 2 (calculations): Re-run `docs/04-calcs/sizing.py` with R13's limit at 4.0 kg including FieldNode's sun shield, so [J1] and `results.csv` show R13 at risk rather than not met.
2. Decision 2 (model, drawings, build plan pictures): Carry the four lightening steps into the TRL 4 design: saddles printed at 40 % infill, 40 x 4 mm rail, 1.5 mm shield plates and windows in the adapter plates; update AST-DWG-001 and the making sketches.
3. Decision 2 (BOM, calculations): Reprice and reweigh the lightened parts (rail, shield plates, adapter plates) and check whether the lightened 3.6 kg figure includes FieldNode's 0.16 kg sun shield (about 3.76 kg if it does not).
4. Decision 2 (documents): Ask the pole owner of the first site to confirm a 4.0 kg load on the pole.
5. Decision 3 (test plan): At TRL 4, check LoRaWAN signal strength with the pod fitted; move the pod 8 mm left in the model and pictures only if the check shows a loss.
6. Decision 4 (documents): Approach the first candidate partner (TCEQ's Dallas-Fort Worth monitoring network, with a local university or city partner); nothing is agreed yet.
7. Decision 5 and 6 (cross-repo): Send FieldNode the adapter plate request and track its confirmation of port B's always-on 5 V and the 5 min private-gateway interval as one cross-repo action.
8. Decision 7 (build plan pictures, documents): Propose the common M12 pin assignment to FieldNode (with CurbCount, which asks for 3.3 V on port A); once FieldNode agrees, update the pod wiring in build plan section 3.10 and its wiring picture.
9. Decision 8 (BOM, requirements): Once the partner is agreed, fix the band and FieldNode antenna in the BOM; for US915, restate R10 against the 400 ms dwell limit (SF9 or lower) instead of the EU868 duty cycle.

### Points found in the review

Raised when the recommendations were written (2026-10-01) and kept here so they are not lost:

- Item 8 says it 'Follows decision 5'; it should follow decision 4 (partner, city and reference station). Decision 5 is the adapter plates.
- Item 6 was already accepted by Amish on 2026-09-25 (AST-DDR-002, N5 and its cross-repo actions); only FieldNode's confirmation is outstanding, so it belongs with cross-repo actions rather than open decisions.
- Cross-repo conflict on FieldNode port A: AirStreet's build plan powers the SPS30 from a switched 5 V on port A, while CurbCount's build plan replaces FieldNode's port A boost converter with a 3.3 V load switch. FieldNode's pinout decision (FND-DDR-001, O2) must allow a per-project port supply.
- The four appearance items from REVIEW.md 2026-09-26 (pod service window, lipped shield plates, FieldNode interior, label wording) were 'Proposed, awaiting Amish' and are not in the register.
- Item 2: the lightened 3.6 kg figure does not say whether it includes FieldNode's 0.16 kg sun shield; if it does not, the lightened node with shield is about 3.76 kg.

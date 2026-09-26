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

### Proposed, awaiting Amish

1. **Budget.** Options: (a) budget covers the sensor head only, with the FieldNode core costed in FieldNode, and rises to about $280; (b) raise `budget_usd` to about $400 for the whole node; (c) keep $180 with a cheaper PM sensor and a three-electrode NO2 sensor, at a clear loss of NO2 accuracy. Recommendation: (a). `project.yaml` is unchanged.
2. **Pitch wording.** The pitch says "calibrated on CalRig", but CalRig covers only temperature, humidity, CO2 and particles. Proposed: "A street-level air quality node measuring PM2.5 and NO2, with particles checked on CalRig and NO2 calibrated against a reference station, for neighborhood-scale pollution maps." Recommendation: adopt. `project.yaml` and the README intro are unchanged until Amish decides.
3. **NO2 calibration method.** Field collocation with a regulatory reference station for at least 14 days before deployment, at least every 6 months after, and one permanently collocated anchor node; multiple linear regression first, random forest later. Alternative: collocation only at deployment. Recommendation: the full plan.
4. **NO2 sensor.** Alphasense NO2-B43F class (four electrodes, ozone filter) versus a cheaper three-electrode sensor. Recommendation: B43F class.
5. **NO2 front end.** Buy an ISB class board for the first units versus an open two-channel potentiostat (saves about $35). Recommendation: buy first, study the open design at TRL 3.
6. **PM sensor.** Sensirion SPS30 class versus a Plantower PMS5003 class sensor (about $25 cheaper). Recommendation: SPS30 class.
7. **Inlet height.** About 3.0 m (proposed) versus about 2.5 m, both within the EU 1.5 to 4 m range. Recommendation: 3.0 m.
8. **Reporting.** One record every 5 min, PM sensor run 30 s per record, raw signals sent. Recommendation: adopt.
9. **Open data.** Publish calibrated hourly data, with calibration version, to an open platform such as OpenAQ. Recommendation: yes, subject to the partner's agreement.
10. **First partner, city and reference station** for co-design and collocation.

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

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 budget covers the sensor head only, FieldNode core costed in FieldNode (R15 redefined; the $280 figure is recorded only and `budget_usd` stays $180); D2 pitch reworded and applied to `project.yaml` and `README.md`; D3 full NO2 collocation plan; D4 NO2-B43F class sensor; D5 buy an ISB class front end first; D6 SPS30 class PM sensor; D7 inlets at 3.0 m; D8 5 min records, 30 s PM run, raw signals; D9 open data subject to the partner's agreement.

### Still awaiting Amish

1. **O1, first partner, city and reference station.** No recommendation was made.
2. **Budget figure.** `budget_usd` is $180; $280 is recommended (D1); the sensor head is now $283.00. Options: accept about $285; find $3 (for example quantity pricing on the SPS30, $57.48 at 25 or more); or the open front end at about $25 instead of $60 once designed. Recommendation: set about $285 for now and revisit the open front end later.
3. **New, mass and area (R13).** Options: (a) leave off FieldNode's 0.47 kg back plate and fix its enclosure and bracket to the AirStreet rail (3.19 kg, area slightly lower), which changes the FieldNode mounting interface; (b) relax R13 to 4.0 kg and 0.15 m²; (c) both. Recommendation: (a), agreed with FieldNode, plus relaxing the area limit to 0.15 m², since the panel alone is set by FieldNode. Not applied.
4. **New, WHO guideline (R3).** Options: drop R3 and state plainly that AirStreet ranks streets and checks the EU limit only; or keep R3 as a research goal needing an anchor node at every site. Recommendation: drop it as a requirement and keep it as an open research question. Not applied.
5. **New, PM run length.** The SPS30 needs up to 30 s to a first reading in clean air. Options: keep 30 s; or run 60 s (design load 87.0 mW, still inside 100 mW). Recommendation: 60 s. Not applied.
6. **New, fair use on The Things Network.** At 5 min, only SF7 fits the 30 s/day policy. Options: 5 min on private gateways only; or 15 min on TTN at SF8 and slower. Recommendation: 5 min on the TwinKit gateway, 15 min on TTN. Not applied.
7. **New, R12 temperature range.** FieldNode is rated to 45 °C ambient. Options: cap R12 at 45 °C; or require FieldNode's proposed sun shield at hot sites. Recommendation: require the shield at sites above 45 °C, consistent with FieldNode's own recommendation. Not applied.
8. **New, service unit (R16).** Recommendation: exchange a pre-collocated pod rather than individual sensors at the pole. Not applied.

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

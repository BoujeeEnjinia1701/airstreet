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

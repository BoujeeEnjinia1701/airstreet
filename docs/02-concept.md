---
doc_id: AST-PRC-001
title: AirStreet design precis
project: AirStreet
doc_type: Design precis
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, components, calibration route, first-order numbers, safety)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update from AST-CAL-001, the parametric model and AST-DWG-001; design choices adopted for TRL 3 work per AST-DDR-001, open for Amish's review
---


# AirStreet design precis

## Summary

AirStreet is a pole-mounted node that measures PM2.5 and NO2 at street level for neighborhood-scale pollution maps. A small sensor pod and a radiation shield hang below a FieldNode core on a street light pole, with the inlet plane 3.0 m above the sidewalk. Temperature, humidity and particle readings are checked on CalRig. CalRig does not cover NO2, so each NO2 sensor is calibrated by field collocation with a reference station before deployment and at intervals afterward. The node sends raw signals, so calibrations can be improved and reapplied later. The design choices below are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review ([AST-DDR-001](decisions/0001-trl2-review-decisions.md)).

The TRL 3 calculations ([AST-CAL-001](04-calcs/01-sizing.md)) confirm the power and radio budget: a 48 mW design sensor load against FieldNode's 100 mW design allowance, 11.9 days without sun, and 0.60 % duty cycle even at SF12. They find three requirements not met. An annual NO2 mean carries about 4.2 µg/m³ of uncertainty, too much to resolve the WHO guideline of 10 µg/m³ (R3). The node weighs 3.65 kg and presents 0.138 m² to the street, over the 3.5 kg and 0.12 m² of R13, because the FieldNode core weighs 2.41 kg rather than the 1.7 kg assumed at TRL 2. The sensor head costs $283.00 in parts, over the $180 budget and the $280 proposed in AST-DDR-001 (R15); the node costs $409.00 with the FieldNode core.

![Figure 1. AirStreet on a street light pole, with a 1.75 m person for scale.](../media/hero.png)

Figure 1. AirStreet on a street light pole, with a 1.75 m person for scale (concept, not for fabrication).

## How it works

1. Street air enters the sensor pod from below, through stainless insect mesh under an overhanging drip lid. Downward-facing inlets keep rain and direct sun out.
2. An optical particle sensor draws a sample with its own fan for 30 s every 5 min and counts particles by laser scattering, giving PM1, PM2.5 and PM10. The SPS30 needs 8 to 30 s to its first reading, depending on particle count, so readings are averaged over the valid part of each run.
3. A four-electrode electrochemical NO2 sensor with an ozone filter faces down through a slot in the pod floor. Its working electrode (WE) responds to NO2, and its auxiliary electrode (AE) tracks the temperature-driven baseline. A potentiostat front end holds the bias continuously, and a 16-bit ADC reads both signals.
4. A temperature and humidity sensor sits inside a white multi-plate radiation shield beside the pod, so readings reflect air temperature rather than sun-heated plastic. These values drive the humidity correction for PM and the temperature correction for NO2.
5. Two short cables with M12 plugs run up to FieldNode's two sensor ports. Port A, on a switched 5 V rail, carries the PM sensor and the temperature and humidity sensor on one I2C bus and is powered only during each PM run. Port B carries the NO2 front end on a 5 V rail that stays on, because the sensor bias must be held continuously. FieldNode provides power, storage and a LoRaWAN radio, and its 6 W panel shades the enclosure.
6. Every 5 min the node sends one record of 20 bytes: raw PM values, raw WE and AE voltages, temperature, humidity, a status word, a counter and flags. It never sends images, audio or identifiers of people.
7. A server-side calibration model converts raw values to PM2.5 and NO2 concentrations. Each model is versioned and linked to the node's CalRig record and its collocation record, so any map can be traced to the calibration behind it.

![Figure 2. Cutaway of the sensor pod and radiation shield.](../media/cutaway.png)

Figure 2. Cutaway of the sensor pod (PM sensor, NO2 sensor and front end) and the radiation shield.

## Main components

Item numbers match the BOM ([bom/bom.csv](../bom/bom.csv)), the exploded view (Figure 3) and the parametric model `cad/src/model.py`. The general arrangement is drawing AST-DWG-001 (`cad/drawings/`).

Table 1. Main components.

| No. | Component | Key choice (adopted for TRL 3, open for Amish's review) |
| --- | --- | --- |
| 1 | FieldNode core | Shared lab core per FND: IP65 enclosure 150 x 90 x 200 mm, LiFePO4 cell, MPPT charger, STM32WL LoRaWAN, two M12 5-pin sensor ports, back plate; FieldNode's own V-blocks and 40 to 60 mm clamps are not used |
| 2 | FieldNode 6 W panel hood | Part of FieldNode; 40° tilt toward the street side as a sun and rain hood |
| 3 | Band clamps and mounting rail | Two 12.7 mm stainless band clamps for 80 to 200 mm poles, 375 mm apart, on printed V-saddles; 40 x 5 mm aluminum rail 565 mm long; 20 x 8 mm shield arm; no drilling |
| 4 | Sensor pod | Printed ASA shell 170 x 110 x 95 mm, open underneath behind mesh, 200 x 140 mm drip lid; offset 70 mm to one side so the FieldNode whip hangs beside it with 23 mm clearance |
| 5 | Optical PM sensor | Sensirion SPS30 (D6); the maker states a lifetime of more than ten years ([Sensirion](https://sensirion.com/products/catalog/SPS30)) |
| 6 | Electrochemical NO2 sensor | Alphasense NO2-B43F class (D4): four electrodes and an ozone filter; replace about every 2 years (estimate) |
| 7 | NO2 front end and ADC | Alphasense ISB class potentiostat bought for the first units (D5), with an ADS1115 class 16-bit ADC |
| 8 | Radiation shield | Eight white 120 mm plates at 13 mm pitch on three rods, 124 mm cap, naturally ventilated |
| 9 | Temperature and humidity sensor | Sensirion SHT45 on a probe board |
| 10 | Sensor cables | Two 0.5 m shielded cables with M12 plugs |
| 11 | Fasteners and consumables | Not modeled |

![Figure 3. Exploded view with BOM numbers.](../media/exploded.png)

Figure 3. Exploded view with BOM numbers.

## Key design choices

The choices below are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (AST-DDR-001). None is decided by Amish.

- **Build on FieldNode.** AirStreet designs only the sensor head, its mount and the calibration route. Power, radio and enclosure fixes found in other deployments carry over. The FieldNode core is costed in FieldNode, and AirStreet's budget covers the sensor head (D1).
- **Two calibration routes, stated plainly.** CalRig checks temperature, humidity and particle response in a chamber. NO2 is calibrated by field collocation with a regulatory reference station (chemiluminescence), because field calibration corrects temperature, humidity and cross-sensitivity effects that laboratory calibration misses ([Zimmerman et al., 2018](https://amt.copernicus.org/articles/11/291/2018/)). This follows the approach of the US EPA NO2 sensor protocols, which include field evaluation alongside regulatory monitors ([US EPA](https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols)).
- **Collocation plan (D3).** Each node sits beside a reference station for at least 14 days before deployment, covering a range of temperature, humidity and NO2. At least one anchor node stays at the reference site permanently to track seasonal drift, and every node returns for collocation at least every 6 months. The first model is a multiple linear regression on WE, AE, temperature and humidity, with a random forest model as an option once enough data exist.
- **Send raw signals (D8).** Raw WE and AE voltages and raw PM values let the city or community reprocess data when a better model or a new collocation becomes available.
- **Four-electrode NO2 sensor with ozone filter (D4).** The auxiliary electrode helps remove the temperature-driven baseline, and the filter reduces ozone interference.
- **Duty-cycled PM sensor (D8).** Running the particle sensor for 30 s every 5 min keeps its average draw near 30 mW and slows fouling.
- **Inlets 3.0 m above the sidewalk (D7).** This is within the 1.5 to 4 m inlet range in EU Directive 2008/50/EC ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050)) and out of easy reach.
- **Open data (D9).** Calibrated hourly data, with the calibration version, are published to an open platform such as OpenAQ, subject to the partner's agreement.

## Key numbers (TRL 3)

All values come from AST-CAL-001, which lists every assumption.

Table 2. Key numbers.

| Quantity | Value | Note |
| --- | --- | --- |
| PM sensor average power | 27.5 mW typical, 32.5 mW maximum | SPS30 55 mA typical, 65 mA maximum at 5 V (datasheet), 30 s in every 300 s |
| NO2 front end and ADC | 7.5 mW | 1.5 mA at 5 V held continuously (assumed) |
| Design sensor load | 48.0 mW | Maximum SPS30 current and 1.2 margin; FieldNode allows 100 mW (design) or 115 mW (ceiling) (R9 met on paper) |
| Daily draw and autonomy | 1.29 Wh/day; 11.9 days without sun | 8.3 days at -20 °C; 7.75 Wh stored in FieldNode's worst month |
| Payload and airtime | 20 bytes every 5 min; 247 ms at SF9, 1.81 s at SF12 | 0.082 % and 0.60 % duty cycle (R10 met on paper); only SF7 fits The Things Network's 30 s/day fair use |
| NO2 hourly error | About 3.9 ppb MAE (7.4 µg/m³) | Budget of literature and assumed terms (R2 at risk) |
| NO2 annual uncertainty | About 4.2 µg/m³ (1σ) | Against 2 µg/m³ at the 10 µg/m³ WHO guideline (R3 not met) |
| EU limit classification | Decisive below 34.6 or above 45.4 µg/m³ | 90 % confidence against 40 µg/m³ (R4 at risk) |
| PM2.5 hourly error | Within ±5 µg/m³ or ±30 % up to 80 % RH | Outside the bound at 85 % RH and above (R1 at risk) |
| Shield radiation error | 0.43 to 0.89 K at 1 m/s | Reads up to 4.2 % RH low at 85 % RH (R5 at risk) |
| Mass on the pole | 3.65 kg | FieldNode 2.21 kg as used, sensor head and mount 1.44 kg (R13 not met) |
| Frontal area | 0.138 m² | Rasterized from the model (R13 not met) |
| Wind at 35 m/s | 124 N, 414 N·m at the pole base | Clamp slip factor 25; the pole check is the owner's |
| Parts cost | Sensor head $283.00; $409.00 with the FieldNode core | Against $180 (`budget_usd`) and $280 proposed (R15 not met) |

![Figure 4. Measurement and data flow.](../media/flow.png)

Figure 4. Measurement and data flow.

## Safety

> **Safety:** Mounting on a street pole is work at height next to traffic. Install only with the pole owner's written permission, by trained crews using a mobile elevating work platform or a secured ladder with a second person, with traffic management as local rules require. The node adds about 124 N of wind load and about 414 N·m at the pole base in a 35 m/s gust; the pole owner must confirm the pole can carry it.

> **Safety:** Street light poles carry mains voltage inside. Never open the pole's access door or tap pole power; AirStreet runs only on its own solar and battery supply.

> **Safety:** The FieldNode core holds a lithium iron phosphate cell. Use a fused, protected cell, charge only within the maker's temperature limits and replace any swollen or damaged cell. FieldNode is rated for ambient temperatures up to 45 °C; hotter sites need FieldNode's proposed sun shield.

> **Safety:** Electrochemical gas sensors contain an acid electrolyte. Do not open, crush or heat them; dispose of them as the maker directs. Band clamp ends and cut flat bar have sharp edges; deburr them and wear gloves. Band clamps rely on their preload; installers need a torque figure before any field use.

> **Safety:** AirStreet data are indicative and are not a regulatory measurement or health advice. Maps must state the calibration version and its uncertainty.

## Open questions

- [ ] Which city, partner and reference station host the first collocation? (AST-DDR-001 O1, proposed, awaiting Amish.)
- [ ] Is the NO2 error after field calibration stable across seasons, and how large is the reference-to-street transfer bias in practice?
- [ ] How fast does air move inside the shield in low wind, and so how large is the radiation error?
- [ ] Does the SPS30 need a heated or dried inlet above 85 % RH, or is a humidity flag on the data enough?
- [ ] Should the pod be exchanged as a pre-collocated unit rather than swapping sensors at the pole?
- [ ] Can the FieldNode back plate be left off and the enclosure fixed to the AirStreet rail, to save 0.47 kg? (Proposed, awaiting Amish.)
- [ ] How are nodes secured against theft, and what does the pole owner require for insurance and inspection?

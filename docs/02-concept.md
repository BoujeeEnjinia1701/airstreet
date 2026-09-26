---
doc_id: AST-PRC-001
title: AirStreet design precis
project: AirStreet
doc_type: Design precis
version: "0.2"
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
---

# AirStreet design precis

## Summary

AirStreet is a pole-mounted node that measures PM2.5 and NO2 at street level for neighborhood-scale pollution maps. A small sensor pod and a radiation shield hang below a FieldNode core on a street light pole, with inlets about 3 m above the sidewalk (proposed). Temperature, humidity and particle readings are checked on CalRig. CalRig does not cover NO2, so each NO2 sensor is calibrated by field collocation with a reference station before deployment and at intervals afterward. The node sends raw signals, so calibrations can be improved and reapplied later.

First-order estimates (TRL 2, to be checked at TRL 3): about 45 mW average sensor power, one record every 5 min, about 3.0 kg on the pole, and about $391 in parts including the FieldNode core. The cost is over the $180 budget (R15 not met), and NO2 accuracy is not good enough to resolve the WHO annual guideline (R3 not met).

![Figure 1. AirStreet on a street light pole, with a 1.75 m person for scale.](../media/hero.png)

Figure 1. AirStreet on a street light pole, with a 1.75 m person for scale (concept, not for fabrication).

## How it works

1. Street air enters the sensor pod from below, through stainless insect mesh under an overhanging drip lid. Downward-facing inlets keep rain and direct sun out.
2. An optical particle sensor draws a sample with its own fan for about 30 s every 5 min and counts particles by laser scattering, giving PM1, PM2.5 and PM10.
3. A four-electrode electrochemical NO2 sensor with an ozone filter faces down through a slot in the pod floor. Its working electrode (WE) responds to NO2, and its auxiliary electrode (AE) tracks the temperature-driven baseline. A potentiostat front end holds the bias continuously, and a 16-bit ADC reads both signals.
4. A temperature and humidity sensor sits inside a white multi-plate radiation shield beside the pod, so readings reflect air temperature rather than sun-heated plastic. These values drive the humidity correction for PM and the temperature correction for NO2.
5. Cables with M12 plugs run to two sensor ports on the FieldNode core, which provides power, storage and a LoRaWAN radio. FieldNode's 6 W panel also shades the enclosure.
6. Every 5 min the node sends one record of about 20 bytes: raw PM values, raw WE and AE voltages, temperature, humidity and a status word. It never sends images, audio or identifiers of people.
7. A server-side calibration model converts raw values to PM2.5 and NO2 concentrations. Each model is versioned and linked to the node's CalRig record and its collocation record, so any map can be traced to the calibration behind it.

![Figure 2. Cutaway of the sensor pod and radiation shield.](../media/cutaway.png)

Figure 2. Cutaway of the sensor pod (PM sensor, NO2 sensor and front end) and the radiation shield with the temperature and humidity sensor.

## Main components

Item numbers match the BOM ([bom/bom.csv](../bom/bom.csv)) and the exploded view (Figure 3).

Table 1. Main components.

| No. | Component | Key choice (proposed, awaiting Amish) |
| --- | --- | --- |
| 1 | FieldNode core | Shared lab core: IP65 enclosure, LiFePO4 cell, MPPT charger, STM32WL LoRaWAN, two M12 sensor ports |
| 2 | FieldNode 6 W panel hood | Part of FieldNode; tilted toward the street side as a sun and rain hood |
| 3 | Band clamps and mounting rail | Two stainless band clamps, 520 mm aluminum rail and a shield arm; no drilling |
| 4 | Sensor pod | Printed ASA shell about 170 x 110 x 95 mm, open underneath behind mesh, drip lid |
| 5 | Optical PM sensor | Sensirion SPS30 class; the maker states ±10 % mass concentration precision and a lifetime of more than ten years ([Sensirion](https://sensirion.com/products/catalog/SPS30)) |
| 6 | Electrochemical NO2 sensor | Alphasense NO2-B43F class: four electrodes and an ozone filter; replace about every 2 years (estimate) |
| 7 | NO2 front end and ADC | Four-electrode potentiostat (Alphasense ISB class, or an open two-channel design) with an ADS1115 class 16-bit ADC |
| 8 | Radiation shield | Eight white 120 mm plates on three rods, naturally ventilated |
| 9 | Temperature and humidity sensor | Sensirion SHT45 class |
| 10 | Sensor cables | Two 1 m shielded cables with M12 plugs |
| 11 | Fasteners and consumables | Not modeled |

![Figure 3. Exploded view with BOM numbers.](../media/exploded.png)

Figure 3. Exploded view with BOM numbers.

## Key design choices

All choices below are proposed, awaiting Amish.

- **Build on FieldNode.** AirStreet designs only the sensor head and calibration route. Power, radio and enclosure fixes found in other deployments carry over. This keeps AirStreet consistent with the FieldNode README, which lists AirStreet among its smart city users.
- **Two calibration routes, stated plainly.** CalRig checks temperature, humidity and particle response in a chamber. NO2 is calibrated by field collocation with a regulatory reference station (chemiluminescence), because field calibration corrects temperature, humidity and cross-sensitivity effects that laboratory calibration misses ([Zimmerman et al., 2018](https://amt.copernicus.org/articles/11/291/2018/)). This follows the approach of the US EPA NO2 sensor protocols, which include field evaluation alongside regulatory monitors ([US EPA](https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols)).
- **Collocation plan.** Each node sits beside a reference station for at least 14 days before deployment, covering a range of temperature, humidity and NO2. At least one "anchor" node stays at the reference site permanently to track seasonal drift, and every node returns for collocation at least every 6 months. The first model is a multiple linear regression on WE, AE, temperature and humidity, with a random forest model as an option once enough data exist.
- **Send raw signals.** Raw WE and AE voltages and raw PM values let the city or community reprocess data when a better model or a new collocation becomes available.
- **Four-electrode NO2 sensor with ozone filter.** The auxiliary electrode helps remove the temperature-driven baseline, and the filter reduces ozone interference. Cheaper three-electrode sensors would save about $50 but increase error.
- **Duty-cycled PM sensor.** Running the particle sensor for 30 s every 5 min keeps the average power within the FieldNode budget and slows fouling.
- **Inlets about 3.0 m above the sidewalk.** This is within the 1.5 to 4 m inlet range in EU Directive 2008/50/EC ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050)) and out of easy reach. A lower height is closer to the breathing zone but more exposed to tampering.

## First-order numbers

All values are estimates for TRL 2 and will be checked at TRL 3.

Table 2. First-order estimates.

| Quantity | Estimate | Assumptions |
| --- | --- | --- |
| PM sensor average power | about 35 mW | About 300 mW while running (60 mA at 5 V, datasheet class value to be confirmed), 30 s in every 300 s, 85 % boost converter efficiency |
| NO2 front end and ADC | about 6 mW | About 1.5 mA at 3.3 V held continuously plus ADC; to be confirmed with the chosen board |
| Temperature and humidity sensor | under 0.1 mW | One reading per record |
| Total sensor average | about 41 mW, budget 45 mW with margin | Versus FieldNode's allowance of about 115 mW (R9 met) |
| Payload | about 20 bytes every 5 min | PM1, PM2.5, PM10, WE, AE, T, RH and status, 2 bytes each, plus a counter |
| LoRaWAN airtime | about 0.2 s per uplink at SF9, about 1.3 s at SF12 | 125 kHz channel; 12 uplinks per hour gives about 0.06 % and 0.5 % of an hour, within 1 % duty-cycle sub-bands (R10 met) |
| NO2 unit conversion | 1 ppb = 1.88 µg/m³ | 25 °C, 101.325 kPa, molar mass 46.01 g/mol |
| NO2 error after field calibration | about 5 ppb (9.4 µg/m³) hourly, target | Near the 3.5 ppb reported for field-calibrated electrochemical sensors ([Zimmerman et al., 2018](https://amt.copernicus.org/articles/11/291/2018/)); unverified for this design |
| WHO annual NO2 guideline | 10 µg/m³ (about 5.3 ppb) | As cited by the [EEA, 2024](https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024); hourly error is of the same size, so R3 is not met |
| Mass on the pole | about 3.0 kg | FieldNode about 1.7 kg, aluminum rail and clamps about 0.5 kg, pod about 0.25 kg, shield about 0.3 kg, sensors and cables about 0.25 kg |
| Frontal area | about 0.09 m² | Panel projection about 0.03 m², enclosure 0.03 m², pod and shield 0.03 m² |
| Parts cost | about $391 per node; about $265 for the sensor head | Indicative prices in the BOM; FieldNode core at $126 from its README; over the $180 budget (R15 not met) |

![Figure 4. Measurement and data flow.](../media/flow.png)

Figure 4. Measurement and data flow (estimates).

## Safety

> **Safety:** Mounting on a street pole is work at height next to traffic. Install only with the pole owner's written permission, by trained crews using a mobile elevating work platform or a secured ladder with a second person, with traffic management as local rules require. Check the pole can carry the added wind load.

> **Safety:** Street light poles carry mains voltage inside. Never open the pole's access door or tap pole power; AirStreet runs only on its own solar and battery supply.

> **Safety:** The FieldNode core holds a lithium iron phosphate cell. Use a fused, protected cell, charge only within the maker's temperature limits and replace any swollen or damaged cell.

> **Safety:** Electrochemical gas sensors contain an acid electrolyte. Do not open, crush or heat them; dispose of them as the maker directs. Band clamp ends and cut flat bar have sharp edges; deburr them and wear gloves.

> **Safety:** AirStreet data are indicative and are not a regulatory measurement or health advice. Maps must state the calibration version and its uncertainty.

## Open questions

- [ ] Which city, partner and reference station host the first collocation? (Proposed, awaiting Amish.)
- [ ] Is the NO2 error after field calibration stable across seasons, and how often must nodes return to the reference site?
- [ ] Does the naturally ventilated shield keep the radiation error within 1 °C in low wind and strong sun?
- [ ] Does the SPS30 class sensor need a heated or dried inlet in very humid climates, or is the humidity correction enough?
- [ ] Can an open two-channel potentiostat match a commercial front end, to cut about $35 per node?
- [ ] How are nodes secured against theft, and what does the pole owner require for insurance and inspection?
- [ ] Should data publish to an open platform such as OpenAQ by default? (Proposed, awaiting Amish.)

---
doc_id: AST-CAL-001
title: AirStreet sizing calculations
project: AirStreet
doc_type: Calculation
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (power and energy, airtime and storage, NO2 error budget, radiation shield, PM2.5 humidity error, geometry, mass and area, wind and mounting, service, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-30'
  author: Amish Chadha
  change: Design made constructable (AST-DDR-003); mass, area, mounting loads and cost recalculated; R13 and R15 now not met
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R13 status against the 4.0 kg limit accepted on 2026-10-02 (AST-DDR-003 A1); sizing.py still to be re-run with it"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "sizing.py re-run with R13 at 4.0 kg including the sun shield and the four lightening steps in the model (40 x 4 mm rail, plate windows, 1.5 mm shield plates, saddles at 40 % infill); lines 3 and 8 repriced; R13 met on paper; cost in the approved value-engineering wording"
---

# AirStreet sizing calculations

Version 0.6 follows the constructable design of AST-DDR-003 (2026-09-30), which made every part of the node buildable and moved onto FieldNode's own constructable core, with the four lightening steps of AST-DDR-003, A1 (accepted on 2026-10-02) now in the model: a 40 x 4 mm rail, windows in the adapter plates, 1.5 mm shield plates and saddles printed at 40 % infill. On paper AirStreet now meets nine of its sixteen requirements (five by calculation, four by design), has five at risk and is over its cost target on one (R15); R3 stays withdrawn. The node weighs 3.62 kg on the pole and 3.78 kg with FieldNode's sun shield, against R13's limit of 4.0 kg including the shield (set on 2026-10-02; it was 3.5 kg), so R13 is met on paper with 0.22 kg of margin; before the lightening it was 4.00 kg, on the limit. The pole owner of the first site is still to confirm the 4.0 kg load. Value-engineering target: USD 285. Estimated cost of the constructable design: USD 302.50 (USD 17.50 over the target); the cost drivers and savings worth trying are in the design decisions register. The frontal area, 0.139 m², stays inside 0.15 m², and every mounting part carries its load with a large margin. Power, airtime and the NO2 error budget are unchanged from v0.2, and the thinner shield plates change the shield and humidity results only in the second decimal: the 60 s particle run gives an 87.0 mW design sensor load inside FieldNode's 100 mW allowance and 6.6 days without sun, and an annual NO2 mean carries about 4.2 µg/m³ of uncertainty (1σ). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the node is safe to mount on any particular pole, and they are not a substitute for the pole owner's structural check, for electrical checks on the FieldNode cell or for field collocation of the sensors. AirStreet data are indicative, not a regulatory measurement or health advice. See AST-PRC-001, Safety.

## Scope and method

The note checks every requirement in AST-REQ-001 v0.8 against the design in AST-PRC-001 v0.8 and the parametric model `cad/src/model.py`, which builds the FieldNode core from FieldNode's own model (vendored as `cad/src/fieldnode_core.py`). The script imports the model's `PARAMS`, derived dimensions and part solids, so the pod, shield, rail, clamp positions and projected areas used here are those in the STEP files and in drawing AST-DWG-001. It reads `bom/bom.csv` and `budget_usd` in `project.yaml`. FieldNode figures are taken from FND-CAL-001 (v0.1 for power and energy, v0.3 for mass) in the FieldNode repo. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

The design case is a 140 mm street light pole with the inlet plane 3.0 m above the sidewalk (AST-DDR-001 D7), one record every 5 min with a 60 s PM run (D8 and DDR-002), LoRaWAN at SF9 in EU868 through a private gateway (15 min on The Things Network), FieldNode's back plate left off (DDR-002), and ambient -10 to 50 °C.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| PM sensor | SPS30 at 5 V, 55 mA typical and 65 mA maximum in measurement mode; 41 x 41 x 12 mm, 26.3 g; up to 30 s to first reading at low particle counts; recommended 10 to 40 °C and 20 to 80 % RH | Sensirion SPS30 datasheet (07/2023), checked 2026-09-25 |
| NO2 chain | Front end and ADC held on continuously, 1.5 mA at 5 V; overall gain 0.25 mV/ppb; 5 ppb (1σ) noise per 1 s sample; 10 samples per record | Assumed; the Alphasense pages could not be fetched, so these are not checked |
| T and RH | SHT45, ±0.1 °C and ±1 % RH typical | Adafruit SHT45 product page, checked 2026-09-25 |
| Margin | 1.2 on the port load, applied to the maximum SPS30 current | Judgment |
| FieldNode core | Rails 90 % efficient; SX1262 +14 dBm at 45 mA, receive 4.6 mA, two 0.1 s windows, controller 0.5 s at 8 mA per report, 33 µA sleep; 6 Ah LiFePO4 cell, 80 % usable; capacity ratios 0.70 at -20 °C and 0.80 at end of life; 7.75 Wh/day stored in the worst month, 0.8 Wh/day on a hot clear day without a sun shield; 2.41 kg; $126.00 | FND-CAL-001 v0.1 |
| Extra controller time | 1 s at 8 mA per record to run and read the sensors | Assumed |
| NO2 calibration | Field-calibrated residual MAE 3.5 ppb, taken as σ = 4.39 ppb; zero drift 0.5 ppb/month, half removed by the anchor node; 2 ppb bias moving from the reference site to a street; 6 h correlation time | Residual from [Zimmerman et al., 2018](https://amt.copernicus.org/articles/11/291/2018/); the rest assumed |
| PM humidity growth | κ-Köhler volume growth 1 + κ·aw/(1 − aw) with κ = 0.3 ± 0.1; residual after the CalRig transfer check 2 µg/m³ + 5 % | Assumed typical urban aerosol |
| Shield | 1,000 W/m² sun, ground albedo 0.2, absorptance 0.25 (aged white ASA), 15 W/m²K per plate face, view factors from the probe of 0.1 (cap), 0.1 (bottom plate) and 0.6 (other plates, 0.5 K warm); inner air speed 10 to 30 % of a 1 m/s wind | Handbook ranges; assumed |
| Mass | ASA 1.07, aluminum 2.70, stainless 7.90 g/cm³ from model volumes; FieldNode V-blocks and small clamps (0.20 kg) and back plate (0.47 kg) left off | Estimates |
| Wind | 35 m/s gust; air 1.225 kg/m³; drag coefficient 1.2 on the projected area; band preload 1,000 N (as FND-CAL-001), friction 0.3 | Screening values, not a code check |

## A. Power and energy (R9)

- **PM sensor.** 0.275 W while running at 20 % duty (60 s in 300 s) is 55.0 mW typical, or 65.0 mW at the datasheet maximum [A1].
- **Port load.** The NO2 front end and ADC add 7.5 mW continuously and the T and RH sensor 0.01 mW, for 62.5 mW typical [A2]. With the maximum SPS30 current and the 1.2 margin, the design load is 87.0 mW, against FieldNode's 100 mW design value and 115 mW ceiling [A3]. R9 is met on paper under either figure, with 13 mW left under the design value.
- **Core.** At a 5 min interval each uplink costs 52.9 mJ at SF9, and the core uses 9.0 mWh/day including sensor wake-ups and sleep, against 4.0 mWh/day for FieldNode alone at 15 min [A4].
- **Daily draw.** 2.33 Wh/day from the cell, a 97.1 mW average [A5].
- **Autonomy.** A full cell lasts 6.6 days without sun, 4.6 days at -20 °C and 5.3 days at end of cell life [A6]. The cold figure is below the 5 days FieldNode's own R6 asks of its core; AirStreet's R9 does not set an autonomy target.
- **Energy balance.** In FieldNode's worst month the cell stores 7.75 Wh/day against 2.33 Wh drawn, 3.3 times the demand [A7]. On a hot clear day without FieldNode's sun shield only 0.8 Wh is stored, a 1.53 Wh/day deficit, which a full cell covers for 10 such days in a row [A8]; the shield is required above 45 °C (DDR-002).
- **Clean air.** The SPS30 needs up to 30 s to its first reading at low particle counts, so the 60 s run (DDR-002) leaves at least 30 s of valid readings. The 30 s run of v0.1 gave 48.0 mW [A9].

## B. Data, airtime and storage (R8, R10)

- **Record.** Eight 2-byte values (PM1, PM2.5, PM10, WE, AE, T, RH, status), a 2-byte counter and 2 bytes of flags: 20 bytes, 288 records a day [B1].
- **Airtime.** With 13 bytes of LoRaWAN overhead on a 125 kHz channel, one uplink takes 72 ms at SF7, 134 ms at SF8, 247 ms at SF9, 453 ms at SF10 and 1,810 ms at SF12 [B2]. The TRL 2 figure of about 1.3 s at SF12 was low.
- **EU868 duty cycle.** The worst case, SF12, uses 0.60 % of each 5 min, so the 1 % sub-band limit is met at every spreading factor [B3]. R10 is met on paper.
- **Fair use.** On The Things Network's 30 s/day fair-use policy, a 5 min interval fits only at SF7 (20.7 s); SF8 needs 38.5 s and SF9 71.1 s [B4]. Under DDR-002 the node reports every 5 min only through a private gateway (TwinKit by default, FND-DDR-001 D7), where this limit does not apply, and every 15 min on TTN. At 15 min an uplink takes 12.8 s/day at SF8 and 23.7 s/day at SF9, inside 30 s, but 43.5 s/day at SF10, so fair use is met up to SF9 [B8].
- **US915.** The 400 ms dwell limit allows SF9 (247 ms) and not SF10 (453 ms) [B5].
- **Storage.** 7 days of store and forward take 40.3 kB of FieldNode's 16 MB flash [B6], and an hourly mean is ready within one record interval of the hour's end, at most 15 min on TTN [B7]. R8 is met on paper.

## C. NO2 error budget (R2, R3, R4)

- **Units and resolution.** 1 ppb = 1.880 µg/m³ at 25 °C; one ADC step of 62.5 µV is 0.25 ppb at the assumed gain [C1].
- **Hourly error.** The hourly terms (1σ) are noise 0.46 ppb after averaging 120 samples, calibration residual 4.39 ppb, drift 0.87 ppb and transfer bias 2.00 ppb, 4.92 ppb in all [C2]. That is a mean absolute error of 3.9 ppb (7.4 µg/m³) against the 5 ppb of R2 [C3]. R2 is at risk: every term except noise rests on literature or an assumption, and only collocation can show it.
- **Annual mean.** Random terms average out over a year, but the transfer bias, the drift residual and the collocation intercept (0.59 ppb from 14 days) do not: 2.26 ppb, or 4.25 µg/m³, against 2 µg/m³ [C4]. Meeting 2 µg/m³ would need the transfer bias held to 0.16 ppb, which no field calibration can promise [C6]. R3 is therefore withdrawn as a requirement and kept as a research question (DDR-002).
- **EU limit.** At 90 % one-sided confidence, a street's annual mean can be classified against 40 µg/m³ only if it is below 34.6 or above 45.4 µg/m³ [C5]. R4 is at risk: it holds for streets well clear of the limit but not for those near it.

## D. Radiation shield (R5)

- **Plate temperatures.** In 1,000 W/m² sun the cap runs 8.3 K and the bottom plate 1.7 K above ambient; the mean radiant excess seen by the probe is 1.30 K [D2].
- **Probe error.** With inside air at 30 % of a 1 m/s wind the probe reads 0.26 K high from radiation and 0.16 K from warmed air, 0.42 K in all; at 10 % it reads 0.38 K and 0.49 K, 0.87 K in all [D1]. The 1.5 mm plates (2 mm before v0.6) leave slightly wider gaps between plates, so a little more air passes. Both are under the 1 °C of R5, but the result depends on the inner air speed, which is assumed.
- **Humidity.** A 0.87 K warm error reads 2.4 % RH low at 50 % RH and 4.1 % RH low at 85 % RH, at 30 °C [D3]. The SHT45 alone meets ±0.5 °C and ±3 % RH, but the shield error at high humidity does not. R5 is at risk.

## E. PM2.5 error with humidity (R1)

- **RH input.** The humidity correction uses RH with an uncertainty of 4.3 % (1 % sensor and the shield error at 85 % RH) [E1].
- **Error against the bound.** Table 2 compares the combined error with the R1 bound of ±5 µg/m³ or ±30 % [E2].

*Table 2. Hourly PM2.5 error after humidity correction, µg/m³ (bound in parentheses).*

| RH | 10 µg/m³ | 25 µg/m³ | 50 µg/m³ |
| --- | --- | --- | --- |
| 50 % | 2.2 (5.0) | 3.2 (7.5) | 5.4 (15.0) |
| 70 % | 2.6 (5.0) | 4.7 (7.5) | 8.6 (15.0) |
| 80 % | 3.1 (5.0) | 6.3 (7.5) | 12.1 (15.0) |
| 85 % | 3.6 (5.0) | **7.8 (7.5)** | **15.2 (15.0)** |
| 90 % | 4.7 (5.0) | **10.8 (7.5)** | **21.4 (15.0)** |

- **Result.** R1 is met on paper up to 80 % RH at every level tested, which is also the top of the SPS30's recommended humidity range [E3]. Above 85 % RH the particles' water uptake is steep and the correction is uncertain. R1 is at risk for humid climates and nights.

## F. Geometry, area and mass (R11, R13)

- **Fit.** Inlet plane 3,000 mm above the sidewalk, inside the EU 1,500 to 4,000 mm range; 140° V-saddles and bands cut to length fit 80 to 200 mm poles; no drilling [F1]. R11 is met by design.
- **Layout.** FieldNode's whip clears the pod's drip lid by 15 mm (23 mm in v0.2, before FieldNode's antenna moved 28 mm toward the pod and the pod moved 20 mm away), the clamps are 375 mm apart, the node is 706 mm tall and it stands 172 mm out from the pole face (173 mm before the rail was thinned) [F2].
- **Area.** Rasterizing the model gives 0.139 m² seen from the street and 0.054 m² along it, against 0.15 m² [F3] (0.143 m² in v0.5, 0.126 m² in v0.2). FieldNode's constructable bracket, the adapter plates and the cross arm add to the outline; the plate windows above and below the enclosure take a little off it. R13's area limit is met on paper.
- **Mass.** FieldNode core as used 1.89 kg (FieldNode's base node of 2.45 kg less its back plate, V-blocks and bands, 0.56 kg); rail 0.19 kg; adapter plates 0.21 kg; cross arm 0.19 kg; V-saddles 0.10 kg (6 walls and 40 % infill, 57 % of solid); pod shell and floor 0.37 kg; shield plates, cap and spacers 0.23 kg; bands 0.10 kg; shield rods 0.06 kg; sensors, front end, probe, cables, glands, inserts and fixings 0.29 kg [F4]. In all 3.62 kg on the pole and 3.78 kg with FieldNode's sun shield at a hot site, against 4.0 kg including the shield: 0.22 kg of margin. The sensor head and mount are 1.73 kg [F5]. R13 is met on paper; the pole owner of the first site is still to confirm the load.
- **Lightening.** The four steps of AST-DDR-003, A1 take 0.22 kg off: 3.84 to 3.62 kg without the sun shield and 4.00 to 3.78 kg with it [F8]. The saddles save 0.08 kg, the thinner rail 0.05 kg, the plate windows 0.06 kg and the thinner shield plates 0.04 kg. The "about 3.6 kg" of AST-DDR-003, A1 is the node without the sun shield; with it the lightened node is 3.78 kg, close to the 3.76 kg estimated when the recommendation was reviewed.
- **Why it rose.** FieldNode's constructable core is 0.15 kg heavier as AirStreet uses it, and the parts that make AirStreet buildable (adapter plates in place of adapter bars, the cross arm in place of the short shield arm, larger saddles, the separate pod floor, spacers and fixings) add the rest [F6]. Option (c) of AST-DDR-003, A1 was accepted on 2026-10-02: the limit is 4.0 kg and the four lightening steps are now in the design.
- **Bands.** Each band runs 487 mm round the 140 mm design pole and its saddle, 326 mm round an 80 mm pole and 664 mm round a 200 mm pole, plus about 100 mm for the housing and tail [F7].

## G. Wind and mounting

- **Load.** A 35 m/s gust gives 750 Pa and 125 N on the node at about 3.33 m, or 416 N·m at the pole base [G1]. The pole's capacity is for its owner to confirm.
- **Clamps.** The downward load of 76 N (weight and wind on the tilted panel) compares with 1,885 N of friction from two bands, a factor of 25 [G2]. Twist about the pole from wind on the offset shield is 2.42 N·m against 132 N·m [G5]. Both rest on the assumed 1,000 N band preload.
- **Cross arm.** The 30 x 30 x 3 mm angle carries the shield (0.30 kg, 12.1 N of wind) 200 mm to the right of the rail and the pod (0.46 kg) 90 mm to the left: 0.60 N·m vertical and 2.42 N·m horizontal at the rail, 4.4 MPa [G3]. Its two M5 bolts each take about 67 N in the gust [G4].
- **Rail and pod.** The rail at the lower clamp carries 26.6 N and 2.73 N·m, 25.6 MPa in the 40 x 4 mm bar (16.4 MPa in the 40 x 5 mm bar of v0.5) [G6]. Each of the pod's two hanging screws takes about 11 N in the gust, far below what an M5 heat-set insert in ASA holds; the insert pull-out is to be checked at TRL 4 [G7]. Every stress is far below the roughly 150 MPa yield of 6063 aluminium.

## H. Service and environment (R12, R16)

- **Service time.** Under DDR-002 the pod is exchanged whole: ladder 5 min, unplug two M12 plugs and the probe lead 1.5 min, release the pod 1.5 min, fit the pre-collocated pod 2 min, reconnect and check glands 1.5 min, uplink check 2 min: about 14 min against 15 min [H1]. The exchange pod arrives with its collocation and CalRig record, and the returned pod is serviced and recollocated at the reference site [H2]. R16 is met on paper, with a small margin.
- **Temperature range.** FieldNode is rated for -20 to +45 °C ambient and reaches 58.7 to 73.3 °C inside at 45 °C, while AirStreet's R12 asks for -10 to 50 °C [H3]. The SPS30's recommended range is 10 to 40 °C and 20 to 80 % RH, with absolute limits of -10 to 60 °C and 0 to 95 % RH [H4]. Under DDR-002 FieldNode's sun shield is required at sites above 45 °C, so R12 asks for it there; FieldNode has now designed it (FND-DDR-003), and it fixes to AirStreet's adapter plates (AST-DDR-003). R12 stays at risk; condensation and insects in the pod remain unverified.

## I. Cost (R15)

- **Totals.** The BOM has 11 lines, all priced: $433.50 per node, of which the FieldNode core is $131.00 (FieldNode's $139.00 less its unused $8.00 pole mounting kit; costed in FieldNode, AST-DDR-001 D1) and the sensor head $302.50 [I1].
- **Against the value-engineering target.** Value-engineering target: USD 285. Estimated cost of the constructable design: USD 302.50 (USD 17.50 over the target) [I2]. `budget_usd` is a hypothetical control target. **R15 is over the target by $17.50.** The rise from $285.00 is in line 3 (band stock, adapter plates and cross arm, +$4.50), line 9 (probe tube, +$1), line 10 (probe lead with its M8 plug, +$4) and line 11 (inserts, glands, probe socket, terminal block and fixings, +$8). Line 8 is back to $9.00: the thinner shield plates save about as much filament as the spacers use. In line 3 the thinner rail saves about $0.50, and the saddles are repriced at about $3.00 of filament at 40 % infill (the $1.50 used before was low), so line 3 is $21.50. The cost drivers and savings worth trying are in the design decisions register and AST-DDR-003, A2.
- **Running costs.** A replacement NO2 sensor about every 2 years and the collocation time are not in the BOM [I3].

## J. Results

*Table 3. Requirement status (AST-REQ-001 v0.8). Counts, as the script's line [J1] prints them: 1 over the value-engineering target, 5 at risk, 5 met on paper, 4 met by design, 1 withdrawn.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R15 | Low cost | Sensor head $302.50; $433.50 with FieldNode [I1] | Sensor head $285 value-engineering target (`budget_usd`) | Over the target by $17.50 |
| R1 | PM2.5 | Within the bound up to 80 % RH, outside it above 85 % RH [E2] | ±5 µg/m³ or ±30 % hourly | At risk |
| R2 | NO2 | Hourly MAE about 3.9 ppb [C3] | 5 ppb or less | At risk |
| R4 | EU limit classification | Decisive outside 34.6 to 45.4 µg/m³ [C5] | 90 % confidence at 40 µg/m³ | At risk |
| R5 | T and RH | Shield 0.42 to 0.87 K at 1 m/s; 4.1 % RH low at 85 % RH [D1, D3] | ±0.5 °C, ±3 % RH; radiation 1 °C or less | At risk |
| R12 | Survive outdoors | FieldNode sun shield required above 45 °C, designed and fits the adapter plates; SPS30 recommended to 80 % RH [H3, H4] | -10 to 50 °C; shield above 45 °C | At risk |
| R13 | Light and compact | 3.78 kg with the sun shield (3.62 kg without); 0.139 m² [F3, F5] | 4.0 kg with the sun shield (3.5 kg until 2026-10-02); 0.15 m² | Met on paper (0.22 kg margin) |
| R8 | Reporting | 5 min on the private gateway; 15 min on TTN, fair use met up to SF9; 7 days = 40.3 kB [B6, B8] | 5 min private, 15 min TTN; hourly within 15 min; 7 days | Met on paper |
| R9 | Power | 87.0 mW design load; 2.33 Wh/day against 7.75 Wh [A3, A7] | 115 mW or less; energy neutral | Met on paper |
| R10 | Duty cycle | 0.082 % at SF9, 0.60 % at SF12 [B3] | Below 1 % | Met on paper |
| R16 | Serviceable | About 14 min for a pod exchange [H1] | Pre-collocated pod in 15 min | Met on paper |
| R6 | Stated calibration | CalRig for T, RH, PM; collocation per D3 | Calibration record per node | Met by design |
| R7 | Raw data | Raw WE, AE, PM, T, RH and version tag | Raw signals kept | Met by design |
| R11 | Pole mounting | 80 to 200 mm, V-saddles and bands, inlet 3.0 m [F1] | No drilling; 1.5 to 4 m | Met by design |
| R14 | Levels only | Levels, T and RH only | No images, audio or identifiers | Met by design |
| R3 | NO2 near the WHO guideline | 4.2 µg/m³ annual (1σ) [C4] | Withdrawn; research question | Withdrawn |

*Table 4. TRL 2 numbers checked (v0.1).*

| TRL 2 figure | TRL 3 value | Action |
| --- | --- | --- |
| Sensor power about 41 mW, 45 mW with margin | 35.0 mW typical, 48.0 mW design | Precis updated |
| Airtime about 1.3 s at SF12, 0.5 % | 1.81 s, 0.60 % | Precis and requirements updated |
| Mass about 3.0 kg | 3.65 kg (FieldNode 2.41 kg, not 1.7 kg) | R13 not met in v0.1; see Table 5 |
| Frontal area about 0.09 m² | 0.138 m² from the model | R13 not met in v0.1; see Table 5 |
| Cost $391 per node; $265 sensor head | $409.00; $283.00 | BOM repriced |
| NO2 hourly error about 5 ppb | About 3.9 ppb MAE, budget of assumed terms | R2 stays at risk |

*Table 5. Changes from v0.1 under AST-DDR-002.*

| Quantity | v0.1 | v0.2 | Decision |
| --- | --- | --- | --- |
| PM run per record | 30 s | 60 s | PM run length |
| Design sensor load | 48.0 mW | 87.0 mW | PM run length |
| Autonomy without sun | 11.9 days | 6.6 days | PM run length |
| Reporting | 5 min on any network | 5 min private gateway; 15 min on TTN | Fair use on TTN |
| Mass on the pole | 3.65 kg | 3.26 kg | Back plate left off |
| Frontal area | 0.138 m² against 0.12 m² | 0.126 m² against 0.15 m² | Back plate left off; area limit relaxed |
| Sensor head cost | $283.00 against $180 | $285.00 against $285 | Budget figure; adapter bars |
| Service | 14 min sensor swap, recollocation needed | 14 min pod exchange | Pod as exchange unit |
| R3 | Not met | Withdrawn, research question | WHO guideline |

*Table 6. Changes from v0.2 under AST-DDR-003 (design for construction).*

| Quantity | v0.2 | v0.3 | Reason |
| --- | --- | --- | --- |
| Mass on the pole | 3.26 kg | 3.84 kg (4.00 kg with the sun shield) | FieldNode's constructable core; adapter plates, cross arm, saddles, pod floor, fixings |
| Frontal area | 0.126 m² | 0.143 m² | FieldNode's bracket, plates and cross arm |
| Wind on the node | 114 N, 379 N·m | 128 N, 428 N·m | Larger area |
| Sensor head cost | $285.00 | $303.00 | Parts added for construction |
| FieldNode core cost | $126.00 | $131.00 | FieldNode's constructable BOM less its pole mounting kit |
| Whip clearance to the pod | 23 mm | 15 mm | FieldNode's antenna moved; pod moved 20 mm left |
| Shield arm | 20 x 8 mm bar, 4.6 MPa | 30 x 30 x 3 mm cross arm carrying pod and shield, 4.5 MPa | Pod and shield needed fixings |
| R13 | Met on paper | Not met against 3.5 kg; at risk against 4.0 kg | Limit set at 4.0 kg with the sun shield, AST-DDR-003 A1, accepted 2026-10-02 |
| R15 | Met on paper | Over the value-engineering target by $18.00 | Parts added for construction, AST-DDR-003 |

*Table 7. Changes from v0.5 under AST-DDR-003, A1 (lightening steps, accepted 2026-10-02).*

| Quantity | v0.5 | v0.6 | Reason |
| --- | --- | --- | --- |
| Rail | 40 x 5 mm, 0.24 kg, 16.4 MPa | 40 x 4 mm, 0.19 kg, 25.6 MPa | Thinner bar |
| Adapter plates | 0.27 kg | 0.21 kg | Two windows in each plate |
| V-saddles | 0.18 kg (solid) | 0.10 kg (6 walls, 40 % infill) | Print settings counted in the mass |
| Shield plates, cap and spacers | 0.27 kg | 0.23 kg | Plates 1.5 mm (was 2 mm) |
| Mass on the pole | 3.84 kg (4.00 kg with the sun shield) | 3.62 kg (3.78 kg with the sun shield) | The four steps together |
| Frontal area | 0.143 m² | 0.139 m² | Plate windows |
| Wind on the node | 128 N, 428 N·m | 125 N, 416 N·m | Smaller area |
| Shield error at 1 m/s | 0.43 to 0.89 K | 0.42 to 0.87 K | Wider gaps between thinner plates |
| Sensor head cost | $303.00 | $302.50 | Lines 3 and 8 repriced |
| R13 | At risk (4.00 kg against 4.0 kg) | Met on paper (3.78 kg against 4.0 kg) | Lightening steps in the design |
| R15 | Over the target by $18.00 | Over the target by $17.50 | Lines 3 and 8 repriced |

---
doc_id: AST-CAL-001
title: AirStreet sizing calculations
project: AirStreet
doc_type: Calculation
version: "0.8"
status: Draft
date: '2026-10-30'
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
- version: "0.7"
  date: '2026-10-24'
  author: Amish Chadha
  change: "STEM check fixes made under Amish's standing instruction of 2026-10-23 (AST-DDR-005): NO2 noise from the datasheet (C2), ozone filter life (C7), rated-range flags (H5), band thickness read from the model; hollow shield spacers of the D3 model (3.77 kg with the sun shield); requirements cited from AST-PRS-001"
- version: "0.8"
  date: '2026-10-30'
  author: Amish Chadha
  change: "Amish's decisions of 2026-10-30 (AST-DDR-006): tube hood in mass, area, wind, cross arm and cost (3.70 kg, 3.86 kg with the sun shield, 0.144 m2, USD 306.00); R4 against 40 and 20 ug/m3 [C9]"
---

# AirStreet sizing calculations

Version 0.8 (2026-10-30) carries Amish's decisions of that day into the numbers (AST-DDR-006): the diffusion tube hood with three clips on the cross arm (decision 2) adds 0.09 kg, 0.005 m² of frontal area and $3.50 (line 12 and two inserts, screws and washers in line 11), so the node weighs 3.70 kg on the pole and 3.86 kg with FieldNode's sun shield (margin 0.14 kg), presents 0.144 m² (limit 0.15 m²), and the sensor head costs $306.00, $21.00 over the target; R4 is now worked against both 40 and 20 µg/m³ (decision 4, [C9]). Version 0.7 (2026-10-24) adds the STEM check fixes of AST-DDR-005, made under Amish's standing instruction of 2026-10-23: the NO2 noise term now uses the sensor datasheet's 15 ppb at 2 sigma (C2), the NO2 cell is replaced before its ozone filter is used up (C7), every record carries flags for readings outside the sensors' rated ranges (H5), and the band thickness is read from the model (0.6 mm, as the mass always used); the D3 model's hollow shield spacers take 0.01 kg off. The independent review of 2026-10-24 (AST-STM-001) then corrected the NO2 budget (the noise averages over 12 independent records an hour, not 120 samples; a 5 % slope term; the EU reference temperature of 20 °C), the cross arm bolt force, the rail check (twist and minimum yield) and the ozone rule, and added sensitivity lines (C8, D4, B9, G1, G8). The hourly NO2 error rises from about 3.9 to 4.3 ppb and the annual uncertainty from 4.25 to 4.65 µg/m³; no requirement status changes. Version 0.6 followed the constructable design of AST-DDR-003 (2026-09-30), which made every part of the node buildable and moved onto FieldNode's own constructable core, with the four lightening steps of AST-DDR-003, A1 (accepted on 2026-10-02) now in the model: a 40 x 4 mm rail, windows in the adapter plates, 1.5 mm shield plates and saddles printed at 40 % infill. On paper AirStreet now meets nine of its sixteen requirements (five by calculation, four by design), has five at risk and is over its cost target on one (R15); R3 stays withdrawn. The node weighs 3.61 kg on the pole and 3.77 kg with FieldNode's sun shield, against R13's limit of 4.0 kg including the shield (set on 2026-10-02; it was 3.5 kg), so R13 is met on paper with 0.23 kg of margin; before the lightening it was 4.00 kg, on the limit. The pole owner of the first site is still to confirm the 4.0 kg load. Value-engineering target: USD 285. Estimated cost of the constructable design: USD 302.50 (USD 17.50 over the target); the cost drivers and savings worth trying are in the design decisions register. The frontal area, 0.139 m², stays inside 0.15 m², and every mounting part carries its load with a large margin. Power and airtime are unchanged from v0.2, the NO2 error budget is larger after the review (4.3 ppb hourly MAE, 4.65 µg/m³ annual), and the thinner shield plates change the shield and humidity results only in the second decimal: the 60 s particle run gives an 87.0 mW design sensor load inside FieldNode's 100 mW allowance and 6.6 days without sun, and an annual NO2 mean carries about 4.65 µg/m³ of uncertainty (1σ). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the node is safe to mount on any particular pole, and they are not a substitute for the pole owner's structural check, for electrical checks on the FieldNode cell or for field collocation of the sensors. AirStreet data are indicative, not a regulatory measurement or health advice. See AST-PRC-001, Safety.

## Scope and method

The note checks every requirement in AST-PRS-001 v0.10 (cited here by the R numbers in its "Was" column: R1 is PR-001, and so on) against the design in AST-PRC-001 v0.9 and the parametric model `cad/src/model.py`, which builds the FieldNode core from FieldNode's own model (vendored as `cad/src/fieldnode_core.py`). The script imports the model's `PARAMS`, derived dimensions and part solids, so the pod, shield, rail, clamp positions and projected areas used here are those in the STEP files and in drawing AST-DWG-001. It reads `bom/bom.csv` and `budget_usd` in `project.yaml`. FieldNode figures are taken from FND-CAL-001 (v0.1 for power and energy, v0.3 for mass) in the FieldNode repo. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

The design case is a 140 mm street light pole with the inlet plane 3.0 m above the sidewalk (AST-DDR-001 D7), one record every 5 min with a 60 s PM run (D8 and DDR-002), LoRaWAN at SF9 in EU868 through a private gateway (15 min on The Things Network), FieldNode's back plate left off (DDR-002), and ambient -10 to 50 °C.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| PM sensor | SPS30 at 5 V, 55 mA typical and 65 mA maximum in measurement mode; 41 x 41 x 12 mm, 26.3 g; up to 30 s to first reading at low particle counts; recommended 10 to 40 °C and 20 to 80 % RH | Sensirion SPS30 datasheet (07/2023), checked 2026-09-25 |
| NO2 chain | Front end and ADC held on continuously, 1.5 mA at 5 V; overall gain 0.25 mV/ppb; 7.5 ppb (1σ) noise per 1 s sample; 10 samples per record; ozone filter 500 ppm h; rated -30 to 40 °C and 15 to 85 % RH continuous | Noise, filter and range from the NO2-B43F data sheet ([Alphasense](https://pdf.directindustry.com/pdf/alphasense/no2-b43f/16860-1025996.html), checked 2026-10-24; 15 ppb at 2σ); current and gain assumed |
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
- **Autonomy.** A full cell lasts 6.6 days without sun, 4.6 days at -20 °C, 5.3 days at end of cell life and 3.7 days cold at end of life [A6]. A LiFePO4 cell is not charged below 0 °C, so a sub-zero spell is ridden through on the stored charge (AST-STM-001 S4). The cold figure is below the 5 days FieldNode's own R6 asks of its core; AirStreet's R9 does not set an autonomy target.
- **Energy balance.** In FieldNode's worst month the cell stores 7.75 Wh/day against 2.33 Wh drawn, 3.3 times the demand [A7]. On a hot clear day without FieldNode's sun shield only 0.8 Wh is stored, a 1.53 Wh/day deficit, which a full cell covers for 10 such days in a row [A8]; the shield is required above 45 °C (DDR-002).
- **Clean air.** The SPS30 needs up to 30 s to its first reading at low particle counts, so the 60 s run (DDR-002) leaves at least 30 s of valid readings. The 30 s run of v0.1 gave 48.0 mW [A9].

## B. Data, airtime and storage (R8, R10)

- **Record.** Eight 2-byte values (PM1, PM2.5, PM10, WE, AE, T, RH, status), a 2-byte counter and 2 bytes of flags: 20 bytes, 288 records a day [B1].
- **Airtime.** With 13 bytes of LoRaWAN overhead on a 125 kHz channel, one uplink takes 72 ms at SF7, 134 ms at SF8, 247 ms at SF9, 453 ms at SF10 and 1,810 ms at SF12 [B2]. The TRL 2 figure of about 1.3 s at SF12 was low.
- **EU868 duty cycle.** The worst case, SF12, uses 0.60 % of each 5 min, so the 1 % sub-band limit is met at every spreading factor [B3]. R10 is met on paper.
- **Fair use.** On The Things Network's 30 s/day fair-use policy, a 5 min interval fits only at SF7 (20.7 s); SF8 needs 38.5 s and SF9 71.1 s [B4]. Under DDR-002 the node reports every 5 min only through a private gateway (TwinKit by default, FND-DDR-001 D7), where this limit does not apply, and every 15 min on TTN. At 15 min an uplink takes 12.8 s/day at SF8 and 23.7 s/day at SF9, inside 30 s, but 43.5 s/day at SF10, so fair use is met up to SF9 [B8].
- **US915.** The 400 ms dwell limit allows SF9 (247 ms) and not SF10 (453 ms) [B5].
- **Storage.** 7 days of store and forward take 40.3 kB of FieldNode's 16 MB flash [B6], and an hourly mean is ready within one record interval of the hour's end, at most 15 min on TTN [B7]. A full 7-day backlog of 2,016 records takes about 14 h to send at SF9 within the 1 % duty cycle through a private gateway; on TTN a backlog cannot be flushed within 30 s a day, so store and forward relies on the private gateway [B9]. R8 is met on paper.

## C. NO2 error budget (R2, R3, R4)

- **Units and resolution.** 1 ppb = 1.880 µg/m³ at 25 °C; one ADC step of 62.5 µV is 0.25 ppb at the assumed gain [C1].
- **Hourly error.** The hourly terms (1σ) are noise 2.17 ppb (7.5 ppb per sample from the data sheet, averaged over the 12 independent records of an hour: the 10 samples of one record fall within the cell's response time, so they are not independent; v0.6 used 5 ppb over 120 samples, 0.46 ppb), calibration residual 4.39 ppb, drift 0.87 ppb, transfer bias 2.00 ppb and a slope term of 1.00 ppb (a 5 % span error left after a 14-day collocation, at a 20 ppb street mean; assumed), 5.45 ppb in all [C2]. On The Things Network each 15 min uplink carries the mean of its three 5 min records, so the same 12 records an hour are averaged. That is a mean absolute error of 4.3 ppb (8.2 µg/m³) against the 5 ppb of R2 [C3]. R2 is at risk: every term except noise rests on literature or an assumption (the 3.5 ppb residual comes from a model that also used other gas sensors on its node, so it is optimistic for an NO2 cell alone), and only collocation can show it.
- **Annual mean.** Random terms average out over a year, but the transfer bias, the drift residual, the collocation intercept (0.59 ppb from 14 days) and the slope term do not: 2.47 ppb, or 4.65 µg/m³, against 2 µg/m³ [C4]. With the slope term, 2 µg/m³ cannot be met even with no transfer bias at all [C6]. R3 is therefore withdrawn as a requirement and kept as a research question (DDR-002).
- **EU limit.** The directive refers gas concentrations to 20 °C, where 1 ppb is 1.913 µg/m³. At 90 % one-sided confidence, a street's annual mean can be classified against 40 µg/m³ only if it is below 33.9 or above 46.1 µg/m³ [C5]. R4 is at risk: it holds for streets well clear of the limit but not for those near it. The recast Directive (EU) 2024/2881 lowers the limit to 20 µg/m³ from 2030; against it the band is 13.9 to 26.1 µg/m³ [C9]; since Amish's decision 4 of 2026-10-30 R4 classifies against both limits (AST-DEC-001, AST-DDR-006). If the street transfer bias is 3 ppb rather than 2 (a 5 to 10 % fall in NO2 from 1.5 to 3 m), the 40 µg/m³ band widens to 31.8 to 48.2 µg/m³ [C8].
- **Ozone filter.** The cell's ozone filter holds more than 500 ppm h. At a 30 ppb annual mean ozone it lasts 23 months, at 40 ppb 17 months, and at the 50 to 60 ppb of hot, sunny sites 14 to 11 months, against the cell's 24-month life [C7]. So the cell is replaced every 12 months at the pod exchange, or at 18 or 24 months where the collocated reference station's ozone record shows the dose since fitting stays under 500 ppm h by then (AST-DDR-005 F3).

## D. Radiation shield (R5)

- **Plate temperatures.** In 1,000 W/m² sun the cap runs 8.3 K and the bottom plate 1.7 K above ambient; the mean radiant excess seen by the probe is 1.30 K [D2].
- **Probe error.** With inside air at 30 % of a 1 m/s wind the probe reads 0.26 K high from radiation and 0.16 K from warmed air, 0.42 K in all; at 10 % it reads 0.38 K and 0.49 K, 0.87 K in all [D1]. The 1.5 mm plates (2 mm before v0.6) leave slightly wider gaps between plates, so a little more air passes. Both are under the 1 °C of R5, but the result depends on the inner air speed, which is assumed: it passes 1 K once the inner air falls below 8.3 % of the wind, so in calm sun the error exceeds 1 K [D4]. The result is fragile and is checked against an aspirated reference at TRL 4.
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
- **Area.** Rasterizing the model gives 0.144 m² seen from the street and 0.055 m² along it, against 0.15 m² [F3] (0.139 m² in v0.7 before the tube hood of AST-DDR-006, 0.143 m² in v0.5, 0.126 m² in v0.2). FieldNode's constructable bracket, the adapter plates and the cross arm add to the outline; the plate windows above and below the enclosure take a little off it. R13's area limit is met on paper.
- **Mass.** FieldNode core as used 1.89 kg (FieldNode's base node of 2.45 kg less its back plate, V-blocks and bands, 0.56 kg); rail 0.19 kg; adapter plates 0.21 kg; cross arm 0.19 kg; V-saddles 0.10 kg (6 walls and 40 % infill, 57 % of solid); pod shell and floor 0.37 kg; shield plates, cap and spacers 0.22 kg (the spacers are tubes with a 5.5 mm bore for the rods since v0.7); bands 0.10 kg (12.7 x 0.6 mm, read from the model); shield rods 0.06 kg; the diffusion tube hood and its three clips 0.08 kg (printed solid, from the model; AST-DDR-006); sensors, front end, probe, cables, glands, inserts and fixings 0.29 kg [F4]. In all 3.70 kg on the pole and 3.86 kg with FieldNode's sun shield at a hot site, against 4.0 kg including the shield: 0.14 kg of margin. The sensor head and mount are 1.81 kg [F5]. R13 is met on paper; the pole owner of the first site is still to confirm the load.
- **Lightening.** The four steps of AST-DDR-003, A1 took 0.22 kg off (3.84 to 3.62 kg without the sun shield and 4.00 to 3.78 kg with it); with the hollow spacers of v0.7 the totals were 3.61 and 3.77 kg, and with the tube hood of v0.8 they are 3.70 and 3.86 kg [F8]. The saddles save 0.08 kg, the thinner rail 0.05 kg, the plate windows 0.06 kg and the thinner shield plates 0.04 kg. The "about 3.6 kg" of AST-DDR-003, A1 is the node without the sun shield; with it the lightened node was 3.77 kg before the tube hood, close to the 3.76 kg estimated when the recommendation was reviewed.
- **Why it rose.** FieldNode's constructable core is 0.15 kg heavier as AirStreet uses it, and the parts that make AirStreet buildable (adapter plates in place of adapter bars, the cross arm in place of the short shield arm, larger saddles, the separate pod floor, spacers and fixings) add the rest [F6]. Option (c) of AST-DDR-003, A1 was accepted on 2026-10-02: the limit is 4.0 kg and the four lightening steps are now in the design.
- **Bands.** Each band runs 487 mm round the 140 mm design pole and its saddle, 326 mm round an 80 mm pole and 664 mm round a 200 mm pole, plus about 100 mm for the housing and tail [F7].

## G. Wind and mounting

- **Load.** A 35 m/s gust gives 750 Pa and 129 N on the node at about 3.33 m, or 431 N·m at the pole base [G1] (125 N and 416 N·m before the tube hood). 35 m/s is a screening speed; where the local code asks 45 m/s the load is 214 N and 712 N·m. The pole's capacity is for its owner to confirm.
- **Clamps.** The downward load of 75 N (weight and wind on the tilted panel) compares with 1,885 N of friction from two bands, a factor of 25 [G2]. Twist about the pole from wind on the offset shield and tube hood is 2.79 N·m against 132 N·m [G5]. Both rest on the assumed 1,000 N band preload.
- **Cross arm.** The 30 x 30 x 3 mm angle carries the shield (0.30 kg, 12.1 N of wind) 200 mm to the right of the rail, the tube hood (0.09 kg, 4.8 N of wind) 78 mm to the right and the pod (0.46 kg) 90 mm to the left: 0.65 N·m vertical and 2.79 N·m horizontal at the rail, 5.1 MPa [G3]. Its two M5 bolts, 20 mm apart, resist the wind's twist as a couple: the worse bolt takes about 148 N in the gust, against about 7,000 N proof load [G4] (127 N before the tube hood, 67 N before the review, which halved the couple).
- **Rail and pod.** The rail at the lower clamp carries 26.6 N and 2.73 N·m, 25.6 MPa in the 40 x 4 mm bar (16.4 MPa in the 40 x 5 mm bar of v0.5) [G6]. Each of the pod's two hanging screws takes about 11 N in the gust, far below what an M5 heat-set insert in ASA holds; the insert pull-out is to be checked at TRL 4 [G7]. With the cross arm's 2.79 N·m twist the rail also carries 14.1 MPa of torsion, 35.4 MPa von Mises, against 73 MPa (the minimum yield of 6063-T5, about 110 MPa, over 1.5) [G8]. Every stress is well below yield.

## H. Service and environment (R12, R16)

- **Service time.** Under DDR-002 the pod is exchanged whole: ladder 5 min, unplug two M12 plugs and the probe lead 1.5 min, release the pod 1.5 min, fit the pre-collocated pod 2 min, reconnect and check glands 1.5 min, uplink check 2 min: about 14 min against 15 min [H1]. The exchange pod arrives with its collocation and CalRig record, and the returned pod is serviced and recollocated at the reference site [H2]. R16 is met on paper, with a small margin.
- **Temperature range.** FieldNode is rated for -20 to +45 °C ambient and reaches 58.7 to 73.3 °C inside at 45 °C, while AirStreet's R12 asks for -10 to 50 °C [H3]. The SPS30's recommended range is 10 to 40 °C and 20 to 80 % RH, with absolute limits of -10 to 60 °C and 0 to 95 % RH [H4]. Under DDR-002 FieldNode's sun shield is required at sites above 45 °C, so R12 asks for it there; FieldNode has now designed it (FND-DDR-003), and it fixes to AirStreet's adapter plates (AST-DDR-003). R12 stays at risk; condensation and insects in the pod remain unverified.
- **Rated ranges.** The NO2-B43F is rated -30 to 40 °C and 15 to 85 % RH continuous, and the SPS30 is recommended for 10 to 40 °C and 20 to 80 % RH, while R12 asks the node to survive -10 to 50 °C [H5]. Every record therefore carries flags (AST-DDR-005 F2): shield air above 35 °C (40 °C less an estimated 5 K by which the sunlit pod air runs above the shield air, to measure at TRL 4; 3 K before the review), RH above 80 % for PM and above 85 % for NO2, RH below 20 % for PM and below 15 % for NO2, and below 10 °C for PM. Flagged hours are kept and published with the flag, not dropped, so a map can show them; the flag is set from the shield's T and RH already in the record, so the record stays 20 bytes. R7 now names the flags; R12 stays at risk.

## I. Cost (R15)

- **Totals.** The BOM has 12 lines, all priced: $437.00 per node, of which the FieldNode core is $131.00 (FieldNode's $139.00 less its unused $8.00 pole mounting kit; costed in FieldNode, AST-DDR-001 D1) and the sensor head $306.00 [I1].
- **Against the value-engineering target.** Value-engineering target: USD 285. Estimated cost of the constructable design: USD 306.00 (USD 21.00 over the target) [I2]. `budget_usd` is a hypothetical control target and is not raised. **R15 is over the target by $21.00.** The tube hood of AST-DDR-006 added $3.50: line 12 (the printed hood and three clips, 0.081 kg of ASA at about $30/kg, $2.50, an estimate) and $1.00 in line 11 (two inserts, two screws and two washers, an estimate); the diffusion tubes are a running cost at about £8 each with analysis (2015 price), not in the BOM. The rise from $285.00 is in line 3 (band stock, adapter plates and cross arm, +$4.50), line 9 (probe tube, +$1), line 10 (probe lead with its M8 plug, +$4) and line 11 (inserts, glands, probe socket, terminal block and fixings, +$8). Line 8 is back to $9.00: the thinner shield plates save about as much filament as the spacers use. In line 3 the thinner rail saves about $0.50, and the saddles are repriced at about $3.00 of filament at 40 % infill (the $1.50 used before was low), so line 3 is $21.50. The cost drivers and savings worth trying are in the design decisions register and AST-DDR-003, A2.
- **Running costs.** A replacement NO2 sensor every 12 months (18 or 24 where the site's ozone record allows) [C7], and the collocation time, are not in the BOM [I3].

## J. Results

*Table 3. Requirement status (AST-PRS-001 v0.10, by the R numbers in its "Was" column). Counts, as the script's line [J1] prints them: 1 over the value-engineering target, 5 at risk, 5 met on paper, 4 met by design, 1 withdrawn.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R15 | Low cost | Sensor head $306.00; $437.00 with FieldNode [I1] | Sensor head $285 value-engineering target (`budget_usd`) | Over the target by $21.00 |
| R1 | PM2.5 | Within the bound up to 80 % RH, outside it above 85 % RH [E2] | ±5 µg/m³ or ±30 % hourly | At risk |
| R2 | NO2 | Hourly MAE about 4.3 ppb [C3] | 5 ppb or less | At risk |
| R4 | EU limit classification | Decisive outside 33.9 to 46.1 µg/m³ (40) and 13.9 to 26.1 µg/m³ (20 from 2030) [C5, C9] | 90 % confidence at 40 and 20 µg/m³ | At risk |
| R5 | T and RH | Shield 0.42 to 0.87 K at 1 m/s; 4.1 % RH low at 85 % RH [D1, D3] | ±0.5 °C, ±3 % RH; radiation 1 °C or less | At risk |
| R12 | Survive outdoors | FieldNode sun shield required above 45 °C, designed and fits the adapter plates; SPS30 recommended to 80 % RH [H3, H4] | -10 to 50 °C; shield above 45 °C | At risk |
| R13 | Light and compact | 3.86 kg with the sun shield (3.70 kg without); 0.144 m² [F3, F5] | 4.0 kg with the sun shield (3.5 kg until 2026-10-02); 0.15 m² | Met on paper (0.14 kg margin) |
| R8 | Reporting | 5 min on the private gateway; 15 min on TTN, fair use met up to SF9; 7 days = 40.3 kB [B6, B8] | 5 min private, 15 min TTN; hourly within 15 min; 7 days | Met on paper |
| R9 | Power | 87.0 mW design load; 2.33 Wh/day against 7.75 Wh [A3, A7] | 115 mW or less; energy neutral | Met on paper |
| R10 | Duty cycle | 0.082 % at SF9, 0.60 % at SF12 [B3] | Below 1 % | Met on paper |
| R16 | Serviceable | About 14 min for a pod exchange [H1] | Pre-collocated pod in 15 min | Met on paper |
| R6 | Stated calibration | CalRig for T, RH, PM; collocation per D3 | Calibration record per node | Met by design |
| R7 | Raw data | Raw WE, AE, PM, T, RH, version tag and rated-range flags [H5] | Raw signals kept | Met by design |
| R11 | Pole mounting | 80 to 200 mm, V-saddles and bands, inlet 3.0 m [F1] | No drilling; 1.5 to 4 m | Met by design |
| R14 | Levels only | Levels, T and RH only | No images, audio or identifiers | Met by design |
| R3 | NO2 near the WHO guideline | 4.65 µg/m³ annual (1σ) [C4] | Withdrawn; research question | Withdrawn |

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

*Table 8. Changes from v0.6 under AST-DDR-005 (STEM check fixes, 2026-10-24, made under Amish's standing instruction of 2026-10-23).*

| Quantity | v0.6 | v0.7 | Reason |
| --- | --- | --- | --- |
| NO2 noise per sample | 5 ppb (1σ), assumed, over 120 samples an hour | 7.5 ppb (1σ), data sheet 15 ppb at 2σ, over 12 independent records | F1 and the review |
| NO2 slope term | None | 1.00 ppb (5 % at 20 ppb, assumed) | Review |
| NO2 hourly total | 4.92 ppb, MAE 3.9 ppb | 5.45 ppb, MAE 4.3 ppb | F1 and the review |
| NO2 annual (1σ) | 2.26 ppb, 4.25 µg/m³ | 2.47 ppb, 4.65 µg/m³ | Review |
| EU limit band (R4) | 34.6 to 45.4 µg/m³ at 25 °C | 33.9 to 46.1 µg/m³ at the directive's 20 °C | Review |
| NO2 cell replacement | About every 2 years | Every 12 months, or 18 or 24 where the ozone record allows | F3 and the review |
| Rated-range flags | None | Shield air above 35 °C; RH above 80 % (PM) or 85 % (NO2), below 20 % (PM) or 15 % (NO2); below 10 °C (PM) | F2 and the review |
| Cross arm bolt force | 67 N | 127 N (couple on one bolt) | Review |
| Rail check | 25.6 MPa bending against about 150 MPa | 33.2 MPa von Mises with twist against 73 MPa (minimum yield over 1.5) | Review |
| Band in the model | 12.7 x 0.8 mm (calculation used 0.6 mm) | 12.7 x 0.6 mm, read from the model | F4 |
| Shield plates, cap and spacers | 0.229 kg (solid spacers in the model) | 0.222 kg (spacers with a 5.5 mm bore) | F5, D3 model |
| Mass on the pole | 3.62 kg (3.78 kg with the sun shield) | 3.61 kg (3.77 kg) | F5 |
| Downward load on the clamps | 76 N | 75 N | F5 |

*Table 9. Changes from v0.7 under AST-DDR-006 (Amish's decisions of 2026-10-30).*

| Quantity | v0.7 | v0.8 | Reason |
| --- | --- | --- | --- |
| Mass on the pole | 3.61 kg (3.77 kg with the sun shield) | 3.70 kg (3.86 kg) | Tube hood and clips 0.081 kg, hood screws and inserts 0.006 kg (decision 2) |
| Mass margin to 4.0 kg | 0.23 kg | 0.14 kg | Same |
| Frontal area | 0.139 m² | 0.144 m² | Hood 92 mm wide and 58 mm deep seen from the street |
| Wind on the node, 35 m/s | 125 N, 416 N·m | 129 N, 431 N·m | Larger area; at 45 m/s 214 N and 712 N·m |
| Cross arm | 0.58 N·m vertical, 2.42 N·m horizontal, 4.4 MPa | 0.65 N·m vertical, 2.79 N·m horizontal, 5.1 MPa | Hood on the shield side, 78 mm from the rail |
| Cross arm bolt force | 127 N | 148 N | Same |
| Rail, von Mises with twist | 33.2 MPa | 35.4 MPa | Same |
| BOM | 11 lines, sensor head $302.50 | 12 lines, sensor head $306.00 | Line 12 $2.50 and line 11 $1.00, both estimates |
| R15 | Over the target by $17.50 | Over the target by $21.00 | Same |
| R4 | Classify against 40 µg/m³ | Classify against 40 and 20 µg/m³ | Decision 4 [C9] |

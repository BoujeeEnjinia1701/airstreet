---
doc_id: AST-CAL-001
title: AirStreet sizing calculations
project: AirStreet
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (power and energy, airtime and storage, NO2 error budget, radiation shield, PM2.5 humidity error, geometry, mass and area, wind and mounting, service, cost)
---

# AirStreet sizing calculations

On paper, AirStreet meets seven of its sixteen requirements (three by calculation, four by design), has six at risk and misses three. The misses are NO2 near the WHO guideline (R3), mass and frontal area on the pole (R13) and cost (R15). An annual NO2 mean carries about 4.2 µg/m³ of uncertainty (1σ) against the 2 µg/m³ of R3, because a reference-to-street transfer bias of a few ppb does not average away. The node weighs 3.65 kg against 3.5 kg and presents 0.138 m² to the street against 0.12 m², mostly because the FieldNode core weighs 2.41 kg, not the 1.7 kg assumed at TRL 2. The sensor head costs $283.00, over both the $180 `budget_usd` and the $280 recommended in AST-DDR-001. Power is comfortable: the design sensor load is 48 mW against FieldNode's 100 mW design allowance, and a full cell lasts 11.9 days without sun. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the node is safe to mount on any particular pole, and they are not a substitute for the pole owner's structural check, for electrical checks on the FieldNode cell or for field collocation of the sensors. AirStreet data are indicative, not a regulatory measurement or health advice. See AST-PRC-001, Safety.

## Scope and method

The note checks every requirement in AST-REQ-001 v0.3 against the design in AST-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and part solids, so the pod, shield, rail, clamp positions and projected areas used here are those in the STEP files and in drawing AST-DWG-001. It reads `bom/bom.csv` and `budget_usd` in `project.yaml`. FieldNode figures are taken from FND-CAL-001 v0.1 in the FieldNode repo. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

The design case is a 140 mm street light pole with the inlet plane 3.0 m above the sidewalk (AST-DDR-001 D7), one record every 5 min with a 30 s PM run (D8), LoRaWAN at SF9 in EU868, and ambient -10 to 50 °C.

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
| Mass | ASA 1.07, aluminum 2.70, stainless 7.90 g/cm³ from model volumes; FieldNode V-blocks and small clamps (0.20 kg) left off | Estimates |
| Wind | 35 m/s gust; air 1.225 kg/m³; drag coefficient 1.2 on the projected area; band preload 1,000 N (as FND-CAL-001), friction 0.3 | Screening values, not a code check |

## A. Power and energy (R9)

- **PM sensor.** 0.275 W while running at 10 % duty is 27.5 mW typical, or 32.5 mW at the datasheet maximum [A1].
- **Port load.** The NO2 front end and ADC add 7.5 mW continuously and the T and RH sensor 0.01 mW, for 35.0 mW typical [A2]. With the maximum SPS30 current and the 1.2 margin, the design load is 48.0 mW, against FieldNode's 100 mW design value and 115 mW ceiling [A3]. R9 is met on paper under either figure.
- **Core.** At a 5 min interval each uplink costs 52.9 mJ at SF9, and the core uses 9.0 mWh/day including sensor wake-ups and sleep, against 4.0 mWh/day for FieldNode alone at 15 min [A4].
- **Daily draw.** 1.29 Wh/day from the cell, a 53.7 mW average [A5].
- **Autonomy.** A full cell lasts 11.9 days without sun, 8.3 days at -20 °C and 9.5 days at end of cell life [A6].
- **Energy balance.** In FieldNode's worst month the cell stores 7.75 Wh/day against 1.29 Wh drawn, 6.0 times the demand [A7]. On a hot clear day without FieldNode's proposed sun shield only 0.8 Wh is stored, a 0.49 Wh/day deficit, which a full cell covers for 31 such days in a row [A8].
- **Clean air.** The SPS30 needs up to 30 s to its first reading at low particle counts, so a 30 s run may return no reading in clean air. A 60 s run raises the design load to 87.0 mW, still inside 100 mW [A9]. This is listed in `docs/REVIEW.md` as a new item.

## B. Data, airtime and storage (R8, R10)

- **Record.** Eight 2-byte values (PM1, PM2.5, PM10, WE, AE, T, RH, status), a 2-byte counter and 2 bytes of flags: 20 bytes, 288 records a day [B1].
- **Airtime.** With 13 bytes of LoRaWAN overhead on a 125 kHz channel, one uplink takes 72 ms at SF7, 134 ms at SF8, 247 ms at SF9, 453 ms at SF10 and 1,810 ms at SF12 [B2]. The TRL 2 figure of about 1.3 s at SF12 was low.
- **EU868 duty cycle.** The worst case, SF12, uses 0.60 % of each 5 min, so the 1 % sub-band limit is met at every spreading factor [B3]. R10 is met on paper.
- **Fair use.** On The Things Network's 30 s/day fair-use policy, a 5 min interval fits only at SF7 (20.7 s); SF8 needs 38.5 s and SF9 71.1 s [B4]. The default network is a private TwinKit gateway (FND-DDR-001 D7), where this limit does not apply, but a TTN fallback needs a longer interval or SF7. New item in `docs/REVIEW.md`.
- **US915.** The 400 ms dwell limit allows SF9 (247 ms) and not SF10 (453 ms) [B5].
- **Storage.** 7 days of store and forward take 40.3 kB of FieldNode's 16 MB flash [B6], and an hourly mean is ready within one record interval of the hour's end [B7]. R8 is met on paper.

## C. NO2 error budget (R2, R3, R4)

- **Units and resolution.** 1 ppb = 1.880 µg/m³ at 25 °C; one ADC step of 62.5 µV is 0.25 ppb at the assumed gain [C1].
- **Hourly error.** The hourly terms (1σ) are noise 0.46 ppb after averaging 120 samples, calibration residual 4.39 ppb, drift 0.87 ppb and transfer bias 2.00 ppb, 4.92 ppb in all [C2]. That is a mean absolute error of 3.9 ppb (7.4 µg/m³) against the 5 ppb of R2 [C3]. R2 is at risk: every term except noise rests on literature or an assumption, and only collocation can show it.
- **Annual mean.** Random terms average out over a year, but the transfer bias, the drift residual and the collocation intercept (0.59 ppb from 14 days) do not: 2.26 ppb, or 4.25 µg/m³, against 2 µg/m³ [C4]. **R3 is not met.** Meeting it would need the transfer bias held to 0.16 ppb, which no field calibration can promise [C6].
- **EU limit.** At 90 % one-sided confidence, a street's annual mean can be classified against 40 µg/m³ only if it is below 34.6 or above 45.4 µg/m³ [C5]. R4 is at risk: it holds for streets well clear of the limit but not for those near it.

## D. Radiation shield (R5)

- **Plate temperatures.** In 1,000 W/m² sun the cap runs 8.3 K and the bottom plate 1.7 K above ambient; the mean radiant excess seen by the probe is 1.30 K [D2].
- **Probe error.** With inside air at 30 % of a 1 m/s wind the probe reads 0.26 K high from radiation and 0.17 K from warmed air, 0.43 K in all; at 10 % it reads 0.38 K and 0.52 K, 0.89 K in all [D1]. Both are under the 1 °C of R5, but the result depends on the inner air speed, which is assumed.
- **Humidity.** A 0.89 K warm error reads 2.5 % RH low at 50 % RH and 4.2 % RH low at 85 % RH, at 30 °C [D3]. The SHT45 alone meets ±0.5 °C and ±3 % RH, but the shield error at high humidity does not. R5 is at risk.

## E. PM2.5 error with humidity (R1)

- **RH input.** The humidity correction uses RH with an uncertainty of 4.4 % (1 % sensor and the shield error at 85 % RH) [E1].
- **Error against the bound.** Table 2 compares the combined error with the R1 bound of ±5 µg/m³ or ±30 % [E2].

*Table 2. Hourly PM2.5 error after humidity correction, µg/m³ (bound in parentheses).*

| RH | 10 µg/m³ | 25 µg/m³ | 50 µg/m³ |
| --- | --- | --- | --- |
| 50 % | 2.2 (5.0) | 3.2 (7.5) | 5.4 (15.0) |
| 70 % | 2.6 (5.0) | 4.7 (7.5) | 8.7 (15.0) |
| 80 % | 3.1 (5.0) | 6.3 (7.5) | 12.2 (15.0) |
| 85 % | 3.6 (5.0) | **7.9 (7.5)** | **15.4 (15.0)** |
| 90 % | 4.8 (5.0) | **11.0 (7.5)** | **21.7 (15.0)** |

- **Result.** R1 is met on paper up to 80 % RH at every level tested, which is also the top of the SPS30's recommended humidity range [E3]. Above 85 % RH the particles' water uptake is steep and the correction is uncertain. R1 is at risk for humid climates and nights.

## F. Geometry, area and mass (R11, R13)

- **Fit.** Inlet plane 3,000 mm above the sidewalk, inside the EU 1,500 to 4,000 mm range; band clamps fit 80 to 200 mm poles; no drilling [F1]. R11 is met by design.
- **Layout.** The FieldNode whip clears the pod lid by 23 mm, the clamps are 375 mm apart, the node is 706 mm tall and it stands 176 mm out from the pole face [F2]. The pod is offset to -X so that the whip, on FieldNode's bottom face at x = 58 mm, hangs beside it.
- **Area.** Rasterizing the model gives 0.138 m² seen from the street and 0.046 m² along it, against 0.12 m² [F3].
- **Mass.** FieldNode core as used 2.21 kg, rail 0.31 kg, shield arm 0.10 kg, saddles 0.06 kg, band clamps 0.13 kg, pod 0.36 kg, shield 0.26 kg and bought sensor-head parts 0.23 kg [F4]: 3.65 kg on the pole against 3.5 kg; the sensor head and mount alone are 1.44 kg [F5]. **R13 is not met** on either mass or area. The TRL 2 figures (3.0 kg, 0.09 m²) used 1.7 kg for FieldNode.
- **Option.** Fixing the FieldNode enclosure and panel bracket straight to the AirStreet rail and leaving off FieldNode's 0.47 kg back plate gives 3.19 kg [F6]. It changes the FieldNode mounting interface, so it is proposed in `docs/REVIEW.md`, not applied.

## G. Wind and mounting

- **Load.** A 35 m/s gust gives 750 Pa and 124 N on the node at about 3.33 m, or 414 N·m at the pole base [G1]. The pole's capacity is for its owner to confirm.
- **Clamps.** The downward load of 76 N (weight and wind on the tilted panel) compares with 1,885 N of friction from two bands, a factor of 25 [G2]. Twist about the pole from wind on the offset shield is 2.33 N·m against 132 N·m [G4]. Both rest on the assumed 1,000 N band preload.
- **Arm and rail.** The shield arm carries 11.7 N and 2.44 N·m, 4.6 MPa in the 20 x 8 mm bar [G3]; the rail below the lower clamp carries 26.2 N and 2.69 N·m, 16.1 MPa in the 40 x 5 mm bar [G5], both far below the roughly 170 MPa yield of 6063 aluminum.

## H. Service and environment (R12, R16)

- **Service time.** Ladder 5 min, lid 1.5 min, SPS30 2 min, NO2 sensor 2 min, lid and seals 1.5 min, uplink check 2 min: about 14 min against 15 min [H1]. A new NO2 sensor has no field calibration until it has been collocated, so a pre-collocated spare pod is the practical unit of exchange [H2]. R16 is at risk.
- **Temperature range.** FieldNode is rated for -20 to +45 °C ambient and reaches 58.7 to 73.3 °C inside at 45 °C, while AirStreet's R12 asks for -10 to 50 °C [H3]. The SPS30's recommended range is 10 to 40 °C and 20 to 80 % RH, with absolute limits of -10 to 60 °C and 0 to 95 % RH [H4]. R12 is at risk; condensation and insects in the pod remain unverified.

## I. Cost (R15)

- **Totals.** The BOM has 11 lines, all priced: $409.00 per node, of which the FieldNode core is $126.00 (costed in FieldNode, AST-DDR-001 D1) and the sensor head $283.00 [I1].
- **Against the budget.** The sensor head is $103.00 over the $180 `budget_usd` and $3.00 over the $280 recommended in AST-DDR-001, which is awaiting Amish [I2]. **R15 is not met** against either figure. The main change from TRL 2 is the SPS30, now $60.50 at a checked retail price instead of $45.
- **Running costs.** A replacement NO2 sensor about every 2 years and the collocation time are not in the BOM [I3].

## J. Results

*Table 3. Requirement status (AST-REQ-001 v0.3). Counts: 3 not met, 6 at risk, 3 met on paper, 4 met by design [J1].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R3 | NO2 near the WHO guideline | 4.2 µg/m³ annual (1σ) [C4] | 2 µg/m³ or less at 10 µg/m³ | **Not met** |
| R13 | Light and compact | 3.65 kg; 0.138 m² [F3, F5] | 3.5 kg; 0.12 m² | **Not met** |
| R15 | Low cost | Sensor head $283.00; $409.00 with FieldNode [I1] | Sensor head $180 (`budget_usd`); $280 proposed | **Not met** |
| R1 | PM2.5 | Within the bound up to 80 % RH, outside it above 85 % RH [E2] | ±5 µg/m³ or ±30 % hourly | At risk |
| R2 | NO2 | Hourly MAE about 3.9 ppb [C3] | 5 ppb or less | At risk |
| R4 | EU limit classification | Decisive outside 34.6 to 45.4 µg/m³ [C5] | 90 % confidence at 40 µg/m³ | At risk |
| R5 | T and RH | Shield 0.43 to 0.89 K at 1 m/s; 4.2 % RH low at 85 % RH [D1, D3] | ±0.5 °C, ±3 % RH; radiation 1 °C or less | At risk |
| R12 | Survive outdoors | FieldNode rated to 45 °C; SPS30 recommended to 80 % RH [H3, H4] | -10 to 50 °C | At risk |
| R16 | Serviceable | About 14 min; recollocation after an NO2 swap [H1] | 15 min | At risk |
| R8 | Reporting | 5 min; hourly within about 5 min; 7 days = 40.3 kB [B6] | 5 min; 15 min; 7 days | Met on paper |
| R9 | Power | 48.0 mW design load; 1.29 Wh/day against 7.75 Wh [A3, A7] | 115 mW or less; energy neutral | Met on paper |
| R10 | Duty cycle | 0.082 % at SF9, 0.60 % at SF12 [B3] | Below 1 % | Met on paper |
| R6 | Stated calibration | CalRig for T, RH, PM; collocation per D3 | Calibration record per node | Met by design |
| R7 | Raw data | Raw WE, AE, PM, T, RH and version tag | Raw signals kept | Met by design |
| R11 | Pole mounting | 80 to 200 mm, band clamps, inlet 3.0 m [F1] | No drilling; 1.5 to 4 m | Met by design |
| R14 | Levels only | Levels, T and RH only | No images, audio or identifiers | Met by design |

*Table 4. TRL 2 numbers checked.*

| TRL 2 figure | TRL 3 value | Action |
| --- | --- | --- |
| Sensor power about 41 mW, 45 mW with margin | 35.0 mW typical, 48.0 mW design | Precis updated |
| Airtime about 1.3 s at SF12, 0.5 % | 1.81 s, 0.60 % | Precis and requirements updated |
| Mass about 3.0 kg | 3.65 kg (FieldNode 2.41 kg, not 1.7 kg) | R13 now not met |
| Frontal area about 0.09 m² | 0.138 m² from the model | R13 now not met |
| Cost $391 per node; $265 sensor head | $409.00; $283.00 | BOM repriced |
| NO2 hourly error about 5 ppb | About 3.9 ppb MAE, budget of assumed terms | R2 stays at risk |

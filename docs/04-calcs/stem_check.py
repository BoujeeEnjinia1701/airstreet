"""AirStreet STEM check, AST-STM-001 (STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv and prints the verdict counts. Option A numbers come from
docs/04-calcs/sizing.py (AST-CAL-001), which this script runs first, so the check follows any change in the
design or the calculation note. Options B and C (AST-OPT-001) are first-order screens with their own
estimates, stated below. The "closed_by" field names the decision or calculation that closed a row; an empty
field leaves a Plausible row open.
"""
import contextlib
import io
import math
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from stem_check import Check, WITHIN, PLAUSIBLE, FIX  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    S = runpy.run_path(str(ROOT / "docs" / "04-calcs" / "sizing.py"))

c = Check(ROOT / "docs" / "04-calcs" / "stem_results.csv")
CAL = "AST-CAL-001"

# ------------------------------------------------------------------ option A, the current design
c.claim("S1", "The sensor port load (design case, maximum SPS30 current and 1.2 margin) fits FieldNode's 100 mW design allowance",
        "Physics", "Electromagnetism and circuits", law="P = V I x duty; SPS30 datasheet 65 mA maximum at 5 V, 60 s in 300 s; front end 1.5 mA held on (CAL [A3])",
        value=round(S["p_design"], 1), limit=100.0, unit="mW", rule="below", closed_by=CAL)
c.balance("S2", "In FieldNode's worst month the cell is charged with more energy than the node draws in a day",
          "Chemistry", "Electrochemistry and batteries", inputs={"stored": S["E_STORED_WORST"]}, outputs={"drawn": round(S["e_day"], 2)},
          unit="Wh/day", law="Energy balance; FND-CAL-001 worst-month storage 7.75 Wh/day (CAL [A7])", closed_by=CAL)
c.order_of_magnitude("S3", "A full 6 Ah LiFePO4 cell (80 % usable) runs the node 6.6 days without sun", "Chemistry", "Electrochemistry and batteries",
                     claimed=6.6, estimate=6.0 * 3.2 * 0.8 / (0.097 * 24), unit="days", law="Usable energy over average draw (97 mW) (CAL [A6])", closed_by=CAL)
c.cited("S4", "The LiFePO4 cell is not charged below 0 degC; a cold spell is ridden through on the cell (4.6 days at -20 degC)",
        "Chemistry", "Electrochemistry and batteries", law="LiFePO4 charge temperature limit (cell maker's data, in FieldNode); capacity ratio 0.70 at -20 degC (FND-CAL-001)",
        detail="Autonomy 4.6 days at -20 degC (CAL [A6]); the first partner's climate data must show no sub-zero spell longer than that", verdict=PLAUSIBLE)
t9 = S["t_air"][9]
c.order_of_magnitude("S5", "A 20-byte uplink takes about 247 ms at SF9 on a 125 kHz channel", "Engineering and technology", "Power and link budgets",
                     claimed=247.0, estimate=(8 + 4.25 + 48) * (2 ** 9) / 125e3 * 1e3, unit="ms",
                     law="Semtech AN1200.13 time-on-air formula, 33 bytes with LoRaWAN overhead, 48 payload symbols (CAL [B2])", closed_by=CAL)
c.claim("S6", "The worst-case uplink (SF12) stays under the 1 % duty cycle of an EU868 sub-band", "Engineering and technology", "Standards practice",
        law="ETSI EN 300 220 and LoRaWAN EU868 regional parameters; 1.81 s in each 300 s (CAL [B3])",
        value=round(S["t_air"][12] / S["T_REC"] * 100, 2), limit=1.0, unit="%", rule="below", closed_by=CAL)
c.claim("S7", "In US915 the 20-byte record fits the 400 ms dwell limit at SF9 (DR1 carries up to 53 bytes; DR0 at SF10 carries 11)",
        "Engineering and technology", "Standards practice", law="FCC 47 CFR 15.247 dwell time; LoRaWAN US915 regional parameters (CAL [B5])",
        value=round(t9 * 1e3), limit=400.0, unit="ms", rule="below", closed_by=CAL)
c.claim("S8", "At 15 min on The Things Network the node keeps within 30 s of airtime a day up to SF9", "Engineering and technology", "Standards practice",
        law="The Things Network fair use policy, 30 s per device per day (CAL [B8])", value=round(t9 * 96, 1), limit=30.0, unit="s/day", rule="below", closed_by=CAL)
c.cited("S9", "The 16-bit ADC's step is not what limits the NO2 reading (the cell's noise is)",
        "Chemistry", "Analytical", law="NO2-B43F sensitivity -200 to -650 nA/ppm (Alphasense datasheet); 0.8 mV/nA front end; ADS1115 62.5 uV step",
        detail=f"0.16 to 0.52 mV/ppb, so one ADC step is 0.12 to 0.39 ppb, 20 to 60 times below the 7.5 ppb noise per sample (CAL [C1])", verdict=WITHIN, closed_by=CAL)
c.cited("S10", "Noise term of the hourly NO2 budget: per-sample noise taken from the sensor datasheet",
        "Mathematics", "Statistics and uncertainty", law="NO2-B43F datasheet noise 15 ppb at 2 sigma; averaging 120 samples an hour divides it by the square root of 120",
        detail=f"Was 5 ppb (1 sigma) assumed over 120 samples (Fails, fix proposed); now 7.5 ppb over the 12 independent records of an hour (the 10 samples of a record fall within the cell's response time), {S['s_noise']:.2f} ppb hourly, total {S['s_hour']:.2f} ppb, MAE {S['mae']:.1f} ppb (CAL [C2], [C3])",
        verdict=WITHIN, closed_by="AST-DDR-005 F1")
c.cited("S11", f"After field calibration the hourly NO2 mean absolute error is about {S['mae']:.1f} ppb, within 5 ppb",
        "Mathematics", "Statistics and uncertainty", law="Field-calibrated residual 3.5 ppb MAE (Zimmerman et al., 2018, a model that also drew on other gas sensors on the node, so optimistic for WE, AE, T and RH alone); drift, street transfer bias and a 5 % slope error assumed (CAL C)",
        detail=f"Budget {S['s_hour']:.2f} ppb (1 sigma), MAE {S['mae']:.1f} ppb; only collocation at TRL 4 can show it (PR-002 at risk)", verdict=PLAUSIBLE)
c.claim("S12", "An annual NO2 mean cannot be resolved to 2 ug/m3, so AirStreet makes no claim at the WHO guideline", "Mathematics", "Statistics and uncertainty",
        law="Systematic terms do not average out over a year (CAL [C4])", value=round(S["s_year"] * S["UG"], 2), limit=2.0, unit="ug/m3", rule="above", closed_by=CAL)
c.order_of_magnitude("S13", "1 ppb of NO2 is 1.88 ug/m3 at 25 degC, and 1.91 ug/m3 at the 20 degC the EU directive uses for limit values", "Chemistry", "Environmental and atmospheric chemistry",
                     claimed=1.913, estimate=46.0055 / 24.055, unit="ug/m3 per ppb at 20 degC", law="Ideal gas molar volume 24.465 L/mol at 25 degC and 24.055 L/mol at 20 degC; NO2 46.006 g/mol; Directive 2008/50/EC refers gas volumes to 293 K (CAL [C1], [C5])", closed_by=CAL)
c.cited("S14", "The NO2 cell's ozone filter lasts until the cell is replaced", "Chemistry", "Analytical",
        law="NO2-B43F datasheet: ozone filter capacity more than 500 ppm h at 0.5 ppm O3; operating life more than 24 months (to 50 % signal)",
        detail=f"At 40 to 60 ppb mean ozone the filter is used up in {S['o3_life'][1]:.0f} to {S['o3_life'][3]:.0f} months, before the 24-month replacement assumed before (Fails, fix proposed); "
               "now the cell is replaced every 12 months at the pod exchange, or at 18 or 24 months where the site's ozone record keeps the dose under 500 ppm h (CAL [C7])",
        verdict=WITHIN, closed_by="AST-DDR-005 F3")
c.cited("S15", "Every reading taken outside the sensors' rated temperature and humidity ranges is marked as such in the data",
        "Engineering and technology", "Sensing resolution",
        law="NO2-B43F rated -30 to 40 degC and 15 to 85 % RH continuous; SPS30 recommended 10 to 40 degC and 20 to 80 % RH (datasheets)",
        detail=f"Rated-range flags in every record: shield air above {S['t_flag']:.0f} degC (a 5 K pod allowance, to measure at TRL 4), RH above 80 % or 85 % and below 20 % or 15 %, below 10 degC for PM; flagged hours are published with the flag (CAL [H5])",
        verdict=WITHIN, closed_by="AST-DDR-005 F2")
c.cited("S33", "The NO2 cell and the particle sensor measure validly inside their rated ranges; hours beyond them (the node is built for -10 to 50 degC, 10 to 100 % RH) are flagged and published as indicative",
        "Engineering and technology", "Sensing resolution",
        law="NO2-B43F rated -30 to 40 degC and 15 to 85 % RH continuous; SPS30 recommended 10 to 40 degC and 20 to 80 % RH (datasheets)",
        detail="Above 40 degC and 85 % RH the cell runs outside its rating; the flags (S15) mark those hours but do not make them valid. Failed on first check (Fails, fix proposed); Amish decided option (a) on 2026-10-30: accept the flagged hours now and seek a cell rated above 40 degC with the partner when one is agreed (AST-DEC-001 decision 3). The flag threshold and the pod allowance are measured at TRL 4",
        verdict=PLAUSIBLE, closed_by="AST-DDR-006 decision 3")
c.cited("S16", "After humidity correction the hourly PM2.5 error stays within 5 ug/m3 or 30 % up to 80 % RH",
        "Physics", "Optics and radiation", law="Laser scattering counts particles; kappa-Koehler water uptake 1 + kappa aw / (1 - aw), kappa 0.3 +/- 0.1 assumed (CAL E)",
        detail="Within the bound to 80 % RH, outside it at 85 % RH and above at 25 and 50 ug/m3 (CAL [E2]); the comparison is at 1 sigma (about 68 % of hours), the base error and kappa are assumed and the RH is the shield's, not the pod's, so collocation at TRL 4 confirms it", verdict=PLAUSIBLE)
c.claim("S17", "The passive eight-plate shield keeps the radiation error of the air temperature under 1 K at 1 m/s wind in full sun", "Physics", "Heat transfer",
        law="Plate energy balance and probe convection (Zukauskas), inner air at 10 to 30 % of the wind (assumed) (CAL D)",
        value=round(S["err_hi"], 2), limit=1.0, unit="K", rule="below", margin=0.2)   # passes only while inner air moves at 8 % of the wind or more (CAL [D4])
c.order_of_magnitude("S18", "A 0.87 K warm error reads about 4.1 % RH low at 85 % RH and 30 degC", "Physics", "Thermodynamics",
                     claimed=4.1, estimate=85 - 85 * math.exp(17.62 * 30 / (243.12 + 30)) / math.exp(17.62 * 30.87 / (243.12 + 30.87)), unit="% RH",
                     law="Magnus saturation vapour pressure (Sonntag constants) (CAL [D3])", closed_by=CAL)
c.order_of_magnitude("S19", "A 35 m/s gust puts about 129 N on the node", "Physics", "Fluid mechanics",
                     claimed=129.0, estimate=0.5 * 1.225 * 35 ** 2 * 1.2 * 0.144, unit="N", law="F = 0.5 rho v^2 Cd A, Cd 1.2 on the 0.144 m2 model silhouette (with the tube hood); 35 m/s is a screening speed, 214 N at 45 m/s for windier codes (CAL [G1])", closed_by=CAL)
c.claim("S20", "Two bands hold the node against slipping down the pole", "Physics", "Mechanics and statics",
        law="Belt friction F = mu T theta per band, 1,000 N preload and mu 0.3 assumed; load is weight and wind on the tilted panel (CAL [G2])",
        value=round(S["f_down"]), limit=round(S["slip_cap"]), unit="N", rule="below", closed_by=CAL)
c.claim("S21", "The 40 x 4 mm rail at the lower clamp stays below the yield of 6063 aluminium with a factor of 1.5, in bending and twist together", "Physics", "Strength of materials",
        law="Bending M / Z and flat-bar torsion T / (0.31 b t^2), von Mises; 6063-T5 minimum yield about 110 MPa (CAL [G6], [G8])", value=round(S["sig_vm"], 1), limit=73.0, unit="MPa", rule="below", closed_by=CAL)
c.claim("S22", "The cross arm carries the pod, the shield and the tube hood far below yield (with a factor of 1.5)", "Physics", "Strength of materials",
        law="Combined bending of a 30 x 30 x 3 angle (CAL [G3])", value=round(S["sig"], 1), limit=100.0, unit="MPa", rule="below", closed_by=CAL)
c.cited("S23", "The 12.7 x 0.6 mm stainless band carries its 1,000 N preload below yield (with a factor of 1.5)", "Physics", "Strength of materials",
        law="Tension stress T / (w t); 304 stainless, minimum yield 205 MPa annealed (ASTM A240); worm-drive bands are cold rolled and stronger, but slotted",
        detail=f"Gross section {1000.0 / (12.7 * S['P']['band'][1]):.0f} MPa against 137 MPa; at the worm slots, with about 35 % of the section cut away, about 200 MPa; to confirm with the band maker's rated tension (AST-DEC-001, to confirm item 1)",
        verdict=PLAUSIBLE)
c.cited("S24", "The band thickness used for the mass is the one in the model", "Mathematics", "Units and dimensional analysis",
        law="One source of dimensions: the calculation reads PARAMS (STANDARDS section 24)",
        detail="The model drew a 0.8 mm band while the mass used 0.6 mm (Fails, fix proposed); now 0.6 mm in the model and read from it (CAL [F4])",
        verdict=WITHIN, closed_by="AST-DDR-005 F4")
c.cited("S25", "Printed ASA saddles keep the band preload over years in sun", "Chemistry", "Materials and polymer chemistry",
        law="ASA is UV stable outdoors; printed thermoplastics creep under sustained load, faster when warm (heat deflection of ASA about 95 degC at 0.45 MPa)",
        detail="Contact stress on the V faces is low (a few MPa), but creep at up to about 60 degC surface temperature can relax the preload; a re-torque at the first pod exchange and a check at TRL 4", verdict=PLAUSIBLE)
c.cited("S26", "The pod's two hanging screws hold in their heat-set inserts with a wide margin", "Physics", "Strength of materials",
        law="Worst pull-out per screw from weight and wind prying about the 40 mm bearing edge, shared by the two screws in line (CAL [G7]), against an M5 insert in printed ASA",
        detail="About 11 N per screw against an assumed 200 N for the insert, which is not yet from maker data and falls when the ASA is warm; pull test at 23 and 60 degC at TRL 4 (AST-DEC-001, to confirm item 8)",
        verdict=PLAUSIBLE)
c.cited("S27", "Traffic NO2 varies several fold within city blocks, so street-level nodes see what a city station misses",
        "Biology", "Epidemiology", law="Apte et al. (2017), Oakland: NO2 varied 5 to 8 times within single blocks; WHO ambient air quality fact sheet",
        detail="Cited as the problem, not as a health claim; AirStreet gives indicative levels, not health advice", verdict=WITHIN)
c.cited("S28", "Inlets 3.0 m above the sidewalk sample the street air people breathe closely enough to rank streets",
        "Chemistry", "Environmental and atmospheric chemistry", law="EU Directive 2008/50/EC Annex III: inlets 1.5 to 4 m above ground; Defra diffusion tube guidance: 2 to 4 m, higher tubes may read low",
        detail="Inside the regulated range; a small vertical gradient is part of the transfer bias term (CAL C)", verdict=WITHIN)
c.claim("S29", "A 60 s particle run leaves at least 30 s of valid readings in clean air", "Engineering and technology", "Sensing resolution",
        law="SPS30 datasheet: up to 30 s to the first reading at low counts (CAL [A9])", value=60.0 - 30.0, limit=30.0, unit="s", rule="above", closed_by=CAL)
c.claim("S30", "The node with FieldNode's sun shield stays within 4.0 kg on the pole", "Engineering and technology", "Manufacturing tolerances",
        law="Part volumes from the model and densities (CAL [F5])", value=float(f"{S['m_sh']:.2f}"), limit=4.0, unit="kg", rule="below", closed_by=CAL)
c.cited("S31", "Stainless insect mesh under the pod keeps insects and spiders out of the sensors", "Biology", "Ecology and agronomy",
        law="Insect screens stop insects larger than the aperture; spiders and wasps nest in sheltered openings",
        detail="Mesh aperture to be chosen for the smallest local insects; nesting is checked at each pod exchange (TRL 4)", verdict=PLAUSIBLE)
c.cited("S34", "Twelve 10 s NO2 readings and twelve 60 s PM runs an hour represent the hourly mean", "Mathematics", "Statistics and uncertainty",
        law="Sampling a fluctuating signal: the error of the hourly mean falls with the number of independent samples; the cell's response (T90 under 80 s) smooths the NO2 signal",
        detail="Street NO2 changes over seconds near traffic; the sampling error is not in the budget and is measured in the TRL 4 collocation against the reference's continuous record", verdict=PLAUSIBLE)
c.cited("S35", "The printed and bolted parts survive years of wind vibration and occasional ice", "Physics", "Acoustics and vibration",
        law="Fatigue under vortex shedding and gusts; ice load on the shield and panel",
        detail="Stresses are low (S21, S22), but no fatigue or ice case is calculated; nyloc nuts and inserts resist loosening; checked at TRL 4 and by inspection at each pod exchange", verdict=PLAUSIBLE)
c.cited("S32", "FieldNode's core survives 50 degC ambient with its sun shield fitted above 45 degC", "Physics", "Heat transfer",
        law="FieldNode is rated to 45 degC ambient and runs 58.7 to 73.3 degC inside at 45 degC (FND-CAL-001); the sun shield is FieldNode's fix",
        detail="To confirm in FieldNode's calculation note; AirStreet relies on it at hot sites", verdict=PLAUSIBLE)

# ------------------------------------------------------------------ option B (first-order estimates, AST-OPT-001)
p_pump, p_heat, p_fan, p_sens = 1.0 * 0.2, 2.0 * 0.3, 0.25, 0.10          # W: pump 1 W at 20 %, heater 2 W 30 % of hours, fan, sensors
e_b = (p_pump + p_heat + p_fan + p_sens) * 24
c.balance("B1", "Option B: a 30 W panel charges more than the heated, pumped node uses in a winter day", "Engineering and technology", "Power and link budgets",
          inputs={"30 W panel x 2.0 peak sun hours x 0.75": 30 * 2.0 * 0.75}, outputs={"pump, heater, fan, sensors": round(e_b, 1)}, unit="Wh/day",
          law="Energy balance with estimated loads (pump 1 W at 20 %, heater 2 W for 30 % of hours, fan 0.25 W, sensors 0.1 W)")
q = 1e-3 / 60 * 1.2
c.claim("B2", "Option B: warming the 1 L/min sample by 5 K takes far less than the 2 W heater gives", "Physics", "Thermodynamics",
        law="P = m_dot cp dT; most of the heater power is lost through the sleeve", value=round(q * 1005 * 5, 2), limit=2.0, unit="W", rule="below")
rh_after = 90 * math.exp(17.62 * 20 / (243.12 + 20)) / math.exp(17.62 * 25 / (243.12 + 25))
c.claim("B3", "Option B: warming the sample 5 K brings 90 % RH below the SPS30's 80 % recommended limit", "Physics", "Thermodynamics",
        law="Magnus saturation vapour pressure at 20 and 25 degC", value=round(rh_after, 0), limit=80.0, unit="% RH", rule="below")
c.cited("B4", "Option B: the heated inlet does not change the particles it measures", "Chemistry", "Environmental and atmospheric chemistry",
        law="Semi-volatile ammonium nitrate evaporates when an inlet is heated (known loss in heated-inlet PM monitors)",
        detail="A few kelvin of warming loses part of the nitrate fraction; to quantify by collocation if B were chosen", verdict=PLAUSIBLE)

# ------------------------------------------------------------------ option C (first-order estimates, AST-OPT-001)
D_NO2, A_T, L_T = 0.154, math.pi * 0.55 ** 2, 7.1          # cm2/s (Palmes et al., 1976), cm2, cm
up = D_NO2 * A_T / L_T
m_ug = 30e-6 * up * 28 * 86400
c.order_of_magnitude("C1", "Option C: a Palmes tube collects about 1.5 ug of NO2 in 28 days at 30 ug/m3", "Chemistry", "Analytical",
                     claimed=1.5, estimate=m_ug, unit="ug", law="Fick's first law, uptake D A / L with D(NO2) 0.154 cm2/s, 11 mm bore, 71 mm long")
c.cited("C2", "Option C: triplicate tubes give monthly NO2 means within about 25 %", "Mathematics", "Statistics and uncertainty",
        law="Defra NO2 diffusion tube practical guidance: indicative technique, uncertainty about 25 %; bias adjusted by collocation with a chemiluminescence analyser",
        detail="Monthly means only; no hourly or daily data", verdict=WITHIN)
e_c = (0.275 * 60 / 900 + 0.002) * 24 * 30
c.balance("C3", "Option C: four alkaline D cells run the particle logger for a month between tube changes", "Chemistry", "Electrochemistry and batteries",
          inputs={"4 D cells, 6 V, 12 Ah, 70 % usable": 4 * 1.5 * 12 * 0.7}, outputs={"SPS30 60 s every 15 min and logger, 30 days": round(e_c, 1)}, unit="Wh",
          law="Energy balance; alkaline D capacity about 12 Ah at low drain (estimate)")

state = c.write()
print("stem_check:", state)

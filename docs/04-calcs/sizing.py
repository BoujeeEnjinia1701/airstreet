"""AirStreet sizing calculations, AST-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[A3] that the note cites, and the requirement table is written to docs/04-calcs/results.csv.
Geometry comes from cad/src/model.py (PARAMS, derived and the part solids), the parts cost from
bom/bom.csv and the budget from project.yaml. FieldNode figures come from FND-CAL-001 v0.1.
First-principles estimates for a paper proof of concept; not a substitute for tests.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, build_parts  # noqa: E402

D = derived(P)
OUT = {}


def tag(t, text):
    print(f"[{t}] {text}")


print("AirStreet sizing, AST-CAL-001 v0.1")

# ------------------------------------------------------------------ assumptions
# Sensors (SPS30 values from the Sensirion SPS30 datasheet, 07/2023; others assumed)
V5 = 5.0
I_SPS_TYP, I_SPS_MAX = 0.055, 0.065   # A in measurement mode (datasheet typ, max)
T_RUN, T_REC = 30.0, 300.0            # s PM run per record, s between records (DDR-001 D8)
I_AFE = 1.5e-3                        # A at 5 V, potentiostat and ADC held on continuously (assumed)
P_TH = 0.01e-3                        # W, SHT45 one reading per record (negligible, assumed)
MARGIN = 1.2                          # design margin on the port load
# FieldNode core (FND-CAL-001 v0.1): rails 90 %, core per-report energy parts, sleep, battery
ETA_RAIL = 0.90
V_CORE = 3.3
I_TX, I_RX, T_RXW, I_MCU, T_MCU = 0.045, 0.0046, 0.1, 0.008, 0.5
I_SLEEP = 33e-6
T_MCU_EXTRA = 1.0                     # s extra controller time per record to run and read the sensors (assumed)
E_USABLE = 6.0 * 3.2 * 0.8            # Wh, 6 Ah LiFePO4, 80 % usable
COLD, EOL = 4.03 / 5.75, 4.60 / 5.75  # capacity ratios at -20 degC and end of life, from FND-CAL-001
E_STORED_WORST, E_STORED_HOT = 7.75, 0.8   # Wh/day stored: worst month; hot clear day without shield
FND_ALLOW, FND_CEIL = 100.0, 115.0    # mW: FND design value (proposed) and 5-day ceiling
FND_MASS, FND_VBLOCK = 2.41, 0.20     # kg: FieldNode as built; V-blocks and small clamps not used here

# ------------------------------------------------------------------ A. Power and energy (R9)
duty = T_RUN / T_REC
p_pm = V5 * I_SPS_TYP * duty * 1e3
p_pm_max = V5 * I_SPS_MAX * duty * 1e3
p_afe = V5 * I_AFE * 1e3
p_port = p_pm + p_afe + P_TH * 1e3
p_design = (p_pm_max + p_afe + P_TH * 1e3) * MARGIN
tag("A1", f"PM sensor {V5 * I_SPS_TYP:.3f} W while running, {duty * 100:.0f} % duty: {p_pm:.1f} mW typical, {p_pm_max:.1f} mW at the datasheet maximum")
tag("A2", f"NO2 front end and ADC {p_afe:.1f} mW continuous; T and RH {P_TH * 1e3:.2f} mW; port load {p_port:.1f} mW typical")
tag("A3", f"Design port load (maximum SPS30 current, x{MARGIN}): {p_design:.1f} mW against {FND_ALLOW:.0f} mW (FND design value) and {FND_CEIL:.0f} mW (FND ceiling)")
recs = 86400 / T_REC
t_air = {}


def airtime(sf, payload=20, bw=125e3, cr=1, preamble=8, crc=1, header=1):
    """LoRa time on air (Semtech AN1200.13 formula) for a LoRaWAN uplink with 13 bytes of MAC overhead."""
    pl = payload + 13
    ts = (2 ** sf) / bw
    de = 1 if (sf >= 11 and bw == 125e3) else 0
    ih = 0 if header else 1
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16 * crc - 20 * ih) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (preamble + 4.25 + n) * ts


for sf in (7, 8, 9, 10, 11, 12):
    t_air[sf] = airtime(sf)
e_rep = V_CORE * (I_TX * t_air[9] + 2 * I_RX * T_RXW + I_MCU * T_MCU)          # J per uplink at SF9
e_core = (e_rep * recs + V_CORE * I_MCU * T_MCU_EXTRA * recs + V_CORE * I_SLEEP * 86400) / 3600  # Wh/day
e_day = p_design / 1e3 * 24 / ETA_RAIL + e_core
tag("A4", f"Core at a 5 min interval: {e_rep * 1e3:.1f} mJ per uplink at SF9, {e_core * 1e3:.1f} mWh/day with sensor wake-ups and sleep (FieldNode alone at 15 min: 4.0 mWh/day)")
tag("A5", f"Daily draw from the cell at the design load: {e_day:.2f} Wh/day ({e_day / 24 * 1e3:.1f} mW average)")
aut = E_USABLE / e_day
tag("A6", f"Autonomy without sun: {aut:.1f} days; {aut * COLD:.1f} days at -20 degC; {aut * EOL:.1f} days at end of cell life (R9 context; FND R6 asks 5 days)")
tag("A7", f"Worst month: {E_STORED_WORST:.2f} Wh stored against {e_day:.2f} Wh drawn, ratio {E_STORED_WORST / e_day:.1f}")
deficit = e_day - E_STORED_HOT
tag("A8", f"Hot clear day without the FieldNode sun shield: {E_STORED_HOT:.1f} Wh stored, deficit {deficit:.2f} Wh/day; a full cell covers {E_USABLE / deficit:.0f} such days in a row")
p_run60 = (V5 * I_SPS_MAX * 60 / T_REC * 1e3 + p_afe) * MARGIN
tag("A9", f"Option: 60 s PM run (for clean air, where the SPS30 needs up to 30 s to its first reading): design load {p_run60:.1f} mW")
OUT["R9"] = (f"Design load {p_design:.1f} mW at the ports; {e_day:.2f} Wh/day drawn against {E_STORED_WORST:.2f} Wh stored in the worst month; "
             f"{aut:.1f} days without sun", "115 mW or less; energy neutral at FieldNode design sun hours", "Met on paper")

# ------------------------------------------------------------------ B. Data, airtime, storage (R8, R10)
payload = 2 * 8 + 2 + 2
tag("B1", f"Record: PM1, PM2.5, PM10, WE, AE, T, RH, status (2 bytes each), counter 2 bytes, flags 2 bytes: {payload} bytes; {recs:.0f} records per day")
for sf in (7, 8, 9, 10, 12):
    tag("B2", f"SF{sf}: {t_air[sf] * 1e3:.0f} ms per uplink; {t_air[sf] * recs:.1f} s/day; {t_air[sf] / T_REC * 100:.3f} % of each 5 min")
tag("B3", f"EU868 1 % sub-band limit: met at every SF (worst SF12, {t_air[12] / T_REC * 100:.2f} %)")
tag("B4", f"The Things Network fair use (30 s/day): met only at SF7 ({t_air[7] * recs:.1f} s); SF8 {t_air[8] * recs:.1f} s, SF9 {t_air[9] * recs:.1f} s")
tag("B5", f"US915 400 ms dwell limit: SF9 {t_air[9] * 1e3:.0f} ms passes, SF10 {t_air[10] * 1e3:.0f} ms fails")
store = payload * recs * 7 / 1e3
tag("B6", f"7 days of store and forward: {store:.1f} kB against 16 MB FieldNode flash")
tag("B7", "Hourly mean ready when the last record of the hour arrives: within one record interval (5 min) plus server time")
OUT["R8"] = (f"5 min records; hourly mean within about 5 min; 7 days = {store:.1f} kB of 16 MB", "5 min; hourly within 15 min; 7 days", "Met on paper")
OUT["R10"] = (f"{t_air[9] / T_REC * 100:.3f} % at SF9, {t_air[12] / T_REC * 100:.2f} % at SF12", "Below 1 % per EU868 sub-band", "Met on paper")

# ------------------------------------------------------------------ C. NO2 error budget (R2, R3, R4)
UG = 46.0055 / 24.465                 # ug/m3 per ppb at 25 degC, 101.325 kPa
GAIN = 0.25                           # mV per ppb, sensor about 300 nA/ppm and 0.8 mV/nA front end (assumed)
LSB = 2048.0 / 32768                  # mV, ADS1115 at +/-2.048 V
tag("C1", f"1 ppb = {UG:.3f} ug/m3; ADC step {LSB * 1e3:.1f} uV = {LSB / GAIN:.2f} ppb at an assumed {GAIN} mV/ppb")
s_noise1 = 5.0                        # ppb 1-sigma per 1 s sample (assumed)
n_hour = 10 * 12                      # 10 samples per record, 12 records per hour
s_noise = s_noise1 / math.sqrt(n_hour)
s_cal = 3.5 / 0.798                   # ppb: MAE 3.5 ppb (Zimmerman et al., 2018) as a normal sigma
drift_rate, anchor = 0.5, 0.5         # ppb per month zero drift (assumed); anchor node removes half (assumed)
drift_res = drift_rate * 6 * (1 - anchor)
s_drift = drift_res / math.sqrt(3)    # uniform ramp over the 6-month collocation interval
s_transfer = 2.0                      # ppb bias moving from the reference site to a street (assumed)
s_hour = math.sqrt(s_noise ** 2 + s_cal ** 2 + s_drift ** 2 + s_transfer ** 2)
mae = 0.798 * s_hour
tag("C2", f"Hourly terms (1 sigma, ppb): noise {s_noise:.2f}, calibration residual {s_cal:.2f}, drift {s_drift:.2f}, transfer {s_transfer:.2f}; total {s_hour:.2f} ppb")
tag("C3", f"Hourly mean absolute error {mae:.1f} ppb ({mae * UG:.1f} ug/m3) against 5 ppb (R2)")
n_eff_col = 14 * 24 / 6               # effective independent hours in a 14-day collocation (6 h correlation, assumed)
s_int = s_cal / math.sqrt(n_eff_col)
s_rand_yr = s_cal / math.sqrt(8760 / 6)
s_year = math.sqrt(s_transfer ** 2 + s_drift ** 2 + s_int ** 2 + s_rand_yr ** 2)
tag("C4", f"Annual mean (1 sigma): transfer {s_transfer:.2f}, drift {s_drift:.2f}, intercept {s_int:.2f}, random {s_rand_yr:.2f}; total {s_year:.2f} ppb = {s_year * UG:.2f} ug/m3 against 2 ug/m3 (R3)")
band = 1.2816 * s_year * UG
tag("C5", f"90 % one-sided classification against 40 ug/m3: decisive below {40 - band:.1f} or above {40 + band:.1f} ug/m3; streets in between cannot be classified (R4)")
tag("C6", f"Transfer bias needed for R3 at 2 ug/m3 with the other terms unchanged: {math.sqrt(max((2 / UG) ** 2 - s_drift ** 2 - s_int ** 2 - s_rand_yr ** 2, 0)):.2f} ppb")
OUT["R2"] = (f"Hourly MAE about {mae:.1f} ppb (budget of assumed terms)", "5 ppb or less hourly MAE, 0 to 200 ppb", "At risk")
OUT["R3"] = (f"Annual uncertainty {s_year * UG:.1f} ug/m3 (1 sigma)", "2 ug/m3 or less at 10 ug/m3", "Not met")
OUT["R4"] = (f"Decisive outside {40 - band:.1f} to {40 + band:.1f} ug/m3", "Classify vs 40 ug/m3 with 90 % confidence", "At risk")

# ------------------------------------------------------------------ D. Radiation shield (R5)
G, ALB, ALPHA = 1000.0, 0.2, 0.25     # W/m2 global, ground albedo, absorptance of aged white ASA (assumed)
H_PLATE = 15.0                        # W/m2K per face, convection and sky radiation at 1 m/s (assumed)
so, si, stk, pitch, nplates = P["shield"]
a_cap = math.pi * (P["cap"][0] / 2e3) ** 2
a_ring = math.pi * ((so / 2e3) ** 2 - (si / 2e3) ** 2)
dT_cap = ALPHA * G * a_cap / (H_PLATE * 2 * a_cap)
dT_bot = ALPHA * G * ALB * a_ring / (H_PLATE * 2 * a_ring)
dT_mid = 0.5
F_cap, F_bot, F_mid = 0.10, 0.10, 0.60   # view factors from the probe (assumed); rest is open gaps at ambient
dT_rad = F_cap * dT_cap + F_bot * dT_bot + F_mid * dT_mid
eps, sig, Tk = 0.9, 5.67e-8, 308.0
h_r = 4 * eps * sig * Tk ** 3
d_probe, k_air, nu, pr = 0.006, 0.0265, 1.6e-5, 0.71
gap_area = (nplates - 1) * (pitch - stk) / 1e3 * math.pi * so / 1e3
shield_res = {}
for frac in (0.3, 0.1):
    v = 1.0 * frac
    re = v * d_probe / nu
    nuss = 0.683 * re ** 0.466 * pr ** (1 / 3)
    h_c = nuss * k_air / d_probe
    e_rad = h_r / (h_r + h_c) * dT_rad
    flow = 1.2 * 1005 * gap_area * v
    e_air = (ALPHA * G * a_cap / 2 + 0.3) / flow
    shield_res[frac] = (h_c, e_rad, e_air, e_rad + e_air)
    tag("D1", f"Inner air speed {frac * 100:.0f} % of 1 m/s wind: probe h {h_c:.0f} W/m2K, radiant error {e_rad:.2f} K, air heating {e_air:.2f} K, total {e_rad + e_air:.2f} K")
tag("D2", f"Cap {dT_cap:.1f} K and bottom plate {dT_bot:.1f} K above ambient in 1000 W/m2 sun; mean radiant excess seen by the probe {dT_rad:.2f} K")
err_hi = shield_res[0.1][3]


def rh_after_warming(rh, t, dt):
    es = lambda tc: 6.112 * math.exp(17.62 * tc / (243.12 + tc))
    return rh * es(t) / es(t + dt)


for rh in (50, 85):
    tag("D3", f"At 30 degC and {rh} % RH, a {err_hi:.2f} K warm error reads {rh - rh_after_warming(rh, 30, err_hi):.1f} % RH low")
drh_shield = 85 - rh_after_warming(85, 30, err_hi)
OUT["R5"] = (f"SHT45 +/-0.1 degC, +/-1 % RH typical; shield error {shield_res[0.3][3]:.2f} to {err_hi:.2f} K at 1 m/s", "+/-0.5 degC, +/-3 % RH; radiation error 1 degC or less", "At risk")

# ------------------------------------------------------------------ E. PM2.5 error with humidity (R1), using the RH error from D
KAPPA, D_KAPPA = 0.3, 0.1             # hygroscopicity of urban aerosol and its uncertainty (assumed)
d_rh = math.sqrt(1.0 ** 2 + drh_shield ** 2)
tag("E1", f"RH uncertainty used: {d_rh:.1f} % (SHT45 1 % typical and the shield warm error at 85 % RH)")
pm_rows = []
for rh in (50, 70, 80, 85, 90):
    aw = rh / 100
    g = 1 + KAPPA * aw / (1 - aw)
    e_k = D_KAPPA * aw / (1 - aw) / g
    e_rh = KAPPA * (d_rh / 100) / (1 - aw) ** 2 / g
    for c in (10.0, 25.0, 50.0):
        base = math.hypot(2.0, 0.05 * c)          # after the CalRig transfer check (assumed 2 ug/m3 + 5 %)
        err = math.sqrt(base ** 2 + (c * e_k) ** 2 + (c * e_rh) ** 2)
        lim = max(5.0, 0.3 * c)
        pm_rows.append((rh, c, err, lim))
        tag("E2", f"RH {rh} %, PM2.5 {c:.0f} ug/m3: growth x{g:.2f}, error {err:.1f} ug/m3 against {lim:.1f} ({'within' if err <= lim else 'outside'})")
ok_rh = max(r for r in (50, 70, 80, 85, 90) if all(e <= l for rr, c, e, l in pm_rows if rr == r))
tag("E3", f"R1 met on paper up to {ok_rh} % RH at every tested level; the SPS30 datasheet recommends 20 to 80 % RH")
OUT["R1"] = (f"Within the bound up to {ok_rh} % RH on paper; outside it above that", "+/-5 ug/m3 or +/-30 % hourly after humidity correction", "At risk")

# ------------------------------------------------------------------ F. Geometry, area, mass (R11, R13)
parts = build_parts(P)
tag("F1", f"Inlet plane {P['inlet_z']:.0f} mm above the sidewalk (EU range 1500 to 4000); pole range {P['pole_range'][0]:.0f} to {P['pole_range'][1]:.0f} mm by band clamps; no drilling")
tag("F2", f"Whip clearance to the pod lid {D['whip_clear']:.0f} mm; clamp span {D['clamp_span']:.0f} mm; node height {D['overall_h']:.0f} mm; front of node {D['offset_front']:.0f} mm from the pole face")


def silhouette(shapes, axis, px=2.0):
    """Projected area (m2) of the solids seen along an axis, by rasterizing their triangles."""
    tri2 = []
    for s in shapes:
        v, t = s.tessellate(0.5)
        a = np.array([[p.X, p.Y, p.Z] for p in v])
        uv = a[:, [0, 2]] if axis == "y" else a[:, [1, 2]]
        tri2.append(uv[np.array(t)])
    tri2 = np.concatenate(tri2)
    lo = tri2.reshape(-1, 2).min(0)
    hi = tri2.reshape(-1, 2).max(0)
    nx, ny = (np.ceil((hi - lo) / px).astype(int) + 1)
    grid = np.zeros((nx, ny), bool)
    for tr in tri2:
        mn = np.floor((tr.min(0) - lo) / px).astype(int)
        mx = np.ceil((tr.max(0) - lo) / px).astype(int)
        xs = lo[0] + (np.arange(mn[0], mx[0] + 1) + 0.5) * px
        ys = lo[1] + (np.arange(mn[1], mx[1] + 1) + 0.5) * px
        X, Y = np.meshgrid(xs, ys, indexing="ij")
        (x0, y0), (x1, y1), (x2, y2) = tr
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-9:
            continue
        l1 = ((y1 - y2) * (X - x2) + (x2 - x1) * (Y - y2)) / den
        l2 = ((y2 - y0) * (X - x2) + (x0 - x2) * (Y - y2)) / den
        inside = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
        grid[mn[0]:mx[0] + 1, mn[1]:mx[1] + 1] |= inside
    return grid.sum() * px * px / 1e6


node = list(parts.values())
a_front = silhouette(node, "y")
a_side = silhouette(node, "x")
tag("F3", f"Projected area from the model: {a_front:.3f} m2 seen from the street, {a_side:.3f} m2 seen along the street (R13 limit 0.12 m2)")
RHO = {"asa": 1.07e-6, "al": 2.70e-6, "ss": 7.90e-6}   # kg/mm3
W, Dp, H = P["pod"]
pod_m = parts["pod"].volume * RHO["asa"]
plates_vol = nplates * math.pi * ((so / 2) ** 2 - (si / 2) ** 2) * stk + math.pi * (P["cap"][0] / 2) ** 2 * P["cap"][1]
rods_vol = 3 * math.pi * (P["rod_d"] / 2) ** 2 * (P["arm_z"] - D["sh_bot"] + 3)
shield_m = plates_vol * RHO["asa"] + rods_vol * RHO["ss"]
rail_m = P["rail"][0] * P["rail"][1] * D["rail_len"] * RHO["al"]
arm_m = (P["shield_x"] + so * 0.2 - 15) * P["arm"][0] * P["arm"][1] * RHO["al"] + 10 * P["arm"][1] * 60 * RHO["al"]
saddle_m = 2 * 0.030                  # printed ASA V-saddles (from the model envelope, rounded)
clamp_m = 2 * 0.065                   # 12.7 mm stainless worm-drive clamps for up to 200 mm (assumed)
bought = {"SPS30": 0.0263, "NO2 sensor": 0.015, "front end and ADC": 0.025, "T and RH probe": 0.010,
          "cables and plugs": 2 * 0.040 + 0.020, "fasteners, mesh, desiccant": 0.050}
fnd_m = FND_MASS - FND_VBLOCK
mass = {"FieldNode core as used": fnd_m, "rail": rail_m, "shield arm": arm_m, "saddles": saddle_m, "band clamps": clamp_m,
        "sensor pod": pod_m, "radiation shield": shield_m, "bought sensor-head parts": sum(bought.values())}
m_tot = sum(mass.values())
tag("F4", "Mass: " + "; ".join(f"{k} {v:.2f} kg" for k, v in mass.items()))
tag("F5", f"Total on the pole {m_tot:.2f} kg against 3.5 kg (R13); sensor head and mount alone {m_tot - fnd_m:.2f} kg")
plate_m = P["plate"][0] * P["plate"][1] * P["plate"][2] * RHO["al"]
tag("F6", f"Option: fix the FieldNode enclosure and bracket straight to the AirStreet rail and leave off its back plate ({plate_m:.2f} kg): {m_tot - plate_m:.2f} kg")
OUT["R11"] = (f"80 to 200 mm poles, band clamps; inlet {P['inlet_z'] / 1e3:.1f} m", "80 to 200 mm, no drilling, inlets 1.5 to 4 m", "Met by design")
OUT["R13"] = (f"{m_tot:.2f} kg; {a_front:.3f} m2 frontal", "3.5 kg or less; 0.12 m2 or less", "Not met" if m_tot > 3.5 else "Met on paper")

# ------------------------------------------------------------------ G. Wind and mounting
V_W, RHO_AIR, CD = 35.0, 1.225, 1.2
q = 0.5 * RHO_AIR * V_W ** 2
f_wind = q * CD * max(a_front, a_side)
z_c = (D["overall_h"] / 2 + P["rail_z"][0]) / 1e3
tag("G1", f"35 m/s gust: q {q:.0f} Pa; wind force {f_wind:.0f} N at about {z_c:.2f} m; moment at the pole base {f_wind * z_c:.0f} N m (pole check is the owner's)")
T_BAND, MU = 1000.0, 0.3              # N preload per band (as FND-CAL-001), friction on painted steel (assumed)
slip_cap = 2 * MU * math.pi * T_BAND
f_down = m_tot * 9.81 + q * CD * P["panel"][0] * P["panel"][1] / 1e6 * math.cos(math.radians(P["tilt"]))
tag("G2", f"Slip: downward load {f_down:.0f} N (weight and wind on the tilted panel) against {slip_cap:.0f} N friction; factor {slip_cap / f_down:.0f}")
a_sh = so / 1e3 * (nplates * pitch + P["cap"][1]) / 1e3
f_sh = q * CD * a_sh
lever = (P["shield_x"] + so * 0.2 - 15) / 1e3
m_arm = f_sh * lever
z_arm = P["arm"][1] * P["arm"][0] ** 2 / 6
tag("G3", f"Shield arm: {f_sh:.1f} N on the shield, {m_arm:.2f} N m at the rail, stress {m_arm * 1e3 / z_arm:.1f} MPa in the 20 x 8 mm bar (6063 yield about 170 MPa)")
t_twist = f_sh * P["shield_x"] / 1e3
t_cap = slip_cap * D["R"] / 1e3
tag("G4", f"Twist about the pole: {t_twist:.2f} N m against {t_cap:.0f} N m friction")
f_low = q * CD * (W * H + a_sh * 1e6) / 1e6
m_rail = f_low * (P["clamp_z"][0] - (P["inlet_z"] + H / 2)) / 1e3
z_rail = P["rail"][0] * P["rail"][1] ** 2 / 6
tag("G5", f"Rail below the lower clamp: {f_low:.1f} N on pod and shield, {m_rail:.2f} N m, stress {m_rail * 1e3 / z_rail:.1f} MPa in the 40 x 5 mm bar")

# ------------------------------------------------------------------ H. Service and environment (R12, R16)
steps = {"place and secure ladder or platform": 5, "open drip lid (4 screws)": 1.5, "swap SPS30 (plug-in lead)": 2,
         "swap NO2 sensor on its socket": 2, "close lid, check seals": 1.5, "confirm an uplink": 2}
t_serv = sum(steps.values())
tag("H1", "Service steps (min): " + "; ".join(f"{k} {v:g}" for k, v in steps.items()) + f"; total {t_serv:.0f} min against 15 min")
tag("H2", "A new NO2 sensor has no field calibration until it has been collocated; a pre-collocated spare pod avoids this")
tag("H3", "FieldNode is rated for -20 to +45 degC ambient (FND-REQ-001 R2) and reaches 58.7 to 73.3 degC inside at 45 degC; AirStreet R12 asks -10 to 50 degC")
tag("H4", "SPS30 datasheet: recommended 10 to 40 degC and 20 to 80 % RH; absolute -10 to 60 degC and 0 to 95 % RH")
OUT["R12"] = ("FieldNode rated to 45 degC ambient; SPS30 recommended range 20 to 80 % RH; condensation and insects unverified",
              "Outdoors, -10 to 50 degC; mesh, drip lid, IP65 core", "At risk")
OUT["R16"] = (f"About {t_serv:.0f} min estimated; recollocation needed after an NO2 swap", "15 min at the pole with hand tools", "At risk")

# ------------------------------------------------------------------ I. Cost (R15)
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
fnd_cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].startswith(("1 ", "2 ")))
head = tot - fnd_cost
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
PROPOSED = 280.0
tag("I1", f"BOM {len(rows)} lines, all priced: ${tot:.2f} per node; FieldNode core ${fnd_cost:.2f} (costed in FND); sensor head ${head:.2f}")
tag("I2", f"Sensor head against budget_usd ${budget:.0f}: over by ${head - budget:.2f}; against the proposed ${PROPOSED:.0f} (awaiting Amish): {'over' if head > PROPOSED else 'under'} by ${abs(head - PROPOSED):.2f}")
tag("I3", "Replacement NO2 sensor about every 2 years (estimate) and collocation time are running costs, not in the BOM")
OUT["R15"] = (f"Sensor head ${head:.2f}; ${tot:.2f} with the FieldNode core", f"Sensor head ${budget:.0f} or less (budget_usd); ${PROPOSED:.0f} proposed", "Not met")

# ------------------------------------------------------------------ by design
OUT["R6"] = ("CalRig for T, RH and PM; 14-day NO2 collocation and every 6 months (DDR-001 D3)", "Stated method per node", "Met by design")
OUT["R7"] = ("Raw WE, AE, PM, T, RH and a calibration version tag", "Raw signals kept", "Met by design")
OUT["R14"] = ("Levels, T and RH only", "No images, audio or identifiers", "Met by design")

order = [f"R{i}" for i in range(1, 17)]
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    for k in order:
        w.writerow([k, *OUT[k]])
counts = {}
for k in order:
    counts[OUT[k][2]] = counts.get(OUT[k][2], 0) + 1
tag("J1", "Status counts: " + "; ".join(f"{k} {v}" for k, v in sorted(counts.items())))
tag("J2", "Not met: " + ", ".join(k for k in order if OUT[k][2] == "Not met"))

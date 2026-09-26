"""AirStreet concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Street light pole axis at X = 0, Y = 0; sidewalk surface at Z = 0.
The kerb runs along X at Y = -900 and the carriageway is at Y < -900. The node hangs on the
street side (-Y) of the pole with the sensor inlets about 3.0 m above the sidewalk (proposed).
Grey parts (pole, sidewalk, road, person) are context for scale only and carry no BOM number.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all, human_figure

POLE_R = 70.0          # street light pole radius at node height (140 mm diameter)
FACE_Y = -POLE_R       # pole face on the street side
RAIL_Y = FACE_Y - 8.0  # mounting rail centre line (6 mm flat bar)

# 3 Pole mounting: two stainless band clamps and a vertical rail (FieldNode rail, longer version)
def band(z):
    return Pos(0, 0, z) * (Cylinder(POLE_R + 3, 20) - Cylinder(POLE_R, 22))

rail = Pos(0, RAIL_Y, 3120) * Box(50, 6, 520)
clamps = band(2920) + band(3320) + rail

# 1 FieldNode core: IP65 enclosure (about 200 x 150 x 100 mm, estimate) on the rail
ENC_W, ENC_D, ENC_H = 200.0, 100.0, 150.0
ENC_Y = RAIL_Y - 3 - ENC_D / 2
ENC_Z = 3230.0
enclosure = Pos(0, ENC_Y, ENC_Z) * Box(ENC_W, ENC_D, ENC_H)
gland = Pos(0, ENC_Y, ENC_Z - ENC_H / 2 - 8) * Cylinder(9, 16)
fieldnode = enclosure + gland

# 2 FieldNode 6 W panel, tilted toward the street side, doubling as a sun and rain hood
panel = Pos(0, ENC_Y - 20, ENC_Z + ENC_H / 2 + 60) * Rot(30, 0, 0) * Box(260, 220, 18)
panel_posts = (Pos(-90, ENC_Y + 20, ENC_Z + ENC_H / 2 + 30) * Box(12, 12, 60)
               + Pos(90, ENC_Y + 20, ENC_Z + ENC_H / 2 + 30) * Box(12, 12, 60))
panel_set = panel + panel_posts

# 4 Sensor pod: printed ASA shell, open underneath behind insect mesh, below the enclosure
POD_W, POD_D, POD_H, WALL = 170.0, 110.0, 95.0, 3.0
POD_Y = RAIL_Y - 3 - POD_D / 2
POD_Z = 3010.0
pod_bot = POD_Z - POD_H / 2
shell = Box(POD_W, POD_D, POD_H) - Pos(0, 0, -WALL) * Box(POD_W - 2 * WALL, POD_D - 2 * WALL, POD_H)
inlet_slots = None
for dx in (-45, 45):
    s = Pos(dx, 0, -POD_H / 2 + WALL / 2) * Box(50, 60, WALL + 2)
    inlet_slots = s if inlet_slots is None else inlet_slots + s
floor = Pos(0, 0, -POD_H / 2 + WALL / 2) * Box(POD_W, POD_D, WALL) - inlet_slots
mesh = Pos(0, 0, -POD_H / 2 - 1) * Box(POD_W - 10, POD_D - 10, 1.0)
drip = Pos(0, 0, POD_H / 2 + 4) * Box(POD_W + 30, POD_D + 30, 8)   # overhanging lid
pod = Pos(0, POD_Y, POD_Z) * (shell + floor + mesh + drip)

# 5 Optical PM sensor (Sensirion SPS30 class, about 41 x 41 x 12 mm), inlet facing down
sps30 = Pos(-45, POD_Y + 20, pod_bot + WALL + 26) * Box(41, 12, 41)
sps_inlet = Pos(-45, POD_Y + 20, pod_bot + WALL + 3) * Box(14, 10, 6)
pm = sps30 + sps_inlet

# 6 Electrochemical NO2 sensor (Alphasense B4 class, 32 mm diameter), face down over the slot
no2 = Pos(45, POD_Y + 20, pod_bot + WALL + 12) * Cylinder(16, 20)

# 7 NO2 analog front end and 16-bit ADC board, standing at the back of the pod
afe = Pos(0, POD_Y + POD_D / 2 - WALL - 5, POD_Z + 8) * Box(120, 3, 55)
afe_parts = Pos(0, POD_Y + POD_D / 2 - WALL - 10, POD_Z + 8) * Box(60, 7, 25)
afe = afe + afe_parts

# 8 Multi-plate radiation shield beside the pod, on an arm from the rail
SH_X, SH_Y, SH_Z = 205.0, POD_Y, 3000.0
plates = None
for k in range(8):
    pl = Pos(SH_X, SH_Y, SH_Z - 50 + k * 13) * (Cylinder(60, 3) - Cylinder(28, 4))
    plates = pl if plates is None else plates + pl
cap = Pos(SH_X, SH_Y, SH_Z - 50 + 8 * 13) * Cylinder(62, 4)
rods = None
for dx, dy in ((40, 0), (-20, 35), (-20, -35)):
    r = Pos(SH_X + dx, SH_Y + dy, SH_Z + 3) * Cylinder(3, 112)
    rods = r if rods is None else rods + r
arm = Pos((SH_X + POD_W / 2) / 2 + 10, RAIL_Y - 3 - 10, SH_Z + 58) * Box(SH_X - POD_W / 2 + 40, 20, 8)
shield = plates + cap + rods + arm

# 9 Temperature and humidity sensor (Sensirion SHT45 class) on a probe in the shield centre
th = Pos(SH_X, SH_Y + 12, SH_Z - 5) * Box(14, 10, 4) + Pos(SH_X, SH_Y + 12, SH_Z + 25) * Cylinder(3, 56)

# 10 Sensor cables with M12 plugs into the FieldNode ports
cable = (Pos(20, POD_Y, POD_Z + POD_H / 2 + 8 + (ENC_Z - ENC_H / 2 - 16 - POD_Z - POD_H / 2 - 8) / 2)
         * Cylinder(5, ENC_Z - ENC_H / 2 - 16 - POD_Z - POD_H / 2 - 8)
         + Pos(20, POD_Y, ENC_Z - ENC_H / 2 - 14) * Cylinder(9, 14))
cable2 = Pos(SH_X, SH_Y, 3112) * Cylinder(4, 104) + Pos(152, SH_Y, 3164) * Box(122, 8, 8)
cables = cable + cable2

parts = [
    Part("FieldNode core (enclosure, cell, radio)", fieldnode, "#475569", 1, (0, -60, 260)),
    Part("FieldNode 6 W panel hood", panel_set, "#1E3A8A", 2, (0, -140, 480)),
    Part("Band clamps and mounting rail", clamps, "#94A3B8", 3, (0, 260, 0)),
    Part("Sensor pod with mesh and drip lid", pod, "#E5E7EB", 4, (0, -120, -160)),
    Part("Optical PM sensor (SPS30 class)", pm, "#0F766E", 5, (-70, -120, -420)),
    Part("Electrochemical NO2 sensor (B4 class)", no2, "#C2410C", 6, (70, -120, -420)),
    Part("NO2 front end and 16-bit ADC", afe, "#16A34A", 7, (0, 60, 160)),
    Part("Multi-plate radiation shield", shield, "#F8FAFC", 8, (220, -60, 60)),
    Part("Temperature and humidity sensor", th, "#7C3AED", 9, (220, -60, -170)),
    Part("Sensor cables, M12", cables, "#111827", 10, (-300, -60, 60)),
]

# Street context for the hero render (grey, not in the BOM)
pole = Pos(0, 0, 2100) * Cylinder(POLE_R, 4200) + Pos(0, 0, 60) * Cylinder(POLE_R + 30, 120)
lamp_arm = Pos(0, -450, 4150) * Box(40, 900, 40) + Pos(0, -850, 4110) * Box(160, 320, 60)
sidewalk = Pos(300, 0, -75) * Box(3200, 1800, 150)
kerb = Pos(300, -900, -60) * Box(3200, 150, 180)
road = Pos(300, -1700, -160) * Box(3200, 1500, 20)
person = human_figure(1750.0, x=750.0, y=-350.0, z=0.0)
context = [
    Part("Street light pole", pole + lamp_arm, "#9CA3AF"),
    Part("Sidewalk and kerb", sidewalk + kerb, "#D1D5DB"),
    Part("Carriageway", road, "#6B7280"),
    person,
]

# The kit's cutaway cutter is centred on Z = 0, so shift the whole scene down by the node
# height; the node then sits near Z = 0 and the sidewalk at Z = -3000. Relative geometry is unchanged.
SHIFT = Pos(0, 0, -3000)
parts = [Part(p.name, SHIFT * p.shape, p.color, p.bom, p.explode, p.alpha) for p in parts]
context = [Part(p.name, SHIFT * p.shape, p.color, p.bom, p.explode, p.alpha) for p in context]

render_all(
    parts, project="AirStreet", title="Street air quality node concept", dwg_no="AST-DWG-010",
    key_figures=["PM2.5 (optical) and NO2 (electrochemical) with T and RH",
                 "Inlets about 3.0 m above the sidewalk (proposed)",
                 "PM, T, RH checked on CalRig; NO2 by field collocation",
                 "Sensors about 45 mW average; 5 min reports (estimate)",
                 "About 3.0 kg with FieldNode core (estimate)",
                 "About $391 in parts with FieldNode core (indicative)"],
    scale_figure=False, context=context, cut_exclude=("FieldNode core (enclosure, cell, radio)", "FieldNode 6 W panel hood",
                                                   "Band clamps and mounting rail", "Sensor cables, M12"),
    flow={"title": "measurement and data flow (estimates)", "unit": "",
          "stages": [("Street air", "PM, NO2, heat, damp"),
                     ("Pod and shield", "PM 30 s per 5 min"),
                     ("FieldNode core", "raw WE, AE, PM, T, RH"),
                     ("LoRaWAN uplink", "about 20 B per 5 min"),
                     ("Calibration model", "CalRig + collocation"),
                     ("Street map", "hourly PM2.5, NO2")]},
)

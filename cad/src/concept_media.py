"""AirStreet concept media (TRL 3), built from the kit 1.9 D3 model in cad/src/model.py: components(CHOSEN),
every part of option A with its fasteners, grouped by BOM line for the exploded view and the callouts
(constructable design, AST-DDR-003, with the A1 lightening steps and the fixes of AST-DDR-005).

Run from the repo root:  python cad/src/concept_media.py         (every picture and the web model)
                         python cad/src/concept_media.py --web   (only media/model.glb and media/viewer.html)
Main dimensions and interfaces only; not for fabrication.

Coordinates in mm. Street light pole axis at X = 0, Y = 0; sidewalk surface at Z = 0. The kerb
runs along X at Y = -900 and the carriageway is at Y < -900. The node hangs on the street side
(-Y) of the pole with the inlet plane 3.0 m above the sidewalk (AST-DDR-001 D7). Grey parts (pole,
lamp arm, sidewalk, road, person) are context for scale only and carry no BOM number.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Compound, Cylinder, Pos  # noqa: E402
from concept import Part, render_all, human_figure, export_web_model  # noqa: E402
from model import PARAMS as P, BOM, CHOSEN, components  # noqa: E402
import concept as _concept  # noqa: E402


def _safe_project_views(part, workdir, line_weight=0.35, center_lines=True):
    """Kit bug workaround: drawing.project_views stops on a full-circle ellipse edge (start == end) in the
    hidden-line projection of the D3 model; here such an edge is skipped. Centre lines are left out."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box(); c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p)); out[name] = p
    return out


import drawing as _drawing  # noqa: E402
_drawing.project_views = _safe_project_views


def _key(q):
    """BOM group of a D3 part, for the exploded view and the callouts."""
    g, n = q["group"], q.get("bom")
    if g == "panel":
        return "panel"
    if g in ("fieldnode", "internal"):
        return "fieldnode"
    if g in ("mount", "cables", "hood"):
        return g
    if n in (5, 6, 7, 9):
        return {5: "pm", 6: "no2", 7: "afe", 9: "th"}[n]
    return "pod" if g == "pod" else "shield"


_groups = {}
for q in components(CHOSEN):
    if q["kind"] != "context":
        _groups.setdefault(_key(q), []).append(q["shape"])
shapes = {k: Compound(children=v) for k, v in _groups.items()}
style = {  # key: (color, exploded-view offset in mm)
    "fieldnode": ("#475569", (0, -60, 300)),
    "panel": ("#1E3A8A", (0, -160, 520)),
    "mount": ("#94A3B8", (0, 280, 0)),
    "pod": ("#E5E7EB", (0, -140, -200)),
    "pm": ("#0F766E", (-260, -200, -380)),
    "no2": ("#C2410C", (230, -200, -380)),
    "afe": ("#16A34A", (0, 80, 180)),
    "shield": ("#F8FAFC", (260, -60, 60)),
    "th": ("#7C3AED", (420, -60, -300)),
    "cables": ("#111827", (-340, -60, 120)),
    "hood": ("#0D9488", (160, -200, -330)),
}
parts = [Part(BOM[k][1], shapes[k], style[k][0], BOM[k][0], style[k][1]) for k in style]

# Street context for the hero render (grey, not in the BOM)
R = P["pole_od"] / 2
pole = Pos(0, 0, 2100) * Cylinder(R, 4200) + Pos(0, 0, 60) * Cylinder(R + 30, 120)
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

if "--web" in sys.argv:
    export_web_model(parts, "media", title="AirStreet: Street air quality node concept")
    print("wrote media/model.glb and media/viewer.html")
    sys.exit(0)

# The kit's cutaway cutter is centred on Z = 0, so shift the whole scene down by the inlet height;
# the node then sits near Z = 0 and the sidewalk at Z = -3000. Relative geometry is unchanged.
SHIFT = Pos(0, 0, -P["inlet_z"])
parts = [Part(p.name, SHIFT * p.shape, p.color, p.bom, p.explode, p.alpha) for p in parts]
context = [Part(p.name, SHIFT * p.shape, p.color, p.bom, p.explode, p.alpha) for p in context]

render_all(
    parts, project="AirStreet", title="Street air quality node concept", dwg_no="AST-DWG-010",
    date="2026-10-30",
    key_figures=["PM2.5 (SPS30) and NO2 (B43F class), shielded T and RH",
                 "Inlets 3.0 m above the sidewalk; poles 80 to 200 mm",
                 "PM, T, RH checked on CalRig; NO2 by field collocation",
                 "87 mW design sensor load; 5 min records (15 min on TTN)",
                 "3.69 kg (3.85 kg with sun shield) and 0.143 m² on the pole",
                 "Sensor head $305.50; $436.50 with FieldNode core"],
    scale_figure=False, context=context,
    cut_exclude=(BOM["fieldnode"][1], BOM["panel"][1], BOM["mount"][1], BOM["cables"][1]),
    flow={"title": "measurement and data flow (AST-CAL-001)", "unit": "",
          "stages": [("Street air", "PM, NO2, heat, damp"),
                     ("Pod and shield", "PM 60 s per 5 min"),
                     ("FieldNode core", "raw WE, AE, PM, T, RH"),
                     ("LoRaWAN uplink", "20 B, 0.25 s at SF9"),
                     ("Calibration model", "CalRig + collocation"),
                     ("Street map", "hourly PM2.5, NO2")]},
)

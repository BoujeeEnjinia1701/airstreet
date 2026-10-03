"""AirStreet product appearance model (build123d), TRL 3, constructable design.

Finished-product look for photoreal renders, built from the constructable model (cad/src/model.py,
AST-DDR-003, with the lightening steps of A1 accepted on 2026-10-02): the FieldNode core (enclosure,
lid, lugs, glands, M12 ports, vent, antenna, internal plate, cell and modules, panel bracket and
6 W panel, all from FieldNode's own model as vendored in cad/src/fieldnode_core.py); the mount
(two printed V-saddles, 40 x 4 mm rail, stainless bands, two windowed adapter plates and the angle
cross arm); the two-part sensor pod (shell with drip lid, sensor floor, mesh, glands and probe
socket) with the PM sensor, NO2 sensor, front end and terminal block inside; the eight-plate
radiation shield (1.5 mm plates, spacers, rods, cap) with the T and RH probe on its tube; and the
sensor cables and probe lead. Context is a short section of a 140 mm street light pole.

Every part's shape is taken from build_components() in model.py, so every dimension and position
matches the model, the drawings and the build plan. Appearance-only additions, recorded in
docs/REVIEW.md as proposed, awaiting Amish: a printed label and a lit green status light on the
FieldNode lid, and a printed label strip on the pod's street face. FieldNode's hot-site sun shield
is left off (it is fitted only at sites above 45 degC).
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import Align, Plane, Pos, Sphere, Text, extrude  # noqa: E402
from model import PARAMS, derived, build_components, pole_stub, bx, ycyl  # noqa: E402

_FONT = Path(__file__).resolve().parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf"

TITLE = "AirStreet: street-level air quality node for PM2.5 and NO2"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 20, "az": -56,
     "note": "Product render from the front right and above (about 20 deg elevation), on a short section of "
             "street light pole: solar panel over the FieldNode core, sensor pod hanging from the cross arm at "
             "left, radiation shield at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded view from the front right and above (about 26 deg elevation): solar panel and bracket, "
             "FieldNode enclosure, lid and internal plate; rail, V-saddles, bands, adapter plates and cross arm; "
             "sensor pod shell, front end, sensor floor with the PM and NO2 sensors, and mesh; radiation shield, "
             "cap and probe"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 12, "az": -64,
     "note": "Detail from the front right, slightly above (about 12 deg elevation), without the pole: sensor pod "
             "on the cross arm with its drip lid and roof glands, radiation shield and probe tube at right, green "
             "status light lit"},
]

POLE_Z = (2900.0, 3740.0)   # context pole section, just enough to carry the node

# Colours (restrained product palette, shared with the other FieldNode renders; kit accent)
C_SHELL = "#DADDE1"      # light grey polycarbonate enclosure
C_LID = "#E6E8EB"
C_POD = "#ECECEA"        # printed ASA, off-white
C_FLOOR = "#D9D9D6"
C_PLATE = "#F2F2EF"      # shield plates, white ASA
C_SADDLE = "#2B2F36"     # printed ASA, dark
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_ALU = "#C3C8CE"
C_ALU2 = "#AEB4BB"
C_STEEL = "#9CA3AB"
C_CELLS = "#1B2735"
C_PCB = "#166534"
C_CELL = "#2F4F6F"
C_LABEL = "#F4F4F2"
C_LED_G = "#22C55E"
C_SPS = "#B9BFC6"        # SPS30 metal shell
C_POLE = "#A7ADB4"

# Explode offsets (mm) by subsystem
E_BODY, E_LID, E_INT = (0, -170, 40), (0, -420, 40), (0, -300, 110)
E_PAN, E_BRK = (0, -170, 300), (0, -110, 170)
E_SAD, E_BAND, E_RAIL, E_PLATE, E_ARM = (0, 90, 0), (0, 170, 0), (0, 30, 0), (0, -40, 0), (0, -20, -40)
E_POD, E_AFE, E_FLR, E_MESH = (-130, -190, -90), (-130, -190, -180), (-130, -190, -290), (-130, -190, -360)
E_SH, E_CAP, E_TH = (260, -190, -120), (260, -190, -30), (260, -190, -260)
E_CAB = (-60, -230, -40)

# component key in model.build_components: (display name, colour, material, AirStreet BOM line, group, explode)
SPEC = {
    # 1 FieldNode core
    "fnd_body": ("FieldNode enclosure body (IP65)", C_SHELL, "plastic", 1, "shell", E_BODY),
    "fnd_lid": ("FieldNode enclosure lid", C_LID, "plastic", 1, "shell", E_LID),
    "fnd_lugs": ("FieldNode enclosure lugs", C_SHELL, "plastic", 1, "shell", E_BODY),
    "fnd_lug_screws": ("Lug screws and nuts", C_STEEL, "metal", 1, "shell", E_BODY),
    "fnd_glands": ("FieldNode cable glands (blanked)", C_DARK, "plastic", 1, "shell", E_BODY),
    "fnd_ports": ("M12 sensor ports A and B", C_STEEL, "metal", 1, "shell", E_BODY),
    "fnd_vent": ("Membrane vent", C_DARK, "plastic", 1, "shell", E_BODY),
    "fnd_antenna": ("Whip antenna (sub-GHz) and bulkhead", C_BLACK, "rubber", 1, "shell", E_BODY),
    "fnd_mplate": ("FieldNode internal mounting plate", C_ALU2, "metal", 1, "internal", E_INT),
    "fnd_mplate_screws": ("Internal plate screws", C_STEEL, "metal", 1, "internal", E_INT),
    "fnd_cell": ("LiFePO4 cell in fused holder", C_CELL, "plastic", 1, "internal", E_INT),
    "fnd_power": ("Power modules", C_PCB, "plastic", 1, "internal", E_INT),
    "fnd_ctrl": ("Controller and LoRa module", C_PCB, "plastic", 1, "internal", E_INT),
    "fnd_connectors": ("Plug-in connector strip", "#2E7D5B", "plastic", 1, "internal", E_INT),
    # 2 panel and bracket
    "fnd_plate_clip_r": ("Plate clip, right", C_ALU2, "metal", 2, "shell", E_BRK),
    "fnd_plate_clip_l": ("Plate clip, left", C_ALU2, "metal", 2, "shell", E_BRK),
    "fnd_post_r": ("Panel post, right", C_ALU2, "metal", 2, "shell", E_BRK),
    "fnd_post_l": ("Panel post, left", C_ALU2, "metal", 2, "shell", E_BRK),
    "fnd_strut_r": ("Panel strut, right", C_ALU2, "metal", 2, "shell", E_BRK),
    "fnd_strut_l": ("Panel strut, left", C_ALU2, "metal", 2, "shell", E_BRK),
    "fnd_high_panel_clip_r": ("High panel clip, right", C_ALU2, "metal", 2, "shell", E_PAN),
    "fnd_high_panel_clip_l": ("High panel clip, left", C_ALU2, "metal", 2, "shell", E_PAN),
    "fnd_low_panel_clip_r": ("Low panel clip, right", C_ALU2, "metal", 2, "shell", E_PAN),
    "fnd_low_panel_clip_l": ("Low panel clip, left", C_ALU2, "metal", 2, "shell", E_PAN),
    "fnd_bracket_bolts": ("Bracket bolts", C_STEEL, "metal", 2, "shell", E_BRK),
    "fnd_panel": ("Solar panel (6 W)", C_CELLS, "screen", 2, "shell", E_PAN),
    "fnd_panel_bolts": ("Panel clip bolts", C_STEEL, "metal", 2, "shell", E_PAN),
    # 3 mount
    "saddle_low": ("Printed V-saddle, lower (ASA)", C_SADDLE, "plastic", 3, "shell", E_SAD),
    "saddle_up": ("Printed V-saddle, upper (ASA)", C_SADDLE, "plastic", 3, "shell", E_SAD),
    "rail": ("Mounting rail (40 x 4 mm aluminium)", C_ALU, "metal", 3, "shell", E_RAIL),
    "bands": ("Stainless band clamps", C_STEEL, "metal", 3, "shell", E_BAND),
    "lplate": ("Lower adapter plate (aluminium, windowed)", C_ALU2, "metal", 3, "shell", E_PLATE),
    "uplate": ("Upper adapter plate (aluminium, windowed)", C_ALU2, "metal", 3, "shell", E_PLATE),
    "arm": ("Cross arm (aluminium angle)", C_ALU, "metal", 3, "shell", E_ARM),
    "saddle_screws": ("Saddle screws", C_STEEL, "metal", 11, "shell", E_RAIL),
    "plate_bolts": ("Adapter plate bolts", C_STEEL, "metal", 11, "shell", E_PLATE),
    "arm_bolts": ("Cross arm bolts", C_STEEL, "metal", 11, "shell", E_ARM),
    # 4 to 7 pod and its sensors
    "pod_shell": ("Sensor pod shell with drip lid (printed ASA)", C_POD, "plastic", 4, "shell", E_POD),
    "pod_glands": ("Pod roof glands and probe socket", C_DARK, "plastic", 11, "shell", E_POD),
    "pod_screws": ("Pod hanging screws", C_STEEL, "metal", 11, "shell", E_ARM),
    "pod_floor": ("Pod sensor floor (printed ASA)", C_FLOOR, "plastic", 4, "internal", E_FLR),
    "mesh": ("Stainless insect mesh", C_STEEL, "metal", 4, "shell", E_MESH),
    "floor_screws": ("Floor screws", C_STEEL, "metal", 11, "shell", E_MESH),
    "pm": ("PM sensor (SPS30 class)", C_SPS, "metal", 5, "internal", E_FLR),
    "no2": ("NO2 sensor (B4 class, four-electrode)", C_DARK, "plastic", 6, "internal", E_FLR),
    "afe": ("NO2 front end and ADC board", "#1E3A8A", "plastic", 7, "internal", E_AFE),
    "afe_standoffs": ("Front end standoffs", C_STEEL, "metal", 11, "internal", E_AFE),
    "tblock": ("Pod terminal block", "#2E7D5B", "plastic", 11, "internal", E_AFE),
    # 8, 9 shield and probe
    "shield_plates": ("Radiation shield plates (white ASA)", C_PLATE, "plastic", 8, "shell", E_SH),
    "spacers": ("Shield spacers", C_LABEL, "plastic", 8, "shell", E_SH),
    "rods": ("Shield rods and nuts (stainless)", C_STEEL, "metal", 8, "shell", E_SH),
    "shield_cap": ("Radiation shield cap", C_PLATE, "plastic", 8, "shell", E_CAP),
    "cap_screws": ("Cap screws", C_STEEL, "metal", 11, "shell", E_ARM),
    "th": ("Temperature and humidity probe (SHT45) on its tube", C_ALU, "metal", 9, "internal", E_TH),
    # 10 cables
    "cables": ("Sensor cables M12 and probe lead", C_BLACK, "rubber", 10, "shell", E_CAB),
}


def _text_ny(txt, size, x, y, z, h=0.3):
    """Raised text on a face that looks toward -Y (reads correctly from the street), centred on (x, z)."""
    t = extrude(Text(txt, font_size=size, font_path=str(_FONT), align=(Align.CENTER, Align.CENTER)), amount=h)
    pl = Plane(origin=(x, y, z), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    return pl * t


def product_parts(P=PARAMS):
    D = derived(P)
    C = build_components(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    for key, (name, color, material, bom, group, ex) in SPEC.items():
        add(name, C[key].shape, color, material, bom, group, ex)

    # ------------------------------------------------ appearance-only: FieldNode lid label and status light
    ew, ed, eh = P["enc"]
    z0 = P["enc_z0"]
    ly = C["fnd_lid"].shape.bounding_box().min.Y - 0.2         # just proud of the lid's street face
    lz = z0 + eh / 2 + 18
    add("Lid label", bx(-54, 54, ly - 0.2, ly + 0.2, lz - 42, lz + 42), C_LABEL, "paper", 1, "shell", E_LID)
    add("Lid label accent band", bx(-54, 54, ly - 0.45, ly - 0.15, lz + 27, lz + 41), C_ACCENT, "painted", 1, "shell", E_LID)
    ink = _text_ny("AirStreet", 13.0, 0, ly - 0.2, lz + 12)
    ink += _text_ny("PM2.5 + NO2 STREET NODE", 5.6, 0, ly - 0.2, lz - 6)
    ink += _text_ny("RAW SIGNALS, OPEN CALIBRATION", 4.6, 0, ly - 0.2, lz - 17)
    ink += bx(-42, 42, ly - 0.5, ly - 0.2, lz - 30.6, lz - 29.4)
    add("Lid label print", ink, C_DARK, "paper", 1, "shell", E_LID)
    add("Lid label band text", _text_ny("FIELDNODE CORE", 6.5, 0, ly - 0.45, lz + 34, h=0.2), C_LABEL, "paper", 1,
        "shell", E_LID)
    lx_, lz_ = ew / 2 - 22, z0 + 24
    bez = ycyl(lx_, ly - 0.8, lz_, 4.5, 1.6) - ycyl(lx_, ly - 0.8, lz_, 2.6, 3.0)
    add("Status light bezel", bez, C_BLACK, "plastic", 1, "shell", E_LID)
    dome = Pos(lx_, ly + 1.4, lz_) * Sphere(3.0) & bx(lx_ - 5, lx_ + 5, ly - 1.6, ly, lz_ - 5, lz_ + 5)
    add("Status light, green (lit)", dome, C_LED_G, "emissive", 1, "shell", E_LID)

    # ------------------------------------------------ appearance-only: pod label strip on the street face
    W, Dp, H = P["pod"]
    px = P["pod_x"]
    yl = D["pod_yc"] - Dp / 2 - 0.2
    zl = D["pod_bot"] + H / 2
    add("Pod accent band", bx(px - W / 2 + 22, px + W / 2 - 22, yl - 0.2, yl + 0.2, zl + 14, zl + 18), C_ACCENT,
        "painted", 4, "shell", E_POD)
    add("Pod label print", _text_ny("INLET BELOW  ·  PM  ·  NO2", 5.0, px, yl - 0.1, zl + 4, h=0.3), C_DARK,
        "paper", 4, "shell", E_POD)

    # ------------------------------------------------ context (not in the BOM)
    add("Street light pole section (140 mm)", pole_stub(P, *POLE_Z), C_POLE, "painted", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:52s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")

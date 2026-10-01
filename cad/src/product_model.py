"""AirStreet product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the FieldNode core (light grey IP65 enclosure with a
lid, parting line, lid screws, side ribs, lid label and a lit green status light), its 6 W solar
panel with an aluminium frame and cell grid on the flat-bar bracket, M12 sockets and the two sensor
cables with knurled plugs, the whip antenna with its swivel knuckle, the printed sensor pod with its
drip lid, lid screws, cable glands, side ribs and a clear service window showing the PM sensor, the
NO2 sensor and the front end board, the eight-plate radiation shield with dished plates, spacers,
rods, nuts and the temperature and humidity probe, and the mount (V-saddles, rail, band clamps with
worm housings, adapter bars, shield arm with its probe cable clips). Inside the FieldNode core:
the power and radio board and the LiFePO4 cell (illustrative envelopes). Context is a short
section of a 140 mm street light pole.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and build_parts() in model.py,
with the same axes: the pole is the Z axis, Z is up with the sidewalk at z = 0 and the node faces
the street (-Y). The pod window is an appearance choice for the renders and is recorded in
docs/REVIEW.md (session 2026-09-26) as proposed, awaiting Amish.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Align, Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Text,
                       Vector, extrude, fillet)
from model import PARAMS as _PARAMS, derived, build_parts, box as m_box, zcyl as m_zcyl, fuse

# STALE (AST-DDR-003, 2026-09-30): this appearance model still follows the TRL 3 concept. The
# constructable model.py dropped the concept-only parameters below, so they are kept here to let
# the renders run unchanged until the appearance model is rebuilt on Amish's Mac.
_CONCEPT_ONLY = {"adapter": (180.0, 25.0, 3.0), "ant_x": 58.0, "arm_z": 3100.0, "gland_x": (8.0, 34.0),
                 "m16_d": (20.0, 24.0), "port_x": (-52.0, -22.0), "post_foot_dz": 260.0, "slot": (50.0, 60.0),
                 "strut_foot_dz": 210.0, "th_stem": (6.0, 56.0), "whip": (10.0, 190.0)}
PARAMS = dict(_PARAMS, **_CONCEPT_ONLY)

_FONT = Path(__file__).resolve().parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf"

TITLE = "AirStreet: street-level air quality node for PM2.5 and NO2"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 20, "az": -56,
     "note": "Product render from the front right and above (about 20 deg elevation), on a short section of "
             "street light pole: solar panel over the FieldNode core, sensor pod with its clear window at "
             "left, radiation shield on its arm at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded view from the front right and above (about 26 deg elevation): solar panel and bracket, "
             "FieldNode enclosure, lid, board and LiFePO4 cell; sensor pod, drip lid, PM sensor, NO2 sensor "
             "and front end; radiation shield, cap and probe; rail, saddles and band clamps"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 12, "az": -64,
     "note": "Detail from the front right, slightly above (about 12 deg elevation), without the pole: PM "
             "sensor, NO2 sensor and front end behind the pod window, radiation shield at right, green "
             "status light lit"},
]

POLE_Z = (2900.0, 3740.0)   # context pole section, just enough to carry the node

# Colours (restrained product palette, shared with the other FieldNode renders; kit accent)
C_SHELL = "#DADDE1"      # light grey polycarbonate
C_LID = "#E6E8EB"
C_POD = "#ECECEA"        # printed ASA, off-white
C_PLATE = "#F2F2EF"      # shield plates, white ASA
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_ALU = "#C3C8CE"
C_ALU2 = "#AEB4BB"
C_STEEL = "#9CA3AB"
C_CELLS = "#1B2735"
C_GRID = "#C9CDD3"
C_PCB = "#166534"
C_CHIP = "#111827"
C_CELL = "#2F4F6F"
C_WINDOW = "#DCEBF5"
C_LABEL = "#F4F4F2"
C_LED_G = "#22C55E"
C_SPS = "#B9BFC6"        # SPS30 metal shell
C_POLE = "#A7ADB4"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _bx(x0, x1, y0, y1, z0, z1):
    return _box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _rod(a, c, r):
    a, c = Vector(*a), Vector(*c)
    d = c - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = _rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_y(x, y, z, af, h):
    return Pos(x, y - h / 2, z) * extrude(Plane.XZ * RegularPolygon(af / 1.732, 6), amount=-h)


def _hex_x(x, y, z, af, h):
    return Pos(x - h / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=h)


def _fmin(s, axis):
    return s.faces().sort_by(axis)[0].edges()


def _fmax(s, axis):
    return s.faces().sort_by(axis)[-1].edges()


def _text_ny(txt, size, x, y, z, h=0.3):
    """Raised text on a face that looks toward -Y (reads correctly from the street), centred on (x, z)."""
    t = extrude(Text(txt, font_size=size, font_path=str(_FONT), align=(Align.CENTER, Align.CENTER)), amount=h)
    pl = Plane(origin=(x, y, z), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    return pl * t


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def product_parts(P=PARAMS):
    D = derived(P)
    model = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    R = P["pole_od"] / 2

    # ------------------------------------------------------------ FieldNode core (BOM 1)
    ew, ed, eh = P["enc"]
    z0 = P["enc_z0"]
    y_back, y_front = D["plate_front"], D["enc_front"]      # -91 (on the rail) and -181 (lid face)
    ys = y_front + P["lid_d"]                               # parting line, as model.py
    zc = z0 + eh / 2
    wt = 3.0
    E_BODY, E_LID = (0, -170, 40), (0, -420, 40)
    E_BOARD, E_CELL = (0, -300, 110), (0, -300, -40)

    outer = _bx(-ew / 2, ew / 2, y_front, y_back, z0, z0 + eh)
    outer = _fillet_try(outer, outer.edges().filter_by(Axis.Y), [9.0, 7.0, 5.0])
    outer = _fillet_try(outer, _fmin(outer, Axis.Y), [3.0, 2.0, 1.0])
    body = outer & _bx(-200, 200, ys + 0.3, y_back + 1, z0 - 10, z0 + eh + 10)
    body -= _bx(-ew / 2 + wt, ew / 2 - wt, ys, y_back - wt, z0 + wt, z0 + eh - wt)
    for sx in (-1, 1):                                      # vertical side ribs (texture)
        for k in range(5):
            body -= _box(sx * ew / 2, ys + 14 + 10 * k, zc, 1.6, 3.0, eh - 50)
    for x in P["port_x"] + (P["ant_x"],):                   # port bosses on the bottom face
        body += _zcyl(x, D["enc_yc"], z0 - 3.0, 8.5, 6.0)
    add("FieldNode enclosure body (IP65 polycarbonate)", body, C_SHELL, "plastic", 1, "shell", E_BODY)

    lid = outer & _bx(-200, 200, y_front - 1, ys - 0.3, z0 - 10, z0 + eh + 10)
    lid -= _bx(-ew / 2 + wt, ew / 2 - wt, y_front + wt, ys, z0 + wt, z0 + eh - wt)
    add("FieldNode enclosure lid", lid, C_LID, "plastic", 1, "shell", E_LID)
    gasket = (_bx(-ew / 2 + 1.0, ew / 2 - 1.0, ys - 0.3, ys + 0.3, z0 + 1.0, z0 + eh - 1.0)
              - _bx(-ew / 2 + wt, ew / 2 - wt, ys - 1, ys + 1, z0 + wt, z0 + eh - wt))
    add("Lid gasket (seen at the parting line)", gasket, C_DARK, "rubber", 1, "shell", (0, -300, 40))

    scr = None
    for sx in (-1, 1):
        for sz in (-1, 1):
            x, z = sx * (ew / 2 - 11), zc + sz * (eh / 2 - 11)
            s = _ycyl(x, y_front - 0.6, z, 3.4, 1.2)
            s = _fillet_try(s, _fmin(s, Axis.Y), [0.5, 0.3])
            s -= _box(x, y_front - 1.2, z, 4.0, 1.0, 0.8)
            scr = s if scr is None else scr + s
    add("Lid screws", scr, C_STEEL, "metal", 11, "shell", (0, -470, 40))

    # lid label (thin raised parts)
    ly = y_front - 0.2
    lz = zc + 18
    EL = (0, -450, 40)
    add("Lid label", _box(0, ly, lz, 108, 0.4, 84), C_LABEL, "paper", 1, "shell", EL)
    add("Lid label accent band", _box(0, ly - 0.3, lz + 34, 108, 0.3, 14), C_ACCENT, "painted", 1, "shell", EL)
    ink = _text_ny("AirStreet", 13.0, 0, ly - 0.2, lz + 12)
    ink += _text_ny("PM2.5 + NO2 STREET NODE", 5.6, 0, ly - 0.2, lz - 6)
    ink += _text_ny("RAW SIGNALS, OPEN CALIBRATION", 4.6, 0, ly - 0.2, lz - 17)
    ink += _box(0, ly - 0.35, lz - 30, 84, 0.3, 1.2)
    add("Lid label print", ink, C_DARK, "paper", 1, "shell", EL)
    add("Lid label band text", _text_ny("FIELDNODE CORE", 6.5, 0, ly - 0.4, lz + 34, h=0.2), C_LABEL, "paper", 1,
        "shell", EL)

    # status light on the lid (lit)
    lx_, lz_ = ew / 2 - 22, z0 + 24
    bez = _ycyl(lx_, y_front - 1.0, lz_, 4.5, 2.0) - _ycyl(lx_, y_front - 1.0, lz_, 2.6, 3.0)
    add("Status light bezel", bez, C_BLACK, "plastic", 1, "shell", E_LID)
    dome = Pos(lx_, y_front + 0.2, lz_) * Sphere(3.0) & _bx(lx_ - 5, lx_ + 5, y_front - 3.1, y_front, lz_ - 5, lz_ + 5)
    add("Status light, green (lit)", dome, C_LED_G, "emissive", 1, "shell", E_LID)

    # bottom face: M12 sockets (port A, port B), cable glands, antenna base, as model.py positions
    yc = D["enc_yc"]
    socks = None
    for x in P["port_x"]:
        s = _hex_z(x, yc, z0 - 7.5, 20.0, 3.0) + _zcyl(x, yc, z0 - 12.5, 8.0, 7.0)
        socks = s if socks is None else socks + s
    add("M12 sensor sockets (ports A and B)", socks, C_STEEL, "metal", 1, "shell", E_BODY)
    gl = None
    for x in P["gland_x"]:
        g = _hex_z(x, yc, z0 - 8.0, P["m16_d"][1], 4.0) + (Pos(x, yc, z0 - 10.0) * Sphere(9.0)
                                                          & _bx(x - 10, x + 10, yc - 10, yc + 10, z0 - 18, z0 - 10))
        gl = g if gl is None else gl + g
    add("Enclosure glands (blanked)", gl, C_DARK, "plastic", 1, "shell", E_BODY)

    # whip antenna: model.py position and length, swivel knuckle near the top
    wd, wl = P["whip"]
    ax = P["ant_x"]
    wtop = z0 - 16.0
    ant = _hex_z(ax, yc, z0 - 8.0, 12.0, 4.0) + _zcyl(ax, yc, wtop + 3.0, 5.5, 6.0)
    ant += _ycyl(ax, yc, wtop - 5.0, 5.5, 12.0)
    add("Antenna base and swivel", ant, C_STEEL, "metal", 1, "shell", E_BODY)
    whip = _zcyl(ax, yc, wtop - 11 - (wl - 11) / 2, wd / 2, wl - 11)
    whip = _fillet_try(whip, _fmin(whip, Axis.Z), [4.0, 2.5])
    whip += _zcyl(ax, yc, wtop - 14, wd / 2 + 0.6, 6.0)
    add("Whip antenna (sub-GHz)", whip, C_BLACK, "rubber", 1, "shell", E_BODY)

    # power and radio board and LiFePO4 cell inside (illustrative envelopes, part of BOM 1)
    by = y_back - wt - 3
    pcb = _bx(-60, 60, by - 1.6, by, z0 + 60, z0 + 180)
    add("Power and radio board PCB", pcb, C_PCB, "plastic", 1, "internal", E_BOARD)
    mod = _bx(-45, -5, by - 5.0, by - 1.6, z0 + 120, z0 + 170)
    add("LoRaWAN module", mod, C_CHIP, "plastic", 1, "internal", E_BOARD)
    can = _bx(-42, -8, by - 6.0, by - 5.0, z0 + 124, z0 + 166)
    add("LoRaWAN module shield can", can, C_ALU, "metal", 1, "internal", E_BOARD)
    comps = (_bx(10, 22, by - 3.0, by - 1.6, z0 + 140, z0 + 152) + _bx(30, 42, by - 2.5, by - 1.6, z0 + 150, z0 + 158)
             + _bx(12, 40, by - 8.0, by - 1.6, z0 + 80, z0 + 100) + _bx(-50, -20, by - 12, by - 1.6, z0 + 66, z0 + 80))
    comps += _ycyl(-2, by - 7.6, z0 + 95, 4.0, 12.0)
    add("Board components", comps, C_CHIP, "plastic", 1, "internal", E_BOARD)
    add("Board terminal block", _bx(-20, 20, by - 10, by - 1.6, z0 + 62, z0 + 72), "#2E7D5B", "plastic", 1,
        "internal", E_BOARD)

    cyy, czz = yc - 4, z0 + 30
    cell = _xcyl(0, cyy, czz, 16.0, 66.0)
    cell = _fillet_try(cell, cell.edges(), [2.0, 1.0])
    add("LiFePO4 cell (32700, 6 Ah)", cell, C_CELL, "plastic", 1, "internal", E_CELL)
    caps = _xcyl(34.0, cyy, czz, 7.0, 2.0) + _xcyl(-34.0, cyy, czz, 12.0, 2.0)
    add("Cell terminals", caps, C_ALU, "metal", 1, "internal", E_CELL)
    cradle = _bx(-42, 42, cyy - 19, cyy + 19, z0 + wt, czz - 2) - _xcyl(0, cyy, czz, 16.4, 80.0)
    cradle -= _bx(-30, 30, cyy - 20, cyy + 20, z0 + wt + 4, czz)
    add("Cell cradle", cradle, C_DARK, "plastic", 1, "internal", E_CELL)

    # ------------------------------------------------------------ solar panel and bracket (BOM 2)
    pw, pl, pt = P["panel"]
    pan = Pos(0, D["panel_cy"], D["panel_cz"]) * Rot(P["tilt"], 0, 0)
    E_PAN = (0, -170, 300)
    frame = Box(pw, pl, pt)
    frame = _fillet_try(frame, frame.edges().filter_by(Axis.Z), [5.0, 3.0])
    frame -= Pos(0, 0, pt / 2 - 2) * Box(pw - 14, pl - 14, 5)
    frame -= Pos(0, 0, -pt / 2 + 6) * Box(pw - 8, pl - 8, 12.02)
    add("Solar panel frame", pan * frame, C_ALU, "metal", 2, "shell", E_PAN)
    lam = Pos(0, 0, pt / 2 - 3.2) * Box(pw - 14, pl - 14, 2.4)
    lam = lam + Pos(0, 0, -pt / 2 + 11.5) * Box(pw - 8, pl - 8, 1.0)
    add("Solar cells (6 W)", pan * lam, C_CELLS, "screen", 2, "shell", E_PAN)
    grid = None
    zt = pt / 2 - 1.85
    for k in range(1, 6):
        g = Pos(-(pw - 14) / 2 + k * (pw - 14) / 6, 0, zt) * Box(0.9, pl - 16, 0.3)
        grid = g if grid is None else grid + g
    for k in range(1, 4):
        grid += Pos(0, -(pl - 14) / 2 + k * (pl - 14) / 4, zt) * Box(pw - 16, 0.9, 0.3)
    add("Solar cell grid lines", pan * grid, C_GRID, "metal", 2, "shell", E_PAN)
    jb = Pos(0, 20, -pt / 2 + 11.0 - 6.0) * Box(50, 40, 10)
    jb = _fillet_try(jb, jb.edges().filter_by(Axis.Z), [3.0, 2.0])
    add("Panel junction box", pan * jb, C_BLACK, "plastic", 2, "shell", E_PAN)
    brk = model["panel"] - pan * Box(pw, pl, pt)
    add("Panel flat-bar bracket", brk, C_ALU2, "metal", 2, "shell", (0, -110, 170))

    # ------------------------------------------------------------ mount (BOM 3), model.py geometry
    sw, sh, st = P["saddle"]
    rw, rt = P["rail"]
    z_a, z_b = P["rail_z"]
    saddles = None
    for z in P["clamp_z"]:
        s = m_box(0, -(2 * R + st - 20) / 2, z, sw, st + 20, sh)
        s = _fillet_try(s, s.edges().filter_by(Axis.Y), [3.0, 2.0])
        s -= m_zcyl(0, 0, z, R, sh + 2)
        saddles = s if saddles is None else saddles + s
    add("Printed V-saddles (ASA)", saddles, C_DARK, "plastic", 3, "shell", (0, 90, 0))

    rail = _bx(-rw / 2, rw / 2, D["rail_back"] - rt, D["rail_back"], z_a, z_b)
    rail = _fillet_try(rail, rail.edges().filter_by(Axis.Y), [3.0, 2.0])
    for z in (z_a + 175.0, z_b - 55.0):
        rail -= _box(0, D["rail_back"] - rt / 2, z, 8.0, rt + 2, 30.0) - _box(0, D["rail_back"] - rt / 2, z, 20, rt + 4, 22)
        rail -= _ycyl(0, D["rail_back"] - rt / 2, z + 11, 4.0, rt + 2) + _ycyl(0, D["rail_back"] - rt / 2, z - 11, 4.0, rt + 2)
        rail -= _box(0, D["rail_back"] - rt / 2, z, 8.0, rt + 2, 22)
    add("Mounting rail (40 x 5 mm aluminium)", rail, C_ALU, "metal", 3, "shell", (0, 30, 0))

    bw, bt = P["band"]
    bands = None
    heads = None
    for z in P["clamp_z"]:
        ring = m_zcyl(0, 0, z, R + bt, bw) - m_zcyl(0, 0, z, R, bw + 2)
        strap = m_box(0, D["rail_front"] - bt / 2, z, rw + 12, bt, bw)
        sides = fuse(m_box(sx * (rw / 2 + 6 - bt / 2), (D["rail_front"] - R * 0.35) / 2, z, bt,
                           abs(D["rail_front"]) - R * 0.35, bw) for sx in (-1, 1))
        hous = _box(rw / 2 + 14, D["rail_front"] + 6, z, 16, 12, bw + 4)
        hous = _fillet_try(hous, hous.edges().filter_by(Axis.X), [2.0, 1.0])
        c = ring + strap + sides + hous
        bands = c if bands is None else bands + c
        h = _hex_x(rw / 2 + 24.0, D["rail_front"] + 6, z, 8.0, 4.0) + _xcyl(rw / 2 + 21.0, D["rail_front"] + 6, z, 3.0, 3.0)
        heads = h if heads is None else heads + h
    add("Stainless band clamps", bands, C_STEEL, "metal", 3, "shell", (0, 170, 0))
    add("Band clamp worm screws", heads, C_ALU2, "metal", 3, "shell", (0, 170, 0))

    al, aw_, at_ = P["adapter"]
    ad = None
    bolts = None
    for dz in (P["post_foot_dz"], P["strut_foot_dz"] + 5.0):
        z = z0 + dz
        a = _box(0, D["rail_front"] - at_ / 2, z, al, at_, aw_)
        a = _fillet_try(a, a.edges().filter_by(Axis.Y), [3.0, 2.0])
        ad = a if ad is None else ad + a
        for x in (-12.0, 12.0):
            b = _hex_y(x, D["rail_front"] - at_ - 1.5, z, 10.0, 3.0)
            bolts = b if bolts is None else bolts + b
    add("Panel bracket adapter bars", ad, C_ALU2, "metal", 3, "shell", (0, -40, 170))
    add("Adapter bar bolts", bolts, C_STEEL, "metal", 11, "shell", (0, -60, 170))

    aw, at = P["arm"]
    so = P["shield"][0]
    x_arm0, x_arm1 = 15.0, P["shield_x"] + so * 0.2
    arm = _bx(x_arm0, x_arm1, D["pod_yc"] - aw / 2, D["pod_yc"] + aw / 2, P["arm_z"], P["arm_z"] + at)
    arm = _fillet_try(arm, _fmax(arm, Axis.X), [3.0, 2.0])
    gusset = m_box(rw / 2 + 5, (D["rail_front"] + D["pod_yc"] - aw / 2) / 2, P["arm_z"] + at / 2,
                   10, D["rail_front"] - D["pod_yc"] + aw / 2, at)
    add("Shield arm and gusset", arm + gusset, C_ALU, "metal", 3, "shell", (0, 0, 0))

    # ------------------------------------------------------------ sensor pod (BOM 4)
    W, Dp, H = P["pod"]
    pwt = P["pod_wall"]
    px, py = P["pod_x"], D["pod_yc"]
    pb, ptop = D["pod_bot"], D["pod_top"]
    E_POD, E_PLID, E_SENS = (-130, -190, -330), (-130, -190, -90), (-130, -190, -200)
    po = _bx(px - W / 2, px + W / 2, py - Dp / 2, py + Dp / 2, pb, ptop)
    po = _fillet_try(po, po.edges().filter_by(Axis.Z), [10.0, 8.0, 6.0])
    po = _fillet_try(po, _fmin(po, Axis.Z), [2.5, 1.5, 1.0])
    pod = po - _bx(px - W / 2 + pwt, px + W / 2 - pwt, py - Dp / 2 + pwt, py + Dp / 2 - pwt, pb - 1, ptop - pwt)
    floor = _bx(px - W / 2 + pwt, px + W / 2 - pwt, py - Dp / 2 + pwt, py + Dp / 2 - pwt, pb, pb + pwt)
    for dx in (-45, 45):
        floor -= _box(px + dx, py, pb + pwt / 2, P["slot"][0], P["slot"][1], pwt + 2)
    pod += floor
    # service window in the street face
    wx0, wx1, wz0, wz1 = px - 70, px + 70, pb + 12, pb + 62
    win = _bx(wx0, wx1, py - Dp / 2 - 1, py - Dp / 2 + pwt + 1, wz0, wz1)
    win = _fillet_try(win, win.edges().filter_by(Axis.Y), [6.0, 4.0])
    pod -= win
    for sx in (-1, 1):                                      # vertical side ribs (texture)
        for k in range(4):
            pod -= _box(px + sx * W / 2, py - 30 + 20 * k, pb + H / 2 + 4, 1.6, 3.0, H - 36)
    add("Sensor pod shell (printed ASA)", pod, C_POD, "plastic", 4, "shell", E_POD)
    bez = _bx(wx0 - 5, wx1 + 5, py - Dp / 2 - 1.2, py - Dp / 2, wz0 - 5, wz1 + 5)
    bez = _fillet_try(bez, bez.edges().filter_by(Axis.Y), [9.0, 7.0])
    bez -= _bx(wx0, wx1, py - Dp / 2 - 3, py - Dp / 2 + 1, wz0, wz1)
    add("Pod window bezel", bez, C_DARK, "plastic", 4, "shell", E_POD)
    pane = _bx(wx0 - 2, wx1 + 2, py - Dp / 2 + pwt, py - Dp / 2 + pwt + 1.5, wz0 - 2, wz1 + 2)
    pane = _fillet_try(pane, pane.edges().filter_by(Axis.Y), [7.0, 5.0])
    add("Pod service window (clear polycarbonate)", pane, C_WINDOW, "clear", 4, "shell", E_POD)
    mesh = _bx(px - W / 2 + 5, px + W / 2 - 5, py - Dp / 2 + 5, py + Dp / 2 - 5, pb - 1.0, pb)
    for k in range(15):
        mesh -= _box(px - W / 2 + 12 + k * 10.5, py, pb - 1.0, 1.2, Dp - 16, 0.8)
    add("Stainless insect mesh", mesh, C_STEEL, "metal", 4, "shell", (-130, -190, -390))
    # pod label strip above the window
    yl = py - Dp / 2 - 0.2
    add("Pod accent band", _box(px, yl, pb + 84, W - 44, 0.4, 4.0), C_ACCENT, "painted", 4, "shell", E_POD)
    add("Pod label print", _text_ny("INLET BELOW  ·  PM  ·  NO2", 5.0, px, yl - 0.1, pb + 74.5, h=0.3),
        C_DARK, "paper", 4, "shell", E_POD)

    ov, lt = P["lid"]
    dl = _bx(px - W / 2 - ov, px + W / 2 + ov, py - Dp / 2 - ov, py + Dp / 2 + ov, ptop, ptop + lt)
    dl = _fillet_try(dl, dl.edges().filter_by(Axis.Z), [14.0, 10.0, 6.0])
    dl = _fillet_try(dl, _fmax(dl, Axis.Z), [1.2, 0.8])
    add("Pod drip lid", dl, C_POD, "plastic", 4, "shell", E_PLID)
    ls = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = px + sx * (W / 2 - 10), py + sy * (Dp / 2 - 10)
            s = _zcyl(x, y, ptop + lt + 0.6, 3.2, 1.2)
            s = _fillet_try(s, _fmax(s, Axis.Z), [0.5, 0.3])
            s -= _box(x, y, ptop + lt + 1.2, 3.8, 0.8, 1.0)
            ls = s if ls is None else ls + s
    add("Pod lid screws", ls, C_STEEL, "metal", 11, "shell", (-130, -190, -60))
    pg = None
    lid_top = D["lid_top"]
    for x in list(P["port_x"]) + [px + W / 2 - 10]:
        g = _hex_z(x, py, lid_top + 1.5, 14.0, 3.0) + (Pos(x, py, lid_top + 3.0) * Sphere(6.0)
                                                      & _bx(x - 7, x + 7, py - 7, py + 7, lid_top + 3.0, lid_top + 8))
        pg = g if pg is None else pg + g
    add("Pod cable glands", pg, C_DARK, "plastic", 11, "shell", E_PLID)

    # sensors inside the pod (BOM 5, 6, 7), model.py envelopes
    a, c_, d = P["sps30"]
    zf = pb + pwt
    spx, spy = px - 45, py + 20
    sps = _box(spx, spy, zf + 8 + a / 2, a, d, c_)
    sps = _fillet_try(sps, sps.edges().filter_by(Axis.Y), [1.5, 1.0])
    add("PM sensor (SPS30 class)", sps, C_SPS, "metal", 5, "internal", E_SENS)
    inl = _box(spx, spy, zf + 4, 14, 10, 8)
    add("PM sensor inlet and fan outlet", inl, C_BLACK, "plastic", 5, "internal", E_SENS)
    sfy = spy - d / 2 - 0.15
    add("PM sensor label", _box(spx, sfy, zf + 8 + a / 2 + 2, 30, 0.3, 22), C_LABEL, "paper", 5, "internal", E_SENS)
    add("PM sensor label print", _text_ny("SPS30", 5.0, spx, sfy - 0.2, zf + 8 + a / 2 + 6, h=0.2)
        + _box(spx, sfy - 0.25, zf + 8 + a / 2 - 3, 22, 0.2, 1.0), C_DARK, "paper", 5, "internal", E_SENS)

    bd, bh = P["b4"]
    nx_, ny_ = px + 45, py + 20
    nz_ = zf + 8 + bh / 2
    no2 = _zcyl(nx_, ny_, nz_, bd / 2, bh)
    no2 = _fillet_try(no2, _fmax(no2, Axis.Z), [1.5, 1.0])
    add("NO2 sensor (B4 class, four-electrode)", no2, C_DARK, "plastic", 6, "internal", E_SENS)
    band = (_zcyl(nx_, ny_, nz_ + 1, bd / 2 + 0.3, 10) - _zcyl(nx_, ny_, nz_ + 1, bd / 2 - 1, 12)) \
        & _bx(nx_ - 20, nx_ + 20, ny_ - 20, ny_, nz_ - 10, nz_ + 10)
    add("NO2 sensor label", band, C_LABEL, "paper", 6, "internal", E_SENS)
    holder = _zcyl(nx_, ny_, zf + 5, bd / 2 + 2.5, 10) - _zcyl(nx_, ny_, zf + 5, bd / 2 + 0.1, 12)
    holder += _zcyl(nx_, ny_, zf + 0.5 + 0.5, bd / 2 + 2.5, 1) - _zcyl(nx_, ny_, zf + 1, bd / 2 - 4, 3)
    add("NO2 sensor holder (with ozone filter)", holder, C_BLACK, "plastic", 6, "internal", E_SENS)

    fw, ft, fh = P["afe"]
    ay = py + Dp / 2 - pwt - 4
    az_ = pb + H / 2 + 5
    afe = _box(px, ay, az_, fw, ft, fh)
    afe = _fillet_try(afe, afe.edges().filter_by(Axis.Y), [2.0, 1.0])
    add("NO2 front end and ADC board", afe, "#1E3A8A", "plastic", 7, "internal", E_SENS)
    comp = _box(px, ay - 5, az_, 50, 7, 22)
    comp += _box(px - 36, ay - 3.5, az_ + 14, 14, 4, 10) + _box(px + 36, ay - 3.5, az_ + 14, 12, 4, 8)
    comp += _box(px + 34, ay - 4.5, az_ - 18, 20, 6, 8)
    add("Front end components", comp, C_CHIP, "plastic", 7, "internal", E_SENS)
    add("Front end shield can", _box(px, ay - 8.7, az_, 46, 0.6, 18), C_ALU, "metal", 7, "internal", E_SENS)

    # ------------------------------------------------------------ radiation shield (BOM 8, 9)
    so, si, stk, pitch, n = P["shield"]
    sx0, sy0 = P["shield_x"], D["sh_yc"]
    E_SH, E_CAP, E_TH = (260, -190, -120), (260, -190, -30), (260, -190, -260)
    plates = None
    for k in range(n):
        zk = D["sh_bot"] + k * pitch
        ring = _zcyl(sx0, sy0, zk, so / 2, stk) - _zcyl(sx0, sy0, zk, si / 2, stk + 2)
        lip = _zcyl(sx0, sy0, zk - stk / 2 - 3.0, so / 2, 6.0) - _zcyl(sx0, sy0, zk - stk / 2 - 3.0, so / 2 - 1.6, 7.0)
        pk = ring + lip
        pk = _fillet_try(pk, [e for e in pk.edges() if abs(e.center().Z - (zk - stk / 2 - 6.0)) < 0.2], [0.7, 0.4])
        plates = pk if plates is None else plates + pk
    add("Radiation shield plates (white ASA)", plates, C_PLATE, "plastic", 8, "shell", E_SH)
    rods_xy = [(sx0 + dx, sy0 + dy) for dx, dy in ((42, 0), (-21, 36), (-21, -36))]
    spc = None
    for k in range(n - 1):
        z_lo = D["sh_bot"] + k * pitch + stk / 2
        z_hi = D["sh_bot"] + (k + 1) * pitch - stk / 2
        for (x, y) in rods_xy:
            s = _zcyl(x, y, (z_lo + z_hi) / 2, 4.0, z_hi - z_lo)
            spc = s if spc is None else spc + s
    z_lo = D["sh_bot"] + (n - 1) * pitch + stk / 2
    for (x, y) in rods_xy:
        spc += _zcyl(x, y, (z_lo + D["sh_cap"]) / 2, 4.0, D["sh_cap"] - z_lo)
    add("Shield spacers", spc, C_LABEL, "plastic", 8, "shell", E_SH)
    rods = fuse(_rod((x, y, D["sh_bot"] - 3), (x, y, P["arm_z"]), P["rod_d"] / 2) for x, y in rods_xy)
    nuts = fuse(_hex_z(x, y, D["sh_bot"] - stk / 2 - 2.5, 8.0, 4.0) for x, y in rods_xy)
    nuts += fuse(Pos(x, y, D["sh_bot"] - stk / 2 - 4.5) * Sphere(3.2) & _bx(x - 4, x + 4, y - 4, y + 4, D["sh_bot"] - 9, D["sh_bot"] - 5)
                 for x, y in rods_xy)
    nuts += fuse(_hex_z(x, y, D["sh_cap"] + P["cap"][1] + 1.5, 8.0, 3.0) for x, y in rods_xy)
    add("Shield rods and acorn nuts (stainless)", rods + nuts, C_STEEL, "metal", 8, "shell", E_SH)
    cd_, ct = P["cap"]
    cap = _zcyl(sx0, sy0, D["sh_cap"] + ct / 2, cd_ / 2, ct)
    cap = _fillet_try(cap, _fmax(cap, Axis.Z), [2.0, 1.5, 1.0])
    cap += _zcyl(sx0, sy0, D["sh_cap"] - 4.0, cd_ / 2, 8.0) - _zcyl(sx0, sy0, D["sh_cap"] - 4.5, cd_ / 2 - 1.6, 9.2)
    add("Radiation shield cap", cap, C_PLATE, "plastic", 8, "shell", E_CAP)
    ab = fuse(_hex_z(x, sy0, P["arm_z"] + at + 1.5, 8.0, 3.0) for x in (P["shield_x"] - 15, P["shield_x"] + 15))
    add("Arm to cap bolts", ab, C_STEEL, "metal", 11, "shell", (0, 0, 0))

    tbx, tby, tbz = P["th_board"]
    sd, sl = P["th_stem"]
    probe = _box(sx0, sy0, D["th_z"], tbx, tby, tbz)
    add("Temperature and humidity probe board (SHT45)", probe, C_PCB, "plastic", 9, "internal", E_TH)
    stem = _zcyl(sx0, sy0, D["th_z"] + tbz / 2 + sl / 2, sd / 2, sl)
    stem += _zcyl(sx0, sy0, D["th_z"] - tbz / 2 - 2.0, 3.2, 4.0)
    add("Probe stem and filter cap", stem, C_LABEL, "plastic", 9, "internal", E_TH)

    # ------------------------------------------------------------ cables (BOM 10)
    cr = P["cable_d"] / 2
    pgd, pgl = P["plug"]
    top = z0 - 16
    E_CAB = (0, -170, 10)
    plugs = None
    for x in P["port_x"]:
        nut = _zcyl(x, yc, top - 7.0, pgd / 2 + 1.0, 14.0)
        for k in range(14):
            ang = 2 * math.pi * k / 14
            nut -= Pos(x + (pgd / 2 + 1.0) * math.cos(ang), yc + (pgd / 2 + 1.0) * math.sin(ang), top - 7.0) * Box(1.2, 1.2, 15)
        plugs = nut if plugs is None else plugs + nut
    add("M12 plug coupling nuts (knurled)", plugs, C_STEEL, "metal", 10, "shell", E_CAB)
    grips = None
    for x in P["port_x"]:
        g = _zcyl(x, yc, top - 14.0 - (pgl - 14.0) / 2, pgd / 2 - 0.5, pgl - 14.0)
        g = _fillet_try(g, _fmin(g, Axis.Z), [3.0, 2.0])
        grips = g if grips is None else grips + g
    add("M12 plug bodies", grips, C_BLACK, "rubber", 10, "shell", E_CAB)
    cab = None
    for x in P["port_x"]:
        c = _rod((x, yc, top - pgl + 2), (x, py, lid_top + 6), cr)
        cab = c if cab is None else cab + c
    add("Sensor cables M12", cab, C_BLACK, "rubber", 10, "shell", E_CAB)
    zcab = P["arm_z"] + at + cr
    xe = px + W / 2 - 10
    pc = _pipe([(sx0, sy0, D["sh_cap"] + ct), (sx0, sy0, zcab), (xe, sy0, zcab), (xe, sy0, lid_top + 6)], cr)
    add("Probe cable along the arm", pc, C_BLACK, "rubber", 10, "shell", (0, 0, 0))
    clips = fuse(_bx(x - 4, x + 4, sy0 - 6, sy0 + 6, P["arm_z"] + at, zcab + cr + 1.2)
                 - _ycyl(x, sy0, zcab, cr + 0.2, 20) for x in (70.0, 140.0))
    add("Cable clips", clips, C_DARK, "plastic", 11, "shell", (0, 0, 0))

    # ------------------------------------------------------------ context (not in the BOM)
    pole = _zcyl(0, 0, (POLE_Z[0] + POLE_Z[1]) / 2, R, POLE_Z[1] - POLE_Z[0])
    pole = _fillet_try(pole, pole.edges(), [3.0, 2.0])
    add("Street light pole section (140 mm)", pole, C_POLE, "painted", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:46s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")

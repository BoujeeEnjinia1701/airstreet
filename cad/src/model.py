"""AirStreet parametric model (build123d), TRL 3, constructable design (AST-DDR-003).

Run from the repo root:  python cad/src/model.py          (exports and checks)
                         python cad/src/model.py --check  (constructability checks only)
Exports STEP and STL into cad/step and cad/stl:
    airstreet-assembly.step / .stl     the whole node on a stub of its 140 mm design pole
    airstreet-sensor-head.step / .stl  pod, sensors, front end, radiation shield, probe and cables
    airstreet-mount.step / .stl        rail, saddles, band clamps, adapter plates and cross arm

Axes: the street light pole is the Z axis (x = y = 0), Z is up with the sidewalk at z = 0, and the
node faces the street (-Y). X is to the right seen from the street.

The FieldNode core (FND, shared component) is FieldNode's own constructable model (FND-DDR-003),
imported from the vendored copy cad/src/fieldnode_core.py and moved into place: enclosure, lugs,
penetrations, internal plate and modules, panel bracket and panel, and (hot sites) the sun shield.
Per AST-DDR-002 FieldNode's back plate, V-blocks and band clamps are left off. In their place
(AST-DDR-003, "Design for construction"):
    a 40 x 5 mm rail held to the pole by two printed V-saddles (140 deg V for 80 to 200 mm poles)
        and two stainless bands cut to length, each running in a groove between saddle and rail;
    two 3 mm aluminium adapter plates on the rail that carry FieldNode's four lugs, its two plate
        clips and (hot sites) its sun shield screws, at the hole positions of FieldNode's back plate;
    a 30 x 30 x 3 mm aluminium cross arm on the rail below the enclosure, from which the pod and
        the radiation shield hang on screws from above;
    a pod made of a printed shell (walls, roof and drip lid in one) and a printed sensor floor that
        carries the PM sensor cradle and the NO2 sensor collar, behind stainless mesh;
    a radiation shield of eight printed plates on three M5 rods and spacers under a printed cap,
        with the T and RH probe on a 6 mm tube through the cap and the arm.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (AST-CAL-001), the drawing AST-DWG-001 (cad/src/sheets.py), the concept
media (cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fieldnode_core as fnd  # noqa: E402

FP = fnd.PARAMS

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site interface: pole on the Z axis; design case 140 mm OD at node height; fits 80 to 200 mm
    "pole_od": 140.0, "pole_range": (80.0, 200.0),
    # R11 inlet plane (underside of the pod mesh) above the sidewalk (DDR-001 D7: 3.0 m)
    "inlet_z": 3000.0,
    # 3 V-saddles, printed ASA: width (X), height (Z), depth (Y); included V angle; material behind
    #   the apex; band groove in the back face (height, depth); two M5 insert screws (x, dz)
    "saddle": (100.0, 50.0, 24.0), "saddle_v": 140.0, "saddle_base": 8.0, "groove": (14.0, 1.5),
    "saddle_screws": ((-14.0, 16.0), (14.0, 16.0)),
    # 3 rail flat bar (W x t) and its ends; clamp (saddle centre) heights; band width and thickness
    "rail": (40.0, 5.0), "rail_z": (3099.0, 3550.0), "clamp_z": (3150.0, 3525.0), "band": (12.7, 0.8),
    # 1 FieldNode core: enclosure (from FND), bottom height
    "enc": FP["enc"], "lid_d": FP["lid_d"], "enc_z0": 3230.0,
    # 3 adapter plates, 3 mm aluminium (W, z from, z to, relative to enc_z0) with the rail bolts (dz)
    "lplate": (180.0, -24.0, 51.0), "uplate": (180.0, 170.0, 280.0), "plate_t": 3.0,
    "lplate_bolts": (-12.0, 38.0), "uplate_bolts": (185.0, 255.0),
    # 3 cross arm: aluminium angle (leg, thickness), x from, x to; underside height = pod top;
    #   rail bolt x positions
    "arm": (30.0, 3.0), "arm_x": (-165.0, 250.0), "arm_bolt_x": (-10.0, 10.0),
    # 2 FieldNode panel at its FieldNode tilt (from FND), kept for the drawing notes
    "panel": FP["panel"], "tilt": FP["tilt"],
    # 4 sensor pod: W x D x H (floor plus shell), wall, drip lid overhang and thickness, centre x;
    #   mesh thickness; hanging screws (x offsets from the pod centre)
    "pod": (170.0, 110.0, 95.0), "pod_wall": 3.0, "lid": (15.0, 3.0), "pod_x": -90.0, "mesh_t": 1.0,
    "pod_hang_dx": (-50.0, 50.0),
    # 4 floor inlet slots: (x, y in pod coordinates, size x, size y); y + toward the back wall
    "slots": ((-45.0, -12.0, 50.0, 50.0), (45.0, -17.0, 50.0, 40.0)),
    # 5 PM sensor SPS30 (41 x 41 x 12 mm, datasheet), on edge, centre (x, y) in the pod, gap below
    "sps30": (41.0, 41.0, 12.0), "sps_xy": (-45.0, 23.0), "sps_gap": 8.0,
    # 6 NO2 sensor B4 (dia x height, assumed), centre (x, y) in the pod; window hole and collar OD
    "b4": (32.0, 20.0), "no2_xy": (45.0, 24.0), "no2_window": 28.0, "collar": (38.0, 15.0),
    # 7 front end and ADC board (W x t x H), its bottom above the floor underside, standoff length
    "afe": (86.0, 3.0, 55.0), "afe_z": 25.0, "afe_standoff": 6.0,
    # 8 radiation shield: plate OD, ID, thickness, pitch, count; cap OD and thickness; centre x;
    #   rod diameter and pitch circle radius; spacer OD
    "shield": (120.0, 56.0, 2.0, 13.0, 8), "cap": (124.0, 8.0), "shield_x": 200.0, "rod_d": 5.0,
    "rod_r": 42.0, "spacer_od": 8.0, "cap_screw_dx": (-30.0, 30.0),
    # 9 temperature and humidity probe: board (x, y, z), tube (dia)
    "th_board": (14.0, 10.0, 4.0), "th_tube": 6.0,
    # 10 cables: diameter, M12 plug (dia x length); probe cable diameter
    "cable_d": 6.0, "plug": (16.0, 45.0), "probe_cable_d": 4.5,
}

BOM = {  # build_parts key: (BOM line, name)
    "fieldnode": (1, "FieldNode core (enclosure, cell, radio)"),
    "panel": (2, "FieldNode 6 W panel hood"),
    "mount": (3, "Band clamps, saddles, rail, adapter plates and cross arm"),
    "pod": (4, "Sensor pod: shell, sensor floor, mesh"),
    "pm": (5, "Optical PM sensor (SPS30 class)"),
    "no2": (6, "Electrochemical NO2 sensor (B4 class)"),
    "afe": (7, "NO2 front end and 16-bit ADC"),
    "shield": (8, "Multi-plate radiation shield"),
    "th": (9, "Temperature and humidity sensor"),
    "cables": (10, "Sensor cables, M12, and probe lead"),
}


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought", "fieldnode" or "fixing"
    group: str | None  # key in BOM (build_parts groups components by it)


def derived(p=PARAMS):
    """Dimensions the calc note and the drawings quote, computed from PARAMS."""
    R = p["pole_od"] / 2
    sw, sh, sd = p["saddle"]
    half = math.radians(p["saddle_v"] / 2)
    rail_back = -(p["saddle_base"] + R / math.sin(half))
    rw, rt = p["rail"]
    rail_front = rail_back - rt
    plate_front = rail_front - p["plate_t"]
    ew, ed, eh = p["enc"]
    z0 = p["enc_z0"]
    dy = plate_front - (FP["plate_y0"] - FP["plate"][2])      # FieldNode model to AirStreet
    dz = z0 - FP["z0"]
    W, Dp, H = p["pod"]
    pod_bot = p["inlet_z"] + p["mesh_t"]                      # floor underside
    pod_top = pod_bot + H                                     # roof top (drip lid below it? no: lid on top)
    lid_top = pod_top + p["lid"][1]
    so, si, stk, pitch, n = p["shield"]
    sh_bot = p["inlet_z"] - 10.0                              # centre of the lowest plate
    arm_y = rail_front - p["arm"][0] / 2                      # centre line of the horizontal leg
    fd = fnd.derived(FP)
    t = math.radians(p["tilt"])
    panel_cy, panel_cz = fd["panel_cy"] + dy, fd["panel_cz"] + dz
    panel_top = fd["overall_top"] + dz
    whip_x = FP["pens"]["antenna"][0]
    whip_y = fd["enc_back"] + dy - FP["pen_rows"][1]
    pod_right = p["pod_x"] + W / 2 + p["lid"][0]
    # band length round the design pole (inner face), for the cut-to-length band
    yg = rail_back + p["groove"][1]
    P0 = (sw / 2, yg)
    d0 = math.hypot(*P0)
    a_t = math.atan2(P0[1], P0[0]) + math.acos(R / d0)
    straight = math.sqrt(d0 ** 2 - R ** 2)
    arc = R * (math.pi - 2 * a_t)
    band_len = sw + 2 * straight + arc
    return {
        "R": R, "rail_back": rail_back, "rail_front": rail_front, "plate_front": plate_front, "dy": dy, "dz": dz,
        "v_apex": rail_back + p["saddle_base"], "v_mouth": 2 * (sd - p["saddle_base"]) * math.tan(half),
        "v_contact_lat": R * math.cos(half), "enc_front": plate_front - ed, "enc_back": plate_front,
        "enc_top": z0 + eh, "enc_yc": plate_front - ed / 2,
        "panel_cy": panel_cy, "panel_cz": panel_cz, "panel_top": panel_top,
        "pod_back": rail_front, "pod_yc": rail_front - Dp / 2, "pod_bot": pod_bot, "pod_top": pod_top, "lid_top": lid_top,
        "arm_y": arm_y, "arm_z": lid_top, "arm_len": p["arm_x"][1] - p["arm_x"][0],
        "sh_bot": sh_bot, "sh_yc": arm_y, "sh_cap": lid_top - p["cap"][1],
        "th_z": sh_bot + n * pitch / 2 - 10.0,
        "whip_x": whip_x, "whip_y": whip_y, "whip_bot": z0 - 20 - FP["whip"][1],
        "whip_clear": whip_x - FP["whip"][0] / 2 - pod_right,
        "clamp_span": p["clamp_z"][1] - p["clamp_z"][0], "rail_len": p["rail_z"][1] - p["rail_z"][0],
        "overall_h": panel_top - (p["inlet_z"] - 20.0),
        "offset_front": -min(plate_front - ed, panel_cy - FP["panel"][1] / 2 * math.cos(t) - FP["panel"][2] / 2 * math.sin(t),
                            rail_front - Dp - p["lid"][0]) - R,
        "band_len": band_len, "band_tangent_deg": math.degrees(a_t),
    }


# ------------------------------------------------------------------ geometry helpers
def _b():
    import build123d as b
    return b


box, bx, zcyl, ycyl, xcyl, hexprism, fuse = fnd.box, fnd.bx, fnd.zcyl, fnd.ycyl, fnd.xcyl, fnd.hexprism, fnd.fuse


def rod(a, c, r):
    """Solid rod of radius r between two 3D points."""
    b = _b()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def path_rod(pts, r):
    """Rod along a polyline, with a ball at each corner."""
    b = _b()
    out = None
    for a, c in zip(pts, pts[1:]):
        s = rod(a, c, r)
        out = s if out is None else out + s
    for q in pts[1:-1]:
        out = out + b.Pos(*q) * b.Sphere(r)
    return out


def csk_screw_y(x, y_face, z, d, length, toward=+1):
    """Countersunk screw entering at the face y_face and running toward +Y (toward=+1) or -Y."""
    b = _b()
    hd = 2 * d
    hh = d * 0.5
    head = b.Pos(x, y_face + toward * hh / 2, z) * b.Rot(-90 * toward, 0, 0) * b.Cone(hd / 2 + 0.1, d / 2, hh)
    shank = ycyl(x, y_face + toward * length / 2, z, d / 2 - 0.3, length)
    return head + shank


def bolt_y_from_back(y_back, y_front, x, z, d=5.0, head=8.0, csk=False):
    """Bolt along Y clamping y_front..y_back (y_front < y_back). Head at the back (+Y side) and nyloc
    nut in front, or countersunk head flush in front and nyloc behind (csk=True)."""
    hl, nl = 0.55 * d, 0.9 * d
    if csk:
        return (csk_screw_y(x, y_front, z, d, y_back - y_front, toward=+1)
                + hexprism("y", x, y_back + nl / 2, z, head, nl) + ycyl(x, y_back + nl + 1, z, d / 2 - 0.3, 2))
    return (ycyl(x, y_back + hl / 2, z, head / 2 + 0.75, hl) + ycyl(x, (y_back + y_front) / 2, z, d / 2 - 0.3, y_back - y_front)
            + hexprism("y", x, y_front - nl / 2, z, head, nl) + ycyl(x, y_front - nl - 1, z, d / 2 - 0.3, 2))


def screw_z_down(x, y, z_top, length, d=5.0, head=8.5):
    """Pan-head screw from above: head sits on z_top, shank runs down `length`."""
    hl = 0.6 * d
    return zcyl(x, y, z_top + hl / 2, head / 2, hl) + zcyl(x, y, z_top - length / 2, d / 2 - 0.3, length)


def _fnd_components(p=PARAMS, shield=False):
    """FieldNode's own components (FND-DDR-003), moved into place. Its back plate, V-blocks and
    band clamps are not used (AST-DDR-002)."""
    b = _b()
    D = derived(p)
    T = b.Pos(0, D["dy"], D["dz"])
    C = fnd.build_components(FP, shield=shield)
    skip = {"plate", "vblock_low", "vblock_up", "bands"}
    return {k: Comp(c.name, T * c.shape, c.bom, "fieldnode", c.group) for k, c in C.items() if k not in skip}


def pod_frame(p=PARAMS):
    """Placement from pod coordinates (x across, y toward the back wall, z up from the floor
    underside) to the model."""
    b = _b()
    D = derived(p)
    return b.Pos(p["pod_x"], D["pod_yc"], D["pod_bot"])


def build_components(p=PARAMS, shield=False):
    """Every component as a Comp, keyed by a short name. shield=True adds FieldNode's hot-site
    sun shield and its thumb screws."""
    b = _b()
    D = derived(p)
    R = D["R"]
    z0 = p["enc_z0"]
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    # ---------------------------------------------------------- 3 mount
    sw, sh, sd = p["saddle"]
    rw, rt = p["rail"]
    yrb, yrf = D["rail_back"], D["rail_front"]
    gh, gd = p["groove"]
    half = math.radians(p["saddle_v"] / 2)
    ya = D["v_apex"]
    m = sd - p["saddle_base"] + 2
    for key, zc in (("saddle_low", p["clamp_z"][0]), ("saddle_up", p["clamp_z"][1])):
        s = bx(-sw / 2, sw / 2, yrb, yrb + sd, zc - sh / 2, zc + sh / 2)
        tri = b.Pos(0, 0, zc - sh / 2 - 1) * b.extrude(b.Polygon((0, ya), (m * math.tan(half), ya + m), (-m * math.tan(half), ya + m), align=None), sh + 2)
        s -= tri
        s -= bx(-sw / 2 - 1, sw / 2 + 1, yrb - 1, yrb + gd, zc - gh / 2, zc + gh / 2)          # band groove
        for sx, dzs in p["saddle_screws"]:
            s -= ycyl(sx, yrb + 5, zc + dzs, 3.4, 10.0)                                  # M5 heat-set insert hole
        add(key, "V-saddle, " + ("lower" if key == "saddle_low" else "upper"), s, 3, "made", "mount")

    za, zb = p["rail_z"]
    rail = bx(-rw / 2, rw / 2, yrf, yrb, za, zb)
    holes = []
    for zc in p["clamp_z"]:
        holes += [(sx, zc + dzs, "csk_rail") for sx, dzs in p["saddle_screws"]]
    holes += [(0.0, z0 + dzb, "plain") for dzb in p["lplate_bolts"] + p["uplate_bolts"]]
    arm_bz = D["arm_z"] + p["arm"][1] + (p["arm"][0] - p["arm"][1]) / 2
    holes += [(x, arm_bz, "plain") for x in p["arm_bolt_x"]]
    for x, z, kind in holes:
        rail -= ycyl(x, (yrf + yrb) / 2, z, 2.75, rt + 2)
        if kind == "csk_rail":
            rail -= b.Pos(x, yrf, z) * b.Rot(-90, 0, 0) * b.Cone(5.1, 2.6, 2.6, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
    add("rail", "Rail", rail, 3, "made", "mount")

    # bands: stainless band cut to length, round the far side of the pole and through the saddle groove
    bw, bt = p["band"]
    bands = []
    for zc in p["clamp_z"]:
        yg = yrb + gd
        inner = b.make_hull(b.Circle(R).edges() + b.Polyline((-sw / 2, yg), (sw / 2, yg)).edges())
        outer = b.offset(inner, bt, kind=b.Kind.ARC)
        ring = b.Pos(0, 0, zc - bw / 2) * (b.extrude(outer, bw) - b.extrude(inner, bw))
        ang = math.radians(35.0)
        hx, hy = (R + bt + 5) * math.cos(ang), (R + bt + 5) * math.sin(ang)
        ring += b.Pos(hx, hy, zc) * b.Rot(0, 0, math.degrees(ang) + 90) * b.Box(18, 10, bw + 4)
        bands.append(ring)
    add("bands", "Band clamps (2), cut to length", fuse(bands), 3, "bought", "mount")

    # adapter plates: FieldNode's back plate hole pattern, in two strips
    pt = p["plate_t"]
    ypm = yrf - pt / 2
    lx = FP["lug"][0]
    clip_hx = FP["clip_x"] + FP["angle"][1] - FP["angle"][0] + 12
    shx = FP["enc"][0] / 2 + FP["shield_gap"] - FP["shield_flange"] / 2
    lug_dz = (-(FP["lug"][3] / 2) - 1, FP["enc"][2] + FP["lug"][3] / 2 + 1)
    for key, spec, bolts, name in (("lplate", p["lplate"], p["lplate_bolts"], "Lower adapter plate"),
                                   ("uplate", p["uplate"], p["uplate_bolts"], "Upper adapter plate")):
        w_, z_a, z_b = spec
        pl = bx(-w_ / 2, w_ / 2, yrf - pt, yrf, z0 + z_a, z0 + z_b)
        for sx in (-1, 1):
            for dz in lug_dz:
                if z_a < dz < z_b:
                    pl -= ycyl(sx * lx, ypm, z0 + dz, 2.75, pt + 2)
            for dz in (FP["clip_z"][0] + 17, FP["clip_z"][1] - 30):
                if z_a < dz < z_b:
                    pl -= ycyl(sx * clip_hx, ypm, z0 + dz, 2.75, pt + 2)
            for dz in FP["shield_screw_dz"]:
                if z_a < dz < z_b:
                    pl -= ycyl(sx * shx, ypm, z0 + dz, 1.65, pt + 2)          # M4 tapped
        for dzb in bolts:
            pl -= ycyl(0, ypm, z0 + dzb, 2.75, pt + 2)
            pl -= b.Pos(0, yrf - pt, z0 + dzb) * b.Rot(-90, 0, 0) * b.Cone(5.1, 2.6, 2.6, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
        add(key, name, pl, 3, "made", "mount")

    # cross arm: 30 x 30 x 3 angle, vertical leg on the rail front, horizontal leg at the bottom
    #   pointing to the street; the pod and the shield cap hang under it on screws from above
    al, at = p["arm"]
    xa0, xa1 = p["arm_x"]
    zA = D["arm_z"]
    arm = bx(xa0, xa1, yrf - al, yrf, zA, zA + at) + bx(xa0, xa1, yrf - at, yrf, zA, zA + al)
    for x in p["arm_bolt_x"]:
        arm -= ycyl(x, yrf - at / 2, arm_bz, 2.75, at + 2)
    ay = D["arm_y"]
    hang = [(p["pod_x"] + dx, ay) for dx in p["pod_hang_dx"]] + [(p["shield_x"] + dx, ay) for dx in p["cap_screw_dx"]]
    for x, y in hang:
        arm -= zcyl(x, y, zA + at / 2, 2.75, at + 2)
    arm -= zcyl(p["shield_x"], ay, zA + at / 2, 4.0, at + 2)                          # probe tube and lead
    add("arm", "Cross arm", arm, 3, "made", "mount")

    # mount fixings
    fx = []
    for zc in p["clamp_z"]:
        for sx, dzs in p["saddle_screws"]:
            fx.append(csk_screw_y(sx, yrf, zc + dzs, 5.0, 14.0, toward=+1))
    add("saddle_screws", "M5 countersunk screws, saddles (4)", fuse(fx), 11, "fixing", None)
    fx = [bolt_y_from_back(yrb, yrf - pt, 0.0, z0 + dzb, csk=True) for dzb in p["lplate_bolts"] + p["uplate_bolts"]]
    add("plate_bolts", "M5 countersunk bolts, adapter plates (4)", fuse(fx), 11, "fixing", None)
    fx = [bolt_y_from_back(yrb, yrf - at, x, arm_bz) for x in p["arm_bolt_x"]]
    add("arm_bolts", "M5 bolts, cross arm (2)", fuse(fx), 11, "fixing", None)

    # ---------------------------------------------------------- 1, 2 FieldNode core
    for k, c in _fnd_components(p, shield=shield).items():
        C["fnd_" + k] = c

    # ---------------------------------------------------------- 4 sensor pod
    F = pod_frame(p)
    W, Dp, H = p["pod"]
    wt = p["pod_wall"]
    ov, lt = p["lid"]
    ft = wt                                              # floor thickness
    # shell: four walls and roof from the floor top up, drip lid on top, open at the bottom
    shell = bx(-W / 2, W / 2, -Dp / 2, Dp / 2, ft, H) - bx(-W / 2 + wt, W / 2 - wt, -Dp / 2 + wt, Dp / 2 - wt, ft - 1, H - wt)
    shell += bx(-W / 2 - ov, W / 2 + ov, -Dp / 2 - ov, Dp / 2 + ov, H, H + lt)
    bxs, bys = W / 2 - wt - 4, Dp / 2 - wt - 4
    for sx in (-1, 1):
        for sy in (-1, 1):
            shell += zcyl(sx * bxs, sy * bys, ft + 10, 4.0, 20.0)                 # floor screw bosses
            shell -= zcyl(sx * bxs, sy * bys, ft + 5, 2.0, 10.1)                  # M3 insert
    hy = D["arm_y"] - D["pod_yc"]
    for dx in p["pod_hang_dx"]:
        shell += zcyl(dx, hy, H - wt - 6, 6.0, 12.0)                              # hanging bosses
        shell -= zcyl(dx, hy, H + lt - 5, 3.4, 10.1)                              # M5 insert from above
    # glands: two M16 in the roof under the ports; an M8 4-pin panel socket in the right wall for the probe lead
    gx = [x - p["pod_x"] for x in (FP["pens"]["port_a"][0], FP["pens"]["port_b"][0])]
    gy = D["whip_y"] - D["pod_yc"]                                                  # the port row
    for x in gx:
        shell -= zcyl(x, gy, H + lt / 2 - wt / 2, 8.1, wt + lt + 2)
    pgy, pgz = 10.0, 49.0
    shell -= xcyl(W / 2 - wt / 2, pgy, pgz, 4.1, wt + 2)
    # back wall bosses for the front end standoffs
    afw, aft, afh = p["afe"]
    for sx in (-1, 1):
        for zz in (p["afe_z"] + 6, p["afe_z"] + afh - 6):
            shell += ycyl(sx * (afw / 2 - 5), Dp / 2 - wt - 2, zz, 3.5, 4.0)
            shell -= ycyl(sx * (afw / 2 - 5), Dp / 2 - wt - 2, zz, 1.6, 4.1)       # M3 insert
    add("pod_shell", "Pod shell", F * shell, 4, "made", "pod")

    floor = bx(-W / 2, W / 2, -Dp / 2, Dp / 2, 0, ft)
    for sx_, sy_, lx_, ly_ in p["slots"]:
        floor -= bx(sx_ - lx_ / 2, sx_ + lx_ / 2, sy_ - ly_ / 2, sy_ + ly_ / 2, -1, ft + 1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            floor -= zcyl(sx * bxs, sy * bys, ft / 2, 1.7, ft + 2)
    # PM sensor cradle: two ribs either side of the sensor and two pads it stands on
    a_, c_, d_ = p["sps30"]
    spx, spy = p["sps_xy"]
    for sy in (-1, 1):
        floor += bx(spx - 25, spx + 25, spy + sy * (d_ / 2 + 0.25), spy + sy * (d_ / 2 + 3.25), ft, ft + 25)
    for sx in (-1, 1):
        floor += bx(spx + sx * 17 - 3, spx + sx * 17 + 3, spy - d_ / 2 + 0.25, spy + d_ / 2 - 0.25, ft, ft + p["sps_gap"])
    # NO2 sensor collar round a window in the floor
    bd, bh = p["b4"]
    nx, ny = p["no2_xy"]
    co, ch = p["collar"]
    floor += zcyl(nx, ny, ft + ch / 2, co / 2, ch) - zcyl(nx, ny, ft + ch / 2, bd / 2 + 0.3, ch + 1)
    floor -= zcyl(nx, ny, ft / 2, p["no2_window"] / 2, ft + 2)
    add("pod_floor", "Pod sensor floor", F * floor, 4, "made", "pod")
    mesh = bx(-W / 2 + 5, W / 2 - 5, -Dp / 2 + 5, Dp / 2 - 5, -p["mesh_t"], 0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            mesh -= zcyl(sx * bxs, sy * bys, -p["mesh_t"] / 2, 1.7, p["mesh_t"] + 2)
    add("mesh", "Stainless insect mesh", F * mesh, 4, "bought", "pod")
    fx = [zcyl(sx * bxs, sy * bys, -p["mesh_t"] - 1.2, 3.0, 2.4) + zcyl(sx * bxs, sy * bys, ft, 1.35, 2 * ft + 2 * p["mesh_t"] + 4)
          for sx in (-1, 1) for sy in (-1, 1)]
    add("floor_screws", "M3 screws, sensor floor (4)", F * fuse(fx), 11, "fixing", None)

    # 5 SPS30 on edge in its cradle, inlet face down
    zs0 = ft + p["sps_gap"]
    add("pm", "PM sensor (SPS30)", F * bx(spx - a_ / 2, spx + a_ / 2, spy - d_ / 2, spy + d_ / 2, zs0, zs0 + c_), 5, "bought", "pm")
    # 6 NO2 sensor in its collar, face down on the floor over the window
    add("no2", "NO2 sensor (B4 class)", F * zcyl(nx, ny, ft + bh / 2, bd / 2, bh), 6, "bought", "no2")
    # 7 front end and ADC board on four standoffs from the back wall, with its connector block
    yb_in = Dp / 2 - wt
    yb_board = yb_in - 4.0 - p["afe_standoff"]
    afe = bx(-afw / 2, afw / 2, yb_board - aft, yb_board, p["afe_z"], p["afe_z"] + afh)
    afe += bx(-25, 25, yb_board - aft - 8, yb_board - aft, p["afe_z"] + 17, p["afe_z"] + 39)
    so_ = [ycyl(sx * (afw / 2 - 5), yb_board + p["afe_standoff"] / 2, zz, 2.5, p["afe_standoff"])
           for sx in (-1, 1) for zz in (p["afe_z"] + 6, p["afe_z"] + afh - 6)]
    add("afe", "NO2 front end and ADC", F * afe, 7, "bought", "afe")
    add("afe_standoffs", "M3 standoffs, front end (4)", F * fuse(so_), 11, "fixing", None)
    # terminal block on the back wall, left of the board
    add("tblock", "Pod terminal block", F * bx(-W / 2 + wt + 6, -W / 2 + wt + 28, yb_in - 12, yb_in, 62, 76), 11, "bought", "afe")

    # pod hanging screws from above the arm
    fx = [screw_z_down(p["pod_x"] + dx, D["arm_y"], D["arm_z"] + at, at + 10.0) for dx in p["pod_hang_dx"]]
    add("pod_screws", "M5 screws, pod to arm (2)", fuse(fx), 11, "fixing", None)
    # roof glands and probe gland
    gl = []
    for x in gx:
        gl.append(zcyl(x, gy, H + lt + 6, 9.5, 12) + zcyl(x, gy, H + lt + 1, 12.0, 2) + zcyl(x, gy, H - wt / 2 + lt / 2, 8.0, wt + lt)
                  + hexprism("z", x, gy, H - wt - 2.5, 22.0, 5.0))
    gl.append(xcyl(W / 2 + 5, pgy, pgz, 5.0, 8) + xcyl(W / 2 + 1, pgy, pgz, 6.5, 2) + xcyl(W / 2 - wt / 2, pgy, pgz, 4.0, wt)
              + hexprism("x", W / 2 - wt - 1.5, pgy, pgz, 11.0, 3.0))
    add("pod_glands", "Pod glands (2 x M16, roof) and probe socket (M8, wall)", F * fuse(gl), 11, "bought", "pod")

    # ---------------------------------------------------------- 8 radiation shield
    so, si, stk, pitch, n = p["shield"]
    scx, scy = p["shield_x"], D["sh_yc"]
    rr = p["rod_r"]
    rods_xy = [(scx + rr * math.cos(math.radians(a)), scy + rr * math.sin(math.radians(a))) for a in (90, 210, 330)]
    plates = []
    for k in range(n):
        zc = D["sh_bot"] + k * pitch
        pl = zcyl(scx, scy, zc, so / 2, stk) - zcyl(scx, scy, zc, si / 2, stk + 2)
        for x, y in rods_xy:
            pl -= zcyl(x, y, zc, 2.75, stk + 2)
        plates.append(pl)
    add("shield_plates", "Shield plates (8)", fuse(plates), 8, "made", "shield")
    cz0 = D["sh_cap"]
    ct = p["cap"][1]
    cap = zcyl(scx, scy, cz0 + ct / 2, p["cap"][0] / 2, ct)
    cap -= zcyl(scx, scy, cz0 + ct / 2, p["th_tube"] / 2, ct + 2)
    for x, y in rods_xy:
        cap -= zcyl(x, y, cz0 + ct / 2, 2.75, ct + 2)
    for dx in p["cap_screw_dx"]:
        cap -= zcyl(scx + dx, scy, cz0 + ct - 4, 3.4, 8.1)                           # M5 insert from above
    add("shield_cap", "Shield cap", cap, 8, "made", "shield")
    top_plate = D["sh_bot"] + (n - 1) * pitch + stk / 2
    sp = []
    for x, y in rods_xy:
        for k in range(n - 1):
            z_a_ = D["sh_bot"] + k * pitch + stk / 2
            sp.append(zcyl(x, y, z_a_ + (pitch - stk) / 2, p["spacer_od"] / 2, pitch - stk))
        sp.append(zcyl(x, y, (top_plate + cz0) / 2, p["spacer_od"] / 2, cz0 - top_plate))
    add("spacers", "Shield spacers (24)", fuse(sp), 8, "made", "shield")
    z_rod0 = D["sh_bot"] - stk / 2 - 8
    z_rod1 = cz0 + ct + 7
    rods = fuse(zcyl(x, y, (z_rod0 + z_rod1) / 2, p["rod_d"] / 2 - 0.25, z_rod1 - z_rod0) for x, y in rods_xy)
    nuts = fuse(hexprism("z", x, y, cz0 + ct + 2.0, 8.0, 4.0) + b.Pos(x, y, D["sh_bot"] - stk / 2 - 4) * b.Box(8, 8, 8) for x, y in rods_xy)
    add("rods", "Shield rods, M5 (3), with nuts", rods + nuts, 8, "bought", "shield")
    fx = [screw_z_down(scx + dx, scy, D["arm_z"] + at, at + 7.0) for dx in p["cap_screw_dx"]]
    add("cap_screws", "M5 screws, cap to arm (2)", fuse(fx), 11, "fixing", None)

    # ---------------------------------------------------------- 9 T and RH probe on its tube
    tbx, tby, tbz = p["th_board"]
    thz = D["th_z"]
    tube_top = D["arm_z"] + at + 8
    probe = box(scx, scy, thz, tbx, tby, tbz) + zcyl(scx, scy, (thz + tbz / 2 + tube_top) / 2, p["th_tube"] / 2, tube_top - thz - tbz / 2)
    add("th", "T and RH probe (SHT45) on its tube", probe, 9, "bought", "th")

    # ---------------------------------------------------------- 10 cables
    cr = p["cable_d"] / 2
    pgd, pgl = p["plug"]
    port_bot = z0 - 22.0
    lid_top_abs = D["pod_bot"] + H + lt
    cab = None
    for x in (FP["pens"]["port_a"][0], FP["pens"]["port_b"][0]):
        y = D["whip_y"]
        c = zcyl(x, y, port_bot - pgl / 2, pgd / 2, pgl) + zcyl(x, y, (port_bot - pgl + lid_top_abs + 12) / 2, cr, port_bot - pgl - lid_top_abs - 12)
        cab = c if cab is None else cab + c
    pr = p["probe_cable_d"] / 2
    yA = D["arm_y"]
    xg = p["pod_x"] + W / 2 + 9 + 12    # the M8 plug body is 12 mm long
    zg = D["pod_bot"] + pgz
    lead = path_rod([(scx, scy, tube_top), (scx, scy, tube_top + 6), (scx - 30, yA, D["arm_z"] + at + pr),
                     (20.0, yA, D["arm_z"] + at + pr), (20.0, D["rail_front"] - al - 6, D["arm_z"] + at + pr),
                     (20.0, D["rail_front"] - al - 6, zg), (xg, D["pod_yc"] + pgy, zg)], pr)
    lead += xcyl(p["pod_x"] + W / 2 + 9 + 6, D["pod_yc"] + pgy, zg, 5.0, 12.0)      # M8 plug
    add("cables", "Sensor cables (2) and probe lead", cab + lead, 10, "bought", "cables")
    return C


def build_parts(p=PARAMS):
    """Return {BOM key: solid} for the BOM lines with geometry (line 11, fixings, is left out)."""
    C = build_components(p)
    out = {}
    for k, c in C.items():
        g = c.group
        if c.kind == "fieldnode":
            if c.group is None:
                continue
            g = "panel" if c.bom in (4, 5) else "fieldnode"
        if g:
            out[g] = c.shape if g not in out else out[g] + c.shape
    return out


def pole_stub(p=PARAMS, z_a=2800.0, z_b=3750.0):
    return zcyl(0, 0, (z_a + z_b) / 2, p["pole_od"] / 2, z_b - z_a)


def assembly(p=PARAMS, with_pole=True):
    b = _b()
    parts = build_parts(p)
    kids = list(parts.values()) + ([pole_stub(p)] if with_pole else [])
    return b.Compound(children=kids)


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm). Returns a list of
    (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p, shield=True)
    pole = pole_stub(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-3 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    box_ = S("fnd_body") + S("fnd_lid")
    for k in ("saddle_low", "saddle_up"):
        chk(f"{C[k].name} on the pole (both V faces)", S(k), pole, "touch")
        chk(f"{C[k].name} on the rail", S(k), S("rail"), "touch")
        chk(f"{C[k].name}: band in its groove", S(k), S("bands"), "touch")
    chk("Bands on the pole", S("bands"), pole, "touch")
    chk("Bands clear of the rail (held in the saddle grooves)", S("bands"), S("rail"), 0.5)
    chk("Saddle screws in the rail and saddles", S("saddle_screws"), S("rail") + S("saddle_low") + S("saddle_up"), "touch")
    for k in ("lplate", "uplate"):
        chk(f"{C[k].name} on the rail", S(k), S("rail"), "touch")
        chk(f"{C[k].name} clear of the saddles", S(k), S("saddle_low") + S("saddle_up"), 5.0)
        chk(f"Enclosure back on the {C[k].name.lower()}", box_, S(k), "touch")
        chk(f"Lugs on the {C[k].name.lower()}", S("fnd_lugs"), S(k), "touch")
    chk("Enclosure clear of the rail (sits on the plates)", box_, S("rail"), 2.0)
    chk("Lug screws clear of the rail", S("fnd_lug_screws"), S("rail"), 3.0)
    chk("Adapter plate bolts flush, clear of the enclosure", S("plate_bolts"), box_, 0.0)
    chk("Adapter plate bolts clear of the pole", S("plate_bolts"), pole, 3.0)
    for side in ("r", "l"):
        chk(f"Plate clip ({side}) on the upper adapter plate", S(f"fnd_plate_clip_{side}"), S("uplate"), "touch")
        chk(f"Plate clip ({side}) clear of the upper saddle", S(f"fnd_plate_clip_{side}"), S("saddle_up"), 5.0)
        chk(f"Post ({side}) clear of the upper adapter plate", S(f"fnd_post_{side}"), S("uplate"), 1.0)
        chk(f"Post ({side}) clear of the rail, saddle and band", S(f"fnd_post_{side}"), S("rail") + S("saddle_up") + S("bands"), 5.0)
    chk("Bracket bolts clear of the rail and saddles", S("fnd_bracket_bolts"), S("rail") + S("saddle_up"), 3.0)
    chk("Panel clear of the rail, saddle and bands", S("fnd_panel"), S("rail") + S("saddle_up") + S("bands"), 10.0)
    chk("Panel clear of the pole", S("fnd_panel"), pole, 5.0)
    chk("Shield flanges (hot sites) on both adapter plates", S("fnd_shield"), S("lplate") + S("uplate"), "touch")
    chk("Shield thumb screws in the plates", S("fnd_shield_screws"), S("lplate") + S("uplate"), "touch")
    chk("Shield clear of the rail and plate bolts", S("fnd_shield"), S("rail") + S("plate_bolts"), 2.0)
    chk("Cross arm on the rail", S("arm"), S("rail"), "touch")
    chk("Cross arm clear of the lower saddle and band", S("arm"), S("saddle_low") + S("bands"), 5.0)
    chk("Cross arm clear of the pole", S("arm"), pole, 5.0)
    chk("Cross arm bolts clear of the pole", S("arm_bolts"), pole, 3.0)
    chk("Cross arm clear of the enclosure, glands and ports", S("arm"), box_ + S("fnd_glands") + S("fnd_ports") + S("fnd_vent"), 20.0)
    chk("Pod shell hangs on the cross arm", S("pod_shell"), S("arm"), "touch")
    chk("Pod shell against the rail", S("pod_shell"), S("rail"), "touch")
    chk("Pod hanging screws through the arm into the pod", S("pod_screws"), S("arm") + S("pod_shell"), "touch")
    chk("Sensor floor under the pod shell", S("pod_floor"), S("pod_shell"), "touch")
    chk("Mesh under the sensor floor", S("mesh"), S("pod_floor"), "touch")
    chk("Floor screws clamp the mesh to the floor", S("floor_screws"), S("mesh"), "touch")
    chk("PM sensor in its cradle", S("pm"), S("pod_floor"), "touch")
    chk("PM sensor clear of the shell", S("pm"), S("pod_shell"), 2.0)
    chk("NO2 sensor in its collar", S("no2"), S("pod_floor"), "touch")
    chk("NO2 sensor clear of the front end", S("no2"), S("afe"), 2.0)
    chk("Front end on its standoffs", S("afe"), S("afe_standoffs"), "touch")
    chk("Standoffs on the back wall bosses", S("afe_standoffs"), S("pod_shell"), "touch")
    chk("Front end clear of the PM sensor and cradle", S("afe"), S("pm") + S("pod_floor"), 1.0)
    chk("Front end clear of the roof glands and bosses", S("afe"), S("pod_glands") + S("pod_shell"), 0.5)
    chk("Terminal block on the back wall", S("tblock"), S("pod_shell"), "touch")
    chk("Terminal block clear of the PM sensor and front end", S("tblock"), S("pm") + S("afe"), 2.0)
    chk("Pod glands in the roof and wall", S("pod_glands"), S("pod_shell"), "touch")
    chk("Pod glands clear of the arm", S("pod_glands"), S("arm"), 5.0)
    chk("Antenna whip clear of the pod", S("fnd_antenna"), S("pod_shell") + S("pod_glands"), 10.0)
    chk("Antenna whip clear of the arm and probe lead", S("fnd_antenna"), S("arm") + S("cables"), 5.0)
    chk("Pod clear of the enclosure, glands and ports", S("pod_shell"), box_ + S("fnd_glands") + S("fnd_ports") + S("fnd_vent"), 50.0)
    chk("Shield cap hangs on the cross arm", S("shield_cap"), S("arm"), "touch")
    chk("Cap screws through the arm into the cap", S("cap_screws"), S("arm") + S("shield_cap"), "touch")
    chk("Spacers between the plates and the cap", S("spacers"), S("shield_plates") + S("shield_cap"), "touch")
    chk("Rods through plates, spacers and cap", S("rods"), S("shield_plates"), "touch")
    chk("Probe clear of the shield plates", S("th"), S("shield_plates"), 10.0)
    chk("Probe tube through the cap", S("th"), S("shield_cap"), "touch")
    chk("Shield clear of the pole and band", S("shield_plates") + S("shield_cap"), pole + S("bands"), 20.0)
    chk("Shield clear of the pod", S("shield_plates") + S("shield_cap"), S("pod_shell"), 50.0)
    chk("Rod nuts clear of the arm", S("rods"), S("arm"), 0.5)
    chk("Sensor cables clear of the arm", S("cables"), S("arm"), 0.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def main():
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    C = build_components()
    head = [c.shape for k, c in C.items() if c.bom in (4, 5, 6, 7, 8, 9, 10) or k in ("pod_screws", "cap_screws", "floor_screws", "afe_standoffs", "tblock", "pod_glands")]
    mount = [C[k].shape for k in ("rail", "saddle_low", "saddle_up", "bands", "lplate", "uplate", "arm", "saddle_screws", "plate_bolts", "arm_bolts")]
    groups = {
        "airstreet-assembly": [c.shape for c in C.values()] + [pole_stub()],
        "airstreet-sensor-head": head,
        "airstreet-mount": mount,
    }
    for name, shapes in groups.items():
        comp = Compound(children=shapes)
        export_step(comp, str(root / "step" / f"{name}.step"))
        export_stl(comp, str(root / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = comp.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"inlet plane {PARAMS['inlet_z']:.0f} mm; overall node height {D['overall_h']:.0f} mm; "
          f"whip clearance to the pod lid {D['whip_clear']:.0f} mm; band {D['band_len']:.0f} mm round the 140 mm pole")
    print(f"V-saddle: apex {PARAMS['saddle_base']:.0f} mm from the rail, mouth {D['v_mouth']:.1f} mm; the design pole touches "
          f"{D['v_contact_lat']:.1f} mm each side of centre; a 200 mm pole touches {100 * math.cos(math.radians(70)):.1f} mm out")
    print_checks()


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    main()

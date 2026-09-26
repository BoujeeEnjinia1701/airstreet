"""AirStreet parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    airstreet-assembly.step / .stl     the whole node on a stub of its 140 mm design pole
    airstreet-sensor-head.step / .stl  pod, sensors, front end, radiation shield and cables
    airstreet-mount.step / .stl        rail, saddles, band clamps and shield arm

Axes: the street light pole is the Z axis (x = y = 0), Z is up with the sidewalk at z = 0,
and the node faces the street (-Y). The FieldNode core (FND, shared component) is modeled as
its interface envelope only: back plate, enclosure, bottom-face penetrations at the FieldNode
positions, antenna whip and the 6 W panel at its FieldNode tilt, all taken from FieldNode's
cad/src/model.py PARAMS (enclosure 150 x 90 x 200 mm, back plate 180 x 320 x 3 mm, panel
290 x 200 x 17 mm at 40 deg). AirStreet replaces FieldNode's V-blocks and 40 to 60 mm clamps with
its own rail, saddles and 80 to 200 mm band clamps. Main dimensions and interfaces only; not
fabrication detail; not for fabrication. The same PARAMS feed docs/04-calcs/sizing.py
(AST-CAL-001), the drawing AST-DWG-001 (cad/src/sheets.py) and cad/src/concept_media.py.
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site interface: pole on the Z axis; design case 140 mm OD at node height; fits 80 to 200 mm
    "pole_od": 140.0, "pole_range": (80.0, 200.0),
    # R11 inlet plane (underside of the pod mesh) above the sidewalk (DDR-001 D7: 3.0 m)
    "inlet_z": 3000.0,
    # 3 mount: V-saddle (W x H x min thickness), rail flat bar (W x t), rail ends, clamp heights
    "saddle": (60.0, 40.0, 16.0), "rail": (40.0, 5.0), "rail_z": (2980.0, 3545.0),
    "clamp_z": (3150.0, 3525.0), "band": (12.7, 1.5),        # band width; thickness drawn 1.5 (real 0.6)
    # 3 shield arm (W in Y x t in Z), height of its underside
    "arm": (20.0, 8.0), "arm_z": 3100.0,
    # 1 FieldNode core (FND model PARAMS): enclosure W x D x H, lid depth, bottom height, back plate
    "enc": (150.0, 90.0, 200.0), "lid_d": 12.0, "enc_z0": 3230.0,
    "plate": (180.0, 320.0, 3.0), "plate_drop": 40.0,
    "port_x": (-52.0, -22.0), "gland_x": (8.0, 34.0), "ant_x": 58.0,
    "m12_d": (16.0, 22.0), "m16_d": (20.0, 24.0), "whip": (10.0, 190.0),
    # 2 FieldNode panel: size, tilt, center (in front of the plate rear face, above enc_z0); bracket bar
    "panel": (290.0, 200.0, 17.0), "tilt": 40.0, "panel_c": (73.0, 385.0),
    "bar": (25.0, 3.0), "bracket_x": 80.0, "post_ly": 80.0, "strut_ly": -60.0,
    "post_foot_dz": 260.0, "strut_foot_dz": 210.0,
    # 4 sensor pod: W x D x H, wall, drip lid overhang and thickness, center x (clear of the whip)
    "pod": (170.0, 110.0, 95.0), "pod_wall": 3.0, "lid": (15.0, 3.0), "pod_x": -70.0,
    "slot": (50.0, 60.0),                                    # two inlet slots in the floor
    # 5 PM sensor SPS30 (41 x 41 x 12 mm, datasheet); 6 NO2 sensor B4 (dia x height, assumed)
    "sps30": (41.0, 41.0, 12.0), "b4": (32.0, 20.0),
    # 7 front end and ADC board (W x t x H)
    "afe": (100.0, 3.0, 55.0),
    # 8 radiation shield: plate OD, ID, thickness, pitch, count, cap OD and thickness, center x, rods
    "shield": (120.0, 56.0, 2.0, 13.0, 8), "cap": (124.0, 4.0), "shield_x": 200.0, "rod_d": 5.0,
    # 9 temperature and humidity probe: board, stem
    "th_board": (14.0, 10.0, 4.0), "th_stem": (6.0, 56.0),
    # 10 cables: diameter, M12 plug (dia x length)
    "cable_d": 6.0, "plug": (16.0, 45.0),
}

BOM = {  # model key: (BOM line, name)
    "fieldnode": (1, "FieldNode core (enclosure, cell, radio)"),
    "panel": (2, "FieldNode 6 W panel hood"),
    "mount": (3, "Band clamps, saddles, rail and shield arm"),
    "pod": (4, "Sensor pod with mesh and drip lid"),
    "pm": (5, "Optical PM sensor (SPS30 class)"),
    "no2": (6, "Electrochemical NO2 sensor (B4 class)"),
    "afe": (7, "NO2 front end and 16-bit ADC"),
    "shield": (8, "Multi-plate radiation shield"),
    "th": (9, "Temperature and humidity sensor"),
    "cables": (10, "Sensor cables, M12"),
}


def derived(p=PARAMS):
    """Dimensions the calc note and the drawing quote, computed from PARAMS."""
    R = p["pole_od"] / 2
    sw, sh, st = p["saddle"]
    rw, rt = p["rail"]
    rail_back = -(R + st)
    rail_front = rail_back - rt
    pw, pl, pt = p["plate"]
    plate_front = rail_front - pt
    ew, ed, eh = p["enc"]
    enc_front = plate_front - ed
    z0 = p["enc_z0"]
    t = math.radians(p["tilt"])
    pcy, pcz = rail_front - p["panel_c"][0], z0 + p["panel_c"][1]
    half = p["panel"][1] / 2
    podw, podd, podh = p["pod"]
    pod_back = rail_front
    pod_yc = pod_back - podd / 2
    pod_bot = p["inlet_z"]
    pod_top = pod_bot + podh
    so, si, stk, pitch, n = p["shield"]
    sh_bot = p["inlet_z"] - 10.0
    sh_cap = sh_bot + n * pitch
    panel_top = pcz + half * math.sin(t) + p["panel"][2] / 2 * math.cos(t)
    return {
        "R": R, "rail_back": rail_back, "rail_front": rail_front, "plate_front": plate_front,
        "enc_front": enc_front, "enc_yc": (plate_front + enc_front) / 2, "enc_top": z0 + eh,
        "plate_bot": z0 - p["plate_drop"], "plate_top": z0 - p["plate_drop"] + pl,
        "panel_cy": pcy, "panel_cz": pcz, "panel_top": panel_top,
        "pod_back": pod_back, "pod_yc": pod_yc, "pod_bot": pod_bot, "pod_top": pod_top,
        "lid_top": pod_top + p["lid"][1],
        "whip_bot": z0 - 16.0 - p["whip"][1],
        "sh_bot": sh_bot, "sh_cap": sh_cap, "sh_yc": pod_yc,
        "th_z": sh_bot + n * pitch / 2 - 10.0,
        "clamp_span": p["clamp_z"][1] - p["clamp_z"][0],
        "rail_len": p["rail_z"][1] - p["rail_z"][0],
        "arm_len": p["shield_x"] + so / 2 * 0.4 - 15.0,
        "overall_h": panel_top - p["rail_z"][0],
        "whip_clear": p["ant_x"] - p["whip"][0] / 2 - (p["pod_x"] + podw / 2 + p["lid"][0]),
        "offset_front": -min(enc_front, pcy - half * math.cos(t) - p["panel"][2] / 2 * math.sin(t), pod_yc - podd / 2 - p["lid"][0]) - R,
    }


def _b():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def zcyl(x, y, z, r, h):
    b = _b()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def rod(a, c, r):
    """Solid rod of radius r between two 3D points."""
    b = _b()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def bar(a, c, w, t):
    """Flat bar w (along X) by t between two points in a plane x = const."""
    b = _b()
    dy, dz = c[1] - a[1], c[2] - a[2]
    L = math.hypot(dy, dz)
    ang = math.degrees(math.atan2(-dy, dz))
    return b.Pos(a[0], (a[1] + c[1]) / 2, (a[2] + c[2]) / 2) * b.Rot(ang, 0, 0) * b.Box(w, t, L)


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def build_parts(p=PARAMS):
    """Return {key: solid} for BOM lines 1 to 10 (line 11, fasteners, is not modeled)."""
    b = _b()
    D = derived(p)
    R = p["pole_od"] / 2
    parts = {}

    # 3 Mount: two V-saddles on the pole face, rail, band clamps, shield arm and its gusset
    sw, sh, st = p["saddle"]
    rw, rt = p["rail"]
    z_a, z_b = p["rail_z"]
    saddles = fuse(box(0, -(2 * R + st - 20) / 2, z, sw, st + 20, sh) - zcyl(0, 0, z, R, sh + 2)
                   for z in p["clamp_z"])
    rail = box(0, D["rail_back"] - rt / 2, (z_a + z_b) / 2, rw, rt, z_b - z_a)
    bw, bt = p["band"]
    bands = None
    for z in p["clamp_z"]:
        ring = zcyl(0, 0, z, R + bt, bw) - zcyl(0, 0, z, R, bw + 2)
        strap = box(0, D["rail_front"] - bt / 2, z, rw + 12, bt, bw)
        sides = fuse(box(sx * (rw / 2 + 6 - bt / 2), (D["rail_front"] - R * 0.35) / 2, z, bt,
                         abs(D["rail_front"]) - R * 0.35, bw) for sx in (-1, 1))
        screw = box(rw / 2 + 14, D["rail_front"] + 6, z, 16, 12, bw + 4)
        c = ring + strap + sides + screw
        bands = c if bands is None else bands + c
    aw, at = p["arm"]
    so = p["shield"][0]
    x_arm0, x_arm1 = 15.0, p["shield_x"] + so * 0.2
    arm = box((x_arm0 + x_arm1) / 2, D["pod_yc"], p["arm_z"] + at / 2, x_arm1 - x_arm0, aw, at)
    gusset = box(rw / 2 + 5, (D["rail_front"] + D["pod_yc"] - aw / 2) / 2, p["arm_z"] + at / 2,
                 10, D["rail_front"] - D["pod_yc"] + aw / 2, at)
    parts["mount"] = saddles + rail + bands + arm + gusset

    # 1 FieldNode core envelope: back plate, enclosure with lid line, bottom-face penetrations, whip
    pw, pl, pt = p["plate"]
    plate = box(0, D["rail_front"] - pt / 2, (D["plate_bot"] + D["plate_top"]) / 2, pw, pt, pl)
    ew, ed, eh = p["enc"]
    z0 = p["enc_z0"]
    body = box(0, D["plate_front"] - (ed - p["lid_d"]) / 2, z0 + eh / 2, ew, ed - p["lid_d"], eh)
    lid = box(0, D["enc_front"] + p["lid_d"] / 2, z0 + eh / 2, ew - 2, p["lid_d"], eh - 2)
    yc = D["enc_yc"]
    pens = fuse([zcyl(x, yc, z0 - 8, p["m12_d"][1] / 2, 16) for x in p["port_x"]]
                + [zcyl(x, yc, z0 - 9, p["m16_d"][1] / 2, 18) for x in p["gland_x"]]
                + [zcyl(p["ant_x"], yc, z0 - 8, 7, 16)])
    whip = zcyl(p["ant_x"], yc, z0 - 16 - p["whip"][1] / 2, p["whip"][0] / 2, p["whip"][1])
    parts["fieldnode"] = plate + body + lid + pens + whip

    # 2 FieldNode panel on its flat-bar bracket (posts and struts from the back plate)
    t = math.radians(p["tilt"])
    pcy, pcz = D["panel_cy"], D["panel_cz"]
    panel = b.Pos(0, pcy, pcz) * b.Rot(p["tilt"], 0, 0) * b.Box(*p["panel"])
    th = p["panel"][2]

    def under(s):  # point on the panel underside at slope coordinate s (toward +Y is up the slope)
        return (pcy + s * math.cos(t) + th / 2 * math.sin(t), pcz + s * math.sin(t) - th / 2 * math.cos(t))
    bw_, bt_ = p["bar"]
    brk = None
    for sx in (-1, 1):
        x = sx * p["bracket_x"]
        for s, dz in ((p["post_ly"], p["post_foot_dz"]), (p["strut_ly"], p["strut_foot_dz"])):
            uy, uz = under(s)
            m = bar((x, D["plate_front"] - bt_ / 2, z0 + dz), (x, uy, uz), bw_, bt_)
            brk = m if brk is None else brk + m
    parts["panel"] = panel + brk

    # 4 Sensor pod: shell open underneath behind mesh, floor with two inlet slots, drip lid
    W, Dp, H = p["pod"]
    wt = p["pod_wall"]
    px, py, pz = p["pod_x"], D["pod_yc"], p["inlet_z"] + H / 2
    shell = b.Box(W, Dp, H) - b.Pos(0, 0, -wt) * b.Box(W - 2 * wt, Dp - 2 * wt, H)
    slots = fuse(b.Pos(dx, 0, -H / 2 + wt / 2) * b.Box(p["slot"][0], p["slot"][1], wt + 2) for dx in (-45, 45))
    floor = b.Pos(0, 0, -H / 2 + wt / 2) * b.Box(W, Dp, wt) - slots
    mesh = b.Pos(0, 0, -H / 2 - 0.5) * b.Box(W - 10, Dp - 10, 1.0)
    ov, lt = p["lid"]
    drip = b.Pos(0, 0, H / 2 + lt / 2) * b.Box(W + 2 * ov, Dp + 2 * ov, lt)
    parts["pod"] = b.Pos(px, py, pz) * (shell + floor + mesh + drip)

    # 5 SPS30 standing on edge, inlet facing down over the left slot
    a, c_, d = p["sps30"]
    zf = p["inlet_z"] + wt
    parts["pm"] = box(px - 45, py + 20, zf + 8 + a / 2, a, d, c_) + box(px - 45, py + 20, zf + 4, 14, 10, 8)
    # 6 NO2 sensor, face down over the right slot
    bd, bh = p["b4"]
    parts["no2"] = zcyl(px + 45, py + 20, zf + 8 + bh / 2, bd / 2, bh)
    # 7 front end and ADC board standing at the back of the pod
    fw, ft, fh = p["afe"]
    parts["afe"] = (box(px, py + Dp / 2 - wt - 4, pz + 5, fw, ft, fh)
                    + box(px, py + Dp / 2 - wt - 9, pz + 5, 50, 7, 22))

    # 8 radiation shield under the arm: plates, cap, three rods
    so, si, stk, pitch, n = p["shield"]
    sx0, sy0 = p["shield_x"], D["sh_yc"]
    plates = fuse(zcyl(sx0, sy0, D["sh_bot"] + k * pitch, so / 2, stk) - zcyl(sx0, sy0, D["sh_bot"] + k * pitch, si / 2, stk + 2)
                  for k in range(n))
    cap = zcyl(sx0, sy0, D["sh_cap"] + p["cap"][1] / 2, p["cap"][0] / 2, p["cap"][1])
    rod_top = p["arm_z"]
    rods = fuse(rod((sx0 + dx, sy0 + dy, D["sh_bot"] - 3), (sx0 + dx, sy0 + dy, rod_top), p["rod_d"] / 2)
                for dx, dy in ((42, 0), (-21, 36), (-21, -36)))
    parts["shield"] = plates + cap + rods

    # 9 T and RH probe hanging from the cap into the shield center
    tbx, tby, tbz = p["th_board"]
    sd, sl = p["th_stem"]
    parts["th"] = box(sx0, sy0, D["th_z"], tbx, tby, tbz) + zcyl(sx0, sy0, D["th_z"] + tbz / 2 + sl / 2, sd / 2, sl)

    # 10 cables: two from the FieldNode M12 ports down into the pod lid; the probe cable along the arm
    cr = p["cable_d"] / 2
    pgd, pgl = p["plug"]
    cab = None
    for x in p["port_x"]:
        top = z0 - 16
        c = zcyl(x, yc, top - pgl / 2, pgd / 2, pgl) + rod((x, yc, top - pgl), (x, py, D["lid_top"]), cr)
        cab = c if cab is None else cab + c
    zc = p["arm_z"] + p["arm"][1] + cr
    probe = (rod((sx0, sy0, D["th_z"] + tbz / 2 + sl), (sx0, sy0, zc), cr)
             + rod((sx0, sy0, zc), (px + W / 2 - 10, sy0, zc), cr)
             + rod((px + W / 2 - 10, sy0, zc), (px + W / 2 - 10, sy0, D["lid_top"]), cr))
    parts["cables"] = cab + probe
    return parts


def pole_stub(p=PARAMS, z_a=2800.0, z_b=3750.0):
    return zcyl(0, 0, (z_a + z_b) / 2, p["pole_od"] / 2, z_b - z_a)


def assembly(p=PARAMS, with_pole=True):
    b = _b()
    parts = build_parts(p)
    kids = list(parts.values()) + ([pole_stub(p)] if with_pole else [])
    return b.Compound(children=kids)


def main():
    b = _b()
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    groups = {
        "airstreet-assembly": list(parts.values()) + [pole_stub()],
        "airstreet-sensor-head": [parts[k] for k in ("pod", "pm", "no2", "afe", "shield", "th", "cables")],
        "airstreet-mount": [parts["mount"]],
    }
    for name, shapes in groups.items():
        comp = b.Compound(children=shapes)
        b.export_step(comp, str(root / "step" / f"{name}.step"))
        b.export_stl(comp, str(root / "stl" / f"{name}.stl"))
        bb = comp.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"inlet plane {PARAMS['inlet_z']:.0f} mm; overall node height {D['overall_h']:.0f} mm; "
          f"whip clearance to pod lid {D['whip_clear']:.0f} mm")


if __name__ == "__main__":
    main()

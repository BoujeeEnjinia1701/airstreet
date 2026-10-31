"""Option A (the current AirStreet design, AST-DDR-003) as kit 1.9 detailed parts (STANDARDS section 24, D3).

Every component of model.build_components() becomes the parts a maker cuts, prints, buys and fits: each band
and its worm housing, each screw, bolt, nyloc nut, washer and brass heat-set insert, each shield plate, spacer,
rod and nut, the two roof glands with their locknuts and the probe socket, the bought modules with their real
features (the particle sensor's inlet and connector, the NO2 sensor's filter face and pins, the front end board
with its holes, chips and terminal block, the probe board with its filter cap), and FieldNode's own parts as
FieldNode models them (vendored copy, cad/src/fieldnode_core.py), with its fixings split piece by piece.
No design dimension changes here: positions and sizes come from PARAMS and derived() in model.py.

    import model; parts = model.components("A")
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

import build123d as b  # noqa: E402
import cad_parts as cp  # noqa: E402
import ast_parts as ap  # noqa: E402

WHITE = "#ECECEA"        # printed ASA, off-white
DARK = "#2B2F36"         # printed ASA, dark (saddles)
PCB = "#1F5135"
FND_GREY = "#DADDE1"

# FieldNode component key -> (material, kind, AirStreet BOM line, colour)
FND_MAT = {
    "body": ("hdpe_natural", "bought", 1, FND_GREY), "lid": ("hdpe_natural", "bought", 1, "#E6E8EB"),
    "lugs": ("hdpe_natural", "bought", 1, FND_GREY), "lug_screws": ("stainless", "fastener", 11, None),
    "glands": ("hdpe_black", "bought", 1, None), "ports": ("brass", "bought", 1, "#9CA3AB"),
    "vent": ("hdpe_black", "bought", 1, None), "antenna": ("matte_black", "bought", 1, None),
    "mplate": ("aluminium", "made", 1, None), "mplate_screws": ("stainless", "fastener", 11, None),
    "cell": ("hdpe_black", "bought", 1, "#2563EB"), "power": ("hdpe_recycled", "bought", 1, PCB),
    "ctrl": ("hdpe_recycled", "bought", 1, PCB), "connectors": ("hdpe_black", "bought", 1, "#15803D"),
    "plate_clip_r": ("aluminium", "made", 2, None), "plate_clip_l": ("aluminium", "made", 2, None),
    "post_r": ("aluminium", "made", 2, None), "post_l": ("aluminium", "made", 2, None),
    "strut_r": ("aluminium", "made", 2, None), "strut_l": ("aluminium", "made", 2, None),
    "high_panel_clip_r": ("aluminium", "made", 2, None), "high_panel_clip_l": ("aluminium", "made", 2, None),
    "low_panel_clip_r": ("aluminium", "made", 2, None), "low_panel_clip_l": ("aluminium", "made", 2, None),
    "bracket_bolts": ("stainless", "fastener", 11, None), "panel": ("matte_black", "bought", 2, "#1E293B"),
    "panel_bolts": ("stainless", "fastener", 11, None),
}
FND_PIECE = {"lugs": "Enclosure lug", "lug_screws": "M5 screw and nut, enclosure lug", "glands": "Cable gland M16, FieldNode",
             "ports": "Sensor port M12, FieldNode", "mplate_screws": "M4 screw, internal plate",
             "bracket_bolts": "Bolt and nut, panel bracket", "panel_bolts": "M4 bolt and nut, panel clip"}
FND_GROUP = {"panel": "panel", "plate_clip_r": "panel", "plate_clip_l": "panel", "post_r": "panel", "post_l": "panel",
             "strut_r": "panel", "strut_l": "panel", "high_panel_clip_r": "panel", "high_panel_clip_l": "panel",
             "low_panel_clip_r": "panel", "low_panel_clip_l": "panel", "bracket_bolts": "panel", "panel_bolts": "panel",
             "cell": "internal", "power": "internal", "ctrl": "internal", "connectors": "internal", "mplate": "internal",
             "mplate_screws": "internal"}


def _p(name, shape, mat, kind, bom, group, color=None, explode=(0, 0, 0)):
    shape = ap.solid(shape)
    if kind in ("made", "bought"):
        try:
            f = shape.faces()
            if len(f) == 3 or (len(f) == 6 and all(str(x.geom_type).endswith("PLANE") for x in f)):
                shape = cp.break_edges(shape, 0.8)
        except Exception:
            pass
    return cp.part(name, shape, mat, kind=kind, bom=bom if kind != "context" else None, group=group, color=color,
                   explode=explode)


def _solids(shape):
    try:
        s = list(shape.solids())
        return s if s else [shape]
    except Exception:
        return [shape]


def _soften(shape, r):
    """Edge break on a made part; returns the part unchanged where the fillet fails."""
    out = cp.break_edges(shape, r)
    return out


def option_a(P=None):
    import model as M
    P = P or M.PARAMS
    FP = M.FP
    D = M.derived(P)
    C = M.build_components(P)
    out = []
    add = out.append

    yrb, yrf = D["rail_back"], D["rail_front"]
    rw, rt = P["rail"]
    pt = P["plate_t"]
    al, at = P["arm"]
    z0 = P["enc_z0"]
    R = D["R"]

    # ------------------------------------------------------------------ 3 mount
    for k in ("saddle_low", "saddle_up"):
        add(_p(C[k].name, C[k].shape, "hdpe_black", "made", 3, "mount", DARK, (0, 120, 0)))
    add(_p("Rail, 40 x 4 mm aluminium flat bar", _soften(C["rail"].shape, 0.5), "aluminium", "made", 3, "mount", None, (0, 90, 0)))
    for k in ("lplate", "uplate"):
        add(_p(C[k].name, C[k].shape, "aluminium", "made", 3, "mount", None, (0, -40, 0)))
    add(_p("Cross arm, 30 x 30 x 3 mm aluminium angle", _soften(C["arm"].shape, 0.4), "aluminium", "made", 3, "mount", None, (0, -60, -40)))

    # bands: each a stainless band round the pole and through its saddle groove, with a worm housing
    bw, bt = P["band"]
    sw = P["saddle"][0]
    gd = P["groove"][1]
    for i, zc in enumerate(P["clamp_z"]):
        yg = yrb + gd
        inner = b.make_hull(b.Circle(R).edges() + b.Polyline((-sw / 2, yg), (sw / 2, yg)).edges())
        outer = b.offset(inner, bt, kind=b.Kind.ARC)
        ring = b.Pos(0, 0, zc - bw / 2) * (b.extrude(outer, bw) - b.extrude(inner, bw))
        lvl = "lower" if i == 0 else "upper"
        add(_p(f"Band, 12.7 mm stainless, {lvl} clamp", ring, "stainless", "bought", 3, "mount", None, (0, 160, 0)))
        ang = math.radians(35.0)
        house = b.Pos((R + bt) * math.cos(ang), (R + bt) * math.sin(ang), zc) * b.Rot(0, 0, math.degrees(ang) - 90) * ap.worm_housing(bw)
        add(_p(f"Worm-drive housing and screw, {lvl} clamp", house, "stainless", "bought", 3, "mount", None, (0, 160, 0)))

    # saddle screws (countersunk, from the rail front into brass inserts in the saddles)
    for zc in P["clamp_z"]:
        for sx, dzs in P["saddle_screws"]:
            z = zc + dzs
            add(_p("M5 x 14 countersunk screw, saddle", ap.place(ap.csk_screw(5, 14), (sx, yrf, z), "y", 1),
                   "stainless", "fastener", 11, "mount"))
            add(_p("M5 brass heat-set insert, saddle", ap.place(ap.insert(5), (sx, yrb + 0.5, z), "y", 1),
                   "brass", "fastener", 11, "mount"))
    # adapter plate bolts: countersunk from the plate front, nyloc nut behind the rail
    for dzb in P["lplate_bolts"] + P["uplate_bolts"]:
        z = z0 + dzb
        add(_p("M5 x 14 countersunk screw, adapter plate", ap.place(ap.csk_screw(5, 14), (0, yrf - pt, z), "y", 1),
               "stainless", "fastener", 11, "mount"))
        add(_p("M5 nyloc nut, adapter plate", b.Pos(0, yrb, z) * b.Rot(-90, 0, 0) * ap.nyloc_nut(5),
               "stainless", "fastener", 11, "mount"))
    # cross arm bolts: button head behind the rail, washer and nyloc nut in front of the arm's upright leg
    arm_bz = D["arm_z"] + at + (al - at) / 2
    for x in P["arm_bolt_x"]:
        add(_p("M5 x 14 button head screw, cross arm", ap.place(ap.button_screw(5, 14), (x, yrb, arm_bz), "y", -1),
               "stainless", "fastener", 11, "mount"))
        add(_p("M5 washer, cross arm", b.Pos(x, yrf - at, arm_bz) * b.Rot(90, 0, 0) * ap.washer_small(5),
               "stainless", "fastener", 11, "mount"))
        add(_p("M5 nyloc nut, cross arm", b.Pos(x, yrf - at - 1.0, arm_bz) * b.Rot(90, 0, 0) * ap.nyloc_nut(5),
               "stainless", "fastener", 11, "mount"))

    # ------------------------------------------------------------------ 1, 2 FieldNode core (its own parts)
    for k, c in C.items():
        if not k.startswith("fnd_"):
            continue
        key = k[4:]
        mat, kind, bom, col = FND_MAT[key]
        grp = FND_GROUP.get(key, "fieldnode")
        ex = (0, -80, 260) if grp == "panel" else ((0, -40, 120) if grp != "internal" else (0, -120, 140))
        sols = _solids(c.shape)
        if key in FND_PIECE and len(sols) > 1:
            for j, s in enumerate(sols, 1):
                add(_p(f"{FND_PIECE[key]} ({j})", s, mat, kind, bom, grp, col, ex))
        else:
            add(_p(c.name, c.shape, mat, kind, bom, grp, col, ex))

    # ------------------------------------------------------------------ 4 sensor pod
    F = M.pod_frame(P)
    W, Dp, H = P["pod"]
    wt = P["pod_wall"]
    ov, lt = P["lid"]
    ft = wt
    exp_pod = (0, -140, -220)
    add(_p("Pod shell (walls, roof and drip lid)", C["pod_shell"].shape, "pe_tank_white", "made", 4, "pod", WHITE, exp_pod))
    add(_p("Pod sensor floor", C["pod_floor"].shape, "pe_tank_white", "made", 4, "pod", "#D9D9D6", (0, -140, -320)))
    add(_p("Stainless insect mesh (drawn as a sheet)", C["mesh"].shape, "stainless", "bought", 4, "pod", None, (0, -140, -360)))
    bxs, bys = W / 2 - wt - 4, Dp / 2 - wt - 4
    for sx in (-1, 1):
        for sy in (-1, 1):
            add(_p("M3 x 8 pan head screw, sensor floor", F * ap.place(ap.pan_screw(3, 8), (sx * bxs, sy * bys, -P["mesh_t"] - 0.5), "z", 1),
                   "stainless", "fastener", 11, "pod"))
            add(_p("M3 washer, sensor floor", F * (b.Pos(sx * bxs, sy * bys, -P["mesh_t"]) * b.Rot(180, 0, 0) * ap.washer_small(3)),
                   "stainless", "fastener", 11, "pod"))
            add(_p("M3 brass heat-set insert, pod shell", F * ap.place(ap.insert(3), (sx * bxs, sy * bys, ft + 0.5), "z", 1),
                   "brass", "fastener", 11, "pod"))
    hy = D["arm_y"] - D["pod_yc"]
    for dx in P["pod_hang_dx"]:
        add(_p("M5 brass heat-set insert, pod hanging boss", F * ap.place(ap.insert(5), (dx, hy, H + lt - 1.0), "z", -1),
               "brass", "fastener", 11, "pod"))
        x_abs = P["pod_x"] + dx
        add(_p("M5 x 12 pan head screw, pod to cross arm", ap.place(ap.pan_screw(5, 12), (x_abs, D["arm_y"], D["arm_z"] + at + 1.0), "z", -1),
               "stainless", "fastener", 11, "pod"))
        add(_p("M5 washer, pod screw", b.Pos(x_abs, D["arm_y"], D["arm_z"] + at) * ap.washer_small(5), "stainless", "fastener", 11, "pod"))

    # 5 particle sensor: body with inlet recess, outlet grille, connector
    a_, c_, d_ = P["sps30"]
    spx, spy = P["sps_xy"]
    zs0 = ft + P["sps_gap"]
    body = ap.rounded_box(spx - a_ / 2, spx + a_ / 2, spy - d_ / 2, spy + d_ / 2, zs0, zs0 + c_, 1.0)
    body -= b.Pos(spx, spy, zs0 + 0.75) * b.Box(18, 6, 1.5)                                  # inlet recess
    for k in range(4):
        body -= b.Pos(spx - 12 + 8 * k, spy - d_ / 2 + 0.5, zs0 + 30) * b.Box(2.5, 1.0, 12)      # outlet grille
    body += b.Pos(spx, spy, zs0 + c_ + 2) * b.Box(10, 5, 4) - b.Pos(spx, spy, zs0 + c_ + 3) * b.Box(8, 3, 2.1)
    add(_p("Particle sensor (SPS30)", F * body, "matte_black", "bought", 5, "pod", "#3F3F46", (-120, -200, -420)))

    # 6 NO2 sensor: body, filter face, four pins
    bd, bh = P["b4"]
    nx, ny = P["no2_xy"]
    nb = b.Pos(nx, ny, ft + 8.25) * b.Cylinder(bd / 2, 16.5)
    try:
        nb = b.chamfer(nb.edges().sort_by(b.Axis.Z)[-1], 0.8)
    except Exception:
        pass
    nb -= b.Pos(nx, ny, ft + 0.3) * b.Cylinder(10.0, 0.6)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        nb += b.Pos(nx + 8 * math.cos(a), ny + 8 * math.sin(a), ft + 16.5 + 1.75) * b.Cylinder(0.8, 3.5)
    add(_p("NO2 sensor (NO2-B43F class)", F * nb, "stainless", "bought", 6, "pod", "#B0B4B8", (120, -200, -420)))

    # 7 front end and ADC: board with holes, chips, sensor connector and terminal block, on four standoffs
    afw, aft, afh = P["afe"]
    yb_in = Dp / 2 - wt
    yb_board = yb_in - 4.0 - P["afe_standoff"]
    zc_b = P["afe_z"] + afh / 2
    hx = afw / 2 - 5
    hz = (P["afe_z"] + 6 - zc_b, P["afe_z"] + afh - 6 - zc_b)
    holes = [(sx * hx, z, 3.2) for sx in (-1, 1) for z in hz]
    comps = [(0, P["afe_z"] + 28 - zc_b, 50, 22, 6.4),     # terminal block
             (28, -16, 9, 7, 1.4), (-28, -16, 7, 7, 1.4), (-30, 18, 5, 3, 2.5), (30, 18, 5, 3, 2.5)]
    board = ap.pcb(afw, afh, 1.6, holes, comps)
    add(_p("NO2 front end and 16-bit ADC board", F * (b.Pos(0, yb_board, zc_b) * board), "hdpe_recycled", "bought", 7, "pod", PCB, (0, 80, 160)))
    for sx in (-1, 1):
        for z in hz:
            pos = (sx * hx, yb_board, zc_b + z)
            add(_p("M3 x 6 hex standoff, front end", F * (b.Pos(*pos) * b.Rot(90, 0, 0) * ap.standoff(3, P["afe_standoff"], stub=3.5)),
                   "brass", "fastener", 11, "pod"))
            add(_p("M3 x 5 pan head screw, front end", F * ap.place(ap.pan_screw(3, 5), (pos[0], yb_board - 1.6, pos[2]), "y", 1),
                   "stainless", "fastener", 11, "pod"))
            add(_p("M3 brass heat-set insert, pod back wall", F * ap.place(ap.insert(3, 4.0), (pos[0], yb_in, pos[2]), "y", -1),
                   "brass", "fastener", 11, "pod"))
    # terminal block on the back wall
    tb = ap.rounded_box(-W / 2 + wt + 6, -W / 2 + wt + 28, yb_in - 12, yb_in, 62, 76, 0.6)
    for k in range(4):
        x = -W / 2 + wt + 8.75 + 5.5 * k
        tb -= b.Pos(x, yb_in - 12, 72) * b.Rot(90, 0, 0) * b.Cylinder(1.4, 6)
        tb -= b.Pos(x, yb_in - 6, 76) * b.Box(3.0, 3.0, 6)
    add(_p("Pod terminal block, 4-way", F * tb, "hdpe_black", "bought", 11, "pod", "#4B5563", (0, 60, 100)))

    # glands in the roof (2 x M16 with locknuts) and the M8 probe socket in the right wall
    gx = [x - P["pod_x"] for x in (FP["pens"]["port_a"][0], FP["pens"]["port_b"][0])]
    gy = D["whip_y"] - D["pod_yc"]
    for j, x in enumerate(gx, 1):
        add(_p(f"Cable gland M16, pod roof ({j})", F * (b.Pos(x, gy, H + lt) * ap.gland(16, P["cable_d"])), "hdpe_black", "bought", 11, "pod", None, exp_pod))
        add(_p(f"Gland locknut M16, pod roof ({j})", F * (b.Pos(x, gy, H - wt) * ap.locknut(16, 4.0)), "hdpe_black", "fastener", 11, "pod"))
    pgy, pgz = 10.0, 49.0
    sock = (b.Pos(W / 2 + 1, pgy, pgz) * b.Rot(0, 90, 0) * b.extrude(b.RegularPolygon(11.0 / math.sqrt(3), 6), 1.0, both=True)
            + b.Pos(W / 2 + 5.5, pgy, pgz) * b.Rot(0, 90, 0) * (b.Cylinder(4.0, 7.0) - b.Cylinder(2.5, 7.5))
            + b.Pos(W / 2 - wt / 2, pgy, pgz) * b.Rot(0, 90, 0) * b.Cylinder(4.0, wt))
    add(_p("M8 4-pin panel socket, probe lead", F * sock, "brass", "bought", 11, "pod", "#9CA3AB", exp_pod))
    add(_p("M8 socket nut", F * (b.Pos(W / 2 - wt - 1.5, pgy, pgz) * b.Rot(0, 90, 0) * ap.hex_nut_small(4, 3.0).moved(b.Location((0, 0, -1.5)))),
           "brass", "fastener", 11, "pod"))

    # ------------------------------------------------------------------ 8 radiation shield
    so, si, stk, pitch, n = P["shield"]
    scx, scy = P["shield_x"], D["sh_yc"]
    exp_sh = (260, -60, 60)
    for j, s in enumerate(_solids(C["shield_plates"].shape), 1):
        add(_p(f"Shield plate {j}, 1.5 mm printed ASA", s, "pe_tank_white", "made", 8, "shield", "#F2F2EF", exp_sh))
    add(_p("Shield cap", C["shield_cap"].shape, "pe_tank_white", "made", 8, "shield", "#F2F2EF", exp_sh))
    for j, s in enumerate(_solids(C["spacers"].shape), 1):
        add(_p(f"Shield spacer {j}", s, "pe_tank_white", "made", 8, "shield", "#F2F2EF", exp_sh))
    rr = P["rod_r"]
    rods_xy = [(scx + rr * math.cos(math.radians(a)), scy + rr * math.sin(math.radians(a))) for a in (90, 210, 330)]
    cz0, ct = D["sh_cap"], P["cap"][1]
    z_pb = D["sh_bot"] - stk / 2
    z_rod0, z_rod1 = z_pb - 8, cz0 + ct + 7
    for j, (x, y) in enumerate(rods_xy, 1):
        add(_p(f"Shield rod {j}, M5 stainless threaded rod", b.Pos(x, y, z_rod0) * cp.round_bar(P["rod_d"] - 0.5, z_rod1 - z_rod0, 0.4),
               "stainless", "bought", 8, "shield", None, exp_sh))
        add(_p("M5 washer, shield rod top", b.Pos(x, y, cz0 + ct) * cp.washer(5), "stainless", "fastener", 11, "shield"))
        add(_p("M5 nut, shield rod top", b.Pos(x, y, cz0 + ct + 1.0) * cp.hex_nut(5), "stainless", "fastener", 11, "shield"))
        add(_p("M5 washer, shield rod bottom", b.Pos(x, y, z_pb - 1.0) * cp.washer(5), "stainless", "fastener", 11, "shield"))
        add(_p("M5 nut, shield rod bottom", b.Pos(x, y, z_pb - 1.0 - 4.7) * cp.hex_nut(5), "stainless", "fastener", 11, "shield"))
    for dx in P["cap_screw_dx"]:
        add(_p("M5 brass heat-set insert, shield cap", ap.place(ap.insert(5, 6.0), (scx + dx, scy, cz0 + ct - 1.0), "z", -1),
               "brass", "fastener", 11, "shield"))
        add(_p("M5 x 10 pan head screw, shield cap to cross arm", ap.place(ap.pan_screw(5, 10), (scx + dx, scy, D["arm_z"] + at + 1.0), "z", -1),
               "stainless", "fastener", 11, "shield"))
        add(_p("M5 washer, shield cap screw", b.Pos(scx + dx, scy, D["arm_z"] + at) * ap.washer_small(5), "stainless", "fastener", 11, "shield"))

    # ------------------------------------------------------------------ 12 diffusion tube hood (AST-DDR-006)
    exp_hd = (160, -200, -330)
    hxs, hys = P["hood_x"], D["arm_y"] + P["hood_dy"]
    add(_p("Diffusion tube hood, printed ASA", C["hood"].shape, "pe_tank_white", "made", 12, "hood", "#CCFBF1", exp_hd))
    for j, s in enumerate(_solids(C["hood_clips"].shape), 1):
        add(_p(f"Tube clip {j}, printed ASA", s, "pe_tank_white", "made", 12, "hood", "#99F6E4", exp_hd))
    hz0, ht0 = D["arm_z"], P["hood_top"]
    for dx in P["hood_dx"]:
        add(_p("M5 brass heat-set insert, tube hood", ap.place(ap.insert(5, 6.0), (hxs + dx, hys, hz0 - 1.0), "z", -1),
               "brass", "fastener", 11, "hood"))
        add(_p("M5 x 10 pan head screw, tube hood to cross arm", ap.place(ap.pan_screw(5, 10), (hxs + dx, hys, D["arm_z"] + at + 1.0), "z", -1),
               "stainless", "fastener", 11, "hood"))
        add(_p("M5 washer, tube hood screw", b.Pos(hxs + dx, hys, D["arm_z"] + at) * ap.washer_small(5), "stainless", "fastener", 11, "hood"))

    # ------------------------------------------------------------------ 9 T and RH probe on its tube
    thz = D["th_z"]
    tube_top = D["arm_z"] + at + 8
    add(_p("Probe tube, 6 mm aluminium", ap.tube_z(scx, scy, thz + 2.0, tube_top, P["th_tube"], 1.0), "aluminium", "bought", 9, "shield", None, (420, -60, -300)))
    tbx, tby, tbz = P["th_board"]
    pb = ap.rounded_box(scx - tbx / 2, scx + tbx / 2, scy - tby / 2, scy + tby / 2, thz + 0.4, thz + 2.0, 0.4)
    for sx in (-1, 1):
        pb -= b.Pos(scx + sx * 5, scy - 3, thz + 1.2) * b.Cylinder(1.1, 3)
    pb += b.Pos(scx, scy + 1, thz - 0.8) * b.Cylinder(2.5, 2.4) + b.Pos(scx + 3.5, scy - 2.5, thz + 0.1) * b.Box(2.5, 2.5, 0.6)
    add(_p("T and RH probe board (SHT45) with filter cap", pb, "hdpe_recycled", "bought", 9, "shield", "#7C3AED", (420, -60, -300)))

    # ------------------------------------------------------------------ 10 cables
    pgd, pgl = P["plug"]
    port_bot = z0 - 22.0
    lid_top_abs = D["pod_bot"] + H + lt
    for j, x in enumerate((FP["pens"]["port_a"][0], FP["pens"]["port_b"][0]), 1):
        y = D["whip_y"]
        add(_p(f"M12 5-pin plug, sensor cable {'A' if j == 1 else 'B'}", b.Pos(x, y, port_bot) * ap.m12_plug(pgl, pgd),
               "hdpe_black", "bought", 10, "cables", "#111827", (-340, -60, 120)))
        L = port_bot - pgl - lid_top_abs - 12
        add(_p(f"Sensor cable {'A' if j == 1 else 'B'}, 6 mm shielded", b.Pos(x, y, lid_top_abs + 12 + L / 2) * b.Cylinder(P["cable_d"] / 2, L),
               "rubber_belt", "bought", 10, "cables", "#111827", (-340, -60, 120)))
    pr = P["probe_cable_d"] / 2
    yA = D["arm_y"]
    xg = P["pod_x"] + W / 2 + 9 + 12
    zg = D["pod_bot"] + pgz
    lead = M.path_rod(M.probe_lead_points(P), pr)
    add(_p("Probe lead, 4-core shielded", lead, "rubber_belt", "bought", 10, "cables", "#111827", (-340, -60, 120)))
    add(_p("M8 4-pin plug, probe lead", b.Pos(P["pod_x"] + W / 2 + 9, D["pod_yc"] + pgy, zg) * b.Rot(0, 90, 0) * ap.m8_plug(12.0, 10.0).mirror(b.Plane.XY),
           "hdpe_black", "bought", 10, "cables", "#111827", (-340, -60, 120)))
    return out

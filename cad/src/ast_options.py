"""AirStreet concept options B and C, modelled at detail level D3 (AST-OPT-001; STANDARDS sections 21 and 24).

Both options mount on the same 140 mm street light pole as option A, with the same printed 140 degree V-saddles
and cut-to-length stainless bands on a 40 x 4 mm rail, and put their inlets 3.0 m above the sidewalk; they differ
in how the air reaches the sensors and how NO2 is measured.

    Option B, aspirated heated-inlet node: a 10 mm stainless inlet with a heater sleeve and rain cap rises into an
        IP65 enclosure on a back plate; inside, a manifold block carries the NO2 cell in its flow path, a diaphragm
        pump draws the sample, the particle sensor sits in a printed flow box, a 12 Ah LiFePO4 pack and the
        controller board sit on an internal plate; a fan-aspirated double-tube shield for T and RH hangs from a
        cross arm; a 30 W panel on two bent side brackets and a crossbar powers it.
    Option C, passive diffusion-tube station: three Palmes tubes, open end down, under a printed hood on a cross
        arm (the arm spaces them 120 mm or more from the pole), and an IP65 logger box on a back plate with the
        particle sensor behind a louvred cowl, four D cells in a holder and the logger board.

Not chosen: these models exist so the options are compared at one detail level. Main dimensions are first-order
choices recorded in AST-OPT-001, not design values.
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
from ast_detail import _p, _soften, WHITE, DARK, PCB  # noqa: E402


def _bx(x0, x1, y0, y1, z0, z1):
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def _ycyl(x, y, z, r, h):
    return b.Pos(x, y, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)


def _zcyl(x, y, z, r, h):
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)


# ------------------------------------------------------------------ shared pole mount (as option A)
def pole_mount(P, rail_z, clamp_z, holes, tag):
    """Rail, two V-saddles, two bands with housings, saddle screws and inserts. holes: [(x, z, 'csk' | 'plain')]
    drilled through the rail for the option's own bolts. Returns (parts, geometry dict)."""
    import model as M
    D = M.derived(P)
    R = D["R"]
    sw, sh, sd = P["saddle"]
    rw, rt = P["rail"]
    yrb, yrf = D["rail_back"], D["rail_front"]
    gh, gd = P["groove"]
    half = math.radians(P["saddle_v"] / 2)
    ya = D["v_apex"]
    m = sd - P["saddle_base"] + 2
    out = []
    for i, zc in enumerate(clamp_z):
        s = _bx(-sw / 2, sw / 2, yrb, yrb + sd, zc - sh / 2, zc + sh / 2)
        tri = b.Pos(0, 0, zc - sh / 2 - 1) * b.extrude(b.Polygon((0, ya), (m * math.tan(half), ya + m), (-m * math.tan(half), ya + m), align=None), sh + 2)
        s -= tri
        s -= _bx(-sw / 2 - 1, sw / 2 + 1, yrb - 1, yrb + gd, zc - gh / 2, zc + gh / 2)
        for sx, dzs in P["saddle_screws"]:
            s -= _ycyl(sx, yrb + 5, zc + dzs, 3.4, 10.0)
        lvl = "lower" if i == 0 else "upper"
        out.append(_p(f"V-saddle, {lvl} ({tag})", s, "hdpe_black", "made", None, "mount", DARK))
    za, zb = rail_z
    rail = _bx(-rw / 2, rw / 2, yrf, yrb, za, zb)
    allh = [(sx, zc + dzs, "csk") for zc in clamp_z for sx, dzs in P["saddle_screws"]] + list(holes)
    for x, z, kind in allh:
        rail -= _ycyl(x, (yrf + yrb) / 2, z, 2.75, rt + 2)
        if kind == "csk":
            rail -= b.Pos(x, yrf, z) * b.Rot(-90, 0, 0) * b.Cone(5.1, 2.6, 2.6, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
    out.append(_p(f"Rail, 40 x 4 mm aluminium flat bar ({tag})", _soften(rail, 0.5), "aluminium", "made", None, "mount"))
    bw, bt = P["band"]
    for i, zc in enumerate(clamp_z):
        yg = yrb + gd
        inner = b.make_hull(b.Circle(R).edges() + b.Polyline((-sw / 2, yg), (sw / 2, yg)).edges())
        outer = b.offset(inner, bt, kind=b.Kind.ARC)
        ring = b.Pos(0, 0, zc - bw / 2) * (b.extrude(outer, bw) - b.extrude(inner, bw))
        lvl = "lower" if i == 0 else "upper"
        out.append(_p(f"Band, 12.7 mm stainless, {lvl} clamp ({tag})", ring, "stainless", "bought", None, "mount"))
        ang = math.radians(35.0)
        house = b.Pos((R + bt) * math.cos(ang), (R + bt) * math.sin(ang), zc) * b.Rot(0, 0, math.degrees(ang) - 90) * ap.worm_housing(bw)
        out.append(_p(f"Worm-drive housing, {lvl} clamp ({tag})", house, "stainless", "bought", None, "mount"))
        for sx, dzs in P["saddle_screws"]:
            z = zc + dzs
            out.append(_p("M5 x 14 countersunk screw, saddle", ap.place(ap.csk_screw(5, 14), (sx, yrf, z), "y", 1), "stainless", "fastener", None, "mount"))
            out.append(_p("M5 brass heat-set insert, saddle", ap.place(ap.insert(5), (sx, yrb + 0.5, z), "y", 1), "brass", "fastener", None, "mount"))
    return out, dict(yrb=yrb, yrf=yrf, R=R)


def arm_angle(x0, x1, z_a, yrf, leg=30.0, t=3.0, holes_z=(), holes_y=()):
    """30 x 30 x 3 angle along X: upright leg on the rail front, horizontal leg at the bottom toward the street.
    holes_y: bolt holes through the upright leg [(x, z)]; holes_z: holes through the horizontal leg [(x, y, r)]."""
    a = _bx(x0, x1, yrf - leg, yrf, z_a, z_a + t) + _bx(x0, x1, yrf - t, yrf, z_a, z_a + leg)
    for x, z in holes_y:
        a -= _ycyl(x, yrf - t / 2, z, 2.75, t + 2)
    for x, y, r in holes_z:
        a -= _zcyl(x, y, z_a + t / 2, r, t + 2)
    return _soften(a, 0.4)


def rail_bolt_set(x, z, yrb, y_front, nut_side="front", tag="", length=14):
    """Button head screw from behind the rail (head at yrb) toward -Y, washer and nyloc nut at y_front."""
    out = [_p(f"M5 x {length} button head screw{tag}", ap.place(ap.button_screw(5, length), (x, yrb, z), "y", -1), "stainless", "fastener", None, "mount"),
           _p(f"M5 washer{tag}", b.Pos(x, y_front, z) * b.Rot(90, 0, 0) * ap.washer_small(5), "stainless", "fastener", None, "mount"),
           _p(f"M5 nyloc nut{tag}", b.Pos(x, y_front - 1.0, z) * b.Rot(90, 0, 0) * ap.nyloc_nut(5), "stainless", "fastener", None, "mount")]
    return out


def csk_plate_bolt(x, z, y_face, yrb, tag="", length=14):
    """Countersunk screw from a plate front (y_face) toward +Y through plate and rail, nyloc nut behind the rail."""
    return [_p(f"M5 x {length} countersunk screw{tag}", ap.place(ap.csk_screw(5, length), (x, y_face, z), "y", 1), "stainless", "fastener", None, "mount"),
            _p(f"M5 nyloc nut{tag}", b.Pos(x, yrb, z) * b.Rot(-90, 0, 0) * ap.nyloc_nut(5), "stainless", "fastener", None, "mount")]


def back_plate(x0, x1, z0, z1, yrf, t, rail_holes, lug_holes, name):
    """Aluminium back plate on the rail front: countersunk rail holes at x = 0 and plain lug holes."""
    pl = _bx(x0, x1, yrf - t, yrf, z0, z1)
    for x, z in rail_holes:
        pl -= _ycyl(x, yrf - t / 2, z, 2.75, t + 2)
        pl -= b.Pos(x, yrf - t, z) * b.Rot(-90, 0, 0) * b.Cone(5.1, 2.6, 2.6, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
    for x, z in lug_holes:
        pl -= _ycyl(x, yrf - t / 2, z, 2.75, t + 2)
    try:
        pl = b.fillet(pl.edges().filter_by(b.Axis.Y), 6.0)
    except Exception:
        pass
    return _p(name, pl, "aluminium", "made", None, "enclosure")


def enclosure(x0, x1, z0, z1, y_back, depth, lid_d, wall, lug_z, color, tag, boss_len=18.0, floor_holes=(), back_holes=()):
    """IP65 box: body open to the front with four lugs at the back corners and four corner bosses, and a lid with
    four screws. Returns (parts, inner (x0, x1, y0, y1, z0, z1), lug points)."""
    yb0 = y_back - depth
    body = _bx(x0, x1, yb0, y_back, z0, z1) - _bx(x0 + wall, x1 - wall, yb0 - 1, y_back - wall, z0 + wall, z1 - wall)
    bosses = [(x0 + wall + 5, z0 + wall + 5), (x1 - wall - 5, z0 + wall + 5), (x0 + wall + 5, z1 - wall - 5), (x1 - wall - 5, z1 - wall - 5)]
    for x, z in bosses:
        body += _ycyl(x, yb0 + boss_len / 2, z, 5.0, boss_len)
        body -= _ycyl(x, yb0 + 6, z, 1.7, 12.1)
    for x, y, r in floor_holes:
        body -= _zcyl(x, y, z0 + wall / 2, r, wall + 2)
    for x, z, r, dep in back_holes:
        body -= _ycyl(x, y_back - wall + dep / 2 - 0.01, z, r, dep)
    lugs = []
    for x in (x0 - 6, x1 + 6):
        for z in lug_z:
            lug = _bx(x - 6, x + 6, y_back - 6, y_back, z - 10, z + 10) - _ycyl(x, y_back - 3, z, 2.75, 8)
            body += lug
            lugs.append((x, z))
    try:
        body = b.fillet(body.edges().filter_by(b.Axis.Y).group_by(b.Axis.X)[0], 2.0)
    except Exception:
        pass
    lid = _bx(x0, x1, yb0 - lid_d, yb0, z0, z1) - _bx(x0 + 2.5, x1 - 2.5, yb0 - lid_d + 2.5, yb0 + 1, z0 + 2.5, z1 - 2.5)
    for x, z in bosses:
        lid += _ycyl(x, yb0 - (lid_d - 2.5) / 2, z, 5.0, lid_d - 2.5)
        lid -= _ycyl(x, yb0 - lid_d / 2, z, 2.2, lid_d + 2)
    try:
        lid = b.fillet(lid.edges().filter_by(b.Axis.Y), 3.0)
    except Exception:
        pass
    out = [_p(f"Enclosure body, IP65 ({tag})", body, "hdpe_natural", "bought", None, "enclosure", color),
           _p(f"Enclosure lid, IP65 ({tag})", lid, "hdpe_natural", "bought", None, "enclosure", color)]
    for x, z in bosses:
        out.append(_p("M4 x 16 pan head screw, lid", ap.place(ap.pan_screw(4, 16), (x, yb0 - lid_d, z), "y", 1), "stainless", "fastener", None, "enclosure"))
    inner = (x0 + wall, x1 - wall, yb0, y_back - wall, z0 + wall, z1 - wall)
    return out, inner, lugs


def lug_fixings(lugs, y_back, yrf, t_plate):
    out = []
    for x, z in lugs:
        out.append(_p("M5 x 14 pan head screw, enclosure lug", ap.place(ap.pan_screw(5, 14), (x, y_back - 6, z), "y", 1), "stainless", "fastener", None, "enclosure"))
        out.append(_p("M5 nyloc nut, enclosure lug", b.Pos(x, yrf, z) * b.Rot(-90, 0, 0) * ap.nyloc_nut(5), "stainless", "fastener", None, "enclosure"))
    return out


def sps30(x0, y0, z0):
    """Particle sensor on edge (41 x 12 x 41 mm), inlet face down, from its lower front left corner."""
    body = ap.rounded_box(x0, x0 + 41, y0, y0 + 12, z0, z0 + 41, 1.0)
    body -= b.Pos(x0 + 20.5, y0 + 6, z0 + 0.75) * b.Box(18, 6, 1.5)
    for k in range(4):
        body -= b.Pos(x0 + 8.5 + 8 * k, y0 + 0.5, z0 + 30) * b.Box(2.5, 1.0, 12)
    body += b.Pos(x0 + 20.5, y0 + 6, z0 + 43) * b.Box(10, 5, 4) - b.Pos(x0 + 20.5, y0 + 6, z0 + 44) * b.Box(8, 3, 2.1)
    return body


# ------------------------------------------------------------------ option B
def option_b(P):
    out = []
    add = out.extend
    rail_z, clamp_z = (2960.0, 3660.0), (3020.0, 3600.0)
    arm_z, cb_z = 3120.0, 3540.0
    plate_rail_z = (3262.0, 3302.0, 3438.0, 3478.0)
    holes = [(0.0, z, "plain") for z in plate_rail_z] + [(x, arm_z + 16.5, "plain") for x in (-10.0, 10.0)] \
        + [(x, cb_z + 4 + 18.0, "plain") for x in (-10.0, 10.0)]
    parts, g = pole_mount(P, rail_z, clamp_z, holes, "B")
    add(parts)
    yrb, yrf = g["yrb"], g["yrf"]
    tp = 3.0
    yp = yrf - tp                                       # back plate front face = enclosure back
    # enclosure on its back plate
    ex0, ex1, ez0, ez1 = -100.0, 100.0, 3245.0, 3495.0
    lug_z = (3265.0, 3475.0)
    so_pts = [(-82.0, 3265.0), (82.0, 3265.0), (-82.0, 3475.0), (82.0, 3475.0)]
    tx, ty = -84.0, yp - 33.0
    enc, inner, lugs = enclosure(ex0, ex1, ez0, ez1, yp, 100.0, 12.0, 3.0, lug_z, "#DADDE1", "B",
                                 floor_holes=[(tx, ty, 6.1), (60.0, -150.0, 6.0)],
                                 back_holes=[(x, z, 2.1, 2.5) for x, z in so_pts])
    add(enc)
    out.append(back_plate(-118.0, 118.0, 3225.0, 3515.0, yrf, tp, [(0.0, z) for z in plate_rail_z], lugs, "Back plate, 3 mm aluminium (B)"))
    for z in plate_rail_z:
        add(csk_plate_bolt(0.0, z, yp, yrb, ", back plate"))
    add(lug_fixings(lugs, yp, yrf, tp))
    ix0, ix1, iy0, iy1, iz0, iz1 = inner
    wall_in = iy1                                        # inner face of the back wall
    # internal plate on four standoffs
    ipt, so_l = 2.0, 8.0
    ipy1 = wall_in - so_l
    ipy0 = ipy1 - ipt
    ip = _bx(-85.0, 85.0, ipy0, ipy1, 3255.0, 3485.0)
    for x, z in so_pts:
        ip -= _ycyl(x, ipy0 + ipt / 2, z, 2.2, ipt + 2)
    strap_tab = (0.0, 3342.0)
    pump_br = [(28.0, 3362.0), (28.0, 3386.0)]
    man_h = [(-75.0, 3352.0), (-45.0, 3378.0)]
    pcb_h = [(-85.0 + 6, 3404.0), (5.0 - 6, 3404.0), (-85.0 + 6, 3466.0), (5.0 - 6, 3466.0)]
    fbox_h = [(30.0, 3430.0), (90.0, 3430.0)]
    for x, z in [strap_tab] + pump_br + man_h + fbox_h:
        ip -= _ycyl(x, ipy0 + ipt / 2, z, 2.2 if (x, z) in man_h or (x, z) == strap_tab else 1.7, ipt + 2)
    for x, z in pcb_h:
        ip -= _ycyl(x, ipy0 + ipt / 2, z, 1.7, ipt + 2)
    out.append(_p("Internal plate, 2 mm aluminium (B)", ip, "aluminium", "made", None, "internal"))
    for x, z in so_pts:
        out.append(_p("M4 x 8 hex standoff, internal plate", b.Pos(x, ipy1, z) * b.Rot(90, 0, 0) * ap.standoff(4, so_l, stub=2.0), "brass", "fastener", None, "internal"))
        out.append(_p("M4 x 6 pan head screw, internal plate", ap.place(ap.pan_screw(4, 6), (x, ipy0, z), "y", 1), "stainless", "fastener", None, "internal"))
    # nuts behind the internal plate need room: the standoffs leave 8 mm between plate and wall
    # battery and strap
    bat = ap.rounded_box(-75.0, 75.0, ipy0 - 50.0, ipy0, 3256.0, 3330.0, 3.0)
    bat += _zcyl(-55.0, ipy0 - 25.0, 3332.0, 4.0, 4.0) + _zcyl(55.0, ipy0 - 25.0, 3332.0, 4.0, 4.0)
    out.append(_p("LiFePO4 battery, 12.8 V 12 Ah (B)", bat, "hdpe_black", "bought", None, "internal", "#2563EB"))
    sy0 = ipy0 - 51.5
    strap = (_bx(-10, 10, sy0, ipy0, 3330.5, 3332.0) + _bx(-10, 10, sy0, sy0 + 1.5, 3295.0, 3332.0)
             + _bx(-10, 10, ipy0 - 1.5, ipy0, 3332.0, 3352.0) - _ycyl(0.0, ipy0 - 0.75, 3342.0, 2.2, 3))
    out.append(_p("Battery strap, bent 1.5 mm aluminium (B)", strap, "aluminium", "made", None, "internal"))
    out.append(_p("M4 x 10 pan head screw, battery strap", ap.place(ap.pan_screw(4, 10), (0.0, ipy0 - 1.5, 3342.0), "y", 1), "stainless", "fastener", None, "internal"))
    out.append(_p("M4 nyloc nut, battery strap", b.Pos(0.0, ipy1, 3342.0) * b.Rot(-90, 0, 0) * ap.nyloc_nut(4), "stainless", "fastener", None, "internal"))
    # manifold block with the NO2 cell, clamp ring
    my1 = ipy0
    my0 = my1 - 36.0
    mc_y = my1 - 20.0
    man = _soften(_bx(-90.0, -30.0, my0, my1, 3345.0, 3385.0), 0.8)
    man -= _zcyl(-84.0, mc_y, 3365.0, 4.0, 42.0)                      # sample bore, bottom to top
    man -= _xcyl(-77.0, mc_y, 3365.0, 2.5, 14.0)                      # bore to the cell face
    man -= _xcyl(-38.0, mc_y, 3365.0, 2.5, 16.0)                      # cell face to the pump port
    man -= _ycyl(-60.0, my0 + 8.25, 3365.0, 16.3, 16.5)               # cell pocket in the front face
    for x, z in man_h:
        man -= _ycyl(x, (my0 + my1) / 2, z, 2.2, 40.0)
        man -= _ycyl(x, my0 + 2.0, z, 4.2, 4.0)                       # counterbore
    for x in (-82.0, -38.0):
        man -= _ycyl(x, my0 + 4.0, 3365.0, 1.25, 8.0)                 # M3 tapped, clamp ring
    out.append(_p("Sample manifold, machined aluminium block (B)", man, "aluminium", "made", None, "internal"))
    for x, z in man_h:
        out.append(_p("M4 x 40 socket head screw, manifold", ap.place(ap.pan_screw(4, 40), (x, my0 + 4.0, z), "y", 1), "stainless", "fastener", None, "internal"))
        out.append(_p("M4 nyloc nut, manifold", b.Pos(x, ipy1, z) * b.Rot(-90, 0, 0) * ap.nyloc_nut(4), "stainless", "fastener", None, "internal"))
    cell = b.Pos(-60.0, my0 + 8.25, 3365.0) * b.Rot(90, 0, 0) * b.Cylinder(16.0, 16.5)
    cell -= b.Pos(-60.0, my0 + 16.5 - 0.3, 3365.0) * b.Rot(90, 0, 0) * b.Cylinder(10.0, 0.6)
    out.append(_p("NO2 sensor (NO2-B43F class) in the manifold (B)", cell, "stainless", "bought", None, "internal", "#B0B4B8"))
    ring = _ycyl(-60.0, my0 - 1.5, 3365.0, 26.0, 3.0) - _ycyl(-60.0, my0 - 1.5, 3365.0, 13.0, 4.0)
    for x in (-82.0, -38.0):
        ring -= _ycyl(x, my0 - 1.5, 3365.0, 1.7, 4.0)
    out.append(_p("Cell clamp ring, printed ASA (B)", ring, "pe_tank_white", "made", None, "internal", WHITE))
    for x in (-82.0, -38.0):
        out.append(_p("M3 x 8 pan head screw, clamp ring", ap.place(ap.pan_screw(3, 8), (x, my0 - 3.0, 3365.0), "y", 1), "stainless", "fastener", None, "internal"))
    # pump on its bracket
    by0 = ipy0 - 2.0
    br = _bx(-6.0, 34.0, by0, ipy0, 3356.0, 3392.0) + _bx(20.0, 22.0, by0 - 40.0, by0, 3340.0, 3390.0)
    for x, z in pump_br:
        br -= _ycyl(x, ipy0 - 1.0, z, 1.7, 4.0)
    for z in (3346.0, 3384.0):
        br -= _xcyl(21.0, by0 - 20.0, z, 1.7, 4.0)
    out.append(_p("Pump bracket, bent 2 mm aluminium (B)", _soften(br, 0.3), "aluminium", "made", None, "internal"))
    for x, z in pump_br:
        out.append(_p("M3 x 8 pan head screw, pump bracket", ap.place(ap.pan_screw(3, 8), (x, by0, z), "y", 1), "stainless", "fastener", None, "internal"))
        out.append(_p("M3 nyloc nut, pump bracket", b.Pos(x, ipy1, z) * b.Rot(-90, 0, 0) * ap.nyloc_nut(3), "stainless", "fastener", None, "internal"))
    pc_y = by0 - 20.0
    pump = _xcyl(45.0, pc_y, 3365.0, 13.5, 46.0)
    pump += _bx(-6.0, 20.0, pc_y - 14.0, pc_y + 14.0, 3340.0, 3390.0)
    for z in (3346.0, 3384.0):
        pump -= _xcyl(14.0, pc_y, z, 1.25, 12.0)
    pump += _xcyl(-10.0, pc_y, 3365.0, 2.0, 8.0) + _zcyl(7.0, pc_y, 3394.0, 2.0, 8.0)
    out.append(_p("Diaphragm pump, 12 V, about 1 L/min (B)", pump, "matte_black", "bought", None, "internal", "#374151"))
    for z in (3346.0, 3384.0):
        out.append(_p("M3 x 8 pan head screw, pump", ap.place(ap.pan_screw(3, 8), (22.0, pc_y, z), "x", -1), "stainless", "fastener", None, "internal"))
    # sample tubing: manifold side port to the pump inlet barb
    out.append(_p("Silicone tube, 6 mm, manifold to pump (B)", _xcyl(-22.0, mc_y, 3365.0, 3.0, 16.0) - _xcyl(-22.0, mc_y, 3365.0, 1.5, 17.0),
                  "epdm", "bought", None, "internal"))
    # particle sensor in a printed flow box
    fy1 = ipy0
    fy0 = fy1 - 28.0
    fb = _bx(35.0, 85.0, fy0, fy1, 3400.0, 3455.0) - _bx(37.5, 82.5, fy0 + 2.5, fy1 - 2.5, 3402.5, 3452.5)
    fb += _bx(24.0, 96.0, fy1 - 2.5, fy1, 3422.0, 3438.0)
    for x, z in fbox_h:
        fb -= _ycyl(x, fy1 - 1.25, z, 1.7, 4.0)
    fb -= _zcyl(60.0, fy0 + 14.0, 3401.0, 3.0, 4.0)
    fb += _zcyl(60.0, fy0 + 14.0, 3394.0, 3.0, 12.0) - _zcyl(60.0, fy0 + 14.0, 3394.0, 1.8, 14.0)
    fb += _bx(42.0, 48.0, fy0 + 8.0, fy0 + 20.0, 3402.5, 3405.0) + _bx(72.0, 78.0, fy0 + 8.0, fy0 + 20.0, 3402.5, 3405.0)
    out.append(_p("Particle sensor flow box, printed ASA (B)", fb, "pe_tank_white", "made", None, "internal", WHITE))
    for x, z in fbox_h:
        out.append(_p("M3 x 8 pan head screw, flow box", ap.place(ap.pan_screw(3, 8), (x, fy1 - 2.5, z), "y", 1), "stainless", "fastener", None, "internal"))
        out.append(_p("M3 nyloc nut, flow box", b.Pos(x, ipy1, z) * b.Rot(-90, 0, 0) * ap.nyloc_nut(3), "stainless", "fastener", None, "internal"))
    out.append(_p("Particle sensor (SPS30) (B)", sps30(39.5, fy0 + 8.0, 3405.0), "matte_black", "bought", None, "internal", "#3F3F46"))
    # controller board on standoffs
    pz0, pz1 = 3398.0, 3472.0
    board = ap.pcb(90.0, pz1 - pz0, 1.6, [(x + 40.0, z - (pz0 + pz1) / 2, 3.2) for x, z in pcb_h],
                   [(-10, 10, 20, 16, 2.5), (20, -15, 14, 10, 3.0), (-30, -20, 12, 8, 6.0), (25, 20, 10, 6, 2.0)])
    py = ipy0 - 6.0
    out.append(_p("Controller and LoRa board (B)", b.Pos(-40.0, py, (pz0 + pz1) / 2) * board, "hdpe_recycled", "bought", None, "internal", PCB))
    for x, z in pcb_h:
        out.append(_p("M3 x 6 hex standoff, controller", b.Pos(x, py, z) * b.Rot(90, 0, 0) * ap.standoff(3, 6.0, stub=0.0), "brass", "fastener", None, "internal"))
        out.append(_p("M3 x 4 pan head screw, controller", ap.place(ap.pan_screw(3, 4), (x, py - 1.6, z), "y", 1), "stainless", "fastener", None, "internal"))
        out.append(_p("M3 x 5 pan head screw, standoff to plate", ap.place(ap.pan_screw(3, 5), (x, ipy1, z), "y", -1), "stainless", "fastener", None, "internal"))
    # heated inlet: stainless tube through a bottom gland, heater sleeve, rain cap
    out.append(_p("Inlet tube, 10 x 1 mm stainless (B)", ap.tube_z(tx, ty, 2995.0, 3345.0, 8.0, 1.0), "stainless", "bought", None, "inlet"))
    out.append(_p("Heater sleeve, silicone, 2 W (B)", ap.tube_z(tx, ty, 3080.0, 3215.0, 16.0, 4.0), "epdm", "bought", None, "inlet", "#B91C1C"))
    out.append(_p("Cable gland M12, inlet tube", b.Pos(tx, ty, ez0) * b.Rot(180, 0, 0) * ap.gland(12, 8.0), "hdpe_black", "bought", None, "inlet"))
    out.append(_p("Gland locknut M12, inlet tube", b.Pos(tx, ty, ez0 + 3.0) * b.Rot(180, 0, 0) * ap.locknut(12, 4.0), "hdpe_black", "fastener", None, "inlet"))
    cap = _zcyl(tx, ty, 3000.0, 20.0, 30.0) - _zcyl(tx, ty, 2998.5, 18.0, 30.0)
    cap -= _zcyl(tx, ty, 3013.5, 4.0, 4.0)
    cap -= _xcyl(tx + 6.0, ty, 3013.5, 1.25, 6.0)
    cap += _zcyl(tx, ty, 3019.0, 7.0, 8.0) - _zcyl(tx, ty, 3019.0, 4.0, 9.0) - _xcyl(tx + 6.0, ty, 3019.0, 1.25, 4.0)
    out.append(_p("Inlet rain cap, printed ASA (B)", cap, "pe_tank_white", "made", None, "inlet", WHITE))
    out.append(_p("M3 x 4 set screw, rain cap", _xcyl(tx + 5.5, ty, 3019.0, 1.2, 3.0), "stainless", "fastener", None, "inlet"))
    vent = _zcyl(60.0, -150.0, ez0 - 4.0, 8.0, 8.0) + _zcyl(60.0, -150.0, ez0 + 1.5, 5.8, 3.0)
    out.append(_p("Membrane vent M12 (B)", vent, "hdpe_black", "bought", None, "enclosure"))
    # aspirated T and RH shield under the cross arm
    ay = yrf - 15.0
    cr_x = (180.0, 260.0)
    out.append(_p("Cross arm, 30 x 30 x 3 mm aluminium angle (B)", arm_angle(-20.0, 330.0, arm_z, yrf, holes_y=[(-10.0, arm_z + 16.5), (10.0, arm_z + 16.5)],
                                                                         holes_z=[(x, ay, 2.75) for x in cr_x]), "aluminium", "made", None, "shield"))
    for x in (-10.0, 10.0):
        add(rail_bolt_set(x, arm_z + 16.5, yrb, yrf - 3.0, ", cross arm"))
    zt = 3082.0
    for x in cr_x:
        blk = _bx(x - 15, x + 15, ay - 15, ay + 15, 3100.0, arm_z) - _xcyl(x, ay, zt, 25.8, 32.0)
        blk -= _zcyl(x, ay, arm_z - 5.0, 3.4, 10.1)
        out.append(_p("Shield cradle block, printed ASA (B)", _soften(blk, 0.6), "pe_tank_white", "made", None, "shield", WHITE))
        out.append(_p("M5 brass heat-set insert, cradle", ap.place(ap.insert(5), (x, ay, arm_z - 1.0), "z", -1), "brass", "fastener", None, "shield"))
        out.append(_p("M5 x 10 pan head screw, cradle", ap.place(ap.pan_screw(5, 10), (x, ay, arm_z + 4.0), "z", -1), "stainless", "fastener", None, "shield"))
        out.append(_p("M5 washer, cradle screw", b.Pos(x, ay, arm_z + 3.0) * ap.washer_small(5), "stainless", "fastener", None, "shield"))
        out.append(_p("Shield strap, stainless band", _xcyl(x, ay, zt, 25.8, 9.0) - _xcyl(x, ay, zt, 25.0, 10.0), "stainless", "bought", None, "shield"))
    outer = _xcyl(210.0, ay, zt, 25.0, 200.0) - _xcyl(210.0, ay, zt, 23.0, 202.0)
    outer -= _zcyl(220.0, ay, zt + 24.0, 3.0, 6.0)
    out.append(_p("Shield outer tube, 50 mm white PVC (B)", outer, "pe_tank_white", "bought", None, "shield", "#F2F2EF"))
    inner_t = _xcyl(215.0, ay, zt, 15.0, 170.0) - _xcyl(215.0, ay, zt, 13.5, 172.0)
    inner_t -= _zcyl(220.0, ay, zt + 14.0, 3.0, 4.0)
    out.append(_p("Shield inner tube, 30 mm (B)", inner_t, "pe_tank_white", "bought", None, "shield", "#F2F2EF"))
    for x in (140.0, 290.0):
        sp = _xcyl(x, ay, zt, 23.0, 6.0) - _xcyl(x, ay, zt, 15.0, 7.0)
        for k in range(3):
            a = math.radians(30 + 120 * k)
            sp -= b.Pos(x, ay + 19.0 * math.cos(a), zt + 19.0 * math.sin(a)) * b.Rot(0, 90, 0) * b.Cylinder(3.5, 7.0)
        out.append(_p("Shield spider ring, printed ASA (B)", sp, "pe_tank_white", "made", None, "shield", WHITE))
    ec = (_xcyl(115.0, ay, zt, 27.0, 10.0) - _xcyl(115.0, ay, zt, 25.0, 11.0)) + (_xcyl(108.0, ay, zt, 27.0, 4.0) - _xcyl(108.0, ay, zt, 18.0, 5.0))
    for dy, dz in ((16.0, 16.0), (-16.0, -16.0)):
        ec -= _xcyl(108.0, ay + dy, zt + dz, 1.25, 5.0)
    out.append(_p("Shield end cap and fan mount, printed ASA (B)", ec, "pe_tank_white", "made", None, "shield", WHITE))
    fan = _bx(96.0, 106.0, ay - 20, ay + 20, zt - 20, zt + 20) - _xcyl(101.0, ay, zt, 18.5, 11.0)
    fan += _xcyl(101.0, ay, zt, 7.0, 10.0)
    for dy, dz in ((16.0, 16.0), (-16.0, -16.0), (16.0, -16.0), (-16.0, 16.0)):
        fan -= _xcyl(101.0, ay + dy, zt + dz, 1.7, 11.0)
    out.append(_p("Aspiration fan, 40 mm, 12 V (B)", fan, "matte_black", "bought", None, "shield", "#1F2937"))
    for dy, dz in ((16.0, 16.0), (-16.0, -16.0)):
        out.append(_p("M3 x 14 pan head screw, fan", ap.place(ap.pan_screw(3, 14), (96.0, ay + dy, zt + dz), "x", 1), "stainless", "fastener", None, "shield"))
    out.append(_p("Probe tube, 6 mm aluminium (B)", ap.tube_z(220.0, ay, zt + 2.0, zt + 30.0, 6.0, 1.0), "aluminium", "bought", None, "shield"))
    pb = ap.rounded_box(213.0, 227.0, ay - 5, ay + 5, zt, zt + 2.0, 0.4) - _zcyl(216.0, ay - 3, zt + 1.0, 1.1, 3)
    pb += _zcyl(220.0, ay + 1, zt - 1.2, 2.5, 2.4)
    out.append(_p("T and RH probe board (SHT45) (B)", pb, "hdpe_recycled", "bought", None, "shield", "#7C3AED"))
    # 30 W panel on a crossbar and two bent side brackets
    cb = arm_angle(-275.0, 275.0, cb_z, yrf, leg=40.0, t=4.0, holes_y=[(x, cb_z + 22.0) for x in (-10.0, 10.0)] +
                   [(sx * x, cb_z + 22.0) for sx in (-1, 1) for x in (245.0, 262.0)])
    out.append(_p("Panel crossbar, 40 x 40 x 4 mm aluminium angle (B)", cb, "aluminium", "made", None, "panel"))
    for x in (-10.0, 10.0):
        add(rail_bolt_set(x, cb_z + 22.0, yrb, yrf - 4.0, ", panel crossbar"))
    tilt = 40.0
    PW, PL, PD = 540.0, 350.0, 35.0
    pan = _bx(-PW / 2, PW / 2, -PL / 2, PL / 2, -PD, 0) - _bx(-PW / 2 + 2, PW / 2 - 2, -PL / 2 + 2, PL / 2 - 2, -PD - 1, 1)
    pan += _bx(-PW / 2 + 2, PW / 2 - 2, -PL / 2 + 2, PL / 2 - 2, -4.0, 0)
    pan += _bx(-40, 40, 40, 100, -24.0, -4.0)
    bolt_l = [(-80.0, -18.0), (80.0, -18.0)]                       # (local y, local z) on the side walls
    for ly, lz in bolt_l:
        pan -= _xcyl(PW / 2 - 1, ly, lz, 3.3, 4.0) + _xcyl(-PW / 2 + 1, ly, lz, 3.3, 4.0)
    T = b.Rot(tilt, 0, 0)
    pan_r = T * pan
    bb = pan_r.bounding_box()
    shift = b.Pos(0, (yrf - 25.0) - bb.max.Y, (cb_z + 60.0) - bb.min.Z)
    out.append(_p("Solar panel, 30 W, aluminium frame (B)", shift * pan_r, "matte_black", "bought", None, "panel", "#1E293B"))

    def loc(x, ly, lz):
        v = (shift * T * b.Pos(x, ly, lz)).position
        return (v.X, v.Y, v.Z)

    for sx in (-1, 1):
        corners = [loc(0, -PL / 2, -PD), loc(0, PL / 2, -PD), loc(0, PL / 2, 0), loc(0, -PL / 2, 0)]
        yz = [(c[1], c[2]) for c in corners] + [(yrf - 8.0, cb_z + 4.0), (yrf - 8.0, cb_z + 40.0)]
        hull = b.make_hull(b.Polyline(*[(y, z) for y, z in yz], close=True).edges())
        face = b.Plane.YZ * b.make_face(hull)
        x_in = sx * PW / 2
        plate = b.extrude(face, 4.0) if sx > 0 else b.extrude(face, -4.0)
        plate = b.Pos(x_in, 0, 0) * plate
        tab = _bx(sx * (PW / 2 - 30.0), sx * (PW / 2 + 4.0), yrf - 8.0, yrf - 4.0, cb_z + 4.0, cb_z + 40.0)
        br = plate + tab
        for ly, lz in bolt_l:
            p = loc(x_in, ly, lz)
            br -= _xcyl(x_in + sx * 2.0, p[1], p[2], 3.3, 6.0)
        for x in (245.0, 262.0):
            br -= _ycyl(sx * x, yrf - 6.0, cb_z + 22.0, 2.75, 6.0)
        out.append(_p(f"Panel side bracket, bent 4 mm aluminium ({'right' if sx > 0 else 'left'}) (B)", _soften(br, 0.4), "aluminium", "made", None, "panel"))
        for x in (245.0, 262.0):
            out.append(_p("M5 x 16 hex bolt, side bracket", ap.place(ap.button_screw(5, 16), (sx * x, yrf - 8.0, cb_z + 22.0), "y", 1), "stainless", "fastener", None, "panel"))
            out.append(_p("M5 nyloc nut, side bracket", b.Pos(sx * x, yrf, cb_z + 22.0) * b.Rot(-90, 0, 0) * ap.nyloc_nut(5), "stainless", "fastener", None, "panel"))
        for ly, lz in bolt_l:
            p = loc(x_in, ly, lz)
            seat = (x_in + sx * 4.0, p[1], p[2])
            out.append(_p("M6 x 12 button head screw, panel", ap.place(ap.button_screw(6, 12), seat, "x", -sx), "stainless", "fastener", None, "panel"))
            nut_at = x_in - sx * 2.0
            nut = b.Pos(nut_at, p[1], p[2]) * (b.Rot(0, -90, 0) if sx > 0 else b.Rot(0, 90, 0)) * ap.nyloc_nut(6)
            out.append(_p("M6 nyloc nut, panel", nut, "stainless", "fastener", None, "panel"))
    return out


# ------------------------------------------------------------------ option C
def option_c(P):
    out = []
    add = out.extend
    rail_z, clamp_z = (2940.0, 3260.0), (2990.0, 3210.0)
    arm_z = 3100.0
    plate_rail_z = (3150.0, 3172.0)
    holes = [(x, arm_z + 16.5, "plain") for x in (-10.0, 10.0)] + [(0.0, z, "plain") for z in plate_rail_z]
    parts, g = pole_mount(P, rail_z, clamp_z, holes, "C")
    add(parts)
    yrb, yrf = g["yrb"], g["yrf"]
    ay = yrf - 15.0
    hx = 140.0
    hood_screw_x = (hx - 30.0, hx + 30.0)
    out.append(_p("Cross arm, 30 x 30 x 3 mm aluminium angle (C)", arm_angle(-20.0, 200.0, arm_z, yrf, holes_y=[(-10.0, arm_z + 16.5), (10.0, arm_z + 16.5)],
                                                                         holes_z=[(x, ay, 2.75) for x in hood_screw_x]), "aluminium", "made", None, "tubes"))
    for x in (-10.0, 10.0):
        add(rail_bolt_set(x, arm_z + 16.5, yrb, yrf - 3.0, ", cross arm"))
    # hood: top disc, skirt, three tube sockets
    zA = arm_z
    hood = _zcyl(hx, ay, zA - 5.0, 55.0, 10.0)
    hood += _zcyl(hx, ay, zA - 40.0, 55.0, 60.0) - _zcyl(hx, ay, zA - 41.0, 53.0, 62.0)
    socks = [(hx + 25.0 * math.cos(math.radians(a)), ay + 25.0 * math.sin(math.radians(a))) for a in (90, 210, 330)]
    for x, y in socks:
        hood += _zcyl(x, y, zA - 16.0, 9.5, 12.0)
        hood -= _zcyl(x, y, zA - 17.0, 7.5, 12.0)
    for x in hood_screw_x:
        hood -= _zcyl(x, ay, zA - 4.5, 3.4, 9.1)
    for k in range(6):
        a = math.radians(30 + 60 * k)
        hood -= b.Pos(hx + 54.0 * math.cos(a), ay + 54.0 * math.sin(a), zA - 55.0) * b.Box(8, 8, 18)
    out.append(_p("Tube hood, printed ASA (C)", hood, "pe_tank_white", "made", None, "tubes", WHITE))
    for x in hood_screw_x:
        out.append(_p("M5 brass heat-set insert, hood", ap.place(ap.insert(5), (x, ay, zA - 0.5), "z", -1), "brass", "fastener", None, "tubes"))
        out.append(_p("M5 x 10 pan head screw, hood", ap.place(ap.pan_screw(5, 10), (x, ay, zA + 4.0), "z", -1), "stainless", "fastener", None, "tubes"))
        out.append(_p("M5 washer, hood screw", b.Pos(x, ay, zA + 3.0) * ap.washer_small(5), "stainless", "fastener", None, "tubes"))
    for j, (x, y) in enumerate(socks, 1):
        cap = _zcyl(x, y, zA - 18.0, 7.5, 10.0) - _zcyl(x, y, zA - 19.5, 6.5, 7.1)
        out.append(_p(f"Diffusion tube cap with TEA grids ({j}) (C)", cap, "hdpe_black", "bought", None, "tubes", "#6B7280"))
        tube = ap.tube_z(x, y, zA - 87.0, zA - 16.5, 13.0, 1.0)
        out.append(_p(f"Palmes diffusion tube, acrylic, 71 mm ({j}) (C)", tube, "polycarbonate", "bought", None, "tubes"))
    # logger box on a back plate
    tp = 3.0
    yp = yrf - tp
    ex0, ex1, ez0, ez1 = -200.0, -40.0, 3150.0, 3250.0
    sx0, sy0 = -95.0, -135.5
    cxs, cys = sx0 + 20.5, sy0 + 6.0
    lh = [(-104.0, 3207.0), (-50.0, 3207.0), (-104.0, 3239.0), (-50.0, 3239.0)]
    enc, inner, lugs = enclosure(ex0, ex1, ez0, ez1, yp, 80.0, 10.0, 3.0, (3160.0, 3244.0), "#DADDE1", "C",
                                 floor_holes=[(cxs, cys, 10.0), (cxs, cys - 21.5, 1.7), (cxs, cys + 21.5, 1.7), (-170.0, -150.0, 6.0)],
                                 back_holes=[(x, z, 1.6, 2.5) for x, z in lh])
    add(enc)
    out.append(back_plate(-215.0, 25.0, 3140.0, 3258.0, yrf, tp, [(0.0, z) for z in plate_rail_z], lugs, "Back plate, 3 mm aluminium (C)"))
    for z in plate_rail_z:
        add(csk_plate_bolt(0.0, z, yp, yrb, ", back plate"))
    add(lug_fixings(lugs, yp, yrf, tp))
    ix0, ix1, iy0, iy1, iz0, iz1 = inner
    # battery holder on two floor bosses, four D cells
    hx0, hx1 = -183.0, -113.0
    hy0, hy1 = iy1 - 72.0, iy1 - 2.0
    fl = iz0
    hold = _bx(hx0, hx1, hy0, hy1, fl + 6.0, fl + 6.0 + 64.0)
    cells = []
    for i in (0, 1):
        for j in (0, 1):
            cx, cy = hx0 + 17.5 + 35.0 * i, hy0 + 17.5 + 35.0 * j
            hold -= _zcyl(cx, cy, fl + 6.0 + 2.0 + 33.0, 17.2, 66.0)
            cells.append((cx, cy))
    hold -= _zcyl(hx0 + 35.0, hy0 + 35.0, fl + 7.0, 1.7, 2.5)
    hold -= _zcyl(hx0 + 35.0, hy0 + 35.0, fl + 10.5, 3.3, 5.0)        # counterbore for the screw head
    hold = _soften(hold, 0.8)
    out.append(_p("Battery holder, 4 x D cells (C)", hold, "hdpe_black", "bought", None, "internal"))
    for j, (cx, cy) in enumerate(cells, 1):
        c = _zcyl(cx, cy, fl + 8.0 + 30.75, 17.1, 61.5) + _zcyl(cx, cy, fl + 8.0 + 61.5 + 0.75, 4.5, 1.5)
        out.append(_p(f"Alkaline D cell ({j}) (C)", c, "matte_black", "bought", None, "internal", "#1F2937"))
    y = hy0 + 35.0
    boss = _zcyl(hx0 + 35.0, y, fl + 3.0, 4.0, 6.0) - _zcyl(hx0 + 35.0, y, fl + 3.0, 1.25, 6.5)
    out.append(_p("Floor boss, printed ASA, bonded (C)", boss, "pe_tank_white", "made", None, "internal", WHITE))
    out.append(_p("M3 x 8 pan head screw, battery holder", ap.place(ap.pan_screw(3, 8), (hx0 + 35.0, y, fl + 8.0), "z", -1), "stainless", "fastener", None, "internal"))
    # particle sensor on two pads, inlet through the floor
    out.append(_p("Particle sensor (SPS30) (C)", sps30(sx0, sy0, fl + 3.0), "matte_black", "bought", None, "internal", "#3F3F46"))
    pads = _bx(sx0 + 2, sx0 + 8, sy0 + 1, sy0 + 11, fl, fl + 3.0) + _bx(sx0 + 33, sx0 + 39, sy0 + 1, sy0 + 11, fl, fl + 3.0)
    out.append(_p("Sensor pads, printed ASA, bonded (C)", _soften(pads, 0.4), "pe_tank_white", "made", None, "internal", WHITE))
    cowl = _zcyl(cxs, cys, ez0 - 14.0, 18.0, 22.0) - _zcyl(cxs, cys, ez0 - 13.0, 16.0, 22.0)
    cowl += _zcyl(cxs, cys, ez0 - 1.5, 24.0, 3.0) - _zcyl(cxs, cys, ez0 - 1.5, 10.0, 4.0)
    for k in range(6):
        a = math.radians(60 * k)
        cowl -= b.Pos(cxs + 17.0 * math.cos(a), cys + 17.0 * math.sin(a), ez0 - 12.0) * b.Box(6, 6, 10)
    for dy in (-21.5, 21.5):
        cowl -= _zcyl(cxs, cys + dy, ez0 - 1.5, 1.7, 4.0)
    out.append(_p("Inlet cowl, louvred, printed ASA (C)", cowl, "pe_tank_white", "made", None, "internal", WHITE))
    for dy in (-21.5, 21.5):
        out.append(_p("M3 x 10 pan head screw, cowl", ap.place(ap.pan_screw(3, 10), (cxs, cys + dy, ez0 - 3.0), "z", 1), "stainless", "fastener", None, "internal"))
        out.append(_p("M3 nyloc nut, cowl", b.Pos(cxs, cys + dy, fl) * ap.nyloc_nut(3), "stainless", "fastener", None, "internal"))
    # logger board on standoffs from the back wall
    lz0, lz1 = 3202.0, 3244.0
    board = ap.pcb(66.0, lz1 - lz0, 1.6, [(x + 77.0, z - (lz0 + lz1) / 2, 3.2) for x, z in lh],
                   [(-5, 5, 24, 14, 2.5), (18, -8, 12, 8, 2.0), (-20, -8, 6, 6, 1.2)])
    py = iy1 - 6.0
    out.append(_p("Logger board with memory card and SHT45 (C)", b.Pos(-77.0, py, (lz0 + lz1) / 2) * board, "hdpe_recycled", "bought", None, "internal", PCB))
    for x, z in lh:
        out.append(_p("M3 x 6 hex standoff, logger", b.Pos(x, py, z) * b.Rot(90, 0, 0) * ap.standoff(3, 6.0, stub=2.5), "brass", "fastener", None, "internal"))
        out.append(_p("M3 x 5 pan head screw, logger", ap.place(ap.pan_screw(3, 5), (x, py - 1.6, z), "y", 1), "stainless", "fastener", None, "internal"))
    vent = _zcyl(-170.0, -150.0, ez0 - 4.0, 8.0, 8.0) + _zcyl(-170.0, -150.0, ez0 + 1.5, 5.8, 3.0)
    out.append(_p("Membrane vent M12 (C)", vent, "hdpe_black", "bought", None, "internal"))
    return out

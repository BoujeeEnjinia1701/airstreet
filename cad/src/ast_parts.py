"""AirStreet repo helpers for the kit 1.9 detailed model (STANDARDS section 24).

Small hardware that .kit/cad_parts.py does not carry (it has ISO data from M5 up and no countersunk,
pan or button head screws): M3 to M5 pan, button and countersunk screws, nyloc nuts, small washers,
brass heat-set inserts, hex standoffs, cable glands, M8 and M12 connectors, and simple bought modules
(printed circuit boards with parts, worm-drive band housings). Every function returns a build123d solid
in millimetres, built along an axis from a stated face, so the model places it with one call.

Dimensions are nominal catalogue values (ISO 7045 pan heads, ISO 7380 button heads, ISO 10642
countersunk heads, ISO 10511 nyloc nuts, ISO 7089 and ISO 7092 washers); threads are plain shanks.
Kept in the repo, not in .kit/ (rollout brief, 2026-10-24).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))

import build123d as b  # noqa: E402

# nominal d: (pan head dk, k), (button head dk, k), (csk head dk, k), (nut s, m nyloc), (washer d2, h), (small washer d2, h)
PAN = {2.5: (5.0, 1.5), 3: (5.6, 1.8), 4: (8.0, 2.4), 5: (9.5, 3.0), 6: (12.0, 3.6)}
BUTTON = {3: (5.7, 1.65), 4: (7.6, 2.2), 5: (9.5, 2.75), 6: (10.5, 3.3)}
CSK = {3: (6.0, 1.7), 4: (8.0, 2.3), 5: (10.0, 2.5), 6: (12.0, 3.3)}
NYLOC = {3: (5.5, 4.0), 4: (7.0, 5.0), 5: (8.0, 5.0), 6: (10.0, 6.0)}
WASHER = {3: (7.0, 0.5), 4: (9.0, 0.8), 5: (10.0, 1.0), 6: (12.0, 1.6)}
INSERT = {3: (4.0, 5.0), 5: (6.8, 8.0)}      # as installed: OD (equal to the printed hole), length


def _rot(axis, sign):
    """Rotation that turns a part built along +Z (head at z = 0, shank toward -Z) to point its shank along
    axis 'x', 'y' or 'z' with the given sign (+1 shank toward +axis)."""
    return {("z", -1): b.Rot(0, 0, 0), ("z", 1): b.Rot(180, 0, 0),
            ("y", 1): b.Rot(90, 0, 0), ("y", -1): b.Rot(-90, 0, 0),
            ("x", 1): b.Rot(0, -90, 0), ("x", -1): b.Rot(0, 90, 0)}[(axis, sign)]


def place(shape, at, axis="z", sign=-1):
    """Place a fastener built along +Z (head on z = 0, shank down -Z) with its seat at `at` and its shank
    running along `axis` toward `sign`."""
    return b.Pos(*at) * _rot(axis, sign) * shape


def _shank(d, length, clear=0.3):
    s = b.Pos(0, 0, -length / 2) * b.Cylinder(d / 2 - clear, length)
    try:
        s = b.chamfer(s.edges().sort_by(b.Axis.Z)[0], min(0.4, d * 0.1))
    except Exception:
        pass
    return s


def pan_screw(d, length):
    """ISO 7045 pan head screw: head from z 0 up to k, shank to -length, with a cross recess."""
    dk, k = PAN[d]
    head = b.Pos(0, 0, k / 2) * b.Cylinder(dk / 2, k)
    try:
        head = b.fillet(head.edges().sort_by(b.Axis.Z)[-1], k * 0.45)
    except Exception:
        pass
    rec = b.Pos(0, 0, k) * (b.Box(dk * 0.5, d * 0.25, k) + b.Box(d * 0.25, dk * 0.5, k))
    return head - rec + _shank(d, length)


def button_screw(d, length):
    """ISO 7380 button head socket screw: domed head z 0 to k, hex socket, shank to -length."""
    dk, k = BUTTON[d]
    head = b.Pos(0, 0, k / 2) * b.Cylinder(dk / 2, k)
    try:
        head = b.fillet(head.edges().sort_by(b.Axis.Z)[-1], k * 0.8)
    except Exception:
        pass
    sock = b.Pos(0, 0, k) * b.extrude(b.RegularPolygon(d * 0.35, 6), -k * 0.6)
    return head - sock + _shank(d, length)


def csk_screw(d, length):
    """ISO 10642 countersunk socket screw: the 90 degree head lies below z 0 (its top face flush at z 0),
    the shank continues to -length measured from the top face."""
    dk, k = CSK[d]
    head = b.Pos(0, 0, -k) * b.Cone(d / 2, dk / 2, k, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
    sock = b.extrude(b.RegularPolygon(d * 0.32, 6), -k * 0.7)
    return head - sock + _shank(d, length)


def nyloc_nut(d):
    """ISO 10511 nyloc nut from z 0 to m (bearing face on z = 0), with its nylon ring band and a clearance bore."""
    s, m = NYLOC[d]
    hexa = b.extrude(b.RegularPolygon(s / math.sqrt(3), 6), m * 0.72)
    ring = b.Pos(0, 0, m * 0.72) * b.extrude(b.Circle(s * 0.47), m * 0.28)
    nut = hexa + ring
    try:
        nut = b.chamfer(nut.edges().sort_by(b.Axis.Z)[0:6], 0.3)
    except Exception:
        pass
    return nut - b.Pos(0, 0, m / 2) * b.Cylinder(d / 2, m + 2)


def hex_nut_small(d, m=None):
    """Plain hex nut (ISO 4032 proportions) from z 0 to m with a clearance bore."""
    s = NYLOC[d][0]
    m = m or 0.8 * d
    nut = b.extrude(b.RegularPolygon(s / math.sqrt(3), 6), m)
    return nut - b.Pos(0, 0, m / 2) * b.Cylinder(d / 2, m + 2)


def washer_small(d, small=False):
    """ISO 7089 (or ISO 7092 small series) plain washer from z 0 to h."""
    d2, h = WASHER[d]
    if small:
        d2 = d2 * 0.82
    return b.extrude(b.Sketch() + b.Circle(d2 / 2) - b.Circle(d * 0.54), h)


def insert(d, length=None):
    """Brass heat-set insert as installed: a knurled sleeve from z 0 down to -length; OD equals the printed hole."""
    od, L = INSERT[d]
    L = length or L
    body = b.Pos(0, 0, -L / 2) * b.Cylinder(od / 2, L) - b.Pos(0, 0, -L / 2) * b.Cylinder(d / 2 + 0.05, L + 2)
    for i in range(3):                       # knurl grooves
        body -= b.Pos(0, 0, -L * (0.25 + 0.25 * i)) * (b.Cylinder(od / 2 + 1, 0.6) - b.Cylinder(od / 2 - 0.35, 0.6))
    return body


def standoff(d, length, af=None, stub=0.0):
    """Hex standoff from z 0 down to -length (female thread bore); optional male stub below it."""
    af = af or (5.5 if d == 3 else 7.0)
    s = b.Pos(0, 0, -length) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), length)
    s -= b.Pos(0, 0, -length / 2) * b.Cylinder(d / 2 - 0.1, length + 2)
    if stub:
        s += b.Pos(0, 0, -length - stub / 2) * b.Cylinder(d / 2 - 0.15, stub)
    return s


def gland(thread=16, seal_d=6.0):
    """Nylon cable gland (EN 62444 class), entry face at z = 0: dome cap and body hex above the wall,
    thread down into the wall (length 8), cable bore seal_d. Returns the gland body; the locknut is separate."""
    t = thread
    af = t + 6
    hexa = b.Pos(0, 0, 0) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), 4.0)
    dome = b.Pos(0, 0, 4.0) * b.Cylinder(t * 0.62, t * 0.55, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
    try:
        dome = b.fillet(dome.edges().sort_by(b.Axis.Z)[-1], t * 0.12)
    except Exception:
        pass
    thr = b.Pos(0, 0, -4.0) * b.Cylinder(t / 2 - 0.1, 8.0)
    return hexa + dome + thr - b.Cylinder(seal_d / 2, 80)


def locknut(thread=16, h=4.0):
    """Gland locknut from z 0 down to -h (inside a wall), bore equal to the thread."""
    af = thread + 6
    return b.Pos(0, 0, -h) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), h) - b.Cylinder(thread / 2, 40)


def m12_plug(length=45.0, d=16.0):
    """M12 5-pin A-coded cable plug along -Z from its mating face at z = 0: knurled coupling nut, grip body,
    strain relief."""
    nut = b.Pos(0, 0, -6) * b.Cylinder(d / 2, 12)
    for i in range(12):                                         # knurl flutes
        a = i * 30
        nut -= b.Pos(d / 2 * math.cos(math.radians(a)), d / 2 * math.sin(math.radians(a)), -6) * b.Cylinder(0.8, 12.5)
    body = b.Pos(0, 0, -12 - (length - 22) / 2) * b.Cylinder(d / 2 - 2, length - 22)
    tail = b.Pos(0, 0, -length + 5) * b.Cone(d / 2 - 2.5, 4.0, 10)
    return nut + body + tail


def m8_plug(length=12.0, d=10.0):
    """M8 4-pin cable plug along -Z from its mating face at z = 0 (knurled nut and body)."""
    nut = b.Pos(0, 0, -3) * b.Cylinder(d / 2, 6)
    for i in range(10):
        a = i * 36
        nut -= b.Pos(d / 2 * math.cos(math.radians(a)), d / 2 * math.sin(math.radians(a)), -3) * b.Cylinder(0.5, 6.5)
    body = b.Pos(0, 0, -6 - (length - 6) / 2) * b.Cylinder(d / 2 - 1.0, length - 6)
    return nut + body


def m8_socket(wall=3.0):
    """M8 4-pin panel socket, front flange at z = 0 against the wall, thread through to -wall, rear nut."""
    flange = b.Pos(0, 0, 1.0) * b.extrude(b.RegularPolygon(11.0 / math.sqrt(3), 6), 2.0, both=True)
    thr = b.Pos(0, 0, 5.0) * b.Cylinder(4.0, 8.0)                 # outside, the plug side
    body = b.Pos(0, 0, -wall / 2) * b.Cylinder(4.0, wall)
    pins = b.Pos(0, 0, 6.0) * b.Cylinder(2.5, 6.0)
    return flange + thr - pins + body


def worm_housing(bw=12.7):
    """Worm-drive band housing with its captive hex screw (stainless), lying along X, centred on the origin,
    base face on y = 0, height +Y."""
    w = bw + 4
    cage = b.Pos(0, 5, 0) * b.Box(18, 10, w)
    cage -= b.Pos(0, 5, 0) * b.Box(20, 6, bw + 0.4)
    screw = b.Pos(0, 6.5, 0) * b.Rot(0, 90, 0) * b.Cylinder(3.0, 22)
    head = b.Pos(12, 6.5, 0) * b.Rot(0, 90, 0) * b.extrude(b.RegularPolygon(7.0 / math.sqrt(3), 6), 4.0, both=True)
    return cage + screw + head


def pcb(w, h, t=1.6, holes=(), parts=()):
    """Printed circuit board in the XZ plane (width w along X, height h along Z, thickness t along -Y from
    y = 0), with mounting holes [(x, z, d)] and components [(x, z, sx, sz, height)] on its -Y face."""
    s = b.Pos(0, -t / 2, 0) * b.Box(w, t, h)
    try:
        s = b.fillet(s.edges().filter_by(b.Axis.Y), 1.5)
    except Exception:
        pass
    for x, z, d in holes:
        s -= b.Pos(x, -t / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(d / 2, t + 2)
    for x, z, sx, sz, hh in parts:
        s += b.Pos(x, -t - hh / 2, z) * b.Box(sx, hh, sz)
    return s


def rounded_box(x0, x1, y0, y1, z0, z1, r=1.0):
    """Axis-aligned box with every edge rounded by r (a moulded or bought module)."""
    s = b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))
    try:
        return b.fillet(s.edges(), r)
    except Exception:
        return s


def tube_z(x, y, z0, z1, od, wall):
    """Round tube along Z between z0 and z1."""
    L = z1 - z0
    return b.Pos(x, y, (z0 + z1) / 2) * (b.Cylinder(od / 2, L) - b.Cylinder(od / 2 - wall, L + 2))


def solid(shape):
    """A fresh Solid wrapper (a solid taken out of a compound will not always write to STEP on its own)."""
    if isinstance(shape, b.Solid):
        return b.Solid(shape.wrapped)
    return shape

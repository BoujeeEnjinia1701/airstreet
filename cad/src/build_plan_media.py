"""AirStreet prototype build plan pictures (AST-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/AST-DWG-101 to 109        making sketches for the made components
    docs/05-build-plan/plate-holes.png     hole positions in the rail and the two adapter plates
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring of the pod (matplotlib)
A single sheet, joint or step can be drawn alone (for example "sheets 103" or "steps 7"), which keeps
memory low on a small machine. Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, pole_stub, FP  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
REPO = "github.com/BoujeeEnjinia1701/airstreet"
D = derived(P)
C = build_components(P, shield=True)


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731

COL = {"rail": "#64748B", "saddle": "#57534E", "band": "#9CA3AF", "plate": "#A8A29E", "arm": "#1D4ED8",
       "body": "#D1D5DB", "lid": "#E5E7EB", "fnd": "#94A3B8", "clip": "#0E7490", "post": "#0891B2", "strut": "#B45309",
       "panel": "#1E3A8A", "pod": "#E7E5E4", "floor": "#A3A3A3", "mesh": "#78716C", "pm": "#0F766E", "no2": "#C2410C",
       "afe": "#16A34A", "tb": "#7C3AED", "splate": "#F5F5F4", "cap": "#D6D3D1", "rod": "#6B7280", "th": "#7C3AED",
       "cable": "#111827", "bolt": "#111827", "pole": "#9CA3AF", "fshield": "#F5F5F4", "gland": "#374151"}

FND_CORE = ("fnd_body", "fnd_lid", "fnd_lugs", "fnd_lug_screws", "fnd_vent", "fnd_glands", "fnd_ports", "fnd_antenna",
            "fnd_mplate", "fnd_mplate_screws", "fnd_cell", "fnd_power", "fnd_ctrl", "fnd_connectors")
CLIPS = ("fnd_plate_clip_r", "fnd_plate_clip_l")
POSTS = ("fnd_post_r", "fnd_post_l", "fnd_strut_r", "fnd_strut_l")
PANEL = ("fnd_panel", "fnd_high_panel_clip_r", "fnd_high_panel_clip_l", "fnd_low_panel_clip_r", "fnd_low_panel_clip_l", "fnd_panel_bolts")
SH = ("shield_plates", "spacers", "rods")


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def pole(z_a=2900.0, z_b=3700.0):
    return part("Street light pole (site)", pole_stub(P, z_a, z_b), COL["pole"])


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "rail": part("Rail", C["rail"].shape, COL["rail"]),
        "saddles": part("V-saddles (2)", S("saddle_low", "saddle_up"), COL["saddle"]),
        "plates": part("Adapter plates (2)", S("lplate", "uplate"), COL["plate"]),
        "arm": part("Cross arm", C["arm"].shape, COL["arm"]),
        "core": part("FieldNode enclosure, built", S(*FND_CORE), COL["fnd"]),
        "clips": part("Plate clips (2), FieldNode", S(*CLIPS), COL["clip"]),
        "posts": part("Posts and struts (4), FieldNode", S(*POSTS), COL["post"]),
        "panel": part("Panel with its clips, FieldNode", S(*PANEL), COL["panel"]),
        "shell": part("Pod shell", S("pod_shell", "pod_glands"), COL["pod"]),
        "afe": part("Front end and terminal block", S("afe", "afe_standoffs", "tblock"), COL["afe"]),
        "floor": part("Sensor floor with PM and NO2 sensors", S("pod_floor", "pm", "no2"), COL["floor"]),
        "mesh": part("Insect mesh", C["mesh"].shape, COL["mesh"]),
        "splates": part("Shield plates, spacers and rods", S(*SH), COL["splate"]),
        "cap": part("Shield cap", C["shield_cap"].shape, COL["cap"]),
        "th": part("T and RH probe on its tube", C["th"].shape, COL["th"]),
        "cables": part("Sensor cables and probe lead", C["cables"].shape, COL["cable"]),
        "bands": part("Band clamps (2)", C["bands"].shape, COL["band"]),
        "fshield": part("Sun shield (hot sites), FieldNode", S("fnd_shield", "fnd_shield_screws"), COL["fshield"]),
    }


ORDER = ["rail", "saddles", "plates", "arm", "core", "clips", "posts", "panel", "shell", "afe", "floor", "mesh",
         "splates", "cap", "th", "cables", "bands", "fshield"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"rail": (0, 0, 0), "saddles": (0, 150, 0), "plates": (0, -70, 0), "arm": (0, -60, -40),
           "core": (0, -230, 30), "clips": (0, -150, 150), "posts": (0, -230, 260), "panel": (0, -300, 430),
           "shell": (-260, -160, -150), "afe": (-260, -160, -280), "floor": (-260, -160, -420), "mesh": (-260, -160, -520),
           "splates": (220, -160, -330), "cap": (220, -160, -140), "th": (220, -160, -500), "cables": (-140, -330, 60),
           "bands": (0, 320, 0), "fshield": (-380, -150, 300)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "AirStreet prototype: every component, pulled apart",
                       subtitle="Numbered in build order; 18 is fitted only at hot sites. Seen from the street side, right and above",
                       elev=16, azim=-58, size=(11, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="AirStreet", date=DATE)
    out = []
    z0 = P["enc_z0"]
    jobs = {}

    jobs["101"] = lambda: bv.component_sheet(
        part("Rail", C["rail"].shape, COL["rail"]), [M["saddles"], M["plates"], M["arm"], M["core"], pole(3050, 3600)],
        dwg_no="AST-DWG-101", title="AirStreet rail: making sketch", material="Aluminium flat bar 40 x 5 mm, 6082 or 6063 class",
        view_shape=b.Pos(0, 0, -P["rail_z"][0]) * C["rail"].shape, inset_view=(18, -60),
        notes=["Cut 451 mm of 40 x 5 mm flat bar; square and deburr the ends.",
               "Heights up from the bottom end; the front is the face away from the pole.",
               "Saddle screws: 5.5 mm, 14 mm each side of centre, 67 and 442 up;",
               "  countersink from the front so M5 countersunk heads sit flush.",
               "Cross arm bolts: 5.5 mm, 10 mm each side of centre, 16.5 up.",
               "Adapter plate bolts: 5.5 mm on the centre line, 119, 169, 316, 386 up",
               "  (plain holes: the countersinks are in the plates).",
               "The saddle centres are 51 and 426 up (375 mm apart).",
               "Fit: saddles behind, plates and cross arm in front; see the build plan.",
               "Check: lay the plates and arm on it; every hole lines up."], **base)

    sd = C["saddle_low"].shape
    jobs["102"] = lambda: bv.component_sheet(
        part("V-saddle", sd, COL["saddle"]), [M["rail"], M["bands"], pole(3080, 3580)],
        dwg_no="AST-DWG-102", title="AirStreet V-saddle (make 2): making sketch", material="ASA, 3D printed, 6 walls, 40 % infill",
        view_shape=b.Pos(0, 0, -P["clamp_z"][0]) * sd, inset_view=(55, -60),
        notes=["Make two. Block 100 wide, 50 tall, 24 deep, with a 140 degree V across",
               "  its full height. The flat back goes on the rail; the V faces the pole.",
               "V: apex 8 mm in front of the back face, 87.9 mm wide at the front face.",
               "Band groove: 14 mm tall, 1.5 mm deep, across the whole back face,",
               "  centred on the height. The band runs in it, between saddle and rail.",
               "Print standing on the 100 x 24 end, so the V profile is on the bed.",
               "Two M5 heat-set inserts, 6.8 mm holes 10 deep in the back face,",
               "  14 mm each side of centre and 16 mm above the middle (lower saddle)",
               "  or below it (upper saddle): print one, turn the other over.",
               "Fit: two M5 x 16 countersunk screws from the front of the rail.",
               "A 140 mm pole touches the V faces 24 mm each side of centre; a 200 mm",
               "  pole 34 mm; an 80 mm pole 14 mm. Never on the V's edges.",
               "Check: on a pole or tube it must not rock."], **base)

    lp, up = C["lplate"].shape, C["uplate"].shape
    jobs["103"] = lambda: bv.component_sheet(
        part("Lower adapter plate", lp, COL["plate"]), [M["rail"], M["core"], M["arm"]],
        dwg_no="AST-DWG-103", title="AirStreet lower adapter plate: making sketch", material="Aluminium sheet 3 mm, 5052 or 6061 class",
        view_shape=b.Pos(0, 0, -(z0 - 24)) * lp, inset_view=(15, 125),
        notes=["Cut 180 x 75 mm from 3 mm sheet; round the corners about 2 mm.",
               "Heights up from the bottom edge; sideways from the centre line.",
               "Lug holes: 5.5 mm, 62 mm each side, 15 up (FieldNode's lower lugs).",
               "Sun shield holes (hot sites): drill 3.3 mm and tap M4, 84 mm each",
               "  side, 64 up. Drill them on every node; they cost nothing.",
               "Rail bolts: 5.5 mm on the centre line, 12 and 62 up, countersunk",
               "  from the front so the M5 heads sit flush under the enclosure.",
               "This is FieldNode's back plate hole pattern for its lower half.",
               "Fit: back face on the rail front, centred; enclosure back sits on",
               "  its front face, bottom of the enclosure 24 above the plate's edge.",
               "Check: the lug holes are 124 mm apart, the shield holes 168 mm."], **base)

    jobs["104"] = lambda: bv.component_sheet(
        part("Upper adapter plate", up, COL["plate"]), [M["rail"], M["core"], M["clips"], M["saddles"]],
        dwg_no="AST-DWG-104", title="AirStreet upper adapter plate: making sketch", material="Aluminium sheet 3 mm, 5052 or 6061 class",
        view_shape=b.Pos(0, 0, -(z0 + 170)) * up, inset_view=(15, 125),
        notes=["Cut 180 x 110 mm from 3 mm sheet; round the corners about 2 mm.",
               "Heights up from the bottom edge; sideways from the centre line.",
               "Sun shield holes (hot sites): drill 3.3 mm, tap M4; 84 each side, 10 up.",
               "Lug holes: 5.5 mm, 62 mm each side, 39 up (FieldNode's upper lugs).",
               "Plate clip holes: 5.5 mm, 65 mm each side, 65 and 95 up.",
               "Rail bolts: 5.5 mm on the centre line, 15 and 85 up, countersunk",
               "  from the front so the M5 heads sit flush.",
               "The top edge is where FieldNode's back plate top edge would be, so",
               "  FieldNode's posts pass it with the same clearance.",
               "Fit: back face on the rail front; enclosure back on its lower 30 mm.",
               "Check: plate clip holes 130 apart across, 30 apart up."], **base)

    arm = C["arm"].shape
    jobs["105"] = lambda: bv.component_sheet(
        part("Cross arm", arm, COL["arm"]), [M["rail"], M["shell"], M["cap"], M["splates"]],
        dwg_no="AST-DWG-105", title="AirStreet cross arm: making sketch", material="Aluminium equal angle 30 x 30 x 3 mm, 6063 class",
        view_shape=b.Pos(-P["arm_x"][0], -D["rail_front"], -D["arm_z"]) * arm, inset_view=(30, -55),
        notes=["Cut 415 mm of 30 x 30 x 3 angle; square and deburr the ends.",
               "Positions from the left end (seen from the street).",
               "Upright leg (goes on the rail): two 5.5 mm holes at 155 and 175,",
               "  16.5 mm up from the underside of the flat leg.",
               "Flat leg (points to the street): 15 mm in front of the back face:",
               "  pod screws 5.5 mm at 25 and 125; probe tube 8 mm at 365;",
               "  cap screws 5.5 mm at 335 and 395.",
               "Fit: upright leg flat on the rail front, its underside 451 mm below",
               "  the rail's top end (flush with the rail's bottom end); two M5",
               "  bolts, heads behind the rail, nyloc nuts inside the angle.",
               "The pod and the shield cap hang under the flat leg on M5 screws",
               "  put in from above.",
               "Check: the flat leg is level when the rail is upright."], **base)

    F = __import__("model").pod_frame(P)
    shell_local = F.inverse() * C["pod_shell"].shape
    jobs["106"] = lambda: bv.component_sheet(
        part("Pod shell", C["pod_shell"].shape, "#A8A29E"), [M["arm"], M["rail"], M["floor"], M["afe"]],
        dwg_no="AST-DWG-106", title="AirStreet pod shell: making sketch", material="ASA, 3D printed, white or light grey, 4 walls",
        view_shape=shell_local, inset_view=(20, -55),
        notes=["Outside 170 wide, 110 deep, 92 tall (walls and roof 3 mm), open at the",
               "  bottom; drip lid 200 x 140 x 3 on top. Print upside down, lid on the bed.",
               "Corner bosses: four 8 mm, 20 tall at the open edge, 7 mm in from the",
               "  sides and ends; M3 heat-set inserts for the sensor floor screws.",
               "Hanging bosses: two 12 mm inside the roof, 50 each side of centre,",
               "  15 from the back face; M5 inserts put in from the top of the lid.",
               "Roof glands: two 16.2 mm holes, 58 from the back face, 36 and 68 right",
               "  of centre (under FieldNode's ports A and B).",
               "Probe socket: 8.2 mm hole in the right wall, 45 from the back face,",
               "  46 above the open edge.",
               "Back wall: four 7 mm bosses, 4 tall, M3 inserts, 76 apart across and",
               "  43 apart up, for the front end standoffs.",
               "Check: the floor fits the open edge all round; inserts square."], **base)

    fl_local = F.inverse() * C["pod_floor"].shape
    jobs["107"] = lambda: bv.component_sheet(
        part("Sensor floor", C["pod_floor"].shape, "#A3A3A3"), [M["shell"], M["mesh"], part("Sensors", S("pm", "no2"), "#D1D5DB")],
        dwg_no="AST-DWG-107", title="AirStreet pod sensor floor: making sketch", material="ASA, 3D printed, 100 % infill",
        view_shape=fl_local, inset_view=(-35, -55),
        notes=["Plate 170 x 110 x 3, printed flat with its features standing up.",
               "Inlet slots: 50 x 50 centred 45 left and 12 forward of centre;",
               "  50 x 40 centred 45 right and 17 forward of centre.",
               "PM sensor cradle, 45 left and 23 back of centre: two ribs 50 long,",
               "  3 thick, 25 tall, 12.5 apart inside; two pads 6 wide, 8 tall, 34",
               "  apart, between the ribs. The sensor stands on the pads, inlet down.",
               "NO2 sensor: 28 mm window 45 right and 24 back of centre, inside a",
               "  collar 38 outside, 32.6 inside, 15 tall. The sensor sits face down.",
               "Corner holes 3.4 mm, 78 each side and 48 forward and back of centre.",
               "Mesh: cut stainless insect mesh 160 x 100; punch the four corner holes;",
               "  it goes under the floor, held by the four M3 screws.",
               "Check: both sensors drop in without force; the floor sits flat."], **base)

    pl0 = C["shield_plates"].shape
    one = pl0 & (b.Pos(P["shield_x"], D["sh_yc"], D["sh_bot"]) * b.Box(130, 130, 4))
    jobs["108"] = lambda: bv.component_sheet(
        part("Shield plate", one, COL["splate"]), [M["cap"], M["arm"], part("Other plates", pl0 - one, "#D1D5DB")],
        dwg_no="AST-DWG-108", title="AirStreet shield plate (make 8): making sketch", material="White ASA, 3D printed, 100 % infill",
        view_shape=b.Pos(-P["shield_x"], -D["sh_yc"], -D["sh_bot"]) * one, inset_view=(20, -55),
        notes=["Make eight. Ring 120 outside, 56 inside, 2 thick, printed flat.",
               "Three 5.5 mm holes on an 84 mm circle, 120 degrees apart; one of",
               "  them on the line from the centre toward the pole.",
               "White plastic reflects the sun; do not paint or use another colour.",
               "Make 24 spacers too: 8 mm outside, 5.5 mm bore, 21 of them 11 long",
               "  and 3 of them 9 long (the top row, under the cap).",
               "Stack: plate, 11 spacer, plate ... 8 plates, then the 9 spacers and",
               "  the cap, all on three M5 rods, 13 mm from plate to plate.",
               "Check: the stack is 13 mm pitch, plates parallel, gaps open."], **base)

    cap = C["shield_cap"].shape
    jobs["109"] = lambda: bv.component_sheet(
        part("Shield cap", cap, COL["cap"]), [M["splates"], M["arm"], M["th"]],
        dwg_no="AST-DWG-109", title="AirStreet shield cap and probe tube: making sketch", material="White ASA, 3D printed; aluminium tube 6 mm",
        view_shape=b.Pos(-P["shield_x"], -D["sh_yc"], -D["sh_cap"]) * cap, inset_view=(25, -55),
        notes=["Cap: disc 124 x 8, printed flat. A 6 mm hole at the centre for the",
               "  probe tube; three 5.5 mm holes on the 84 mm circle (as the plates).",
               "Two M5 heat-set inserts in the top face, 30 each side of centre on",
               "  the line along the cross arm: 6.8 mm holes, 8 deep.",
               "Probe tube: cut 76 mm of 6 mm aluminium tube; deburr inside.",
               "Thread the 4-core probe lead up through it; glue the SHT45 board to",
               "  the lower end with neutral-cure silicone, sensor facing down.",
               "Fit: the tube goes up through the cap and the arm's 8 mm hole; the",
               "  board then hangs 57 mm below the cap, in the middle of the stack.",
               "  A bead of silicone holds the tube in the cap.",
               "Check: the board does not touch any plate (19 mm clear)."], **base)

    for k, f in jobs.items():
        if only and k not in only:
            continue
        out.append(f())
    return out


# ----------------------------------------------------------------- hole layout of rail and plates
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    z0 = P["enc_z0"]
    fig = plt.figure(figsize=(12, 8.6), dpi=150)
    fig.text(0.03, 0.975, "Rail and adapter plates: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.945, "Seen from the street (the front). Full size figures in mm from the model; sideways from each centre line, up from each bottom edge.",
             fontsize=8.5, color=MUT, va="top")

    def holes(shape, yface):
        face = [f for f in shape.faces() if abs(f.center().Y - yface) < 0.01 and f.area > 1e3][0]
        out = []
        for w in face.inner_wires():
            bb = w.bounding_box()
            out.append((bb.center().X, bb.center().Z, bb.size.X))
        return out

    def draw(ax, shape, w, h, zb, title, names):
        ax.set_aspect("equal"); ax.set_axis_off()
        ax.add_patch(Rectangle((-w / 2, 0), w, h, fc="#F5F5F4", ec=INK, lw=1.2))
        ax.axvline(0, color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
        H = holes(shape, D["rail_front"] - (P["plate_t"] if w > 50 else 0))
        xs, zs = set(), set()
        for x, z, d in H:
            zz = z - zb
            import numpy as np
            t_ = np.linspace(0, 2 * np.pi, 60)
            ax.fill(x + d / 2 * np.cos(t_), zz + d / 2 * np.sin(t_), fc="white", ec=INK, lw=1)
            ax.plot([x - d / 2 - 2, x + d / 2 + 2], [zz, zz], color=MUT, lw=0.4)
            ax.plot([x, x], [zz - d / 2 - 2, zz + d / 2 + 2], color=MUT, lw=0.4)
            if x > 0.5:
                xs.add(round(x, 1))
            zs.add(round(zz, 1))
        for i, x in enumerate(sorted(xs)):
            ax.plot([x, x], [0, -6 - 7 * (i % 2)], color=AC, lw=0.4, ls=":")
            ax.text(x, -8 - 7 * (i % 2), f"{x:g}", ha="center", va="top", fontsize=7.5, color=AC)
        prev, stag = -1e9, 0
        for z in sorted(zs):
            stag = (1 - stag) if z - prev < 9 else 0
            prev = z
            xl = -w / 2 - 4 - 16 * stag
            ax.plot([xl + 1, -w / 2], [z, z], color=AC, lw=0.4, ls=":")
            ax.text(xl, z, f"{z:g}", ha="right", va="center", fontsize=7.5, color=AC)
        ax.set_title(title, fontsize=9.5, fontweight="bold", color=INK, loc="left")
        return ax

    # rail: tall and thin, on the left
    ax = fig.add_axes([0.03, 0.08, 0.2, 0.83])
    draw(ax, C["rail"].shape, P["rail"][0], D["rail_len"], P["rail_z"][0], "Rail 40 x 5 x 451", None)
    ax.set_xlim(-55, 40); ax.set_ylim(-25, 460)
    ax = fig.add_axes([0.27, 0.53, 0.42, 0.36])
    draw(ax, C["uplate"].shape, 180, 110, z0 + 170, "Upper adapter plate 180 x 110 x 3", None)
    ax.set_xlim(-110, 95); ax.set_ylim(-25, 115)
    ax = fig.add_axes([0.27, 0.12, 0.42, 0.3])
    draw(ax, C["lplate"].shape, 180, 75, z0 - 24, "Lower adapter plate 180 x 75 x 3", None)
    ax.set_xlim(-110, 95); ax.set_ylim(-25, 80)
    key = [("Rail", ""), ("14 each side, 67 and 442 up", "saddle screws, countersunk from the front"),
           ("10 each side, 16.5 up", "cross arm bolts"), ("centre line, 119, 169, 316, 386 up", "adapter plate bolts"),
           ("", ""), ("Adapter plates", ""), ("62 each side", "FieldNode lug screws, 5.5"),
           ("65 each side (upper only)", "FieldNode plate clip screws, 5.5"), ("84 each side", "sun shield screws, M4 tapped (drill 3.3)"),
           ("centre line", "rail bolts, countersunk from the front"), ("", ""),
           ("All other holes 5.5 mm.", ""), ("Plate holes follow FieldNode's back", ""), ("plate pattern: same parts, same screws.", "")]
    fig.text(0.72, 0.88, "What each hole is", fontsize=9.5, fontweight="bold", color=INK, va="top")
    for i, (a, b_) in enumerate(key):
        bold = b_ == "" and a in ("Rail", "Adapter plates")
        fig.text(0.72, 0.85 - i * 0.033, a, fontsize=8, color=INK, va="top", fontweight="bold" if bold else "normal")
        if b_:
            fig.text(0.735, 0.85 - i * 0.033 - 0.015, b_, fontsize=7.6, color=MUT, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    out = OUT / "plate-holes.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    import build123d as b
    out = []
    win = lambda sh, x0, x1, y0, y1, z0_, z1_: sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0_ + z1_) / 2) * b.Box(x1 - x0, y1 - y0, z1_ - z0_))  # noqa: E731
    z0 = P["enc_z0"]
    rf = D["rail_front"]
    jobs = {}
    zc = P["clamp_z"][1]
    bx_ = (-110, 110, -100, 110, zc - 25, zc + 2)
    jobs["01"] = lambda bx_=bx_: bv.joint([
        part("Pole (site), a hollow tube", win(pole_stub(P) - __import__("model").zcyl(0, 0, 3300, D["R"] - 4, 1200), *bx_), COL["pole"]),
        part("Rail", win(C["rail"].shape, *bx_), COL["rail"]),
        part("V-saddle", win(C["saddle_up"].shape, *bx_), "#A16207"),
        part("Band, in the saddle's groove", win(C["bands"].shape, *bx_), "#B91C1C"),
        part("M5 countersunk screw", win(C["saddle_screws"].shape, *bx_), COL["bolt"])],
        OUT / "joint-01.png", "Joint 1: V-saddle, rail and band on the pole",
        subtitle="Cut just above the upper band, seen from above. The pole bears on both V faces; the band runs between saddle and rail",
        elev=80, azim=-90, size=(8, 6))
    bx_ = (-20, 85, -120, -70, z0 - 30, z0 + 20)
    jobs["02"] = lambda bx_=bx_: bv.joint([
        part("Rail (continues down to the cross arm)", win(C["rail"].shape, -20, 85, -120, -70, z0 - 75, z0 - 24), COL["rail"]),
        part("Lower adapter plate", win(C["lplate"].shape, *bx_), COL["plate"]),
        part("Countersunk M5 bolt, flush under the box", win(C["plate_bolts"].shape, *bx_), COL["bolt"]),
        part("Enclosure (cut)", win(S("fnd_body"), *bx_), COL["body"]),
        part("FieldNode lug and M5 screw", win(S("fnd_lugs", "fnd_lug_screws"), *bx_), "#374151")],
        OUT / "joint-02.png", "Joint 2: lower adapter plate on the rail, with the enclosure lug",
        subtitle="Seen from the street side, right and below. The box back sits flat on the plate; the lug screw misses the rail",
        elev=-25, azim=-50, size=(8, 6))
    bx_ = (-10, 110, -150, -50, z0 + 165, z0 + 300)
    jobs["03"] = lambda bx_=bx_: bv.joint([
        part("Rail (continues up to the upper saddle)", win(C["rail"].shape, -10, 110, -150, -50, z0 + 280, z0 + 300), COL["rail"]),
        part("Upper adapter plate", win(C["uplate"].shape, *bx_), COL["plate"]),
        part("Plate clip (FieldNode)", win(C["fnd_plate_clip_r"].shape, *bx_), "#1D4ED8"),
        part("Post and strut feet (FieldNode)", win(S("fnd_post_r", "fnd_strut_r"), *bx_), COL["post"]),
        part("Enclosure top corner and lug", win(S("fnd_body", "fnd_lid", "fnd_lugs"), *bx_), COL["body"]),
        part("M5 and M6 bolts", win(S("fnd_bracket_bolts", "fnd_lug_screws", "plate_bolts"), *bx_), COL["bolt"])],
        OUT / "joint-03.png", "Joint 3: upper adapter plate, enclosure lug and plate clip (right side)",
        subtitle="Seen from the street side and right. Every FieldNode part lands on the same holes as on its own back plate",
        elev=18, azim=-40, size=(8, 6))
    bx_ = (-180, 60, -260, -75, D["arm_z"] - 30, D["arm_z"] + 45)
    jobs["04"] = lambda bx_=bx_: bv.joint([
        part("Rail", win(C["rail"].shape, -30, 30, -100, -75, D["arm_z"] + 31, D["arm_z"] + 70), COL["rail"]),
        part("Cross arm", win(C["arm"].shape, *bx_), COL["arm"]),
        part("M5 bolts, arm to rail", win(C["arm_bolts"].shape, *bx_), COL["bolt"]),
        part("Pod (cut below its roof)", win(S("pod_shell"), -200, 60, -260, -75, D["arm_z"] - 40, D["arm_z"])
             + win(S("pod_glands"), -200, 60, -260, -75, D["arm_z"] - 40, D["arm_z"] + 30), COL["pod"]),
        part("M5 screws, pod to arm", win(C["pod_screws"].shape, *bx_), "#B91C1C")],
        OUT / "joint-04.png", "Joint 4: cross arm on the rail, and the pod hanging under it",
        subtitle="Seen from the street side, right and above. Two screws from above hold the pod; nothing to reach behind",
        elev=28, azim=-50, size=(8, 6))
    F = __import__("model").pod_frame(P)
    jobs["05"] = lambda bx_=bx_: bv.joint([
        part("Pod shell", C["pod_shell"].shape, COL["pod"]),
        part("Sensor floor", C["pod_floor"].shape, COL["floor"]),
        part("Insect mesh", C["mesh"].shape, COL["mesh"]),
        part("PM sensor, inlet down, on its pads", C["pm"].shape, COL["pm"]),
        part("NO2 sensor, face down in its collar", C["no2"].shape, COL["no2"]),
        part("Front end on four standoffs", S("afe", "afe_standoffs"), COL["afe"]),
        part("Terminal block", C["tblock"].shape, COL["tb"])],
        OUT / "joint-05.png", "Joint 5: inside the pod (cut open front to back)",
        subtitle="Seen from the street side and below. The floor carries both sensors and lifts out with them; the front end stays on the back wall",
        cut="+Y", elev=-12, azim=-62, size=(8, 6))
    scx, scy = P["shield_x"], D["sh_yc"]
    bx_ = (scx - 75, scx + 75, scy - 75, scy + 75, D["sh_bot"] - 20, D["arm_z"] + 25)
    jobs["06"] = lambda bx_=bx_: bv.joint([
        part("Cross arm", win(C["arm"].shape, *bx_), COL["arm"]),
        part("Shield cap", C["shield_cap"].shape, COL["cap"]),
        part("Shield plates (8)", C["shield_plates"].shape, "#E7E5E4"),
        part("Spacers", C["spacers"].shape, "#A8A29E"),
        part("M5 rods and nuts", C["rods"].shape, COL["rod"]),
        part("T and RH probe on its tube", C["th"].shape, COL["th"]),
        part("M5 screws, cap to arm", C["cap_screws"].shape, COL["bolt"])],
        OUT / "joint-06.png", "Joint 6: radiation shield stack (cut open)",
        subtitle="Seen from the street side. Plates on three rods with spacers; the probe hangs in the middle on its tube",
        cut="+Y", elev=12, azim=-80, size=(8, 6))
    bx_ = (-180, 60, -210, -70, D["pod_bot"] + 30, z0 + 5)
    jobs["07"] = lambda bx_=bx_: bv.joint([
        part("Pod shell", win(C["pod_shell"].shape, *bx_), COL["pod"]),
        part("Roof glands and probe socket", win(C["pod_glands"].shape, *bx_), COL["gland"]),
        part("Sensor cables and probe lead", win(C["cables"].shape, *bx_), "#B91C1C"),
        part("FieldNode ports A and B", win(C["fnd_ports"].shape, *bx_), "#D4A017"),
        part("Cross arm", win(C["arm"].shape, *bx_), COL["arm"]),
        part("Antenna whip", win(C["fnd_antenna"].shape, *bx_), "#374151")],
        OUT / "joint-07.png", "Joint 7: cables from the FieldNode ports to the pod",
        subtitle="Seen from the street side and right. Each M12 cable drops straight to a gland in the roof; the whip hangs 15 mm clear",
        elev=12, azim=-35, size=(8, 6))
    bx_ = (55, 89.9, -125, -80, z0 + 155, z0 + 210)
    jobs["08"] = lambda bx_=bx_: bv.joint([
        part("Rail", win(C["rail"].shape, *bx_), COL["rail"]),
        part("Adapter plates", win(S("lplate", "uplate"), *bx_), COL["plate"]),
        part("Enclosure", win(S("fnd_body", "fnd_lid"), *bx_), COL["body"]),
        part("Sun shield flange (side sheet cut away)", win(C["fnd_shield"].shape, *bx_), "#D6D3D1"),
        part("M4 thumb screws", win(C["fnd_shield_screws"].shape, *bx_), COL["bolt"])],
        OUT / "joint-08.png", "Joint 8: sun shield flange on the upper adapter plate (hot sites)",
        subtitle="Right side, side sheet cut away: the flange lies on the plate; the thumb screw goes into the tapped hole",
        elev=25, azim=-15, size=(8, 6))
    for k, f in jobs.items():
        if only and k not in only:
            continue
        out.append(f())
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []
    jobs = {}

    def st(n, done, new, title, sub, **kw):
        jobs[f"{n:02d}"] = lambda: bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw)

    rail = M["rail"]
    st(1, [rail], [mv(part("V-saddles (2)", S("saddle_low", "saddle_up"), COL["saddle"]), (0, 90, 0))],
       "V-saddles onto the rail",
       "Seen from behind. Two M5 countersunk screws each, from the front of the rail into the inserts", elev=18, azim=60, label_done=True)
    sad = M["saddles"]
    st(2, [rail, sad], [mv(part("Adapter plates (2)", S("lplate", "uplate"), COL["plate"]), (0, -90, 0)),
                        mv(part("M5 countersunk bolts (4)", C["plate_bolts"].shape, COL["bolt"]), (0, -140, 0))],
       "adapter plates onto the rail", "Countersunk from the front of the plates, nyloc nuts behind the rail; centred, square",
       elev=18, azim=-55, label_done=False)
    pl = M["plates"]
    st(3, [rail, sad, pl], [mv(M["arm"], (0, -90, 0)), mv(part("M5 bolts (2)", C["arm_bolts"].shape, COL["bolt"]), (0, 70, 0))],
       "cross arm onto the rail", "Flush with the rail's bottom end, flat leg pointing to the street; heads behind the rail",
       elev=18, azim=-55, label_done=False)
    frame = [rail, sad, pl, M["arm"]]
    st(4, frame, [mv(M["core"], (0, -160, 0))], "FieldNode enclosure onto the adapter plates",
       "Enclosure built and closed per FieldNode's plan; four M5 screws through its lugs and the plates, nyloc nuts in front",
       elev=18, azim=-55, label_done=False)
    st(5, frame + [M["core"]], [mv(M["clips"], (0, -70, 0))], "plate clips onto the upper adapter plate",
       "Two M5 screws each from behind the plate, nyloc nuts in front; upright legs forward", elev=20, azim=-40, label_done=False)
    st(6, frame + [M["core"], M["clips"]], [mv(part("Posts (2)", S("fnd_post_r", "fnd_post_l"), COL["post"]), (0, 0, 120)),
                                             mv(part("Struts (2)", S("fnd_strut_r", "fnd_strut_l"), COL["strut"]), (0, -70, 60))],
       "posts and struts onto the plate clips", "As FieldNode: post outside the clip on two M6 bolts, strut inside on one",
       elev=15, azim=-40, label_done=False)
    st(7, frame + [M["core"], M["clips"], M["posts"]], [mv(M["panel"], (0, -90, 170))], "panel onto the posts and struts",
       "Panel clips fitted to the panel first, as FieldNode; one M6 bolt at each post and strut head; check 40 degrees",
       elev=15, azim=-45, label_done=False)
    st(8, [part("Pod shell", C["pod_shell"].shape, COL["pod"])],
       [mv(part("Front end on standoffs", S("afe", "afe_standoffs"), COL["afe"]), (0, 0, -150)),
        mv(part("Terminal block", C["tblock"].shape, COL["tb"]), (0, 0, -110)),
        mv(part("Roof glands and probe socket", C["pod_glands"].shape, COL["gland"]), (0, 0, 60))],
       "fit out the pod shell", "Work with the shell upside down (shown upright): front end and terminal block on the back wall, glands in the roof",
       elev=-25, azim=-60, label_done=True)
    st(9, [part("Sensor floor", C["pod_floor"].shape, COL["floor"])],
       [mv(part("PM sensor", C["pm"].shape, COL["pm"]), (0, 0, 70)), mv(part("NO2 sensor", C["no2"].shape, COL["no2"]), (0, 0, 70))],
       "sensors into the floor", "PM sensor on its pads between the ribs, inlet down; NO2 sensor face down in its collar",
       elev=30, azim=-60, label_done=True)
    shell_done = [part("Pod shell, fitted out", S("pod_shell", "pod_glands", "afe", "afe_standoffs", "tblock"), COL["pod"])]
    st(10, shell_done, [mv(part("Floor with sensors", S("pod_floor", "pm", "no2"), COL["floor"]), (0, 0, -90)),
                        mv(part("Insect mesh", C["mesh"].shape, COL["mesh"]), (0, 0, -150)),
                        mv(part("M3 screws (4)", C["floor_screws"].shape, COL["bolt"]), (0, 0, -200))],
       "close the pod from below", "Wire the sensors first; then floor, mesh and four M3 screws into the corner bosses",
       elev=-25, azim=-60, label_done=False)
    on_frame = frame + [M["core"], M["clips"], M["posts"], M["panel"]]
    pod = part("Pod, complete", S("pod_shell", "pod_glands", "pod_floor", "mesh", "pm", "no2", "afe", "tblock"), COL["pod"])
    st(11, on_frame, [mv(pod, (0, 0, -120)), mv(part("M5 screws (2), from above", C["pod_screws"].shape, COL["bolt"]), (0, 0, 80))],
       "pod onto the cross arm", "Back face against the rail; two M5 screws down through the arm into the pod's inserts",
       elev=18, azim=-50, label_done=False)
    st(12, [part("Shield cap", C["shield_cap"].shape, COL["cap"])],
       [mv(part("Plates, spacers, rods", S(*SH), "#A8A29E"), (0, 0, -90)),
        mv(part("Probe on its tube", C["th"].shape, COL["th"]), (0, 0, -200))],
       "build the radiation shield", "Work with the cap upside down (shown upright): rods through the cap, then spacers and plates in turn; nuts",
       elev=15, azim=-60, label_done=True)
    with_pod = on_frame + [pod]
    shield = part("Radiation shield and probe", S("shield_cap", *SH, "th"), COL["cap"])
    st(13, with_pod, [mv(shield, (0, 0, -120)), mv(part("M5 screws (2), from above", C["cap_screws"].shape, COL["bolt"]), (0, 0, 80))],
       "shield onto the cross arm", "Probe tube up through the arm's hole; two M5 screws down through the arm into the cap",
       elev=18, azim=-50, label_done=False)
    st(14, with_pod + [shield], [mv(M["cables"], (0, -80, 0))], "cables",
       "M12 plugs onto ports A and B, cables down into the roof glands; probe lead along the arm to its socket",
       elev=14, azim=-40, label_done=False)
    full = with_pod + [shield, M["cables"]]
    st(15, full, [mv(M["bands"], (0, 170, 0))], "onto the pole with the bands",
       "Seen from the right. Saddles on the pole; each band round the pole and through its saddle groove; tighten",
       context=[pole(2900, 3700)], elev=15, azim=12, label_done=False)
    st(16, full, [mv(M["fshield"], (0, -170, 0))], "FieldNode sun shield (hot sites only)",
       "Slide it over the enclosure from the street side; flanges flat on both plates; four M4 thumb screws",
       elev=18, azim=-40, label_done=False)
    for k, f in jobs.items():
        if only and k not in only:
            continue
        out.append(f())
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "AirStreet pod: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought sensor boards wired at block level; no circuit board is laid out. All wires 0.25 mm² (24 AWG) stranded, shielded cables to the ports.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((30, 9), 66, 50, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(31.5, 57.8, "Inside the pod (the exchange unit)", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU = "#B91C1C", "#1D4ED8"
    blk(3, 40, 18, 14, "FieldNode port A", "M12, switched 5 V,\nI2C bus A\n(on only for the PM run)", "#D4A017")
    blk(3, 14, 18, 14, "FieldNode port B", "M12, 5 V held on,\nI2C bus B\n(NO2 bias never off)", "#D4A017")
    blk(36, 40, 16, 12, "Terminal block", "5 V, GND, SDA, SCL\nshared by bus A", "#7C3AED")
    blk(62, 44, 14, 11, "PM sensor", "SPS30, 5 V, I2C\n(select pin to GND)", "#0F766E")
    blk(80, 44, 14, 11, "Probe socket", "M8 4-pin\nin the pod wall", "#374151")
    blk(100, 44, 16, 11, "T and RH probe", "SHT45 on its tube,\n0.5 m probe lead", "#7C3AED")
    blk(40, 13, 22, 14, "NO2 front end", "four-electrode\npotentiostat (ISB class)\nwith 16-bit ADC", "#16A34A")
    blk(72, 13, 16, 14, "NO2 sensor", "B4 class, WE, AE,\nreference, counter;\nshort leads", "#C2410C")
    wire([(21, 47), (36, 47)], RED); lab(28.5, 49.2, "M12 cable 1, 0.5 m", RED, "center")
    wire([(21, 45), (36, 45)], BLU)
    wire([(52, 48), (62, 48)], RED); wire([(52, 46), (62, 46)], BLU); lab(57, 50.2, "0.25 mm²", RED, "center")
    wire([(44, 40), (44, 36), (87, 36), (87, 44)], RED); wire([(46, 40), (46, 37.6), (85, 37.6), (85, 44)], BLU)
    lab(66, 34.4, "4 wires to the probe socket", MUT, "center")
    wire([(94, 49.5), (100, 49.5)], "#374151"); lab(97, 52.2, "plug", MUT, "center")
    wire([(21, 21), (40, 21)], RED); wire([(21, 19), (40, 19)], BLU); lab(30.5, 23.4, "M12 cable 2, 0.5 m", RED, "center")
    wire([(62, 20), (72, 20)], "#C2410C", 1.4); lab(67, 22.6, "4 leads, short", "#C2410C", "center")
    ax.text(31, 6.0, "Red: 5 V and ground. Blue: I2C (SDA, SCL). The port pins follow FieldNode's port pin assignment. Check the PM sensor's interface select pin and logic level on its datasheet.",
            fontsize=7.2, color=MUT)
    ax.text(31, 3.6, "Port B must stay on: switching it off removes the NO2 sensor's bias, and it then needs hours to settle.", fontsize=7.2, color="#B45309", fontweight="bold")
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    i = 0
    while i < len(args):
        w = args[i]
        sel = []
        while i + 1 < len(args) and args[i + 1] not in fns:
            sel.append(args[i + 1]); i += 1
        r = fns[w](sel) if sel else fns[w]()
        print(w, "->", r)
        i += 1

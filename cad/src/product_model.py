"""AirStreet product model for photoreal renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.

Every product part is components(CHOSEN) from cad/src/model.py as it is: the D3 model of option A with the
FieldNode core and its 6 W panel on their bracket, the rail, saddles, bands, adapter plates and cross arm, the
sensor pod with its sensors, front end, glands and probe socket, the eight-plate radiation shield with its probe,
the cables and every screw, nut, washer and insert. Only the site is added, as context parts named "(site)": the
140 mm street light pole from below the sidewalk to its lamp arm and luminaire, and a sidewalk slab 3 mm proud of
ground level reaching 150 mm below it; and a 1.75 m mannequin standing on the slab for scale. Ground level is
model z = 0 (the sidewalk surface), so the inlets sit 3.0 m above it as designed. The hero is rendered by
.kit/photoreal.py as an outdoor scene with the sun on the side the camera sees.
No appearance additions: the earlier label and status light are not modelled (they were proposed, not decided).
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "mount" (rail, saddles, bands, plates, arm and their fixings), "fieldnode" (enclosure, lid, lugs, glands,
ports, vent, antenna), "internal" (FieldNode's plate, cell and boards), "panel" (bracket and 6 W panel), "pod",
"shield" (plates, cap, spacers, rods, probe), "cables" and "context" (site and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, round_tube, break_edges  # noqa: E402

TITLE = "AirStreet: street-level air quality node for PM2.5 and NO2"

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=40,-35", "--lens=45"]
_ALL = ["mount", "fieldnode", "internal", "panel", "pod", "shield", "cables"]
RENDER_VIEWS = [
    {"name": "hero", "groups": _ALL + ["context"], "explode": False, "el": 10, "az": -56, "args": _SITE,
     "note": "Site render from the sidewalk, front right and a little above eye level (about 10 deg elevation): the node on a "
             "140 mm street light pole with its inlets 3.0 m above the sidewalk, FieldNode's 6 W panel over the enclosure, the "
             "sensor pod on the cross arm at left and the radiation shield at right; 1.75 m person on the sidewalk for scale"},
    {"name": "studio", "groups": _ALL, "explode": False, "el": 20, "az": -56,
     "note": "Studio render from the front right and above (about 20 deg elevation): rail with two printed V-saddles and "
             "stainless bands, windowed adapter plates carrying the FieldNode enclosure and panel bracket, cross arm with the "
             "pod and the shield hanging from it, sensor cables to the M12 ports"},
    {"name": "detail", "groups": ["pod", "shield", "cables", "mount"], "explode": False, "el": 12, "az": -64,
     "note": "Detail from the front right, slightly above (about 12 deg elevation): the pod with its drip lid, roof glands "
             "and probe socket, the shield's eight plates on three rods under its cap, and the probe lead along the arm"},
]

SITE_Z = (-300.0, 4300.0)


def site():
    """The street as context: the pole with a lamp arm and luminaire, the sidewalk slab and a mannequin."""
    P = M.PARAMS
    out = []
    pole = Pos(0, 0, SITE_Z[0]) * round_tube(P["pole_od"], 4.0, SITE_Z[1] - SITE_Z[0])
    out.append(part("Street light pole, 140 mm (site)", pole, "galvanised", kind="context", group="context"))
    arm = Pos(0, -60, SITE_Z[1] - 120) * Rot(90, 0, 0) * round_tube(60.0, 3.0, 900.0)
    out.append(part("Lamp arm (site)", arm, "galvanised", kind="context", group="context"))
    lum = break_edges(Pos(0, -1020, SITE_Z[1] - 150) * Box(240, 420, 70), 12.0)
    out.append(part("Luminaire (site)", lum, "painted_steel", kind="context", group="context", color="#4B5563"))
    slab = Pos(250, -350, (-150 + 3) / 2) * Box(3600, 2400, 153)
    out.append(part("Sidewalk slab (site)", slab, "concrete", kind="context", group="context"))
    try:
        import context_parts
        man = Pos(650, -800, 3) * Rot(0, 0, -30) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:      # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    comps = [dict(p) for p in M.components(M.CHOSEN) if p["kind"] != "context"]
    return comps + site()


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(len(ps), "parts;", dict(Counter(p["group"] for p in ps)))

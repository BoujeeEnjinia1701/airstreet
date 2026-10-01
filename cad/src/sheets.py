"""AirStreet general arrangement sheet AST-DWG-001, Rev P4 (TRL 3, constructable design AST-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/AST-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is AST-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-30"
DATE_P1 = "2026-09-25"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
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
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly(with_pole=True)
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="AirStreet", title="General arrangement", dwg_no="AST-DWG-001", rev="P4",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="FieldNode core per FND-BLD-001; parts per bom/bom.csv; making sketches AST-DWG-101 to 109. PRELIMINARY",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE_P1, "AC"),
                         ("P2", "DDR-002: FieldNode back plate left off, adapter bars; notes", DATE_P1, "AC"),
                         ("P3", "Layout and labels tidied", DATE_P1, "AC"),
                         ("P4", "DDR-003: design for construction; saddles, plates, cross arm, pod", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    W, Dp, H = P["pod"]
    ew, ed, eh = P["enc"]
    z0 = P["enc_z0"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zi = Z(P["inlet_z"])
    L.append(f'<line x1="{x - 4:.2f}" y1="{zi:.2f}" x2="{x + w + 4:.2f}" y2="{zi:.2f}" stroke="{INK}" stroke-width="0.18" stroke-dasharray="3 1 0.6 1"/>')
    xl = X(bb.min.X) - 5
    L += [ext(X(P["pod_x"] - W / 2), Z(D["pod_top"]), xl - 1, Z(D["pod_top"]))]
    L += dim_v(xl, Z(D["pod_top"]), zi, f"{H:.0f}")
    xl2 = xl - 7
    L += [ext(X(-P["rail"][0] / 2), Z(P["rail_z"][0]), xl2 - 1, Z(P["rail_z"][0])),
          ext(X(-P["panel"][0] / 2), Z(D["panel_top"]), xl2 - 1, Z(D["panel_top"]))]
    L += dim_v(xl2, Z(D["panel_top"]), Z(P["rail_z"][0]), f"{D['overall_h']:.0f} node")
    xr = X(bb.max.X) + 5
    for zz in P["clamp_z"]:
        L.append(ext(X(P["rail"][0] / 2 + 20), Z(zz), xr + 1, Z(zz)))
    L += dim_v(xr, Z(P["clamp_z"][1]), Z(P["clamp_z"][0]), f"{D['clamp_span']:.0f}", side=1)
    L += [ext(X(ew / 2), Z(z0), xr + 8, Z(z0)), ext(X(ew / 2), Z(z0 + eh), xr + 8, Z(z0 + eh))]
    L += dim_v(xr + 7, Z(z0 + eh), Z(z0), f"{eh:.0f}", side=1)
    yb = zi + 12
    L += [ext(X(P["pod_x"] - W / 2), zi, X(P["pod_x"] - W / 2), yb + 1), ext(X(P["pod_x"] + W / 2), zi, X(P["pod_x"] + W / 2), yb + 1)]
    L += dim_h(X(P["pod_x"] - W / 2), X(P["pod_x"] + W / 2), yb, f"{W:.0f}")
    yb2 = yb + 6
    L += [ext(X(0), zi, X(0), yb2 + 1), ext(X(P["shield_x"]), Z(D["sh_bot"]), X(P["shield_x"]), yb2 + 1)]
    L += dim_h(X(0), X(P["shield_x"]), yb2, f"{P['shield_x']:.0f}")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    L.append(_t(Xt(bb.max.X) + 4, Yt(bb.min.Y) + 2.8, "STREET SIDE (-Y); KERB BEYOND", 2.1, 400, INK, "start"))

    # right view (from +X): +Y to the right, Z up
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    R = P["pole_od"] / 2
    zt = Zr(bb.max.Z) - 4
    L += [ext(Yr(-R), Zr(bb.max.Z), Yr(-R), zt - 1), ext(Yr(R), Zr(bb.max.Z), Yr(R), zt - 1)]
    L += dim_h(Yr(-R), Yr(R), zt, f"POLE {P['pole_od']:.0f}")
    zb = Zr(D["sh_bot"]) + 8
    yf = -R - D["offset_front"]
    L += [ext(Yr(yf), Zr(D["sh_bot"]), Yr(yf), zb + 1), ext(Yr(-R), Zr(P["rail_z"][0]), Yr(-R), zb + 1)]
    L += dim_h(Yr(yf), Yr(-R), zb, f"{D['offset_front']:.0f}")
    L.append(_t(Yr(D["panel_cy"]), Zr(D["panel_top"]) - 1.2, f"PANEL TILT {P['tilt']:.0f} DEG", 2.0, 400, INK, "middle"))

    s._layers += L
    s.add_svg(views["iso"], 276, 38, 140, 96, label="Isometric view", sublabel="Not to scale; pole stub shown")
    so, si, stk, pitch, n = P["shield"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Pole {P['pole_range'][0]:.0f} to {P['pole_range'][1]:.0f} OD (design {P['pole_od']:.0f}); two 12.7 stainless bands {D['clamp_span']:.0f} apart, 140 deg V-saddles",
        f"Rail {P['rail'][0]:.0f} x {P['rail'][1]:.0f} x {D['rail_len']:.0f}; two 3 mm adapter plates carry the FieldNode lugs and bracket",
        f"Cross arm 30 x 30 x 3 angle, {D['arm_len']:.0f} long; pod and shield hang under it on screws",
        f"FieldNode core {ew:.0f} x {ed:.0f} x {eh:.0f}, underside {z0:,.0f}; 6 W panel at {P['tilt']:.0f} deg",
        f"Pod {W:.0f} x {Dp:.0f} x {H:.0f} behind mesh, drip lid +{P['lid'][0]:.0f}; FieldNode whip {D['whip_clear']:.0f} clear of the lid",
        f"Inlet plane {P['inlet_z']:,.0f} above sidewalk, chain line in front view (EU 1,500 to 4,000)",
        f"Shield {n} plates {so:.0f} OD at {pitch:.0f} pitch, {P['shield_x']:.0f} from pole axis, {D['offset_front']:.0f} from pole face; T and RH probe at {D['th_z']:,.0f}",
        "M12 port A (switched 5 V): SPS30 and SHT45; port B (5 V held on): NO2 front end",
        "Mass 3.84 kg (R13 not met), frontal area 0.143 m² (AST-CAL-001 v0.3)",
        "Third-angle; front view from the street (-Y); pole on the Z axis",
    ], x=276, y=158, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "AST-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()

---
doc_id: AST-DDR-003
title: AirStreet design for construction
project: AirStreet
doc_type: Design decision record
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish (2026-10-02), with the recommendations for A1 and A3; status kept Draft"
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "A1 carried out: the four lightening steps are in the model, BOM, calculations, drawings and build plan (3.78 kg with the sun shield; R13 met on paper); A1's 3.6 kg figure shown to exclude the sun shield; consequences updated"
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A1 and A3 in Table 3, which are now decided as recommended and recorded in the design decisions register (AST-DEC-001). A2 is a value-engineering note, not a decision; its route back to the target stands.

## Context

On 2026-09-30 Amish asked for a build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of AirStreet (AST-DDR-002) showed what the node does, but at massing level: several parts could not be made or fixed as drawn, and the FieldNode core it hung from has since been made constructable in its own repository (FND-DDR-003), which moved its antenna, gave its enclosure external lugs and rebuilt its panel bracket from angle clips on its back plate.

The changes keep what the node does: the same sensors, front end, shield, inlet height (3.0 m), pole range (80 to 200 mm), clamp positions, FieldNode core, panel and hood, and the same pod exchange for service. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now imports FieldNode's own constructable model (vendored as `cad/src/fieldnode_core.py`) and runs 71 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must stay apart are apart by at least the stated clearance. All 71 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The FieldNode core was an envelope with FieldNode's TRL 3 layout (ports and antenna in one row, whip 58 mm right of centre). FieldNode's constructable core has two rows of penetrations and its whip 30 mm right of centre, which would hang through the pod's drip lid. | The model uses FieldNode's own constructable model, moved into place. The pod moves from 70 to 90 mm left of the pole, so the whip hangs 15 mm clear of the drip lid (23 mm in the concept). | AirStreet builds the FieldNode core exactly as FieldNode does; the pod is the part that can move. |
| P2 | The enclosure was to bolt "straight to the rail", but its four lugs are 124 mm apart across and the rail is 40 mm wide. The two 180 x 25 x 3 mm adapter bars had no holes for FieldNode's bracket, which now starts from angle clips on a flat plate. | Two 3 mm aluminium adapter plates, 180 x 75 and 180 x 110 mm, each bolted to the rail by two M5 countersunk bolts. They carry the hole pattern of FieldNode's back plate for the lugs and the plate clips, and the enclosure back sits flat on both. | FieldNode's lugs, clips, screws and bracket fit unchanged. The plates keep most of the mass saved by leaving off FieldNode's back plate (AST-DDR-002 N2). |
| P3 | FieldNode's sun shield, required at sites above 45 °C (AST-DDR-002 N6), screws into its back plate 40 and 180 mm above the enclosure base; with the back plate left off it had nothing to fix to. | The adapter plate heights are set so that both rows of shield screw holes (M4, tapped) land on them. | The shield fits at a hot site with no extra part. |
| P4 | V-saddles 60 x 40 x 16 mm with a round seat cut to the 140 mm design pole; a round seat cannot seat the 80 to 200 mm range of R11. | Printed ASA V-saddles 100 x 50 x 24 mm with a 140° V. A 140 mm pole touches both faces 24 mm each side of centre; 80 and 200 mm poles at 14 and 34 mm; never on the V's edges. | A shallow V seats the whole range in a part small enough to print; the rail stands off the pole by the same amount as before. |
| P5 | Bands drawn as rings round the pole plus a strap across the rail front, with no path past the saddles; and one worm-drive clamp does not span 80 to 200 mm. | Each band runs round the far side of the pole and through a 14 x 1.5 mm groove across the back of its saddle, between saddle and rail. Bands are cut to length from a 12.7 mm stainless worm-drive band roll with separate housings (487 mm round the 140 mm pole, 326 to 664 mm over the range, plus about 100 mm). | The band pulls the saddle onto the pole and cannot slide off it; one band stock covers every pole in the range. |
| P6 | The saddles had no fixing to the rail. | Two M5 countersunk screws through the rail into heat-set inserts in each saddle. | Keeps the saddles on the rail on the bench and while the bands go on. |
| P7 | The shield arm (20 x 8 mm bar with a gusset) only touched the rail's edge, and the pod had no fixing at all. | One 30 x 30 x 3 mm aluminium angle, 415 mm long, bolted flat to the rail by two M5 bolts. The pod hangs under it on two M5 screws from above into inserts in the pod roof, and the shield cap on two more. The rail now ends at the arm (451 mm, was 565 mm). | One part carries both and every screw is reached from above; a pod exchange is two screws and three plugs (R16). |
| P8 | The pod was a closed solid with its sensors floating inside: there was no way to fit them, and the floor slots left no solid floor to mount the sensors on. | A printed shell (walls, roof and drip lid in one, open at the bottom) and a separate printed sensor floor on four M3 screws into corner bosses, with the mesh clamped under it. The floor carries a cradle that holds the PM sensor on edge 8 mm above the floor, inlet down, and a collar that holds the NO2 sensor face down over a 28 mm window. The inlet slots become 50 x 50 and 50 x 40 mm. The front end stands on four standoffs on the back wall, with a small terminal block beside it. | The sensors drop into the floor from above and the floor closes the pod from below; the concept's sensor positions and inlet faces are kept. |
| P9 | The sensor cables ended on top of the drip lid with no way through it, and the probe lead had no connector, so the pod could not be unplugged for an exchange. | Two M16 glands in the pod roof directly under FieldNode's ports A and B; the probe lead ends in an M8 4-pin plug on a socket in the pod's right wall. | Straight cable drops; the pod unplugs from the probe as the service step (AST-CAL-001 H1) assumes. |
| P10 | Shield plates floated on the rods with no spacers, the cap had no fixing, and the probe hung from nothing. | 24 printed spacers (8 mm outside) on three M5 rods through the cap, nuts top and bottom; the cap screws up under the cross arm; the SHT45 board is glued to the end of a 6 mm aluminium tube that passes up through the cap and an 8 mm hole in the arm, and the lead runs along the arm to the pod. | Plate pitch, count and size are unchanged, so the radiation error result (AST-CAL-001 D) stands. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 3.84 kg on the pole (was 3.26 kg); 4.00 kg with FieldNode's sun shield [F4], [F5]. R13 (3.5 kg) is now **not met**. | FieldNode's constructable core is 0.15 kg heavier as used; the adapter plates, cross arm, larger saddles, pod floor and fixings add the rest. See Table 3, A1. |
| Frontal area | 0.143 m² (was 0.126 m²) against 0.15 m² [F3]; met on paper. | Taken from the model; FieldNode's bracket and the plates show more. |
| Cost | BOM lines 1, 3, 4, 8, 9, 10 and 11 revised: sensor head $303.00 (was $285.00) against the $285 value-engineering target (`budget_usd`); R15 is now **over the target by $18.00** [I1], [I2]. FieldNode core as used $131.00 (FieldNode's $139.00 less its unused pole mounting kit). Whole node $434.00. | Plates, arm, band stock, spacers, inserts, glands, probe socket and fixings. See Table 3, A2. |
| Mounting loads | Cross arm 4.5 MPa, its bolts about 67 N each in a 35 m/s gust, rail 16.4 MPa at the lower clamp, pod screws about 11 N each [G3], [G4], [G6], [G7]. Clamp slip factor 24 [G2]. | New load paths, all with large margins. |
| Drawings | AST-DWG-001 Rev P4; making sketches AST-DWG-101 to 109 added. (Rev P5 and sketches 101, 103, 104 and 108 at P2 after the A1 lightening, 2026-10-02.) | Follows the model. |
| Documents | AST-CAL-001 v0.3, AST-REQ-001 v0.5, AST-PRC-001 v0.5: mass, area, cost, mount and pod figures updated. | Follows the model. |

*Table 3. Items proposed to Amish; A1 and A3 accepted as recommended on 2026-10-02 (A1 with the limit set at 4.0 kg including FieldNode's sun shield).*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Mass on the pole is 3.84 kg (4.00 kg with the sun shield) against R13's 3.5 kg. | (a) raise the R13 limit to 4.0 kg, with the pole owner confirming the load; (b) lighten: print the saddles at 40 % infill, use 40 x 4 mm rail, 1.5 mm shield plates and cut windows in the adapter plates, which gives about 3.6 kg and still misses 3.5 kg; (c) both. | (c): adopt the lightening at TRL 4 and set the limit to 4.0 kg. Accepted 2026-10-02: R13 is 4.0 kg including FieldNode's sun shield, the pole owner is asked to confirm the load, and the four lightening steps are carried into the TRL 4 build. Carried into the design on 2026-10-02 (AST-CAL-001 v0.6 [F8]): 3.62 kg without the sun shield and 3.78 kg with it, so the "about 3.6 kg" above excludes the shield. |
| A2 | Value engineering (a note, not a decision). Sensor head parts cost $303.00 against the $285 value-engineering target (`budget_usd`), $18.00 over ($302.50 and $17.50 after the A1 lightening and repricing, 2026-10-02). | (a) recover the $18 with the open two-channel NO2 front end (about $35 cheaper, PCB work on hold with TRL 4); (b) look for cheaper band hardware and fixings at purchase. | (a) as the route back to the target, with (b) at purchase. |
| A3 | The whip now hangs 15 mm from the pod's drip lid, not 23 mm. | (a) accept, and check the radio link with the pod fitted at TRL 4; (b) move the pod a further 8 mm left, widening the node. | (a). Accepted 2026-10-02: check signal strength with the pod fitted at TRL 4 and move the pod only if that check shows a loss. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan AST-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open decisions are in the register AST-DEC-001.
- Requirement status (AST-CAL-001 v0.3): 1 not met (R13), 1 over the value-engineering target (R15), 5 at risk (R1, R2, R4, R5, R12), 4 met on paper (R8, R9, R10, R16), 4 met by design (R6, R7, R11, R14), R3 withdrawn. With A1 accepted on 2026-10-02, R13's mass limit is 4.0 kg including FieldNode's sun shield: the node meets it with no margin (4.00 kg), so R13 is now at risk rather than not met, and the lightening at TRL 4 gives the margin (AST-REQ-001 v0.7). The lightening was then carried into the model, BOM and calculations on 2026-10-02 (AST-CAL-001 v0.6): 3.78 kg with the sun shield, 0.22 kg under the limit, so R13 is met on paper (AST-REQ-001 v0.8). Status counts are now 1 over the value-engineering target (R15, $17.50), 5 at risk, 5 met on paper, 4 met by design and R3 withdrawn.
- Cross-repo: with register decision 5 approved on 2026-10-02, FieldNode is to be asked to accept its enclosure, plate clips and sun shield on AirStreet's two adapter plates in place of its back plate (this replaces the adapter-bar request of AST-DDR-002 N2), and to keep `cad/src/model.py` stable, since AirStreet carries a copy.
- `media/card.png` and `media/social-preview.png` and the photoreal renders (made on Amish's Mac) show the concept mount and pod and are stale. On 2026-10-02 the appearance model `cad/src/product_model.py` was brought into line with the constructable, lightened design and its render scenes exported; the photoreal renders and the cards are to be made from them on Amish's Mac.

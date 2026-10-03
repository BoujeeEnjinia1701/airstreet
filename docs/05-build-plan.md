---
doc_id: AST-BLD-001
title: AirStreet prototype build plan
project: AirStreet
doc_type: Build plan
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (AST-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Section 2: AST-DDR-003 accepted by Amish (2026-10-02)"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Lightening steps of AST-DDR-003 A1 carried in: 40 x 4 mm rail, windows in the adapter plates, 1.5 mm shield plates and longer spacers, saddles at 40 % infill; mass and cost figures updated; pictures regenerated"
---

# AirStreet prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order; 18, FieldNode's sun shield, is fitted only at hot sites.*

The prototype is one AirStreet node on a short length of 140 mm street light pole (any pole from 80 to 200 mm will do). A FieldNode core, the grey box with its solar panel above it, hangs on an aluminium rail that two bands clamp to the pole. Below the box a cross arm carries the sensor pod on the left, with its particle and NO2 sensors behind insect mesh, and a stack of white plates on the right that shades the temperature and humidity probe. Figure 1 shows the 18 components in the order you make or fit them. Nine are made in a small workshop: the rail, two V-saddles, two adapter plates, the cross arm, the pod shell, the sensor floor, the shield plates with their spacers, and the shield cap with the probe tube. The FieldNode core is built to FieldNode's own build plan. Everything else is bought: bands, sensors, the NO2 front end, cables, glands, mesh and fixings. The work is sawing, drilling, countersinking and tapping aluminium bar, angle and sheet, 3D printing in ASA, setting heat-set inserts, and wiring bought sensor boards with screw terminals. The sensor head parts cost about $302.50 from the bill of materials.

> **Safety:** The FieldNode core holds a lithium iron phosphate cell; follow the safety stops of FieldNode's build plan as well as section 6 here. The NO2 sensor contains an acid electrolyte: do not open, crush or heat it. Cut aluminium and band ends are sharp: deburr everything and wear gloves. Printing ASA and setting heat-set inserts give off fumes; work in a ventilated space. A street light pole carries mains voltage inside: this plan builds on a pole stub on the bench only.

## 2. What changed to make it buildable

The concept showed what the node does; some of its parts could not be made or fixed as drawn, and the FieldNode core it hangs from has since been made buildable in its own right. Each change below keeps what the node does, and all of them are recorded in decision record AST-DDR-003, which Amish accepted on 2026-10-02.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Enclosure to rail | The enclosure bolted straight to a 40 mm rail, and two narrow bars for the panel bracket | Two 3 mm adapter plates on the rail, drilled like FieldNode's back plate for its four lugs, its two plate clips and its sun shield (Figures 4 to 7) | FieldNode's lugs are 124 mm apart and its bracket now starts from clips on a flat plate |
| V-saddles | A round seat cut to fit only the 140 mm pole | A 140° V that seats every pole from 80 to 200 mm on both faces (Figures 3 and 3a) | The pole bears on the V's faces, never on its edges |
| Bands | Rings round the pole with no path past the saddles; one clamp for 80 to 200 mm | Band cut to length from a roll, running in a groove across the back of each saddle (Figure 3a) | The band pulls the saddle onto the pole and cannot slide off |
| Shield arm and pod fixing | A short bar touching the rail's edge; no fixing for the pod | One angle cross arm bolted to the rail; pod and shield hang under it on screws from above (Figures 8 and 9) | Every screw is reached from above; a pod exchange is two screws and three plugs |
| Pod position | 70 mm left of the pole | 90 mm left, so FieldNode's antenna hangs 15 mm clear of the drip lid (Figure 18) | FieldNode's antenna moved 28 mm toward the pod |
| Pod | A closed box with the sensors floating inside | A printed shell open at the bottom and a sensor floor that carries both sensors, screwed on from below over the mesh (Figures 11 to 13) | The sensors can be fitted and the floor comes off as one unit |
| Cable entries | Cables ending on the drip lid | Two glands in the pod roof under FieldNode's ports, and a plug-in socket for the probe lead (Figure 18) | The pod unplugs for exchange |
| Radiation shield | Plates on rods with nothing between them; no fixing for the cap or the probe | Spacers between the plates, rods through the cap, the cap screwed under the arm, and the probe on a tube through the cap (Figures 15 and 16) | The 13 mm plate spacing holds and the probe hangs in the middle |
| Rail | 565 mm | 451 mm, ending at the cross arm | Nothing fixed to the part below the arm |
| Weight | 3.84 kg on the pole, 4.00 kg with FieldNode's sun shield | A 40 x 4 mm rail (was 40 x 5), windows in both adapter plates, 1.5 mm shield plates (was 2 mm) and saddles printed at 40 % infill: 3.62 kg, 3.78 kg with the sun shield (Figures 2, 4, 5 and 14) | The node must stay at or under 4.0 kg on the pole with the sun shield, with some margin |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing in the street, looking at the node; "front" is the side facing the street and "back" the side facing the pole. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Rail

![Figure 2. Making sketch of the rail](../cad/drawings/AST-DWG-101.png)

*Figure 2. Rail making sketch (AST-DWG-101).*

![Figure 2a. Hole positions in the rail and the adapter plates](05-build-plan/plate-holes.png)

*Figure 2a. Hole positions in the rail and both adapter plates, full size figures, seen from the front.*

**What it is and what it is made from.** The upright bar that carries everything: saddles behind it, adapter plates and cross arm in front. Aluminium flat bar 40 x 4 mm, 6082 or 6063 class.

**How to make it.**

1. Cut 451 mm and square and deburr the ends. The end nearer the pod is the bottom.
2. Scribe a centre line down the front face. Mark every hole from Figure 2a, heights up from the bottom end.
3. Saddle screw holes: four 5.5 mm holes, 14 each side of centre, at 67 and 442 up. Countersink them from the front so M5 countersunk heads sit flush.
4. Adapter plate bolt holes: four 5.5 mm holes on the centre line at 119, 169, 316 and 386 up (plain; the countersinks are in the plates).
5. Cross arm bolt holes: two 5.5 mm holes, 10 each side of centre, 16.5 up.
6. Deburr every hole on both faces.

**How it fits the parts next to it.** The saddles sit flat on its back face, centred 51 and 426 up (375 apart). The adapter plates and the cross arm sit flat on its front face.

**Check before moving on.** Lay the plates and the arm on it and look through each hole: every hole lines up without forcing a screw.

### 3.2 V-saddles (make 2)

![Figure 3. Making sketch of the V-saddle](../cad/drawings/AST-DWG-102.png)

*Figure 3. V-saddle making sketch (AST-DWG-102).*

**What it is and what it is made from.** A printed block with a wide V that the pole sits in, one at each band. ASA, printed with six walls and 40 % infill.

**How to make it.**

1. Print each saddle standing on its 100 x 24 end, so the V profile lies on the bed: 100 wide, 50 tall, 24 deep, with a 140° V whose point is 8 mm in front of the back face and which is 87.9 mm wide at the front face.
2. The band groove, 14 tall and 1.5 deep, runs across the whole back face at mid-height; print it in.
3. Two 6.8 mm holes, 10 deep, in the back face, 14 each side of centre and 16 off the middle. Print one saddle with them above the middle (the lower saddle) and one below (the upper saddle), or print two the same and turn one over.
4. Press an M5 heat-set insert into each hole with a soldering iron and insert tip, square to the face, flush or 0.2 below.

**How it fits the parts next to it.**

![Figure 3a. Joint 1: V-saddle, rail and band on the pole](05-build-plan/joint-01.png)

*Figure 3a. Seen from above. The pole bears on both faces of the V; the band runs round the pole and through the groove between saddle and rail.*

The back face sits flat on the back of the rail, held by two M5 x 16 countersunk screws from the front of the rail into the inserts. A 140 mm pole touches the V faces 24 mm each side of centre; a 200 mm pole 34 mm out, an 80 mm pole 14 mm out. The pole never touches the bottom of the V or its outer edges.

**Check before moving on.** Held against a pole or a tube, the saddle must not rock; you should see light at the bottom of the V.

### 3.3 Adapter plates (a lower and an upper)

![Figure 4. Making sketch of the lower adapter plate](../cad/drawings/AST-DWG-103.png)

*Figure 4. Lower adapter plate making sketch (AST-DWG-103).*

![Figure 5. Making sketch of the upper adapter plate](../cad/drawings/AST-DWG-104.png)

*Figure 5. Upper adapter plate making sketch (AST-DWG-104).*

**What they are and what they are made from.** Two plates on the front of the rail that FieldNode's enclosure, plate clips and sun shield fix to, in place of FieldNode's back plate. Aluminium sheet 3 mm, 5052 or 6061 class.

**How to make them.**

1. Cut the lower plate 180 x 75 and the upper plate 180 x 110. Round the corners to about 2 mm and deburr.
2. Scribe a centre line on each. Mark the holes from Figure 2a: heights up from each plate's bottom edge, sideways from the centre line.
3. Lower plate: lug holes 5.5 mm, 62 each side, 15 up; sun shield holes 84 each side, 64 up, drilled 3.3 mm and tapped M4; rail bolt holes 5.5 mm on the centre line at 12 and 62 up, countersunk from the front.
4. Upper plate: sun shield holes 84 each side, 10 up, drilled 3.3 mm and tapped M4; lug holes 5.5 mm, 62 each side, 39 up; plate clip holes 5.5 mm, 65 each side, 65 and 95 up; rail bolt holes 5.5 mm on the centre line at 15 and 85 up, countersunk from the front.
5. Drill the sun shield holes on every node. They cost nothing and let the shield go on later at a hot site.
6. Cut two lightening windows in each plate, one each side of the centre line, from 26 to 50 mm out with 5 mm corner radii: in the lower plate 8 to 67 up (24 x 59), in the upper plate 8 to 102 up (24 x 94). Drill a 10 mm hole in each corner, saw or nibble between them and file the edges smooth. The windows lie behind the enclosure and keep at least 5 mm of metal round every hole and clear of the rail. They save about 60 g.

**How they fit the parts next to them.**

![Figure 6. Joint 2: lower adapter plate, rail and enclosure lug](05-build-plan/joint-02.png)

*Figure 6. The lower plate on the rail, with the enclosure's lower right lug on it. The countersunk bolt sits flush under the enclosure; the lug screw misses the rail.*

![Figure 7. Joint 3: upper adapter plate, enclosure lug and plate clip](05-build-plan/joint-03.png)

*Figure 7. The upper plate carries the enclosure's upper lugs and the bracket's plate clips on the same holes as FieldNode's own back plate.*

Each plate's back face sits flat on the rail's front face, centred, held by two M5 x 16 countersunk bolts from the front with nyloc nuts behind the rail. The lower plate's bottom edge is 24 below the enclosure's bottom; the upper plate's top edge is 280 above it, which is where FieldNode's back plate ends, so FieldNode's posts pass it with the same clearance. The enclosure's back sits flat on both plates and stands 3 mm clear of the rail between them.

**Check before moving on.** Offer the enclosure with its lugs fitted up to both plates on the rail: all four lug holes and both pairs of clip holes line up.

### 3.4 Cross arm

![Figure 8. Making sketch of the cross arm](../cad/drawings/AST-DWG-105.png)

*Figure 8. Cross arm making sketch (AST-DWG-105).*

**What it is and what it is made from.** A length of angle across the bottom of the rail that the pod hangs under on the left and the radiation shield on the right. Aluminium equal angle 30 x 30 x 3 mm, 6063 class.

**How to make it.**

1. Cut 415 mm and square and deburr the ends. Measure every hole from the left end.
2. Upright leg (the one that goes on the rail): two 5.5 mm holes at 155 and 175, 16.5 up from the underside of the flat leg.
3. Flat leg (the one that points to the street), all on a line 15 mm in front of the angle's back face: pod screw holes 5.5 mm at 25 and 125; cap screw holes 5.5 mm at 335 and 395; a probe tube hole 8 mm at 365. Fit a rubber grommet in the 8 mm hole.

**How it fits the parts next to it.**

![Figure 9. Joint 4: cross arm on the rail, with the pod hanging under it](05-build-plan/joint-04.png)

*Figure 9. The upright leg bolts flat to the rail's front; the pod's roof sits flat under the flat leg on two screws put in from above.*

The upright leg sits flat on the front of the rail, its underside flush with the rail's bottom end, held by two M5 x 12 button-head screws from behind the rail with nyloc nuts inside the angle. The flat leg points to the street. The pod's drip lid and the shield cap sit flat against its underside.

**Check before moving on.** With the rail upright, the flat leg is level.

### 3.5 FieldNode core

**What it is.** The FieldNode enclosure with its cell, power modules, controller, ports, glands, vent and antenna; its four lugs; its panel bracket (two plate clips, two posts, two struts and four panel clips); its 6 W panel; and, at hot sites only, its sun shield. Build them to FieldNode's own build plan (FND-BLD-001), sections 3.3 to 3.9 and steps 2, 4, 5, 6 and 9, with these differences:

- Do not make FieldNode's back plate or V-blocks and do not buy its band clamps. The adapter plates of section 3.3 take the back plate's place, on the same hole pattern.
- FieldNode's steps 3, 7, 8, 10 and 11 (enclosure, plate clips, posts and struts, panel and sun shield onto the back plate) become steps 4, 5, 6, 7 and 16 here.
- Port B must be wired so that its 5 V supply stays on all the time; port A is switched for each particle run.

**How it fits the parts next to it.** The enclosure's lugs, the plate clips and the sun shield's flanges fix to the adapter plates exactly as they would to FieldNode's back plate:

![Figure 10. Joint 8: FieldNode's sun shield on the adapter plates](05-build-plan/joint-08.png)

*Figure 10. At a hot site, each folded flange of the shield lies on both adapter plates and an M4 thumb screw goes into each tapped hole.*

**Check before moving on.** FieldNode's own checks in its build plan have passed, and the enclosure is closed with its fuse out.

### 3.6 Pod shell

![Figure 11. Making sketch of the pod shell](../cad/drawings/AST-DWG-106.png)

*Figure 11. Pod shell making sketch (AST-DWG-106).*

**What it is and what it is made from.** The walls, roof and drip lid of the sensor pod in one printed piece, open at the bottom. White or light grey ASA, four walls.

**How to make it.**

1. Print it upside down, the drip lid on the bed: outside 170 wide, 110 deep and 92 tall with 3 mm walls and roof, and a drip lid 200 x 140 x 3 that overhangs by 15 all round. The printer bed must take 200 x 140.
2. Corner bosses: four, 8 mm across and 20 tall, inside the corners at the open edge, 7 in from the sides and ends. Press in M3 heat-set inserts for the floor screws.
3. Hanging bosses: two, 12 mm across, inside the roof, 50 each side of centre and 15 from the back face. Press M5 heat-set inserts in from the top of the drip lid.
4. Back wall: four bosses 7 mm across and 4 tall, 76 apart across and 43 apart up, with M3 heat-set inserts, for the front end's standoffs.
5. Roof gland holes: two 16.2 mm holes, 58 from the back face, 36 and 68 right of the pod's centre, so each sits under one of FieldNode's ports.
6. Probe socket hole: one 8.2 mm hole in the right wall, 45 from the back face and 46 above the open edge.

**How it fits the parts next to it.** Its back face rests against the rail's front; its drip lid sits flat under the cross arm (Figure 9). The sensor floor closes its open bottom (Figure 13).

**Check before moving on.** The sensor floor sits on the open edge all round with no gap, and every insert is square.

### 3.7 Sensor floor and mesh

![Figure 12. Making sketch of the sensor floor](../cad/drawings/AST-DWG-107.png)

*Figure 12. Sensor floor making sketch (AST-DWG-107).*

**What it is and what it is made from.** The pod's floor, which carries both sensors and closes the pod from below behind insect mesh. ASA, printed flat at 100 % infill; stainless insect mesh.

**How to make it.**

1. Print the plate 170 x 110 x 3 with its features standing up from it.
2. Inlet slots: one 50 x 50, centred 45 left and 12 forward of centre; one 50 x 40, centred 45 right and 17 forward of centre.
3. Particle sensor cradle, centred 45 left and 23 back of centre: two ribs 50 long, 3 thick and 25 tall, 12.5 apart inside; between them two pads 6 wide and 8 tall, 34 apart. The sensor stands on edge on the pads with its inlet and outlet face down, 8 mm above the floor and beside the slot.
4. NO2 sensor window, 28 mm, 45 right and 24 back of centre, inside a collar 38 outside, 32.6 inside and 15 tall. The sensor sits face down in the collar on the rim of the window.
5. Corner holes: four 3.4 mm, 78 each side and 48 forward and back of centre.
6. Mesh: cut stainless insect mesh 160 x 100 and punch the four corner holes to match.

**How it fits the parts next to it.**

![Figure 13. Joint 5: inside the pod](05-build-plan/joint-05.png)

*Figure 13. The pod cut open from front to back. The floor carries both sensors; the front end stays on the back wall.*

The floor sits on the shell's open edge and the corner bosses; the mesh lies under it; four M3 x 8 screws with washers go up through mesh and floor into the corner inserts. The particle sensor clears the front end by 1.5 mm and the NO2 sensor by 4.5 mm.

**Check before moving on.** Both sensors drop into the floor without force and sit square; the floor lies flat.

### 3.8 Shield plates and spacers (make 8 plates and 24 spacers)

![Figure 14. Making sketch of the shield plate](../cad/drawings/AST-DWG-108.png)

*Figure 14. Shield plate making sketch (AST-DWG-108).*

**What they are and what they are made from.** Eight white rings stacked 13 mm apart, which shade the probe while letting air through. White ASA, printed flat at 100 % infill. Do not paint them or print them in another colour: the white reflects the sun.

**How to make them.**

1. Print eight rings, 120 outside, 56 inside, 1.5 thick.
2. Each has three 5.5 mm holes on an 84 mm circle, 120° apart; one of them points to the pole when fitted.
3. Print 24 spacers 8 mm outside with a 5.5 mm bore: 21 of them 11.5 long and 3 of them 9.25 long.

**How they fit the parts next to them.** See section 3.9 and Figure 16: plate, 11.5 mm spacer, plate and so on, eight plates, then the three 9.25 mm spacers and the cap, all on three M5 rods.

**Check before moving on.** Every plate is flat; the spacers slide on an M5 rod freely.

### 3.9 Shield cap and probe tube

![Figure 15. Making sketch of the shield cap and probe tube](../cad/drawings/AST-DWG-109.png)

*Figure 15. Shield cap and probe tube making sketch (AST-DWG-109).*

**What they are and what they are made from.** The top of the shield, which screws up under the cross arm, and the tube the temperature and humidity probe hangs on. White ASA, printed flat; aluminium tube 6 mm outside.

**How to make them.**

1. Print the cap: a disc 124 across and 8 thick, with a 6 mm hole at its centre and three 5.5 mm holes on the 84 mm circle, matching the plates.
2. Two 6.8 mm holes, 8 deep, in the top face, 30 each side of centre on a line through the centre; press in M5 heat-set inserts.
3. Cut 76 mm of 6 mm aluminium tube and deburr it inside. Cut three M5 stainless rods 125 long.
4. Thread the 4-core probe lead up through the tube. Solder it to the probe board, then glue the board to the lower end of the tube with neutral-cure silicone, sensor facing down.
5. Fit the M8 plug to the other end of the lead, wired to match the socket of step 9 in section 3.10.

**How they fit the parts next to them.**

![Figure 16. Joint 6: the radiation shield stack](05-build-plan/joint-06.png)

*Figure 16. The stack cut open: plates on three rods with spacers between them, the cap on top, and the probe hanging in the middle on its tube.*

The rods go up through the plates, spacers and cap, with an acorn nut under the bottom plate and a nyloc nut on top of the cap. The cap screws up under the cross arm with two M5 x 10 pan-head screws from above. The tube goes up through the cap's centre hole and the arm's grommet; a bead of silicone holds it in the cap. The probe board then hangs 57 mm below the cap, 19 mm clear of every plate.

**Check before moving on.** Plates parallel and 13 mm apart; the probe board does not touch any plate.

### 3.10 Pod wiring

![Figure 17. Block-level wiring of the pod](05-build-plan/wiring.png)

*Figure 17. Block-level wiring of the pod. No circuit board is laid out at this stage.*

All wires inside the pod are 0.25 mm² (24 AWG) stranded copper, with a ferrule on every screw terminal.

1. Fit the front end board on four M3 x 6 standoffs into the back wall inserts, and the small terminal block on the back wall to its left.
2. Fit the two M16 glands in the roof and the M8 4-pin socket in the right wall, each with its seal outside and its nut inside.
3. Pass each M12 cable's open end down through its roof gland (port A cable through the left gland, port B cable through the right), leaving about 150 mm of slack inside, and tighten the gland on the cable jacket.
4. Port A cable to the terminal block: 5 V, ground, data and clock.
5. Terminal block to the particle sensor: 5 V, ground, data, clock, and its interface select pin to ground for the two-wire interface.
6. Terminal block to the M8 socket: 5 V, ground, data, clock.
7. Port B cable to the front end board: 5 V, ground, data and clock (its own bus, so the NO2 readings never share a bus that switches off).
8. NO2 sensor to the front end: its four electrode pins on short leads, under 100 mm, twisted in pairs, away from the cable glands.
9. Label every wire. The pins of the M12 ports follow FieldNode's port pin assignment.

Before step 8, take the shorting spring off the NO2 sensor's pins only when you are ready to plug it into the front end, and power the front end soon after: the sensor needs its bias held from then on.

**Check before moving on.** Every wire continues end to end; with nothing powered, 5 V reads open to ground on both cables.

### 3.11 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Band clamps (line 3).** 12.7 mm (half inch) stainless worm-drive band from a roll, with two separate worm-drive housings. Each band is about 0.6 m including its tail for poles up to 200 mm; 487 mm goes round a 140 mm pole and saddle.
- **Aluminium (line 3).** Flat bar 40 x 4 mm, 451 mm; sheet 3 mm, 180 x 185 mm; equal angle 30 x 30 x 3 mm, 415 mm.
- **Particle sensor (line 5).** Sensirion SPS30 class, 41 x 41 x 12 mm, 5 V, two-wire (I2C) interface, with its interface cable.
- **NO2 sensor (line 6).** Four-electrode B4 class with an ozone filter (Alphasense NO2-B43F class), with its shorting spring.
- **NO2 front end (line 7).** Four-electrode potentiostat board for B4 sensors (Alphasense ISB class) with a 16-bit ADC on a two-wire bus; the model assumes it is 86 x 55 mm with mounting holes 76 x 43 mm apart.
- **Temperature and humidity probe (line 9).** Sensirion SHT45 on a small breakout board, two-wire bus, 3.3 to 5 V.
- **Sensor cables (line 10).** Two 0.5 m shielded cables with an M12 5-pin A-coded plug; 0.5 m of 4-core shielded probe lead with an M8 4-pin plug.
- **Pod parts (lines 4 and 11).** Stainless insect mesh; two M16 cable glands for 4 to 8 mm cable; an M8 4-pin panel socket; a small 4-way terminal block; a desiccant sachet.
- **Fixings (line 11).** Stainless: 4 x M5 x 16 countersunk screws (saddles); 4 x M5 x 16 countersunk screws with nyloc nuts (adapter plates); 2 x M5 x 12 button-head screws with nyloc nuts (cross arm); 4 x M5 x 10 pan-head screws (pod and cap); 3 x M5 x 125 rods with 3 acorn and 3 nyloc nuts; 8 x M5 and 8 x M3 brass heat-set inserts; 4 x M3 x 8 screws with washers; 4 x M3 x 6 standoffs; an 8 mm grommet; cable ties.
- **FieldNode core (lines 1 and 2).** As FieldNode's bill of materials, without its pole mounting kit.

## 4. Putting it together

In each picture the parts already fitted are grey and the parts being fitted are in colour, with an arrow showing the way they go in. Steps 1 to 14 are done on the bench with the rail lying flat or held upright in a vice; step 15 puts the node on a pole stub.

### Step 1: V-saddles onto the rail

![Step 1](05-build-plan/step-01.png)

Seen from behind. Each saddle's flat back on the back of the rail, its band groove across the rail; two M5 x 16 countersunk screws from the front of the rail into its inserts, snug. Do not overtighten: the inserts are in plastic.

### Step 2: adapter plates onto the rail

![Step 2](05-build-plan/step-02.png)

Each plate centred on the rail's front face; two M5 x 16 countersunk screws from the front of the plate, nyloc nuts behind the rail, tight. The countersunk heads must sit flush or below the plate's face, since the enclosure sits on them.

### Step 3: cross arm onto the rail

![Step 3](05-build-plan/step-03.png)

Upright leg flat on the rail's front face, its underside flush with the rail's bottom end, flat leg pointing to the street. Two M5 x 12 button-head screws from behind the rail, nyloc nuts inside the angle, tight.

### Step 4: FieldNode enclosure onto the adapter plates

![Step 4](05-build-plan/step-04.png)

The enclosure is built, closed and checked to FieldNode's plan, with its lugs on and its fuse out. Hold it flat on both plates, centred, and fit four M5 x 12 button-head screws through the lugs from behind the plates, nyloc nuts in front, snug.

### Step 5: plate clips onto the upper adapter plate

![Step 5](05-build-plan/step-05.png)

Two M5 x 12 button-head screws each from behind the plate, nyloc nuts in front, upright legs standing forward and square to the plate.

### Step 6: posts and struts onto the plate clips

![Step 6](05-build-plan/step-06.png)

As FieldNode's plan: each post against the outside of its clip on two M6 bolts, tight; each strut against the inside on one M6 bolt, snug so it can still swing.

### Step 7: panel onto the posts and struts

![Step 7](05-build-plan/step-07.png)

Fit the four panel clips to the panel first, as FieldNode's plan. With a helper holding the panel, fit one M6 bolt at each post head and one at each strut head; check 40° with an angle finder, then tighten every bracket bolt.

### Step 8: fit out the pod shell

![Step 8](05-build-plan/step-08.png)

Work with the shell upside down on a soft cloth (the picture shows it upright). Fit the front end on its standoffs and the terminal block on the back wall, and the two roof glands and the probe socket, as section 3.10, steps 1 and 2.

### Step 9: sensors into the floor

![Step 9](05-build-plan/step-09.png)

The particle sensor stands on its pads between the ribs, inlet and outlet face down; a cable tie over the ribs holds it. The NO2 sensor goes face down into its collar, shorting spring still on.

### Step 10: close the pod from below

![Step 10](05-build-plan/step-10.png)

Wire the sensors to the front end and the terminal block as section 3.10, steps 4 to 8, leaving the M12 cables out for now if they are not yet through the glands. Add a fresh desiccant sachet. Lay the floor on the shell's open edge, the mesh under it, and fit four M3 x 8 screws with washers into the corner inserts. **Hold point:** no wire pinched between floor and shell; the mesh lies flat over both slots and the NO2 window.

### Step 11: pod onto the cross arm

![Step 11](05-build-plan/step-11.png)

Lift the pod under the arm's left end, its back face against the rail, and fit two M5 x 10 pan-head screws down through the arm into the inserts in its roof, snug.

### Step 12: build the radiation shield

![Step 12](05-build-plan/step-12.png)

Work with the cap upside down (the picture shows it upright). Push the three rods through the cap and fit the nyloc nuts on the cap's top face. Then thread on, in turn, a 9.25 mm spacer on each rod, a plate, 11.5 mm spacers, a plate, and so on to the eighth plate, and fit an acorn nut on each rod, snug. Push the probe tube through the cap's centre hole from below, the probe board in the middle of the stack.

### Step 13: shield onto the cross arm

![Step 13](05-build-plan/step-13.png)

Feed the probe lead and tube up through the arm's grommet, lift the cap flat under the arm's right end, and fit two M5 x 10 pan-head screws down through the arm into the cap's inserts. Seal the tube in the cap with a bead of silicone.

### Step 14: cables

![Step 14](05-build-plan/step-14.png)

Plug each M12 cable into its FieldNode port (port A left, port B right) and tighten the coupling nut by hand; each cable drops straight down to its roof gland.

![Figure 18. Joint 7: cables from the ports to the pod](05-build-plan/joint-07.png)

*Figure 18. Each M12 cable runs straight down to a gland in the pod roof; the probe lead runs along the top of the arm, then down to its socket on the pod's right wall. The antenna whip hangs 15 mm clear of the drip lid.*

Run the probe lead along the top of the arm's flat leg against the upright leg, tie it to the arm every 50 mm, bring it down at the arm's middle and plug it into the pod's socket. **Hold point:** the probe lead does not touch the antenna whip.

### Step 15: onto the pole with the bands

![Step 15](05-build-plan/step-15.png)

Seen from the right. Clamp a pole stub upright to a stand that cannot tip under about 4 kg. Hold the node with both saddles on the pole. Pass each band round the far side of the pole and through its saddle's groove between saddle and rail, fit the housing at the side of the pole where a screwdriver reaches it, and tighten both bands evenly to the band maker's torque; record it. Trim the band tails and file the cut ends. **Hold point:** safety stop S5 in section 6.

### Step 16: FieldNode's sun shield (hot sites only)

![Step 16](05-build-plan/step-16.png)

Slide the shield over the enclosure from the street side until its flanges lie flat on both adapter plates, and fit the four M4 thumb screws into the tapped holes, finger tight.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of AST-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Pole range | R11 | Seat the mount on 80, 140 and 200 mm tubes | Both saddles touch the tube on both V faces; each band closes with adjustment to spare |
| Band torque | R11, R13 | Torque screwdriver on each band housing | The maker's torque is reached with no band slip; value recorded |
| Inlet height | R11 | Measure from the mesh to the pole's ground mark on the stub | The mesh is level and the inlet plane can be set 3.0 m above the sidewalk |
| Mass | R13 | Weigh the node off the pole, with and without FieldNode's sun shield | Recorded; the estimate is 3.62 kg without the shield and 3.78 kg with it, against 4.0 kg with it |
| Port supplies | R9 | Bench supply in place of the cell as FieldNode's plan; measure 5 V at each M12 plug with the pod unplugged | Port A switches on and off from the controller; port B stays on |
| Sensor current | R9 | Pod plugged in; measure each port's current over a particle run | Port A about 55 mA while the particle sensor runs; port B a few milliamps, continuously |
| Readings arrive | R7, R8 | Read every sensor over its bus from the controller | Particle, NO2 working and auxiliary, temperature and humidity values all arrive |
| Drip lid and inlets | R12 | Pour water over the pod from above, then look inside through a slot | No water inside; the mesh covers both slots and the NO2 window |
| Pod exchange | R16 | Time a pod exchange with hand tools: unplug two M12 plugs and the probe plug, two screws out, fit a second pod | 15 minutes or less including the access time allowance |
| Shield stack | R5 | Measure plate spacing and the probe's clearance | 13 mm pitch; probe board clear of every plate |
| Antenna clearance | R8 | Measure whip to drip lid | 15 mm or more |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. FieldNode's own stops.** Every safety stop in FieldNode's build plan (cell, fuse, charger, first charge, radio) applies to the core, at the same points in its build.
- **S2. Before the pod is plugged in.** With the cell out and the fuse out, continuity checked from each M12 plug pin to its board terminal; no short between 5 V and ground on either cable.
- **S3. Before the NO2 sensor's shorting spring comes off.** The front end is wired and ready to power; the sensor is undamaged with no electrolyte on its pins. Wash hands after handling a damaged sensor and dispose of it as its maker directs.
- **S4. Before the radio transmits.** The antenna is connected and matches the pilot region's band.
- **S5. Before the node goes on the pole stub.** Every bolt tight with nyloc nuts where shown, the panel glass whole, sharp edges and band tails deburred. The stub is clamped to a bench or stand that cannot tip under about 4 kg.
- **S6. Before any installation on a street pole (outside this plan).** The pole owner's written permission; a trained crew with a mobile elevating work platform or a secured ladder and a second person; traffic management as local rules require; the pole owner has confirmed the pole can carry about 125 N of wind load 3.3 m up, and a load on the pole of 4.0 kg. Never open the pole's access door or touch its wiring: street light poles carry mains voltage.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade (or a bandsaw); bench vice with soft jaws; bench drill or a drill in a stand; drills 2.5 to 16.2 mm and a step drill; countersink; M4 tap and tap drill; flat and half-round files; deburring tool; scriber, engineer's square, steel rule and calipers; 3D printer with an enclosure that prints ASA on a bed of at least 200 x 140 mm; soldering iron with a heat-set insert tip; band cutter or tin snips; screwdrivers and hex keys; torque screwdriver covering about 1 to 6 N·m; digital angle finder; ferrule crimper and wire strippers; multimeter; bench power supply with an adjustable current limit; scale to 5 kg; stopwatch. FieldNode's build plan lists the tools for the core.

**Skills.** No certified trade is needed. Basic metalwork (marking out, sawing, drilling, countersinking, tapping), 3D printing in ASA, setting heat-set inserts, through-hole soldering and crimping, and care with lithium cells and gas sensors. All circuits are extra-low voltage: 5 V at the sensors and under about 15 V anywhere in the core.

**Workspace.** A bench about 1.2 x 0.6 m; a metalwork corner kept apart from the electronics so chips stay off the boards; a ventilated place for the printer and the insert iron; a stand or vice that holds a pole stub upright.

**Personal protective equipment.** Safety glasses for cutting, drilling, soldering and band cutting; cut-resistant gloves for bar, sheet and band; hearing protection when sawing; no gloves near a turning drill; nitrile gloves to handle a damaged NO2 sensor.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 77 checks), using FieldNode's model vendored as `cad/src/fieldnode_core.py`; STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/AST-DWG-101` to `AST-DWG-109`.
- General arrangement: `cad/drawings/AST-DWG-001.pdf`, Rev P5.
- Calculations: `docs/04-calcs/01-sizing.md` (AST-CAL-001 v0.6) and `docs/04-calcs/sizing.py`: mass [F4], [F5], [F8], band lengths [F7], mounting loads [G2] to [G7], service time [H1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (AST-DDR-003), with AST-DDR-001 and AST-DDR-002; the design decisions register `docs/06-design-decisions.md` (AST-DEC-001).
- Requirements: `docs/03-requirements.md` (AST-REQ-001 v0.8).
- FieldNode core: FieldNode's build plan FND-BLD-001 and calculation note FND-CAL-001 v0.3, in the fieldnode repository.

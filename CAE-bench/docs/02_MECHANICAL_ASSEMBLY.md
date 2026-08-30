# 2 — Mechanical assembly

Build order: **engine first, then bench, then actuator, then sensors.** The engine
must spin freely by hand before anything else is attached to it.

Safety first — read §0 before charging the tank.

---

## 0. Safety

Verbatim from the 2024 assembly manual (Damien Dufour, 6 February 2024):

> Since you'll be dealing with pressurized air, wearing **safety glasses at all times
> is a must**, especially when the external storage tank is being filled or is full.
> […] Given that some engines can reach extremely high RPMs, prioritizing safety
> cannot be overstated. […] Before you run your engine, thoroughly inspect it for air
> leaks.

Three additions from what the archive shows actually happened:

1. **8 bar is the ceiling.** The tank is a converted fire extinguisher.
2. **The engine reaches ~2700 rpm unloaded at the normal operating point**, and over
   7000 rpm in the 10 bar test. Printed parts leaving a rotor at that speed are
   dangerous. Do not stand in the plane of the rotor.
3. Aart's own future-work section: *"running the experiment at full force can not be
   considered safe, the screws in the current connecting piece loosen due to the high
   vibrations and rotational force and get launched at high speed."* **Fit a guard,
   and thread-lock the coupling screws.**

---

## 1. Wankel engine sub-assembly

Print list: mainframe, top cover, rotor, crank. Tough PLA, 0.2 mm layers.

**Step 1 — Graphite the chamber.** Apply graphite to the inside of the
epitrochoid-shaped chamber. Coat it well; the graphite is both the lubricant and the
air seal. Flip the chamber upside down and tap out the excess.

**Step 2 — Bearing into the rotor.** Press one **Bearing B** (6802, 15 × 24 × 5 mm)
into the rotor with your thumbs until it seats.

**Step 3 — Apex seals.** Apply super glue to the inserts at the three corners of the
rotor, then push a **15 mm length of graphite** into each. Sand each corner down
until it is flush with the adjacent face.

**Step 4 — Crank into the rotor.** Insert the crank into the centre of the bearing,
**smaller rod facing down**. It must be a tight fit. *Lateral play in the crank costs
a large amount of efficiency* — this is the single most common build fault.

**Step 5 — Crank bearings.** Place one **Bearing A** (R188 ZZ, 6.35 × 12.7 × 4.76 mm)
on the top of the crank shaft, pushed flush with the extruding edge of the rod. Repeat
on the bottom.

**Step 6 — Rotor into the chamber.** Drop the rotor assembly into the main chamber
with the **gear teeth aligned**. The lower crank bearing sits in the centre pocket of
the main chamber. Twist the top rod by hand: the rotor must sweep the chamber with no
jamming. **If it jams, take it apart and start again** — do not force it.

**Step 7 — Top cover.** Place the top cover on the chamber with all holes aligned to
the cut-out inserts.

**Step 8 — Close it up.** Insert **6 × M3 square nuts** into the inserts of the top
chamber, then screw **6 × M3 screws** in from the underside. Tighten evenly.

Check: the assembled engine should spin for a second or two from a flick of the shaft.

---

## 2. Bench frame

The bench is a 30 × 40 cm wooden plank with everything screwed down to it.

1. Mount the **tank holder** (supplied with the extinguisher) at one end. Screw
   through with 3 × 12 T10 wood screws.
2. Mount the **Arduino holder** near the opposite corner, away from the air line.
3. Mount the **corner bracket** — this carries the engine and, later, the brake.
4. Mount the **engine mounting base** (`Engine mounting base.stl`) to the bracket.
5. Fit the engine to the base. Support the output shaft with the two **5 mm bearings**
   and the **OKFLEX flexible coupling** so that shaft misalignment does not load the
   printed crank.

The flexible coupling matters. It was bought in January 2024 specifically as an
"enhanced mounting strategy" after the rigid mounting caused problems.

---

## 3. Actuator: valve + servo bracket

This is the part `cad/aart-2024/` covers in full. See `docs/CAD.md` for measured
dimensions and `cad/aart-2024/CAEfinal_views.png` for the drawing.

1. **Print `CAEfinal.STL`.** Tough PLA red, **100 % infill, 15 mm/s**, 5 walls,
   0.2 mm layers, **tree support in PVA**, no build-plate adhesion. About 17 h 42 on
   an UltiMaker S5. The 100 % infill is not optional — this part takes the servo
   reaction torque.
2. **Print `CAEconnect.SLDPRT`** (the horn). It screws into the AX-12A horn at the
   top and bottom holes, **16 mm apart**.
3. **Snap the ball valve into the bracket.** The Ø17.87 mm bore in the left wall is a
   tight fit by design: it constrains the valve in every direction but vertical, and
   pressing it up against the servo removes that last degree of freedom.
4. **Mount the AX-12A** along the top of the bracket, secured on both sides.
5. **Bolt the bracket to the plank** through the four Ø3.96 mm feet — **M4**, on the
   33.00 × 44.00 mm pattern.
6. Fit the horn between the servo output and the valve stem. Tolerance here is
   critical; a loose horn shows up as vibration and lost accuracy.

**Design intent, in Aart's words:** the valve is mounted at the same height as the
tubing so the 8 mm line bends as little as possible, raising the tube height by only
1 mm. The side windows exist so the user can see the control input applied to the
valve.

---

## 4. Torque rig (optional, and never used — see the note)

The parts exist and print. Nothing in any report used them.

1. Print `Engine mounting base.stl`, `Torquemotor base complete.stl`,
   `holder friction torquemotor.stl`, one brake rotor (32 mm or 35 mm), one friction
   element (11 mm or 11.2 mm), and `coupling output shaft stabilizer.stl`.
2. The coupling takes the engine output shaft to the brake rotor.
3. The friction element bears on the rotor; the reaction is read by a load cell on a
   known arm.
4. Wire the load cell to an **HX711** and read it on a spare Arduino input.

**Status:** the load cells were bought and fitted to the 2024 bench (they are in
Aart's BOM as `Load cell 500g/1kg`, qty 2). The **load-cell attachment bracket has no
CAD**, and no firmware ever read the channel. Closing this is the single highest-value
improvement to the bench. See `docs/06_KNOWN_ISSUES.md` §T.

---

## 5. Final checks before first run

- [ ] Engine spins freely by hand, no jamming
- [ ] All 6 M3 cover screws tight, square nuts seated
- [ ] Servo bracket bolted down with M4, horn engaged, no play
- [ ] Hand shut-off valve fitted and **closed**
- [ ] All push-fit joints fully inserted (push until the collet clicks, then tug)
- [ ] Soap-water leak test at 2 bar before going to 8
- [ ] Eye protection on
- [ ] Guard between you and the rotor plane

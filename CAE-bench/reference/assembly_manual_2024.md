# Compressed-air engines assembly manual

**Damien Dufour, Mechanical Craftsmanship, 6 February 2024**

Transcribed from `Compressed_air_engine_assembly_manual (4).pdf`. **The technical
drawings are not reproduced** — download the original for those. This manual covers
three engines; the bench in this repository uses the Wankel.

---

## 1. Safety precautions for engine testing and assembly

Before you dive into assembling and testing your engines, it's crucial to understand
and follow certain safety guidelines and procedures.

First off, since you'll be dealing with pressurized air, wearing safety glasses at all
times is a must, especially when the external storage tank is being filled or is full.
This simple precaution ensures that your eyes are protected in case any component
unexpectedly detaches or breaks.

When you're ready to fill and test your engine, it's important to get clearance from a
teaching assistant (TA). Your engine must pass a safety inspection by the TA, who will
check that it's been correctly assembled and is safe for testing. Given that some
engines can reach extremely high RPMs, prioritizing safety cannot be overstated.

Understanding the pressure limits of your engine is critical. Exceeding these limits
can cause severe damage, including parts breaking away or the engine failing
altogether. Before you run your engine, thoroughly inspect it for air leaks. Fixing
these leaks before proceeding is essential to maintain efficiency and prevent damage.
Also, the use of appropriate tools for assembly and adjustments is crucial to ensure
the engine's integrity and your safety.

Finally, make sure to maintain a clean and organized workspace.

---

## 2. Wankel rotary engine

A compressed air-powered, 3D-printed Wankel rotary engine works by combining creative
design with effective energy conversion. Its triangular rotor, which is specially made
to spin inside an epitrochoid-shaped chamber, is essential to how it works. The
pressurized air that is kept in external tanks is drawn in by the engine to start its
cycle. The compressed air expands as it enters the chamber and presses up against the
sides of the rotor, starting it in motion. After being transmitted to a central output
shaft, this rotation provides mechanical power. The expanded air is discharged after
energy transfer, concluding the exhaust phase. The engine is suitable at both low and
high pressures.

### 2.1 Bill of materials

| Part | Description | Qty |
|---|---|---|
| Base cover | Base of the engine, has the extruding pipes and attachment to the clutch system | 1 |
| Rotor | | 1 |
| Crank | | 1 |
| Bearing A | Small bearings | 2 |
| Bearing B | Larger bearing | 1 |
| Top Cover | | 1 |
| Graphite (15 mm) | Comes as a stick, filed down to length | 3 |
| Super Glue | | 1 |
| M3 screw | | 6 |
| M3 square nut | | 6 |

### 2.2 Assembly

**Step 1.** Locate the main epitrochoid-shaped chamber. Apply graphite to the inside
of the chamber. Ensure the chamber is well coated in graphite as it acts as the
lubricant and air sealant. Once thoroughly applied, remove the excess graphite by
flipping the chamber upside down.

**Step 2.** Insert 1 × Bearing B into the rotor by pushing with your thumbs until the
bearing fits snug.

**Step 3.** Apply super glue to the inserts on the 3 corners of the rotor. Following
this, insert a 15 mm piece of graphite into each corner. Using sandpaper, file each
corner down until flush with each adjacent side.

**Step 4.** Insert the crank into the center of the bearing with the smaller rod
facing downwards. Ensure it is a tight and snug fit. This step is crucial as any
lateral movement in the crank can cause the engine to lose a large amount of
efficiency.

**Step 5.** Place 1 × Bearing A on the top of the crank shaft. Push it down the rod
until it is flush with the extruding edge of the rod. Likewise for the bottom, place
1 × Bearing A on the rod and push it down until it is flush with the extruding edge.

**Step 6.** Place the rotary assembly into the main chamber with the gearing teeth
aligned. The bearing on the lower part of the crank should fit in the center pocket of
the main chamber. Once the rotor is in, check for correct rotational movement by
twisting the top rod and ensuring there is no jamming while the rotor spins in the
chamber. If there is jamming, remove the rotor and start again.

**Step 7.** Once the rotor is placed in the chamber without jamming and has a fluid
motion, place the top cover on the chamber, ensuring that all the holes line up with
the cutout inserts.

**Step 8.** Secure the top cover to the main chamber. Insert the 6 M3 nuts into the
inserts of the top chamber. Screw 6 M3 screws from the underside of the engine in
their respective holes. Ensure the top cover is securely attached.

### 2.3 Technical drawings

Not reproduced. The PDF carries dimensioned drawings for the mainframe, the top cover
and the rotor, with the epitrochoid angles called out (20°, 35°, 24.05°, 66.05°).

---

## 3. Single piston engine — summary

Not used on this bench. The PDF gives a full 16-step assembly and an 18-line BOM
including an M1.6 screw, an 8 mm O-ring, a BB bullet used as the inlet valve, brass
tubes, 5 × M2 screws and 120-grit sandpaper. Key technique: sand the cylinder and
piston until no 3D-printing lines are visible and the piston falls out of the chamber
under gravity alone, then graphite both.

## 4. Turbine engine — summary

Not used on this bench. 12-line BOM including 3 × M5 screws, 6 × M5 nuts, 13 spacers,
an M5 threaded drive rod, 2 × Bearing B and rubber sealing tape. Key technique: the
blade openings must face downwards, confirmed by the inserted nut facing the inside of
the chamber — mounted the other way the turbine is highly inefficient and struggles to
spin.

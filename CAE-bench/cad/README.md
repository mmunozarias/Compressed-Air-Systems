# CAD

## What is here

`aart-2024/` — the servo and valve bracket, complete, byte-exact from Aart van
Werven's repository. This is the only subassembly whose CAD survived with its author.

| File | What |
|---|---|
| `CAEfinal.STL` | the bracket, mesh form, 4188 triangles |
| `CAE(1).SLDPRT` | SolidWorks source for the bracket |
| `CAEconnect.SLDPRT` | SolidWorks source for the servo horn |
| `UMS5_CAE8.3mf` | Cura 5.7.1 project, sliced, with the full print profile |
| `CAEfinal_views.png` | measured orthographic and isometric views |
| `UMS5_CAE8_thumbnail.png` | Cura's own render |

Both `.SLDPRT` files are post-2015 compressed SolidWorks containers. They open in
SolidWorks and nowhere else; there is no extractable preview or neutral geometry.
If you do not have SolidWorks, work from `CAEfinal.STL` and the measurements below.

## Measured geometry — CAEfinal.STL

Taken from the mesh, not from the report.

```
bounding box      78.00 x 45.00 x 53.00 mm
triangles         4188
volume            49.63 cm3 solid
surface area      198.46 cm2
mass in PLA       61.5 g at 100% infill, 1.24 g/cm3

valve bore        D 17.87 mm, axis along X
                  centre at Y 12.96, Z 26.46

mounting holes    4 x D 3.96 mm   <- M4 clearance, the report's "M2" is wrong
                  X 16.48 and 49.48   (33.00 mm apart)
                  Z  4.49 and 48.49   (44.00 mm apart)

top plate         carries the AX-12A screw pattern and the horn slot
horn screws       16 mm apart, into the AX-12A horn
```

## Print profile, recovered from the 3MF

Cura 5.7.1, UltiMaker S5, dual extrusion.

```
global            layer_height 0.2 · adhesion_type none · prime_tower True
                  support_enable True · support_structure tree
left  (AA 0.4)    Tough PLA Red · infill 100% · speed 15 mm/s · walls 5 · support infill 40%
right (BB 0.4)    PVA           · infill  70% · speed 50 mm/s · walls 5 · support infill 10%
print time        17 h 42
```

**The part is on the left extruder.** Table II of the 2024 report quotes the right
extruder's numbers (70 % / 50 mm/s), which describe the PVA support, not the part.
Print at 100 % infill; this bracket takes the servo reaction torque.

## What is not here

`wankel-2023/`, `pneumatics/` and `torquemeter/` are empty placeholders. Those files
are binary and could not be pulled programmatically. Every download link is in
`MISSING_FILES.md` section C.

# 1 — Bill of materials

Everything needed to build one compressed-air Wankel engine test bench, split by
discipline. Two sources are merged here: the **TA bench BOM** from
`BoM_experimentalSetup_MCDC.xlsx` (the setup as actually built, with quantities and
unit costs) and **Appendix A of Aart van Werven's 2024 report** (the setup after the
electronics rebuild). Where they disagree, both are shown.

Prices are as paid, 2023–24, in EUR unless the source quoted USD.

---

## 1.1 Pneumatic parts

| # | Part | Spec | Qty | Unit | Notes |
|---|------|------|-----|------|-------|
| P1 | Air tank | Smartwares 10.014.68 ABC powder fire extinguisher, 2 kg — tank only, contents removed | 1 | €36.99 | This is the "pneumatic battery". A 1 kg version (10.018.56, €29.00) was also used. Maximum working pressure 8 bar in this application. |
| P2 | Tank outlet adapter | 3D printed, G7/8-14 to G1/8-28 | 1 | printed | `g78p14_to_g18p28_ASPART.STL`. Threads onto the extinguisher valve body. |
| P3 | Pneumatic tubing | HUAZIZ PU hose, 8 mm OD / 5 mm ID, blue | ~70 cm | €15.66 / 12 m | 10–12 m rolls were bought; a bench needs under a metre. |
| P4 | Straight push-fit fittings | TAILONZ PC8-01, 8 mm tube OD × 1/8 BSP male | 6–10 | €9.99 / 10 | The workhorse fitting of the whole rig. |
| P5 | Elbow push-fit fittings | TAILONZ male elbow, 8 mm OD × 1/8 BSP | 2–4 | €13.49 | For routing around the plank. |
| P6 | T-split | G1/8 pneumatic T-piece, or IQS R1/4 to 8 mm tee | 1 | €38.72 / set | Splits the line to the pressure sensor. |
| P7 | Quick connectors | 8 mm to 1/4 BSP adapters | 2 | €9.99 / 10 | Compressor side. |
| P8 | Hand shut-off valve | TAILONZ BVU-8, 8 mm OD ball valve, push-to-connect | 1 | €18.99 | Master isolation. Always fit one. |
| P9 | **Throttle valve (the actuator)** | TAILONZ BVU-8 8 mm OD ball valve — a second unit, driven by the servo | 1 | €9.99 | This is the control element. See §1.5 and `docs/03_PNEUMATIC_CIRCUIT.md`. |
| P10 | O-ring set | NBR, 32 sizes, 419 pieces | 1 set | €17.45 | Sealing the printed adapters. Sizes 1 and 2 in the TA BOM, ×2 and ×4. |
| P11 | Compressor | HBM, with 5-piece air tool set for the hose and couplings | 1 | €26.90 (accessories) | Any 8 bar workshop compressor. |

> **Safety.** The tank is a repurposed fire extinguisher. Do not exceed **8 bar**.
> Wear eye protection whenever the tank is charged. See §1 of the assembly manual
> in `reference/`.

---

## 1.2 Mechanical parts — the engine

The Wankel is fully 3D printed apart from bearings and fasteners.

| # | Part | Spec | Qty | Source |
|---|------|------|-----|--------|
| M1 | Base cover / mainframe | PLA, printed | 1 | `Wankel mainframe.stl` |
| M2 | Top cover | PLA, printed | 1 | `Wankel topcover.stl` |
| M3 | Rotor | PLA, printed | 1 | `rotor.step.SLDPRT` |
| M4 | Crank / eccentric shaft | PLA, printed | 1 | `crank rotary.SLDPRT`, or `crank rotary_full_thread.STL` |
| M5 | Output shaft | PLA, printed | 1 | `outputshaft wankel redesigned.stl` |
| M6 | Bearing A — small | **IBB R188 ZZ, 6.35 × 12.7 × 4.76 mm** | 2 | Lagerkoning.nl, €82.45 / pack |
| M7 | Bearing B — large | IBB 6802 / 61802 2RS, 15 × 24 × 5 mm | 1 | Lagerkoning.nl, €32.28 |
| M8 | Apex seals | Graphite stick, 15 mm lengths, filed flush | 3 | STAEDTLER Mars Micro 1.3 mm HB, €7.67 |
| M9 | Super glue | any cyanoacrylate | 1 | €11.99 / 18 |
| M10 | Cover screws | **M3 × 12** | 6 | with M3 square nuts |
| M11 | Cover nuts | M3 DIN557 square nuts, SS304 | 6 | €6.10 / 100 |

> **Bearing substitution, February 2024.** The original spec was IBB R188
> 6.35 × 12.7 × **3.18** mm. It was replaced by **R188 ZZ 6.35 × 12.7 × 4.76 mm**.
> The 4.76 mm width is what is on the bench now. Ordering the 3.18 mm part will not fit.

---

## 1.3 Mechanical parts — the bench frame

| # | Part | Spec | Qty | Unit |
|---|------|------|-----|------|
| F1 | Base plank | wood, 30 × 40 cm | 1 | €5.25 |
| F2 | Corner bracket | Alberts 330330, heavy, zinc | 1 | €15.13 |
| F3 | M5 threaded rod | for the load arm / mounting | 1 | €5.48 |
| F4 | M5 nuts | Jeboler DIN 985 nylon-insert lock nuts, A2 | 2 | €12.52 / 100 |
| F5 | Wood screws | 3 × 12 T10 | 19 | €7.79 / 200 |
| F6 | Bracket mounting screws | **M4** — see the warning below | 4 | — |
| F7 | 5 mm bearing | for the output shaft support | 2 | €9.56 / 20 |
| F8 | Flexible shaft coupling | OKFLEX | 1 | €24.15 |
| F9 | Tank holder | supplied with the extinguisher | 1 | included |
| F10 | Arduino holder | supplied with the board | 1 | included |
| F11 | Tube holders | printed | 4 | **no CAD survives** |

> **M4, not M2.** Aart's report §IV-D-1 says the servo bracket is secured with
> "4 4-m2-screws". The holes in `CAEfinal.STL` measure **Ø3.96 mm**, which is M4
> clearance. Buy M4.

---

## 1.4 Sensors

| # | Sensor | Spec | Qty | Unit | Interface |
|---|--------|------|-----|------|-----------|
| S1 | Flow | **SENSTREE G1/2 brass water flow sensor** | 1 | €16.11 | Digital pulse, 5 V. Pulse-per-litre constant 11 for water (see the calibration note). |
| S2 | Pressure | **G1/4 pressure transducer, 5 V in, 0.5–4.5 V out, 0–100 psi** | 1 | €19.07 | Analog. |
| S3 | Speed | **SHARP GP1A57HRJ00F photo interrupter** + SparkFun breakout | 1 | €16.85 + €5.85 | Digital, interrupt-driven. |
| S4 | Torque / force | **Load cell 500 g** (B0CJ93Y21V, €18.33) and **1 kg** (HALJIA, €7.99 ×2), plus a 100 g unit (€10.60) | 1–2 | — | Needs an **HX711** amplifier (ICQUANZX, €6.99). *Bought and fitted; never wired into the data acquisition. See `docs/06_KNOWN_ISSUES.md`.* |
| S5 | Sensor adapters | printed: G1/4-to-flowsensor, flow/pressure-to-G1/4 | 1 each | printed | `adapter pneumatic flow pressure sensor v2.stl`, `connector tube to flow sensor 1_8 v1.stl` |
| S6 | Sensor holder, IR holder, IR interruptor disc | printed | 1 each | printed | **no CAD survives — must be redesigned** |

> **The flow sensor is a water turbine used on air.** Its 11 pulses/litre constant
> does not transfer to a compressible fluid. Treat all flow readings as indicative
> until the sensor is calibrated against a known air flow. The 2023 team calibrated
> it by the choked-flow method; see `docs/04_SENSORS_AND_CALIBRATION.md`.

---

## 1.5 Actuator

Two generations exist. Build the 2024 one.

| Generation | Servo | Stall torque | Notes |
|---|---|---|---|
| 2023 | SpringRC **SR431** (from the Braccio arm kit) | 1.22 N·m @ 4.8 V, 1.45 N·m @ 6.0 V | Imprecise, vibrates at high flow, prone to failure. Replaced. |
| **2024 (build this)** | **DYNAMIXEL AX-12A** | **1.5 N·m @ 12 V** | €19.07. TTL protocol 1, ID 0, baud 1 000 000. |

The AX-12A needs three more items, all Reichelt:

| # | Part | Unit |
|---|------|------|
| A1 | DYNAMIXEL **U2D2** USB-to-TTL interface | €56.62 |
| A2 | **U2S2 PHB** Dynamixel U2D2 Power Hub | €40.62 |
| A3 | **SMPS 12 V 5 A** Dynamixel power adapter | €46.72 |

Plus two printed parts: the **valve + motor holder** (`CAEfinal.STL`) and the **horn**
that couples the servo output to the valve stem (`CAEconnect.SLDPRT`), screwed into
the AX-12A horn at two holes 16 mm apart.

---

## 1.6 Electrical and control

| # | Part | Spec | Qty | Unit |
|---|------|------|-----|------|
| E1 | Microcontroller | **Arduino Uno Rev 3** | 1 | €26.50 |
| E2 | Host computer | Any Windows/Linux PC. A **Raspberry Pi 5** was used in 2024 but Aart's own conclusion is that it "proved to be unnecessary, since the same functionality is achieved by running the code on a laptop or PC". | 1 | — |
| E3 | Breadboard | AZDelivery mini, 400 pin | 1 | €3.99 |
| E4 | Jumper wires | male/female sets, flexible | 1 set | €16.20 |
| E5 | Crimping tool + Dupont connectors | Homca SN-28B, 2030 connectors | 1 | €38.99 |
| E6 | 9 V battery clip to 2.1 mm DC jack | for standalone power | 1 | €10.75 |
| E7 | HX711 load-cell amplifier | ICQUANZX breakout | 1 | €6.99 |
| E8 | PVC insulation tape | | 1 | — |

---

## 1.7 Consumables and tooling

| Item | Spec |
|------|------|
| Filament, part | **UltiMaker Tough PLA, red** |
| Filament, support | **UltiMaker PVA** (water soluble) |
| Printer | UltiMaker S5 (S3 / S7 also used), AA 0.4 and BB 0.4 cores |
| Sandpaper | 120 grit, for the piston and turbine variants |
| Magnetic bit holder | 60 mm, 1/4" |
| Graphite | see M8 |

---

## 1.8 Complete printed-part list

| Part | Qty | CAD available? | File |
|------|-----|----------------|------|
| Wankel housing / mainframe | 1 (4 printed per cohort) | yes | `Wankel mainframe.stl` |
| Wankel top cover | 1 | yes | `Wankel topcover.stl` |
| Rotor | 1 | yes | `rotor.step.SLDPRT` + 8 iterations |
| Crank / eccentric | 1 | yes | `crank rotary.SLDPRT` |
| Output shaft | 1 | yes | `outputshaft wankel redesigned.stl` |
| Wankel frame | 1 | yes | `mainframe_wankel.step` |
| Valve + motor holder | 1 | **yes, in this repo** | `cad/aart-2024/CAEfinal.STL` |
| Servo horn / coupler | 1 | **yes, in this repo** | `cad/aart-2024/CAEconnect.SLDPRT` |
| Fire extinguisher adapter | 1 | probable | `g78p14_to_g18p28_ASPART.STL` |
| G1/4 to flow-sensor adapter | 1 | probable | `adapter pneumatic flow pressure sensor v2.stl` |
| Flow/pressure sensor to G1/4 | 1 | probable | `connector tube to flow sensor 1_8 v1.stl` |
| Throttle valve frame | 1 | yes | `frame_updated.stl` (supersedes `frame_flowvalve.stl`) |
| Throttle valve adapter | 1 | yes | `adapter_flowvalve.stl` |
| **Tube holder** | 4 | **NO** | — |
| **Sensor holder** | 1 | **NO** | — |
| **IR-sensor holder** | 1 | **NO** | — |
| **IR-sensor interruptor disc** | 1 | **NO** | — |
| **Load-cell attachment** | 2 | **NO** | — |
| Torquemeter base plate | 1 | yes | `Torquemotor base complete.stl` |
| Torquemeter clutch | 2 | yes | `friction part 11mm.stl`, `friction thingy 11.2mm.stl` |
| Torque meter holder | 1 | yes | `holder friction torquemotor.stl` |
| Brake rotor | 1 | yes | `Rotor Torquemotor 35mm.stl` or the 32 mm variant |
| Output shaft stabiliser | 1 | yes | `coupling output shaft stabilizer.stl` |
| Engine mounting base | 1 | yes | `Engine mounting base.stl` |

**Five printed part types have no CAD in any archive.** All five carry an
instrument. They are the tube holder, sensor holder, IR-sensor holder, IR
interruptor disc and load-cell attachment. See `MISSING_FILES.md`.

---

## 1.9 Approximate cost of one bench

Taking one of each item at the unit prices above and amortising the pack purchases,
a single bench is roughly **€300–350** in bought parts, plus about €11 of filament.
The dominant costs are the Dynamixel chain (U2D2 + U2S2 + SMPS + AX-12A ≈ €163) and
the sensors (≈ €60). The 2023 SpringRC generation was far cheaper but is the reason
the servo was replaced.

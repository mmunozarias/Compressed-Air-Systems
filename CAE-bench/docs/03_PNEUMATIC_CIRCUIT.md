# 3 — Pneumatic circuit

## 3.1 The line, in order

```
  [ Fire extinguisher tank, 8 bar max ]
              |
              |  G7/8-14 outlet
        ( P2 ) printed adapter  g78p14_to_g18p28_ASPART.STL   -> G1/8
              |
        ( P4 ) PC8-01 straight fitting, 1/8 BSP -> 8 mm push-fit
              |
        ( P3 ) 8 mm OD / 5 mm ID PU hose
              |
        ( P6 ) G1/8 T-split ----------------> ( S2 ) PRESSURE SENSOR
              |                                     G1/4, 0-100 psi, analog
              |
        ( S1 ) FLOW SENSOR, SENSTREE G1/2
              |    via printed adapters S5
              |
        ( P8 ) HAND BALL VALVE   <- master isolation, operator controlled
              |
        ( P9 ) SERVO BALL VALVE  <- THE CONTROL ELEMENT, driven by the AX-12A
              |                     mounted in CAEfinal.STL
              |
        [ WANKEL ENGINE inlet port ]
              |
        exhaust to atmosphere
              |
      output shaft --> ( S3 ) IR PHOTO INTERRUPTER (speed)
                   --> optional brake + load cell (torque)
```

## 3.2 Notes that are easy to get wrong

**The pressure sensor reads line pressure, not tank pressure.** In the 2024 data the
open-loop runs peak at only 2.4-2.6 bar while the closed-loop runs reach 6.1-7.4 bar,
from the same tank charge. That is the pressure drop across the flow sensor and tubing
at high flow. If you want true tank pressure, tee the sensor in *before* the flow
sensor, or fit a second transducer.

**Keep the bends out of the 8 mm line.** The bracket was designed to raise the tube
height by only 1 mm precisely to avoid this. Every bend costs flow.

**Seal the printed adapters with O-rings, not tape.** The O-ring set (P10) was bought
for this. PTFE tape on a printed thread tends to shred.

**Leak test before every session.** Aart's predecessors lost measurement days to
leaks. Soap water at 2 bar, then work up.

## 3.3 Operating points on record

| Condition | Tank / line pressure | Speed (corrected) | Flow (corrected) |
|---|---|---|---|
| Open loop, valve wide | 2.4-2.6 bar at the sensor | 2655-3038 rpm plateau | ~2540-2700 L/h |
| Closed loop, setpoint 200 logged | 5.0-5.3 bar at the sensor | ~960 rpm | ~250-475 L/h |
| High-pressure limit test | 10.1 bar peak | up to ~7700 rpm peak | ~4700 L/h peak |

All speeds and flows above are **corrected** figures. The raw logs are wrong by fixed
factors; see `docs/06_KNOWN_ISSUES.md` before using any number from `data/raw-2024/`.

## 3.4 Valve angle and flow area

The throttle is a quarter-turn ball valve. Its flow area is **not** linear in angle:
it is the overlap of two circular apertures. Max Kloosterman measured a valve of the
same family through a microscope in 2 .5 degree steps:

| Rotation from fully open | Aperture, % of maximum |
|---|---|
| 0 deg | 100 % |
| 10 deg | 79 % |
| 20 deg | 57 % |
| 30 deg | 33 % |
| **40 deg** | **17 %** |
| **50 deg** | **5.7 %** |
| 55 deg | 1.5 % |

The pure two-circle geometry over-predicts badly (46 % where the real valve is 3 %
open). The empirical fit that works is the lens area multiplied by (1 - theta/60 deg).

**Consequence for control:** the 2024 bench settles at 43-44 degrees from open, which
is about **13 % of maximum aperture** — on the steep part of the curve, with almost no
margin before the engine stalls. Any controller for this rig should command *area*,
not angle, and invert this curve. That is what the 2025 rover firmware does.

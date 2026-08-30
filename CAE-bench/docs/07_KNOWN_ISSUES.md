# 7 — Known issues

Found by auditing the 2024 code against the 11 recorded runs, August 2026. Fix D1 to
D3 before taking any new measurement; they change the numbers.

---

## D1 — CRITICAL. The speed calculation assumes a one-second counting window

The Arduino accumulates IR pulses, publishes them, then zeroes the counter, once per
`delay(200)` loop. Python converts that count to RPM as if it covered a full second.

```
arduinoADC.ino   delay(200);   irPulseCount = 0;
CAEPC.py         rpm = (ir_pulse_count * 60) / 3
measured         4.839 Hz emission -> 206.6 ms window
correction       true rpm = logged rpm x 4.84
```

**Every speed figure in the 2024 report and data is about a fifth of the real speed.**
The nominal "200 rpm" operating point is really about 960 rpm.

Three independent confirmations:

1. Air consumed per revolution. Corrected flow / corrected speed gives 4.3-19 cm3/rev
   against a geometric displacement of 12.5 cm3/shaft-rev. Uncorrected it gives
   260-1140 cm3/rev, 20 to 90 times the displacement, which no engine can do.
2. The bench reference of "about 2700 rpm" used elsewhere matches the corrected
   open-loop plateau of 2655 rpm to within 2 %.
3. The 2023 MATLAB controller computes speed event-based and correctly. The bug was
   introduced by the 2024 rewrite, not inherited.

**Fix.** Timestamp the window instead of assuming it:

```c
// arduinoADC.ino
unsigned long now = micros();
float dt = (now - lastPublish) / 1e6f;
lastPublish = now;
doc["dt_s"] = dt;
```
```python
# CAEPC.py
rpm = (ir_pulse_count / 3) / data['dt_s'] * 60
```

---

## D2 — CRITICAL. Flow carries the same window error, twice over

The YF-S201 family datasheet gives litres per minute as frequency divided by the
pulse constant. The sketch divides a *windowed* count by 7.5 and then multiplies by
60, which converts L/min to L/hour, while the column stays labelled `L/m`.

```
as coded     Q = pulseCount * 8.000
correct      Q = pulseCount * 0.645     (L/min, at a 206.6 ms window)
net          the logged figure is 12.4x the true flow in L/min
peak logged  572 "L/m"  ->  46 L/min  =  2770 L/h
```

On top of the arithmetic there is an unquantified error: the sensor is a **water
turbine used on compressed air**, well outside its rated fluid. Recalibrate.

**Fix.** `flowRate = (pulseCount / dt) / calibrationFactor;   // L/min`

---

## D3 — CRITICAL. Loop gain is divided by the setpoint

```python
servo_position = 200 + ((512 - 200) * pid_output / Desired_Speed)
```

The setpoint sits in the denominator, so the actuator gain moves inversely with it:

| Setpoint | servo units per unit of controller output | relative gain |
|---|---|---|
| 100 | 3.120 | x2.00 |
| 200 | 1.560 | x1.00 (tuned here) |
| 400 | 0.780 | x0.50 |

The report reads the resulting behaviour as a property of the engine — over-damped at
100 rpm, under-damped at 400. It is the controller detuning itself.

**Fix.** `servo_position = 200 + SERVO_SPAN * pid_output` with `SERVO_SPAN` fixed, and
let the gains carry the tuning. One gain set then holds across the range.

---

## D4 — MAJOR. Integral and derivative have no timestep

`integral += error` and `derivative = error - previous_error` are per-sample, not
per-second. At the measured 4.84 Hz the effective integral gain is 0.097 per second,
not the 0.02 written in the file. Change the Arduino delay, the baud rate or the PC
and the tuning moves with it.

**Fix.** Scale both by the measured `dt` from D1.

---

## D5 — MAJOR. The integrator winds up against a clamped actuator

`set_servo_position` clamps to 200-512 but the integral keeps accumulating with no
anti-windup and no limit. This is the mechanism behind the sustained oscillation in
the 100 rpm run, where the valve reaches its closed stop and the controller has to
unwind before it can respond.

**Fix.** Freeze the integral whenever the command is clamped.

---

## D6 — MINOR. Timestamps are frame times, not sample times

Serial lines are drained inside a matplotlib animation callback, so every sample read
in one frame gets the same timestamp. 284 samples share about 127 distinct stamps, in
bursts of up to three. Any derivative or spectral analysis inherits that jitter.

**Fix.** Stamp each sample when it is parsed, not once per frame.

---

## D7 — MINOR. The derivative term does nothing

With speed quantised to 20 logged units and Kd = 0.0003, a one-step change contributes
0.006 servo units, four orders of magnitude below the 0.5-unit servo deadband. Call it
a PI controller so whoever tunes it next has the right expectation.

---

## T — The torque channel: built twice, logged zero times

| Evidence | Where |
|---|---|
| Printed friction brake, 11 parts | shared drive, folder `torquemeter`, Dec 2023 |
| Brake firmware, 3 versions | `torquemotor1/2/3.ino`, Oct 2023 |
| Load-cell calibration procedure and sketch | `calibration_force.ino`, Nov 2023 |
| 2 x load cell 500 g / 1 kg, bought and fitted | Aart's BOM, 2024 |
| Load-cell attachment, printed, qty 2 | Aart's BOM, 2024 |
| **Any force column in any data file** | **none** |
| **Any torque figure in any report** | **none** |

Both 2023 reports list load torque as future work. Aart's discussion says back
pressure was a starting goal and the focus shifted. The hardware is there; the
acquisition never was. Adding one analog channel closes it.

Note also that the **load-cell attachment bracket has no CAD anywhere**, so it must be
redrawn before the channel can be rebuilt.

---

## Two documentation errors worth fixing at source

**Screw size.** The report says the servo bracket uses "4 4-m2-screws". The holes in
`CAEfinal.STL` are Ø3.96 mm, which is M4 clearance.

**Print settings.** Table II of the report quotes 70 % infill, 4 mm infill line
distance and 50 mm/s. Those are the values on the *right* extruder, which prints PVA
support. The part is on the left extruder at **100 % infill and 15 mm/s**. The quoted
17 h 42 print time is only consistent with the latter.

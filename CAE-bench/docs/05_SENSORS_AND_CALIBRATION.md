# 5 — Sensors and calibration

Source: `MCDC_Sensor_calibration_procedure.pdf`, **Jelmer Veenhuizen & Quentin
Hopman, 6 November 2023**, reproduced as text in `reference/`. Calibrate in this
order: pressure, flow, force.

---

## 5.1 Pressure sensor

Calibrated against atmosphere. The reading with the sensor open to air corresponds to
1 bar. The datasheet gives 0.5 % output error from non-linearity, hysteresis and
repeatability combined, so zeroing against atmosphere is assumed to hold at 8 bar.

**Procedure**

1. Expose the sensor to atmosphere by decoupling and closing the valves.
2. Wire it: **black to GND, red to 5 V, green to A0**. Connect the Arduino, open the
   Arduino IDE.
3. Run the calibration sketch `calibration_pressure.ino`.
4. Insert the resulting `pressureZero` and `pressureMax` into the experiment firmware.
5. Connect the sensor to the tank charged to 8 bar. Cross-check with the compressor's
   pneumatic pistol pressure dial, in a closed system.
6. Check the value. A discrepancy can come from the dial, a leak, or the calibration
   itself — check all three.

**Values currently in `arduinoADC.ino`:**

```c
const int   pressureZero              = 98;      // ADC counts at 1 atm
const int   pressureMax               = 800;     // ADC counts at full scale
const float pressuretransducermaxPSI  = 100;
const float psiToBarConversion        = 0.0689476;
```

Conversion, verbatim from the firmware:

```
pressureValue     = (analogRead(A0) - pressureZero) * (100 / (pressureMax - pressureZero));
pressureValue     = max(pressureValue, 0.0);
pressureValueInBar= pressureValue * 0.0689476 + 1;
```

---

## 5.2 Flow sensor

This is the hard one. Quoting the 2023 procedure directly:

> This is a difficult sensor to calibrate without a well-known flow. Here we will
> approximate the flow using the choking principle. If the pressure ratio between the
> tank and the outside is two or greater, it can be assumed the flow is choking on the
> small tube. In these cases, the flow rate is equal to the speed of sound
> approximately 343 m/s.

With `Q_tube = A * v`, `A = pi * r^2`, `r = 6.25e-3 m`, `v = 343 m/s`.

**Procedure**

1. Close the pneumatic system and charge to 8 bar. Wire the sensor and check the pins
   against the code.
2. Start the code and be ready to act quickly. Open the valve fast; once the flow is
   fully developed, start the code and let the pressure run out. Reduce the sampling
   time if the flow does not stay high long enough.
3. Insert the calibration factor into the test-setup code.

**The manufacturer's constant is 11 pulses per litre — for water.** The 2023 MATLAB
controller uses 11 and correctly reports **L/hour**:

```matlab
flow_rate = (flow/11) * 60;   % flowrate L/hour
```

The 2024 Arduino firmware uses **7.5** and mislabels the result:

```c
const float calibrationFactor = 7.5;
flowRate = (pulseCount / calibrationFactor) * 60;   // published as "flow_rate"
```

**Neither is right for air.** Both constants are water constants on a water turbine
being used on compressed air, well outside its rated fluid. Recalibrate by the choked
method above before trusting any absolute flow number. See
`docs/06_KNOWN_ISSUES.md` §D2 for the arithmetic error on top of this.

---

## 5.3 Force / load cell

Verbatim procedure:

1. Securely mount the load cell and make sure it is free from any external loads.
2. Apply load *i* to the load cell.
3. Read and record the output value for the applied load.
4. Repeat 2 and 3 for all loads.
5. Calculate the calibration factor by dividing the known loads by the corresponding
   load-cell output values.
6. Update the `calibration factor` value in the Arduino code.

And the closing line of the 2023 document, which is the whole reason this channel
exists:

> **Consider low loads corresponding with the engine torques to enhance accuracy.**

**Status.** The load cells were bought and fitted. `calibration_force.ino` exists in
the shared drive. No firmware in any generation ever published a force reading, and
none of the 2024 data files contain a force column. This is the open gap.

---

## 5.4 Speed

No calibration is needed, but the **resolution** must be understood.

The IR photo interrupter sees a printed disc with **3 lobes**. The Arduino counts
falling edges over one publish period and zeroes the counter each loop.

- Publish period, measured across all 11 runs: **206.6 ms** (4.839 Hz)
- One pulse therefore equals 1/3 revolution in 206.6 ms = **96.8 rpm**
- Every logged speed value is an exact multiple of 20 in the raw files, because the
  firmware divides by an assumed 1 s window. See `docs/06_KNOWN_ISSUES.md` §D1.

**Improving it.** Reprint the interruptor disc with **10 lobes** instead of 3 and
timestamp the publish window, and the resolution goes to about **29 rpm**. Both
changes are small; the disc has no surviving CAD and must be redrawn anyway.

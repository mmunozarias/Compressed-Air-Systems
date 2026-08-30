# 4 — Electronics and wiring

## 4.1 Architecture, 2024 generation

```
   PC or Raspberry Pi 5                         12 V SMPS
      |                                             |
      | USB serial 19200 baud, JSON lines           |
      |                                          [ U2S2 power hub ]
   [ Arduino Uno Rev 3 ]                            |  3-pin TTL
      |  5 V rail                                   |
      |                                          [ AX-12A servo ] -- horn -- ball valve
      +-- A0  <-- pressure sensor  (analog 0.5-4.5 V)
      +-- D2  <-- flow sensor      (digital pulse, INT, RISING)
      +-- D3  <-- IR interrupter   (digital pulse, INT, FALLING)
      |
      +-- USB (separate port) --> PC --------- U2D2 USB-to-TTL --> U2S2
```

The Arduino is used **only as an ADC and pulse counter**. All control runs on the PC.

## 4.2 Pin map — this is fixed by the firmware

| Signal | Pin | Mode | Why this pin |
|---|---|---|---|
| Pressure sensor | **A0** | analog in | the only analog channel used |
| Flow sensor | **D2** | `INPUT_PULLUP`, `attachInterrupt`, RISING | the Uno supports external interrupts only on D2 and D3 |
| IR photo interrupter | **D3** | `INPUT`, `attachInterrupt`, FALLING | as above |
| Serial | USB | 19200 baud | must match `CAEPC.py` |

Power and ground for all three sensors come from the Arduino 5 V and GND rails.

## 4.3 Why 5 V, and why the Arduino stayed

Aart's design decision, worth preserving: the flow, pressure and IR sensors all
require 5 V and return 5 V logic or analog. A 3.3 V controller would need a separate
5 V supply plus level shifters. The Raspberry Pi 5 has 3.3 V GPIO and **no ADC at
all**, which is why the Arduino remains in the chain purely to digitise A0 and to
count the two interrupt lines.

His conclusion after building it: *"The Raspberry Pi 5 proved to be unnecessary, since
the same functionality is achieved by running the code on a laptop or PC with less
effort."* **Build it with a laptop.** The Pi adds cost and no capability.

## 4.4 Dynamixel chain

| Setting | Value |
|---|---|
| Protocol | 1.0 |
| ID | 0 |
| Baud rate | 1 000 000 |
| Port (Windows) | `COM8` in the shipped code |
| Torque enable address | 24 |
| Goal position address | 30 |
| Present position address | 36 |
| Position range used | **200 to 512** |
| Angular span | 90 degrees, so 0.288 deg per unit |
| Moving status threshold | 0.5 units |

Use **Dynamixel Wizard** to confirm the ID, baud and COM port before running anything.

> **Convention warning.** In `CAEPC.py` position **200 is declared fully closed** and
> **512 fully open**. Max Kloosterman's rover mounts the same servo the other way
> round: 204 is 0 degrees and that is where the aperture is *maximum*. Both are
> internally consistent; they are different physical mountings. Verify yours by
> watching the valve before you trust either sign.

## 4.5 Load cell, if you fit one

Not present in any working firmware. To add it:

- Load cell (500 g or 1 kg) -> **HX711** breakout -> two digital pins (DT, SCK)
- The HX711 library `HX711_ADC` was already used on an adjacent project in 2022
- Add a `force` field to the JSON the Arduino publishes and a column to the Excel
  writer in `CAEPC.py`. That is the whole change.

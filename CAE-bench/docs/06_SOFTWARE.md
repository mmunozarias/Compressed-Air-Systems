# 6 — Software

Two generations. Build the 2024 one; the 2023 MATLAB is included because it is
correct in ways the 2024 rewrite is not.

---

## 6.1 What runs where

| Layer | 2023 | 2024 (this repo) |
|---|---|---|
| Sensor acquisition | `CEA_OLD_Jan_2024.ino` on an Arduino Uno | `arduinoADC.ino` on an Arduino Uno |
| Wire format | CSV over serial, 19200 baud | **JSON lines** over serial, 19200 baud |
| Control loop | MATLAB, `Final_PID.m` | Python, `CAEPC.py` |
| Actuator | SpringRC SR431 via Arduino | Dynamixel AX-12A via U2D2 from the PC |
| Output | live MATLAB plots | live matplotlib + PDF + `.xlsx` |

---

## 6.2 Install

```powershell
# 1. Python 3.9 or newer, and the Arduino IDE
python --version

# 2. Python packages
python -m pip install -r software/requirements.txt

# 3. Flash the Arduino
#    Open firmware/arduinoADC/arduinoADC.ino in the Arduino IDE.
#    Install the ArduinoJson library via Library Manager.
#    Select Arduino Uno, pick the port, Upload.

# 4. Find your COM ports
#    Device Manager for the Arduino; Dynamixel Wizard for the servo.
#    Then edit software/CAEPC.py:
#        DEVICENAME = 'COM8'      <- the U2D2
#        ser = serial.Serial('COM6', 19200, timeout=0.1)   <- the Arduino
```

`software/requirements.txt` is reconstructed from the imports in `CAEPC.py`; it was
not in the original repository.

---

## 6.3 Run

```powershell
cd software
python CAEPC.py
```

The loop runs for **60 seconds** and then stops itself. It writes two files to your
Desktop:

- `experiment_data.pdf` — the four plots plus a text page of the raw arrays
- `DATACAE.xlsx` — columns `Time (s)`, `RPM`, `Pressure (Bar)`, `Flow Rate (L/m)`,
  `Servo Position`

Rename `DATACAE.xlsx` immediately after each run or the next run overwrites it. This
is how the 11 files in `data/raw-2024/` came to have ad-hoc names.

**Procedure for a run.** Start the script with the hand valve closed. At about
t = 10 s open the hand valve — this is the step input. The controller takes roughly
6 s to settle. Let it run to 60 s.

---

## 6.4 The control law as shipped

```python
class PID:
    def compute(self, setpoint, pv):
        error = setpoint - pv
        self.integral += error
        derivative = error - self.previous_error
        output = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
        self.previous_error = error
        return output

pid = PID(0.1, 0.02, 0.0003)
Desired_Speed = 210          # was 200 for every run in data/raw-2024

servo_position = 200 + ((512 - 200) * pid_output / Desired_Speed)
```

Four things to know before you tune it. All four are expanded in
`docs/07_KNOWN_ISSUES.md`.

1. There is **no timestep** in the integral or derivative. The gains are per-sample,
   so they change if the loop rate changes.
2. There is **no anti-windup**. `set_servo_position` clamps to 200-512 while the
   integral keeps accumulating.
3. **The setpoint divides the actuator gain.** Loop gain at a setpoint of 100 is
   double that at 200 and four times that at 400. Retuning per setpoint is treating a
   symptom.
4. The **derivative term is inert** — with 20-unit speed quantisation and
   Kd = 0.0003 it contributes 0.006 servo units against a 0.5-unit deadband. This is
   a PI controller.

---

## 6.5 The 2023 MATLAB controller

`software/matlab/Final_PID_2023_RECOVERED.m`. Gains `Kp = -0.003`, `Ki = 0.0002`,
`Kd = -0.003`, setpoint **1500 rpm**, angle clamped to **0-45 degrees**.

Two things it does better than the 2024 rewrite:

- **Speed is event-based and correct.** It times one full revolution with `tic`/`toc`
  and computes `RPM = 60/elapsedTime`. No window assumption, no scale error.
- **Flow is labelled L/hour**, which matches the arithmetic.

It also does outlier rejection with a 10-sample moving mean on speed, pressure and
flow, which the Python rewrite dropped.

`software/matlab/baip_old.m` is the earlier MATLAB the repository marks as outdated.

---

## 6.6 Data format

`data/raw-2024/*.xlsx`, 11 runs, ~284 rows each:

| Column | Unit as labelled | Trust it? |
|---|---|---|
| `Time (s)` | s | Frame time, not sample time. Up to 3 samples share one stamp. |
| `RPM` | rpm | **No — multiply by 4.84** |
| `Pressure (Bar)` | bar absolute | Yes |
| `Flow Rate (L/m)` | L/min | **No — divide by 12.4 for L/min** |
| `Servo Position` | Dynamixel units, 200-512 | Yes |

`data/processed/CAE_bench_corrected_data.xlsx` has every run with corrected columns
driven by formula off a single correction sheet, so editing the measured emission rate
rescales the whole workbook.

Run-to-test mapping, verified by reproducing the report's own error metric:

| File | Setpoint | Role |
|---|---|---|
| `Result31` | 200 | Test 1 |
| `Result32` | 200 | Test 2 |
| `Result33` | 200 | Test 3 |
| `Result34` | 200 | Test 4 |
| `Result11` | 200 | Test 5 |
| `ResultNoPID`, `ResultNoPID2` | 200 | open-loop baselines |
| `Result10bar` | 200 | high-pressure limit test |
| `Result100` | 100 | low-setpoint test |
| `Result400` | 400 | high-setpoint test |
| `DATACAE` | 200 | unreported spare |

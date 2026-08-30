# Energy-Based Speed Regulation of Compressed-Air Engines

Simulation code for

> M. Munoz-Arias, L. M. Esquivel-Sancho and D. del Puerto-Flores,
> "Energy-Based Speed Regulation of Compressed-Air Engines,"
> *IEEE Transactions on Control Systems Technology* (submitted).

The scripts here regenerate **Figure 3** and **Figure 4** of the paper and print
every number quoted in Section V and Table II, so the results can be checked
without re-deriving anything.

---

## Contents

| File | What it does |
|---|---|
| `cae_model.py` | Shared parameters and dynamics, eqs. (6) to (35). Draws nothing. |
| `cae_open_loop.py` | Open-loop three-chamber simulation. Produces **Figure 3** and the Section V-A numbers. |
| `cae_closed_loop.py` | Closed-loop controller simulation, eqs. (40) to (42). Produces **Figure 4** and **Table II**. |
| `requirements.txt` | Python dependencies. |

Every function carries the equation number it implements. `cae_model.py` opens
with a table mapping each equation of the paper to the code that realises it.

Equation numbers in the source comments refer to the manuscript.

---

## Requirements

Python 3.9 or newer, with NumPy, SciPy and Matplotlib.

---

## Setup on Windows (PowerShell)

Check that Python is on the path:

```powershell
python --version
```

If that fails, install Python from <https://www.python.org/downloads/windows/>
and tick **Add python.exe to PATH** during installation.

Clone the repository and create a virtual environment inside it:

```powershell
git clone https://github.com/<user>/<repo>.git
cd <repo>
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell refuses with a script-execution error, allow local scripts for
this session only and try again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Running

Both scripts write a vector `.pdf` for the paper and a `.png` preview into the
current directory, and print their results to the terminal.

```powershell
python cae_open_loop.py
python cae_closed_loop.py
```

Useful options:

```powershell
python cae_closed_loop.py --show              # open an interactive window
python cae_open_loop.py --outdir figures      # write into .\figures\
python cae_open_loop.py --tmax 30 --n 24000   # run length and sample count
```

To deactivate the environment when finished:

```powershell
deactivate
```

---

## What you should see

### `cae_closed_loop.py`

This reproduces Table II of the paper exactly. Expected output:

```
[baseline]  A=5.0  Kp=0.002  Kd=0.0005  Ki=0.002
   Delta(s), eq. (51) = s^3 + 10 s^2 + 65 s + 100
   eigenvalues of M   : -3.973-5.735j, -3.973+5.735j, -2.054+0j
   Routh a2a1 - a3a0  : 550.0   > 0, Hurwitz
   decay rate gamma   : 2.054 1/s

[fast]  A=12.0  Kp=0.008  Kd=0.0012  Ki=0.01
   Delta(s) = s^3 + 24 s^2 + 324 s + 1200
   eigenvalues of M   : -9.324-11.72j, -9.324+11.72j, -5.353+0j
   Routh a2a1 - a3a0  : 6576.0   > 0, Hurwitz
   decay rate gamma   : 5.353 1/s

[baseline] omega_e = 2000.1 rpm,  z = 0.0500 N m,  theta_bar = -3.69e-03 rad
[fast    ] omega_e = 2000.0 rpm,  z = 0.0500 N m,  theta_bar = -1.64e-09 rad
```

The script also checks that the eigenvalues of the closed-loop matrix `M` in
eq. (47) agree with the roots of the characteristic polynomial of eq. (49) to
machine precision, which is the numerical statement of Theorem 2.

### `cae_open_loop.py`

Four panels: tank pressure, chamber gauge pressure, pipe mass flow and shaft
speed, each for `D = 1.0` and `D = 0.5`. The engine self-starts, runs, and stops
when the tank reaches atmospheric pressure. The script prints the peak speed,
the plateau speed, the mean flow and the stopping time for each throttle
setting. Expected output:

```
D = 1.0 (fully open)
    peak shaft speed        2169.2 rpm
    plateau speed (2-5 s)    735.2 rpm
    mean flow (2-5 s)       2186.8 L/h
    engine stops at          10.13 s
D = 0.5 (half open)
    peak shaft speed        1940.8 rpm
    plateau speed (2-5 s)    750.9 rpm
    mean flow (2-5 s)       2172.7 L/h
    engine stops at          11.10 s
```

These are the numbers quoted in Section V-A. The figures the scripts write are
byte-for-byte the ones included in the manuscript.

---

## Model notes

**Geometry.** The simulations use the **measured** bench geometry,
`V_BAR = 8.25e-6` m^3 and `DELTA_V = 1.25e-5` m^3, not the reference geometry
of Table I, whose mean chamber volume of 0.1 L is about twelve times larger.
This is the scale discrepancy discussed in Section VII, and it accounts for
roughly an order of magnitude in the absolute pressure and flow amplitudes.

**Port timing.** The four port angles in `cae_model.py`
(`INTAKE_OPEN`, `INTAKE_CUTOFF`, `EXHAUST_OPEN`, `EXHAUST_CLOSE`) are not
documented for this engine and are set to physically reasonable values rather
than calibrated. The steady-speed plateau is sensitive to them. This is the
port-timing calibration gap named in Section VII, and closing it against a
measured bench trace is the first item of future work.

**Scope of the closed-loop result.** `cae_closed_loop.py` simulates the shaft
subsystem under Assumption 3, which is the setting Theorems 1 and 2 address. It
does not include the valve realisation, the one-sided throttling authority, or
the depleting tank. The commanded torque staying inside the engine envelope is
evidence that the realisability assumption is not being violated, but the full
cascade on the three-chamber plant is future work.

---

## Licence

%% TODO: choose a licence. MIT is the usual choice for code accompanying a
%% paper. Add a LICENSE file at the repository root.

## Citing

%% TODO: add the BibTeX entry for the paper once it has a DOI, and consider
%% archiving a release on Zenodo so the code itself is citable.

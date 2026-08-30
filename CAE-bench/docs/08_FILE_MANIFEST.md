# 8 — File manifest

Every file in this repository, where it came from, and how much to trust it.

Legend — **A** byte-exact from Aart's GitHub repository · **B** recovered as text
through the Drive API and mechanically un-escaped, verify before relying on it ·
**C** generated during the August 2026 audit · **D** placeholder, download required.

| Path | Src | Bytes | What it is |
|---|---|---|---|
| `README.md` | C | — | Entry point |
| `MISSING_FILES.md` | C | — | Download list, redraw list, corrupt list |
| `CITATION.cff` | A | 700 | Aart's citation metadata |
| **docs/** | | | |
| `01_BILL_OF_MATERIALS.md` | C | — | Merged from the TA bench BOM and Aart's Appendix A |
| `02_MECHANICAL_ASSEMBLY.md` | C | — | From the 2024 assembly manual plus the CAD measurements |
| `03_PNEUMATIC_CIRCUIT.md` | C | — | Air path, operating points, valve area curve |
| `04_ELECTRONICS_AND_WIRING.md` | C | — | Pin map read out of the firmware |
| `05_SENSORS_AND_CALIBRATION.md` | C | — | From the Veenhuizen & Hopman procedure |
| `06_SOFTWARE.md` | C | — | Install, run, control law, data format |
| `07_KNOWN_ISSUES.md` | C | — | Seven defects, the torque gap, two doc errors |
| `08_FILE_MANIFEST.md` | C | — | This file |
| **cad/aart-2024/** | | | |
| `CAEfinal.STL` | A | 209 484 | Servo/valve bracket, 4188 triangles |
| `CAE(1).SLDPRT` | A | 338 482 | SolidWorks source, bracket |
| `CAEconnect.SLDPRT` | A | 98 441 | SolidWorks source, servo horn |
| `UMS5_CAE8.3mf` | A | 196 921 | Cura 5.7.1 project with the full print profile |
| `CAEfinal_views.png` | C | 37 899 | Measured orthographic and isometric views |
| `UMS5_CAE8_thumbnail.png` | C | 29 731 | Extracted from the 3MF |
| `README.md` | C | — | Measured geometry and print settings |
| **cad/wankel-2023/**, **cad/pneumatics/**, **cad/torquemeter/** | D | — | Empty. See MISSING_FILES.md §C1–C4 |
| **firmware/** | | | |
| `arduinoADC/arduinoADC.ino` | A | 3 100 | 2024 acquisition sketch. JSON over serial at 19200 |
| `legacy-2024/CEA_OLD_Jan_2024.ino` | A | — | The superseded January 2024 sketch |
| `bench-2023/` | D | — | Empty. Calibration and brake sketches, MISSING_FILES.md §C5 |
| **software/** | | | |
| `CAEPC.py` | A | 14 056 | 2024 PC-side control loop, Dynamixel + matplotlib + xlsx |
| `requirements.txt` | C | — | Reconstructed from the imports; not in the original repo |
| `matlab/baip_old.m` | A | 8 600 | Marked outdated in the original repository |
| `matlab/Final_PID_2023_RECOVERED.m` | **B** | — | Hilbrands' 2023 controller. **Diff against the original before use.** |
| **data/raw-2024/** | | | |
| `DATACAE.xlsx` … `ResultNoPID2.xlsx` (11 files) | A | ~40 kB each | The runs as logged. **Speed ×4.84 too low, flow ×12.4 too high.** |
| `*.pdf` (10 files) | A | — | The plots as generated at run time |
| `experiment_data.pdf` | A | — | Combined plot export |
| **data/processed/** | | | |
| `CAE_bench_corrected_data.xlsx` | C | — | All 11 runs with corrected columns, driven by formula from one correction sheet |
| **reference/** | | | |
| `assembly_manual_2024.md` | **B** | — | Dufour, 6 Feb 2024. Technical drawings NOT reproduced |
| `sensor_calibration_procedure_2023.md` | **B** | — | Veenhuizen & Hopman, 6 Nov 2023 |
| `bench_purchase_record.csv` | **B** | — | The compressed-air rows of the MCDC purchase record |
| `README.md` | C | — | Source table for the above |

## Verifying the B files

```powershell
# after downloading the original from the link in MISSING_FILES.md
git diff --no-index original.m software/matlab/Final_PID_2023_RECOVERED.m
```

Expect differences in whitespace and in the header comment block, which was added.
Any difference in a numeric literal or an operator is a transcription error — fix it
and note it here.

## Suggested .gitignore

```
__pycache__/
*.pyc
.venv/
*.tmp
~$*
```

Everything else in this tree is meant to be committed, including the data.

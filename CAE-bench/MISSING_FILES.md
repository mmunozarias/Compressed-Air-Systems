# Files still to fetch, and files that no longer exist

Updated 30 August 2026, after the manual Drive download.

**The CAD and 2023 firmware gaps are closed.** Four of the five folders that were
empty are now populated: `cad/wankel-2023/`, `cad/pneumatics/`, `cad/torquemeter/`
and `firmware/bench-2023/`. What remains below is a short list.

---

## A. Byte-exact, in the repository

### A1. From `github.com/AartCodes/RUG-Pneumatic-Engine-experiment` @ `270cbc5`

- `firmware/arduinoADC/arduinoADC.ino`
- `firmware/legacy-2024/CEA_OLD_Jan_2024.ino`
- `software/CAEPC.py`, `software/matlab/baip_old.m`
- `cad/aart-2024/` — all four CAD files
- `data/raw-2024/` — all 11 run workbooks and their PDF plots
- `CITATION.cff`

### A2. Downloaded by hand from Google Drive, 30 August 2026

| Folder | Count | Contents |
|---|---|---|
| `cad/wankel-2023/` | 8 + 17 | Engine assembly, mainframe, top cover, rotor, crank, output shaft, two GT2 pulleys; `Random/` holds the design iterations and STEP exports |
| `cad/pneumatics/` | 5 | Sensor adapters, flow-valve frame and adapter |
| `cad/torquemeter/` | 11 | **The complete friction-brake torque rig** — bases, three brake rotors, two friction elements, holder, coupling stabiliser, engine mounting base, and the Cura 3MF |
| `firmware/bench-2023/` | 14 | Calibration sketches, three brake firmwares, the demo sketch, sensor test sketches |

---

## B. Three files that arrived and were not on any list

Worth knowing about — none of these appeared in the original sweep.

| File | Where it landed | Why it matters |
|---|---|---|
| `Final_PID.m` | `firmware/bench-2023/Code provided by Max 23 Jan 2024/` | **The byte-exact original** of the 2023 controller. Until now the repository only had the text-recovered copy. Diff them — see §B1. |
| `NewDatasetPQN.m` | `firmware/bench-2023/CEA_Demo_22_Jan_2024/` | A MATLAB pressure/flow/speed dataset script that accompanied the January 2024 demo. Not referenced in any report. |
| `braccioServoTestwithoutShield.ino`, `pressure_sensor.ino`, `water_flow_sensor.ino` | `firmware/bench-2023/` | Single-sensor test sketches. The two sensor ones are the cleanest reference for the raw pin reads. |

### B1. Do this diff

`software/matlab/Final_PID_2023_RECOVERED.m` was reconstructed from a
markdown-escaped API rendering. The original is now sitting next to it. Confirm they
agree, then keep only the original:

```powershell
cd "$env:USERPROFILE\Documents\GitHub\Compressed-Air-Systems\CAE-bench"
Compare-Object `
  (Get-Content "software\matlab\Final_PID_2023_RECOVERED.m") `
  (Get-Content "firmware\bench-2023\Code provided by Max 23 Jan 2024\Final_PID.m")
```

No output means the recovery was faithful and every conclusion drawn from it holds.

### B2. Three files are in the wrong folder

They came inside the firmware zip but they are not firmware:

| File | Move to |
|---|---|
| `firmware/bench-2023/calibration codes/MCDC_Sensor_calibration_procedure (1).pdf` | `reference/` — this is the byte-exact original of `reference/sensor_calibration_procedure_2023.md` |
| `firmware/bench-2023/Code provided by Max 23 Jan 2024/Final_PID.m` | `software/matlab/` — after the diff in §B1 |
| `firmware/bench-2023/CEA_Demo_22_Jan_2024/NewDatasetPQN.m` | `software/matlab/` |

---

## C. Recovered as text, and therefore NOT byte-exact

The Google Drive API returns text files as a markdown-escaped rendering. These have
been mechanically un-escaped. Every line I could verify is faithful, but **download
the originals and diff before relying on them.**

| File in this repo | Original | Status |
|---|---|---|
| `software/matlab/Final_PID_2023_RECOVERED.m` | https://drive.google.com/file/d/1AHEYelm9op-rKECdSCq290AfyVtu5YcN/view | **Original now in repo — diff it, §B1** |
| `reference/sensor_calibration_procedure_2023.md` | https://drive.google.com/file/d/1NcTs68NeVQ3JF6jvzESmAeCHfGNlPs-o/view | **Original PDF now in repo, §B2** |
| `reference/assembly_manual_2024.md` | https://drive.google.com/file/d/12QYhJ9bgo3Mi30Q98cJiB5EE-rjmYTcK/view | still text-only |
| `reference/bench_purchase_record.csv` | https://drive.google.com/file/d/12S-FDaBVhX_Im-J83x53LmS7h7cCgfUk/view | still text-only |

---

## D. Still to download

Short list. Everything else on the old list arrived.

### D1. One STL, one adapter

| File | Into | Link | Note |
|---|---|---|---|
| `crank rotary_full_thread.STL` | `cad/wankel-2023/` | https://drive.google.com/file/d/1MkxhRA-5ii5pRoACFyRBst1Ptty3XrNf/view | `crank rotary_full_thread.STEP` and `…1.SLDPRT` did arrive, in `Random/`. Only the print-ready mesh is absent. |
| `g78p14_to_g18p28_ASPART.STL` | `cad/pneumatics/` | Drive folder "Adaptors & Connectors" | G7/8-1/4 to G1/8-1/4 thread adapter |

### D2. Two firmware variants

| File | Into | Link |
|---|---|---|
| `calibration_pressureNEW.ino` | `firmware/bench-2023/` | https://drive.google.com/file/d/10WHNEVndiqODSPl31ZAOfcYgzPOO-sFT/view |
| `Cal_flow1.ino` | `firmware/bench-2023/` | https://drive.google.com/file/d/1XcnWjRBtoMcRpctCfh-zhMIp4V-T_4Xi/view |

Both are variants of sketches that already arrived. Low priority.

### D3. Reference documents, into `reference/`

The largest remaining gap, and the one that matters most for a stranger trying to
rebuild the bench — the three final reports contain the reasoning behind the design.

| File | Link |
|---|---|
| `Compressed_air_engine_assembly_manual (4).pdf` — with all technical drawings | https://drive.google.com/file/d/12QYhJ9bgo3Mi30Q98cJiB5EE-rjmYTcK/view |
| `BoM_experimentalSetup_MCDC.xlsx` | https://drive.google.com/file/d/12S-FDaBVhX_Im-J83x53LmS7h7cCgfUk/view |
| `Final report - Aart van Werven.pdf` | https://drive.google.com/file/d/1jeOsAo6GKKWHYmRFczAijTgDJKLy9ffv/view |
| `Koen Kiewiet - Final Report.pdf` | https://drive.google.com/file/d/19jPMe1Uf--jlzvOY9KKocOAmeYLkY6l5/view |
| `Niek Hilbrands - Final Report.pdf` | https://drive.google.com/file/d/19nG8YkGtTjL5F2W3YVkus5UZwvXdnWn0/view |
| `CAE_drawing3.pdf`, `CAE.SLDPRT`, `CAE.SLDDRW` — **the dimensioned 2D drawing** | Gmail, 6 May 2024, message `18f4c5735a05912d` |
| Purchase orders, ~90 PDFs | https://drive.google.com/drive/folders/15pth04qXh3LmkRtO3BiwIH30W6IG_41J |

Check the licence position on the student reports before pushing them to a public
repository.

---

## E. Does not exist anywhere — must be redrawn

Five printed parts appear in the bill of materials with no CAD in any archive,
including the folders downloaded on 30 August 2026. All five carry an instrument.

| Part | Qty | What it does |
|---|---|---|
| **IR-sensor interruptor disc** | 1 | 3-lobe disc on the output shaft. **Redraw with 10 lobes** — see `docs/07_KNOWN_ISSUES.md` D1. |
| **IR-sensor holder** | 1 | positions the photo interrupter over the disc |
| **Load-cell attachment** | 2 | mounts the load cell to the brake arm. Without it the torque channel cannot be rebuilt. |
| **Sensor holder** | 1 | holds the pressure and flow sensors to the plank |
| **Tube holder** | 4 | routes the 8 mm line |

The load-cell attachment is now the **only** thing standing between this bench and a
working torque channel. Every other part of the rig — the brake, the rotors, the
friction elements, the coupling, and `calibration_force.ino` — is in this repository.

---

## F. Corrupt

`Engine_mount_wankel.STL` appears twice in the shared drive at **zero bytes**, ids
`1t633eYdxz7QXZYz_nJCpnm2AZ7vxKtjh` and `13ULi0r8Ysf9A_df54gEAvZRMN9DEu9cy`. Both
copies are unrecoverable. Use `cad/torquemeter/Engine mounting base.stl` instead —
it is now in the repository.

`cad/wankel-2023/Random/rotorstepje.err` is a SolidWorks export error log, not a
model. It is kept because it records a failed STEP translation of the rotor.

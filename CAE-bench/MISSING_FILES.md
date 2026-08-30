# Files still to fetch, and files that no longer exist

This repository contains **everything that could be pulled programmatically**. Two
categories could not be, and one category is gone for good.

---

## A. What is already here, byte-exact

Cloned from `github.com/AartCodes/RUG-Pneumatic-Engine-experiment` at commit `270cbc5`:

- `firmware/arduinoADC/arduinoADC.ino`
- `firmware/legacy-2024/CEA_OLD_Jan_2024.ino`
- `software/CAEPC.py`, `software/matlab/baip_old.m`
- `cad/aart-2024/` — all four CAD files
- `data/raw-2024/` — all 11 run workbooks and their PDF plots
- `CITATION.cff`

---

## B. Recovered as text, and therefore NOT byte-exact

The Google Drive API returns text files as a markdown-escaped rendering. These have
been mechanically un-escaped. Every line I could verify is faithful, but **download
the originals and diff before relying on them.**

| File in this repo | Original |
|---|---|
| `software/matlab/Final_PID_2023_RECOVERED.m` | https://drive.google.com/file/d/1AHEYelm9op-rKECdSCq290AfyVtu5YcN/view |
| `reference/assembly_manual_2024.md` | https://drive.google.com/file/d/12QYhJ9bgo3Mi30Q98cJiB5EE-rjmYTcK/view |
| `reference/sensor_calibration_procedure_2023.md` | https://drive.google.com/file/d/1NcTs68NeVQ3JF6jvzESmAeCHfGNlPs-o/view |
| `reference/bench_purchase_record.csv` | https://drive.google.com/file/d/12S-FDaBVhX_Im-J83x53LmS7h7cCgfUk/view |

---

## C. Could NOT be retrieved — binary MIME types

The Drive connector available to this session can read text, PDF, Office and image
files. It cannot read `.stl`, `.step`, `.sldprt`, `.3mf`, `.zip` or `.ino` (Arduino
files are served as `application/octet-stream`). **Every file below has to be
downloaded by hand.** Open the link, click download, drop it in the folder named.

### C1. CAD — engine, into `cad/wankel-2023/`

| File | Link |
|---|---|
| `Wankel assembly.SLDASM` | https://drive.google.com/file/d/10qnbtJt9fP_gMgu03DqM-8jDLkC_yWdX/view |
| `rotor.step.SLDPRT` | https://drive.google.com/file/d/13ASVkHMaLWXPjTd-TEHc85AliFdI-eEQ/view |
| `crank rotary.SLDPRT` | https://drive.google.com/file/d/11LppCMC88IKBaVyKsSRSL8pCiLaR9OQ7/view |
| `crank rotary_full_thread.STL` | https://drive.google.com/file/d/1MkxhRA-5ii5pRoACFyRBst1Ptty3XrNf/view |
| `Wankel mainframe.stl` | https://drive.google.com/file/d/1VrSIEBLdH981VqKtHvGi_fwCkHCAVbBJ/view |
| `Wankel topcover.stl` | https://drive.google.com/file/d/1edk3bMwUNo_yOBTZCfFxwnzmB797kezG/view |
| `outputshaft wankel redesigned.stl` | https://drive.google.com/file/d/12hjodYtBpD0ERMpRKSHuk8z-6wzSWGFS/view |
| Design iterations: Casing 1–8, Rotor 1–8, Lid 1–8, Shaft 1–8, `mainframe_wankel.step`, `Topcover_wankel.step` | https://drive.google.com/drive/folders/11kiRT0R87QFezq4LrvzLkMvkKvEzTsNK |

### C2. CAD — drive train, into `cad/wankel-2023/`

| File | Link |
|---|---|
| `GT2_80T_8mm_Bore_Pulley_for_10mm_Belt.step.SLDPRT` | https://drive.google.com/file/d/12O0SBczzuLBMp4y1QN0jm6CrffQ0UO6S/view |
| `Pulley 15T 3mm.stp.SLDPRT` | https://drive.google.com/file/d/12Vmczr1nmsFqlOKPDuS-62mTEXgtehfW/view |

### C3. CAD — pneumatic line, into `cad/pneumatics/`

Whole folder: https://drive.google.com/drive/folders/1K8AGULQLnYK_spOuj3I9cGfxOOl6y3SA

| File | Link |
|---|---|
| `adapter pneumatic flow pressure sensor v2.stl` | https://drive.google.com/file/d/1QWtnrH5u5R8IYqY0rvRU-OKHc2BH7FXv/view |
| `connector tube to flow sensor 1_8 v1.stl` | https://drive.google.com/file/d/1ezaLpgTu4k2y648dAcikOIlGHbXTLK_e/view |
| `adapter_flowvalve.stl` | https://drive.google.com/file/d/1q8b_8EFaHkZw3dyxIKtLF5bOVbY0FtYE/view |
| `frame_flowvalve.stl` | https://drive.google.com/file/d/1NV4YqyVHmf6g_B9ATW6jOrzWQiUp72jr/view |
| `frame_updated.stl` (use this one) | https://drive.google.com/file/d/1YlL04xBiSqgjuNNAmcmnErDD0_KyvZZb/view |
| `g78p14_to_g18p28_ASPART.STL` | in folder "Adaptors & Connectors" |

### C4. CAD — torque rig, into `cad/torquemeter/`

Whole folder: https://drive.google.com/drive/folders/1Yzjp4fKt7rG8Q8j1aQUwIbYP5OV0g3dm

| File | Link |
|---|---|
| `Torquemotor base complete.stl` | https://drive.google.com/file/d/1aRtJ1ntES35K00hKQ_ZFvhuL681t3iuq/view |
| `torquemotor base only base.stl` | https://drive.google.com/file/d/11OKgu8LKvYN8xcmkTFrerzWF6L0AQCOt/view |
| `Rotor Torquemotor 35mm.stl` | https://drive.google.com/file/d/11lq-IsH4nAKA34GuHuvW4fo0MELl7yMb/view |
| `rotor torquemotor 32mm.stl` | https://drive.google.com/file/d/14BlxnppeO_4KYdD-_jgibXJr78iSylot/view |
| `rotor torquemotor speed (v1~recovered).stl` | https://drive.google.com/file/d/1_k4k0X4cATc5ecr3r-TJTnuPcKDS4j9n/view |
| `holder friction torquemotor.stl` | https://drive.google.com/file/d/1IABbhGwXHTZXFvJQkb6hu1bcqtHS715a/view |
| `friction thingy 11.2mm.stl` | https://drive.google.com/file/d/1qf3CIkbcbyIPMZ0lR_XCwYmqGo40WxpU/view |
| `friction part 11mm.stl` | https://drive.google.com/file/d/1LAzqiDXZx3lDihRCx0iZcUX-DHONTIhG/view |
| `coupling output shaft stabilizer.stl` | https://drive.google.com/file/d/1blI3CYFhS4_dBnDB5tIaoYlxAtGPqG2M/view |
| `Engine mounting base.stl` | https://drive.google.com/file/d/1JJQe9DySRxVN28QpFtZh3KKRzL__SOco/view |
| `MCDC project print.3mf` | https://drive.google.com/file/d/1XCR7AvDlo9WIIJGY2gES5K3-R58icCGj/view |

### C5. Firmware — into `firmware/bench-2023/`

All `.ino`, all served as octet-stream, all must be downloaded by hand.

| File | Purpose | Link |
|---|---|---|
| `calibration_pressure.ino` | §5.1 | https://drive.google.com/file/d/1N5TNWYmDKPXWIamPsnneZvXHBETUde2X/view |
| `calibration_flow.ino` | §5.2 | https://drive.google.com/file/d/1NYfv6ezN-nQ1ZO533Tar7QxmUWB7ZQNv/view |
| `calibration_force.ino` | §5.3 — **the load-cell one** | https://drive.google.com/file/d/1Nakx0HwFnjOQpSjgHod1vDwGDWDcIyK0/view |
| `torquemotor1.ino` | brake firmware v1 | https://drive.google.com/file/d/1iC03KaTdKn0i8FAQqfNAd0lENzJyhhzy/view |
| `torquemotor2.ino` | brake firmware v2 | https://drive.google.com/file/d/1DluyMISuivTC9EgrmcJ2hmIU5cQ14Ixc/view |
| `torquemotor3.ino` | brake firmware v3, largest | https://drive.google.com/file/d/1zCVbaCvh6qnvbGdga4ZuDbaaMkDXsbaZ/view |
| `calibration_pressureNEW.ino` | revised pressure cal | https://drive.google.com/file/d/10WHNEVndiqODSPl31ZAOfcYgzPOO-sFT/view |
| `Cal_flow1.ino` | flow cal variant | https://drive.google.com/file/d/1XcnWjRBtoMcRpctCfh-zhMIp4V-T_4Xi/view |
| `flow_pressure_combined.ino` | combined logger | https://drive.google.com/file/d/1FswZpI0Cl1eMz4Pq9e8EjK-bNJmKYT_V/view |
| `CEA_Demo_22_Jan_2024.ino` | live demo firmware | https://drive.google.com/file/d/19t_huvy9FV7dNBoX9Z1M2itmF2YDf3hP/view |

### C6. Reference documents, into `reference/`

| File | Link |
|---|---|
| `Compressed_air_engine_assembly_manual (4).pdf` — original with all technical drawings | https://drive.google.com/file/d/12QYhJ9bgo3Mi30Q98cJiB5EE-rjmYTcK/view |
| `BoM_experimentalSetup_MCDC.xlsx` | https://drive.google.com/file/d/12S-FDaBVhX_Im-J83x53LmS7h7cCgfUk/view |
| `MCDC_Sensor_calibration_procedure (1).pdf` | https://drive.google.com/file/d/1NcTs68NeVQ3JF6jvzESmAeCHfGNlPs-o/view |
| `Final report - Aart van Werven.pdf` | https://drive.google.com/file/d/1jeOsAo6GKKWHYmRFczAijTgDJKLy9ffv/view |
| `Koen Kiewiet - Final Report.pdf` | https://drive.google.com/file/d/19jPMe1Uf--jlzvOY9KKocOAmeYLkY6l5/view |
| `Niek Hilbrands - Final Report.pdf` | https://drive.google.com/file/d/19nG8YkGtTjL5F2W3YVkus5UZwvXdnWn0/view |
| `CAE_drawing3.pdf`, `CAE.SLDPRT`, `CAE.SLDDRW` — **the dimensioned 2D drawing** | Gmail, 6 May 2024, message `18f4c5735a05912d` |
| Purchase orders, ~90 PDFs | https://drive.google.com/drive/folders/15pth04qXh3LmkRtO3BiwIH30W6IG_41J |

---

## D. Does not exist anywhere — must be redrawn

Five printed parts appear in the bill of materials with no CAD in any archive. All
five carry an instrument.

| Part | Qty | What it does |
|---|---|---|
| **IR-sensor interruptor disc** | 1 | 3-lobe disc on the output shaft. **Redraw with 10 lobes** — see `docs/07_KNOWN_ISSUES.md` D1. |
| **IR-sensor holder** | 1 | positions the photo interrupter over the disc |
| **Load-cell attachment** | 2 | mounts the load cell to the brake arm. Without it the torque channel cannot be rebuilt. |
| **Sensor holder** | 1 | holds the pressure and flow sensors to the plank |
| **Tube holder** | 4 | routes the 8 mm line |

---

## E. Corrupt

`Engine_mount_wankel.STL` appears twice in the shared drive at **zero bytes**, ids
`1t633eYdxz7QXZYz_nJCpnm2AZ7vxKtjh` and `13ULi0r8Ysf9A_df54gEAvZRMN9DEu9cy`. Both
copies are unrecoverable. Use `Engine mounting base.stl` from the torquemeter folder
instead.

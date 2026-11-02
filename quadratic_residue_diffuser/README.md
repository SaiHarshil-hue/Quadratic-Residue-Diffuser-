# Quadratic Residue Diffusers Using Number Theory in Acoustic Panel Design

First-year B.Tech CSE (AI) project. **Python** does all calculations, validation,
tables, exports and the interface. **MATLAB** is used **only** to draw the graph.
No other libraries are needed (Python standard library only).

> **Honest note:** this program calculates well depths from a simplified
> mathematical model. It does **not** prove that a diffuser improves sound.
> That needs an acoustic simulation or a physical experiment.

## Folder structure

```
quadratic_residue_diffuser/
├── main.py            Tkinter interface (terminal menu if Tkinter is missing)
├── calculations.py    residues, wavelength, depths, comparison, frequency table
├── validation.py      input checks
├── exports.py         text tables, CSV, report, calling MATLAB
├── explanation.py     text of the Explanation panel
├── matlab/plot_depths.m   MATLAB plotting script (plots only)
├── data/              exported CSV
├── graphs/            graphs made by MATLAB
├── reports/           exported text reports
├── tests/test_calculations.py
├── README.md
└── PROJECT_REPORT.md  short report, viva questions, limitations
```

Two small files (`exports.py`, `explanation.py`) were added to your structure so
that `main.py` stays short and the maths stays separate from file handling.

## Windows setup (step by step)

1. **Install Python 3.9 or newer** from https://www.python.org/downloads/
   - On the first installer screen tick **"Add python.exe to PATH"**.
   - Choose "Customize installation" and make sure **"tcl/tk and IDLE"** is ticked
     (this gives Tkinter, needed for the window).
2. Open **Command Prompt** and check: `python --version`
3. Check Tkinter: `python -m tkinter` (a small test window should appear; close it).
4. Unzip this project, then in Command Prompt:
   ```
   cd path\to\quadratic_residue_diffuser
   ```
   (Tip: type `cd ` and drag the folder into the window.)

## Run the tests

```
python tests\test_calculations.py
```
Expected: `Ran 23 tests ... OK`

## Run the program

```
python main.py
```
A window opens with the default example (p = 7, f0 = 500 Hz, c = 343 m/s).
Tabs: **Results**, **Compare primes**, **Frequency exploration**, **Explanation**, **Export**.
Wrong inputs show a red message and a pop-up; the program does not crash.

If Tkinter is not available, the same program runs as a terminal menu.

## Expected output for the default example

| Item | Value |
|---|---|
| Sequence s(n) | [0, 1, 4, 2, 2, 4, 1] |
| Wavelength | 0.686 m |
| Maximum depth | 0.343 m |
| Relative depths | [0, 0.25, 1, 0.5, 0.5, 1, 0.25] |
| Depths (cm) | [0, 8.575, 34.3, 17.15, 17.15, 34.3, 8.575] |

## Python -> MATLAB data transfer

Python writes `data/results.csv` with columns
`Well, Square, Residue, Relative_Depth, Depth_m, Depth_cm` (unrounded values).
MATLAB reads that file with `readtable` and draws a bar graph of `Well` vs `Depth_cm`.

**Option A – from the program:** Export tab -> **Create MATLAB graph**.
This works if `matlab` is on your Windows PATH (MATLAB R2019a or newer). The graph is saved
to `graphs\depths.png`. Use **Save graph PNG as...** to copy it elsewhere.

**Option B – manually (always works):**
1. In the program click **Save results CSV** (or **Create MATLAB graph**, which also writes the CSV).
2. Open MATLAB, set the *Current Folder* to the `matlab` folder of this project.
3. Run: `plot_depths('..\data\results.csv', '..\graphs\depths.png')`
4. Open `graphs\depths.png`.

Typing `plot_depths` with no arguments uses those same default files.

## Formulas

| Formula | Meaning |
|---|---|
| s(n) = n² mod p | square n, divide by p, keep the remainder |
| r(n) = s(n) / max(s) | scale residues to 0…1 (max(s) > 0 for every prime p > 2) |
| λ₀ = c / f₀ | wavelength at the design frequency |
| Dmax = λ₀ / 2 | deepest well in this simplified model |
| d(n) = r(n) · Dmax | depth of well n |

**Different method:** many textbooks use d(n) = s(n)·λ₀/(2p). That is a *separate* design
method (for p = 7 its deepest well is 19.6 cm, not 34.3 cm). This project does **not** use it
or mix it with the formulas above.

## Input limits

Prime: whole number, prime, 3 ≤ p ≤ 1000. Frequency and speed: 0.000001 to 1,000,000,000.
Lists (Compare / Frequency tabs): at most 12 items, separated by commas.

## What has and has not been tested

- Python calculations, validation, CSV/report export and the terminal menu were tested by running them.
- The Tkinter window code was checked only with a stand-in for Tkinter (logic, not appearance).
  Please open it once on your PC to confirm it looks right.
- **`plot_depths.m` has not been run in MATLAB** (MATLAB was not available when this was built).
  Run it once and tell your guide if any error appears.

See `PROJECT_REPORT.md` for the report, viva questions, limitations and future work.

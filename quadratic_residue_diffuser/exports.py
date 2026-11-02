# exports.py
# Text tables, CSV export, report export, and the call to MATLAB.
# (Kept in its own file so main.py stays short and easy to read.)
# Python never draws graphs. It only writes a CSV and asks MATLAB to plot it.
import csv
import datetime
import os
import shutil
import subprocess

import calculations as calc

# Folder paths are built from the location of this file, so the project
# works no matter where the folder is placed.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
GRAPH_DIR = os.path.join(BASE_DIR, "graphs")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
MATLAB_DIR = os.path.join(BASE_DIR, "matlab")
DEFAULT_CSV = os.path.join(DATA_DIR, "results.csv")
DEFAULT_PNG = os.path.join(GRAPH_DIR, "depths.png")

CSV_HEADER = ["Well", "Square", "Residue", "Relative_Depth", "Depth_m", "Depth_cm"]

NOTE = ("NOTE: This is a simplified normalization-based model. The depths are\n"
        "calculated values, not a validated acoustic design or a measurement.")


# ---------- text formatting (rounding is for display only) ----------

def list_text(values, decimals):
    """Format a list of numbers like [0.00, 8.57, 34.30]."""
    return "[" + ", ".join("{:.{d}f}".format(v, d=decimals) for v in values) + "]"


def format_table(rows):
    """Neat results table."""
    head = "{:>6} {:>8} {:>9} {:>10} {:>12}".format(
        "Well", "Square", "Residue", "Relative", "Depth (cm)")
    lines = [head, "-" * len(head)]
    for r in rows:
        lines.append("{:>6} {:>8} {:>9} {:>10.3f} {:>12.3f}".format(
            r["n"], r["square"], r["residue"], r["relative"], r["depth_cm"]))
    return "\n".join(lines)


def format_summary(p, f0, c, rows):
    """Inputs, sequence, wavelength, max depth, table and note."""
    w = calc.wavelength(c, f0)
    dmax = calc.max_depth(w)
    seq = [r["residue"] for r in rows]
    rel = [r["relative"] for r in rows]
    cm = [r["depth_cm"] for r in rows]
    lines = [
        "Inputs: p = {}, f0 = {:g} Hz, c = {:g} m/s".format(p, f0, c),
        "",
        "'mod' gives the remainder after division (example: 9 mod 7 = 2).",
        "",
        "Residue sequence s(n) = n^2 mod p:",
        str(seq),
        "",
        "Wavelength  lambda0 = c / f0       = {:.3f} m".format(w),
        "Max depth   Dmax = lambda0 / 2     = {:.3f} m ({:.3f} cm)".format(dmax, dmax * 100),
        "",
        "Relative depths r(n) = s(n) / max(s):",
        list_text(rel, 3),
        "",
        "Physical depths d(n) = r(n) x Dmax (cm):",
        list_text(cm, 3),
        "",
        format_table(rows),
        "",
        NOTE,
    ]
    return "\n".join(lines)


def format_compare(results, f0, c):
    """Residues and depth profile for each prime."""
    lines = ["Comparison of primes (f0 = {:g} Hz, c = {:g} m/s)".format(f0, c), ""]
    for item in results:
        lines.append("p = {}  ({} wells)".format(item["p"], item["p"]))
        lines.append("  Residues   : " + str(item["residues"]))
        lines.append("  Relative   : " + list_text(item["relative"], 3))
        lines.append("  Depth (cm) : " + list_text(item["depth_cm"], 3))
        lines.append("")
    lines.append("Changing the prime changes the pattern AND the number of wells.")
    lines.append("A larger prime does NOT automatically mean better sound diffusion;")
    lines.append("that can only be judged by simulation or real measurement.")
    return "\n".join(lines)


def format_frequency(p, c, table):
    """Wavelength and depths for several frequencies."""
    head = "{:>12} {:>16} {:>16}".format("f0 (Hz)", "Wavelength (m)", "Max depth (cm)")
    lines = ["Frequency exploration (p = {}, c = {:g} m/s)".format(p, c), "", head,
             "-" * len(head)]
    for row in table:
        lines.append("{:>12g} {:>16.4f} {:>16.3f}".format(
            row["f0"], row["wavelength_m"], row["dmax_cm"]))
    lines.append("")
    lines.append("Depths of every well (cm):")
    for row in table:
        lines.append("  f0 = {:g} Hz: ".format(row["f0"]) + list_text(row["depth_cm"], 3))
    lines.append("")
    lines.append("When the frequency goes UP, the wavelength goes DOWN (c is constant),")
    lines.append("so all calculated depths become smaller.")
    lines.append("This is only a mathematical exploration, not a real acoustic test.")
    return "\n".join(lines)


# ---------- saving files ----------

def save_csv(rows, path):
    """Save the results table as CSV. Values are NOT rounded."""
    if not rows:
        raise ValueError("There are no results to save.")
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)
        for r in rows:
            writer.writerow([r["n"], r["square"], r["residue"],
                             repr(r["relative"]), repr(r["depth_m"]), repr(r["depth_cm"])])
    return path


def make_report_text(p, f0, c, rows):
    """Short text report: inputs, formulas, results, limitations."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "QUADRATIC RESIDUE DIFFUSER - SHORT REPORT",
        "Generated on: " + now,
        "=" * 60,
        "",
        "INPUTS",
        "  Prime p                 : {}".format(p),
        "  Design frequency f0     : {:g} Hz".format(f0),
        "  Speed of sound c        : {:g} m/s".format(c),
        "",
        "FORMULAS (simplified normalization-based model)",
        "  s(n)    = n^2 mod p",
        "  r(n)    = s(n) / max(s)",
        "  lambda0 = c / f0",
        "  Dmax    = lambda0 / 2",
        "  d(n)    = r(n) x Dmax",
        "",
        "RESULTS",
        format_summary(p, f0, c, rows),
        "",
        "LIMITATIONS",
        "  1. Depths are calculated, not measured. This report does not prove",
        "     that the diffuser improves sound diffusion.",
        "  2. The model is simplified. Textbooks also use d(n) = s(n) x lambda0 / (2p),",
        "     which is a separate design method and gives different depths.",
        "  3. Real diffusers also depend on well width, material, bandwidth and",
        "     edge effects, which are not modelled here.",
        "  4. Real performance needs an acoustic simulation or a physical test.",
        "",
    ]
    return "\n".join(lines)


def save_report(text, path):
    """Save the report text file."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


# ---------- MATLAB (plotting only) ----------

def find_matlab():
    """Return the path of the MATLAB program if it is on PATH, else None."""
    return shutil.which("matlab")


def matlab_statement(csv_path, png_path):
    """The MATLAB command that draws the graph."""
    def q(text):                      # MATLAB strings double the single quote
        return str(text).replace("'", "''")
    return "addpath('{}'); plot_depths('{}', '{}');".format(
        q(MATLAB_DIR), q(csv_path), q(png_path))


def run_matlab(csv_path, png_path):
    """Ask MATLAB to draw the graph. Returns (ok, message)."""
    exe = find_matlab()
    if exe is None:
        return False, ("MATLAB was not found on your PATH.\n"
                       "The CSV file is saved. Open MATLAB and run:\n  "
                       + matlab_statement(csv_path, png_path))
    folder = os.path.dirname(png_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    if os.path.exists(png_path):
        os.remove(png_path)           # so an old graph is never mistaken for a new one
    try:
        result = subprocess.run([exe, "-batch", matlab_statement(csv_path, png_path)],
                                capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.SubprocessError) as error:
        return False, "Could not run MATLAB: " + str(error)
    if result.returncode != 0 or not os.path.exists(png_path):
        details = (result.stderr or result.stdout or "").strip()[-500:]
        return False, "MATLAB did not create the graph.\n" + details
    return True, "Graph saved: " + png_path


def copy_graph(destination):
    """Copy the last MATLAB graph to another place chosen by the user."""
    if not os.path.exists(DEFAULT_PNG):
        raise FileNotFoundError("No graph yet. Click 'Create MATLAB graph' first.")
    shutil.copyfile(DEFAULT_PNG, destination)
    return destination

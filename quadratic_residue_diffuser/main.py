# main.py
# Main program: Tkinter interface, with a terminal menu as a backup.
# Run with:  python main.py
import os
import shutil

import calculations as calc
import validation as val
import exports as ex
from explanation import EXPLANATION

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    TK_OK = True
except ImportError:          # Tkinter not installed -> terminal version is used
    TK_OK = False


# ---------------- actions shared by the GUI and the terminal ----------------

def run_calculate(p_text, f_text, c_text):
    """Validate, calculate. Returns (True, data_dict) or (False, message)."""
    ok, result = val.validate_all(p_text, f_text, c_text)
    if not ok:
        return False, result
    p, f0, c = result
    rows = calc.build_results(p, f0, c)
    text = ex.format_summary(p, f0, c, rows)
    return True, {"p": p, "f0": f0, "c": c, "rows": rows, "text": text}


def run_compare(primes_text, f_text, c_text):
    """Compare several primes. Returns (ok, text_or_message)."""
    ok, primes = val.validate_prime_list(primes_text)
    if not ok:
        return False, primes
    ok, f0 = val.validate_positive(f_text, "Frequency")
    if not ok:
        return False, f0
    ok, c = val.validate_positive(c_text, "Speed of sound")
    if not ok:
        return False, c
    return True, ex.format_compare(calc.compare_primes(primes, f0, c), f0, c)


def run_frequency(p_text, freq_text, c_text):
    """Explore several frequencies. Returns (ok, text_or_message)."""
    ok, p = val.validate_prime(p_text)
    if not ok:
        return False, p
    ok, freqs = val.validate_frequency_list(freq_text)
    if not ok:
        return False, freqs
    ok, c = val.validate_positive(c_text, "Speed of sound")
    if not ok:
        return False, c
    return True, ex.format_frequency(p, c, calc.frequency_table(p, c, freqs))


# ---------------- Tkinter interface ----------------

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quadratic Residue Diffuser - Number Theory Project")
        self.root.geometry("860x640")
        self.data = None                       # last successful calculation
        self.make_inputs()
        self.make_tabs()
        self.calculate()                       # show the default example at start

    # ----- layout -----
    def make_inputs(self):
        frame = ttk.LabelFrame(self.root, text="Inputs")
        frame.pack(fill="x", padx=8, pady=6)
        self.p_var = tk.StringVar(value="7")
        self.f_var = tk.StringVar(value="500")
        self.c_var = tk.StringVar(value="343")
        items = [("Prime p:", self.p_var), ("Frequency f0 (Hz):", self.f_var),
                 ("Speed of sound c (m/s):", self.c_var)]
        for i, (label, var) in enumerate(items):
            ttk.Label(frame, text=label).grid(row=0, column=2 * i, padx=4, pady=6)
            ttk.Entry(frame, textvariable=var, width=10).grid(row=0, column=2 * i + 1)
        ttk.Button(frame, text="Calculate", command=self.calculate).grid(
            row=0, column=6, padx=10)
        self.status = tk.StringVar(value="Ready.")
        self.status_label = tk.Label(self.root, textvariable=self.status, anchor="w")
        self.status_label.pack(fill="x", padx=10)

    def make_text(self, parent):
        box = scrolledtext.ScrolledText(parent, font=("Courier New", 10), wrap="word")
        box.pack(fill="both", expand=True, padx=4, pady=4)
        return box

    def make_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=8, pady=6)

        # Tab 1: results
        t1 = ttk.Frame(self.tabs)
        self.tabs.add(t1, text="Results")
        self.results_box = self.make_text(t1)

        # Tab 2: compare primes
        t2 = ttk.Frame(self.tabs)
        self.tabs.add(t2, text="Compare primes")
        bar = ttk.Frame(t2)
        bar.pack(fill="x", padx=4, pady=4)
        ttk.Label(bar, text="Primes (comma separated):").pack(side="left")
        self.primes_var = tk.StringVar(value="5, 7, 11, 13")
        ttk.Entry(bar, textvariable=self.primes_var, width=24).pack(side="left", padx=6)
        ttk.Button(bar, text="Compare", command=self.compare).pack(side="left")
        self.compare_box = self.make_text(t2)

        # Tab 3: frequency exploration
        t3 = ttk.Frame(self.tabs)
        self.tabs.add(t3, text="Frequency exploration")
        bar = ttk.Frame(t3)
        bar.pack(fill="x", padx=4, pady=4)
        ttk.Label(bar, text="Frequencies in Hz (comma separated):").pack(side="left")
        self.freqs_var = tk.StringVar(value="250, 500, 1000, 2000")
        ttk.Entry(bar, textvariable=self.freqs_var, width=24).pack(side="left", padx=6)
        ttk.Button(bar, text="Explore", command=self.explore).pack(side="left")
        self.freq_box = self.make_text(t3)

        # Tab 4: explanation
        t4 = ttk.Frame(self.tabs)
        self.tabs.add(t4, text="Explanation")
        self.explain_box = self.make_text(t4)
        self.set_text(self.explain_box, EXPLANATION)

        # Tab 5: export
        t5 = ttk.Frame(self.tabs)
        self.tabs.add(t5, text="Export")
        bar = ttk.Frame(t5)
        bar.pack(fill="x", padx=4, pady=8)
        ttk.Button(bar, text="Save results CSV", command=self.save_csv).pack(side="left", padx=4)
        ttk.Button(bar, text="Create MATLAB graph", command=self.make_graph).pack(side="left", padx=4)
        ttk.Button(bar, text="Save graph PNG as...", command=self.save_png).pack(side="left", padx=4)
        ttk.Button(bar, text="Save text report", command=self.save_report).pack(side="left", padx=4)
        self.export_box = self.make_text(t5)
        self.set_text(self.export_box, "Export messages will appear here.\n")

    # ----- small helpers -----
    def set_text(self, box, text):
        box.config(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", text)
        box.config(state="disabled")

    def log(self, message):
        self.export_box.config(state="normal")
        self.export_box.insert("end", message + "\n\n")
        self.export_box.see("end")
        self.export_box.config(state="disabled")

    def show_ok(self, message):
        self.status.set(message)
        self.status_label.config(fg="dark green")

    def show_error(self, message):
        self.status.set("Error: " + message)
        self.status_label.config(fg="red")
        messagebox.showerror("Invalid input", message)

    # ----- button actions -----
    def calculate(self):
        ok, result = run_calculate(self.p_var.get(), self.f_var.get(), self.c_var.get())
        if not ok:
            self.show_error(result)
            return False
        self.data = result
        self.set_text(self.results_box, result["text"])
        self.show_ok("Calculated for p = {}, f0 = {:g} Hz, c = {:g} m/s.".format(
            result["p"], result["f0"], result["c"]))
        return True

    def compare(self):
        ok, result = run_compare(self.primes_var.get(), self.f_var.get(), self.c_var.get())
        if not ok:
            self.show_error(result)
            return
        self.set_text(self.compare_box, result)
        self.show_ok("Comparison done.")

    def explore(self):
        ok, result = run_frequency(self.p_var.get(), self.freqs_var.get(), self.c_var.get())
        if not ok:
            self.show_error(result)
            return
        self.set_text(self.freq_box, result)
        self.show_ok("Frequency exploration done.")

    def save_csv(self):
        if not self.calculate():               # always use the current inputs
            return
        path = filedialog.asksaveasfilename(
            initialdir=ex.DATA_DIR, initialfile="results.csv",
            defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
        if not path:
            return
        try:
            ex.save_csv(self.data["rows"], path)
            self.log("CSV saved: " + path)
        except OSError as error:
            messagebox.showerror("Could not save", str(error))

    def make_graph(self):
        if not self.calculate():
            return
        try:
            ex.save_csv(self.data["rows"], ex.DEFAULT_CSV)
        except OSError as error:
            messagebox.showerror("Could not save", str(error))
            return
        self.show_ok("Running MATLAB, please wait...")
        self.root.update()
        ok, message = ex.run_matlab(ex.DEFAULT_CSV, ex.DEFAULT_PNG)
        self.log(message)
        if ok:
            self.show_ok("MATLAB graph created.")
        else:
            messagebox.showinfo("MATLAB graph", message)

    def save_png(self):
        if not os.path.exists(ex.DEFAULT_PNG):
            messagebox.showinfo("No graph yet", "Click 'Create MATLAB graph' first.")
            return
        path = filedialog.asksaveasfilename(
            initialdir=ex.GRAPH_DIR, initialfile="depths_copy.png",
            defaultextension=".png", filetypes=[("PNG image", "*.png")])
        if not path:
            return
        try:
            ex.copy_graph(path)
            self.log("Graph copied to: " + path)
        except (OSError, shutil.Error) as error:
            messagebox.showerror("Could not save", str(error))

    def save_report(self):
        if not self.calculate():
            return
        d = self.data
        path = filedialog.asksaveasfilename(
            initialdir=ex.REPORT_DIR, initialfile="report_p{}.txt".format(d["p"]),
            defaultextension=".txt", filetypes=[("Text file", "*.txt")])
        if not path:
            return
        try:
            ex.save_report(ex.make_report_text(d["p"], d["f0"], d["c"], d["rows"]), path)
            self.log("Report saved: " + path)
        except OSError as error:
            messagebox.showerror("Could not save", str(error))

    def run(self):
        self.root.mainloop()


# ---------------- terminal version (backup) ----------------

def ask(prompt, default):
    """Ask the user; an empty answer means the default."""
    text = input(prompt + " [" + str(default) + "]: ").strip()
    return text if text else str(default)


def terminal_calculate():
    """Ask for the three inputs and show the results. Returns data or None."""
    ok, result = run_calculate(ask("Prime p", 7), ask("Frequency f0 (Hz)", 500),
                               ask("Speed of sound c (m/s)", 343))
    if ok:
        print("\n" + result["text"])
        return result
    print("Error:", result)
    return None


def terminal_export(choice, data):
    """Options 4, 5 and 6 of the menu."""
    try:
        if choice == "4":
            print("Saved:", ex.save_csv(data["rows"], ex.DEFAULT_CSV))
        elif choice == "5":
            ex.save_csv(data["rows"], ex.DEFAULT_CSV)
            print(ex.run_matlab(ex.DEFAULT_CSV, ex.DEFAULT_PNG)[1])
        else:
            path = os.path.join(ex.REPORT_DIR, "report_p{}.txt".format(data["p"]))
            text = ex.make_report_text(data["p"], data["f0"], data["c"], data["rows"])
            print("Saved:", ex.save_report(text, path))
    except OSError as error:
        print("Error: could not save the file:", error)


def terminal_menu():
    print("Quadratic Residue Diffuser (terminal version)")
    data = None
    while True:
        print("\n1 Calculate   2 Compare primes   3 Frequency exploration")
        print("4 Save CSV    5 Create MATLAB graph  6 Save report")
        print("7 Explanation 0 Quit")
        choice = input("Choose: ").strip()
        if choice == "0":
            return
        elif choice == "1":
            data = terminal_calculate() or data
        elif choice == "2":
            ok, result = run_compare(ask("Primes", "5, 7, 11, 13"), ask("Frequency f0 (Hz)", 500),
                                     ask("Speed of sound c (m/s)", 343))
            print("\n" + result if ok else "Error: " + result)
        elif choice == "3":
            ok, result = run_frequency(ask("Prime p", 7), ask("Frequencies (Hz)", "250, 500, 1000, 2000"),
                                       ask("Speed of sound c (m/s)", 343))
            print("\n" + result if ok else "Error: " + result)
        elif choice in ("4", "5", "6"):
            if data is None:                   # nothing calculated yet
                data = terminal_calculate()
            if data is not None:
                terminal_export(choice, data)
        elif choice == "7":
            print(EXPLANATION)
        else:
            print("Please type a number from the menu.")


def main():
    if TK_OK:
        try:
            App().run()
            return
        except tk.TclError:                    # e.g. no display available
            print("The window could not be opened. Using the terminal version.")
    else:
        print("Tkinter is not installed. Using the terminal version.")
    try:
        terminal_menu()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")


if __name__ == "__main__":
    main()

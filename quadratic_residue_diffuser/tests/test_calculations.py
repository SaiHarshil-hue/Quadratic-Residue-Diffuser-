# tests/test_calculations.py
# Tests for calculations, validation, exports and the shared actions.
# Run from the project folder:   python tests\test_calculations.py
import csv
import math
import os
import sys
import tempfile
import unittest

# Let the tests find the project files in the parent folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import calculations as calc
import validation as val
import exports as ex
import main as app


class TestCalculations(unittest.TestCase):
    def test_sequence_p7(self):
        self.assertEqual(calc.residue_sequence(7), [0, 1, 4, 2, 2, 4, 1])

    def test_squares_p7(self):
        self.assertEqual(calc.square_list(7), [0, 1, 4, 9, 16, 25, 36])

    def test_relative_p7(self):
        rel = calc.relative_depths(calc.residue_sequence(7))
        self.assertEqual(rel, [0, 0.25, 1, 0.5, 0.5, 1, 0.25])

    def test_wavelength_and_dmax(self):
        w = calc.wavelength(343, 500)
        self.assertTrue(math.isclose(w, 0.686))
        self.assertTrue(math.isclose(calc.max_depth(w), 0.343))

    def test_physical_cm(self):
        rows = calc.build_results(7, 500, 343)
        expected = [0, 8.575, 34.3, 17.15, 17.15, 34.3, 8.575]
        for row, e in zip(rows, expected):
            self.assertTrue(math.isclose(row["depth_cm"], e, abs_tol=1e-9))

    def test_build_results_length(self):
        for p in (3, 5, 7, 11, 13, 997):
            self.assertEqual(len(calc.build_results(p, 500, 343)), p)

    def test_other_primes(self):
        self.assertEqual(calc.residue_sequence(5), [0, 1, 4, 4, 1])
        self.assertEqual(calc.residue_sequence(11), [0, 1, 4, 9, 5, 3, 3, 5, 9, 4, 1])
        self.assertEqual(calc.residue_sequence(13),
                         [0, 1, 4, 9, 3, 12, 10, 10, 12, 3, 9, 4, 1])

    def test_relative_between_0_and_1(self):
        for p in (3, 5, 7, 11, 13):
            rel = calc.relative_depths(calc.residue_sequence(p))
            self.assertEqual(min(rel), 0)
            self.assertEqual(max(rel), 1)

    def test_frequency_up_wavelength_down(self):
        table = calc.frequency_table(7, 343, [250, 500, 1000])
        waves = [row["wavelength_m"] for row in table]
        self.assertTrue(waves[0] > waves[1] > waves[2])
        self.assertTrue(math.isclose(table[1]["dmax_cm"], 34.3))

    def test_compare_primes(self):
        results = calc.compare_primes([5, 7], 500, 343)
        self.assertEqual(len(results[0]["residues"]), 5)
        self.assertEqual(len(results[1]["residues"]), 7)


class TestValidation(unittest.TestCase):
    def test_good_prime(self):
        self.assertEqual(val.validate_prime("7"), (True, 7))
        self.assertEqual(val.validate_prime(" 13 "), (True, 13))

    def test_bad_primes(self):
        for bad in ("2", "9", "1", "0", "-5", "abc", "", "7.5", "1009", "99999999999"):
            self.assertFalse(val.validate_prime(bad)[0], bad)

    def test_positive(self):
        self.assertEqual(val.validate_positive("500", "F"), (True, 500.0))
        for bad in ("0", "-3", "x", "nan", "inf", "", "1e400", "1e-9"):
            self.assertFalse(val.validate_positive(bad, "F")[0], bad)

    def test_lists(self):
        self.assertEqual(val.validate_prime_list("5, 7;11,13,7"), (True, [5, 7, 11, 13]))
        self.assertFalse(val.validate_prime_list("5, 8")[0])
        self.assertFalse(val.validate_prime_list("")[0])
        self.assertEqual(val.validate_frequency_list("250, 500"), (True, [250.0, 500.0]))
        self.assertFalse(val.validate_frequency_list("250, -1")[0])

    def test_validate_all(self):
        self.assertEqual(val.validate_all("7", "500", "343"), (True, (7, 500.0, 343.0)))
        self.assertFalse(val.validate_all("7", "0", "343")[0])
        self.assertFalse(val.validate_all("7", "500", "abc")[0])


class TestExportsAndActions(unittest.TestCase):
    def test_csv_roundtrip(self):
        rows = calc.build_results(7, 500, 343)
        with tempfile.TemporaryDirectory() as folder:
            path = ex.save_csv(rows, os.path.join(folder, "sub", "r.csv"))
            with open(path, newline="") as f:
                data = list(csv.reader(f))
        self.assertEqual(data[0], ex.CSV_HEADER)
        self.assertEqual(len(data), 8)                      # header + 7 wells
        self.assertEqual([int(r[2]) for r in data[1:]], [0, 1, 4, 2, 2, 4, 1])
        self.assertTrue(math.isclose(float(data[3][5]), 34.3))

    def test_csv_empty_rejected(self):
        with self.assertRaises(ValueError):
            ex.save_csv([], "never_written.csv")

    def test_report_text(self):
        rows = calc.build_results(7, 500, 343)
        text = ex.make_report_text(7, 500, 343, rows)
        for word in ("INPUTS", "FORMULAS", "RESULTS", "LIMITATIONS", "0.686", "34.300"):
            self.assertIn(word, text)

    def test_save_report(self):
        with tempfile.TemporaryDirectory() as folder:
            path = ex.save_report("hello", os.path.join(folder, "a.txt"))
            with open(path) as f:
                self.assertEqual(f.read(), "hello")

    def test_matlab_statement(self):
        s = ex.matlab_statement("C:\\a b\\it's.csv", "C:\\g\\d.png")
        self.assertIn("plot_depths(", s)
        self.assertIn("it''s.csv", s)

    def test_run_matlab_without_matlab(self):
        if ex.find_matlab() is None:
            ok, message = ex.run_matlab("x.csv", "y.png")
            self.assertFalse(ok)
            self.assertIn("plot_depths", message)

    def test_table_default_values(self):
        ok, data = app.run_calculate("7", "500", "343")
        self.assertTrue(ok)
        self.assertIn("0.686 m", data["text"])
        self.assertIn("34.300", data["text"])
        self.assertIn("[0, 1, 4, 2, 2, 4, 1]", data["text"])

    def test_actions_report_errors_not_crash(self):
        self.assertFalse(app.run_calculate("9", "500", "343")[0])
        self.assertFalse(app.run_calculate("7", "-5", "343")[0])
        self.assertFalse(app.run_compare("5, x", "500", "343")[0])
        self.assertFalse(app.run_frequency("7", "", "343")[0])
        ok, text = app.run_compare("5, 7, 11, 13", "500", "343")
        self.assertTrue(ok)
        self.assertIn("p = 13", text)
        ok, text = app.run_frequency("7", "250, 500, 1000, 2000", "343")
        self.assertTrue(ok)
        self.assertIn("1000", text)


if __name__ == "__main__":
    unittest.main()

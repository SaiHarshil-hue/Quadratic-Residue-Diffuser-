# calculations.py
# All the maths for the project. No input, no output, no graphs here.


def square_list(p):
    """Return n*n for n = 0, 1, ..., p-1."""
    return [n * n for n in range(p)]


def residue_sequence(p):
    """s(n) = n^2 mod p. 'mod' gives the remainder after division."""
    return [(n * n) % p for n in range(p)]


def relative_depths(sequence):
    """r(n) = s(n) / max(s). Safe because max(s) > 0 when p > 2."""
    biggest = max(sequence)
    if biggest == 0:
        raise ValueError("Largest residue is 0, cannot divide by it.")
    return [s / biggest for s in sequence]


def wavelength(c, f0):
    """lambda0 = c / f0 (in metres)."""
    return c / f0


def max_depth(wave):
    """Dmax = lambda0 / 2 (in metres)."""
    return wave / 2


def physical_depths(relative, dmax):
    """d(n) = r(n) * Dmax (in metres, NOT rounded)."""
    return [r * dmax for r in relative]


def build_results(p, f0, c):
    """Run the whole chain and return one dictionary (row) per well."""
    squares = square_list(p)
    seq = residue_sequence(p)
    rel = relative_depths(seq)
    dmax = max_depth(wavelength(c, f0))
    depth_m = physical_depths(rel, dmax)
    # The three lists must have the same length (safety check)
    if not (len(squares) == len(seq) == len(rel) == len(depth_m) == p):
        raise ValueError("Internal error: list lengths do not match.")
    rows = []
    for n in range(p):
        rows.append({
            "n": n,
            "square": squares[n],
            "residue": seq[n],
            "relative": rel[n],
            "depth_m": depth_m[n],
            "depth_cm": depth_m[n] * 100,
        })
    return rows


def compare_primes(primes, f0, c):
    """Return the pattern of each prime in the list (for comparison)."""
    results = []
    for p in primes:
        rows = build_results(p, f0, c)
        results.append({
            "p": p,
            "residues": [r["residue"] for r in rows],
            "relative": [r["relative"] for r in rows],
            "depth_cm": [r["depth_cm"] for r in rows],
        })
    return results


def frequency_table(p, c, frequencies):
    """For each frequency: wavelength, max depth and all depths (cm)."""
    seq = residue_sequence(p)
    rel = relative_depths(seq)
    table = []
    for f0 in frequencies:
        w = wavelength(c, f0)
        dmax = max_depth(w)
        depths = physical_depths(rel, dmax)
        table.append({
            "f0": f0,
            "wavelength_m": w,
            "dmax_cm": dmax * 100,
            "depth_cm": [d * 100 for d in depths],
        })
    return table

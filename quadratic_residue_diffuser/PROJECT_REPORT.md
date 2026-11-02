# Quadratic Residue Diffusers Using Number Theory in Acoustic Panel Design

**Short project report – First-year B.Tech CSE (AI), Amrita Vishwa Vidyapeetham, Coimbatore**

## 1. Aim
To build a simple program that uses modular arithmetic and quadratic residues to generate
well depths for a proposed acoustic diffuser, and to show how the depths change with the
prime number and the design frequency.

## 2. Introduction
A flat wall reflects sound mainly in one direction. A diffuser has wells of different depths,
so sound returning from different wells is delayed by different amounts and spreads out.
Number Theory gives a ready-made pattern of "different but orderly" numbers: the quadratic
residues. Here those numbers are turned into depths.

## 3. Method
1. Input a prime p, design frequency f₀ and speed of sound c (validated).
2. s(n) = n² mod p for n = 0 … p−1.
3. r(n) = s(n) / max(s).
4. λ₀ = c / f₀ and Dmax = λ₀ / 2.
5. d(n) = r(n) · Dmax.
6. Python exports the results to CSV; MATLAB reads the CSV and plots depth against well number.

Tools: Python (all calculations, validation, Tkinter interface), MATLAB (plotting only).

## 4. Result for the default input (p = 7, f₀ = 500 Hz, c = 343 m/s)

| n | n² | n² mod 7 | Relative | Depth (cm) |
|---|---|---|---|---|
| 0 | 0 | 0 | 0.000 | 0.000 |
| 1 | 1 | 1 | 0.250 | 8.575 |
| 2 | 4 | 4 | 1.000 | 34.300 |
| 3 | 9 | 2 | 0.500 | 17.150 |
| 4 | 16 | 2 | 0.500 | 17.150 |
| 5 | 25 | 4 | 1.000 | 34.300 |
| 6 | 36 | 1 | 0.250 | 8.575 |

λ₀ = 0.686 m, Dmax = 0.343 m. The pattern is symmetric because s(n) = s(p − n).

## 5. Observations
- Changing the prime changes both the pattern and the number of wells (p = 5, 7, 11, 13).
- Raising the frequency shortens the wavelength, so all depths shrink (c constant).
- A larger prime does not automatically give better diffusion.

## 6. Limitations
1. Depths are calculated, not measured; no acoustic performance is proven.
2. Simplified model: another textbook formula, d(n) = s(n)·λ₀/(2p), is a separate method and gives different depths.
3. Well width, materials, bandwidth, edge effects and sound absorption are ignored.
4. Only primes up to 1000 are accepted.
5. The MATLAB step needs MATLAB installed.

## 7. Possible future improvements
- Simulate the scattered sound (for example with a simple Fourier/Kirchhoff model) and compare patterns.
- Implement the d(n) = s(n)·λ₀/(2p) method as a clearly labelled second option.
- Add a 2-D (primitive-root) diffuser, and well-width input.
- Build a physical prototype and measure it.

## 8. Conclusion
The program correctly turns quadratic residues into well depths and lets the user explore
primes and frequencies. It is a mathematical model; real acoustic testing is the next step.

## 9. Viva questions and simple answers

1. **What is Number Theory?** The study of whole numbers and their patterns.
2. **What is a prime number?** A number greater than 1 with only two divisors: 1 and itself.
3. **What does "mod" mean?** The remainder after division. 9 mod 7 = 2.
4. **What is congruence?** a ≡ b (mod p) means a and b leave the same remainder when divided by p.
5. **What is a quadratic residue?** The remainder of a perfect square after dividing by p.
6. **Why must p be prime and greater than 2?** Quadratic residue diffusers use odd primes, because a prime modulus gives the well-behaved residue pattern. p = 2 would give only a trivial two-well pattern. (The normalization also needs max(s) ≠ 0.)
7. **Why is the sequence symmetric?** Because (p − n)² ≡ n² (mod p).
8. **What does a diffuser do?** It scatters reflected sound in many directions instead of one.
9. **Why do different depths help?** Sound returns from each well after a different delay, so the reflections are spread out.
10. **What is the wavelength formula?** λ = c / f.
11. **Why is Dmax = λ₀/2?** It is the simplified rule chosen in this model: the deepest well is half a wavelength at the design frequency.
12. **What happens when frequency rises?** Wavelength falls, so depths fall.
13. **Does your program prove the diffuser works?** No. It only calculates depths. Simulation or measurement is needed.
14. **Why Python for calculations and MATLAB for graphs?** To keep roles separate: Python for logic and interface, MATLAB for plotting.
15. **How does data go from Python to MATLAB?** Python saves a CSV file; MATLAB reads it with `readtable`.
16. **What if the user types a wrong value?** Validation shows a clear error message and the program continues.

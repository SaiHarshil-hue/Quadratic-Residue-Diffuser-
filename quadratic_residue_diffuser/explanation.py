# explanation.py
# Simple explanations for the Explanation panel (first-year level).

EXPLANATION = """EXPLANATION PANEL

1. Number Theory
Number Theory is the part of mathematics that studies whole numbers
(0, 1, 2, 3, ...) and the patterns hidden inside them.

2. Prime numbers
A prime number has exactly two divisors: 1 and itself.
Examples: 2, 3, 5, 7, 11, 13. (9 is not prime because 3 x 3 = 9.)

3. Modular arithmetic
'a mod p' means the remainder when a is divided by p.
Example: 9 mod 7 = 2, because 9 = 1 x 7 + 2.
It is like a clock: after reaching p, the count starts again from 0.

4. Congruence
Two numbers are congruent modulo p if they leave the same remainder
when divided by p. We write 9 = 2 (mod 7). Here 9 and 2 are congruent
modulo 7 because both leave remainder 2.

5. Quadratic residues
A quadratic residue is what you get by squaring a number and then taking
mod p. In this project: s(n) = n^2 mod p, for n = 0, 1, ..., p-1.
For p = 7 the sequence is [0, 1, 4, 2, 2, 4, 1].

6. Acoustic diffusers
When sound hits a flat wall it bounces back in one main direction.
An acoustic diffuser has wells (slots) of different depths. Sound
travels into each well and comes back after a different delay, so the
reflected sound is spread in many directions instead of one.

7. From residues to well depths (this project's simplified model)
  r(n)      = s(n) / max(s)      -> scales the residues to 0 ... 1
  lambda0   = c / f0             -> wavelength at the design frequency
  Dmax      = lambda0 / 2        -> deepest well in this simple model
  d(n)      = r(n) x Dmax        -> depth of well n
Bigger residue = deeper well. Different depths = different sound delays.

8. Different formula used in textbooks
Many textbooks use d(n) = s(n) x lambda0 / (2p). It is a SEPARATE design
method. It gives a smaller deepest well (for p = 7 it is 19.6 cm, while
this project's normalization model gives 34.3 cm). This project does not
mix the two formulas.

IMPORTANT: calculating depths does NOT prove that a diffuser sounds
better. Real performance needs an acoustic simulation or a physical test.
"""

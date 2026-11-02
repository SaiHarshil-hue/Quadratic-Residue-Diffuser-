# validation.py
# Input checks. Every function returns a pair: (ok, value_or_message).
# If ok is True the second item is the clean value.
# If ok is False the second item is a clear error message.
import math

MAX_PRIME = 1000      # keeps tables small and the program fast
MAX_LIST = 12         # most items allowed in a comparison list
MIN_VALUE = 1e-6      # smallest allowed frequency / speed
MAX_VALUE = 1e9       # largest allowed frequency / speed


def is_prime(n):
    """True if n is a prime number."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def validate_prime(text):
    """The modulus must be a whole number, prime, greater than 2."""
    try:
        p = int(str(text).strip())
    except ValueError:
        return False, "Prime must be a whole number (for example 7)."
    if p <= 2:
        return False, "Prime must be greater than 2."
    if p > MAX_PRIME:
        return False, "Prime must be at most " + str(MAX_PRIME) + " in this project."
    if not is_prime(p):
        return False, str(p) + " is not a prime number."
    return True, p


def validate_positive(text, name):
    """Frequency and speed of sound must be positive numbers."""
    try:
        x = float(str(text).strip())
    except ValueError:
        return False, name + " must be a number."
    if math.isnan(x) or math.isinf(x):
        return False, name + " must be a normal number."
    if x <= 0:
        return False, name + " must be greater than 0."
    if x < MIN_VALUE or x > MAX_VALUE:
        return False, name + " must be between 0.000001 and 1000000000."
    return True, x


def split_list(text):
    """Turn '5, 7, 11' into ['5', '7', '11'] (commas or semicolons)."""
    parts = str(text).replace(";", ",").split(",")
    return [part.strip() for part in parts if part.strip() != ""]


def validate_prime_list(text):
    """Check a comma-separated list of primes."""
    parts = split_list(text)
    if len(parts) == 0:
        return False, "Please enter at least one prime, for example 5, 7, 11, 13."
    if len(parts) > MAX_LIST:
        return False, "Please enter at most " + str(MAX_LIST) + " primes."
    primes = []
    for part in parts:
        ok, value = validate_prime(part)
        if not ok:
            return False, "In the prime list: " + value
        if value not in primes:        # ignore repeated primes
            primes.append(value)
    return True, primes


def validate_frequency_list(text):
    """Check a comma-separated list of frequencies."""
    parts = split_list(text)
    if len(parts) == 0:
        return False, "Please enter at least one frequency, for example 250, 500, 1000."
    if len(parts) > MAX_LIST:
        return False, "Please enter at most " + str(MAX_LIST) + " frequencies."
    values = []
    for part in parts:
        ok, value = validate_positive(part, "Frequency")
        if not ok:
            return False, "In the frequency list: " + value
        values.append(value)
    return True, values


def validate_all(p_text, f_text, c_text):
    """Check the three main inputs. Returns (True, (p, f0, c)) or (False, message)."""
    ok, p = validate_prime(p_text)
    if not ok:
        return False, p
    ok, f0 = validate_positive(f_text, "Frequency")
    if not ok:
        return False, f0
    ok, c = validate_positive(c_text, "Speed of sound")
    if not ok:
        return False, c
    return True, (p, f0, c)

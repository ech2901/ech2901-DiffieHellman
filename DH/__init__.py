from math import floor, ceil, log2
from random import randint

def modp(base: int, exp: int, mod: int) -> int:
    # Modular exponentiation function
    calculation = base
    base = 1
    while exp:
        if 1 & exp:
            base = (base * calculation) % mod
        calculation = (calculation**2) % mod
        exp = exp >> 1
    return base

def perfect_square(value: int) -> bool:
    # https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
    # Appendix C section 4
    # Checking for a perfect square algorithm
    n = floor(log2(value)) + 1
    exp = ceil(n/2)

    diff = (2**exp) - (2**(exp-1))
    witness = randint(0, diff) + (2**(exp-1))

    while True:
        witness = ((witness**2) + value) / (2 * witness)
        if (witness**2) < ((2**exp) + value):
            break

    return value == floor(witness) ** 2

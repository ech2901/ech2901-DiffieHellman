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

def perfect_square(c: int) -> bool:
    n = floor(log2(c))+1
    m = ceil(n/2)

    diff = (2**m) - (2**(m-1))
    x = randint(0, diff) + (2**(m-1))

    while True:
        x = ((x**2)+c)/(2*x)
        if (x**2) < ((2**m)+c):
            break

    return c == floor(x)**2
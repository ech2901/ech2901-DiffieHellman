from math import floor, ceil, log2, gcd
from random import randint
from secrets import randbits


def decompose(value: int) -> [int, int]:
    # Decompose a value such that
    # value = 2^n * m
    if value in (1, 2):
        return value-1, 1
    if value == 0:
        return 0, 0
    exp = (value & (~(value-1))).bit_length()-1
    m = value >> exp
    return exp, m

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

def jacobi(a: int, n: int) -> int:
    # https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
    # Appendix C section 5
    a = a % n
    if a == 1 or n == 1:
        return 1
    if a == 0:
        return 0

    exp, a = decompose(a)

    if exp % 2 == 0:
        s = 1
    elif (n % 8) == 1 or (n % 8) == 7:
        s = 1
    elif (n % 8) == 3 or (n % 8) == 5:
        s = -1
    if (n % 4) == 3 and (a % 4) == 3:
        s = -s

    n = n % a
    return s * jacobi(n, a)

def miller_rabin(prime: int, iterations: int) -> bool:
    # Miller-Rabin primality test
    # This has the possibility to have a bad witness
    # This would raise a false positive indicating a
    # prime number for a composite number.
    # Recommendation is to follow with a Lucas test to verify
    # the primality.
    # https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
    # Appendix C Section 3.1
    if prime in (1, 2, 3):
        # Prevent infinite loop later
        # A future check for 1 < witness < prime-1
        # will infinite loop for values 1, 2, or 3
        return True

    # Decompose prime to test into
    # expression: prime-1 = 2^exp * m
    exp, m = decompose(prime-1)
    prime_bits = prime.bit_length()

    # Track witnesses so we can
    # guarantee unique tests
    witness_list = list()

    for _ in range(iterations):
        while True:
            witness = randbits(prime_bits)
            if witness in witness_list:
                continue
            if 1 < witness < prime-1:
                break
        witness_list.append(witness)

        test = modp(witness, m, prime)
        if test == 1 or test == (prime-1):
            return True
        for _ in range(exp):
            test = modp(test, 2, prime)
            if test == prime-1:
                return True
            if test == 1:
                break
        return False
    return True

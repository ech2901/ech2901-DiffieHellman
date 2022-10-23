from random import randint
from unittest import TestCase, TestSuite
from math import sqrt

from DH import decompose, modp, perfect_square, miller_rabin, is_prime

iter_count = 10_000

# Consensus is that 50 iterations has a very very very small
# chance of a composite number causing a false positive.
miller_rabin_iterations = 70

max_tests = 10_000

# First 100,000 known primes
# https://oeis.org/A000040/a000040.txt
with open('a000040.txt', 'r') as file:
    known_primes = map(lambda line: line.split(' '), [file.readline() for _ in range(max_tests)])
    known_primes = map(lambda value: (int(value[0]), int(value[1])), known_primes)
known_primes = list(known_primes)

class Decompose(TestCase):
    def test_values(self):
        for value in range(iter_count):
            exp, m = decompose(value)
            with self.subTest(f'{value=}, {exp=}, {m=}'):
                self.assertEqual(value, (2**exp)*m)


class MODP(TestCase):
    def test_iteration(self):
        for _ in range(iter_count):
            base = randint(1, iter_count)
            exp = randint(1, iter_count)
            mod = randint(1, iter_count)

            with self.subTest(f'{base=}, {exp=}, {mod=}'):
                known = int(base**exp) % mod
                test = modp(base, exp, mod)
                self.assertEqual(test, known)


class PerfectSquare(TestCase):
    def test_known_perfect_squares(self):
        for val in map(lambda x: x**2, range(1, iter_count)):
            with self.subTest(f'{val=}'):
                self.assertTrue(perfect_square(val))

    def test_known_non_perfect_squares(self):
        for val in range(2, iter_count):
            if sqrt(val).is_integer():
                continue
            with self.subTest(f'{val=}'):
                self.assertFalse(perfect_square(val))


class MillerRabin(TestCase):

    def test_known_primes(self):
        for index, prime in known_primes:
            if index > max_tests:
                break
            with self.subTest(f'{index=}, {prime=}'):
                verify = miller_rabin(prime, miller_rabin_iterations)
                self.assertTrue(verify)

    def test_composites(self):
        for _ in range(iter_count):
            a, b = randint(2, 100), randint(2, 100)
            with self.subTest(f'{a**b=}'):
                verify = miller_rabin(a**b, miller_rabin_iterations)
                self.assertFalse(verify)


class IsPrime(TestCase):
    def test_known_primes(self):
        for _, prime in known_primes:
            with self.subTest(prime):
                self.assertTrue(is_prime(prime))

    def test_composites(self):
        for _ in range(iter_count):
            a, b = randint(2, 1000), randint(2, 1000)
            test_val = a*b
            with self.subTest(f'{a,b, test_val=}'):
                self.assertFalse(is_prime(test_val))

if __name__ == '__main__':
    pass


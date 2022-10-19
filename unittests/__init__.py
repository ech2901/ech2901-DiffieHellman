from unittest import TestCase, TestSuite
from math import sqrt

from DH import modp, perfect_square

iter_count = 100


class MODP(TestCase):
    def test_iteration(self):
        for base in range(1, iter_count):
            for exp in range(1, iter_count):
                for mod in range(1, iter_count):
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


if __name__ == '__main__':
    TestSuite.run()


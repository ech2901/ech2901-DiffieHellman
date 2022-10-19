from unittest import TestCase, TestSuite

from DH import modp, perfect_square

iter_count = 10


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
    def test_known_values(self):
        for val in map(lambda x:x**2, range(1, iter_count)):
            with self.subTest(f'{val=}'):
                self.assertTrue(perfect_square(val))

if __name__ == '__main__':
    TestSuite.run()
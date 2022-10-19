from unittest import TestCase

from DH import modp

iter_count = 100


class MODP(TestCase):
    def test_iteration(self):
        for base in range(1, iter_count):
            for exp in range(1, iter_count):
                for mod in range(1, iter_count):
                    known = int(base**exp) % mod
                    test = modp(base, exp, mod)
                    self.assertEqual(test, known)


if __name__ == '__main__':
    MODP.run()
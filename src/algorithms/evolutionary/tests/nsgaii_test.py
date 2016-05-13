#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from nsgaii import objective1, objective2, decode, crossover, dominates, fast_nondominated_sort


class TestNsgaii(unittest.TestCase):
    def setUp(self):
        pass

    def testObjective1(self):
        # optima
        self.assertEquals(0, objective1([0, 0]))
        # limits
        self.assertEquals(2000000, objective1([-1000, -1000]))
        self.assertEquals(2000000, objective1([1000, 1000]))

    def testObjective2(self):
        # optima
        self.assertEquals(0, objective2([2, 2]))  # 2,2
        # limits
        self.assertEquals(2000000, objective1([-1000, -1000]))
        self.assertEquals(2000000, objective1([1000, 1000]))

    def testDecode(self):
        # zero
        v = decode("0000000000000000", [[0, 1]], 16)
        self.assertEquals(1, len(v))
        self.assertEquals(0.0, v[0])
        # one
        v = decode("1111111111111111", [[0, 1]], 16)
        self.assertEquals(1, len(v))
        self.assertEquals(1.0, v[0])
        # float #1
        v = decode("0000000000000001", [[0, 1]], 16)
        self.assertEquals(1, len(v))
        a = 1.0 / ((2 ** 16) - 1)
        self.assertEquals(a * (2 ** 0), v[0])
        # float #2
        v = decode("0000000000000010", [[0, 1]], 16)
        self.assertEquals(1, len(v))
        self.assertEquals(a * (2 ** 1), v[0])
        # float #3
        v = decode("0000000000000100", [[0, 1]], 16)
        self.assertEquals(1, len(v))
        self.assertEquals(a * (2 ** 2), v[0])
        # multiple floats
        v = decode("00000000000000001111111111111111", [[0, 1], [0, 1]], 16)
        self.assertEquals(2, len(v))
        self.assertEquals(0.0, v[0])
        self.assertEquals(1.0, v[1])

    def testCrossover(self):
        p1 = "0000000000"
        p2 = "1111111111"
        self.assertEquals(p1, crossover(p1, p2, 0))
        self.assertNotEqual(p1, crossover(p1, p2, 1))
        s = crossover(p1, p2, 1)
        self.assertTrue(p1[0] == s[0] or p2[0] == s[0])
        self.assertTrue(p1[1] == s[1] or p2[1] == s[1])

    def testDominates(self):
        # smaller
        self.assertEquals(False, dominates({"objectives": [1, 1]}, {"objectives": [0, 0]}))
        # equal
        self.assertEquals(True, dominates({"objectives": [0, 0]}, {"objectives": [0, 0]}))
        # bigger
        self.assertEquals(True, dominates({"objectives": [0, 0]}, {"objectives": [1, 1]}))
        # partial
        self.assertEquals(False, dominates({"objectives": [0, 1]}, {"objectives": [1, 0]}))

    def test_fast_nondominated_sort(self):
        # one front
        pop = [{'objectives': [1, 1]}]
        rs = fast_nondominated_sort(pop)
        self.assertEquals(1, len(rs))
        # two fronts
        pop = [{'objectives': [1, 1]}, {'objectives': [0, 0]}]
        rs = fast_nondominated_sort(pop)
        self.assertEquals(2, len(rs))
        self.assertEquals(pop[1], rs[0][0])
        self.assertEquals(pop[0], rs[1][0])
        # two members of first front
        pop = [{'objectives': [1, 1]}, {'objectives': [1, 1]}]
        rs = fast_nondominated_sort(pop)
        self.assertEquals(1, len(rs))
        self.assertEquals(pop, rs[0])


if __name__ == '__main__':
    unittest.main()

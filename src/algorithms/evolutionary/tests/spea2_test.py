#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from spea2 import objective1, objective2, decode, point_mutation, binary_tournament, crossover, reproduce

class TestSpea2(unittest.TestCase):
    def setUp(self):
        pass

    def test_objective1(self):
        # optima
        self.assertEqual(0, objective1([0, 0]))  # 0,0
        # limits
        self.assertEqual(2000000, objective1([-1000, -1000]))
        self.assertEqual(2000000, objective1([1000, 1000]))

    def test_objective2(self):
        # optima
        self.assertEqual(0, objective2([2, 2])) # 2,2
        # limits
        self.assertEqual(2000000, objective1([-1000, -1000]))
        self.assertEqual(2000000, objective1([1000, 1000]))

    def test_decode(self):
        # zero
        v = decode("0000000000000000", [[0, 1]], 16)
        self.assertEqual(1, len(v))
        self.assertEqual(0.0, v[0])
        # one
        v = decode("1111111111111111", [[0, 1]], 16)
        self.assertEqual(1, len(v))
        self.assertEqual(1.0, v[0])
        # float #1
        v = decode("0000000000000001", [[0, 1]], 16)
        self.assertEqual(1, len(v))
        a = 1.0 / ((2**16)-1)
        self.assertEqual(a*(2**0), v[0])
        # float #2
        v = decode("0000000000000010", [[0, 1]], 16)
        self.assertEqual(1, len(v))
        self.assertEqual(a*(2**1), v[0])
        # float #3
        v = decode("0000000000000100", [[0, 1]], 16)
        self.assertEqual(1, len(v))
        self.assertEqual(a*(2**2), v[0])
        # multiple floats
        v = decode("00000000000000001111111111111111", [[0, 1],[0, 1]], 16)
        self.assertEqual(2, len(v))
        self.assertEqual(0.0, v[0])
        self.assertEqual(1.0, v[1])

    def test_point_mutation(self):
        self.assertEqual("0000000000", point_mutation("0000000000", 0))
        self.assertEqual("1111111111", point_mutation("1111111111", 0))
        self.assertEqual("1111111111", point_mutation("0000000000", 1))
        self.assertEqual("0000000000", point_mutation("1111111111", 1))

    def test_point_mutation_ratio(self):
        changes = 0
        for x in xrange(100):
            s = point_mutation("0000000000", 0.5)
            changes += (10 - len(s.replace('1', '')))
        self.assertAlmostEqual(0.5, float(changes)/(100*10), delta=0.05)

    def test_binary_tournament(self):
        pop = [{'fitness': i} for i in xrange(10)]
        for i in xrange(10):
            self.assertTrue(binary_tournament(pop) in pop)

    def test_crossover(self):
        p1 = "0000000000"
        p2 = "1111111111"
        self.assertEqual(p1, crossover(p1, p2, 0))
        self.assertNotEquals(id(p1), id(crossover(p1, p2, 0)))
        s = crossover(p1, p2, 1)
        for i in xrange(len(s)):
            self.assertTrue(p1[i] == s[i] or p2[i] == s[i])

    def test_reproduce(self):
        # normal
        pop = [{'fitness': i, 'bitstring': "0000000000"} for i in xrange(10)]
        children = reproduce(pop, len(pop), 1)
        self.assertEqual(len(pop), len(children))
        self.assertNotEquals(id(pop), id(children))
        for i, child in enumerate(children):
            self.assertNotEqual(id(pop[i]['bitstring']), id(children[i]['bitstring']))
        # odd sized pop
        pop = [{'fitness': i, 'bitstring': "0000000000"} for i in xrange(9)]
        children = reproduce(pop, len(pop), 0)
        self.assertEqual(len(pop), len(children))
        self.assertNotEquals(id(pop), id(children))
        for i, child in enumerate(children):
            self.assertNotEqual(id(pop[i]['bitstring']), id(children[i]['bitstring']))
        # odd sized pop, and mismatched
        pop = [{'fitness': i, 'bitstring': "0000000000"} for i in xrange(10)]
        children = reproduce(pop, 9, 0)
        self.assertEqual(9, len(children))
        self.assertNotEquals(id(pop), id(children))
        for i, child in enumerate(children):
            self.assertNotEqual(id(pop[i]['bitstring']), id(children[i]['bitstring']))

if __name__ == '__main__':
    unittest.main()


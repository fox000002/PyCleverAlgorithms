
#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from genetic_algorithm import iif, point_mutation, crossover, reproduce, search

class TestGeneticAlgorithm(unittest.TestCase):
    def setUp(self):
        pass

    def test_iif(self):
        self.assertEqual(iif(1<50, "1", "0"), "1")
        self.assertEqual(iif('0'=='1', 1, 0), 0)

    def test_point_mutation(self):
        p = "1100"
        c = point_mutation(p, 0.1)
        self.assertEqual(len(c), len(p))
        print c

    def test_crossover(self):
        p1 = "1234"
        p2 = "4321"
        c = crossover(p1, p2, 0.5)
        self.assertEqual(len(c), len(p1))
        print c

    def test_reproduce(self):
        s = [{'bitstring' : "1100"}, {'bitstring': "0011"}]
        r = reproduce(s, 2, 0.5, 0.1)
        self.assertEqual(len(s), len(r))
        print r

    def test_serach(self):
        pass

if __name__ == '__main__':
    unittest.main()


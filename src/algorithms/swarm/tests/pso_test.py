#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from pso import objective_function, random_vector

class TestPSO(unittest.TestCase):
    def setUp(self):
        self.data = [1,2]

    def test_objective_function(self):
        self.assertEqual(objective_function(self.data), 5)

    def test_random_vector(self):
        minmax = [ [1,2], [2,3] ]

        self.assertEqual(minmax[0][0], 1)

        rv = random_vector(minmax)

        self.assertEqual(len(rv), 2)
        self.assertTrue(rv[0] >= minmax[0][0] and rv[0] <= minmax[0][1])
        self.assertTrue(rv[1] >= minmax[1][0] and rv[1] <= minmax[1][1])

if __name__ == '__main__':
    unittest.main()

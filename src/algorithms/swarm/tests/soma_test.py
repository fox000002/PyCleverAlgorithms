#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from soma import objective_function, random_vector, frange

class TestSOMA(unittest.TestCase):
    def setUp(self):
        pass

    def test_objective_function(self):
    	self.assertEqual(objective_function([0,0]), 3)

    def test_random_vector(self):
        minmax = [ [1,2], [2,3] ]

        self.assertEqual(minmax[0][0], 1)

        rv = random_vector(minmax)

        self.assertEqual(len(rv), 2)
        self.assertTrue(rv[0] >= minmax[0][0] and rv[0] <= minmax[0][1])
        self.assertTrue(rv[1] >= minmax[1][0] and rv[1] <= minmax[1][1])

    def test_frange(self):
    	target = 0
    	for i in frange(0, 1, 0.1):
    		self.assertAlmostEqual(i, target) # float values comparsion
    		target = target + 0.1

if __name__ == '__main__':
    unittest.main()


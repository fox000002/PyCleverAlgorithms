#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from backpropagation import iif, random_vector

class TestBackpropagation(unittest.TestCase):
    def setUp(self):
        pass

    def test_iif(self):
        self.assertEqual(iif(1 < 50, "1", "0"), "1")
        self.assertEqual(iif('0' == '1', 1, 0), 0)

    def test_random_vector(self):
        minmax = [[1, 2], [2, 3]]

        self.assertEqual(minmax[0][0], 1)

        rv = random_vector(minmax)

        self.assertEqual(len(rv), 2)
        self.assertTrue(minmax[0][0] <= rv[0] <= minmax[0][1])
        self.assertTrue(minmax[1][0] <= rv[1] <= minmax[1][1])
 

if __name__ == '__main__':
    unittest.main()


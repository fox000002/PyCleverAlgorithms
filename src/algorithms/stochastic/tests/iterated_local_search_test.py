#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from iterated_local_search import euc_2d, cost

class TestIteratedLocalSearch(unittest.TestCase):
    def setUp(self):
        pass

    def test_euc_2d(self):
    	self.assertEqual(euc_2d([0,0], [0,1]), 1)

    def test_cost(self):
    	cities = [[0,0],[0,1],[0,2]]
    	perm = [0, 1, 2]
    	self.assertEqual(cost(perm, cities), 4)

if __name__ == '__main__':
    unittest.main()


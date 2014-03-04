#!/usr/bin/env python

"""
"""
import unittest
import os

os.sys.path.append("..")

from variable_neighborhood_search import cost

class TestVariableNeighborhoodSearch(unittest.TestCase):
    def setUp(self):
        self.cities = [[1, 1], [4, 5]]
        self.permutation = [0, 1]

    def test_random_vector(self):
        self.assertEqual(10.0, cost(self.permutation, self.cities))


if __name__ == '__main__':
    unittest.main()

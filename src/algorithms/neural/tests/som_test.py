#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from som import euclidean_distance

class TestSOM(unittest.TestCase):
    def setUp(self):
        pass

    def test_euclidean_distance(self):
        self.assertEqual(0, euclidean_distance([1, 1], [1, 1]))
        self.assertEqual(1, euclidean_distance([2, 1], [1, 1]))
        self.assertEqual(5, euclidean_distance([1, 1], [5, 4]))


if __name__ == '__main__':
    unittest.main()


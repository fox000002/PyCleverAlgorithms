#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from ba import objective_function

class TestBA(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2]

    def test_objective_function(self):
        self.assertEqual(objective_function(self.data), 5)
        # integer
        self.assertEqual(99**2, objective_function([99]))
        # float
        self.assertEqual(0.1**2.0, objective_function([0.1]))
        # vector
        self.assertEqual(1**2+2**2+3**2, objective_function([1, 2, 3]))
        # optima
        self.assertEqual(0, objective_function([0, 0]))

if __name__ == '__main__':
    unittest.main()


#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from clonal_selection_algorithm import objective_function

class Testclonal_selection_algorithm(unittest.TestCase):
    def setUp(self):
        self.data = [1,2]

    def test_objective_function(self):
        self.assertEqual(objective_function(self.data), 5)

if __name__ == '__main__':
    unittest.main()


#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from mopso import objective1

class TestMOPSO(unittest.TestCase):
    def setUp(self):
        self.data = [1,2]

    def test_objective1(self):
        self.assertEqual(objective_function(self.data), 5)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from differential_evolution import iif

class TestDifferential_evolution(unittest.TestCase):
    def setUp(self):
        pass

    def test_iif(self):
        self.assertEqual(iif(1<50, "1", "0"), "1")
        self.assertEqual(iif('0'=='1', 1, 0), 0)

if __name__ == '__main__':
    unittest.main()


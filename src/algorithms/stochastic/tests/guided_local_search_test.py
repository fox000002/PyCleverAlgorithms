#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from guided_local_search import euc_2d

class TestGuidedLocalSearch(unittest.TestCase):
    def setUp(self):
        pass

    def test_euc_2d(self):
    	self.assertEqual(euc_2d([0,0], [0,1]), 1)


if __name__ == '__main__':
    unittest.main()
 

#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from stochastic_hill_climbing import iif, onemax, random_bitstring, search

class TestStochasticHillSearch(unittest.TestCase):
    def setUp(self):
        self.bitstring = '1010'

    def test_iif(self):
        self.assertEqual(iif(1<50, "1", "0"), "1")
        self.assertEqual(iif('0'=='1', 1, 0), 0)

    def test_onemax(self):
        self.assertEqual(onemax(self.bitstring), 2)

    def test_search(self):
        #
        num_bits = 15
        #
        max_iter = 100
        #
        best = search(max_iter, num_bits)
        print 'Done. Best Solution: c=%d, v=%s' % (best['cost'], str(best['vector']))
        self.assertEqual(onemax(best['vector']), best['cost'])

if __name__ == '__main__':
    unittest.main()

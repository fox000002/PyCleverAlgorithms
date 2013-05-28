#!/usr/bin/env python

import unittest

import os

os.sys.path.append("..")

from adaptive_random_search import objective_function, random_vector, take_step, search

class TestRandomSearch(unittest.TestCase):
    def setUp(self):
        self.data = [1,2]

    def test_objective_function(self):
        self.assertEqual(objective_function(self.data), 5)

    def test_random_vector(self):
        minmax = [ [1,2], [2,3] ]

        self.assertEqual(minmax[0][0], 1)

        rv = random_vector(minmax)

        self.assertEqual(len(rv), 2)
        self.assertTrue(rv[0] >= minmax[0][0] and rv[0] <= minmax[0][1])
        self.assertTrue(rv[1] >= minmax[1][0] and rv[1] <= minmax[1][1])

    def test_take_step(self):
        minmax = [ [1,2], [2,3] ]
        current = [ 1.5, 2.5 ]
        step_size = 0.1
        position = take_step(minmax, current, step_size)
        self.assertEquals(len(position), 2)
        self.assertTrue(position[0] >= minmax[0][0] and position[0] <= minmax[0][1])
        self.assertTrue(position[1] >= minmax[1][0] and position[1] <= minmax[1][1])

    def test_search(self):
        #
        problem_size = 2
        bounds = [[-5,5]] * problem_size
        #
        max_iter = 1000
        init_factor = 0.05
        s_factor = 1.3
        l_factor = 3.0
        iter_mult = 10
        max_no_impr = 30
        best = search(max_iter, bounds, init_factor, s_factor, l_factor, iter_mult, max_no_impr)
        #
        self.assertIsNotNone(best)
        self.assertTrue(best['cost'] >= -5 and best['cost'] <= 5)


if __name__ == '__main__':
    unittest.main()

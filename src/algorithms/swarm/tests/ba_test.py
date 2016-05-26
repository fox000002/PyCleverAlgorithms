#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from ba import objective_function, random_vector, create_bat

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

    def test_random_vector(self):
        min_max = [[1, 2], [2, 3]]

        self.assertEqual(min_max[0][0], 1)

        rv = random_vector(min_max)

        self.assertEqual(len(rv), 2)
        self.assertTrue(min_max[0][0] <= rv[0] <= min_max[0][1])
        self.assertTrue(min_max[1][0] <= rv[1] <= min_max[1][1])

    def test_create_bat(self):
        rs = create_bat([[-1, 1], [-1, 1]])
        self.assertIsNotNone(rs['position'])
        self.assertIsNotNone(rs['cost'])
        self.assertIsNotNone(rs['velocity'])
        self.assertEqual(2, len(rs['position']))
        self.assertEqual(2, len(rs['velocity']))

    def test_get_global_best(self):
        pass



if __name__ == '__main__':
    unittest.main()

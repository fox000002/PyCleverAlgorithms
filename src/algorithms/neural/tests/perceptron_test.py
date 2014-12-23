#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from perceptron import iif, random_vector, initialize_weights, update_weights, activate, transfer, get_output, \
    train_weights, do_test_weights, execute


class TestPerceptron(unittest.TestCase):
    def setUp(self):
        pass

    def test_iif(self):
        self.assertEqual(iif(1 < 50, "1", "0"), "1")
        self.assertEqual(iif('0' == '1', 1, 0), 0)

    def test_random_vector(self):
        minmax = [[1, 2], [2, 3]]

        self.assertEqual(minmax[0][0], 1)

        rv = random_vector(minmax)

        self.assertEqual(len(rv), 2)
        self.assertTrue(minmax[0][0] <= rv[0] <= minmax[0][1])
        self.assertTrue(minmax[1][0] <= rv[1] <= minmax[1][1])

    def test_initialize_weights(self):
        w = initialize_weights(10)
        self.assertEqual(11, len(w))
        for v in w:
            self.assertTrue(-1 <= v <= 1)

    def test_update_weights(self):
        # no error, no change, one inputs
        w = [0.5, 0.5, 0.5]
        update_weights(2, w, [1, 1], 1.0, 1.0, 0.9)
        for x in w:
            self.assertEqual(0.5, x)
        # no error, no change, zero inputs
        w = [0.5, 0.5, 0.5]
        update_weights(2, w, [1, 1], 0.0, 0.0, 0.9)
        for x in w:
            self.assertEqual(0.5, x)
        # an update
        w = [0.5, 0.5, 0.5]
        update_weights(2, w, [1, 1], 1.0, 0.0, 0.9)
        for x in w:
            self.assertEqual(1.4, x)

    def test_activate(self):
        self.assertEqual(5.0, activate([1.0, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]))
        self.assertEqual(2.5, activate([0.5, 0.5, 0.5, 0.5, 0.5], [1.0, 1.0, 1.0, 1.0]))
        self.assertEqual(-6.062263, activate([-6.072185, 2.454509, -6.062263], [0, 0]))

    def test_transfer(self):
        self.assertEqual(0, transfer(-1))
        self.assertEqual(1, transfer(0))
        self.assertEqual(1, transfer(1))

    def test_get_output(self):
        self.assertEqual(1, get_output([1, 1, 1], [1, 1]))
        self.assertEqual(0, get_output([-1, -1, -1], [1, 1]))

    def test_train_weights(self):
        domain = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        w = [-1, -1, -1]
        train_weights(w, domain, 2, 10, 0.5)
        for x in w:
            self.assertNotEqual(-1, x)

    def test_test_weights(self):
        rs = None
        domain = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        w = [0.5, 0.5, -0.5]
        rs = do_test_weights(w, domain, 2)
        self.assertEqual(4, rs)

    def test_search(self):
        domain = [[0,0,0], [0,1,1], [1,0,1], [1,1,1]]
        weights = None
        weights = execute(domain, 2, 20, 0.1)
        self.assertEqual(3, len(weights))
        rs = None
        rs = do_test_weights(weights, domain, 2)
        self.assertEqual(4, rs)

if __name__ == '__main__':
    unittest.main()


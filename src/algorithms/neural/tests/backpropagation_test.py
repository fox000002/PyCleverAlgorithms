#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from backpropagation import iif, random_vector, initialize_weights, activate, transfer, transfer_derivative, \
    forward_propagate, backward_propagate_error, calculate_error_derivatives_for_weights, update_weights, \
    train_network, do_test_network, create_neuron, execute


class TestBackpropagation(unittest.TestCase):
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
        weights = initialize_weights(100)
        # adds a bias
        self.assertEqual(100, len(weights))
        # check values in [-2,2]
        for w in weights:
            self.assertTrue(-2 <= w <= 2)

    def test_activate(self):
        self.assertEqual(5.0, activate([1.0, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]))
        self.assertEqual(2.5, activate([0.5, 0.5, 0.5, 0.5, 0.5], [1.0, 1.0, 1.0, 1.0]))
        self.assertEqual(-6.062263, activate([-6.072185, 2.454509, -6.062263], [0, 0]))

    def test_transfer(self):
        # small values stay smallish
        self.assertAlmostEqual(0.73, transfer(1.0), delta=0.01)
        self.assertAlmostEqual(0.5, transfer(0.0), delta=0.001)
        # large/small values get squashed
        self.assertAlmostEqual(1.0, transfer(10.0), delta=0.0001)
        self.assertAlmostEqual(0.0, transfer(-10.0), delta=0.0001)
        self.assertAlmostEqual(0.00232, transfer(-6.062263), delta=0.00001)

    def test_transfer_derivative(self):
        self.assertEqual(0.0, transfer_derivative(1.0))
        self.assertEqual(0.0, transfer_derivative(0.0))
        self.assertEqual(0.25, transfer_derivative(0.5))

    def test_forward_propagate_xor(self):
        n1 = {"weights": [0.129952, -0.923123, 0.341232]}
        n2 = {"weights": [0.570345, -0.328932, -0.115223]}
        n3 = {"weights": [0.164732, 0.752621, -0.993423]}
        network = [[n1, n2], [n3]]
        output = forward_propagate(network, [0, 0])
        # n1
        self.assertAlmostEqual(0.341232, n1["activation"], delta=0.000001)
        self.assertAlmostEqual(0.584490, n1["output"], delta=0.000001)
        # n2
        self.assertAlmostEqual(-0.115223, n2["activation"], delta=0.000001)
        self.assertAlmostEqual(0.471226, n2["output"], delta=0.000001)
        # n3
        self.assertAlmostEqual(-0.542484, n3["activation"], delta=0.000001)
        self.assertAlmostEqual(0.367610, n3["output"], delta=0.000001)
        # output
        self.assertEqual(output, n3["output"])
        self.assertAlmostEqual(0.367610, output, delta=0.000001)

    def test_backward_propagate_error(self):
        n1 = {"weights": [0.2, 0.2, 0.2], "output": transfer(0.02 + 0.02 + 0.2)}
        n2 = {"weights": [0.3, 0.3, 0.3], "output": transfer(0.03 + 0.03 + 0.3)}
        n3 = {"weights": [0.4, 0.4, 0.4], "output": transfer((0.4 * n1["output"]) + (0.4 * n2["output"]) + 0.4)}
        expected = 1.0
        network = [[n1, n2], [n3]]
        backward_propagate_error(network, expected)
        # output node
        e1 = (expected - n3["output"]) * transfer_derivative(n3["output"])
        self.assertEqual(e1, n3["delta"])
        # input nodes
        e2 = (0.4 * e1) * transfer_derivative(n1["output"])
        self.assertEqual(e2, n1["delta"])
        e3 = (0.4 * e1) * transfer_derivative(n2["output"])
        self.assertEqual(e3, n2["delta"])

    def test_backward_propagate_error_xor(self):
        n1 = {"weights": [0.129952, -0.923123, 0.341232], "output": 0.584490}
        n2 = {"weights": [0.570345, -0.328932, -0.115223], "output": 0.471226}
        n3 = {"weights": [0.164732, 0.752621, -0.993423], "output": 0.367610}
        expected = 0.0
        network = [[n1, n2], [n3]]
        backward_propagate_error(network, expected)
        # output node
        self.assertAlmostEqual(-0.085459, n3["delta"], delta=0.000001)
        # input nodes
        self.assertAlmostEqual(-0.0034190, n1["delta"], delta=0.000001)
        self.assertAlmostEqual(-0.0160263, n2["delta"], delta=0.000001)

    def test_calculate_error_derivatives_for_weights(self):
        n1 = {"weights": [0.2, 0.2, 0.2], "delta": 0.5, "output": transfer(0.02 + 0.02 + 0.2), "deriv": [0, 0, 0]}
        n2 = {"weights": [0.3, 0.3, 0.3], "delta": -0.6, "output": transfer(0.03 + 0.03 + 0.3), "deriv": [0, 0, 0]}
        n3 = {"weights": [0.4, 0.4, 0.4], "delta": 0.7,
              "output": transfer((0.4 * n1["output"]) + (0.4 * n2["output"]) + 0.4), "deriv": [0, 0, 0]}
        network = [[n1, n2], [n3]]
        vector = [0.1, 0.1]
        calculate_error_derivatives_for_weights(network, vector)
        # n1 error
        self.assertEqual(len(n1["weights"]), len(n1["deriv"]))
        self.assertEqual(vector[0] * n1["delta"], n1["deriv"][0])
        self.assertEqual(vector[1] * n1["delta"], n1["deriv"][1])
        self.assertEqual(1 * n1["delta"], n1["deriv"][2])
        # n2 error
        self.assertEqual(len(n2["weights"]), len(n2["deriv"]))
        self.assertEqual(vector[0] * n2["delta"], n2["deriv"][0])
        self.assertEqual(vector[1] * n2["delta"], n2["deriv"][1])
        self.assertEqual(1 * n2["delta"], n2["deriv"][2])
        # n3 error
        self.assertEqual(len(n3["weights"]), len(n3["deriv"]))
        self.assertEqual(n1["output"] * n3["delta"], n3["deriv"][0])
        self.assertEqual(n2["output"] * n3["delta"], n3["deriv"][1])
        self.assertEqual(1 * n3["delta"], n3["deriv"][2])

    def test_calculate_error_derivatives_for_weights_xor(self):
        n1 = {"weights": [0.129952, -0.923123, 0.341232], "output": 0.584490, "delta": -0.0034190, "deriv": [0, 0, 0]}
        n2 = {"weights": [0.570345, -0.328932, -0.115223], "output": 0.471226, "delta": -0.0160263, "deriv": [0, 0, 0]}
        n3 = {"weights": [0.164732, 0.752621, -0.993423], "output": 0.367610, "delta": -0.085459, "deriv": [0, 0, 0]}
        network = [[n1, n2], [n3]]
        calculate_error_derivatives_for_weights(network, [0, 0])
        # n1
        self.assertAlmostEqual(0.0, n1["deriv"][0] * 0.5, delta=0.000001)
        self.assertAlmostEqual(0.0, n1["deriv"][1] * 0.5, delta=0.000001)
        self.assertAlmostEqual(-0.0017095, n1["deriv"][2] * 0.5, delta=0.000001)
        # n2
        self.assertAlmostEqual(0.0, n2["deriv"][0] * 0.5, delta=0.000001)
        self.assertAlmostEqual(0.0, n2["deriv"][1] * 0.5, delta=0.000001)
        self.assertAlmostEqual(-0.0080132, n2["deriv"][2] * 0.5, delta=0.000001)
        # n3
        self.assertAlmostEqual(-0.024975, n3["deriv"][0] * 0.5, delta=0.000001)
        self.assertAlmostEqual(-0.020135, n3["deriv"][1] * 0.5, delta=0.000001)
        self.assertAlmostEqual(-0.042730, n3["deriv"][2] * 0.5, delta=0.000001)

    def test_update_weights(self):
        n1 = {"weights": [0.2, 0.2, 0.2], "deriv": [0.1, -0.5, 100.0], "last_delta": [0, 0, 0]}
        network = [[n1]]
        update_weights(network, 1.0, 0.0)
        self.assertEqual((0.2 + (0.1 * 1.0)), n1["weights"][0])
        self.assertEqual((0.2 + (-0.5 * 1.0)), n1["weights"][1])
        self.assertEqual((0.2 + (100 * 1.0)), n1["weights"][2])

    def test_train_network(self):
        n1 = {"weights": [-1, -1, 1], "last_delta": [0, 0, 0], "deriv": [0, 0, 0]}
        n2 = {"weights": [-1, -1, 1], "last_delta": [0, 0, 0], "deriv": [0, 0, 0]}
        n3 = {"weights": [-1, -1, 1], "last_delta": [0, 0, 0], "deriv": [0, 0, 0]}
        network = [[n1, n2], [n3]]
        domain = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        train_network(network, domain, 2, 100, 0.5)
        # test the network weights were changed
        self.assertNotEqual([-1, -1, 1], n1["weights"])
        self.assertNotEqual([-1, -1, 1], n2["weights"])
        self.assertNotEqual([-1, -1, 1], n3["weights"])

    def test_test_network(self):
        # note the order difference
        n1 = {"weights": [-6.062263, -6.072185, 2.454509]}
        n2 = {"weights": [-4.893081, -4.894898, 7.293063]}
        n3 = {"weights": [-9.792470, 9.484580, -4.473972]}
        network = [[n1, n2], [n3]]
        domain = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        # specifics
        self.assertAlmostEqual(0.017622, forward_propagate(network, domain[0]), delta=0.001)
        self.assertAlmostEqual(0.981504, forward_propagate(network, domain[1]), delta=0.06)
        self.assertAlmostEqual(0.981491, forward_propagate(network, domain[2]), delta=0.06)
        self.assertAlmostEqual(0.022782, forward_propagate(network, domain[3]), delta=0.001)
        # all
        output = do_test_network(network, domain, 2)
        self.assertEqual(4, output)

    def test_create_neuron(self):
        self.assertEqual(2, len(create_neuron(1)["weights"]))
        self.assertEqual(3, len(create_neuron(2)["weights"]))
        self.assertEqual(11, len(create_neuron(10)["weights"]))

    def test_compute(self):
        domain = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        network = execute(domain, 2, 2000, 4, 0.1)
        # structure
        self.assertEqual(2, len(network))
        self.assertEqual(4, len(network[0]))
        self.assertEqual(1, len(network[1]))
        # output
        output = do_test_network(network, domain, 2)
        self.assertEqual(4, output)


if __name__ == '__main__':
    unittest.main()


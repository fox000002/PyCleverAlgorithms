#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from som import euclidean_distance, initialize_vectors, get_best_matching_unit, get_vectors_in_neighborhood, \
    update_codebook_vector, train_network, summarize_vectors, do_test_network, execute


class TestSOM(unittest.TestCase):
    def setUp(self):
        pass

    def test_euclidean_distance(self):
        self.assertEqual(0, euclidean_distance([1, 1], [1, 1]))
        self.assertEqual(1, euclidean_distance([2, 1], [1, 1]))
        self.assertEqual(5, euclidean_distance([1, 1], [5, 4]))

    def test_initialize_vectors(self):
        domain = [[0.0, 1.0], [0.0, 1.0]]
        vectors = initialize_vectors(domain, 10, 20)
        self.assertEqual(10 * 20, len(vectors))
        for p in vectors:
            self.assertIsNotNone(p["vector"])
            self.assertIsNotNone(p["coord"])
            # vector
            for i, x in enumerate(p["vector"]):
                self.assertTrue(0 <= x <= 1)

            # coord
            self.assertEqual(2, len(p["coord"]))
            self.assertTrue(0 <= p["coord"][0] <= 10)
            self.assertTrue(0 <= p["coord"][1] <= 20)

    def test_get_best_matching_unit(self):
        vectors = [{"vector": [1, 1]}, {"vector": [0.5, 0.5]}, {"vector": [0, 0]}]
        rs = get_best_matching_unit(vectors, [0.5, 0.5])
        self.assertEqual(2, len(rs))
        self.assertEqual(vectors[1], rs[0])
        self.assertEqual(0, rs[1])

    def test_get_vectors_in_neighborhood(self):
        # none
        vectors = [{"coord": [1, 1]}, {"coord": [0.5, 0.5]}, {"coord": [0, 0]}]
        rs = get_vectors_in_neighborhood({"coord": [10, 10]}, vectors, 1)
        self.assertEqual(0, len(rs))
        # all
        vectors = [{"coord": [1, 1]}, {"coord": [0.5, 0.5]}, {"coord": [0, 0]}]
        rs = get_vectors_in_neighborhood({"coord": [0.5, 0.5]}, vectors, 0.1)
        self.assertEqual(1, len(rs))
        # some
        vectors = [{"coord": [1, 1]}, {"coord": [0.5, 0.5]}, {"coord": [0, 0]}]
        rs = get_vectors_in_neighborhood({"coord": [0.5, 0.5]}, vectors, 1)
        self.assertEqual(3, len(rs))

    def test_update_codebook_vector(self):
        # no error
        c = {"vector": [0.5, 0.5]}
        update_codebook_vector(c, [0.5, 0.5], 0.5)
        for x in c["vector"]:
            self.assertEqual(0.5, x)
        # lots of error
        c = {"vector": [1, 1]}
        update_codebook_vector(c, [0.5, 0.5], 0.5)
        for x in c["vector"]:
            self.assertEqual(0.75, x)

    def test_train_network(self):
        vectors = [{"vector": [0, 0], "coord": [0, 0]}, {"vector": [1, 1], "coord": [1, 1]}]
        train_network(vectors, [[0.25, 0.75], [0.25, 0.75]], 50, 0.5, 3)

        # weights are changed!
        self.assertNotEqual([0, 0], vectors[0]["vector"])
        self.assertNotEqual([1, 1], vectors[1]["vector"])

    def test_summarize_vectors(self):
        # same
        rs = summarize_vectors([{"vector": [0.5, 0.5]}, {"vector": [0.5, 0.5]}])
        self.assertIsNotNone(rs)
        for de in rs:
            self.assertEqual(0.5, de[0])
            self.assertEqual(0.5, de[1])
        # some distribution
        rs = summarize_vectors([{"vector": [1, 1]}, {"vector": [0, 0]}])
        self.assertIsNotNone(rs)
        for de in rs:
            self.assertEqual(0, de[0])
            self.assertEqual(1, de[1])

    def test_test_network(self):
        # no error
        error = do_test_network([{"vector": [0.5, 0.5]}, {"vector": [0.5, 0.5]}], [[0.25, 0.75], [0.25, 0.75]], 100)
        self.assertIsNotNone(error)
        self.assertAlmostEqual(0, error, delta=0.2)
        # all error
        error = do_test_network([{"vector": [1, 1]}, {"vector": [0, 0]}], [[0.5, 0.5], [0.5, 0.5]], 100)
        self.assertIsNotNone(error)
        self.assertAlmostEqual(0.5, error, delta=0.3)

    def test_search(self):
        # problem
        domain = [[0.0, 1.0], [0.0, 1.0]]
        shape = [[0.3, 0.6], [0.3, 0.6]]
        # compute
        codebooks = execute(domain, shape, 1000, 0.3, 5, 5, 4)

        # verify structure
        self.assertEqual(20, len(codebooks))
        # test result
        rs = do_test_network(codebooks, shape)

        self.assertAlmostEqual(0.0, rs, delta=0.1)

if __name__ == '__main__':
    unittest.main()


#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from clonal_selection_algorithm import objective_function, decode, evaluate, \
    random_bitstring, point_mutation, calculate_mutation_rate, calc_num_clones, \
    calculate_affinity, clone_and_hypermutate, random_insertion


class Testclonal_selection_algorithm(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2]

    def test_objective_function(self):
        self.assertEqual(objective_function(self.data), 5)
        # integer
        self.assertEqual(99**2, objective_function([99]))
        # float
        self.assertEqual(0.1**2.0, objective_function([0.1]))
        # vector
        self.assertEqual(1**2+2**2+3**2, objective_function([1,2,3]))
        # optima
        self.assertEqual(0, objective_function([0,0]))

    def test_decode(self):
        # zero
        v = decode("0000000000000000", [[0,1]], 16)
        self.assertEqual(1, len(v))
        self.assertEqual(0.0, v[0])
        # one
        v = decode("1111111111111111", [[0,1]], 16)
        self.assertEqual(1, len(v))
        self.assertEqual(1.0, v[0])
        # float #1
        v = decode("0000000000000001", [[0,1]], 16)
        self.assertEqual(1, len(v))
        a = 1.0 / ((2**16)-1)
        self.assertEqual(a*(2**0), v[0])
        # float #2
        v = decode("0000000000000010", [[0,1]], 16)
        self.assertEqual(1, len(v))
        self.assertEqual(a*(2**1), v[0])
        # float #3
        v = decode("0000000000000100", [[0,1]], 16)
        self.assertEqual(1, len(v))
        self.assertEqual(a*(2**2), v[0])
        # multiple floats
        v = decode("00000000000000001111111111111111", [[0,1],[0,1]], 16)
        self.assertEqual(2, len(v))
        self.assertEqual(0.0, v[0])
        self.assertEqual(1.0, v[1])

    def test_evaluate(self):
        pop = [{'bitstring': "00000000000000000000000000000000"}, {'bitstring': "11111111111111111111111111111111"}]
        evaluate(pop, [[-1, 1], [-1, 1]], 16)
        for p in pop:
            self.assertIsNotNone(p['vector'])
            self.assertEqual(2, len(p['vector']))
            self.assertIsNotNone(p['cost'])

    def test_random_bitstring(self):
        self.assertEqual(10, len(random_bitstring(10)))
        self.assertEqual(0, len(''.join(random_bitstring(10)).replace('0', '').replace('1', '')))

    def test_random_bitstring_ratio(self):
        s = ''.join(random_bitstring(1000))
        self.assertAlmostEqual(0.5, (len(s.replace('1', ''))/1000.0), delta=0.05)
        self.assertAlmostEqual(0.5, (len(s.replace('0', ''))/1000.0), delta=0.05)

    def test_point_mutation(self):
        self.assertEqual("0000000000", point_mutation("0000000000", 0))
        self.assertEqual("1111111111", point_mutation("1111111111", 0))
        self.assertEqual("1111111111", point_mutation("0000000000", 1))
        self.assertEqual("0000000000", point_mutation("1111111111", 1))

    def test_point_mutation_ratio(self):
        changes = 0
        for i in xrange(100):
            s = point_mutation("0000000000", 0.5)
            changes += (10 - len(s.replace('1', '')))
        self.assertAlmostEqual(0.5, float(changes)/(100*10), delta=0.05)

    def test_calculate_mutation_rate(self):
        # best - lowest rate
        self.assertAlmostEqual(0.0, calculate_mutation_rate({'affinity': 1.0}), delta=0.1)
        # middle
        self.assertAlmostEqual(0.3, calculate_mutation_rate({'affinity': 0.5}), delta=0.1)
        # worst - highest rate
        self.assertEqual(1.0, calculate_mutation_rate({'affinity': 0.0}))

    def test_num_clones(self):
        self.assertEqual(100, calc_num_clones(100, 1))
        self.assertEqual(10, calc_num_clones(100, 0.1))
        self.assertEqual(200, calc_num_clones(100, 2))
        # rounded
        self.assertEqual(12, calc_num_clones(100, 0.123))

    def test_calculate_affinity(self):
        # all ones - no range in cost
        pop = [{'cost': 1}, {'cost': 1}, {'cost': 1}, {'cost': 1}, {'cost': 1}]
        calculate_affinity(pop)
        for p in pop:
            self.assertIsNotNone(p['affinity'])
            self.assertEqual(1.0, p['affinity'])

        pop = [{'cost': 10000}, {'cost': 1000}, {'cost': 100}, {'cost': 10}, {'cost': 1}]
        # normal
        calculate_affinity(pop)
        for p in pop:
            self.assertIsNotNone(p['affinity'])
            self.assertGreaterEqual(p['affinity'], 0.0)
            self.assertLessEqual(p['affinity'], 1.0)

    def test_clone_and_hypermutate(self):
        pop = [{'bitstring': "000000", 'cost': 0}, {'bitstring': "111111", 'cost': 1}]
        clones = clone_and_hypermutate(pop, 10)
        self.assertEqual(40, len(clones))
        self.assertEqual(1.0, pop[0]['affinity'])
        self.assertEqual(0.0, pop[1]['affinity'])
        for i, c in enumerate(clones):
            if i < 20:
                # very low mutation, best affinity
                self.assertNotEqual(id(c), id(pop[0]))
            else:
                # lots of change, worst affinity
                self.assertNotEqual(id(c), id(pop[1]))
                self.assertNotEqual(pop[1]['bitstring'], c['bitstring'])
        # ensure pop was unchanged
        self.assertEqual(pop[0]['bitstring'], "000000")
        self.assertEqual(pop[1]['bitstring'], "111111")

    def test_random_insertion(self):
        pop = [{'bitstring': "000000", 'vector': [0], 'cost': 0}, {'bitstring': "111111", 'vector': [666], 'cost': 1}]
        # less than pop
        p = random_insertion([[-1, 1]], pop, 1, 6)
        self.assertEqual(len(pop), len(p))
        for x in p:
            self.assertIsNotNone(x['vector'])
            self.assertEqual(1, len(x['vector']))
            self.assertEqual(6, len(x['bitstring']))
            self.assertIsNotNone(x['cost'])

        # mdore than pop
        p = random_insertion([[-1, 1]], pop, 10000, 6)
        self.assertEqual(len(pop), len(p))
        for x in p:
            self.assertIsNotNone(x['vector'])
            self.assertEqual(1, len(x['vector']))
            self.assertEqual(6, len(x['bitstring']))
            self.assertIsNotNone(x['cost'])

    def test_search(self):
        best = None
        #silence_stream(STDOUT) do
        #    best = search([[-5,5],[-5,5]], 100, 50, 0.1, 1)
        #assert_not_nil(best[:cost])
        #assert_in_delta(0.0, best[:cost], 0.001)

if __name__ == '__main__':
    unittest.main()


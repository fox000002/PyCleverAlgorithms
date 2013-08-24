#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from onemax import OneMax, GeneticAlgorithm

def iif(condition, true_part, false_part):  
    return (condition and [true_part] or [false_part])[0]  

class TestOneMax(unittest.TestCase):
    def setUp(self):
        self.o = OneMax(4)
        self.g = GeneticAlgorithm()

    def test_onemax(self):
        self.assertEqual(self.o.assess({'bitstring' : "0000"}), 0)
        self.assertEqual(self.o.assess({'bitstring' : "0001"}), 1)
        self.assertEqual(self.o.assess({'bitstring' : "0101"}), 2)
        self.assertEqual(self.o.assess({'bitstring' : "1111"}), 4)

    def test_is_optimal(self):
        self.assertEqual(True, self.o.is_optimal({'fitness' : 4}))
        self.assertEqual(False, self.o.is_optimal({'fitness' : 3}))
        self.assertEqual(False, self.o.is_optimal({'fitness' : 2}))
        self.assertEqual(False, self.o.is_optimal({'fitness' : 1}))
        self.assertEqual(False, self.o.is_optimal({'fitness' : 0}))
        self.assertEqual(False, self.o.is_optimal({'fitness' : 5}))

    def test_random_bitstring(self):
        import string
        self.assertEqual(10, len(self.g.random_bitstring(10)))
        self.assertEqual(0, sum(map(lambda x : iif(x=='1' or x=='0', 0, 1), self.g.random_bitstring(10))))

    def test_random_bitstring_ratio(self):
        pass

    def test_binary_tournament(self):
        pass

    def test_point_mutation(self):
        pass

    def test_point_mutation_ratio(self):
        pass

    def test_uniform_crossover(self):
        pass

    def test_reproduce(self):
        pass

    def test_search(self):
        pass  

if __name__ == '__main__':
    unittest.main()

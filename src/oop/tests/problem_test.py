#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from problem import Problem
from undefined_exception import UndefinedError


class TestProblem(unittest.TestCase):
    def setUp(self):
        self.problem = Problem()
        self.candidate_solution = None

    def test_assess(self):
        try:
            self.problem.assess(self.candidate_solution)
        except UndefinedError:
            pass
        else:
            self.fail('Did not see UndefinedError')

    def test_is_optimal(self):
        try:
            self.problem.is_optimal(self.candidate_solution)
        except UndefinedError:
            pass
        else:
            self.fail('Did not see UndefinedError')

if __name__ == '__main__':
    unittest.main()


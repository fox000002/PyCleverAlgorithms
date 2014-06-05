#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from problem import Problem
from strategy import Strategy
from undefined_exception import UndefinedError


class TestStrategy(unittest.TestCase):
    def setUp(self):
        self.problem = Problem()
        self.strategy = Strategy()

    def test_execute(self):
        try:
            self.strategy.execute(self.problem)
        except UndefinedError:
            pass
        else:
            self.fail('Did not see UndefinedError')

if __name__ == '__main__':
    unittest.main()

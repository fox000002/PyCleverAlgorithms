#!/usr/bin/env python

"""
Firefly Algorithm

Inspired by the flashing pattern of tropical fireflies.
"""

from random import random


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x**2, v))


def random_vector(min_max):
    return list(map(lambda x: x[0] + (x[1]-x[0]) * random(), min_max))


def search():
    pass


def main():
    # problem configuration
    problem_size = 2
    search_space = [[-5, 5]] * problem_size
    # algorithm configuration
    max_iter = 100
    #
    # best = search(search_space, max_iter)
    # print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['vector']))


if __name__ == "__main__":
    main()
#!/usr/bin/env python

"""
Bayesian Optimization Algorithm (BOA)
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def one_max(bitstring):
    return sum(map(lambda x: iif(x == '1', 1, 0), bitstring))


def random_bitstring(num_bits):
    from random import random
    return map(lambda x: iif(random() < 0.5, '1', '0'), xrange(num_bits))


def search(num_bits, max_iter, pop_size, select_size, num_children):
    pass


def main():
    # problem configuration
    num_bits = 20
    # algorithm configuration
    max_iter = 100
    pop_size = 50
    select_size = 15
    num_children = 25
    # execute the algorithm
    best = search(num_bits, max_iter, pop_size, select_size, num_children)
    print "done! Solution: f=%f/%d, s=%s" % (best['cost'], num_bits, best['bitstring'])

if __name__ == "__main__":
    main()


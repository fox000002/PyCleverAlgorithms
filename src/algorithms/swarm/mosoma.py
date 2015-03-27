#!/usr/bin/env python

"""
Multi-Objective Self-Organizing Migrating Algorithm (MOSOMA)
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective1(v):
    return sum(map(lambda x: x ** 2, v))


def objective2(v):
    return sum(map(lambda x: (x - 2.0) ** 2, v))


def main():
    # problem configuration
    problem_size = 1
    search_space = [[-10, 10]] * problem_size
    # algorithm configuration
    max_gens = 50
    pop_size = 80
    p_cross = 0.90
    # execute the algorithm
    #pop = search(search_space, max_gens, pop_size, archive_size, p_cross)
    print "Done!"


if __name__ == "__main__":
    main()

#!/usr/bin/env python

"""
Negative Selection Algorithm
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def random_vector(min_max):
    import random
    return map(lambda x: x[0] + (x[1] - x[0]) * random.random(), min_max)





def main():
    pass

if __name__ == "__main__":
    main()


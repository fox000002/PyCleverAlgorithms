#!/usr/bin/env python

"""
Evolution Strategies
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x**2, v))






def main():
    pass

if __name__ == "__main__":
    main()


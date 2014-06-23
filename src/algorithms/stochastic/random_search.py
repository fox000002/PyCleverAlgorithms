#!/usr/bin/env python

"""
Random Search
"""


def objective_function(v):
    return sum(map(lambda x: x ** 2, v))


def random_vector(min_max):
    import random
    return map(lambda x: x[0] + (x[1] - x[0]) * random.random(), min_max)


def search(search_space, max_iteration):
    best = None
    for iteration in range(0, max_iteration):
        candidate = {'vector': random_vector(search_space)}
        candidate['cost'] = objective_function(candidate['vector'])
        if best is None or candidate['cost'] < best['cost']:
            best = candidate
        print ' > iteration=%d, best=%f' % (iteration + 1, best['cost'])
    return best


def main():
    #
    problem_size = 2
    search_space = [[-5, 5]] * problem_size
    #
    max_iteration = 100
    #
    best = search(search_space, max_iteration)
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['vector']))


if __name__ == "__main__":
    main()

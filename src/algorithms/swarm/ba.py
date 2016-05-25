#!/usr/bin/env python

"""
Bat Algorithm
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x**2, v))


def random_vector(min_max):
    from random import random
    return map(lambda x: x[0] + (x[1]-x[0]) * random(), min_max)


def create_bat(search_space):
    bat = {'position': random_vector(search_space)}
    bat['cost'] = objective_function(bat['position'])
    bat['velocity'] = [0 for _ in search_space]
    return bat


def get_global_best(population):
    best = population[0]
    for i in xrange(1, len(population)-1):
        if population[i]['cost'] < best['cost']:
            best = population[i]
    return {'position': best['position'][:], 'cost': best['cost']}


def update_velocity(bat, global_best, Qmax, Qmin):
    from random import random
    Q = Qmin + (Qmax-Qmin)*random()
    for i in xrange(len(bat['velocity'])):
        bat['velocity'][i] += Q * (bat['position'][i] - global_best['position'][i])


def update_position(bat, bounds, global_best, r, A):
    from random import random
    p = bat['position'][:]
    for i in xrange(len(p)):
        p[i] += bat['velocity'][i]
        if p[i] > bounds[i][1]:
            p[i] = bounds[i][1]
        elif p[i] < bounds[i][0]:
            p[i] = bounds[i][0]

    if random() > r:
        p = global_best['position'][:]
        for i in xrange(len(p)):
            p[i] += 0.001 * random()

    fnew = objective_function(p)

    if (fnew <= bat['cost']) and (random() < A):
        bat['position'] = p
        bat['cost'] = fnew


def search(search_space, max_gen, pop_size, A, r, Qmin, Qmax):
    pop = [create_bat(search_space) for _ in xrange(pop_size)]
    global_best = get_global_best(pop)
    for gen in xrange(max_gen):
        for bat in pop:
            update_velocity(bat, global_best, Qmax, Qmin)
            update_position(bat, search_space, global_best, r, A)
            if bat['cost'] < global_best['cost']:
                global_best['position'] = bat['position'][:]
                global_best['cost'] = bat['cost']
        print " > gen %d, fitness=%f" % (gen + 1, global_best['cost'])
    return global_best


def main():
    # problem configuration
    problem_size = 2
    search_space = [[-5, 5]] * problem_size
    # algorithm configuration
    max_gen = 100
    pop_size = 40
    A = 0.5
    r = 0.5
    Qmax = 2
    Qmin = 0
    #
    best = search(search_space, max_gen, pop_size, A, r, Qmin, Qmax)
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['position']))


if __name__ == "__main__":
    main()
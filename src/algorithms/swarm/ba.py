#!/usr/bin/env python

"""
Bat Algorithm
"""

from random import random, normalvariate
import math

def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x**2, v))


def random_vector(min_max):
    return list(map(lambda x: x[0] + (x[1]-x[0]) * random(), min_max))


def create_bat(search_space):
    bat = {'position': random_vector(search_space)}
    bat['cost'] = objective_function(bat['position'])
    bat['velocity'] = [0 for _ in search_space]
    return bat


def get_global_best(population):
    best = population[0]
    for i in range(1, len(population)-1):
        if population[i]['cost'] < best['cost']:
            best = population[i]
    return {'position': best['position'][:], 'cost': best['cost']}


def update_velocity(bat, global_best, Q):
    """
    Update the bats velocity
    """
    for i in range(len(bat['velocity'])):
        bat['velocity'][i] += Q[i] * (bat['position'][i] - global_best['position'][i])


def update_position(bat, bounds, global_best, r, A):
    p = bat['position'][:]
    for i in range(len(p)):
        p[i] += bat['velocity'][i]
        if p[i] > bounds[i][1]:
            p[i] = bounds[i][1]
        elif p[i] < bounds[i][0]:
            p[i] = bounds[i][0]

    if random() > r:
        p = global_best['position'][:]
        for i in range(len(p)):
            p[i] += 0.001 * normalvariate(0, 1)

    fnew = objective_function(p)

    if (fnew <= bat['cost']) and (random() < A):
        bat['position'] = p
        bat['cost'] = fnew


def update_frequency(Q, Qmax, Qmin):
    """
        Update the pulse frequency
    """
    for i in range(len(Q)):
        Q[i] = Qmin + (Qmax-Qmin)*random()


def update_loudness(old_loudness):
    alpha = 0.5
    return alpha * old_loudness

def update_pulse_rate(old_pulse_rate, iteration):
    gamma = 0.3
    return (1 - math.exp(-gamma * iteration)) * old_pulse_rate

def search(search_space, max_gen, pop_size, A, r, Qmin, Qmax):
    pop = [create_bat(search_space) for _ in range(pop_size)]
    global_best = get_global_best(pop)
    Q = [0.0 for _ in range(len(search_space))]
    for gen in range(max_gen):
        for bat in pop:
            update_frequency(Q, Qmax, Qmin)
            update_velocity(bat, global_best, Q)
            update_position(bat, search_space, global_best, r, A)
            print(bat['cost'])
            if bat['cost'] < global_best['cost']:
                global_best['position'] = bat['position'][:]
                global_best['cost'] = bat['cost']
        print(" > gen %d, fitness=%f" % (gen + 1, global_best['cost']))
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
    print('Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['position'])))


if __name__ == "__main__":
    main()
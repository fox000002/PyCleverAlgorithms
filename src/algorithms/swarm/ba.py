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
    bat['frequency'] = 0
    return bat


def get_global_best(population):
    best = population[0]
    for i in range(1, len(population)-1):
        if population[i]['cost'] < best['cost']:
            best = population[i]
    return {'position': best['position'][:], 'cost': best['cost']}


def update_velocity(bat, global_best):
    """
    Update the bats velocity
    """
    for i in range(len(bat['velocity'])):
        bat['velocity'][i] += bat['frequency'] * (bat['position'][i] - global_best['position'][i])


def update_position(bat, bounds, global_best, r):
    p = bat['position'][:]
    for i in range(len(p)):
        p[i] += bat['velocity'][i]
        if p[i] > bounds[i][1]:
            p[i] = bounds[i][1]
        elif p[i] < bounds[i][0]:
            p[i] = bounds[i][0]

    # generate a local solution around the best solution
    if random() > r:
        p = global_best['position'][:]
        for i in range(len(p)):
            v = normalvariate(0, 1)
            p[i] += 0.001 * v

    return p


def update_frequency(bat, Qmax, Qmin):
    """
        Update the pulse frequency
    """
    bat['frequency'] = Qmin + (Qmax-Qmin)*random()


def update_loudness(old_loudness):
    """
        Update the loudness
    """
    alpha = 0.5
    return alpha * old_loudness


def update_pulse_rate(old_pulse_rate, iteration):
    """
        Update the pulse rate
    """
    gamma = 0.3
    return (1 - math.exp(-gamma * iteration)) * old_pulse_rate


def search(search_space, max_gen, pop_size, A, r, Qmin, Qmax, fixed_ler):
    """
        
    """
    pop = [create_bat(search_space) for _ in range(pop_size)]
    global_best = get_global_best(pop)
    for gen in range(max_gen):
        for bat in pop:
            update_frequency(bat, Qmax, Qmin)
            update_velocity(bat, global_best)
            p = update_position(bat, search_space, global_best, r)
            # 
            fnew = objective_function(p)

            # 
            if (fnew <= bat['cost']) and (random() < A):
                bat['position'] = p
                bat['cost'] = fnew
                if not fixed_ler:
                    A = update_loudness(A)
                    r = update_pulse_rate(r, gen+1)
            
            # Update the current best solution
            if bat['cost'] < global_best['cost']:
                global_best['position'] = bat['position'][:]
                global_best['cost'] = bat['cost']
        print(" > gen %d, fitness=%f" % (gen + 1, global_best['cost']))
    return global_best


def main():
    # problem configuration
    problem_size = 2
    search_space = [[-2, 2]] * problem_size
    # algorithm configuration
    max_gen = 100
    pop_size = 40
    A = 0.5
    r = 0.5
    Qmax = 2
    Qmin = 0
    fixed_ler = True
    #
    best = search(search_space, max_gen, pop_size, A, r, Qmin, Qmax, fixed_ler)
    print('Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['position'])))


if __name__ == "__main__":
    main()
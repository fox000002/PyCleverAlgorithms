#!/usr/bin/env python

"""
Evolution Programming
"""

import random


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x**2, v))


def random_vector(minmax):
    return map(lambda x: x[0] + (x[1]-x[0]) * random.random(), minmax[:])


def random_gaussian(mean=0.0, stdev=1.0):
    import math
    u1 = u2 = w = 0
    while True:
        u1 = 2 * random.random() - 1
        u2 = 2 * random.random() - 1
        w = u1 * u1 + u2 * u2
        if w < 1:
            break
    w = math.sqrt((-2.0 * math.log(w)) / w)
    return mean + (u2 * w) * stdev


def mutate(candidate, search_space):
    child = {'vector': [], 'strategy': []}
    for i in xrange(len(candidate['vector'])):
        v_old = candidate['vector'][i]
        s_old = candidate['strategy'][i]
        v = v_old + s_old * random_gaussian()
        if v < search_space[i][0]:
            v = search_space[i][0]
        if v > search_space[i][1]:
            v = search_space[i][1]
        child['vector'].append(v)
        child['strategy'].append(s_old + random_gaussian() * abs(s_old)**0.5)
    return child


def tournament(candidate, population, bout_size):
    from random import randrange
    candidate['wins'] = 0
    for i in xrange(bout_size):
        other = population[randrange(len(population))]
        if candidate['fitness'] < other['fitness']:
            candidate['wins'] += 1


def init_population(minmax, pop_size):
    strategy = [[0,  (minmax[i][1]-minmax[i][0]) * 0.05] for i in xrange(len(minmax))]
    pop = [{'vector': random_vector(minmax), 'strategy': random_vector(strategy)} for i in xrange(pop_size)]
    for c in pop:
        c['fitness'] = objective_function(c['vector'])
    return pop


def search(max_gens, search_space, pop_size, bout_size):
    population = init_population(search_space, pop_size)
    for c in population:
        c['fitness'] = objective_function(c['vector'])
    population.sort(key=lambda x: x['fitness'])
    best = population[0]
    for gen in xrange(max_gens):
        children = [mutate(population[i], search_space) for i in xrange(pop_size)]
        for c in children:
            c['fitness'] = objective_function(c['vector'])
        children.sort(key=lambda x: x['fitness'])
        if children[0]['fitness'] < best['fitness']:
            best = children[0]
        union = children+population
        for c in union:
            tournament(c, union, bout_size)
        union.sort(key=lambda x: x['wins'], reverse=True)
        population = union[0:pop_size]
        print " > gen %d, fitness=%f" % (gen, best['fitness'])
    return best


def main():
    # problem configuration
    problem_size = 2
    search_space = [[-5, +5]] * problem_size
    # algorithm configuration
    max_gens = 200
    pop_size = 100
    bout_size = 5
    # execute the algorithm
    best = search(max_gens, search_space, pop_size, bout_size)
    print "Done! Solution: f=%f, s=%s" % (best['fitness'], str(best['vector']))

if __name__ == "__main__":
    main()


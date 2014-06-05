#!/usr/bin/env python

"""
Evolution Strategies
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


def mutate_problem(vector, stdevs, search_space):
    child = [0.0] * len(vector)
    for i in xrange(len(vector)):
        v = vector[i]
        child[i] = v + stdevs[i] * random_gaussian()
        if child[i] < search_space[i][0]:
            child[i] = search_space[i][0]
        if child[i] > search_space[i][1]:
            child[i] = search_space[i][1]
    return child


def mutate_strategy(stdevs):
    import math

    tau = math.sqrt(2.0*float(len(stdevs)))**-1.0
    tau_p = math.sqrt(2.0*math.sqrt(float(len(stdevs))))**-1.0
    child = [stdev * math.exp(tau_p*random_gaussian() + tau*random_gaussian()) for stdev in stdevs]
    return child


def mutate(par, minmax):
    child = {}
    child['vector'] = mutate_problem(par['vector'], par['strategy'], minmax)
    child['strategy'] = mutate_strategy(par['strategy'])
    return child


def init_population(minmax, pop_size):
    strategy = [[0,  (minmax[i][1]-minmax[i][0]) * 0.05] for i in xrange(len(minmax))]

    pop = []
    for i in xrange(pop_size):
        pop.append({
            'vector': random_vector(minmax),
            'strategy': random_vector(strategy)
        })

    for c in pop:
        c['fitness'] = objective_function(c['vector'])
    return pop


def search(max_gens, search_space, pop_size, num_children):
    population = init_population(search_space, pop_size)
    population.sort(key=lambda x: x['fitness'])
    best = population[0]
    for gen in xrange(max_gens):
        children = [mutate(population[i], search_space) for i in xrange(num_children)]
        for c in children:
            c['fitness'] = objective_function(c['vector'])
        union = children+population
        union.sort(key=lambda x: x['fitness'])
        if union[0]['fitness'] < best['fitness']:
            best = union[0]
        population = union[0:pop_size]
        print " > gen %d, fitness=%f" % (gen, best['fitness'])
    return best


def main():
    # problem configuration
    problem_size = 2
    search_space = [[-5, +5]] * problem_size

    # algorithm configuration
    max_gens = 100
    pop_size = 30
    num_children = 20
    # execute the algorithm
    best = search(max_gens, search_space, pop_size, num_children)
    print "Done! Solution: f=%f, s=%s"% (best['fitness'], str(best['vector']))

if __name__ == "__main__":
    main()


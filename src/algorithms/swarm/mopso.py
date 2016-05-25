#!/usr/bin/env python

"""
Multi-Objective Particle Swarm Optimization (PSO)
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective1(v):
    return sum(map(lambda x: x ** 2, v))


def objective2(v):
    return sum(map(lambda x: (x - 2.0) ** 2, v))


def random_vector(min_max):
    from random import random
    return map(lambda x: x[0] + (x[1]-x[0]) * random(), min_max)


def create_particle(search_space, vel_space):
    particle = {'position': random_vector(search_space)}
    particle['costs'] = [objective1(particle['position']), objective2(particle['position'])]
    particle['b_position'] = particle['position'][:]
    particle['b_costs'] = particle['costs']
    particle['velocity'] = random_vector(vel_space)
    return particle


def create_grid():
    pass


def dominates(p1, p2):
    for i in xrange(len(p1['objectives'])):
        if p1['objectives'][i] > p2['objectives'][i]:
            return False
    return True


def mutate(p, pm, search_space):
    from random import randint, uniform

    n = len(p['vector'])
    j = randint(0, n - 1)
    dx = pm * (search_space[j][1] - search_space[j][0])

    lb = iif(p['vector'][j] - dx < search_space[j][0], search_space[j][0], p['vector'][j] - dx)
    ub = iif(p['vector'][j] + dx > search_space[j][1], search_space[j][1], p['vector'][j] + dx)

    p['vector'][j] = uniform(lb, ub)


def search(search_space, vel_space, max_gens, pop_size):
    pop = [create_particle(search_space, vel_space) for i in xrange(pop_size)]


def main():
    # problem configuration
    problem_size = 1
    search_space = [[-10, 10]] * problem_size
    # algorithm configuration
    vel_space = [[-1, 1]] * problem_size
    max_gens = 50
    pop_size = 80
    p_cross = 0.90
    # execute the algorithm
    pop_set = search(search_space, vel_space, max_gens, pop_size)
    print "Done!"


if __name__ == "__main__":
    main()

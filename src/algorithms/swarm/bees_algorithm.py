#!/usr/bin/env python

"""
Bees Algorithm
"""

def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x**2, v))


def random_vector(minmax):
    import random
    return map(lambda x: x[0] + (x[1]-x[0]) * random.random(), minmax)


def create_random_bee(search_space):
    return {'vector': random_vector(search_space)}


def create_neigh_bee(site, patch_size, search_space):
    import random
    vector = []
    for i in xrange(len(site)):
        v = site[i]
        v = iif(random.random()<0.5, v+random.random()*patch_size,  v-random.random()*patch_size)
        if v < search_space[i][0]:
            v = search_space[i][0]
        if v > search_space[i][1]:
            v = search_space[i][1]
        vector.append(v)
    return {'vector': vector}


def search_neigh(parent, neigh_size, patch_size, search_space):
    neigh = []
    for i in xrange(neigh_size):
        neigh.append(create_neigh_bee(parent['vector'], patch_size, search_space))
        for bee in neigh:
            bee['fitness'] = objective_function(bee['vector'])
    return neigh.sort(key=lambda x: x['fitness'])[0]


def create_scout_bees(search_space, num_scouts):
    return [create_random_bee(search_space)] * num_scouts


def search(max_gens, search_space, num_bees, num_sites, elite_sites, patch_size, e_bees, o_bees):
    best = None
    pop = [create_random_bee(search_space)] * num_bees
    for gen in xrange(max_gens):
        for bee in pop:
            bee['fitness'] = objective_function(bee['vector'])
        pop.sort(key=lambda x: x['fitness'])
        if best is None or pop[0]['fitness'] < best['fitness']:
            best = pop[0]
        next_gen = []
        for i in xrange(num_sites):
            parent = pop[i]
            neigh_size = iif(i<elite_sites, e_bees, o_bees)
            next_gen.append(search_neigh(parent, neigh_size, patch_size, search_space))

    scouts = create_scout_bees(search_space, (num_bees-num_sites))
    pop = next_gen + scouts
    patch_size *= 0.95
    print " > it=%d, patch_size=%d, f=%f" % (gen+1, patch_size, best['fitness'])
    return best


def main():
    # problem configuration
    problem_size = 3
    search_space = [[-5, 5]] * problem_size
    # algorithm configuration
    max_gens = 500
    num_bees = 45
    num_sites = 3
    elite_sites = 1
    patch_size = 3.0
    e_bees = 7
    o_bees = 2
    # execute the algorithm
    best = search(max_gens, search_space, num_bees, num_sites, elite_sites, patch_size, e_bees, o_bees)
    print "done! Solution: f=%f, s=%s" % (best['fitness'], str(best['vector']))

if __name__ == "__main__":
    main()


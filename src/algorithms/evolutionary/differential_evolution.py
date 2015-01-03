#!/usr/bin/env python

"""
Differential Evolution (DE)
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x**2, v))


def random_vector(min_max):
    import random
    return map(lambda x: x[0] + (x[1]-x[0]) * random.random(), min_max)


def de_rand_1_bin(p0, p1, p2, p3, f, cr, search_space):
    from random import random, randint
    sample = {'vector':  [0] * len(p0['vector'])}
    cut = 1 + randint(0, len(sample['vector'])-1)
    for i in xrange(0, len(sample['vector'])):
        if i == cut or random() < cr:
            v = p3['vector'][i] + f * (p1['vector'][i] - p2['vector'][i])
            if v < search_space[i][0]:
                v = search_space[i][0]
            if v > search_space[i][1]:
                v = search_space[i][1]
            sample['vector'][i] = v
    return sample


def select_parents(pop, current):
    from random import randint
    p1, p2, p3 = randint(0, len(pop)-1), randint(0, len(pop)-1), randint(0, len(pop)-1)
    while p1 == current:
        p1 = randint(0, len(pop)-1)
    while p2 == current or p2 == p1:
        p2 = randint(0, len(pop)-1)
    while p3 == current or p3 == p2 or p3 == p1:
        p3 = randint(0, len(pop)-1)
    return [p1, p2, p3]


def create_children(pop, min_max, f, cr):
    children = []
    for i in xrange(0, len(pop)):
        p0 = pop[i]
        p1, p2, p3 = select_parents(pop, i)
        children.append(de_rand_1_bin(p0, pop[p1], pop[p2], pop[p3], f, cr, min_max))
    return children


def select_population(parents, children):
    return map(lambda i: iif(children[i]['cost'] <= parents[i]['cost'], children[i], parents[i]), xrange(0, len(parents)))


def search(max_gens, search_space, pop_size, w, cr):
    pop = map(lambda i: {'vector' : random_vector(search_space)}, xrange(0, pop_size))
    for p in pop:
        p['cost'] = objective_function(p['vector'])
    pop.sort(key=lambda x: x['cost'])
    best = pop[0]
    for gen in xrange(0, max_gens):
        children = create_children(pop, search_space, w, cr)
        for c in children:
            c['cost'] = objective_function(c['vector'])
        pop = select_population(pop, children)
        pop.sort(key=lambda x: x['cost'])
        if pop[0]['cost'] < best['cost']:
            best = pop[0]
        print ' > gen %d, cost=%f' % (gen+1, best['cost'])
    return best


def main():
    # problem configuration
    problem_size = 3
    search_space = [[-5, +5]] * problem_size
    # algorithm configuration
    max_gens = 200
    pop_size = 10*problem_size
    weight = 0.8
    cross = 0.9
    # execute the algorithm
    best = search(max_gens, search_space, pop_size, weight, cross)
    print "Done! Solution: f=%f, s=%s" % (best['cost'], str(best['vector']))


if __name__ == "__main__":
    main()

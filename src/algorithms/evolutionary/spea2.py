#!/usr/bin/env python

"""
Strength Pareto Evolutionary Algorithm 2 (SPEA2)
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective1(v):
    return sum(map(lambda x: x ** 2, v))


def objective2(v):
    return sum(map(lambda x: (x - 1.0) ** 2, v))


def reverse(text):
    return text[::-1]


def decode(bitstring, search_space, bits_per_param):
    vector = []
    for i in xrange(len(search_space)):
        bounds = search_space[i]
        off, sum_value = i*bits_per_param, 0.0
        param = reverse(bitstring[off:(off+bits_per_param)])
        for j in xrange(len(param)):
            sum_value += iif(param[j] == '1', 1.0, 0.0) * (2.0 ** j)

        min_value, max_value = bounds
        vector.append(min_value + ((max_value-min_value)/((2.0**bits_per_param)-1.0)) * sum_value)

    return vector


def random_bitstring(num_bits):
    from random import random
    return "".join([iif(random() < 0.5, "1", "0") for i in xrange(num_bits)])


def point_mutation(bitstring, rate):
    from random import random
    child = ""
    for i in xrange(len(bitstring)):
        bit = bitstring[i]
        child += iif(random() < rate, iif(bit == '1', "0", "1"), bit)

    return child


def binary_tournament(pop):
    from random import randrange
    i, j = randrange(len(pop)), randrange(len(pop))
    while j == i:
        j = randrange(len(pop))
    return iif(pop[i]['fitness'] < pop[j]['fitness'], pop[i], pop[j])


def crossover(parent1, parent2, rate):
    from random import random
    if random() >= rate:
        return (parent1+'x')[:-1]
    child = ""
    for i in xrange(len(parent1)):
        child += (iif(random() < 0.5, parent1[i], parent2[i]))
    return child


def reproduce(selected, pop_size, p_cross):
    children = []
    for i, p1 in enumerate(selected):
        if i % 2 == 0:
            if i+1 == len(selected):
                p2 = selected[0]
            else:
                p2 = selected[i+1]
        else:
            p2 = selected[i-1]
        if i == len(selected) - 1:
            p2 = selected[0]
        child = {'bitstring': crossover(p1['bitstring'], p2['bitstring'], p_cross)}
        child['bitstring'] = point_mutation(child['bitstring'], 1.0/len(child['bitstring']))
        children.append(child)
        if len(children) >= pop_size:
            break

    return children


def calculate_objectives(pop, search_space, bits_per_param):
    for p in pop:
        p['vector'] = decode(p['bitstring'], search_space, bits_per_param)
        p['objectives'] = []
        p['objectives'].append(objective1(p['vector']))
        p['objectives'].append(objective2(p['vector']))


def dominates(p1, p2):
    for i in xrange(len(p1['objectives'])):
        if p1['objectives'][i] > p2['objectives'][i]:
            return False
    return True


def weighted_sum(x):
    return sum(x['objectives'])


def euclidean_distance(c1, c2):
    import math
    return round(math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2))


def calculate_dominated(pop):
    for p1 in pop:
        p1['dom_set'] = []
        for p2 in pop:
            if p1 != p2 and dominates(p1, p2):
                p1['dom_set'].append(p2)


def calculate_raw_fitness(p1, pop):
    return sum(map(lambda p2: iif(dominates(p1, p2), len(p2['dom_set']), 0), pop))


def calculate_density(p1, pop):
    import math
    for p2 in pop:
        p2['dist'] = euclidean_distance(p1['objectives'], p2['objectives'])

    lst = pop[:]
    lst.sort(key=lambda x: x['dist'])
    k = int(math.sqrt(len(pop)))
    return 1.0 / (lst[k]['dist'] + 2.0)


def calculate_fitness(pop, archive, search_space, bits_per_param):
    calculate_objectives(pop, search_space, bits_per_param)
    union = archive + pop
    calculate_dominated(union)
    for p in union:
        p['raw_fitness'] = calculate_raw_fitness(p, union)
        p['density'] = calculate_density(p, union)
        p['fitness'] = p['raw_fitness'] + p['density']


def environmental_selection(pop, archive, archive_size):
    import math
    union = archive + pop
    environment = [p for p in union if p['fitness'] < 1.0]
    if len(environment) < archive_size:
        union.sort(key=lambda x: x['fitness'])
        for p in union:
            if p['fitness'] >= 1.0:
                environment.append(p)
            if len(environment) >= archive_size:
                break
    elif len(environment) > archive_size:
        while len(environment) > archive_size:
            k = int(math.sqrt(len(environment)))
            for p1 in environment:
                for p2 in environment:
                    p2['dist'] = euclidean_distance(p1['objectives'], p2['objectives'])

                    l = environment.sort(key=lambda x: x['dist'])
                    p1['density'] = l[k]['dist']

            environment.sort(key=lambda x: x['density'])
            environment.pop()

    return environment


def search(search_space, max_gens, pop_size, archive_size, p_cross, bits_per_param=16):
    pop = [{'bitstring': random_bitstring(len(search_space)*bits_per_param)} for i in xrange(pop_size)]
    gen, archive = 0, []
    while True:
        calculate_fitness(pop, archive, search_space, bits_per_param)
        archive = environmental_selection(pop, archive, archive_size)
        archive.sort(key=lambda x: weighted_sum(x))
        best = archive[0]
        print ">gen = %d, objs = %s, bits = %s" % (gen, str(best['objectives']), best['bitstring'])
        if gen >= max_gens:
            break
        selected = [binary_tournament(archive) for i in xrange(pop_size)]
        pop = reproduce(selected, pop_size, p_cross)
        gen += 1

    return archive


def main():
    # problem configuration
    problem_size = 1
    search_space = [[-10, 10]] * problem_size
    # algorithm configuration
    max_gens = 50
    pop_size = 80
    archive_size = 40
    p_cross = 0.90
    # execute the algorithm
    pop = search(search_space, max_gens, pop_size, archive_size, p_cross)
    print "Done!"


if __name__ == "__main__":
    main()
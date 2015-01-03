#!/usr/bin/env python

"""
Genetic Algorithm
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def one_max(bitstring):
    return sum(map(lambda x: iif(x == '1', 1, 0), bitstring))


def random_bitstring(num_bits):
    from random import sample
    return map(lambda x: iif(x < 50, '1', '0'), sample(range(100), num_bits))


def binary_tournament(pop):
    from random import randint
    i, j = randint(0, len(pop) - 1), randint(0, len(pop) - 1)
    while j == i:
        j = randint(0, len(pop) - 1)
    return iif(pop[i]['fitness'] > pop[j]['fitness'], pop[i], pop[j])


def point_mutation(bitstring, rate):
    from random import random
    child = ""
    for i in xrange(0, len(bitstring)):
        bit = bitstring[i]
        child = child + iif(random() < rate, iif(bit == '1', '0', '1'), bit)
    return child


def crossover(parent1, parent2, rate):
    from random import random, randint
    if random() >= rate:
        return parent1
    point = 1 + randint(0, len(parent1) - 2)
    return parent1[0:point] + parent2[point:len(parent1)]


def reproduce(selected, pop_size, p_cross, p_mutation):
    children = []
    for i in xrange(0, len(selected)):
        p1 = selected[i]
        ix = iif(i % 2 == 0, i + 1, i - 1)
        if i == len(selected) - 1:
            ix = 0
        p2 = selected[ix]
        child = {}
        child['bitstring'] = crossover(p1['bitstring'], p2['bitstring'], p_cross)
        child['bitstring'] = point_mutation(child['bitstring'], p_mutation)
        children.append(child)
        if (len(children) >= pop_size):
            break
    return children


def search(max_gens, num_bits, pop_size, p_crossover, p_mutation):
    population = []
    for i in xrange(0, pop_size):
        population.append({'bitstring': random_bitstring(num_bits)})
    for c in population:
        c['fitness'] = one_max(c['bitstring'])
    population.sort(key=lambda x: x['fitness'])
    best = population[0]
    for gen in xrange(max_gens):
        selected = [binary_tournament(population) for i in xrange(0, pop_size)]
        children = reproduce(selected, pop_size, p_crossover, p_mutation)
        for c in children:
            c['fitness'] = one_max(c['bitstring'])
        children.sort(key=lambda x: x['fitness'])
        if children[0]['fitness'] > best['fitness']:
            best = children[0]
        population = children
        print " > gen %d, best: %d, %s" % (gen, best['fitness'], best['bitstring'])
        if best['fitness'] == num_bits:
            break
    return best


def main():
    # problem configuration
    num_bits = 64
    # algorithm configuration
    max_gens = 100
    pop_size = 100
    p_crossover = 0.98
    p_mutation = 1.0 / num_bits
    # execute the algorithm
    best = search(max_gens, num_bits, pop_size, p_crossover, p_mutation)
    print "done! Solution: f=%f, s=%s" % (best['fitness'], str(best['bitstring']))


if __name__ == "__main__":
    main()

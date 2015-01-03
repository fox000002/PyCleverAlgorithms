#!/usr/bin/env python

"""
Clonal Selection Algorithm (CSA)
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x ** 2, v))


def decode(bitstring, search_space, bits_per_param):
    vector = []
    for i, bounds in enumerate(search_space):
        off, sum_v = i*bits_per_param, 0.0
        param_values = bitstring[off:off+bits_per_param]
        param_values = param_values[::-1]
        for j in xrange(len(param_values)):
            sum_v += iif(param_values[j] == '1', 1.0, 0.0) * (2.0 ** float(j))
        min_v, max_v = bounds
        vector.append(min_v + ((max_v-min_v)/((2.0**float(bits_per_param))-1.0)) * sum_v)
    return vector


def evaluate(pop, search_space, bits_per_param):
    for p in pop:
        p['vector'] = decode(p['bitstring'], search_space, bits_per_param)
        p['cost'] = objective_function(p['vector'])


def random_bitstring(num_bits):
    from random import random
    return ''.join(map(lambda x: iif(random() < 0.5, '1', '0'), xrange(num_bits)))


def point_mutation(bitstring, rate):
    from random import random
    child = ""
    for i in xrange(len(bitstring)):
        bit = bitstring[i]
        child = child + (iif(random() < rate, iif(bit == '1', "0", "1"), bit))
    return child


def calculate_mutation_rate(antibody, mutation_factor=-2.5):
    from math import exp
    return exp(mutation_factor * antibody['affinity'])


def calc_num_clones(pop_size, clone_factor):
    from math import floor
    return int(floor(pop_size * clone_factor))


def calculate_affinity(pop):
    pop.sort(key=lambda x: x['cost'])
    range_v = pop[-1]['cost'] - pop[0]['cost']
    if range_v == 0.0:
        for p in pop:
            p['affinity'] = 1.0
    else:
        for p in pop:
            p['affinity'] = 1.0-(p['cost']/range_v)


def clone_and_hypermutate(pop, clone_factor):
    clones = []
    num_clones = calc_num_clones(len(pop), clone_factor)
    calculate_affinity(pop)
    for antibody in pop:
        m_rate = calculate_mutation_rate(antibody)
        for i in xrange(num_clones):
            clone = {'bitstring': point_mutation(antibody['bitstring'], m_rate)}
            clones.append(clone)
    return clones


def random_insertion(search_space, pop, num_rand, bits_per_param):
    if num_rand == 0:
        return pop
    rands = [{'bitstring': random_bitstring(len(search_space)*bits_per_param)} for i in xrange(num_rand)]
    evaluate(rands, search_space, bits_per_param)
    pop_all = pop + rands
    pop_all.sort(key=lambda x: x['cost'])
    return pop_all[:len(pop)]


def search(search_space, max_gens, pop_size, clone_factor, num_rand, bits_per_param=16):
    pop = [{'bitstring': random_bitstring(len(search_space)*bits_per_param)} for i in xrange(pop_size)]
    evaluate(pop, search_space, bits_per_param)
    best = min(pop, key=lambda x: x['cost'])
    for gen in xrange(max_gens):
        clones = clone_and_hypermutate(pop, clone_factor)
        evaluate(clones, search_space, bits_per_param)
        pop = pop + clones
        pop.sort(key=lambda x: x['cost'])
        pop = pop[:pop_size]
        pop = random_insertion(search_space, pop, num_rand, bits_per_param)
        pop.append(best)
        best = min(pop, key=lambda x: x['cost'])
        print " > gen %d, f=%s, s=%s, v=%s" % (gen+1, str(best['cost']), best['bitstring'], str(best['vector']))
    return best


def main():
    # problem configuration
    problem_size = 2
    search_space = [[-5, 5]] * problem_size
    # algorithm configuration
    max_gens = 100
    pop_size = 100
    clone_factor = 0.1
    num_rand = 2
    # execute the algorithm
    best = search(search_space, max_gens, pop_size, clone_factor, num_rand)
    print "done! Solution: f=%f, s=%s, v=%s" % (best['cost'], best['bitstring'], str(best['vector']))


if __name__ == "__main__":
    main()


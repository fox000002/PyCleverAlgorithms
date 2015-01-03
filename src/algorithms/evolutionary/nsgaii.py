#!/usr/bin/env python

"""
NSGA II
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective1(v):
    return sum(map(lambda x: x ** 2, v))


def objective2(v):
    return sum(map(lambda x: (x - 2.0) ** 2, v))


def decode(bitstring, search_space, bits_per_param):
    vector = []
    for i, bounds in enumerate(search_space):
        off, sum_v = i*bits_per_param, 0.0
        param = bitstring[off:(off+bits_per_param)].reverse
        for j in xrange(len(param)):
            sum_v += iif(param[j] == '1', 1.0, 0.0) * (2.0 ** float(j))

        min_v, max_v = bounds
        vector.append(min_v + ((max_v-min_v)/((2.0**float(bits_per_param))-1.0)) * sum_v)
    return vector


def random_bitstring(num_bits):
    from random import sample
    return map(lambda x: iif(x < 50, '1', '0'), sample(range(100), num_bits))


def point_mutation(bitstring, rate):
    from random import random
    child = ""
    for i in xrange(0, len(bitstring)):
        bit = bitstring[i]
        child = child + iif(random() < rate, iif(bit == '1', '0', '1'), bit)
    return child


def crossover(parent1, parent2, rate):
    pass


def reproduce(selected, pop_size, p_cross):
    pass


def calculate_objectives(pop, search_space, bits_per_param):
    pass


def dominates(p1, p2):
    for i in xrange(len(p1['objectives'])):
        if p1['objectives'][i] > p2['objectives'][i]:
            return False
    return True


def fast_nondominated_sort(pop):
    pass


def calculate_crowding_distance(pop):
    for p in pop:
        p['dist'] = 0.0
    num_obs = len(pop[0]['objectives'])
    for i in xrange(num_obs):
        min_v = min(pop, key=lambda x: x['objectives'][i])
        max_v = max(pop, key=lambda x: x['objectives'][i])
        rge = max_v['objectives'][i] - min_v['objectives'][i]
        pop[0]['dist'], pop[-1]['dist'] = 1.0/0.0, 1.0/0.0
        if rge == 0.0:
            continue
        for j in xrange(1, len(pop)):
            pop[j]['dist'] += (pop[j+1]['objectives'][i]-pop[j-1]['objectives'][i])/rge


def crowded_comparison_operator(x, y):
    pass


def better(x, y):
    pass


def select_parents(fronts, pop_size):
    pass


def weighted_sum(x):
    pass


def search(search_space, max_gens, pop_size, p_cross, bits_per_param=16):
    pass


def main():
    # problem configuration
    problem_size = 1
    search_space = [[-10, 10]] * problem_size
    # algorithm configuration
    max_gens = 50
    pop_size = 100
    p_cross = 0.98
    # execute the algorithm
    pop = search(search_space, max_gens, pop_size, p_cross)
    print "done!"


if __name__ == "__main__":
    main()


#!/usr/bin/env python

"""
Stochastic Hill Climbing
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def one_max(v):
    return sum(map(lambda x: iif(x == '1', 1, 0), v))


def random_bitstring(num_bits):
    from random import sample
    return map(lambda x: iif(x < 50, '1', '0'), sample(range(100), num_bits))


def random_neighbor(bitstring):
    from random import randint

    mutant = bitstring[:]
    pos = randint(0, len(bitstring) - 1)
    #print '-->', mutant
    mutant[pos] = iif(mutant[pos] == '1', '0', '1')
    #print '<--', mutant
    return mutant


def search(max_iteration, num_bits):
    candidate = {
        'vector': random_bitstring(num_bits)
    }
    candidate['cost'] = one_max(candidate['vector'])
    for iteration in range(0, max_iteration):
        neighbor = {
            'vector': random_neighbor(candidate['vector'])
        }
        neighbor['cost'] = one_max(neighbor['vector'])
        if neighbor['cost'] >= candidate['cost']:
            candidate = neighbor
        print ' > iteration %d, best=%d' % (iteration + 1, candidate['cost'])
        if candidate['cost'] == num_bits:
            break
    return candidate


def main():
    #
    num_bits = 15
    #
    max_iteration = 10
    #
    best = search(max_iteration, num_bits)
    print 'Done. Best Solution: c=%d, v=%s' % (best['cost'], str(best['vector']))


if __name__ == "__main__":
    main()

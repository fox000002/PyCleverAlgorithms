#!/usr/bin/env python

"""Greedy Randomized Adaptive Search Procedure
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def euc_2d(c1, c2):
    import math

    return round(math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2))


def cost(permutation, cities):
    distance = 0
    for i in range(0, len(permutation)):
        #print '-->', i, '=', permutation[i]
        c1 = permutation[i]
        c2 = permutation[iif(i == len(permutation) - 1, 0, i + 1)]
        distance += euc_2d(cities[c1], cities[c2])
    return distance


def stochastic_two_opt(permutation):
    from random import randrange

    perm = permutation[:]
    c1, c2 = randrange(len(perm)), randrange(len(perm))
    exclude = [c1]
    exclude.append(iif(c1 == 0, len(perm) - 1, c1 - 1))
    exclude.append(iif(c1 == len(perm) - 1, 0, c1 + 1))
    while c2 in exclude:
        c2 = randrange(len(perm))
    if c2 < c1:
        c1, c2 = c2, c1
    r = perm[c1:c2]
    r.reverse()
    perm[c1:c2] = r
    return perm


def local_search(best, cities, max_no_improv):
    count = 0
    while count < max_no_improv:
        candidate = {}
        candidate['vector'] = stochastic_two_opt(best['vector'])
        candidate['cost'] = cost(candidate['vector'], cities)
        count = iif(candidate['cost'] < best['cost'], 0, count + 1)
        if candidate['cost'] < best['cost']:
            best = candidate
    return best


def construct_randomized_greedy_solution(cities, alpha):
    from random import randrange
    candidate = {}
    candidate['vector'] = [randrange(len(cities)) for i in xrange(len(cities))]
    all_cities = list(range(len(cities)))
    while len(candidate['vector']) < len(cities):
        candidates = all_cities - candidate['vector']
        costs = [euc_2d(cities[candidate['vector'][-1]], cities[i]) for i in xrange(len(candidates))]
    rcl, max_cost, min_cost = [], max(costs), min(costs)
    for i in xrange(len(costs)):
        c = costs[i]
        if c <= (min_cost + alpha*(max_cost-min_cost)):
            rcl.append(candidates[i])
    candidate['vector'].append(rcl[randrange(len(rcl))])
    candidate['cost'] = cost(candidate['vector'], cities)
    return candidate


def search(cities, max_iteration, max_no_improve, alpha):
    best = {}
    for iteration in range(0, max_iteration):
        candidate = construct_randomized_greedy_solution(cities, alpha)
        candidate = local_search(candidate, cities, max_no_improve)
        if candidate['cost'] < best['cost']:
            best = candidate
        print ' > iteration %d, best=%d' % (iteration + 1, best['cost'])
    return best


def main():
    # problem configuration
    berlin52 = [[565, 575], [25, 185], [345, 750], [945, 685], [845, 655],
                [880, 660], [25, 230], [525, 1000], [580, 1175], [650, 1130], [1605, 620],
                [1220, 580], [1465, 200], [1530, 5], [845, 680], [725, 370], [145, 665],
                [415, 635], [510, 875], [560, 365], [300, 465], [520, 585], [480, 415],
                [835, 625], [975, 580], [1215, 245], [1320, 315], [1250, 400], [660, 180],
                [410, 250], [420, 555], [575, 665], [1150, 1160], [700, 580], [685, 595],
                [685, 610], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960],
                [95, 260], [875, 920], [700, 500], [555, 815], [830, 485], [1170, 65],
                [830, 610], [605, 625], [595, 360], [1340, 725], [1740, 245]]
    # algorithm configuration
    max_iterations = 100
    max_no_improve = 50
    # execute the algorithm
    best = search(berlin52, max_iterations, max_no_improve)
    print 'Done. Best Solution: c=%d, v=%s' % (best['cost'], str(best['vector']))


if __name__ == "__main__":
    main()
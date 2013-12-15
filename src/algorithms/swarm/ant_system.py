#!/usr/bin/env python

# Ant System algorithm/Ant Cycle algorithm
# It's inspired by the foraging behavior of ants, specifically the pheromone communication
# between ants regarding a good path between the colony and a food source in an environment.
# The mechanism is called stigmergy.


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def euc_2d(c1, c2):
    import math
    return round(math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2))


def cost(permutation, cities):
    distance = 0
    for i in range(0, len(permutation)):
        c1 = permutation[i]
        c2 = permutation[iif(i == len(permutation) - 1, 0, i + 1)]
        distance += euc_2d(cities[c1], cities[c2])
    return distance


def random_permutation(cities):
    import random
    perm = range(0, len(cities))
    for i in perm:
        r = random.randrange(len(perm) - i) + i
        perm[r], perm[i] = perm[i], perm[r]
    return perm


def initialise_pheromone_matrix(num_cities, naive_score):
    v = float(num_cities) / naive_score
    return [[v] * num_cities] * num_cities


def calculate_choices(cities, last_city, exclude, pheromone, c_heur, c_hist):
    choices = []
    for i in xrange(0, len(cities)):
        coord = cities[i]
        if i in exclude:
            continue
        prob = {'city': i}
        prob['history'] = pheromone[last_city][i] ** c_hist
        prob['distance'] = euc_2d(cities[last_city], coord)
        prob['heuristic'] = (1.0 / prob['distance']) ** c_heur
        prob['prob'] = prob['history'] * prob['heuristic']
        choices.append(prob)
    return choices


def select_next_city(choices):
    import random
    s = sum(map(lambda x: x['prob'], choices))
    if s == 0.0:
        return choices[random.randint(0, len(choices)-1)]['city']
    v = random.random()
    for i in xrange(0, len(choices)):
        choice = choices[i]
        v -= (choice['prob'] / s)
    if v <= 0.0:
        return choice['city']

    return choices[-1]['city']


def stepwise_const(cities, phero, c_heur, c_hist):
    import random

    perm = []
    perm.append(random.randint(0, len(cities)-1))

    if len(perm) != len(cities):
        choices = calculate_choices(cities, perm[-1], perm, phero, c_heur, c_hist)
        next_city = select_next_city(choices)
        perm.append(next_city)

    return perm


def decay_pheromone(pheromone, decay_factor):
    for array in pheromone:
        for i in xrange(len(array)):
            p = array[i]
            array[i] = (1.0 - decay_factor) * p


def update_pheromone(pheromone, solutions):
    for other in solutions:
        for i in xrange(len(other['vector'])):
            x = other['vector'][i]
            if i == (len(other['vector']) - 1):
                y = other['vector'][0]
            else:
                y = other['vector'][i + 1]
            pheromone[x][y] += (1.0 / other['cost'])
            pheromone[y][x] += (1.0 / other['cost'])


def search(cities, max_it, num_ants, decay_factor, c_heur, c_hist):
    best = {'vector': random_permutation(cities)}
    best['cost'] = cost(best['vector'], cities)
    pheromone = initialise_pheromone_matrix(len(cities), best['cost'])
    for iter in xrange(max_it):
        solutions = []
        for i in xrange(num_ants):
            candidate = {}
            candidate['vector'] = stepwise_const(cities, pheromone, c_heur, c_hist)
            candidate['cost'] = cost(candidate['vector'], cities)
            if candidate['cost'] < best['cost']:
                best = candidate
            solutions.append(candidate)

        decay_pheromone(pheromone, decay_factor)
        update_pheromone(pheromone, solutions)
        print " > iteration %d, best=%f" % (iter + 1, best['cost'])
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
    max_it = 50
    num_ants = 30
    decay_factor = 0.6
    c_heur = 2.5
    c_hist = 1.0
    # execute the algorithm
    best = search(berlin52, max_it, num_ants, decay_factor, c_heur, c_hist)
    print "Done. Best Solution: c=%f, v=%s" % (best['cost'], str(best['vector']))


if __name__ == "__main__":
    main()


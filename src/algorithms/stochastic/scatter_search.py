#!/usr/bin/env python

"""
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x ** 2, v))


def rand_in_bounds(min_v, max_v):
    import random

    return min_v + ((max_v - min_v) * random.random())


def random_vector(minmax):
    return map(lambda x: rand_in_bounds(x[0], x[1]), minmax)


def take_step(minmax, current, step_size):
    position = [0] * len(current)
    for i in xrange(0, len(position)):
        min_v = max(minmax[i][0], current[i] - step_size)
        max_v = min(minmax[i][1], current[i] + step_size)
        position[i] = rand_in_bounds(min_v, max_v)
    return position


def local_search(best, bounds, max_no_improv, step_size):
    count = 0
    while count < max_no_improv:
        candidate = {'vector': take_step(bounds, best['vector'], step_size)}
        candidate['cost'] = objective_function(candidate['vector'])
        count = iif(candidate['cost'] < best['cost'], 0, count + 1)
        if candidate['cost'] < best['cost']:
            best = candidate
    return best


def construct_initial_set(bounds, set_size, max_no_improv, step_size):
    diverse_set = []
    while len(diverse_set) < set_size:
        cand = {'vector': random_vector(bounds)}
        cand['cost'] = objective_function(cand['vector'])
        cand = local_search(cand, bounds, max_no_improv, step_size)
        if not any(x['vector'] == cand['vector'] for x in diverse_set):
            diverse_set.append(cand)
    return diverse_set


def euclidean_distance(c1, c2):
    import math

    s = sum(map(lambda i: (c1[i] - c2[i]) ** 2, xrange(0, len(c1))))
    return math.sqrt(s)


def distance(v, set):
    return sum(map(lambda x: euclidean_distance(v, x['vector']), set))


def diversify(diverse_set, num_elite, ref_set_size):
    diverse_set.sort(key=lambda x: x['cost'])
    ref_set = diverse_set[0:num_elite]
    remainder = [x for x in diverse_set if not (x in ref_set)]
    for c in remainder:
        c['dist'] = distance(c['vector'], ref_set)
    remainder.sort(key=lambda x: x['dist'])
    ref_set = ref_set + remainder[0: ref_set_size - len(ref_set)]
    return [ref_set, ref_set[0]]


def select_subsets(ref_set):
    additions = [c for c in ref_set if c['new']]
    remainder = [x for x in ref_set if not (x in additions)]
    if remainder is None or len(remainder) == 0:
        remainder = additions
    subsets = []
    for a in additions:
        for r in remainder:
            if a != r and (not ([r, a] in subsets)):
                subsets.append([a, r])
    return subsets


def recombine(subset, minmax):
    import random

    a, b = subset
    d = map(lambda x: (b['vector'][x] - a['vector'][x]) / 2.0, xrange(0, len(a['vector'])))
    children = []
    for p in subset:
        direction, r = iif(random.random() < 0.5, +1.0, -1.0), random.random()
        child = {'vector': [0] * len(minmax)}
        for i in xrange(0, len(child['vector'])):
            child['vector'][i] = p['vector'][i] + (direction * r * d[i])
            if child['vector'][i] < minmax[i][0]:
                child['vector'][i] = minmax[i][0]
            if child['vector'][i] > minmax[i][1]:
                child['vector'][i] = minmax[i][1]
        child['cost'] = objective_function(child['vector'])
        children.append(child)
    return children


def explore_subsets(bounds, ref_set, max_no_improv, step_size):
    was_change = False
    subsets = select_subsets(ref_set)
    for c in ref_set:
        c['new'] = False
    for subset in subsets:
        candidates = recombine(subset, bounds)
        improved = [local_search(candidates[i], bounds, max_no_improv, step_size) for i in xrange(0, len(candidates))]
        for c in improved:
            if not [x for x in ref_set if x['vector'] == c['vector']]:
                c['new'] = True
                ref_set.sort(key=lambda x: x['cost'])
                if c['cost'] < ref_set[-1]['cost']:
                    del ref_set[-1]
                    ref_set.append(c)
                    print "  >> added, cost=%f" % c['cost']
                    was_change = True
    return was_change


def search(bounds, max_iter, ref_set_size, div_set_size, max_no_improv, step_size, max_elite):
    diverse_set = construct_initial_set(bounds, div_set_size, max_no_improv, step_size)
    ref_set, best = diversify(diverse_set, max_elite, ref_set_size)
    for c in ref_set:
        c['new'] = True
    for iter in xrange(0, max_iter):
        was_change = explore_subsets(bounds, ref_set, max_no_improv, step_size)
        ref_set.sort(key=lambda x: x['cost'])
        if ref_set[0]['cost'] < best['cost']:
            best = ref_set[0]
        print " > iter=%d, best=%f" % (iter + 1, best['cost'])
        if not was_change:
            break

    return best


def main():
    #
    problem_size = 3
    bounds = [[-5, 5]] * problem_size
    # algorithm configuration
    max_iter = 100
    step_size = (bounds[0][1] - bounds[0][0]) * 0.005
    max_no_improv = 30
    ref_set_size = 10
    diverse_set_size = 20
    no_elite = 5
    # execute the algorithm
    best = search(bounds, max_iter, ref_set_size, diverse_set_size, max_no_improv, step_size, no_elite)
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['vector']))


if __name__ == "__main__":
    main()

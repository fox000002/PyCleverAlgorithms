#!/usr/bin/env python

"""
Artificial Immune Recognition System
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def random_vector(min_max):
    import random
    return map(lambda x: x[0] + (x[1] - x[0]) * random.random(), min_max)


def generate_random_pattern(domain):
    from random import randrange
    class_label = domain.keys()[randrange(len(domain.keys()))]
    pattern = {
        'label': class_label,
        'vector': random_vector(domain[class_label])
    }
    return pattern


def create_cell(vector, class_label):
    return {'label': class_label, 'vector': vector}


def initialize_cells(domain):
    return [create_cell(random_vector([[0, 1], [0, 1]]), key) for key in domain.keys()]


def distance(c1, c2):
    from math import sqrt
    sum_v = 0.0
    for i in xrange(len(c1)):
        sum_v = (c1[i] - c2[i]) ** 2
    return sqrt(sum_v)


def stimulate(cells, pattern):
    max_dist = distance([0.0, 0.0], [1.0, 1.0])
    for cell in cells:
        cell['affinity'] = distance(cell['vector'], pattern['vector']) / max_dist
        cell['stimulation'] = 1.0 - cell['affinity']


def get_most_stimulated_cell(mem_cells, pattern):
    stimulate(mem_cells, pattern)
    mem_cells.sort(key=lambda x: x['stimulation'])
    return mem_cells[0]


def mutate_cell(cell, best_match):
    from random import random
    range_value = 1.0 - best_match['stimulation']
    for i, v in enumerate(cell['vector']):
        min_v = max([(v-(range_value/2.0)), 0.0])
        max_v = min([(v+(range_value/2.0)), 1.0])
        cell['vector'][i] = min_v + (random() * (max_v-min_v))
    return cell


def create_arb_pool(pattern, best_match, clone_rate, mutate_rate):
    pool = []
    pool.append(create_cell(best_match['vector'], best_match['label']))
    num_clones = int(round(best_match['stimulation'] * clone_rate * mutate_rate))
    for i in xrange(num_clones):
        cell = create_cell(best_match['vector'], best_match['label'])
        pool.append(mutate_cell(cell, best_match))
    return pool


def competition_for_resournces(pool, clone_rate, max_res):
    for cell in pool:
        cell['resources'] = cell['stimulation'] * clone_rate
    pool.sort(key=lambda x: x['resources'])
    total_resources = sum(map(lambda x: x['resources'], pool))
    while total_resources > max_res:
        cell = pool.pop()
        total_resources -= cell['resources']


def refine_arb_pool(pool, pattern, stim_thresh, clone_rate, max_res):
    mean_stim, candidate = 0.0, None
    while mean_stim < stim_thresh:
        stimulate(pool, pattern)
        pool.sort(key=lambda x: x['stimulation'])
        candidate = pool[0]
        mean_stim = sum(map(lambda x: x['stimulation'], pool)) / len(pool)
        if mean_stim < stim_thresh:
            competition_for_resournces(pool, clone_rate, max_res)
            for i in xrange(len(pool)):
                cell = create_cell(pool[i]['vector'], pool[i]['label'])
                mutate_cell(cell, pool[i])
                pool.append(cell)
    return candidate


def add_candidate_to_memory_pool(candidate, best_match, mem_cells):
    if candidate['stimulation'] > best_match['stimulation']:
        mem_cells.append(candidate)


def classify_pattern(mem_cells, pattern):
    stimulate(mem_cells, pattern)
    mem_cells.sort(key=lambda x: x['stimulation'])
    return mem_cells[0]


def train_system(mem_cells, domain, num_patterns, clone_rate, mutate_rate, stim_thresh, max_res):
    for i in xrange(num_patterns):
        pattern = generate_random_pattern(domain)
        best_match = get_most_stimulated_cell(mem_cells, pattern)
        if best_match['label'] != pattern['label']:
            mem_cells.append(create_cell(pattern['vector'], pattern['label']))
        elif best_match['stimulation'] < 1.0:
            pool = create_arb_pool(pattern, best_match, clone_rate, mutate_rate)
            cand = refine_arb_pool(pool,pattern, stim_thresh, clone_rate, max_res)
            add_candidate_to_memory_pool(cand, best_match, mem_cells)
        print " > iter=%d, mem_cells=%d" % (i+1, len(mem_cells))


def do_test_system(mem_cells, domain, num_trials=50):
    correct = 0
    for i in xrange(num_trials):
        pattern = generate_random_pattern(domain)
        best = classify_pattern(mem_cells, pattern)
        if best['label'] == pattern['label']:
            correct += 1
    print "Finished test with a score of %d/%d" % (correct, num_trials)
    return correct


def execute(domain, num_patterns, clone_rate, mutate_rate, stim_thresh, max_res):
    mem_cells = initialize_cells(domain)
    train_system(mem_cells, domain, num_patterns, clone_rate, mutate_rate, stim_thresh, max_res)
    do_test_system(mem_cells, domain)
    return mem_cells


def main():
    # problem configuration
    domain = {"A": [[0, 0.4999999], [0, 0.4999999]], "B": [[0.5, 1], [0.5, 1]]}
    num_patterns = 50
    # algorithm configuration
    clone_rate = 10
    mutate_rate = 2.0
    stim_thresh = 0.9
    max_res = 150
    # execute the algorithm
    execute(domain, num_patterns, clone_rate, mutate_rate, stim_thresh, max_res)


if __name__ == "__main__":
    main()

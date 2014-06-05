#!/usr/bin/env python

"""
Gene Expression Programming
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def binary_tournament(pop):
    from random import randrange

    i, j = randrange(len(pop)), randrange(len(pop))
    return iif(pop[i]['fitness'] < pop[j]['fitness'], pop[i], pop[j])


def point_mutation(grammar, genome, head_length, rate):
    from random import random, randrange

    child = ""
    for i in xrange(len(genome)):
        bit = chr(genome[i])
    if random() < rate:
        if i < head_length:
            selection = iif(random() < 0.5, grammar["FUNC"], grammar["TERM"])
        bit = selection[randrange(len(selection))]
    else:
        bit = grammar["TERM"][randrange(len(grammar["TERM"]))]

    child.append(bit)

    return child


def crossover(parent1, parent2, rate):
    from random import random

    if random() >= rate:
        return "" + parent1
    child = ""
    for i in xrange(len(parent1)):
        child.append(iif(random() < 0.5, parent1[i], parent2[i]))
    return child


def reproduce(grammar, selected, pop_size, p_crossover, head_length):
    children = []
    for i in xrange(len(selected)):
        p1 = selected[i]
        p2 = iif(i % 2 == 0, selected[i + 1], selected[i - 1])
    if i == len(selected) - 1:
        p2 = selected[0]
    child = {}
    child['genome'] = crossover(p1['genome'], p2['genome'], p_crossover)
    child['genome'] = point_mutation(grammar, child['genome'], head_length)
    children.append(child)
    return children


def random_genome(grammar, head_length, tail_length):
    from random import random, randrange

    s = ""
    for i in xrange(head_length):
        selection = iif(random() < 0.5, grammar["FUNC"], grammar["TERM"])
        s += selection[randrange(len(selection))]

    for i in xrange(tail_length):
        s += grammar["TERM"][randrange(len(grammar["TERM"]))]
    return s


def target_function(x):
    return x ** 4.0 + x ** 3.0 + x ** 2.0 + x


def sample_from_bounds(bounds):
    from random import random

    return bounds[0] + ((bounds[1] - bounds[0]) * random())


def cost(program, bounds, num_trials=30):
    errors = 0.0
    for i in xrange(num_trials):
        x = sample_from_bounds(bounds)
        expression, score = program.gsub("x", str(x)), 0.0
        score = eval(expression)
        if score is None or score == float('Inf'):
            return 9999999
        errors += abs(score - target_function(x))

    return errors / float(num_trials)


def mapping(genome, grammar):
    off, queue = 0, []
    root = {}
    root['node'] = chr(genome[off])
    off += 1
    queue.append(root)
    while len(queue) > 0:
        current = queue.pop()
        if current['node'] in grammar["FUNC"]:
            current['left'] = {}
            current['left']['node'] = chr(genome[off])
            off += 1
            queue.append(current['left'])
            current['right'] = {}
            current['right']['node'] = chr(genome[off])
            off += 1
            queue.append(current['right'])
    return root


def tree_to_string(exp):
    if exp['left'] is None or exp['right'] is None:
        return exp['node']
    left = tree_to_string(exp['left'])
    right = tree_to_string(exp['right'])
    return "(%s %s %s)" % (left, exp['node'], right)


def evaluate(candidate, grammar, bounds):
    candidate['expression'] = mapping(candidate['genome'], grammar)
    candidate['program'] = tree_to_string(candidate['expression'])
    candidate['fitness'] = cost(candidate['program'], bounds)


def search(grammar, bounds, h_length, t_length, max_gens, pop_size, p_cross):
    pop = [{'genome': random_genome(grammar, h_length, t_length)} for i in xrange(pop_size)]

    for c in pop:
        evaluate(c, grammar, bounds)
    pop.sort(key=lambda x: x['fitness'])
    best = pop[0]
    for gen in xrange(max_gens):
        selected = [binary_tournament(pop) for i in xrange(len(pop))]
        children = reproduce(grammar, selected, pop_size, p_cross, h_length)
        for c in children:
            evaluate(c, grammar, bounds)
        children.sort(key=lambda x: x['fitness'])
        if children[0]['fitness'] <= best['fitness']:
            best = children[0]
        pop = (children + pop)[0:pop_size]
    print " > gen=%d, f=%f, g=%s" % (gen, best['fitness'], str(best['genome']))

    return best


def main():
    # problem configuration
    grammar = {"FUNC": ["+", "-", "*", "/"], "TERM": ["x"]}
    bounds = [1.0, 10.0]
    # algorithm configuration
    h_length = 20
    t_length = h_length * (2 - 1) + 1
    max_gens = 150
    pop_size = 80
    p_cross = 0.85
    # execute the algorithm
    best = search(grammar, bounds, h_length, t_length, max_gens, pop_size, p_cross)
    print "Done! Solution: f=%f, program=%s" % (best['fitness'], str(best['program']))


if __name__ == "__main__":
    main()


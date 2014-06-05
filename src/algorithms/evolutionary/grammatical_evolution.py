#!/usr/bin/env python

"""
Grammatical Evolution
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def binary_tournament(pop):
    from random import randrange
    i, j = randrange(len(pop)), randrange(len(pop))
    while j == i:
        j = randrange(len(pop))
    return iif(pop[i]['fitness'] < pop[j]['fitness'], pop[i], pop[j])


def point_mutation(bitstring, rate):
    from random import random
    child = ""
    for i in xrange(len(bitstring)):
        bit = chr(bitstring[i])
        child.append(iif(random()<rate, iif(bit == '1', "0", "1"), bit))

    return child


def one_point_crossover(parent1, parent2, codon_bits, p_cross=0.30):
    from random import random, randrange
    if random() >= p_cross:
        return "" + parent1['bitstring']
    cut = randrange(min(len(parent1['bitstring']), len(parent2['bitstring'])/codon_bits))
    cut *= codon_bits
    p2size = len(parent2['bitstring'])
    return parent1['bitstring'][0:cut]+parent2['bitstring'][cut:p2size]


def codon_duplication(bitstring, codon_bits, rate):
    from random import random, randrange
    if random() >= rate:
        return bitstring
    codons = len(bitstring)/codon_bits
    return bitstring + bitstring[randrange(codons)*codon_bits, codon_bits]


def codon_deletion(bitstring, codon_bits, rate):
    from random import random, randrange
    if random() >= rate:
        return bitstring
    codons = len(bitstring)/codon_bits
    off = randrange(codons)*codon_bits
    return bitstring[0:off] + bitstring[off+codon_bits:len(bitstring)]


def reproduce(selected, pop_size, p_cross, codon_bits):
    children = []
    for i in len(selected):
        p1 = selected[i]
        p2 = iif(i % 2 == 0, selected[i+1], selected[i-1])
        if i == len(selected) - 1:
            p2 = selected[0]
        child = {}
        child['bitstring'] = one_point_crossover(p1, p2, codon_bits, p_cross)
        child['bitstring'] = codon_deletion(child['bitstring'], codon_bits)
        child['bitstring'] = codon_duplication(child['bitstring'], codon_bits)
        child['bitstring'] = point_mutation(child['bitstring'])
        children.append(child)
        if len(children) == pop_size:
            break

    return children


def random_bitstring(num_bits):
    from random import random
    return "".join(iif(random < 0.5, "1", "0") for i in xrange(num_bits))


def decode_integers(bitstring, codon_bits):
    ints = []
    for off in xrange(len(bitstring)/codon_bits):
        codon = bitstring[off*codon_bits, codon_bits]
        sum = 0
        for i in xrange(len(codon)):
            sum += iif(chr(codon[i]) == '1', 1, 0) * (2 ** i);
        ints.append(sum)
    return ints


def map(grammar, integers, max_depth):
    done, offset, depth = False, 0, 0
    symbolic_string = grammar["S"]

    for key in grammar.keys:
        for k in symbolic_string.gsub(key):
            #done = False
            set = iif(k == "EXP" and depth >= max_depth-1, grammar["VAR"], grammar[k])
            integer = integers[offset] % len(set)
            offset = iif(offset == len(integers)-1, 0, offset+1)
            symbolic_string[k] = set[integer]

        depth += 1

    return symbolic_string


def target_function(x):
    return x**4.0 + x**3.0 + x**2.0 + x


def sample_from_bounds(bounds):
    from random import random
    return bounds[0] + ((bounds[1] - bounds[0]) * random())


def cost(program, bounds, num_trials=30):
    if program.trim() == "INPUT":
        return 9999999
    sum_error = 0.0
    for i in xrange(num_trials):
        x = sample_from_bounds(bounds)
        expression = program.gsub("INPUT", str(x))
        score = eval(expression)
        if score is None or score == float('Inf'):
            return 9999999
        sum_error += abs(score - target_function(x))

    return sum_error / float(num_trials)


def evaluate(candidate, codon_bits, grammar, max_depth, bounds):
    candidate['integers'] = decode_integers(candidate['bitstring'], codon_bits)
    candidate['program'] = map(grammar, candidate['integers'], max_depth)
    candidate['fitness'] = cost(candidate['program'], bounds)


def search(max_gens, pop_size, codon_bits, num_bits, p_cross, grammar, max_depth, bounds):
    pop = [{'bitstring': random_bitstring(num_bits)} for i in xrange(pop_size)]
    for c in pop:
        evaluate(c,codon_bits, grammar, max_depth, bounds)
    pop.sort(key=lambda x: x['fitness'])
    best = pop[0]
    for gen in xrange(max_gens):
        selected = [binary_tournament(pop) for i in xrange(pop_size)]
        children = reproduce(selected, pop_size, p_cross,codon_bits)
        for c in children:
            evaluate(c, codon_bits, grammar, max_depth, bounds)
        children.sort(key=lambda x: x['fitness'])
        if children[0]['fitness'] <= best['fitness']:
            best = children[0]
        union = children + pop
        union.sort(key=lambda x: x['fitness'])
        pop = union[0:pop_size]
        print " > gen=%d, f=%f, s=%s" % (gen, best['fitness'], best['bitstring'])
        if best['fitness'] == 0.0:
            break

    return best


def main():
    # problem configuration
    grammar = {"S": "EXP",
        "EXP": [" EXP BINARY EXP ", " (EXP BINARY EXP) ", " VAR "],
        "BINARY": ["+", "-", "/", "*" ],
        "VAR": ["INPUT", "1.0"]}
    bounds = [1, 10]
    # algorithm configuration
    max_depth = 7
    max_gens = 50
    pop_size = 100
    codon_bits = 4
    num_bits = 10*codon_bits
    p_cross = 0.30
    # execute the algorithm
    best = search(max_gens, pop_size, codon_bits, num_bits, p_cross, grammar, max_depth, bounds)
    print "Done! Solution: f=%f, s=%s" % (best['fitness'], str(best['program']))

if __name__ == "__main__":
    main()


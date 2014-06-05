#!/usr/bin/env python


def random_vector(minmax):
    import random

    return map(lambda x: x[0] + (x[1] - x[0]) * random.random(), minmax)


def generate_random_pattern(domain):
    from random import randrange

    classes = domain.keys()
    selected_class = randrange(len(classes))
    pattern = {'label': classes[selected_class]}
    pattern['vector'] = random_vector(domain[classes[selected_class]])
    return pattern


def initialize_vectors(domain, num_vectors):
    from random import randrange

    classes = domain.keys()
    codebook_vectors = []
    for i in xrange(num_vectors):
        selected_class = randrange(len(classes))
        codebook = {'label': classes[selected_class], 'vector': random_vector([[0, 1], [0, 1]])}
        codebook_vectors.append(codebook)
    return codebook_vectors


def euclidean_distance(c1, c2):
    import math

    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)


def get_best_matching_unit(codebook_vectors, pattern):
    best, b_dist = None, None
    for codebook in codebook_vectors:
        dist = euclidean_distance(codebook['vector'], pattern['vector'])
        if b_dist is None or dist < b_dist:
            best, b_dist = codebook, dist
    return best


def update_codebook_vector(bmu, pattern, lrate):
    for i in xrange(len(bmu['vector'])):
        v = bmu['vector'][i]
        error = pattern['vector'][i] - bmu['vector'][i]
        if bmu['label'] == pattern['label']:
            bmu['vector'][i] += lrate * error
        else:
            bmu['vector'][i] -= lrate * error


def train_network(codebook_vectors, domain, iterations, learning_rate):
    for iter in xrange(iterations):
        pat = generate_random_pattern(domain)
        bmu = get_best_matching_unit(codebook_vectors, pat)
        lrate = learning_rate * (1.0 - (float(iter) / iterations))
        if iter % 10 == 0:
            print "> iter=%d, got=%s, exp=%s" % (iter, bmu['label'], pat['label'])
        update_codebook_vector(bmu, pat, lrate)


def test_network(codebook_vectors, domain, num_trials=100):
    correct = 0
    for i in xrange(num_trials):
        pattern = generate_random_pattern(domain)
        bmu = get_best_matching_unit(codebook_vectors, pattern)
        if bmu['label'] == pattern['label']:
            correct += 1
    print "Done. Score: %d/%d" % (correct, num_trials)
    return correct


def execute(domain, iterations, num_vectors, learning_rate):
    codebook_vectors = initialize_vectors(domain, num_vectors)
    train_network(codebook_vectors, domain, iterations, learning_rate)
    test_network(codebook_vectors, domain)
    return codebook_vectors


def main():
    # problem configuration
    domain = {"A": [[0, 0.4999999], [0, 0.4999999]], "B": [[0.5, 1], [0.5, 1]]}
    # algorithm configuration
    learning_rate = 0.3
    iterations = 1000
    num_vectors = 20
    # execute the algorithm
    execute(domain, iterations, num_vectors, learning_rate)


if __name__ == "__main__":
    main()


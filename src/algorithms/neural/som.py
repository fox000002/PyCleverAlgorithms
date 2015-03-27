#!/usr/bin/env python

"""
Self-Organized Map
"""


def random_vector(minmax):
    import random
    return map(lambda x: x[0] + (x[1] - x[0]) * random.random(), minmax)


def initialize_vectors(domain, width, height):
    codebook_vectors = []
    for x in range(width):
        for y in range(height):
            codebook = {'vector': random_vector(domain), 'coord': [x, y]}
            codebook_vectors.append(codebook)
    return codebook_vectors


def euclidean_distance(c1, c2):
    import math
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)


def get_best_matching_unit(codebook_vectors, pattern):
    best, b_dist = None, None
    for codebook in codebook_vectors:
        dist = euclidean_distance(codebook['vector'], pattern)
        if b_dist is None or dist < b_dist:
            best, b_dist = codebook, dist
    return [best, b_dist]


def get_vectors_in_neighborhood(bmu, codebook_vectors, neigh_size):
    neighborhood = []
    for other in codebook_vectors:
        if euclidean_distance(bmu['coord'], other['coord']) <= neigh_size:
            neighborhood.append(other)
    return neighborhood


def update_codebook_vector(codebook, pattern, lrate):
    for i in range(len(codebook['vector'])):
        error = pattern[i]-codebook['vector'][i]
        codebook['vector'][i] += lrate * error


def train_network(vectors, shape, iterations, l_rate, neighborhood_size):
    for iteration in range(iterations):
        pattern = random_vector(shape)
        lrate = l_rate * (1.0-(float(iteration)/float(iterations)))
        neigh_size = neighborhood_size * (1.0-(float(iteration)/float(iterations)))
        bmu, dist = get_best_matching_unit(vectors, pattern)
        neighbors = get_vectors_in_neighborhood(bmu, vectors, neigh_size)
        for node in neighbors:
            update_codebook_vector(node, pattern, lrate)
        print(">training: neighbors=%d, bmu_dist=%f" % (len(neighbors), dist))


def summarize_vectors(vectors):
    min_max = [[1, 0]] * len(vectors[0]['vector'])
    for c in vectors:
        for i in range(len(c['vector'])):
            v = c['vector'][i]
            if v < min_max[i][0]:
                min_max[i][0] = v
            if v > min_max[i][1]:
                min_max[i][1] = v

    s = ""
    for i in range(len(min_max)):
        bounds = min_max[i]
        s += "\n%d=%s" % (i, str(bounds))
    print("Vector details: %s" % s)
    return min_max


def do_test_network(codebook_vectors, shape, num_trials=100):
    error = 0.0
    for i in range(num_trials):
        pattern = random_vector(shape)
        bmu, dist = get_best_matching_unit(codebook_vectors, pattern)
        error += dist
    error /= float(num_trials)
    print("Finished, average error=%f" % error)
    return error


def execute(domain, shape, iterations, l_rate, neigh_size, width, height):
    vectors = initialize_vectors(domain, width, height)
    summarize_vectors(vectors)
    train_network(vectors, shape, iterations, l_rate, neigh_size)
    do_test_network(vectors, shape)
    summarize_vectors(vectors)
    return vectors


def main():
    # problem configuration
    domain = [[0.0, 1.0], [0.0, 1.0]]
    shape = [[0.3, 0.6], [0.3, 0.6]]
    # algorithm configuration
    iterations = 100
    l_rate = 0.3
    neigh_size = 5
    width, height = 4, 5
    # execute the algorithm
    execute(domain, shape, iterations, l_rate, neigh_size, width, height)


if __name__ == "__main__":
    main()

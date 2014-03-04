#!/usr/bin/env python


def random_vector(minmax):
    import random

    return map(lambda x: x[0] + (x[1] - x[0]) * random.random(), minmax)


def initialize_vectors(domain, width, height):
    codebook_vectors = []
    for x in xrange(0, width):
        for y in xrange(0, height):
            codebook = {}
            codebook['vector'] = random_vector(domain)
            codebook['coord'] = [x, y]
            codebook_vectors.append(codebook)
    return codebook_vectors


def euclidean_distance(c1, c2):
    pass


def get_best_matching_unit(codebook_vectors, pattern):
    pass


def get_vectors_in_neighborhood(bmu, codebook_vectors, neigh_size):
    pass


def update_codebook_vector(codebook, pattern, lrate):
    pass


def train_network(vectors, shape, iterations, l_rate, neighborhood_size):
    pass


def summarize_vectors(vectors):
    pass


def test_network(codebook_vectors, shape, num_trials=100):
    pass


def execute(domain, shape, iterations, l_rate, neigh_size, width, height):
    pass


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


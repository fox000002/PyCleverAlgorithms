#!/usr/bin/env python


def objective1(v):
    return sum(map(lambda x: x ** 2, v))


def objective2(v):
    return sum(map(lambda x: (x - 2.0) ** 2, v))


def decode(bitstring, search_space, bits_per_param):
    pass


def random_bitstring(num_bits):
    pass


def point_mutation(bitstring, rate):
    pass


def binary_tournament(pop):
    pass


def crossover(parent1, parent2, rate):
    pass


def reproduce(selected, pop_size, p_cross):
    pass


def calculate_objectives(pop, search_space, bits_per_param):
    pass


def dominates(p1, p2):
    pass


def weighted_sum(x):
    pass


def euclidean_distance(c1, c2):
    pass


def calculate_dominated(pop):
    pass


def calculate_raw_fitness(p1, pop):
    pass


def calculate_density(p1, pop):
    pass


def calculate_fitness(pop, archive, search_space, bits_per_param):
    pass


def environmental_selection(pop, archive, archive_size):
    pass


def search(search_space, max_gens, pop_size, archive_size, p_cross, bits_per_param=16):
    pass


def main():
    # problem configuration
    problem_size = 1
    search_space = [[-10, 10]] * problem_size
    # algorithm configuration
    max_gens = 50
    pop_size = 80
    archive_size = 40
    p_cross = 0.90
    # execute the algorithm
    pop = search(search_space, max_gens, pop_size, archive_size, p_cross)
    print "done!"


if __name__ == "__main__":
    main()


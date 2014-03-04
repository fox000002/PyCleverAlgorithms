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


def crossover(parent1, parent2, rate):
    pass


def reproduce(selected, pop_size, p_cross):
    pass


def calculate_objectives(pop, search_space, bits_per_param):
    pass


def dominates(p1, p2):
    pass


def fast_nondominated_sort(pop):
    pass


def calculate_crowding_distance(pop):
    pass


def crowded_comparison_operator(x, y):
    pass


def better(x, y):
    pass


def select_parents(fronts, pop_size):
    pass


def weighted_sum(x):
    pass


def search(search_space, max_gens, pop_size, p_cross, bits_per_param=16):
    pass


def main():
    # problem configuration
    problem_size = 1
    search_space = [[-10, 10]] * problem_size
    # algorithm configuration
    max_gens = 50
    pop_size = 100
    p_cross = 0.98
    # execute the algorithm
    pop = search(search_space, max_gens, pop_size, p_cross)
    print "done!"


if __name__ == "__main__":
    main()


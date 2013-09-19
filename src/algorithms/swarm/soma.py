#!/usr/bin/env python

# Self-Organizing Migrating Algorithm

def objective_function(v):
    return sum(map(lambda x : x**2, v))

def random_vector(minmax):
    import random
    return map(lambda x : x[0] + (x[1]-x[0]) * random.random(), minmax)

def main():
    # problem configuration
    problem_size = 3
    search_space = [[-5, +5]] * problem_size
    # algorithm configuration
    max_gens = 200
    pop_size = 10*problem_size
    weightf = 0.8
    crossf = 0.9
    perturbation = 0.3
    #


if __name__ == "__main__":
    main()


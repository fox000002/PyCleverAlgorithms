#!/usr/bin/env python

"""
"""

def rand_in_bounds(min, max):
    import random
    return random.randrange(min, max)

def print_program(node):
    pass

def eval_program(node, map):
    pass

def generate_random_program(max, funcs, terms, depth=0):
    pass

def count_nodes(node):
    pass

def target_function(input):
    pass

def fitness(program, num_trails=20):
    pass

def tournament_selection(pop, bouts):
    pass

def replace_node(node, replacement, node_num, cur_node=0):
    pass

def copy_program(node):
    pass

def get_node(node, node_num, current_node=0):
    pass

def prune(node, max_depth, terms, depth=0):
    pass

def crossover(parent1, parent2, max_depth, terms):
    pass

def mutation(parent, max_depth, functs, terms):
    pass

def search(max_gens, pop_size, max_depth, bouts, p_repro, p_cross, p_mut, functs, terms):
    pass

def main():
    pass

if __name__ == "__main__":
    main()

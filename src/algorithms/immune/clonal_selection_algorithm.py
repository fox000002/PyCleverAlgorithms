#!/usr/bin/env python

def objective_function(v):
    return sum(map(lambda x : x**2, v))

def decode(bitstring, search_space, bits_per_param):
	pass

def evaluate(pop, search_space, bits_per_param):
	pass

def random_bitstring(num_bits):
    from random import sample
    return map(lambda x: iif(x<50, '1', '0'), sample(range(100), num_bits))

def point_mutation(bitstring, rate):
	pass

def calculate_mutation_rate(antibody, mutation_factor=-2.5):
	pass

def num_clones(pop_size, clone_factor):
	pass

def calculate_affinity(pop):
	pass

def clone_and_hypermutate(pop, clone_factor):
	pass

def random_insertion(search_space, pop, num_rand, bits_per_param):
	pass

def search(search_space, max_gens, pop_size, clone_factor, num_rand, bits_per_param=16):
	return {'cost' : 0.0, 'vector' : []}

def main():
    # problem configuration
    problem_size = 2
    search_space = [[-5,5]] * problem_size
    # algorithm configuration
    max_gens = 100
    pop_size = 100
    clone_factor = 0.1
    num_rand = 2
    # execute the algorithm
    best = search(search_space, max_gens, pop_size, clone_factor, num_rand)
    print "done! Solution: f=%f, s=%s" % (best['cost'], str(best['vector']))

if __name__ == "__main__":
    main()


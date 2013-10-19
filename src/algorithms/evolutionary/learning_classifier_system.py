#!/usr/bin/env python

def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]

def neg(bit):
	return iif(bit==1, 0, 1)

def target_function(s):
	ints = [int(c) for x in s]
	x0, x1, x2, x3, x4, x5 = ints
	return neg(x0) * neg(x1) * x2 + neg(x0)*x1*x3 + x0 * neg(x1)*x4 + x0*x1*x5

def new_classifier(condition, action, gen, p1=10.0, e1=0.0, f1=10.0):
	pass

def copy_classifier(parent):
	pass

def random_bitstring(num_bits):
    from random import sample
    return map(lambda x: iif(x<50, '1', '0'), sample(range(100), num_bits))

def calculate_deletion_vote(classifier, pop, del_thresh, f_thresh=0.1):
	pass

def delete_from_pop(pop, pop_size, del_thresh=20.0):
	pass

def generate_random_classifier(input, actions, gen, rate=1.0/3.0):
	pass

def does_match(input, condition):
	pass

def get_actions(pop):
	pass

def generate_match_set(input, pop, all_actions, gen, pop_size):
	pass

def generate_prediction(match_set):
	pass

def select_action(preditions, p_explorer=false):
	pass

def update_set(action_set, reward, beta=0.2):
	pass

def update_fitness(action_set, min_error=10, l_rate=0.2, alpha=0.1, v=-5.0):
	pass

def can_run_genetic_algorithm(action_set, gen, ga_freq):
	pass

def binary_tournament(pop):
	pass

def mutation(cl, action_set, input, rate=0.04):
	pass

def uniform_crossover(parent1, parent2):
	pass

def insert_in_pop(cla, pop):
	pass

def crossover(c1, c2, p1, p2):
	pass

def run_ga(actions, pop, action_set, input, gen, pop_size, crate=0.8):
	pass

def train_model(pop_size, max_gens, actions, ga_freq):
	pass

def test_model(system, num_trials=50):
	pass

def execute(pop_size, max_gens, actions, ga_freq):
	pass

def main():
    # problem configuration
    all_actions = ['0', '1']
    # algorithm configuration
    max_gens, pop_size = 5000, 200
    ga_freq = 25
    # execute the algorithm
    execute(pop_size, max_gens, all_actions, ga_freq)

if __name__ == "__main__":
    main()


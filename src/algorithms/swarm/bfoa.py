#!/usr/bin/env python

# Bacterial Foraging Optimization Algorithm 

def objective_function(v):
    return sum(map(lambda x : x**2, v))

def random_vector(minmax):
    import random
    return map(lambda x : x[0] + (x[1]-x[0]) * random.random(), minmax)

def generate_random_direction(problem_size):
	pass

def compute_cell_interaction(cell, cells, d, w):
	pass

def attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep):
	pass

def evaluate(cell, cells, d_attr, w_attr, h_rep, w_rep):
	pass

def tumble_cell(search_space, cell, step_size):
	pass

def chemotaxis(cells, search_space, chem_steps, swim_length, step_size, 
    d_attr, w_attr, h_rep, w_rep):
	pass

def search(search_space, pop_size, elim_disp_steps, repro_steps, 
    chem_steps, swim_length, step_size, d_attr, w_attr, h_rep, w_rep, 
    p_eliminate):
	return { 'cost' : 0, 'vector' : [] }

def main():
    # problem configuration
    problem_size = 2
    search_space = [[-5, 5]] * problem_size
    # algorithm configuration
    pop_size = 50
    step_size = 0.1 # Ci
    elim_disp_steps = 1 # Ned
    repro_steps = 4 # Nre
    chem_steps = 70 # Nc
    swim_length = 4 # Ns
    p_eliminate = 0.25 # Ped
    d_attr = 0.1
    w_attr = 0.2 
    h_rep = d_attr
    w_rep = 10
    # execute the algorithm
    best = search(search_space, pop_size, elim_disp_steps, repro_steps, 
      chem_steps, swim_length, step_size, d_attr, w_attr, h_rep, w_rep, 
      p_eliminate)
    print "done! Solution: c=%f, v=%s" % (best['cost'], str(best['vector']))

if __name__ == "__main__":
    main()


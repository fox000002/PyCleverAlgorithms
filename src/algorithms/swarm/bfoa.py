#!/usr/bin/env python

"""
Bacterial Foraging Optimization Algorithm
"""


def objective_function(v):
    return sum(map(lambda x: x**2, v))


def random_vector(minmax):
    import random
    return map(lambda x: x[0] + (x[1]-x[0]) * random.random(), minmax)


def generate_random_direction(problem_size):
    bounds = [[-1.0, 1.0]] * problem_size
    return random_vector(bounds)


def compute_cell_interaction(cell, cells, d, w):
    from math import exp
    sum = 0.0
    for other in cells:
        diff = 0.0
        for i in xrange(len(cell['vector'])):
            diff += (cell['vector'][i] - other['vector'][i])**2.0
        sum += d * exp(w * diff)
    return sum


def attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep):
    attract = compute_cell_interaction(cell, cells, -d_attr, -w_attr)
    repel = compute_cell_interaction(cell, cells, h_rep, -w_rep)
    return attract + repel


def evaluate(cell, cells, d_attr, w_attr, h_rep, w_rep):
    cell['cost'] = objective_function(cell['vector'])
    cell['inter'] = attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep)
    cell['fitness'] = cell['cost'] + cell['inter']


def tumble_cell(search_space, cell, step_size):
    step = generate_random_direction(len(search_space))
    vector = [0] * len(search_space)
    for i in xrange(len(vector)):
        vector[i] = cell['vector'][i] + step_size * step[i]
        if vector[i] < search_space[i][0]:
            vector[i] = search_space[i][0]
        if vector[i] > search_space[i][1]:
            vector[i] = search_space[i][1]
    return {'vector': vector}


def chemotaxis(cells, search_space, chem_steps, swim_length, step_size, 
    d_attr, w_attr, h_rep, w_rep):
    best = None
    for j in xrange(chem_steps):
        moved_cells = []
        for i in xrange(len(cells)):
            cell = cells[i]
            sum_nutrients = 0.0
            evaluate(cell, cells, d_attr, w_attr, h_rep, w_rep)
            if best is None or cell['cost'] < best['cost']:
                best = cell
            sum_nutrients += cell['fitness']
            for m in xrange(swim_length):
                new_cell = tumble_cell(search_space, cell, step_size)
                evaluate(new_cell, cells, d_attr, w_attr, h_rep, w_rep)
                if cell['cost'] < best['cost']:
                    best = cell
                if new_cell['fitness'] > cell['fitness']:
                    break
                cell = new_cell
                sum_nutrients += cell['fitness']
            cell['sum_nutrients'] = sum_nutrients
            moved_cells.append(cell)
        print "  >> chemo=%d, f=%f, cost=%f" % (j, best['fitness'], best['cost'])
        cells = moved_cells
    return [best, cells]


def search(search_space, pop_size, elim_disp_steps, repro_steps,
    chem_steps, swim_length, step_size, d_attr, w_attr, h_rep, w_rep, 
    p_eliminate):
    import random
    cells = [{'vector': random_vector(search_space)}] * pop_size
    best = None
    for l in xrange(elim_disp_steps):
        for k in xrange(repro_steps):
            c_best, cells = chemotaxis(cells, search_space, chem_steps, swim_length, step_size, d_attr, w_attr, h_rep, w_rep)
            if best is None or c_best['cost'] < best['cost']:
                best = c_best
            print " > best fitness=%f, cost=%f" % (best['fitness'], best['cost'])
            cells.sort(key=lambda x: x['sum_nutrients'])
            cells = cells[0](pop_size/2) + cells[0](pop_size/2)
    for cell in cells:
        if random.random() <= p_eliminate:
            cell['vector'] = random_vector(search_space)
    return best


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


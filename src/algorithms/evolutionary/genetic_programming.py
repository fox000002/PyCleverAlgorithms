#!/usr/bin/env python

"""
Genetic Programming
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def rand_in_bounds(min_value, max_value):
    import random
    return random.randrange(min_value, max_value)


def print_program(node):
    if type(node) != 'list':
        return node
    return '(%s %s %s)' % (node[0], print_program(node[1]), print_program(node[2]))


def eval_program(node, map_value):
    if type(node) != 'list':
        if not map_value[node] is None:
            return float(map_value[node])
        return float(node)
    arg1, arg2 = eval_program(node[1], map_value), eval_program(node[2], map_value)
    if node[0] == '/' and arg2 == 0.0:
        return 0
    return eval("%f %s %f" % (arg1, node[0], arg2))


def generate_random_program(max_value, funcs, terms, depth=0):
    import random
    if depth == max_value-1 or (depth > 1 and random.random() < 0.1):
        t = terms[random.randrange(len(terms))]
        return iif((t == 'R'), rand_in_bounds(-5.0, +5.0), t)
    depth += 1
    arg1 = generate_random_program(max_value, funcs, terms, depth)
    arg2 = generate_random_program(max_value, funcs, terms, depth)
    return [funcs[random.randrange(len(funcs))], arg1, arg2]


def count_nodes(node):
    if type(node) != 'list':
        return 1
    a1 = count_nodes(node[1])
    a2 = count_nodes(node[2])
    return a1+a2+1


def target_function(input_value):
    return input_value**2 + input_value + 1


def fitness(program, num_trials=20):
    sum_error = 0.0
    for i in xrange(num_trials):
        input_value = rand_in_bounds(-1.0, 1.0)
        error = eval_program(program, {'X': input_value}) - target_function(input_value)
        sum_error += abs(error)
    return sum_error / float(num_trials)


def tournament_selection(pop, bouts):
    import random
    selected = [pop[random.randrange(len(pop))]] * bouts
    selected.sort(lambda x: x['fitness'])
    return selected[0]


def replace_node(node, replacement, node_num, cur_node=0):
    if cur_node == node_num:
        return [replacement, (cur_node+1)]
    cur_node += 1
    if type(node) != 'list':
        return [node, cur_node]
    a1, cur_node = replace_node(node[1], replacement, node_num, cur_node)
    a2, cur_node = replace_node(node[2], replacement, node_num, cur_node)
    return [[node[0], a1, a2], cur_node]


def copy_program(node):
    if type(node) != 'list':
        return node
    return [node[0], copy_program(node[1]), copy_program(node[2])]


def get_node(node, node_num, current_node=0):
    if current_node == node_num:
        return node, (current_node+1)
    current_node += 1
    if type(node) != 'list':
        return None
    a1, current_node = get_node(node[1], node_num, current_node)
    if not a1 is None:
        return a1, current_node
    a2, current_node = get_node(node[2], node_num, current_node)
    if not a2 is None:
        return a2, current_node
    return None, current_node


def prune(node, max_depth, terms, depth=0):
    from random import randrange
    if depth == max_depth-1:
        t = terms[randrange(len(terms))]
        return iif(t == 'R', rand_in_bounds(-5.0, +5.0), t)
    depth += 1
    if type(node) != 'list':
        return node
    a1 = prune(node[1], max_depth, terms, depth)
    a2 = prune(node[2], max_depth, terms, depth)
    return [node[0], a1, a2]


def crossover(parent1, parent2, max_depth, terms):
    import random
    pt1, pt2 = random.randrange(count_nodes(parent1)-2)+1, random.randrange(count_nodes(parent2)-2)+1
    tree1, c1 = get_node(parent1, pt1)
    tree2, c2 = get_node(parent2, pt2)
    child1, c1 = replace_node(parent1, copy_program(tree2), pt1)
    child1 = prune(child1, max_depth, terms)
    child2, c2 = replace_node(parent2, copy_program(tree1), pt2)
    child2 = prune(child2, max_depth, terms)
    return [child1, child2]


def mutation(parent, max_depth, functions, terms):
    import random
    random_tree = generate_random_program(max_depth/2, functions, terms)
    point = random.randrange(count_nodes(parent))
    child, count = replace_node(parent, random_tree, point)
    child = prune(child, max_depth, terms)
    return child


def search(max_gens, pop_size, max_depth, bouts, p_reproduce, p_cross, p_mutate, functions, terms):
    import random
    population = [{} for i in xrange(pop_size)]
    for i in xrange(pop_size):
        population[i]['prog'] = generate_random_program(max_depth, functions, terms)
    for c in population:
        c['fitness'] = fitness(c['prog'])
    best = population.sort(lambda x: x['fitness'])[0]
    for gen in xrange(max_gens):
        children = []
        while len(children) < pop_size:
            operation = random.random()
        p1 = tournament_selection(population, bouts)
        c1 = {}
        if operation < p_reproduce:
            c1['prog'] = copy_program(p1['prog'])
        else:
            if operation < p_reproduce+p_cross:
                p2 = tournament_selection(population, bouts)
                c2 = {}
                c1['prog'], c2['prog'] = crossover(p1['prog'], p2['prog'], max_depth, terms)
                children.append(c2)
            else:
                if operation < p_reproduce+p_cross+p_mutate:
                    c1['prog'] = mutation(p1['prog'], max_depth, functions, terms)
        if len(children) < pop_size:
            children.append(c1)
        for c in children:
            c['fitness'] = fitness(c['prog'])
        population = children
        population.sort(lambda x: x['fitness'])
        if population[0]['fitness'] <= best['fitness']:
            best = population[0]
        print " > gen %d, fitness=%f" % (gen, best['fitness'])
        if best['fitness'] == 0:
            break
    return best


def main():
    # problem configuration
    terms = ['X', 'R']
    functions = ['+', '-', '*', '/']
    # algorithm configuration
    max_gens = 100
    max_depth = 7
    pop_size = 100
    bouts = 5
    p_reproduce = 0.08
    p_cross = 0.90
    p_mutate = 0.02
    # execute the algorithm
    best = search(max_gens, pop_size, max_depth, bouts, p_reproduce, p_cross, p_mutate, functions, terms)
    print "done! Solution: f=%f, %s" % (best['fitness'], print_program(best['prog']))

if __name__ == "__main__":
    main()

#!/usr/bin/env python

"""
Non-dominated Sorting Genetic Algorithm II (NSGA II)

Encoding approach: real (simulated binary crossover and polynomial mutation)

"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective1(v):
    return sum(map(lambda x: x ** 2, v))


def objective2(v):
    return sum(map(lambda x: (x - 2.0) ** 2, v))


def random_vector(min_max):
    from random import uniform
    return map(lambda x: uniform(x[0], x[1]), min_max)


def polynomial_mutation(v, search_space, rate):
    from random import random
    n = len(v)
    dm = 2
    newv = v[:]
    for i in xrange(n):
        k = random()
        if k < rate:
            ri = random()
            si = iif(ri < 0.5, (2*ri)**(1/(dm+1))-1, 1-(2-2*ri)**(1/(dm+1)))
            newv[i] += (search_space[i][1]-search_space[i][0])*si
    return newv


def crossover(parent1, parent2, rate):
    from random import random
    dc = 2
    n = len(parent1['vector'])
    children = [
        {'vector': parent1['vector'][:]},
        {'vector': parent1['vector'][:]}
    ]
    if random() < rate:
        for i in xrange(n):
            mu = random()
            beta = iif(mu <= 0.5, (2*mu)**(1/(dc+1)), (2-2*mu)**(-1/(dc+1)))
            children[0]['vector'][i] = (parent1['vector'][i]+parent2['vector'][i])/2 + beta*(parent1['vector'][i]-parent2['vector'][i])
            children[1]['vector'][i] = (parent1['vector'][i]+parent2['vector'][i])/2 - beta*(parent1['vector'][i]-parent2['vector'][i])

    return children


def reproduce(selected, pop_size, search_space, p_cross):
    newPop = []
    for i, p1 in enumerate(selected):
        if i % 2 == 1:  # skip even items
            continue
        if i == len(selected)-1:
            p2 = selected[0]
        else:
            p2 = iif(i % 2 == 0, selected[i+1], selected[i-1])
        children = crossover(p1, p2, p_cross)
        children[0]['vector'] = polynomial_mutation(children[0]['vector'], search_space, 0.1)
        children[1]['vector'] = polynomial_mutation(children[1]['vector'], search_space, 0.1)
        newPop.append(children[0])
        if len(newPop) >= pop_size:
            break
        newPop.append(children[1])
        if len(newPop) >= pop_size:
            break
    return newPop


def calculate_objectives(pop):
    for p in pop:
        p['objectives'] = [objective1(p['vector']), objective2(p['vector'])]


def dominates(p1, p2):
    for i in xrange(len(p1['objectives'])):
        if p1['objectives'][i] > p2['objectives'][i]:
            return False
    return True


def fast_nondominated_sort(pop):
    fronts = []
    first_front = []
    count = 0
    for p1 in pop:
        count += 1
        p1['dom_count'] = 0
        p1['dom_set'] = []
        for p2 in pop:
            if dominates(p1, p2):
                p1['dom_set'].append(p2)
            elif dominates(p2, p1):
                p1['dom_count'] += 1
        if p1['dom_count'] == 0:
            p1['rank'] = 0
            first_front.append(p1)
    fronts.append(first_front)
    curr = 0
    while True:
        next_front = []
        for p1 in fronts[curr]:
            for p2 in p1['dom_set']:
                p2['dom_count'] -= 1
                if p2['dom_count'] == 0:
                    p2['rank'] = curr + 1
                    next_front.append(p2)
        curr += 1
        if len(next_front) > 0:
            fronts.append(next_front)
        if curr >= len(fronts):
            break
    return fronts


def calculate_crowding_distance(pop):
    for p in pop:
        p['dist'] = 0.0
    num_obs = len(pop[0]['objectives'])
    for i in xrange(num_obs):
        min_v = min(pop, key=lambda x: x['objectives'][i])
        max_v = max(pop, key=lambda x: x['objectives'][i])
        rge = max_v['objectives'][i] - min_v['objectives'][i]
        # pop[0]['dist'], pop[-1]['dist'] = 1.0/0.0, 1.0/0.0
        if rge == 0.0:
            continue
        for j in xrange(1, len(pop)-1):
            pop[j]['dist'] += (pop[j+1]['objectives'][i]-pop[j-1]['objectives'][i])/rge


def crowded_comparison_operator(x, y):
    return iif(x['rank'] == y['rank'], cmp(y['dist'], x['dist']), cmp(x['rank'], y['rank']))


def better(x, y):
    if 'dist' in x and x['rank'] == y['rank']:
        return iif(x['dist'] > y['dist'], x, y)
    return iif(x['rank'] < y['rank'], x, y)


def select_parents(fronts, pop_size):
    for f in fronts:
        calculate_crowding_distance(f)
    offspring = []
    last_front = 0
    for front in fronts:
        if len(offspring) + len(front) > pop_size:
            break
        for p in front:
            offspring.append(p)
        last_front += 1
    remaining = pop_size-len(offspring)
    if remaining > 0:
        fronts[last_front].sort(cmp=crowded_comparison_operator)
        for i in range(remaining):
            offspring.append(fronts[last_front][i])
    return offspring


def weighted_sum(x):
    return sum(x['objectives'])


def search(search_space, max_gens, pop_size, p_cross):
    from random import randint
    pop = [{'vector': random_vector(search_space)} for _ in xrange(pop_size)]
    calculate_objectives(pop)
    fast_nondominated_sort(pop)
    selected = []
    for i in xrange(pop_size):
        selected.append(better(pop[randint(0, pop_size-1)], pop[randint(0, pop_size-1)]))
    children = reproduce(selected, pop_size, search_space, p_cross)
    calculate_objectives(children)
    for gen in xrange(max_gens):
        union = pop + children
        fronts = fast_nondominated_sort(union)
        parents = select_parents(fronts, pop_size)
        selected = []
        for i in xrange(pop_size):
            selected.append(better(parents[randint(0, pop_size-1)], parents[randint(0, pop_size-1)]))
        pop = children
        children = reproduce(selected, pop_size, search_space, p_cross)
        calculate_objectives(children)
        parents.sort(key=lambda x: weighted_sum(x))
        best = parents[0]
        print "> gen=%d, fronts=%d, best=%s" % (gen, len(fronts), best["objectives"])

    union = pop + children
    fronts = fast_nondominated_sort(union)
    parents = select_parents(fronts, pop_size)
    f1 = []
    f2 = []
    for front in fronts:
        for p in front:
            f1.append(p['objectives'][0])
            f2.append(p['objectives'][1])

    try:
        import matplotlib.pyplot as plt

        plt.scatter(f1, f2, marker='o')
        plt.xlim(-1, 10)
        plt.ylim(-1, 10)
        plt.grid()
        plt.show()
    except:
        print 'Please install matplot to show convergence history'
    return parents


def main():
    # problem configuration
    problem_size = 1
    search_space = [[-10, 10]] * problem_size
    # algorithm configuration
    max_gens = 100
    pop_size = 100
    p_cross = 0.98
    # execute the algorithm
    pop = search(search_space, max_gens, pop_size, p_cross)
    print "done!"


if __name__ == "__main__":
    main()

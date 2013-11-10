#!/usr/bin/env python

"""
"""
def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]

def euc_2d(c1, c2):
    import math
    return round(math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2))

def random_permutation(cities):
    import random
    perm = range(0, len(cities))
    for i in perm:
        r = random.randrange(len(perm)-i) + i
        perm[r], perm[i] = perm[i], perm[r]
    return perm

def stochastic_two_opt(permutation):
    import random
    perm = permutation[:]
    c1, c2 = random.randrange(len(perm)), random.randrange(len(perm))
    exclude = [c1]
    exclude.append(iif(c1==0, len(perm)-1, c1-1))
    exclude.append(iif(c1==len(perm)-1, 0, c1+1))
    while c2 in exclude:
        c2 = random.randrange(len(perm))
    if c2 < c1:
        c1, c2 = c2, c1
    r = perm[c1:c2]
    r.reverse()
    perm[c1:c2] = r
    return perm

def augmented_cost(permutation, penalties, cities, lambda_):
    distance, augmented = 0, 0
    for i in xrange(0, len(permutation)-1):
        c1 = permutation[i]
       	c2 = iif((i==len(permutation)-1),  permutation[0], permutation[i+1])
        if c2 < c1:
            c1, c2 = c2, c1
        d = euc_2d(cities[c1], cities[c2])
        distance = distance + d
        augmented = augmented +  d + (lambda_ * (penalties[c1][c2]))
    return [distance, augmented]

def cost(cand, penalties, cities, lambda_):
    cost, acost = augmented_cost(cand['vector'], penalties, cities, lambda_)
    cand['cost'], cand['aug_cost'] = cost, acost

def local_search(current, cities, penalties, max_no_improv, lambda_):
    cost(current, penalties, cities, lambda_)
    count = 0
    while count < max_no_improv:
        candidate = {'vector' : stochastic_two_opt(current['vector'])}
        cost(candidate, penalties, cities, lambda_)
        count = iif(candidate['aug_cost'] < current['aug_cost'], 0, count+1)
        if candidate['aug_cost'] < current['aug_cost']:
            current = candidate
    return current

def calculate_feature_utilities(penal, cities, permutation):
    utilities = [0] * len(permutation)
    for i in xrange(0, len(permutation)-1):
        c1 = permutation[i]
        c2 = iif(i==len(permutation)-1, permutation[0], permutation[i+1])
        if c2 < c1:
            c1, c2 = c2, c1
        utilities[i] = euc_2d(cities[c1], cities[c2]) / (1.0 + penal[c1][c2])
    return utilities

def update_penalties(penalties, cities, permutation, utilities):
    max_ = max(utilities)
    for i in xrange(0, len(permutation)-1):
        c1 = permutation[i]
        c2 = iif(i==len(permutation)-1, permutation[0], permutation[i+1])
        if c2 < c1:
            c1, c2 = c2, c1
        if utilities[i] == max:
            penalties[c1][c2] = penalties[c1][c2] + 1
    return penalties

def search(max_iterations, cities, max_no_improv, lambda_):
    current = {'vector' : random_permutation(cities)}
    best = None
    penalties = [[0] * len(cities)] * len(cities)
    for iter in xrange(0, max_iterations):
        current = local_search(current, cities, penalties, max_no_improv, lambda_)
        utilities = calculate_feature_utilities(penalties,cities,current['vector'])
        update_penalties(penalties, cities, current['vector'], utilities)
        if best == None or current['cost'] < best['cost']:
            best = current
        print " > iter=%d, best=%f, aug=%f" % (iter+1, best['cost'], best['aug_cost'])
    return best

def main():
    # problem configuration
    berlin52 = [[565,575],[25,185],[345,750],[945,685],[845,655],
        [880,660],[25,230],[525,1000],[580,1175],[650,1130],[1605,620],
        [1220,580],[1465,200],[1530,5],[845,680],[725,370],[145,665],
        [415,635],[510,875],[560,365],[300,465],[520,585],[480,415],
        [835,625],[975,580],[1215,245],[1320,315],[1250,400],[660,180],
        [410,250],[420,555],[575,665],[1150,1160],[700,580],[685,595],
        [685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
        [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],
        [830,610],[605,625],[595,360],[1340,725],[1740,245]]
    # algorithm configuration
    max_iterations = 100
    max_no_improv = 20
    alpha = 0.3
    local_search_optima = 12000.0
    lambda_ = alpha * (local_search_optima/len(berlin52))
    # execute the algorithm
    best = search(max_iterations, berlin52, max_no_improv, lambda_)
    print 'Done. Best Solution: c=%d, v=%s' % (best['cost'], str(best['vector']))

if __name__ == "__main__":
    main()

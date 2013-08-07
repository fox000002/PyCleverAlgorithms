#!/usr/bin/env python

"""
"""
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

def augumented_cost(permutation, penalties, cities, lambda_):
	pass

def cost(cand, penalties, cities, lambda_):
	pass

def local_search(current, cities, penalties, max_no_improv, lambda_):
	pass

def calculate_feature_utilities(penal, cities, permutation):
	pass

def update_penalties(penalties, cities, permutation, utilities):
	pass

def search(max_iterations, cities, max_no_improv, lambda_):
	pass

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
    best = search(berlin52, max_iterations, max_no_improv, lambda_)
    print 'Done. Best Solution: c=%d, v=%s' % (best['cost'], str(best['vector']))

if __name__ == "__main__":
    main()
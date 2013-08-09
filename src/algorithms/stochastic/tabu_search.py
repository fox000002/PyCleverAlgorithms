#!/usr/bin/env python

"""
"""
def iif(condition, true_part, false_part):  
    return (condition and [true_part] or [false_part])[0]  

def euc_2d(c1, c2):
	import math
	return round(math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2))

def cost(permutation, cities):
	distance = 0
	for i in range(0, len(permutation)):
		#print '-->', i, '=', permutation[i]
		c1 = permutation[i]
		c2 = permutation[iif(i==len(permutation)-1, 0, i+1)]
		distance = distance + euc_2d(cities[c1], cities[c2])
	return distance

def random_permutation(cities):
	import random
	perm = range(0, len(cities))
	for i in perm:
		r = random.randrange(len(perm)-i) + i
		perm[r], perm[i] = perm[i], perm[r]
	return perm

def stochastic_two_opt(parent):
	import random
	perm = parent[:]
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
	return perm, [[parent[c1-1], parent[c1]], [parent[c2-1], parent[c2]]]

def is_tabu(permutation, tabu_list):
	for i in xrange(0, len(permutation)):
		c1 = permutation[i]
		c2 = permutation[iif(i==len(permutation)-1, 0, i+1)]
		for forbidden_edge in tabu_list:
			if forbidden_edge == [c1, c2]:
				return True
	return False

def generate_candidate(best, tabu_list, cities):
	perm, edges = stochastic_two_opt(best['vector'])
	while is_tabu(perm, tabu_list):
		perm, edges = stochastic_two_opt(best['vector'])
	candidate = {}
	candidate['vector'] = perm
	candidate['cost'] = cost(candidate['vector'], cities)
	return [candidate, edges]

def search(cities, tabu_list_size, candidate_list_size, max_iter):
	current = {}
	current['vector'] = random_permutation(cities)
	current['cost'] = cost(current['vector'], cities)
	best = current
	tabu_list = []
	for iter in range(0, max_iter):
		candidates = []
		for i in xrange(0, candidate_list_size):
			candidates.append(generate_candidate(current, tabu_list, cities))
		candidates.sort(key=lambda x: x[0]['cost'])
		best_candidate = candidates[0][0]
		best_candidate_edges = candidates[0][1]
		if best_candidate['cost'] < current['cost']:
			current = best_candidate
			if best_candidate['cost'] < best['cost']:
				best = best_candidate
			for edge in best_candidate_edges:
				tabu_list.append(edge)
			while len(tabu_list) > tabu_list_size:
				tabu_list.pop()
		print ' > iteration %d, best=%d' % (iter+1, best['cost'])
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
    max_iter = 100
    tabu_list_size = 50
    max_candidates = 50
    # execute the algorithm
    best = search(berlin52, tabu_list_size, max_candidates, max_iter)
    print 'Done. Best Solution: c=%d, v=%s' % (best['cost'], str(best['vector']))

if __name__ == "__main__":
    main()
#!/usr/bin/env python

"""
Cuckoo Search

three idealized rules:
1. Each cuckoo lays one egg at a time, and dumps its egg in a randomly chosen nest;
2. The best nests with high quality of eggs will carry over to the next generation;
3. The number of available hosts nests is fixed, and the egg laid by a cuckoo is
   discovered by the host bird with a probability p_a \in (0,1). Discovering operate
   on some set of worst nests, and discovered solutions dumped from farther calculations.


pseudo-code:
Objective function: f(x), x = (x_1,x_2,...,x_d)
Generate an initial population of n host nests;
While (t<MaxGeneration) or (stop criterion)
   Get a cuckoo randomly (say, i) and replace its solution by performing Levy flights;
   Evaluate its quality/fitness F_i
         [For maximization, F_i \propto f(x_i) ];
   Choose a nest among n (say, j) randomly;
   if (F_i>F_j ),
          Replace j by the new solution;
   end if
   A fraction (p_a) of the worse nests are abandoned and new ones are built;
   Keep the best solutions/nests;
   Rank the solutions/nests and find the current best;
   Pass the current best solutions to the next generation;
end while
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(v):
    return sum(map(lambda x: x**2, v))


def random_vector(min_max):
    from random import random
    return map(lambda x: x[0] + (x[1]-x[0]) * random(), min_max)


def random_permutation(n):
    from random import randrange
    perm = range(n)
    for i in xrange(len(perm)):
        r = randrange(len(perm)-i) + i
        perm[r], perm[i] = perm[i], perm[r]
    return perm


def get_best_nest(nests, new_nests):
    for i in xrange(len(nests)):
        new_nests[i]['cost'] = objective_function(new_nests[i]['vector'])
        if new_nests[i]['cost'] <= nests[i]['cost']:
            nests[i] = new_nests[i]

    nest = nests[0]
    for i in xrange(len(nests)):
        if nests[i]['cost'] < nest['cost']:
            nest = nests[i]
    return nest


# Get cuckoos by random walk
def get_cuckoos(nests, best_nest, search_space):
    from math import gamma, sin, pi
    from random import random
    # Levy flights
    n = len(nests)
    # Levy exponent and coefficient
    beta = 3.0/2
    sigma = (gamma(1+beta)*sin(pi*beta/2)/(gamma((1+beta)/2)*beta*2**((beta-1)/2)))**(1/beta)

    for j in xrange(n):
        s = nests[j]['vector']
        # This is a simple way of implementing Levy flights
        # For standard random walks, use step=1;
        # Levy flights by Mantegna's algorithm
        # u=randn(size(s))*sigma;
        # v=randn(size(s));
        # step = u./abs(v).^(1/beta)
        step = [random() * sigma / abs(random())**(1/beta) for _ in range(len(s))]

        # In the next equation, the difference factor (s-best) means that
        # when the solution is the best solution, it remains unchanged.
        # stepsize=0.01*step.*(s-best);
        stepsize = [0.01 * step[i] * (s[i]-best_nest['vector'][i]) for i in xrange(len(step))]
        # Here the factor 0.01 comes from the fact that L/100 should the typical
        # step size of walks/flights where L is the typical lenghtscale;
        # otherwise, Levy flights may become too aggresive/efficient,
        # which makes new solutions (even) jump out side of the design domain
        # (and thus wasting evaluations).
        # Now the actual random walks or flights
        # s=s+stepsize.*randn(size(s));
        for i in xrange(len(s)):
            s[i] += stepsize[i] * random()

        # Apply simple bounds/limits
        simple_bound(s, search_space)

        nests[j]['vector'] = s
    return nests


# Replace some nests by constructing new solutions/nests
def empty_nests(nests, search_space, discovery_rate):
    from random import random
    # A fraction of worse nests are discovered with a probability pa
    n = len(nests)
    K = [iif(random() > discovery_rate, 1, 0) for _ in xrange(n)]

    # In the real world, if a cuckoo's egg is very similar to a host's eggs, then
    # this cuckoo's egg is less likely to be discovered, thus the fitness should
    # be related to the difference in solutions.  Therefore, it is a good idea
    # to do a random walk in a biased way with some random step sizes.
    # New solution by biased/selective random walks
    # stepsize=rand*(nest(randperm(n),:)-nest(randperm(n),:));
    # new_nest=nest+stepsize.*K;
    r1 = random_permutation(n)
    r2 = random_permutation(n)

    new_nests = []

    r = random()
    for i in range(n):
        nest1_v = nests[r1[i]]['vector']
        nest2_v = nests[r2[i]]['vector']
        new_nest = {
            'vector': nests[i]['vector'][:]
        }
        for m in range(len(new_nest['vector'])):
            new_nest['vector'][m] += r * (nest1_v[m]-nest2_v[m])*K[i]
        new_nests.append(new_nest)

    for j in xrange(len(new_nests)):
        simple_bound(new_nests[j]['vector'], search_space)

    return new_nests


def simple_bound(v, search_space):
    for i in xrange(len(v)):
        if v[i] < search_space[i][0]:
            v[i] = search_space[i][0]
        elif v[i] > search_space[i][1]:
            v[i] = search_space[i][1]


def search(search_space, max_iter, num_nests=25, discovery_rate=0.25, tol=1.0e-5):
    # Random initial solutions
    nests = [{'vector': random_vector(search_space)} for _ in xrange(num_nests)]
    for nest in nests:
        nest['cost'] = objective_function(nest['vector'])

    # Get the current best
    best = get_best_nest(nests, nests)

    for iteration in xrange(max_iter):
        # Generate new solutions (but keep the current best)
        new_nests = get_cuckoos(nests, best, search_space)
        nest = get_best_nest(nests, new_nests)

        # Discovery and randomization
        new_nests = empty_nests(nests, search_space, discovery_rate)

        # Evaluate this set of solutions
        nest = get_best_nest(nests, new_nests)

        # Find the best objective so far
        if nest['cost'] < best['cost']:
            best = nest

        print best
    return best


def main():
    # problem configuration
    problem_size = 2
    search_space = [[-5, 5]] * problem_size
    # algorithm configuration
    max_iter = 100
    #
    best = search(search_space, max_iter)
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['vector']))


if __name__ == "__main__":
    main()
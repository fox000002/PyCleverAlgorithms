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


def get_best_nest(nests, new_nests):
    for i in xrange(len(nests)):
        if new_nests[i]['cost'] <= nests[i]['cost']:
            nests[i] = new_nests[i]

    nest = nests[0]
    for i in xrange(len(nests)):
        if nests[i]['cost'] < nest['cost']:
            nest = nests[i]
    return nest


# Get cuckoos by random walk
def get_cuckoos(nests, best_nests, search_space):
    return nests


# Replace some nests by constructing new solutions/nests
def empty_nests(nests, search_space, discovery_rate):
    from random import random
    # A fraction of worse nests are discovered with a probability pa
    n = len(nests)
    K = [random() > discovery_rate for _ in xrange(n)]

    # In the real world, if a cuckoo's egg is very similar to a host's eggs, then
    # this cuckoo's egg is less likely to be discovered, thus the fitness should
    # be related to the difference in solutions.  Therefore, it is a good idea
    # to do a random walk in a biased way with some random step sizes.
    # New solution by biased/selective random walks

    for nest in nests:
        nest['vector'] = None
        simple_bound(nest['vector'], search_space)

    return nests


def simple_bound(v, search_space):
    for i in xrange(len(v)):
        if v[i] < search_space[i][0]:
            v[i] = search_space[i][0]
        elif v[i] > search_space[i][1]:
            v[i] = search_space[i][1]


def search(search_space, max_iter, num_nests=25, discovery_rate=0.25, tol=1.0e-5):
    best = None
    # Random initial solutions
    nests = [{'vector': [random_vector(x) for x in search_space]} for _ in xrange(num_nests)]
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
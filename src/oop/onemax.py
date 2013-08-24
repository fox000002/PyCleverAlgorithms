#!/usr/bin/env python

from problem import Problem
from strategy import Strategy
from unmatch_exception import UnmatchError

def iif(condition, true_part, false_part):  
    return (condition and [true_part] or [false_part])[0]  

class OneMax(Problem):
    """docstring for OneMax"""
    def __init__(self, num_bits=64):
        self.num_bits = num_bits

    def assess(self, candidate_solution):
        if len(candidate_solution['bitstring']) != self.num_bits:
              raise UnmatchError("Expected #{@num_bits} in candidate solution.")
        sum = 0
        for i in xrange(0, len(candidate_solution['bitstring'])): 
              if candidate_solution['bitstring'][i] =='1':
                  sum = sum + 1 
        return sum

    def is_optimal(self, candidate_solution):
        return candidate_solution['fitness'] == self.num_bits

class GeneticAlgorithm(Strategy):
    """docstring for ClassName"""
    def __init__(self, max_gens=100, pop_size=100, crossover=0.98, mutation=1.0/64.0):
        self.max_generations = max_gens
        self.population_size = pop_size
        self.p_crossover = crossover
        self.p_mutation = mutation

    def random_bitstring(self, num_bits):
        from random import sample
        return map(lambda x: iif(x<50, '1', '0'), sample(range(100), num_bits))

    def binary_tournament(self, pop):
        pass

    def point_mutation(self, bitstring):
        pass

    def uniform_crossover(self, parent1, parent2):
        pass

    def reproduce(self, selected):
        pass

    def execute(self, problem):
        pass

def main():
    # problem configuration
      problem = OneMax()
      # algorithm configuration
      strategy = GeneticAlgorithm()
      # execute the algorithm
      best = strategy.execute(problem)
      #print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['vector']))

if __name__ == "__main__":
    main()



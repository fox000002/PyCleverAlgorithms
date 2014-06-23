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
        sum_value = 0
        for i in xrange(0, len(candidate_solution['bitstring'])):
            if candidate_solution['bitstring'][i] == '1':
                sum_value += 1
        return sum_value

    def is_optimal(self, candidate_solution):
        return candidate_solution['fitness'] == self.num_bits


class GeneticAlgorithm(Strategy):
    """docstring for ClassName"""

    def __init__(self, max_gens=100, pop_size=100, crossover=0.98, mutation=1.0 / 64.0):
        self.max_generations = max_gens
        self.population_size = pop_size
        self.p_crossover = crossover
        self.p_mutation = mutation

    @staticmethod
    def random_bitstring(num_bits):
        from random import sample
        return map(lambda x: iif(x < 50, '1', '0'), sample(range(100), num_bits))

    @staticmethod
    def binary_tournament(pop):
        from random import randint

        i, j = randint(0, len(pop) - 1), randint(0, len(pop) - 1)
        while j == i:
            j = randint(0, len(pop) - 1)
        return iif(pop[i]['fitness'] > pop[j]['fitness'], pop[i], pop[j])

    def point_mutation(self, bitstring):
        from random import random

        child = ""
        for i in xrange(0, len(bitstring)):
            bit = bitstring[i]
            child = child + iif(random() < self.p_mutation, iif(bit == '1', '0', '1'), bit)
        return child

    def uniform_crossover(self, parent1, parent2):
        from random import random, randint

        if random() >= self.p_crossover:
            return parent1
        point = 1 + randint(0, len(parent1) - 2)
        return parent1[0:point] + parent2[point:len(parent1)]

    def reproduce(self, selected):
        children = []
        for i in xrange(0, len(selected)):
            p1 = selected[i]
            ix = iif(i % 2 == 0, i + 1, i - 1)
            if i == len(selected) - 1:
                ix = 0
            p2 = selected[ix]
            child = {
                'bitstring': self.uniform_crossover(p1['bitstring'], p2['bitstring'])
            }
            child['bitstring'] = self.point_mutation(child['bitstring'])
            children.append(child)
            if len(children) >= self.population_size:
                break
        return children

    def execute(self, problem):
        population = []
        for i in xrange(0, self.population_size):
            population.append({'bitstring': self.random_bitstring(problem.num_bits)})
        for c in population:
            c['fitness'] = problem.assess(c)
        population.sort(key=lambda x: x['fitness'])
        best = population[0]
        for gen in xrange(0, self.max_generations):
            selected = [self.binary_tournament(population) for i in xrange(0, self.population_size)]
            children = self.reproduce(selected)
            for c in children:
                c['fitness'] = problem.assess(c)
            children.sort(key=lambda x: x['fitness'])
            if children[0]['fitness'] > best['fitness']:
                best = children[0]
            population = children
            print " > gen %d, best: %d, %s" % (gen, best['fitness'], best['bitstring'])
            if problem.is_optimal(best):
                break
        return best


def main():
    # problem configuration
    problem = OneMax()
    # algorithm configuration
    strategy = GeneticAlgorithm()
    # execute the algorithm
    best = strategy.execute(problem)
    print 'Done. Best Solution: c=%f, v=%s' % (best['fitness'], str(best['bitstring']))


if __name__ == "__main__":
    main()
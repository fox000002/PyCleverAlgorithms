#!/usr/bin/env python

from problem import Problem
from strategy import Strategy
from unmatch_exception import UnmatchError
from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


class Knapsack(Problem):
    """docstring for OneMax"""

    def __init__(self, items, limit):
        self.num_bits = len(items)
        self.items = items
        self.limit = limit

    def assess(self, candidate_solution):
        if len(candidate_solution['bitstring']) != self.num_bits:
            raise UnmatchError("Expected #{@num_bits} in candidate solution.")
        sum = 0
        cons = 0
        for i in xrange(0, len(candidate_solution['bitstring'])):
            if candidate_solution['bitstring'][i] == '1':
                sum += self.items[i].value
                cons += self.items[i].weight
        if cons > self.limit:
            sum -= sum * 2

        return sum

    def is_optimal(self, candidate_solution):
        return candidate_solution['fitness'] == self.num_bits


class GeneticAlgorithm(Strategy):
    """docstring for ClassName"""

    def __init__(self, max_gens=200, pop_size=100, crossover=0.8, mutation=0.2):
        self.max_generations = max_gens
        self.population_size = pop_size
        self.p_crossover = crossover
        self.p_mutation = mutation

    def random_bitstring(self, num_bits):
        from random import sample, randrange
        return [iif(randrange(100) < 3, '1', '0') for i in xrange(num_bits)]
        #return map(lambda x: iif(x < 10, '1', '0'), sample(range(100), num_bits))

    def binary_tournament(self, pop):
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
            child = {}
            child['bitstring'] = self.uniform_crossover(p1['bitstring'], p2['bitstring'])
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
            #print c['bitstring']
            while c['fitness'] <= 0:
                c['bitstring'] = self.random_bitstring(problem.num_bits)
                #print c['bitstring']
                c['fitness'] = problem.assess(c)
        population.sort(key=lambda x: x['fitness'], reverse=True)
        best = population[0]
        for gen in xrange(0, self.max_generations):
            selected = [self.binary_tournament(population) for i in xrange(0, self.population_size)]
            children = self.reproduce(selected)
            for c in children:
                c['fitness'] = problem.assess(c)
                #print c['bitstring'], c['fitness']
                #while c['fitness'] <= 0:
                #    c['bitstring'] = self.random_bitstring(problem.num_bits)
                #    print c['bitstring']
                #    c['fitness'] = problem.assess(c)
            children.sort(key=lambda x: x['fitness'], reverse=True)
            if children[0]['fitness'] > best['fitness']:
                best = children[0]
            population = children
            #print " > gen %d, best: %d, %s" % (gen, best['fitness'], best['bitstring'])
            if problem.is_optimal(best):
                break
        return best


def knapsack_dp(items, maxweight):
    """
    Solve the knapsack problem by finding the most valuable
    subsequence of `items` subject that weighs no more than
    `maxweight`.

    `items` is a sequence of pairs `(value, weight)`, where `value` is
    a number and `weight` is a non-negative integer.

    `maxweight` is a non-negative integer.

    Return a pair whose first element is the sum of values in the most
    valuable subsequence, and whose second element is the subsequence.

    >>> items = [(4, 12), (2, 1), (6, 4), (1, 1), (2, 2)]
    >>> knapsack_dp(items, 15)
    (11, [(2, 1), (6, 4), (1, 1), (2, 2)])
    """

    # Return the value of the most valuable subsequence of the first i
    # elements in items whose weights sum to no more than j.
    #@memoized
    def bestvalue(i, j):
        if i == 0: return 0
        value, weight = items[i - 1].value, items[i - 1].weight
        if weight > j:
            return bestvalue(i - 1, j)
        else:
            return max(bestvalue(i - 1, j),
                       bestvalue(i - 1, j - weight) + value)

    j = maxweight
    result = []
    for i in xrange(len(items), 0, -1):
        if bestvalue(i, j) != bestvalue(i - 1, j):
            result.append(items[i - 1])
            j -= items[i - 1].weight
    result.reverse()
    return bestvalue(len(items), maxweight), result


def main():
    import sys
    # problem configuration
    items = []
    capacity = 100000
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        # parse the input
        lines = input_data.split('\n')

        first_line = lines[0].split()
        item_count = int(first_line[0])
        capacity = int(first_line[1])

        for i in range(1, item_count+1):
            line = lines[i]
            parts = line.split()
            items.append(Item(i-1, int(parts[0]), int(parts[1])))
    else:
        data = [
            [90000, 90001],
            [89750, 89751],
            [10001, 10002],
            [89500, 89501],
            [10252, 10254],
            [89250, 89251],
            [10503, 10506],
            [89000, 89001],
            [10754, 10758],
            [88750, 88751],
            [11005, 11010],
            [88500, 88501],
            [11256, 11262],
            [88250, 88251],
            [11507, 11514],
            [88000, 88001],
            [11758, 11766],
            [87750, 87751],
            [12009, 12018],
            [87500, 87501],
            [12260, 12270],
            [87250, 87251],
            [12511, 12522],
            [87000, 87001],
            [12762, 12774],
            [86750, 86751],
            [13013, 13026],
            [86500, 86501],
            [13264, 13278],
            [86250, 86251]
        ]
        for i in xrange(len(data)):
            items.append(Item(i, data[i][0], data[i][1]))


    #problem = Knapsack(items, capacity)
    # algorithm configuration
    #strategy = GeneticAlgorithm()
    # execute the algorithm
    #best = strategy.execute(problem)
    #print 'Done. Best Solution: c=%f, v=%s' % (best['fitness'], str(best['bitstring']))
    print(knapsack_dp(items, capacity))

if __name__ == "__main__":
    main()

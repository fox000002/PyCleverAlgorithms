#!/usr/bin/env python

# Self-Organizing Migrating Algorithm

#Ackley Function
def objective_function(v):
    from math import sin, cos, sqrt, exp
    val = 0
    for i in xrange(0, len(v)-1):
        val = val + 3*(cos(2*v[i])+sin(2*v[i+1]))+sqrt(v[i+1]**2+v[i]**2)/exp(0.2)
    return val

def random_vector(minmax):
    import random
    #print minmax
    return map(lambda x : x[0] + (x[1]-x[0]) * random.random(), minmax)

def frange(start, stop, step):
    assert step > 0.0
    total = start
    compo = 0.0
    while total < stop:
        yield total
        y = step - compo
        temp = total + y
        compo = (temp - total) - y
        total = temp

# STRATEGY "ALL-TO-ONE (LEADER)", the basic version
def soma_all_to_one(search_space, step, pathLength, prt, minDiv, migrations, pop_size):
    import random
    dim = len(search_space)

    # generating population within the search space
    individuals = [[0] * dim] * pop_size
    #print search_space
    costValues = [0] * pop_size
    for i in xrange(0, pop_size):
        individuals[i] = random_vector(search_space)
        costValues[i] = objective_function(individuals[i])

    indexOfLeader = 1
    # find the leader (individual with the lowest cost value)
    xmin = 99999999
    for i in xrange(0, pop_size):
        if costValues[i] < xmin:
            min = costValues[i]
            indexOfLeader = i

    globalErrorHistory = [0] * migrations
    mig = 0
    go = True

    while mig < migrations and go :
        # migrate individuals to the leader (except leader to himself, of course :)
        for i in xrange(0, pop_size):
            # check if this individual is not leader
            if i == indexOfLeader:
                if indexOfLeader != pop_size:
                    continue
                else:
                    break

            # store the individual's start position
            startPositionOfIndividual = individuals[i]

            leaderPosition = individuals[indexOfLeader]
            tmpIndividual = individuals[i]

            # Let's migrate!
            for t in frange(0.0, pathLength, step):
                # Generate new PRTVector for each step of this individual
                prtVectorContainOnlyZero = True
                PRTVector = [0] * dim
                while prtVectorContainOnlyZero:
                    for j in xrange(0, dim):
                        if random.random() < prt:
                            PRTVector[j] = 1
                            prtVectorContainOnlyZero = False
                        else:
                            PRTVector[j] = 0

                # new positon for all dimension
                for j in xrange(0, dim):
                    tmpIndividual[j] = startPositionOfIndividual[j] + (leaderPosition[j] - startPositionOfIndividual[j]) * t * PRTVector[j]

                # check boundaries
                for j in xrange(0, dim):
                    if tmpIndividual[j] < search_space[j][0] and tmpIndividual[j] > search_space[j][1]:
                        tmpIndividual[j] = random_vector(search_space[j])

                tmpCostValue = objective_function(tmpIndividual)

                if tmpCostValue < costValues[i]:
                    costValues[i] = tmpCostValue # store better CV and postion
                    individuals[i] = tmpIndividual


        globalErrorHistory[mig] = costValues[indexOfLeader]

        # check and conditions
        migCheck = 20
        if mig > migCheck + 1:
            decrease = 0
            for i in xrange(0, migCheck):
                decrease = decrease + abs(globalErrorHistory[mig-i-1] - globalErrorHistory[mig-i])
                if decrease < minDiv:
                    go = False
        mig = mig + 1

        print 'mig = %d of %d' % (mig, migrations)

    globalErrorHistory4Saving = [0] * mig
    for i in xrange(0, mig):
        globalErrorHistory4Saving[i] = globalErrorHistory[i]

    return { 'position' : individuals[indexOfLeader], 
        'cost' : objective_function(individuals[indexOfLeader]),
        'history' : globalErrorHistory4Saving }    

def soma_all_to_all():
    pass

def soma_all_to_one_randomly():
    pass

def some_all_to_all_adaptive():
    pass

def main():
    # problem configuration
    problem_size = 100
    search_space = [[-20, +20]] * problem_size
    # algorithm configuration
    step = 0.21
    pathLength = 2.1
    prt = 0.1
    minDiv = 0
    migrations = 10
    pop_size = 10*problem_size
    #
    best = soma_all_to_one(search_space, step, pathLength, prt, minDiv, migrations, pop_size)
    #
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['position']))

if __name__ == "__main__":
    main()


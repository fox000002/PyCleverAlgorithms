#!/usr/bin/env python

"""
Self-Organizing Migrating Algorithm (SOMA)
"""


# Ackley Function
def objective_function(v):
    from math import sin, cos, sqrt, exp

    val = 0
    for i in xrange(0, len(v) - 1):
        val = val + 3 * (cos(2 * v[i]) + sin(2 * v[i + 1])) + sqrt(v[i + 1] ** 2 + v[i] ** 2) / exp(0.2)
    return val


def random_bound(bound):
    import random

    return bound[0] + (bound[1] - bound[0]) * random.random()


def random_vector(min_max):
    import random

    return map(lambda x: x[0] + (x[1] - x[0]) * random.random(), min_max)


def frange(start, stop, step):
    #assert step > 0.0
    total = start
    compo = 0.0
    while total <= stop:
        yield total
        y = step - compo
        temp = total + y
        compo = (temp - total) - y
        total = temp


# STRATEGY "ALL-TO-ONE (LEADER)", the basic version
def soma_all_to_one(search_space, step, path_length, prt, min_div, migrations, pop_size):
    import random

    dim = len(search_space)

    # generating population within the search space
    individuals = [[0] * dim] * pop_size
    #print search_space
    cost_values = [0] * pop_size
    for i in xrange(0, pop_size):
        individuals[i] = random_vector(search_space)
        cost_values[i] = objective_function(individuals[i])

    index_of_leader = 0
    # find the leader (individual with the lowest cost value)
    xmin = 99999999
    for i in xrange(0, pop_size):
        if cost_values[i] < xmin:
            xmin = cost_values[i]
            index_of_leader = i

    global_error_history = [0] * migrations
    mig = 0
    go = True

    while mig < migrations and go:
        # migrate individuals to the leader (except leader to himself, of course :)
        for i in xrange(0, pop_size):
            # check if this individual is not leader
            if i == index_of_leader:
                if index_of_leader != pop_size:
                    continue
                else:
                    break

            # store the individual start position
            start_position_of_individual = individuals[i]

            leader_position = individuals[index_of_leader]
            tmp_individual = individuals[i][:]

            # Let's migrate!
            for t in frange(0.0, path_length, step):
                #print 'path : %f' % t
                # Generate new PRTVector for each step of this individual
                prt_vector_contain_only_zero = True
                prt_vector = [0] * dim
                while prt_vector_contain_only_zero:
                    for j in xrange(0, dim):
                        if random.random() < prt:
                            prt_vector[j] = 1
                            prt_vector_contain_only_zero = False
                        else:
                            prt_vector[j] = 0

                # new position for all dimension
                for j in xrange(0, dim):
                    tmp_individual[j] = start_position_of_individual[j] + \
                                        (leader_position[j] - start_position_of_individual[j]) * t * prt_vector[j]

                # check boundaries
                for j in xrange(0, dim):
                    if tmp_individual[j] < search_space[j][0] or tmp_individual[j] > search_space[j][1]:
                        tmp_individual[j] = random_bound(search_space[j])

                tmp_cost_value = objective_function(tmp_individual)

                if tmp_cost_value < cost_values[i]:
                    cost_values[i] = tmp_cost_value  # store better CV and postion
                    individuals[i] = tmp_individual[:]

        # find the leader (individual with the lowest cost value)
        xmin = 9999999
        for i in xrange(0, pop_size):
            if cost_values[i] < xmin:
                xmin = cost_values[i]
                index_of_leader = i

        global_error_history[mig] = cost_values[index_of_leader]

        # check and conditions
        mig_check = 20
        if mig > mig_check + 1:
            decrease = 0
            for i in xrange(0, mig_check):
                decrease = decrease + abs(global_error_history[mig - i - 1] - global_error_history[mig - i])
                if decrease < min_div:
                    go = False
        mig = mig + 1

        print 'mig = %d of %d %f' % (mig, migrations, min(cost_values))

    global_error_history_for_saving = [0] * mig
    for i in xrange(0, mig):
        global_error_history_for_saving[i] = global_error_history[i]

    return {'position': individuals[index_of_leader],
            'cost': objective_function(individuals[index_of_leader]),
            'history': global_error_history_for_saving}


# (individuals migrate to other randomly selected individuals)
def soma_all_to_one_randomly(search_space, step, path_length, prt, min_div, migrations, pop_size):
    import random

    dim = len(search_space)
    # generating population within the search space
    individuals = [[0] * dim] * pop_size
    #print search_space
    costValues = [0] * pop_size
    for i in xrange(0, pop_size):
        individuals[i] = random_vector(search_space)
        costValues[i] = objective_function(individuals[i])

    indexOfLeader = 0
    # find the leader (individual with the lowest cost value)
    xmin = 99999999
    for i in xrange(0, pop_size):
        if costValues[i] < xmin:
            xmin = costValues[i]
            indexOfLeader = i
            #print '--- indexOfLeader : %d (%d)' % (indexOfLeader, pop_size)

    globalErrorHistory = [0] * migrations
    mig = 0
    go = True

    while mig < migrations and go:
        # migrate individuals to the leader (except leader to himself, of course :)
        for i in xrange(0, pop_size):
            # Let's choose a random individual towards whom will this
            # individual perform the migration (a targetIndividual):
            individual_chosen = 0
            index_of_target = -1
            while not individual_chosen:
                index_of_target = int(round(pop_size * random.random()))
                if index_of_target != i and index_of_target != pop_size:  # it can't migrate to itself or be zero (!)
                    individual_chosen = 1;

            # store the individual start position
            startPositionOfIndividual = individuals[i]

            targetPosition = individuals[index_of_target]
            tmpIndividual = individuals[i][:]

            # Let's migrate!
            for t in frange(0.0, path_length, step):
                #print 'path : %f' % t
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
                    tmpIndividual[j] = startPositionOfIndividual[j] + (targetPosition[j] - startPositionOfIndividual[
                        j]) * t * PRTVector[j]

                # check boundaries
                for j in xrange(0, dim):
                    if tmpIndividual[j] < search_space[j][0] or tmpIndividual[j] > search_space[j][1]:
                        tmpIndividual[j] = random_bound(search_space[j])

                tmpCostValue = objective_function(tmpIndividual)

                if tmpCostValue < costValues[i]:
                    costValues[i] = tmpCostValue  # store better CV and postion
                    individuals[i] = tmpIndividual[:]

        # find the leader (individual with the lowest cost value)
        xmin = 9999999
        for i in xrange(0, pop_size):
            if costValues[i] < xmin:
                xmin = costValues[i]
                indexOfLeader = i

        globalErrorHistory[mig] = costValues[indexOfLeader]

        # check and conditions
        migCheck = 20
        if mig > migCheck + 1:
            decrease = 0
            for i in xrange(0, migCheck):
                decrease = decrease + abs(globalErrorHistory[mig - i - 1] - globalErrorHistory[mig - i])
                if decrease < min_div:
                    go = False
        mig = mig + 1

        print 'mig = %d of %d %f' % (mig, migrations, min(costValues))

    globalErrorHistory4Saving = [0] * mig
    for i in xrange(0, mig):
        globalErrorHistory4Saving[i] = globalErrorHistory[i]

    return {'position': individuals[indexOfLeader],
            'cost': objective_function(individuals[indexOfLeader]),
            'history': globalErrorHistory4Saving}


def soma_all_to_all(search_space, step, pathLength, prt, minDiv, migrations, pop_size):
    import random

    dim = len(search_space)

    # generating population within the search space
    individuals = [[0] * dim] * pop_size
    #print search_space
    costValues = [0] * pop_size
    for i in xrange(0, pop_size):
        individuals[i] = random_vector(search_space)
        costValues[i] = objective_function(individuals[i])

    indexOfLeader = 0
    # find the leader (individual with the lowest cost value)
    xmin = 99999999
    for i in xrange(0, pop_size):
        if costValues[i] < xmin:
            xmin = costValues[i]
            indexOfLeader = i

    globalErrorHistory = [0] * migrations
    mig = 0
    go = True

    while mig < migrations and go:
        # migrate all individuals to all others:
        for i in xrange(0, pop_size):
            print 'pop = %d' % i

            # store the individual's start position
            startPositionOfIndividual = individuals[i]

            stopMigrations = False
            for indexOfTarget in xrange(0, pop_size):
                if indexOfTarget == i:
                    if indexOfTarget != pop_size - 1:
                        indexOfTarget = indexOfTarget + 1  # don't migrate to itself
                    else:
                        stopMigrations = True  #  targetIndividual is the last one and shall migrate to itself
                        break

                if stopMigrations:
                    print 'i=%d; indexOfTarget=%d' % (i, indexOfTarget)
                    break

                targetPosition = individuals[indexOfTarget]
                tmpIndividual = individuals[i][:]

                # Let's migrate!
                for t in frange(0.0, pathLength, step):
                    #print 'path : %f' % t
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
                        tmpIndividual[j] = startPositionOfIndividual[j] + (
                                                                          targetPosition[j] - startPositionOfIndividual[
                                                                              j]) * t * PRTVector[j]

                    # check boundaries
                    for j in xrange(0, dim):
                        if tmpIndividual[j] < search_space[j][0] or tmpIndividual[j] > search_space[j][1]:
                            tmpIndividual[j] = random_bound(search_space[j])

                    tmpCostValue = objective_function(tmpIndividual)

                    if tmpCostValue < costValues[i]:
                        costValues[i] = tmpCostValue  # store better CV and postion
                        individuals[i] = tmpIndividual[:]

        # find the leader (individual with the lowest cost value)
        xmin = 9999999
        for i in xrange(0, pop_size):
            if costValues[i] < xmin:
                xmin = costValues[i]
                indexOfLeader = i

        globalErrorHistory[mig] = costValues[indexOfLeader]

        # check and conditions
        migCheck = 20
        if mig > migCheck + 1:
            decrease = 0
            for i in xrange(0, migCheck):
                decrease = decrease + abs(globalErrorHistory[mig - i - 1] - globalErrorHistory[mig - i])
                if decrease < minDiv:
                    go = False
        mig = mig + 1

        print 'mig = %d of %d %f' % (mig, migrations, min(costValues))

    globalErrorHistory4Saving = [0] * mig
    for i in xrange(0, mig):
        globalErrorHistory4Saving[i] = globalErrorHistory[i]

    return {'position': individuals[indexOfLeader],
            'cost': objective_function(individuals[indexOfLeader]),
            'history': globalErrorHistory4Saving}


def soma_all_to_all_adaptive(search_space, step, pathLength, prt, minDiv, migrations, pop_size):
    import random

    dim = len(search_space)

    # generating population within the search space
    individuals = [[0] * dim] * pop_size
    #print search_space
    costValues = [0] * pop_size
    for i in xrange(0, pop_size):
        individuals[i] = random_vector(search_space)
        costValues[i] = objective_function(individuals[i])

    indexOfLeader = 0
    # find the leader (individual with the lowest cost value)
    xmin = 99999999
    for i in xrange(0, pop_size):
        if costValues[i] < xmin:
            xmin = costValues[i]
            indexOfLeader = i

    globalErrorHistory = [0] * migrations
    mig = 0
    go = True

    while mig < migrations and go:
        # migrate all individuals to all others:
        for i in xrange(0, pop_size):
            print 'pop = %d' % i

            stopMigrations = False
            for indexOfTarget in xrange(0, pop_size):
                if indexOfTarget == i:
                    if indexOfTarget != pop_size - 1:
                        indexOfTarget = indexOfTarget + 1  # don't migrate to itself
                    else:
                        stopMigrations = True  #  targetIndividual is the last one and shall migrate to itself
                        break

                if stopMigrations:
                    print 'i=%d; indexOfTarget=%d' % (i, indexOfTarget)
                    break

                # store the individual's start position
                startPositionOfIndividual = individuals[i]

                targetPosition = individuals[indexOfTarget]
                tmpIndividual = individuals[i][:]

                # Let's migrate!
                for t in frange(0.0, pathLength, step):
                    #print 'path : %f' % t
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
                        tmpIndividual[j] = startPositionOfIndividual[j] + (
                                                                          targetPosition[j] - startPositionOfIndividual[
                                                                              j]) * t * PRTVector[j]

                    # check boundaries
                    for j in xrange(0, dim):
                        if tmpIndividual[j] < search_space[j][0] or tmpIndividual[j] > search_space[j][1]:
                            tmpIndividual[j] = random_bound(search_space[j])

                    tmpCostValue = objective_function(tmpIndividual)

                    if tmpCostValue < costValues[i]:
                        costValues[i] = tmpCostValue  # store better CV and postion
                        individuals[i] = tmpIndividual[:]


        # find the leader (individual with the lowest cost value)
        xmin = 9999999
        for i in xrange(0, pop_size):
            if costValues[i] < xmin:
                xmin = costValues[i]
                indexOfLeader = i

        globalErrorHistory[mig] = costValues[indexOfLeader]

        # check and conditions
        migCheck = 20
        if mig > migCheck + 1:
            decrease = 0
            for i in xrange(0, migCheck):
                decrease = decrease + abs(globalErrorHistory[mig - i - 1] - globalErrorHistory[mig - i])
                if decrease < minDiv:
                    go = False
        mig = mig + 1

        print 'mig = %d of %d %f' % (mig, migrations, min(costValues))

    globalErrorHistory4Saving = [0] * mig
    for i in xrange(0, mig):
        globalErrorHistory4Saving[i] = globalErrorHistory[i]

    return {'position': individuals[indexOfLeader],
            'cost': objective_function(individuals[indexOfLeader]),
            'history': globalErrorHistory4Saving}


def main():
    # problem configuration
    problem_size = 100
    search_space = [[-20, +20]] * problem_size
    # algorithm configuration
    step = 0.21
    pathLength = 2.1
    prt = 0.1
    minDiv = 0
    migrations = 50
    pop_size = 2 * problem_size
    #
    best = soma_all_to_one(search_space, step, pathLength, prt, minDiv, migrations, pop_size)
    #
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['position']))
    print 'History : %s' % best['history']

    try:
        import matplotlib.pyplot as plt

        plt.plot(best['history'])
        plt.show()
    except:
        print 'Please install matplot to show convergence history'

    #
    best = soma_all_to_one_randomly(search_space, step, pathLength, prt, minDiv, migrations, pop_size)
    #
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['position']))
    print 'History : %s' % best['history']

    try:
        import matplotlib.pyplot as plt

        plt.plot(best['history'])
        plt.show()
    except:
        print 'Please install matplot to show convergence history'

    #
    best = soma_all_to_all(search_space, step, pathLength, prt, minDiv, migrations, pop_size)
    #
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['position']))
    print 'History : %s' % best['history']

    try:
        import matplotlib.pyplot as plt

        plt.plot(best['history'])
        plt.show()
    except:
        print 'Please install matplot to show convergence history'

    #
    best = soma_all_to_all_adaptive(search_space, step, pathLength, prt, minDiv, migrations, pop_size)
    #
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['position']))
    print 'History : %s' % best['history']

    try:
        import matplotlib.pyplot as plt

        plt.plot(best['history'])
        plt.show()
    except:
        print 'Please install matplot to show convergence history'


if __name__ == "__main__":
    main()


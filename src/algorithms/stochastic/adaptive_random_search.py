#!/usr/bin/env python

def objective_function(v):
    return sum(map(lambda x : x**2, v))

def rand_in_bounds(min, max):
    import random
    return min + (max-min) * random.random()

def random_vector(minmax):
    return map(lambda x : rand_in_bounds(x[0], x[1]), minmax)

def take_step(minmax, current, step_size):
    return map(lambda x, y : rand_in_bounds(max(x[0], y-step_size), min(x[1], y+step_size)), minmax, current)

def large_step_size(iter, step_size, s_factor, l_factor, iter_mult):
    if iter%iter_mult == 0:
        return step_size * l_factor
    return step_size * s_factor

def take_steps(bounds, current, step_size, big_stepsize):
    step, big_step = {}, {}
    step['vector'] = take_step(bounds, current['vector'], step_size)
    step['cost'] = objective_function(step['vector'])
    big_step['vector'] = take_step(bounds, current['vector'], big_stepsize)
    big_step['cost'] = objective_function(big_step['vector'])
    return step, big_step


def search(max_iter, bounds, init_factor, s_factor, l_factor, iter_mult, max_no_impr):
    step_size = (bounds[0][1] - bounds[0][0]) * init_factor
    current, count = {}, 0
    current['vector'] = random_vector(bounds)
    current['cost'] = objective_function(current['vector'])
    for iter in range(0, max_iter):
        big_stepsize = large_step_size(iter, step_size, s_factor, l_factor, iter_mult)
        step, big_step = take_steps(bounds, current, step_size, big_stepsize)
        if step['cost'] <= current['cost'] or big_step['cost'] <= current['cost']:
            if big_step['cost'] <= step['cost']:
                step_size, current = big_stepsize, big_step
            else:
                current = step
            count = 0
        else:
            count = count + 1
            if count >= max_no_impr:
                count, step_size = 0, (step_size/s_factor)
        print ' > iteration=%d, best=%f' % (iter+1, current['cost'])
    return current

def main():
    #
    problem_size = 2
    bounds = [[-5,5]] * problem_size
    #
    max_iter = 1000
    init_factor = 0.05
    s_factor = 1.3
    l_factor = 3.0
    iter_mult = 10
    max_no_impr = 30
    #
    best = search(max_iter, bounds, init_factor, s_factor, l_factor, iter_mult, max_no_impr)
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['vector']))

if __name__ == "__main__":
    main()

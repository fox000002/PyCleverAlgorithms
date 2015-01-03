#!/usr/bin/env python

import unittest
import os

os.sys.path.append("..")

from pso import objective_function, random_vector, create_particle, get_global_best, update_velocity



class TestPSO(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2]

    def test_objective_function(self):
        self.assertEqual(objective_function(self.data), 5)
        # integer
        self.assertEqual(99**2, objective_function([99]))
        # float
        self.assertEqual(0.1**2.0, objective_function([0.1]))
        # vector
        self.assertEqual(1**2+2**2+3**2, objective_function([1, 2, 3]))
        # optima
        self.assertEqual(0, objective_function([0, 0]))

    def test_random_vector(self):
        min_max = [[1, 2], [2, 3]]

        self.assertEqual(min_max[0][0], 1)

        rv = random_vector(min_max)

        self.assertEqual(len(rv), 2)
        self.assertTrue(min_max[0][0] <= rv[0] <= min_max[0][1])
        self.assertTrue(min_max[1][0] <= rv[1] <= min_max[1][1])

    def test_create_particle(self):
        rs = create_particle([[-1, 1], [-1, 1]], [[0, 1]])
        self.assertIsNotNone(rs['position'])
        self.assertIsNotNone(rs['cost'])
        self.assertIsNotNone(rs['b_position'])
        self.assertIsNotNone(rs['b_cost'])
        self.assertIsNotNone(rs['velocity'])
        self.assertEqual(2, len(rs['position']))
        self.assertEqual(1, len(rs['velocity']))
        for x in rs['position']:
            self.assertGreaterEqual(x, -1)
            self.assertLessEqual(x, 1)

        for x in rs['velocity']:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 1)

        self.assertNotEqual(id(rs['position']), id(rs['b_position']))

    def test_get_global_best(self):
        problem_size = 2
        search_space = [[-10, 10] for i in xrange(problem_size)]
        particle = create_particle(search_space, [[-1, 1]])
        vel_space = [[-1, 1]]
        pop_size = 100
        pop = [create_particle(search_space, vel_space) for i in xrange(pop_size)]
        # test ascending order
        for i, p in enumerate(pop):
            pop[i]['cost'] = i
        gbest = get_global_best(pop, None)
        self.assertEqual(0, gbest['cost'])
        # test descending order
        for i, p in enumerate(pop):
            pop[i]['cost'] = pop_size-i-1
        gbest = get_global_best(pop, None)
        self.assertEqual(0, gbest['cost'])

    def test_update_velocity(self):
        problem_size = 1
        search_space = [[-10, 10]] * problem_size
        vel_space = [[0, 0]]
        particle = create_particle(search_space, vel_space)
        gbest = create_particle(search_space, vel_space)
        # test vel updates
        self.do_test_update_velocity(5, particle, gbest, 0, 0, 0, 0, 0)
        self.do_test_update_velocity(5, particle, gbest, 0, 5, 0, 0, 5)
        self.do_test_update_velocity(50, particle, gbest, 0, 0, -10, 10, 0)
        self.do_test_update_velocity(5, particle, gbest, -10, 10, 10, 10, 5)
        self.do_test_update_velocity(50, particle, gbest, 0, 5, -5, 10, 7.5)
        self.do_test_update_velocity(50, particle, gbest, -2.5, -5, 0, 0, -2.5)

    # Helper function for test_update_velocity
    # l_pos - local optima
    # g_pos - global optima
    # gbest - particle containing the global best
    # expected - value to be compared against for the assert
    def do_test_update_velocity(self, max_vel, particle, gbest, pos, vel, l_pos, g_pos, expected):
        sum = 0
        count = 0
        while count < 20000:
            particle['position'], particle['velocity'] = [pos], [vel]
            particle['b_position'], gbest['position'] = [l_pos], [g_pos]
            update_velocity(particle, gbest, max_vel, 1, 1)
            self.assertLessEqual(abs(particle['velocity'][0]), max_vel)
            sum += particle['velocity'][0]
            count += 1

        self.assertAlmostEqual(expected, (sum / count), delta=0.1)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def random_vector(minmax):
    import random
    return map(lambda x : x[0] + (x[1]-x[0]) * random.random(), minmax)


def initialize_weights(problem_size):
	minmax = [[-1.0, 1.0]] * (problem_size + 1)
	return random_vector(minmax)

	
def update_weights(num_inputs, weights, input, out_exp, out_act, l_rate):
	for i in xrange(0, num_inputs):
		weights[i] = weights[i] + l_rate * (out_exp - out_act) * input[i]
	weights[num_inputs] = weights[num_inputs] + l_rate * (out_exp - out_act) * 1.0

	
def activate(weights, vector):
	sum = weights[len(weights)-1] * 1.0
	for i in xrange(0, len(vector)):
		sum = sum + weights[i] * vector[i]
	return sum


def transfer(activation):
	return iif(activation >= 0, 1.0, 0.0)


def get_output(weights, vector):
	activation = activate(weights, vector)
	return transfer(activation)
	
def train_weight(weights, domain, num_inputs, iterations, lrate):
	for epoch in xrange(0, len(iterations)):
		error = 0.0
		for pattern in domain:
			input = pattern[0:num_inputs]
			output = get_output(weights, input)
			expected = pattern[-1]
			error = error + abs(output - expected)
			update_weights(num_inputs, weights, input, expected, output, lrate)
		print "> epoch=%d, error=%f" % (epoch, error)
def test_weights(weights, domain, num_inputs):


def execute(domain, num_inputs, iterations, learning_rate):
	weights = initialize_weights(num_inputs)
	train_weight(weights, domain, num_inputs, iterations, learning_rate)
	test_weights(weights, domain, num_inputs)
	return weights
	
	
def main():
	# problem configuration
	or_problem = [[0,0,0], [0,1,1], [1,0,1], [1,1,1]]
	inputs = 2
	# algorithm configuration
	iterations = 20
	learning_rate = 0.1  
	# execute the algorithm
	execute(or_problem, inputs, iterations, learning_rate)


if __name__ == "__main__":
    main()


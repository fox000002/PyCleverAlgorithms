#!/usr/bin/env python


"""
backpropagation ANN
"""


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def random_vector(min_max):
    import random
    return map(lambda x: x[0] + (x[1] - x[0]) * random.random(), min_max)


def initialize_weights(num_weights):
    import random

    min_max = [[-random.random(), random.random()]] * num_weights
    return random_vector(min_max)


def activate(weights, vector):
    sum_value = weights[-1] * 1.0
    for i in xrange(0, len(vector)):
        sum_value += weights[i] * vector[i]
    return sum_value


def transfer(activation):
    import math
    return 1.0 / (1.0 + math.exp(-activation))


def transfer_derivative(output):
    return output * (1.0 - output)


def forward_propagate(net, vector):
    for i in xrange(0, len(net)):
        layer = net[i]
        #print layer
        if i == 0:
            input_values = vector
        else:
            input_values = [net[i - 1][k]['output'] for k in xrange(0, len(net[i - 1]))]
        for neuron in layer:
            neuron['activation'] = activate(neuron['weights'], input_values)
            neuron['output'] = transfer(neuron['activation'])
    return net[-1][0]['output']


def backward_propagate_error(network, expected_output):
    #print 'backward_propagate_error'
    for n in xrange(0, len(network)):
        index = len(network) - 1 - n
        if index == len(network) - 1:
            neuron = network[index][0]  # assume one node in output layer
            error = (expected_output - neuron['output'])
            neuron['delta'] = error * transfer_derivative(neuron['output'])
        else:
            for k in xrange(0, len(network[index])):
                neuron = network[index][k]
                sum_value = 0.0
                # only sum errors weighted by connection to the current k'th neuron
                for next_neuron in network[index + 1]:
                    sum_value = sum_value + (next_neuron['weights'][k] * next_neuron['delta'])
                neuron['delta'] = sum_value * transfer_derivative(neuron['output'])
                #print 'bpe == ' + str(neuron)
                #print '--> backward_propagate_error'
                #print network


def calculate_error_derivatives_for_weights(net, vector):
    for i, layer in enumerate(net):
        if i == 0:
            input_values = vector
        else:
            input_values = [net[i - 1][k]['output'] for k in xrange(len(net[i - 1]))]
        for neuron in layer:
            for j, signal in enumerate(input_values):
                neuron['deriv'][j] += neuron['delta'] * signal
            neuron['deriv'][-1] += neuron['delta'] * 1.0


def update_weights(network, lrate, mom=0.8):
    for layer in network:
        for neuron in layer:
            for j, w in enumerate(neuron['weights']):
                delta = (lrate * neuron['deriv'][j]) + (neuron['last_delta'][j] * mom)
                neuron['weights'][j] = neuron['weights'][j] + delta
                neuron['last_delta'][j] = delta
                neuron['deriv'][j] = 0.0


def train_network(network, domain, num_inputs, iterations, lrate):
    correct = 0
    for epoch in xrange(0, iterations):
        for pattern in domain:
            vector, expected = pattern[:], pattern[-1]
            output = forward_propagate(network, vector)
            #print network
            if round(output) == expected:
                correct += 1
            backward_propagate_error(network, expected)
            calculate_error_derivatives_for_weights(network, vector)
            update_weights(network, lrate)
            if (epoch + 1) % 100 == 0:
                print "> epoch=%d, Correct=%d/%d" % (epoch + 1, correct, 100 * len(domain))
                correct = 0


def do_test_network(network, domain, num_inputs):
    correct = 0
    for pattern in domain:
        input_vector = pattern[:]
        output = forward_propagate(network, input_vector)
        if round(output) == pattern[-1]:
            correct += 1
    print "Finished test with a score of %d/%d" % (correct, len(domain))
    return correct


def create_neuron(num_inputs):
    return {
        'weights': initialize_weights(num_inputs + 1),
        'last_delta': [0.0] * (num_inputs + 1),
        'deriv': [0.0] * (num_inputs + 1)
    }


def execute(domain, num_inputs, iterations, num_nodes, lrate):
    network = []
    network.append([create_neuron(num_inputs) for i in xrange(num_nodes)])
    network.append([create_neuron(len(network[-1]) - 1)])
    print "Topology: %d " % num_inputs
    train_network(network, domain, num_inputs, iterations, lrate)
    do_test_network(network, domain, num_inputs)
    return network


def main():
    # problem configuration
    xor = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    inputs = 2
    # algorithm configuration
    learning_rate = 0.3
    num_hidden_nodes = 4
    iterations = 2000
    # execute the algorithm
    execute(xor, inputs, iterations, num_hidden_nodes, learning_rate)


if __name__ == "__main__":
    main()

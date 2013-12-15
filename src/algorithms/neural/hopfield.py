#!/usr/bin/env python

def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]

def random_vector(minmax):
    import random
    return map(lambda x : x[0] + (x[1]-x[0]) * random.random(), minmax)

def initialize_weights(problem_size):
    minmax = [[-0.5, 0.5]] * (problem_size)
    return random_vector(minmax)

def create_neuron(num_inputs):
  	neuron = {}
  	neuron['weights'] = initialize_weights(num_inputs)
  	return neuron

def transfer(activation):
	return iif(activation >= 0, 1, -1)

def propagate_was_change(neurons):
  	import random
  	i = random.randint(0, len(neurons))
  	activation = 0
  	for j in xrange(0, len(neurons)):
  		other = neurons[j]
  		if i != j:
    		activation = activation + other['weights'][i]*other['output']
  	output = transfer(activation)
  	change = (output != neurons[i]['output'])
  	neurons[i]['output'] = output
  	return change

def get_output(neurons, pattern, evals=100):
  	vector = pattern.flatten
  	neurons.each_with_index {|neuron,i| neuron['output'] = vector[i]}
  	evals.times { propagate_was_change?(neurons) }
  	return Array.new(neurons.size){|i| neurons[i]['output']}

def train_network(neurons, patters):
  	neurons.each_with_index do |neuron, i|   
    	for j in ((i+1)...neurons.size) do
      		next if i==j
      	wij = 0.0
      	patters.each do |pattern|
        vector = pattern.flatten
        wij += vector[i]*vector[j]
      neurons[i][:weights][j] = wij
      neurons[j][:weights][i] = wij

def to_binary(vector):
  	return map(lambda x : iif(x==-1, 0, 1), vector)

def print_patterns(provided, expected, actual):
  	p, e, a = to_binary(provided), to_binary(expected), to_binary(actual)
  	p1, p2, p3 = p[0:2].join(', '), p[3:5].join(', '), p[6:8].join(', ')
  	e1, e2, e3 = e[0:2].join(', '), e[3:5].join(', '), e[6:8].join(', ')
  	a1, a2, a3 = a[0:2].join(', '), a[3:5].join(', '), a[6:8].join(', ')
  	puts "Provided   Expected     Got"
  	puts "#{p1}     #{e1}      #{a1}"
  	puts "#{p2}     #{e2}      #{a2}"
  	puts "#{p3}     #{e3}      #{a3}"

def calculate_error(expected, actual):
  	sum = 0
  	for i in xrange(0, len(expected)):
  		v = expected[i]
    	if expected[i]!=actual[i]:
    		sum = sum + 1
  	return sum

def perturb_pattern(vector, num_errors=1):
  	perturbed = Array.new(vector)
  	indicies = [rand(perturbed.size)]
  	while indicies.size < num_errors:
    	index = rand(perturbed.size)
    	indicies << index if !indicies.include?(index)
  	indicies.each {|i| perturbed[i] = iif(perturbed[i]==1, -1, 1)}
  	return perturbed

def test_network(neurons, patterns):
  	error = 0.0
  	for pattern in patterns
    	vector = pattern.flatten
    perturbed = perturb_pattern(vector)
    output = get_output(neurons, perturbed)
    error = error + calculate_error(vector, output)
    print_patterns(perturbed, vector, output)
  	error = error / float(len(patterns))
  	print "Final Result: avg pattern error=#{%f}" % error
  	return error

def execute(patters, num_inputs):
  	neurons = [create_neuron(num_inputs)] * num_inputs
  	train_network(neurons, patters)
  	test_network(neurons, patters)
  	return neurons

def main():
  	# problem configuration
  	num_inputs = 9
  	p1 = [[1,1,1],[-1,1,-1],[-1,1,-1]] # T
  	p2 = [[1,-1,1],[1,-1,1],[1,1,1]] # U
  	patters = [p1, p2]  
  	# execute the algorithm
  	execute(patters, num_inputs)

if __name__ == "__main__":
    main()

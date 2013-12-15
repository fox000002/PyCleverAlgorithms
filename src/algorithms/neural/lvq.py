#!/usr/bin/env python

def main():
  	# problem configuration
  	domain = {"A"=>[[0,0.4999999],[0,0.4999999]],"B"=>[[0.5,1],[0.5,1]]}
  	# algorithm configuration
  	learning_rate = 0.3
  	iterations = 1000
  	num_vectors = 20
  	# execute the algorithm
  	execute(domain, iterations, num_vectors, learning_rate)

if __name__ == "__main__":
    main()


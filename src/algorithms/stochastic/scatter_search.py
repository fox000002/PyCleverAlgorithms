#!/usr/bin/env python

"""
"""

def main():
    #
    problem_size = 2
    search_space = [[-5,5]] * problem_size
    #
    max_iter = 100
    #
    best = search(search_space, max_iter)
    print 'Done. Best Solution: c=%f, v=%s' % (best['cost'], str(best['vector']))

if __name__ == "__main__":
    main()

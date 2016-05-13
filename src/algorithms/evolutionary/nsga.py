"""
Non-dominated Sorting Genetic Algorithm (NSGA)
"""


def objective1(v):
    return sum(map(lambda x: x ** 2, v))


def objective2(v):
    return sum(map(lambda x: (x - 1.0) ** 2, v))


def main():
    pass
    print "done!"


if __name__ == "__main__":
    main()

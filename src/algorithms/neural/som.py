#!/usr/bin/env python


def random_vector(minmax):
    import random
    return map(lambda x : x[0] + (x[1]-x[0]) * random.random(), minmax)


def main():
    pass


if __name__ == "__main__":
    main()


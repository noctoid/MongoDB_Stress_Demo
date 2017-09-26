#!/usr/local/bin/python3
from random import randrange
from goodies import timeit
def randomASCII():
    return chr(randrange(33,127))

# generate the dictionary to be inserted into database
# size = breadth * depth
# example: 1000 * 1000 = 1M
@timeit
def genDict(breadth, depth):
    return {i:[randomASCII() for j in range(depth)] for i in range(breadth)}

if __name__ == "__main__":
    # print(",".join([randomASCII() for i in range(20000)]))
    d = genDict(1000,10000)

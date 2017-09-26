#!/usr/local/bin/python3
from random import randrange
from goodies import timeit
def randomASCII():
    return chr(randrange(97,122))

# generate the dictionary to be inserted into database
# size = breadth * depth
# example: 1000 * 1000 = 1M
@timeit
def genDictTimed(key, size):
    return genDict(key, size)

def genDict(index, size):
    return {"key":index, "data":"".join([randomASCII() for j in range(size)])}

if __name__ == "__main__":
    # print(",".join([randomASCII() for i in range(20000)]))
    for i in range(100):
        print(genDict(str(i),50))

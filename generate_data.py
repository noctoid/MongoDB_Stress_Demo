#!/usr/local/bin/python3
from random import randrange
from goodies import timeit
def randomASCII():
    return chr(randrange(97,122))

@timeit
def getRandomASCIIbyLen(length):
    return "".join([randomASCII() for i in range(length)])

# generate the dictionary to be inserted into database
# size = breadth * depth
# example: 1000 * 1000 = 1M
@timeit
def genDictTimed(key, size):
    return genDict(key, size)

def genDict(index, payload):
    return {"key":index, "data":payload}

if __name__ == "__main__":
    # print(",".join([randomASCII() for i in range(20000)]))
    payload = getRandomASCIIbyLen(50)
    for i in range(10):
        print(genDict(i, payload))

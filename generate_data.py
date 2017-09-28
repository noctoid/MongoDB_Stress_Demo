#!/usr/local/bin/python3
from random import randrange
from goodies import timeit
def randomASCII():
    return chr(randrange(97,122))

def getRandomASCIIbyLen(length):
    if length < 1000:
        return "".join([randomASCII() for i in range(length)])
    else:
        return "".join([randomASCII() for i in range(1000)])*(length//1000)+("a"*(length%1000))

# generate the dictionary to be inserted into database
# size = breadth * depth
# example: 1000 * 1000 = 1M
@timeit
def genDictTimed(key, size):
    return genDict(key, size)

def genDict(index, payload):
    return {"key":index, "data":payload}

def genLongDict(index, payload, numberOfKeys):
    d = {"key": index}
    for i in range(numberOfKeys):
        d[str(i)] = payload
    return d

if __name__ == "__main__":
    # print(",".join([randomASCII() for i in range(20000)]))
    payload = getRandomASCIIbyLen(50)
    assert len(getRandomASCIIbyLen(1001)) == 1001
    long_dict = genLongDict(1, "aaaaaaaaaa", 1000)
    assert len(long_dict.keys()) == 1001
    assert type(long_dict) == type(dict())

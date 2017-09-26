#!/usr/local/bin/python3
from connector import connect, insertBatch, purge
from generate_data import genDict
from goodies import timeit, incIndex

@timeit
def doInsertTest(client, quantity, docInDict):
    result = insertBatch(client, 'stress', 'tescolle', docInDict)
    print(result)



if __name__ == "__main__":
    c = connect()
    purge(c, 'stress')
    insertBatch(c, 'stress', 'tescolle', [genDict(i, 1000) for i in range(1000)])
    c.close()

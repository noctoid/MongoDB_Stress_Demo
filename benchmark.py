#!/usr/local/bin/python3
from connector import connect, insertBatch, retrieveAll, purge
from generate_data import genDict, getRandomASCIIbyLen
from goodies import timeit, incIndex
from goodies import printWithTimestamp as tprint

@timeit
def doInsertTest(client, docInDict):
    result = insertBatch(client, 'stress', 'tescolle', docInDict)
    print(result)

@timeit
def doReadTest(client):
    tprint(len(retrieveAll(client, 'stress', 'tescolle')), " record read from the database")

@timeit
def doUpdateTest(client):
    pass

@timeit
def doDropTest(client, db):
    purge(client, db)

if __name__ == "__main__":
    c = connect()

    payload = getRandomASCIIbyLen(1000)

    doInsertTest(c, [genDict(i, payload) for i in range(1000)])

    doReadTest(c)

    # doDropTest(c, 'stress')


    c.close()

#!/usr/local/bin/python3
from connector import connect, insertBatch, retrieveAll, purge
from generate_data import genDict, getRandomASCIIbyLen
from goodies import timeit, incIndex
from goodies import printWithTimestamp as tprint

@timeit
def doInsertTest(client, docInDict):
    return insertBatch(client, 'stress', 'tescolle', docInDict)

@timeit
def doReadAllTest(client):
    tprint(len(retrieveAll(client, 'stress', 'tescolle')), " record read from the database")

@timeit
def doUpdateTest(client):
    pass

@timeit
def doDropTest(client, db):
    purge(client, db)

if __name__ == "__main__":
    # connecting to the db
    c = connect()
    payload_size = int(input("Document Size: "))
    doc_quantity = int(input("Number of Document: "))
    payload = getRandomASCIIbyLen(payload_size)
    # Database Insert Test
    result = doInsertTest(c, [genDict(i, payload) for i in range(doc_quantity)])
    # Database Reading All Collection Test
    doReadAllTest(c)
    # doDropTest(c, 'stress')
    c.close()

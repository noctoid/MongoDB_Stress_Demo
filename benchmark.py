#!/usr/local/bin/python3
from connector import connect, insertBatch, retrieveOne, retrieveAll, purge
from generate_data import genDict, getRandomASCIIbyLen
from goodies import timeit, incIndex
from goodies import printWithTimestamp as tprint
import threading

@timeit
def doInsertTest(client, docInDict):
    return insertBatch(client, 'stress', 'tescolle', docInDict)

@timeit
def doReadAllTest(client):
    tprint(len(retrieveAll(client, 'stress', 'tescolle')), " record read from the database")

@timeit
def doReadOneTest(client):
    for i in range(1000):
        retrieveOne(client, 'stress', 'tescolle', i)

@timeit
def doUpdateTest(client):
    pass

@timeit
def doDropTest(client, db):
    purge(client, db)

class multiThreadRandomRead(threading.Thread):
    def __init__(self, threadID, indexes, client, db, collection):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.indexes = indexes
        self.client = client
        self.db = db
        self.collection = collection
    @timeit
    def run(self):
        tprint("Starting "+self.name)
        # insert readone here
        result = []
        for i in self.indexes:
            result += retrieveOne(self.client, self.db, self.collection, i)
        tprint("Exiting "+self.name)
        # return result


if __name__ == "__main__":
    # connecting to the db
    c = connect()
    payload_size = int(input("Document Size: "))
    doc_quantity = int(input("Number of Document: "))
    payload = getRandomASCIIbyLen(payload_size)
    # Database Insert Test
    # result = doInsertTest(c, [genDict(i, payload) for i in range(doc_quantity)])
    # Database Reading All Collection Test
    # doReadAllTest(c)
    # for i in range(100):
    #     print(retrieveOne(c, 'stress', 'tescolle', i))
    # doDropTest(c, 'stress')
    multiReadResult = []

    # threadList = [multiThreadRandomRead(i, [x for x in range((doc_quantity//4)*(i+1))], c, 'stress', 'tescolle') for i in range(4)]
    # for i in range(4):
    #     threadList[i].start()
    # for i in range(4):
    #     threadList[i].join()

    doReadOneTest(c)
    # t1 = multiThreadRandomRead(1, [i for i in range(10)], c, 'stress', 'tescolle')
    # t2 = multiThreadRandomRead(2, [i for i in range(20)], c, 'stress', 'tescolle')
    # t3 = multiThreadRandomRead(3, [i for i in range(30)], c, 'stress', 'tescolle')
    # t1.start()
    # t2.start()
    # t3.start()
    # t1.join()
    # t2.join()
    # t3.join()
    c.close()

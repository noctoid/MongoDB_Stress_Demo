#!/usr/local/bin/python3
from connector import *
from generate_data import genDict, getRandomASCIIbyLen, genLongDict
from goodies import timeit, incIndex
from goodies import printWithTimestamp as tprint
import threading

def getStatus(c):
    databases = {db:None for db in c.database_names()}
    for k in databases.keys():
        databases[k] = c[k].collection_names()
    docs_count = {}
    for db in databases:
        if db == "admin":
            continue
        for colle in databases[db]:
            docs_count[colle] = c[db][colle].count()

    for n,k in enumerate(databases):
        print(n,":",k,"->",len(databases[k])," collection")

@timeit
def doInsertTest(client, db, colle, docInDict):
    return insertBatch(client, db, colle, docInDict)

@timeit
def doInsertOneTest(client, db, colle, d):
    return insert(client, db, colle, d)

@timeit
def doReadAllTest(client, db, colle):
    return len(retrieveAll(client, db, colle))

@timeit
def doReadOneTest(client, db, colle, condition):
    return len(retrieveOne(client, db, colle, condition))

@timeit
def doUpdateTest(client):
    pass

@timeit
def doDropTest(client, db):
    purge(client, db)

class multiThreadRandomRead(threading.Thread):
    def __init__(self, threadID, numberOfThread, client, db, collection):
        threading.Thread.__init__(self)
        self.threadID = threadID
        collection_size = getColleSize(c, 'stress', 'tescolle')
        self.istart = collection_size//numberOfThread*threadID
        self.iend = self.istart + collection_size//numberOfThread
        self.client = client
        self.db = db
        self.collection = collection
    @timeit
    def run(self):
        # insert readone here
        result = retrieveRange(self.client, self.db, self.collection, self.istart, self.iend)
        # return result

class multiCollectionInsert(threading.Thread):
    def __init__(self, threadID, client, db, d):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.db = db
        self.client = client
        self.d = d

    def run(self):
        tprint(self.threadID," loading")
        doInsertTest(self.client, self.db, "colle"+str(self.threadID), self.d)
        tprint(self.threadID," finished")



if __name__ == "__main__":
    # connecting to the db
    c = connect()
    # tprint(getColleSize(c, 'stress', 'tescolle'), " documents is in test collection.")
    # payload_size = int(input("Document Size: "))
    # doc_quantity = int(input("Number of Document: "))
    #
    doDropTest(c, "test1")
    doDropTest(c, "test2-1")
    doDropTest(c, "test2-2")
    doDropTest(c, "test2-3")
    doDropTest(c, "test2-4")
    #
    #
    # # test1
    # firstly I will create several collections. Insert different amount of docs into them
    tprint("----> Running Test1 for Insert / One Collection <----")
    # colle1 -> 1 doc, 1m lines
    tprint("=== 1 doc, 1m lines ===")
    doInsertOneTest(c, 'test1', 'colle1', genLongDict(1, "a", 1000000))
    # colle2 -> 10 doc, 100k lines
    tprint("=== 10 doc, 100k lines ===")
    doInsertTest(c, 'test1', 'colle2', [genDict(i, genLongDict(i, "a", 100000)) for i in range(10)])
    # colle3 -> 100 doc, 10k lines
    tprint("=== 100 doc, 10k lines ===")
    doInsertTest(c, 'test1', 'colle3', [genDict(i, genLongDict(i, "a", 10000)) for i in range(100)])
    # colle4 -> 1k doc, 1k lines
    tprint("=== 1k doc, 1k lines ===")
    doInsertTest(c, 'test1', 'colle4', [genDict(i, genLongDict(i, "a", 1000)) for i in range(1000)])
    # colle5 -> 10k doc, 100 lines
    tprint("=== 10k doc, 100 lines ===")
    doInsertTest(c, 'test1', 'colle5', [genDict(i, genLongDict(i, "a", 100)) for i in range(10000)])
    # colle6 -> 100k doc, 10 lines
    tprint("=== 100k doc, 10 lines ===")
    doInsertTest(c, 'test1', 'colle6', [genDict(i, genLongDict(i, "a", 10)) for i in range(100000)])
    # colle7 -> 1m doc, 1 lines
    tprint("=== 1m doc, 1 lines ===")
    doInsertTest(c, 'test1', 'colle6', [genDict(i, genLongDict(i, "a", 1)) for i in range(1000000)])

    # doDropTest(c, 'test1')
    #
    #
    #
    # Test 2
    # Also creating another db that stores docs across several collection_size
    # tprint("----> Running Test2 for Insert / Multiple Collections <----")
    # # db1 -> 100k doc, 10 lines each in 1 collections, 100k doc each colle
    # tprint(" <1m docs 10 lines each; in 1 collection, containing 1m ")
    # doInsertTest(c, 'test2-1', 'colle0', [genDict(i, genLongDict(i, "a", 10)) for i in range(1000000)])
    # # db2 -> 100k doc, 10 lines each in 10 collections, 10k doc each colle
    # tprint(" <1m docs 10 lines each; in 10 collections, containing 100k> ")
    # for i in range(10):
    #     doInsertTest(c, 'test2-2', 'colle'+str(i), [genDict(i, genLongDict(i, "a", 10)) for i in range(100000)])
    # # db3 -> 100k doc, 10 lines each in 100 collections, 1k doc each colle
    # tprint(" <1m docs 10 lines each; in 100 collections, containing 10k> ")
    # for i in range(100):
    #     doInsertTest(c, 'test2-3', 'colle'+str(i), [genDict(i, genLongDict(i, "a", 10)) for i in range(10000)])


    # Test 3
    # tprint("----> Running Test3 for Read / Entire DB <----")
    # tprint(" >>> Reading 1 doc, 1m lines <<<")
    # tprint(doReadAllTest(c, "test2-1", 'colle0'), " records read")
    #
    # tprint("----> Running Test3 for Read / Entire DB <----")
    # tprint(" >>> Reading 1 doc, 100k lines <<<")
    # tprint(doReadAllTest(c, "test2-2", 'colle0'), " records read")
    #
    # tprint("----> Running Test3 for Read / Entire DB <----")
    # tprint(" >>> Reading 1 doc, 10k lines <<<")
    # tprint(doReadAllTest(c, "test2-3", 'colle0'), " records read")

    # Test 4
    tprint("*** Running Test3 for Read / for one doc ***")
    tprint(doReadOneTest(c, "test1", "colle1", 1), " records read")

    tprint(doReadOneTest(c, "test1", "colle2", 1), " records read")

    tprint(doReadOneTest(c, "test1", "colle3", 1), " records read")

    tprint(doReadOneTest(c, "test1", "colle4", 1), " records read")

    tprint(doReadOneTest(c, "test1", "colle5", 1), " records read")

    tprint(doReadOneTest(c, "test1", "colle6", 1), " records read")

    # Test 5
    tprint("*** Running Test3 for Read / with given criteria ***")

    tprint(doReadOneTest(c, "test1", "colle1", 1), " records read")

    tprint(doReadOneTest(c, "test1", "colle2", {"$lt": 5}), " records read")

    tprint(doReadOneTest(c, "test1", "colle3", {"$lt": 50}), " records read")

    tprint(doReadOneTest(c, "test1", "colle4", {"$gt": 100, "$lt": 400}), " records read")

    tprint(doReadOneTest(c, "test1", "colle5", {"$gt": 100, "$lt": 400}), " records read")

    tprint(doReadOneTest(c, "test1", "colle6", {"$lt": 100, "$lt": 400}), " records read")




    # # Test X
    # tprint("----> Running Test 3 for Insert / Multiple Collections / Multithreading <----")
    # # db1 -> 100k doc, 10 lines each in 1 collections, 100k doc each colle
    # # doInsertTest(c, 'test3-1', 'colle0', [genDict(i, genLongDict(i, "a", 10)) for i in range(1000000)])
    # # db2 -> 100k doc, 10 lines each in 10 collections, 10k doc each colle
    # threadList = []
    # for i in range(10):
    #     threadList.append(multiCollectionInsert(i, c, "test3-2", [genDict(x*(i+1), genLongDict(x, "a", 10)) for x in range(i*100000)]))
    # # threadList = [multiCollectionInsert(tid, c, "test3-2", [genDict(i*tid, genLongDict(i*tid, "a", 10)) for i in range(100000)]) for tid in range(10)]
    # for i in range(10):
    #     threadList[i].start()
    # for i in range(10):
    #     threadList[i].join()
    # # db3 -> 100k doc, 10 lines each in 100 collections, 10k doc each colle

    getStatus(c)

    # firstly, insert data into

    # payload = getRandomASCIIbyLen(payload_size)

    # long_dict = genLongDict(1, "a", 1000000)
    # doInsertOneTest(c, 'stress', 'colle', long_dict)
    # doInsertOneTest(c, 'stress', 'colle1', {"key":1, "data":payload})

    # fs = gridfsStart(c, 'gridstress')
    # a = gridfsInsert(fs, payload, "foo")
    # readResult = gridfsRetrieveByFilename(fs, "foo")
    # for i in readResult:
    #     print(len(i.read()))



    # Database Insert Test
    # result = doInsertTest(c, 'stress', 'tescolle', [genDict(i, payload) for i in range(doc_quantity)])

    # print(retrieveOne(c, 'stress', 'tescolle', 998))
    # result = retrieveOne(c, 'stress', 'colle', 1)
    # print(type(result[0]))
    # Database Reading All Collection Test
    # doReadOneTest(c)
    # doReadAllTest(c)
    # # for i in range(100):
    # #     print(retrieveOne(c, 'stress', 'tescolle', i))
    # multiReadResult = []
    #
    # threadList = [multiThreadRandomRead(i, 8, c, 'stress', 'tescolle') for i in range(8)]
    # for i in range(8):
    #     threadList[i].start()
    # for i in range(80):
    #     threadList[i].join()

    #
    # # doReadOneTest(c)
    #
    c.close()

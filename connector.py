#!/usr/local/bin/python3

# the connector that will connect to the MongoDB instance and do all the bad stuff
from pymongo import MongoClient
import gridfs
import time
from goodies import printWithTimestamp as tprint


# Fetch the crendentials from the config file
def _fetchCredentials():
    # trying find the configuration file with server info
    try:
        with open("config.cfg") as cfg:
            server_credentials = [i.strip().split(":") for i in cfg.readlines()]
        return {server_credentials[0][0]:server_credentials[0][1], server_credentials[1][0]:server_credentials[1][1]}
    except:
        print("Config File Missing or Error, proceed with local server.")
        return {}

# Connecting to the designated database using crendentials found in config file
def connect():
    info = _fetchCredentials()
    if info:
        return MongoClient("mongodb://"+info["server"]+":"+info["port"])
    return MongoClient()
# get the collection size
def getColleSize(client, db, colle):
    return client[db][colle].count()
# will insert the dictionary passing into this func into the database
def insert(client, db, colle, d):
    cur = client[db]
    result = cur[colle].insert_one(d)
    return result

def insertBatch(client,db,colle, listOfDict):
    cur = client[db]
    result = cur[colle].insert_many(listOfDict)
    return result

def insertBin(client, db, colle, binary):
    pass

def gridfsStart(client, dbname):
    return gridfs.GridFS(client[dbname])

def gridfsInsert(fs, payload, name):
    return fs.put(bytes(payload, encoding='utf-8'), filename=name)

def gridfsRetrieveByFilename(fs, name):
    return [doc for doc in fs.find({'filename': name}, no_cursor_timeout=True)]

def update(client, d):
    pass

def retrieveOne(client, db, colle, condition):
    cur = client[db][colle].find({"key": condition})
    return [doc for doc in cur]

def retrieveRange(client, db, colle, istart, iend):
    cur = client[db][colle].find({"key": {"$lt": iend, "$gt": istart}})
    tprint(len([d for d in cur]), "documents retrieved!")
    return [doc for doc in cur]

def retrieveAll(client, db, colle):
    cur = client[db][colle].find()
    return [doc for doc in cur]
    # for document in cur:
    #     print(document)

def purge(client, db):
    client.drop_database(db)


if __name__ == "__main__":
    # connect to the local database
    c = connect()
    tprint("Connected to local instance successfully!")
    databases = {db:None for db in c.database_names()}
    for k in databases.keys():
        databases[k] = c[k].collection_names()
    for n,k in enumerate(databases):
        tprint(n,":",k,"->",databases[k])

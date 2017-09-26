#!/usr/local/bin/python3

# the connector that will connect to the MongoDB instance and do all the bad stuff
from pymongo import MongoClient
import time
from goodies import printWithTimestamp as tprint
from goodies import timeit

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

# will insert the dictionary passing into this func into the database
@timeit
def insert(client, db, colle, d):
    cur = client[db]
    result = cur[colle].insert_one(d)
    return result

@timeit
def insertBatch(client,db,colle, listOfDict):
    cur = client[db]
    result = cur[colle].insert_many(listOfDict)
    return result

def update(client, d):
    pass

def retrieveOne(client):
    pass

def retrieveAll(client, db, colle):
    cur = client[db]
    cursor = db[colle].find()
    for document in cursor:
        print(document)

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

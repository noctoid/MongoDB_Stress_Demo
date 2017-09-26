#!/usr/local/bin/python3
import connector

client = connector.connect()
db = client.insert_test_1

for i in range(59950):
    result = db.co.insert_one({"name":i})
    print(result.inserted_id)

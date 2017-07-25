import pymongo
import csv
import json
from pymongo import MongoClient



client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.towns_db
print "connected"

def insert_towns():
 #   db.towns.drop()
    f = open('towns.txt', 'rb')
    reader = csv.DictReader(f)

    for line in reader:
        l = json.loads(json.dumps(line))
        db.towns.insert_one(l)

def insert_counties():
#    db.counties.drop()
    f = open('counties_.txt', 'rb')
    reader = csv.DictReader(f)

    for line in reader:
        line['county'] = line['county'].lower()
        l = json.loads(json.dumps(line))
        db.counties.insert_one(l)

insert_counties()
insert_towns()

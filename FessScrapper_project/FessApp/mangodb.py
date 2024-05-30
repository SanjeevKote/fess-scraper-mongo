# mongodb.py

import pymongo

# MONGODB_HOST = 'scrapper-mongodb',#'mongodb://host.docker.internal:27017/' 
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scaperDatabase'

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DB]

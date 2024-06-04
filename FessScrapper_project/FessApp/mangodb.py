# mongodb.py

import pymongo

MONGODB_HOST = 'scrapper-mongodb',#'mongodb://host.docker.internal:27017/' 
# MONGODB_HOST = 'mongodb://192.168.0.103:27017'
# MONGODB_HOST = 'mongodb://localhost:27017/'
MONGODB_PORT = 27017
MONGODB_DB = 'scaperDatabase'

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DB]

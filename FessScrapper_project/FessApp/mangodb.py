# mongodb.py

import pymongo

##MONGODB_HOST = 'mongodb://host.docker.internal:27017/' #'scrapper-mongodb' # local docker
#MONGODB_HOST = 'localhost'  #local
MONGODB_HOST = 'mongodb://54.37.76.85:27017/' #server docker
MONGODB_PORT = 27017
MONGODB_DB = 'scrapperDatabase'

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DB]


# # mongodb.py
import pymongo

# MongoDB connection details
#MONGODB_HOST = 'mongodb://54.37.76.85:27017/' #server docker
MONGODB_HOST = '54.37.76.85' #server docke

# MONGODB_HOST = 'host.docker.internal' #'scrapper-mongodb' # local docker
#MONGODB_HOST = 'localhost' 
MONGODB_USERNAME = 'fess'
MONGODB_PASSWORD = 'fess'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapperDatabase'

# Construct the connection URI with the username and password
connection_uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/"

# Connect to MongoDB 
client = pymongo.MongoClient(connection_uri)
db = client[MONGODB_DB]


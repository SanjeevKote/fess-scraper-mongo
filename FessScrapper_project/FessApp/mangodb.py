# # mongodb.py
import pymongo

# MongoDB connection details
MONGODB_HOST = '57.128.39.222' #prod server docker
# MONGODB_HOST = '54.37.76.85' #test server docker
# MONGODB_HOST = 'host.docker.internal' #'scrapper-mongodb' # local docker
# MONGODB_HOST = 'localhost' 
MONGODB_USERNAME = 'chiesi-prod' #PROD
MONGODB_PASSWORD = 'Q^1JI5t_SuE21(Ss' #PROD
# MONGODB_USERNAME = 'fess' #TEST
# MONGODB_PASSWORD = 'fess' #TEST
MONGODB_PORT = 27017
MONGODB_DB = 'scrapperDatabase'

# Construct the connection URI with the username and password
connection_uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/"


# Connect to MongoDB 
client = pymongo.MongoClient(connection_uri) #PROD & TEST
# client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT) #Local

db = client[MONGODB_DB]


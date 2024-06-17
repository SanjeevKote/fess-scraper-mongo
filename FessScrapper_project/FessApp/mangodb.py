# # mongodb.py

# import pymongo

# ##MONGODB_HOST = 'mongodb://host.docker.internal:27017/' #'scrapper-mongodb' # local docker
# MONGODB_HOST = 'localhost'  #local
# # MONGODB_HOST = 'mongodb://54.37.76.85:27017/' #server docker
# MONGODB_PORT = 27017
# MONGODB_DB = 'scrapperDatabase'

# client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
# db = client[MONGODB_DB]
import pymongo
from pymongo.errors import ConnectionFailure, OperationFailure

MONGODB_USERNAME = 'fess'
MONGODB_PASSWORD = 'fess'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'your_database'

connection_uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}"

try:
    client = pymongo.MongoClient(connection_uri, serverSelectionTimeoutMS=5000)
    db = client[MONGODB_DB]
    # Attempt to connect to the server
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except (ConnectionFailure, OperationFailure) as e:
    print(f"Failed to connect to MongoDB: {e}")



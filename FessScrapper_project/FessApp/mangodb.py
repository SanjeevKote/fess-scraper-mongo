# mongodb.py

import pymongo

#MONGODB_HOST = 'mongodb://host.docker.internal:27017/' #'scrapper-mongodb'
MONGODB_HOST = 'mongodb://54.37.76.85:27017/'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapperDatabase'

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DB]
print('connected')
# import pymongo
# from pymongo import MongoClient 
  
# # creation of MongoClient 
# client=MongoClient() 
  
# # Connect with the portnumber and host 
# client = MongoClient("localhost",27017) 
  
# # Access database 
# mydatabase = client.notes_crud_app
  
# # Access collection of the database 
# db=mydatabase.scaperDatabase
# print('connected')

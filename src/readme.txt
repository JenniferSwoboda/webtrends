Start Mongo:
mongod -dbpath .

sudo mongod --repair


Py Shell
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

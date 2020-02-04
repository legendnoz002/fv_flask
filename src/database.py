import pymongo
from flask import jsonify
class DB():
    URI = "mongodb://admin:admin123@ds211269.mlab.com:11269/face_vertification?retryWrites=false"
    
    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['face_vertification']
        
    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert(data)

    @staticmethod
    def findOne(collection, data):
        return DB.DATABASE[collection].find_one({"username":data['username']})
        